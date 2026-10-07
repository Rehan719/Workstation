"""
QEP — Quran Education Platform HTTP Surface

Mounts the existing religious_domain engines as proper FastAPI endpoints.
All Quran text comes from external authoritative APIs only — NEVER AI-generated.

IMMOVABLE CONSTRAINTS (from WORKSTATION_CONSTITUTION.md):
  - Never AI-generate Arabic Quran text
  - Source ONLY from quran.com / alquran.cloud / tanzil.net
  - Human review required for recitation scoring — AI assists only
  - All AI-generated content clearly labelled as AI-assisted

  GET  /api/v1/qep/suwar              — list all surahs (from alquran.cloud)
  GET  /api/v1/qep/surah/{number}     — get surah text (from alquran.cloud)
  GET  /api/v1/qep/ayah/{surah}/{ayah} — get single ayah
  POST /api/v1/qep/hifz/schedule      — generate SM-2 memorisation schedule
  POST /api/v1/qep/hifz/review        — record a review session, get next interval
  GET  /api/v1/qep/hifz/progress/{uid} — get memorisation progress matrix
  POST /api/v1/qep/tajweed/analyse    — WRITTEN-recall comparison (text only; never recitation)
  POST /api/v1/qep/tajweed/lesson     — AI-generated tajweed lesson plan (labelled)
  GET  /api/v1/qep/gamification/{uid} — get learner gamification state
  POST /api/v1/qep/gamification/award — award XP for a learning achievement
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from agentic_core.config import data_path
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agentic_core.config import atomic_write_json, store_lock

from agentic_core.ai.gateway import gateway
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.religious_domain.tajwid.coach import TajwidCoach

router = APIRouter(prefix="/api/v1/qep", tags=["qep"])

_hifz_engine = MemorizationEngine()
_tajweed_coach = TajwidCoach()
# W439 — GamifiedLearning is NOT constructed here any more: its award path requires a middleware
# that does not exist, and the methods this file used to probe for never existed either (which is
# how every award fell to a fallback claiming "recorded" while persisting nothing). The persisted
# award store below is the real implementation.

_QURAN_API = "https://api.alquran.cloud/v1"

# W439 audit catch (HIGH): uid was interpolated into store paths unvalidated — a body uid of
# "../../organism_config" resolved OUTSIDE the store and atomic_write_json would clobber
# governance files. One choke point covers every uid-taking route.
_UID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def _safe_uid(uid: str) -> str:
    if not _UID_RE.fullmatch(uid or ""):
        raise HTTPException(status_code=400,
                            detail="uid must match [A-Za-z0-9_-]{1,64} — path segments are refused")
    return uid


# The Qur'an's per-surah ayah counts — fixed facts of the text (Hafs numbering), used to refuse
# schedules/reviews for ayaat that do not exist. A "memorised" claim about an ayah outside the
# Qur'an would be a claim about scripture that exceeds reality.
_AYAH_COUNTS = [0, 7, 286, 200, 176, 120, 165, 206, 75, 129, 109, 123, 111, 43, 52, 99, 128, 111,
                110, 98, 135, 112, 78, 118, 64, 77, 227, 93, 88, 69, 60, 34, 30, 73, 54, 45, 83,
                182, 88, 75, 85, 54, 53, 89, 59, 37, 35, 38, 29, 18, 45, 60, 49, 62, 55, 78, 96,
                29, 22, 24, 13, 14, 11, 11, 18, 12, 12, 30, 52, 52, 44, 28, 28, 20, 56, 40, 31,
                50, 40, 46, 42, 29, 19, 36, 25, 22, 17, 19, 26, 30, 20, 15, 21, 11, 8, 8, 19, 5,
                8, 8, 11, 11, 8, 3, 9, 5, 4, 7, 3, 6, 3, 5, 4, 5, 6]

# Immutable-text cache — the Qur'an does not change; availability of sacred text must not depend
# on a third party per request (offline serves from cache, source honestly labelled cached)
_QURAN_CACHE = data_path("quran_cache")
_QURAN_CACHE.mkdir(parents=True, exist_ok=True)


def _cache_read(name: str):
    p = _QURAN_CACHE / f"{name}.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _cache_write(name: str, data) -> None:
    try:
        p = _QURAN_CACHE / f"{name}.json"
        with store_lock(p):
            atomic_write_json(p, {"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                  "data": data})
    except Exception:
        pass
# W439 — `edition` used to be forwarded verbatim to the external API; only known text editions of
# the authoritative source are accepted (never a translation edition here: Arabic text routes
# serve the Arabic text, and translations go through the labelled AI route)
_ALLOWED_EDITIONS = {"quran-uthmani", "quran-simple", "quran-simple-enhanced", "quran-tajweed"}

#  R8 + R11 (Owner ruling 2026-10-05b) — WHAT EACH EDITION IS, AND UNDER WHAT LICENCE. These routes
#  returned only `source: "alquran.cloud"`, so a reader could not tell which edition they were reading nor
#  which riwayah transmits it - and that is the difference a declaration exists to make.
#
#  THE PLATFORM DECLARES, IT DOES NOT CHOOSE. The ruling is that which edition is authoritative is not
#  the platform's to decide, so every value here is a fact about the FETCH: the identifier requested of
#  alquran.cloud, the script it serves, and the riwayah that identifier carries. An edition whose riwayah
#  is not established here reads NOT DECLARED rather than being assigned one, because guessing a riwayah
#  would be the scholarly claim the ruling forbids.
_EDITION_PROVENANCE: dict[str, dict] = {
    "quran-uthmani": {"script": "Uthmani", "riwayah": "Hafs an Asim"},
    "quran-simple": {"script": "simplified", "riwayah": "Hafs an Asim"},
    "quran-simple-enhanced": {"script": "simplified (enhanced)", "riwayah": "Hafs an Asim"},
    #  the tajweed-annotated edition carries colour-coding markup over the same transmission
    "quran-tajweed": {"script": "Uthmani with tajwid annotation", "riwayah": "Hafs an Asim"},
}
_CORPUS_LICENCE = ("served by alquran.cloud, which publishes the Qur'anic text for free use; the Arabic "
                   "is FETCHED from that source and never generated by this platform (§11)")


def _corpus_provenance(edition: str) -> dict:
    """R8's three fields for one fetched item, with an undeclared riwayah SAID rather than filled in."""
    known = _EDITION_PROVENANCE.get(edition)
    return {
        "source": "alquran.cloud",
        "edition": edition,
        "script": (known or {}).get("script"),
        "riwayah": (known or {}).get("riwayah"),
        "licence": _CORPUS_LICENCE,
        "provenance_basis": (
            (f"edition {edition!r} as served by alquran.cloud, transmitted in the "
             f"{(known or {}).get('riwayah')} riwayah. This platform RECORDS which edition it fetched; "
             f"it does not rule on which edition or riwayah is authoritative - that belongs to "
             f"qualified scholarship.")
            if known else
            (f"edition {edition!r} is fetched from alquran.cloud, and the riwayah it transmits is NOT "
             f"DECLARED here. It is reported as unknown rather than assigned one, because naming a "
             f"riwayah this platform has not established would be a scholarly claim it may not make.")),
    }
_HIFZ_STORE = data_path("hifz_progress")
_HIFZ_STORE.mkdir(parents=True, exist_ok=True)

_SURAH_NAMES_CACHE: dict[int, str] = {}  # loaded lazily


def _hifz_path(uid: str) -> Path:
    return _HIFZ_STORE / f"{_safe_uid(uid)}.json"


def _fresh_hifz(uid: str) -> dict:
    return {
        "uid": uid,
        "sessions": [],
        "cards": {},  # {ayah_ref: {repetitions, interval, efactor, next_review_date}}
        "total_ayaat_memorised": 0,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _load_hifz(uid: str) -> dict:
    p = _hifz_path(uid)
    if not p.exists():
        return _fresh_hifz(uid)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        # refuter catch, round 2: a PARSEABLE but wrong-shape record ({}, [], null) sailed past the
        # JSONDecodeError net and 500'd every hifz route forever — the same symptom, different shape
        if isinstance(data, dict) and isinstance(data.get("cards", {}), dict) \
                and isinstance(data.get("sessions", []), list):
            data.setdefault("cards", {})
            data.setdefault("sessions", [])
            data.setdefault("total_ayaat_memorised", 0)
            return data
    except (json.JSONDecodeError, OSError):
        pass
    # W439 audit catch: NEVER delete or silently zero a learner's memorisation record — quarantine
    # it aside for recovery. Refuter catch, round 2: the rename used a same-second suffix that
    # could collide (FileExistsError is an OSError) and the note then CLAIMED preservation after a
    # swallowed failure — the note now tells the truth either way.
    import uuid as _uuid
    preserved = False
    try:
        p.rename(p.with_name(f"{p.stem}.corrupt-{_uuid.uuid4().hex[:8]}.json"))
        preserved = True
    except OSError:
        pass
    fresh = _fresh_hifz(uid)
    fresh["store_note"] = (("previous record was unreadable and has been preserved aside as "
                            "*.corrupt-* for recovery — this is a fresh record, not your history")
                           if preserved else
                           ("previous record was unreadable and COULD NOT be preserved aside "
                            "(rename failed) — a fresh record was started; the original may be "
                            "overwritten on the next save"))
    return fresh


def _save_hifz(uid: str, data: dict) -> None:
    atomic_write_json(_hifz_path(uid), data)   # W439: store convention — no torn reads


# ── Gamification store (W439) ─────────────────────────────────────────────────
# The old surface was FABRICATED SUCCESS end to end: GamifiedLearning lacks the methods api.py
# probed for (get_learner_state / award_achievement do not exist), so every award fell to a
# fallback dict claiming "Achievement recorded" while persisting NOTHING, and every state read
# returned zeros forever. On a learning platform that is a lie to a learner about their own
# effort. Awards now persist; every derived figure carries its basis.
_GAMI_STORE = data_path("qep_gamification")
_GAMI_STORE.mkdir(parents=True, exist_ok=True)

_XP_PER_LEVEL = 100


def _gami_path(uid: str) -> Path:
    return _GAMI_STORE / f"{_safe_uid(uid)}.json"


def _load_gami(uid: str) -> dict:
    p = _gami_path(uid)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            # quarantine, never silently overwrite a learner's earned record (W439 audit catch;
            # round 2: unique target name — a same-second rename collision is an OSError too)
            import uuid as _uuid
            try:
                p.rename(p.with_name(f"{p.stem}.corrupt-{_uuid.uuid4().hex[:8]}.json"))
            except OSError:
                pass
    return {"uid": uid, "xp": 0, "achievements": [], "award_days": [], "history": [],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def _streak_days(award_days: list) -> int:
    # Consecutive UTC days with at least one award, ending today or yesterday (a streak survives
    # until a full day is missed).
    import datetime as _dt
    days = set(award_days)
    day = _dt.datetime.now(_dt.timezone.utc).date()
    if day.isoformat() not in days:
        day = day - _dt.timedelta(days=1)
    streak = 0
    while day.isoformat() in days:
        streak += 1
        day = day - _dt.timedelta(days=1)
    return streak


def _gami_state(g: dict) -> dict:
    xp = int(g.get("xp", 0))
    return {
        "uid": g["uid"],
        "xp": xp,
        "level": 1 + xp // _XP_PER_LEVEL,
        "level_basis": f"1 + xp // {_XP_PER_LEVEL}",
        "achievements": g.get("achievements", []),
        "streak_days": _streak_days(g.get("award_days", [])),
        "streak_basis": "consecutive UTC days with >= 1 recorded award, ending today or yesterday",
        "awards_recorded": len(g.get("history", [])),
        "scope": "recorded awards only — nothing here is estimated",
    }


def _award(uid: str, achievement: str, xp: int, source: str) -> dict:
    with store_lock(_gami_path(uid)):
        g = _load_gami(uid)
        g["xp"] = int(g.get("xp", 0)) + xp
        if achievement not in g.get("achievements", []):
            g.setdefault("achievements", []).append(achievement)
        today = time.strftime("%Y-%m-%d", time.gmtime())   # UTC — the streak_basis says UTC
        if today not in g.setdefault("award_days", []):
            g["award_days"].append(today)
        g.setdefault("history", []).append(
            {"achievement": achievement, "xp": xp, "source": source,
             "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        g["history"] = g["history"][-500:]
        atomic_write_json(_gami_path(uid), g)
    return _gami_state(g)


# ── Sourced-text normalisation (W483, ledger v5 R1.2) ────────────────────────
# The quran-uthmani edition PREPENDS the Basmala to ayah 1 of every surah except 1 and 9, and puts a
# U+FEFF at the head of 1:1. Passed through unchanged, 112 surahs showed a first ayah that is not the
# text of that ayah under Hafs numbering — under a label reading "authentic … not AI-generated". The
# label was true; the boundary was not.
#
# The prefix is never written here. Scripture is never typed into this repository (§11.2): the
# reference text for the prefix IS ayah 1:1, fetched from the same authoritative source and compared
# skeleton-to-skeleton (diacritics, tatweel and whitespace removed — a mechanical Unicode operation,
# not a reading). When 1:1 cannot be sourced, NOTHING is stripped and the response says so: a
# boundary this code cannot verify is never asserted.
_BOM = "﻿"
_TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ࣓-ࣿـ]")


def _skeleton(text: str) -> str:
    """The consonantal skeleton: no BOM, no diacritics/tatweel, no whitespace. Comparison only."""
    return re.sub(r"\s+", "", _TASHKEEL.sub("", (text or "").replace(_BOM, "")))


async def _basmala_prefix(edition: str = "quran-uthmani") -> str | None:
    """The Basmala as the SOURCE gives it — ayah 1:1 in this edition. Cache-first; never generated,
    never typed. Returns None when the source is unreachable and nothing is cached."""
    key = f"ayah_{edition}_1_1_basmala_ref"
    cached = _cache_read(key)
    if cached:
        return ((cached.get("data") or {}).get("data") or {}).get("text")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{_QURAN_API}/ayah/1:1/{edition}")
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return None
    _cache_write(key, data)
    return (data.get("data") or {}).get("text")


def basmala_is_prepended(surah: int, ayah: int) -> bool:
    """Where the edition prepends the Basmala: ayah 1 of every surah but al-Fatiha (it IS 1:1 there)
    and at-Tawba (which has none)."""
    return ayah == 1 and surah not in (1, 9)


async def normalise_ayah_text(text: str, surah: int, ayah: int,
                              edition: str = "quran-uthmani") -> tuple[str, dict]:
    """Return (text of THIS ayah, a note saying what was done and on what evidence).

    The note is part of the answer, not decoration: `basmala_separated` is True only when the prefix
    was sourced AND matched, False when it was sourced and did not match, and None when the prefix
    could not be sourced at all — in which case the text is returned untouched apart from the BOM and
    the note says the boundary was not checked.
    """
    out = (text or "").replace(_BOM, "").strip()
    if not basmala_is_prepended(surah, ayah):
        return out, {"basmala_separated": False,
                     "basmala_basis": ("this ayah carries no prepended Basmala in this edition "
                                       + ("(surah 1: the Basmala is ayah 1 itself)" if surah == 1 else
                                          "(surah 9 has no Basmala)" if surah == 9 else
                                          "(the edition prepends it to ayah 1 only)"))}
    prefix = await _basmala_prefix(edition)
    if not prefix:
        return out, {"basmala_separated": None, "basmala": None,
                     "basmala_basis": ("not checked — the reference text for the prefix (ayah 1:1) could "
                                       "not be sourced, so no boundary is asserted and nothing was removed")}
    skel_p = _skeleton(prefix)
    if skel_p and _skeleton(out).startswith(skel_p):
        # Cut at the character that completes the prefix's skeleton — the cut is located by counting
        # skeleton characters, never by matching a literal.
        # W483 (refutation) — the cut must land on a CHARACTER boundary, not a skeleton boundary. It
        # used to stop at `i + 1`, immediately after the base letter that completed the prefix, which
        # left that letter's own vowel marks at the head of the ayah: the Basmala lost its final
        # vowel and the ayah began with an orphaned diacritic. Both halves would then be wrong, in
        # sacred text. The cut is advanced past every combining mark and any tatweel that belongs to
        # the completing letter, so the prefix keeps its marks and the ayah starts at a real letter.
        seen, cut = 0, len(out)
        for i, ch in enumerate(out):
            if _skeleton(ch):
                seen += 1
                if seen == len(skel_p):
                    cut = i + 1
                    while cut < len(out) and not _skeleton(out[cut]) and not out[cut].isspace():
                        cut += 1          # carry the completing letter's diacritics with the prefix
                    break
        head, body = out[:cut].strip(), out[cut:].strip()
        if body:
            return body, {"basmala_separated": True, "basmala": head,
                          "basmala_basis": ("the edition prepends the Basmala to ayah 1; it is shown "
                                            "separately and is not part of ayah 1 under Hafs numbering. "
                                            "Matched against the sourced text of ayah 1:1.")}
        return out, {"basmala_separated": False, "basmala": None,
                     "basmala_basis": ("the prefix matched the whole of this ayah's text, which cannot be "
                                       "right — nothing was removed")}
    return out, {"basmala_separated": False, "basmala": None,
                 "basmala_basis": ("the sourced text of ayah 1:1 is not a prefix of this ayah in this "
                                   "edition — nothing was removed")}


async def fetch_ayah_arabic(surah: int, ayah: int) -> str | None:
    """Sourced Arabic text of one ayah (cache-first) — for callers that must inject AUTHENTIC text
    into prompts instead of letting a model generate Quranic Arabic (the constitutional rule).
    Returns None when the source is unreachable and no cache exists; NEVER generates."""
    if not (1 <= surah <= 114 and 1 <= ayah <= _AYAH_COUNTS[surah]):
        return None
    key = f"ayah_{surah}_{ayah}_quran-uthmani"
    cached = _cache_read(key)
    if cached:
        raw = (cached["data"].get("data") or {}).get("text")
    else:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{_QURAN_API}/ayah/{surah}:{ayah}/quran-uthmani")
                resp.raise_for_status()
                data = resp.json()
        except Exception:
            return None
        _cache_write(key, data)
        raw = (data.get("data") or {}).get("text")
    if not raw:
        return raw
    # W483 (R1.2) — the text injected into a prompt must be the text of THIS ayah: the edition's
    # prepended Basmala is separated off (and the BOM removed) before the text travels anywhere.
    text, _note = await normalise_ayah_text(raw, surah, ayah)
    return text


# ── Quran Text (alquran.cloud) ────────────────────────────────────────────────

@router.get("/suwar")
async def list_suwar():
    """List all 114 surahs with name and ayah count. Source: alquran.cloud"""
    cached = _cache_read("suwar_index")
    if cached:
        data, fetched_at = cached["data"], cached["fetched_at"]
    else:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{_QURAN_API}/surah")
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")
        _cache_write("suwar_index", data)
        fetched_at = None

    suwar = [
        {
            "number": s["number"],
            "name_arabic": s["name"],
            "name_transliteration": s["englishName"],
            "name_english": s["englishNameTranslation"],
            "ayah_count": s["numberOfAyahs"],
            "revelation_type": s.get("revelationType", ""),
        }
        for s in data.get("data", [])
    ]
    return {"suwar": suwar, "total": len(suwar),
            "source": ("alquran.cloud" if fetched_at is None else
                       f"alquran.cloud (cached {fetched_at})")}


@router.get("/surah/{number}")
async def get_surah(number: int, edition: str = "quran-uthmani"):
    """Get complete surah text. number: 1-114. Source: alquran.cloud — NOT AI-generated."""
    if not 1 <= number <= 114:
        raise HTTPException(status_code=400, detail="Surah number must be 1-114.")
    if edition not in _ALLOWED_EDITIONS:
        raise HTTPException(status_code=422, detail=f"edition must be one of {sorted(_ALLOWED_EDITIONS)}")
    cached = _cache_read(f"surah_{number}_{edition}")
    if cached:
        data, fetched_at = cached["data"], cached["fetched_at"]
    else:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(f"{_QURAN_API}/surah/{number}/{edition}")
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")
        _cache_write(f"surah_{number}_{edition}", data)
        fetched_at = None

    surah_data = data.get("data", {})
    # W483 (R1.2) — ayah 1 carries the edition's prepended Basmala; it is separated off so the ayah
    # shown is the ayah, with the Basmala returned beside it and labelled.
    ayaat = []
    basmala = None
    basmala_basis = None
    for a in surah_data.get("ayahs", []):
        _t, _n = await normalise_ayah_text(a["text"], number, a["numberInSurah"], edition)
        if a["numberInSurah"] == 1:
            basmala, basmala_basis = _n.get("basmala"), _n.get("basmala_basis")
        ayaat.append({"number_in_surah": a["numberInSurah"], "text_arabic": _t})
    return {
        "basmala": basmala,
        "basmala_note": ("shown separately — the edition prepends it to ayah 1; it is not part of "
                         "ayah 1 under Hafs numbering" if basmala else basmala_basis),
        "surah_number": number,
        "name_arabic": surah_data.get("name", ""),
        "name_english": surah_data.get("englishNameTranslation", ""),
        "ayah_count": len(ayaat),
        "ayaat": ayaat,
        #  R8 — the licence, edition and riwayah travel with the text here too. This carried `edition`
        #  and a cache-aware `source` but no riwayah and no licence, so a reader could not tell which
        #  transmission they had. The provenance is spread FIRST so this route's own cache-aware
        #  `source` still wins - losing the cache stamp to gain a licence would be a poor trade.
        **_corpus_provenance(edition),
        "source": ("alquran.cloud" if fetched_at is None else
                   f"alquran.cloud (cached {fetched_at})"),
        "note": "Authentic Arabic text sourced from alquran.cloud — not AI-generated.",
    }


@router.get("/ayah/{surah_number}/{ayah_number}")
async def get_ayah(surah_number: int, ayah_number: int, edition: str = "quran-uthmani"):
    """Get a single ayah. Source: alquran.cloud."""
    if not 1 <= surah_number <= 114:
        raise HTTPException(status_code=400, detail="Surah number must be 1-114.")
    # refuter catch: an out-of-bounds ayah used to hit the upstream 404 and come back rebranded
    # "503 Quran API unavailable" — a false cause statement about scripture bounds
    if not 1 <= ayah_number <= _AYAH_COUNTS[surah_number]:
        raise HTTPException(status_code=422,
                            detail=f"surah {surah_number} has {_AYAH_COUNTS[surah_number]} ayaat — "
                                   f"ayah {ayah_number} does not exist")
    if edition not in _ALLOWED_EDITIONS:
        raise HTTPException(status_code=422, detail=f"edition must be one of {sorted(_ALLOWED_EDITIONS)}")
    ref = f"{surah_number}:{ayah_number}"
    cached = _cache_read(f"ayah_full_{surah_number}_{ayah_number}_{edition}")
    if cached:
        data = cached["data"]
    else:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{_QURAN_API}/ayah/{ref}/{edition}")
                resp.raise_for_status()
                data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")
        _cache_write(f"ayah_full_{surah_number}_{ayah_number}_{edition}", data)

    ayah = data.get("data", {})
    # W483 (R1.2) — see normalise_ayah_text: the prepended Basmala is not part of this ayah.
    _text, _note = await normalise_ayah_text(ayah.get("text", ""), surah_number, ayah_number, edition)
    return {
        "ref": ref,
        "text_arabic": _text,
        **({"basmala": _note["basmala"]} if _note.get("basmala") else {}),
        "basmala_separated": _note.get("basmala_separated"),
        "basmala_basis": _note.get("basmala_basis"),
        "surah_name": ayah.get("surah", {}).get("name", ""),
        "juz": ayah.get("juz", 0),
        "page": ayah.get("page", 0),
        #  R8 — the licence, the canonical edition and the riwayah travel WITH the text. This returned
        #  `source: "alquran.cloud"` alone, so a reader could not tell which edition they had.
        **_corpus_provenance(edition),
    }


# ── Hifz (Memorisation) — SM-2 ────────────────────────────────────────────────

class HifzScheduleRequest(BaseModel):
    uid: str
    surah_number: int
    ayaat_range: list[int]  # [start, end] — ayah numbers to memorise


@router.post("/hifz/schedule")
async def hifz_schedule(req: HifzScheduleRequest):
    """Generate SM-2 memorisation schedule for a range of ayaat."""
    if not 1 <= req.surah_number <= 114:
        raise HTTPException(status_code=400, detail="Invalid surah number.")
    if len(req.ayaat_range) != 2 or req.ayaat_range[0] > req.ayaat_range[1]:
        raise HTTPException(status_code=400, detail="ayaat_range must be [start, end].")

    # W439 audit catch: the range was unbounded (a [1, 10^8] request looped 10^8 card builds) and
    # unvalidated against the surah's REAL ayah count — scheduling "ayah 114:300" minted a card for
    # scripture that does not exist, and a review could then count it "memorised".
    max_ayah = _AYAH_COUNTS[req.surah_number]
    if req.ayaat_range[0] < 1 or req.ayaat_range[1] > max_ayah:
        raise HTTPException(status_code=422,
                            detail=f"surah {req.surah_number} has {max_ayah} ayaat — "
                                   f"range must lie within [1, {max_ayah}]")

    with store_lock(_hifz_path(req.uid)):
        hifz = _load_hifz(req.uid)
        schedule = []
        today = time.strftime("%Y-%m-%d")

        for ayah_num in range(req.ayaat_range[0], req.ayaat_range[1] + 1):
            ref = f"{req.surah_number}:{ayah_num}"
            if ref not in hifz["cards"]:
                hifz["cards"][ref] = {
                    "repetitions": 0,
                    "interval": 1,
                    "efactor": 2.5,
                    "next_review_date": today,
                    "added_at": today,
                }
            card = hifz["cards"][ref]
            schedule.append({
                "ref": ref,
                "next_review_date": card["next_review_date"],
                "interval_days": card["interval"],
                "repetitions": card["repetitions"],
            })

        _save_hifz(req.uid, hifz)
    return {
        "uid": req.uid,
        "surah_number": req.surah_number,
        "ayaat_scheduled": len(schedule),
        "schedule": schedule,
    }


class HifzReviewRequest(BaseModel):
    uid: str
    ayah_ref: str      # "2:255"
    quality: int       # 0-5 (SM-2 quality: 0=total blackout, 5=perfect)


@router.post("/hifz/review")
async def hifz_review(req: HifzReviewRequest):
    """Record a review session. Updates SM-2 interval for the ayah."""
    if not 0 <= req.quality <= 5:
        raise HTTPException(status_code=400, detail="Quality must be 0-5.")

    # W439 audit catch: any ref string used to mint a card on demand — "1:299" (al-Fatiha has 7
    # ayaat) could be reviewed and counted "memorised"
    m = re.fullmatch(r"(\d{1,3}):(\d{1,3})", req.ayah_ref or "")
    if not m or not (1 <= int(m.group(1)) <= 114) or not (1 <= int(m.group(2)) <= _AYAH_COUNTS[int(m.group(1))]):
        raise HTTPException(status_code=422,
                            detail=f"ayah_ref {req.ayah_ref!r} does not name an ayah of the Qur'an")

    # locked read-modify-write (the manual __enter__/__exit__ first version leaked the lock on
    # any exception between them); the XP award below takes its OWN lock, outside this one
    with store_lock(_hifz_path(req.uid)):
        hifz = _load_hifz(req.uid)
        card = hifz["cards"].get(req.ayah_ref, {
            "repetitions": 0, "interval": 1, "efactor": 2.5,
            "next_review_date": time.strftime("%Y-%m-%d"),
        })

        new_interval, new_efactor = _hifz_engine.calculate_next_review(
            quality=req.quality,
            repetitions=card["repetitions"],
            previous_interval=card["interval"],
            previous_efactor=card["efactor"],
        )

        # Update card
        card["repetitions"] = card["repetitions"] + 1 if req.quality >= 3 else 0
        card["interval"] = new_interval
        card["efactor"] = round(new_efactor, 3)

        import datetime
        next_date = (datetime.date.today() + datetime.timedelta(days=new_interval)).isoformat()
        card["next_review_date"] = next_date
        card["last_reviewed"] = time.strftime("%Y-%m-%d")

        hifz["cards"][req.ayah_ref] = card
        hifz["sessions"].append({
            "ayah_ref": req.ayah_ref,
            "quality": req.quality,
            "reviewed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "next_review_date": next_date,
        })
        hifz["sessions"] = hifz["sessions"][-200:]  # keep last 200

        if req.quality >= 3:
            hifz["total_ayaat_memorised"] = len([
                r for r, c in hifz["cards"].items() if c.get("repetitions", 0) >= 1
            ])

        _save_hifz(req.uid, hifz)

    # W439 — a real review is a real achievement: quality >= 3 earns XP in the persisted
    # gamification store (source disclosed), closing the loop the old fallback only pretended to
    gami = None
    if req.quality >= 3:
        gami = _award(req.uid, "ayah_review", 5, source="hifz_review")

    return {
        "uid": req.uid,
        "ayah_ref": req.ayah_ref,
        "quality": req.quality,
        "new_interval_days": new_interval,
        "new_efactor": round(new_efactor, 3),
        "next_review_date": next_date,
        "total_ayaat_memorised": hifz["total_ayaat_memorised"],
        "memorised_basis": ("ayaat with at least one successful (quality>=3) review — a review "
                            "count, not a hifz certification"),
        "xp_awarded": 5 if gami else 0,
        "gamification": gami,
    }


@router.get("/hifz/progress/{uid}")
async def hifz_progress(uid: str):
    """Get full memorisation progress for a user."""
    hifz = _load_hifz(uid)
    today = time.strftime("%Y-%m-%d")
    due_today = [ref for ref, c in hifz["cards"].items() if c.get("next_review_date", "") <= today]

    return {
        "uid": uid,
        "total_ayaat_in_schedule": len(hifz["cards"]),
        "total_ayaat_memorised": hifz.get("total_ayaat_memorised", 0),
        "memorised_basis": ("ayaat with at least one successful (quality>=3) review — a review "
                            "count, not a hifz certification"),
        "due_today": len(due_today),
        "due_refs": due_today[:20],
        "due_refs_capped_at": 20,   # due_today is the FULL count; this list shows the first 20
        "total_sessions": len(hifz.get("sessions", [])),
        "last_session": hifz["sessions"][-1] if hifz.get("sessions") else None,
        "progress_matrix": hifz.get("cards", {}),
    }


# ── Tajweed ───────────────────────────────────────────────────────────────────

class WrittenRecallRequest(BaseModel):
    # max_length (refuter catch): the O(n*m) Levenshtein ran unbounded on the event loop — a 40k-char
    # body blocked every route for minutes. The longest ayah (2:282) is ~1.1k chars; 1500 bounds the
    # comparison at ~2.25M cells, and the compare runs in a worker thread besides.
    ayah_text: str = Field(max_length=1500)     # Arabic text from the authoritative source
    recited_text: str = Field(max_length=1500)  # the learner's TYPED Arabic recollection


@router.post("/tajweed/analyse")
async def tajweed_analyse(req: WrittenRecallRequest):
    """Written-recall check — compares the learner's TYPED Arabic against the authoritative text.

    W439 — this endpoint used to feed English "recitation notes" (or a default English sentence)
    into a Levenshtein against the Arabic ayah and return the garbage ratio as recitation
    "accuracy" with a hardcoded confidence of 0.95 and a "makharij" verdict — a fabricated
    judgement about a recitation nobody heard (the W403 "false witness" class, on the backend).
    What a text engine can honestly do, it now does, and it says exactly what it is NOT:
    no claim about pronunciation, recitation, or articulation is made anywhere in the payload."""
    from fastapi.concurrency import run_in_threadpool
    comparison = await run_in_threadpool(
        _tajweed_coach.compare_written_recall, req.ayah_text, req.recited_text)
    return {
        "comparison": comparison,
        "ayah_text": req.ayah_text[:200],
        "kind": "written_recall_check",
        "disclaimer": ("Compares WRITTEN text only — it says nothing about your recitation or "
                       "pronunciation. Recitation assessment requires a qualified teacher "
                       "(no phonetic model is provisioned)."),
    }


class TajweedLessonRequest(BaseModel):
    rule_name: str        # e.g. "idgham", "ikhfa", "madd al-lazim"
    level: str = "beginner"  # beginner | intermediate | advanced


@router.post("/tajweed/lesson")
async def tajweed_lesson(req: TajweedLessonRequest):
    """
    Generate a tajweed lesson plan. Clearly labelled as AI-assisted educational content.
    """
    prompt = (
        f"You are an educational assistant supporting tajweed learning. "
        f"Generate a structured lesson plan for the tajweed rule: {req.rule_name}\n"
        f"Level: {req.level}\n\n"
        f"Include:\n"
        f"1. Rule definition and Arabic name\n"
        f"2. When the rule applies (triggers)\n"
        f"3. Pronunciation guide\n"
        f"4. 3 example words with transliteration\n"
        f"5. Common mistakes to avoid\n"
        f"6. Practice exercises\n\n"
        f"IMPORTANT: This is educational support only. Learners should verify with a qualified teacher (Shaykh/Ustadha)."
    )
    # W439 — provenance travels with faith content: gateway.query dropped served_by, so a
    # deterministic-floor scaffold could be presented as a lesson with nothing telling the learner
    meta = await gateway.query_meta(prompt, agent="tajweed_lesson", augment=False)
    lesson = meta.get("output") or ""
    served_by = meta.get("served_by", "native")
    floor_served = served_by == "native"

    #  R7 (Owner ruling 2026-10-05b, A.12.3) — A NAMED HUMAN SCHOLAR APPROVES THIS BEFORE A LEARNER SEES
    #  IT. §11 requires the audit and a disclaimer is not a review, so an unreviewed lesson is WITHHELD
    #  rather than shown with a caveat. The composition still happens and is queued for review; what a
    #  learner receives is the APPROVED text or the reason it is not shown.
    #  While the scholar roster is empty nothing can be approved, so every lesson is withheld with that
    #  stated - the designed state until the Owner engages a reviewer, and the reason a reader is given
    #  is the true one rather than a generic absence.
    from agentic_core.api import scholar_review as _sr
    _key = f"tajweed_lesson:{req.rule_name}:{req.level}"
    #  submit_if_new, never submit: `submit` overwrites, so the request after an approval would reset it
    _sr.submit_if_new(_key, "qep/tajweed/lesson", lesson, reference=req.rule_name)
    _published, _review_state, _review_why = _sr.published_body(_key, lesson)

    return {
        "rule": req.rule_name,
        "level": req.level,
        "lesson_plan": _published,
        "review_state": _review_state,
        "review_note": _review_why,
        "scholar_reviewed": _review_state == "approved",
        "served_by": served_by,
        "is_external": bool(meta.get("is_external")),
        "floor_served": floor_served,
        #  W613 (FU-477, M1 v8 R1.2) — THE NOTE DESCRIBES WHAT THE LEARNER RECEIVED. It was emitted whenever the
        #  floor served the composition, including when the scholar gate WITHHELD it, so a learner was told to
        #  treat "this outline" as a checklist above an empty box. A withheld lesson is not an outline the
        #  learner has: the note now speaks only of a published body, and a withheld one says why it is empty.
        **({"floor_note": ("the deterministic native floor served this — it is a structured "
                           "OUTLINE composed from the request, not scholarly content; treat it as "
                           "a study checklist and verify every rule with a qualified teacher")}
           if floor_served and _published is not None else {}),
        "withheld_note": (None if _published is not None else
                          "Nothing is shown because this lesson has not been approved by a scholar: "
                          + str(_review_why or "it is awaiting review")
                          + " The text was composed and queued for review; it is not shown until approved."),
        "ai_assisted": True,
        #  R11 (Owner ruling 2026-10-05b) — THE RIWAYAH IS DECLARED, so a rule set is not presented as
        #  universal. Tajwid rules differ between transmissions, and stating one set without saying which
        #  transmission it belongs to is an implicit scholarly claim. The value is a FACT about this
        #  platform rather than a ruling: it is the transmission of the edition the platform fetches.
        #  Cheap to state because recitation is never scored here (§11), so these rules are reference
        #  material and not a basis on which anyone is judged.
        "riwayah": _EDITION_PROVENANCE.get("quran-uthmani", {}).get("riwayah"),
        "riwayah_basis": (
            "these rules are stated for the transmission of the edition this platform fetches "
            "(quran-uthmani from alquran.cloud). Tajwid rules VARY between transmissions and between "
            "madhahib; this platform records which one it is stating and does not rule on which is "
            "authoritative - that belongs to qualified scholarship. A rule for another transmission is "
            "not reported here rather than being adapted."),
        "disclaimer": "AI-assisted educational content. Verify all rules with a qualified Islamic scholar or Quran teacher.",
    }


# ── Gamification ──────────────────────────────────────────────────────────────

@router.get("/gamification/{uid}")
async def get_gamification(uid: str):
    """Learner gamification state — REAL recorded awards only.

    W439 — the old handler probed GamifiedLearning for methods that do not exist
    (get_learner_state/award_achievement), so it ALWAYS fell to a zeros dict: every learner read
    xp 0, level 1, streak 0 forever, whatever they had done. State now comes from the persisted
    award store, and every derived figure (level, streak) carries its formula."""
    return _gami_state(_load_gami(uid))


class AwardRequest(BaseModel):
    uid: str
    achievement: str    # e.g. "ayah_memorised" | "daily_review" | "surah_complete"
    xp: int = Field(default=10, ge=1, le=100)


@router.post("/gamification/award")
async def award_xp(req: AwardRequest):
    """Award XP for a learning achievement — persisted, then reported.

    W439 — the old fallback returned "Achievement recorded" while persisting NOTHING (the engine
    it deferred to lacks the method it probed for). "recorded: true" now means the write happened;
    the full recomputed state comes back with it."""
    state = _award(req.uid, req.achievement, req.xp, source="explicit_award")
    return {"recorded": True, "achievement": req.achievement, "xp_awarded": req.xp, **state}


@router.get("/leaderboard")
async def qep_leaderboard(limit: int = 20):
    """P3.9 — rank learners by the XP actually RECORDED for them, and say what that means.

    The leaderboard this replaces (`qep_flagship.gamified_competition`, before W404) returned ten
    synthetic rows with scores from `random.randint` and a rank drawn from a die. This reads the store.

    EVERY FIGURE CARRIES ITS BASIS, which is this item's own guard for routes under /qep. In particular
    the POPULATION is stated: these are the learners who have a recorded award, not a field of
    competitors, and a board of two says it ranks two. A tie is named rather than silently broken.
    """
    rows = []
    unreadable = []
    for p in sorted(_GAMI_STORE.glob("*.json")):
        try:
            g = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:                       # noqa: BLE001 — reported, never skipped silently
            unreadable.append({"file": p.name, "why": e.__class__.__name__})
            continue
        _hist = [h for h in (g.get("history") or []) if isinstance(h, dict)]
        rows.append({
            "uid": p.stem,
            "xp": int(g.get("xp", 0) or 0),
            "achievements": len(g.get("achievements") or []),
            "awards_recorded": len(_hist),
            #  the sum of the learner's OWN history, so a reader can check `xp` against it rather than
            #  trusting it. They can differ: history is capped at the last 500 awards while xp is a
            #  running total, and saying so is better than quietly presenting one as proof of the other.
            "xp_in_recorded_history": sum(int(h.get("xp", 0) or 0) for h in _hist),
        })

    #  a tie is ordered by uid for determinism, and NAMED below rather than passed off as a ranking
    rows.sort(key=lambda r: (-r["xp"], r["uid"]))
    #  THE LEARNERS IN A TIE, not the number of duplicate totals. `len(xps) - len(set(xps))` gives 1 for
    #  two learners on 40 and one on 25, and the sentence below would then say "1 learner shares a total
    #  with another" when TWO do. A count that is almost right about people is worse than no count.
    _xps = [r["xp"] for r in rows]
    _tied_totals = {x for x in _xps if _xps.count(x) > 1}
    _ties = sum(1 for x in _xps if x in _tied_totals)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    _shown = rows[:max(0, int(limit))]

    return {
        "leaderboard": _shown,
        "learners_ranked": len(rows),
        "shown": len(_shown),
        "formula": "xp = the sum of the xp on every award recorded for that learner",
        "formula_basis": ("XP is only ever written by _award, which appends {achievement, xp, source, at} "
                          "to the learner's history and adds the same xp to a running total. Nothing here "
                          "scores a recitation, a memorisation attempt or any other performance - the "
                          "ranking is of RECORDED AWARDS and of nothing else."),
        #  THE CAP IS REPORTED, NOT DENIED. This sentence first read "not a top-N of a larger population"
        #  unconditionally, while `_shown` slices to `limit` two lines above - so the moment more learners
        #  had awards than the caller asked for, the basis asserted the opposite of what the code did.
        #  The archived gamification.py held the same defect in its other half (a silent top-10 with no
        #  sentence at all); a sentence that DENIES the cap is worse, because it answers the reader's
        #  question wrongly instead of leaving it open. So the basis is computed from the two counts.
        "truncated": len(_shown) < len(rows),
        "population_basis": (
            (f"{len(rows)} learner(s) have a recorded award on this deployment and {len(_shown)} are "
             f"shown, so THIS IS A TOP-{len(_shown)} OF A LARGER POPULATION: the learners ranked below "
             f"it exist and are not displayed. Raise `limit` to see them.")
            if len(_shown) < len(rows) else
            (f"every learner with a recorded award is shown: {len(rows)} on this deployment, none "
             f"omitted. This is not a field of competitors - if two learners are ranked, two learners "
             f"have awards.")),
        "ties": _ties,
        "tie_basis": (f"{_ties} learner(s) share an XP total with another; equal totals are ordered by uid "
                      f"for a stable response, which is a deterministic order and NOT a ranking between "
                      f"them" if _ties else "no two learners share an XP total, so every rank is distinct"),
        "not_a_certification": ("a position here reflects recorded awards only. It is not an attainment, "
                                "not a hifz certification, and no scholar has assessed it."),
        **({"unreadable": unreadable,
            "unreadable_basis": (f"{len(unreadable)} learner file(s) could not be read, so they are NOT in "
                                 f"the ranking - which is not the same as their having no XP")}
           if unreadable else {}),
    }


class QepCurriculumRequest(BaseModel):
    subject: str = "Quran & Islamic Studies"
    level: str = "Intermediate"
    duration_weeks: int = 12


@router.post("/curriculum")
async def qep_curriculum(req: QepCurriculumRequest):
    """P3.10 — religious curriculum BEHIND the R7 gate: composed, submitted, and served only if approved.

    The three facts a caller gets back, always the same keys so none has to be guessed at:

      curriculum       the approved text, or None. None is never an error and never an empty plan.
      review_state     approved / withheld — what the gate decided about THIS text.
      review_note      WHY, in a sentence a learner can act on. "No scholar is engaged yet" and "a
                       reviewer rejected this" are different things to be told, and the gate keeps them
                       distinct rather than collapsing both into silence.

    While the roster is empty NOTHING can be approved, so every request is withheld with that stated.
    That is the designed state until the Owner engages a reviewer - not a failure, and not dressed up as
    one. P3.10's own instruction is that the surface "must not be dressed".
    """
    from agentic_core.api import scholar_review as _sr

    _weeks = min(max(int(req.duration_weeks), 4), 52)
    prompt = (
        f"Design a {_weeks}-week study plan for: {req.subject}\n"
        f"Level: {req.level}\n\n"
        f"## Learning Objectives\n## Week-by-Week Plan\n## Assessment Approach\n"
        f"## Resources (named editions and authors only)\n\n"
        f"State a scholarly position only where it is agreed; where schools differ, say that they differ "
        f"and name them rather than choosing."
    )
    meta = await gateway.query_meta(prompt, agent="qep_curriculum", augment=False)
    body = meta.get("output") or ""
    served_by = meta.get("served_by", "native")

    #  submit_if_new, never submit: a second request for the same subject must not reset an approval
    _key = f"qep_curriculum:{req.subject}:{req.level}:{_weeks}"
    _sr.submit_if_new(_key, "qep/curriculum", body, reference=req.subject)
    _published, _state, _why = _sr.published_body(_key, body)

    return {
        "subject": req.subject,
        "level": req.level,
        "duration_weeks": _weeks,
        "curriculum": _published,
        "review_state": _state,
        "review_note": _why,
        "scholar_reviewed": _state == "approved",
        "gate": _sr.gate_status(),
        "served_by": served_by,
        "floor_served": served_by == "native",
        "basis": (
            "Owner ruling 2026-10-05b R7 (§A.12.3): a named human scholar approves AI-composed religious "
            "teaching content before a learner sees it, and a disclaimer is not a review. An approval is "
            "bound to the exact text approved, so an edit after approval falls back to withheld. Nothing "
            "here scores a learner, assesses a recitation or rules on a difference between schools."),
    }


@router.get("/status")
async def qep_status():
    """Platform status — component lines say what each ACTUALLY is (W439: they were constants —
    gamification claimed "active — GamifiedLearning" while every award vanished, and quran_text
    claimed "live" without probing anything)."""
    learners = len(list(_GAMI_STORE.glob("*.json")))
    hifz_users = len(list(_HIFZ_STORE.glob("*.json")))
    return {
        "platform": "Quran Education Platform (QEP)",
        "components": {
            "hifz_sm2": f"active — MemorizationEngine (real SM-2); {hifz_users} learner record(s)",
            "tajweed": ("text tools only — written-recall comparison + AI-assisted lesson outlines; "
                        "NO recitation assessment (no phonetic model is provisioned)"),
            "gamification": f"active — persisted award store; {learners} learner record(s)",
            "quran_text": ("external source (alquran.cloud, constitutional) — fetched on demand, "
                           "returns 503 honestly when unreachable; never AI-generated"),
        },
        "constraints": [
            "Quran text sourced from alquran.cloud only — never AI-generated",
            "AI content labelled AI-assisted with serving provenance — not authoritative",
            "Recitation is never scored — no phonetic model exists to score it",
        ],
    }


# ── P3.11 clause (3) — A.8's two contribution channels, recorded against the entity's own books ──────
#  A.8 (Owner-authored) names "Zakat-eligible funds" and "Sponsor-a-Student" among QEP's finances. Both are
#  VIRTUAL WST: no real-money rail is touched here and none may be, which is the Owner's standing constraint.
#
#  WHAT NEITHER CHANNEL DOES, and both say so in their own response:
#   · the Zakat channel does not rule on whether a donor's Zakat obligation is discharged. The charity share
#     is DESIGNATED Zakat-eligible by A.8; whether a given contribution discharges an obligation is a
#     religious ruling, which §11 forbids this platform from making. The donor is referred to their scholar.
#   · Sponsor-a-Student names no learner, because no mechanism matches a contribution to an individual
#     learner. Claiming a sponsored student would be the fabrication this whole plan exists to prevent.

class ContributionRequest(BaseModel):
    vsb_id: str = Field(..., min_length=1, max_length=64)
    amount_wst: float = Field(..., gt=0)
    donor_ref: str = ""


_A8_FINANCE_BASIS = ("vision A.8 (Owner-authored): QEP is 100% donation and waqf-backed, free at the point "
                     "of use for individuals, with Zakat-eligible funds and Sponsor-a-Student. Virtual WST "
                     "only - no real-money rail is touched by this channel.")


def _contribution_entity(vsb_id: str) -> dict:
    """The entity a contribution is for, or an HTTP refusal. NEVER a ledger for an id nobody established.

    `read_strict` answers a missing ledger file with new empty books, so `VirtualLedger(<anything>)` succeeds
    and a channel that skipped this check would report a recorded donation against an entity that does not
    exist - and would leave a ledger file behind as evidence for it.
    """
    #  the SAME pattern this file's W439 choke point uses, because vsb_id is interpolated into a ledger path
    #  exactly as uid was into a store path. Not _safe_uid itself: its refusal names `uid`, and a refusal
    #  naming a field the caller never sent cannot be acted on by the caller who hit it.
    if not _UID_RE.fullmatch(vsb_id or ""):
        raise HTTPException(status_code=400, detail={
            "message": "vsb_id must match [A-Za-z0-9_-]{1,64}; it is interpolated into a ledger path, so a "
                       "path segment is refused. Nothing was recorded.",
            "vsb_id": vsb_id})
    safe = vsb_id
    rec = None
    try:
        from agentic_core.economy.living_vsbs import _load as _load_living
        rec = (_load_living() or {}).get(safe)
    except Exception as err:                        # the roster being unreadable is not "no such entity"
        raise HTTPException(status_code=503, detail={
            "message": f"the living roster could not be read, so it is not known whether {safe} exists; "
                       f"nothing was recorded",
            "error": f"{type(err).__name__}: {err}"})
    if rec is None:
        try:
            from agentic_core.api.vsb import _load_vsb
            rec = _load_vsb(safe)
        except Exception:
            rec = None
    if not rec:
        raise HTTPException(status_code=404, detail={
            "message": f"no entity {safe} is on the living roster or in the VSB store, so a contribution "
                       f"cannot be recorded against its books. Nothing was written.",
            "vsb_id": safe})
    return {"vsb_id": safe, "record": rec}


def _record_contribution(vsb_id: str, amount_wst: float, channel: str, donor_ref: str = "") -> dict:
    """Credit the entity's `revenue` account and REPORT THE BALANCE READ BACK, not the amount handed in.

    This file's own W439 note records the defect this avoids: "every award fell to a fallback claiming
    'recorded' while persisting nothing". A channel that returns the figure it was given cannot tell a
    caller whether anything was persisted, so the balance below is re-read from the books after the write.
    """
    ent = _contribution_entity(vsb_id)
    safe = ent["vsb_id"]
    from agentic_core.economy.ledger import VirtualLedger
    led = VirtualLedger(safe)
    if led.load_error:
        #  REFUSED where the caller can receive it: an unreadable ledger is not an empty one, and writing to
        #  books that could not be read whole would destroy whatever is actually in them.
        raise HTTPException(status_code=503, detail={
            "message": f"{safe}'s ledger could not be read, so nothing was recorded. A contribution is "
                       f"never written on top of books that could not be read whole.",
            "load_error": led.load_error})
    amount = round(float(amount_wst), 2)
    memo = f"QEP contribution via {channel}" + (f" (donor ref {donor_ref})" if donor_ref else "")
    try:
        led.record("revenue", amount, memo=memo, kind="credit", source=f"qep_{channel}")
    except Exception as err:
        raise HTTPException(status_code=503, detail={
            "message": f"the contribution could not be posted to {safe}'s books, so it did NOT happen; "
                       f"nothing is held pending and the contribution should be made again",
            "error": f"{type(err).__name__}: {err}"})
    #  re-read: the balance below is what the books say, not what this function was told
    after = VirtualLedger(safe).balances()
    return {
        "recorded": True,
        "vsb_id": safe,
        "channel": channel,
        "amount_wst": amount,
        "revenue_balance_wst": after.get("revenue"),
        "currency": "WST (virtual)",
        "memo": memo,
        "balance_basis": ("revenue_balance_wst was RE-READ from the entity's ledger after the posting, so it "
                         "is what the books say rather than the figure this request supplied"),
        "distribution_basis": ("a contribution is credited to `revenue`, which the entity's next economic "
                              "cycle distributes through its own waterfall (A.8: owner 0%, surplus capped "
                              "at 5% with reinvestment). It is not allocated by this request."),
        "a8_basis": _A8_FINANCE_BASIS,
    }


@router.post("/contribute/zakat")
async def contribute_zakat(req: ContributionRequest):
    """A Zakat-eligible contribution to a QEP entity. THIS PLATFORM RULES ON NOTHING.

    A.8 designates QEP's charity funds Zakat-eligible. Whether a particular contribution discharges a
    particular donor's Zakat obligation is a religious ruling - §11 forbids this platform from making one,
    so the response states the designation, refuses the ruling, and refers the donor to their own scholar.
    """
    out = _record_contribution(req.vsb_id, req.amount_wst, "zakat", req.donor_ref)
    out["zakat_basis"] = (
        "A.8 DESIGNATED this entity's charity funds Zakat-eligible. This platform does NOT rule on whether "
        "your Zakat obligation is discharged by this contribution: that is a religious ruling and no AI here "
        "makes one. Ask your own scholar, who can weigh your circumstances and the eligibility of the "
        "recipient. A designated fund and a discharged obligation are different facts.")
    out["rules_on"] = []
    return out


@router.post("/contribute/sponsor-a-student")
async def contribute_sponsor_a_student(req: ContributionRequest):
    """Sponsor-a-Student (A.8). NO LEARNER IS NAMED, because nothing here matches one.

    A.8 names Sponsor-a-Student as a channel. Reporting a sponsored learner would require a matching
    mechanism, and none exists - so this says what the contribution DOES fund (the entity's books, which its
    waterfall distributes to the user_projects and charity shares) and does not claim a student.
    """
    out = _record_contribution(req.vsb_id, req.amount_wst, "sponsor_a_student", req.donor_ref)
    out["student_matched"] = None
    out["sponsorship_basis"] = (
        "NO LEARNER IS NAMED OR MATCHED to this contribution: no mechanism exists in this platform that "
        "pairs a donation with an individual learner, and reporting one would be a claim with nothing behind "
        "it. What this contribution does is fund the entity itself, whose waterfall directs the largest "
        "shares to learner projects and charity, with no owner share at all. Because QEP is free at the "
        "point of use, no learner is waiting on a sponsor to be able to study.")
    return out


@router.get("/contribute/statement/{vsb_id}")
async def contribution_statement(vsb_id: str):
    """A.8's transparent donor view: what came in by channel, and how the waterfall allocates it.

    Reads the entity's OWN books and its OWN template. The allocation is what the waterfall WOULD direct;
    the entity's cycle is what actually distributes, so the two are reported separately rather than one
    presented as the other.
    """
    ent = _contribution_entity(vsb_id)
    safe = ent["vsb_id"]
    from agentic_core.economy.ledger import VirtualLedger
    led = VirtualLedger(safe)
    if led.load_error:
        raise HTTPException(status_code=503, detail={
            "message": f"{safe}'s ledger could not be read, so no donor statement can be produced. An "
                       f"unreadable ledger is not an empty one and zero would be a false figure.",
            "load_error": led.load_error})
    #  READ THE POSTINGS, NOT THE LEGACY ENTRIES. `record()` writes an entry carrying ts/account/kind/amount/
    #  memo/balance_after and NO SOURCE - the source tag goes on the balanced POSTING it makes. A statement
    #  built from `entries` would therefore find no channel tag anywhere and report 0.00 for both channels
    #  while the money sat in the books: a donor statement that is silently empty rather than honestly zero.
    split = led.postings_by_source()
    _qep_rows = [r for r in split.get("by_source", []) if str(r.get("source", "")).startswith("qep_")]
    by_channel = {str(r["source"])[4:]: r["total_wst"] for r in _qep_rows}
    _counts = {str(r["source"])[4:]: r["count"] for r in _qep_rows}
    etype = ((ent["record"] or {}).get("economy") or {}).get("entity_type") or \
        (ent["record"] or {}).get("entity_type") or ""
    from agentic_core.economy.entities import ENTITY_TEMPLATES, get_template
    tmpl = get_template(etype)
    total = round(sum(by_channel.values()), 2)
    return {
        "vsb_id": safe,
        "contributions_by_channel_wst": by_channel,
        "contributions_by_channel_count": _counts,
        "contributions_total_wst": total,
        "contributions_count": sum(_counts.values()),
        "revenue_balance_wst": led.balances().get("revenue"),
        #  an undeclared tag is NOT folded into a channel: it would attribute money to a channel on the
        #  strength of a prefix nobody declared, which is what `unknown_sources` exists to prevent
        "undeclared_channel_tags": [s for s in split.get("unknown_sources", [])
                                    if str(s).startswith("qep_")],
        "untagged_postings": split.get("not_stated"),
        "waterfall": dict(tmpl.get("waterfall") or {}),
        "would_allocate_wst": {k: round(total * float(v), 2) for k, v in (tmpl.get("waterfall") or {}).items()},
        "entity_type": etype,
        "template_name": tmpl.get("name"),
        "template_is_a_fallback": bool(etype) and etype not in ENTITY_TEMPLATES,
        "allocation_basis": ("would_allocate_wst is what this entity's waterfall WOULD direct for the total "
                            "contributed; it is not a record of distributions made. Only an economic cycle "
                            "distributes, and a cycle run before some of these contributions arrived "
                            "distributed less. The two are reported separately rather than one presented as "
                            "the other."),
        "template_basis": ("get_template() returns the DEFAULT template for an unrecognised entity_type, so "
                           "template_is_a_fallback says whether this waterfall is the entity's own or the "
                           "generic one standing in for it - a silent fallback would otherwise show the "
                           "wrong figures under the right name."),
        "a8_basis": _A8_FINANCE_BASIS,
    }
