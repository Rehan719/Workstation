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


async def fetch_ayah_arabic(surah: int, ayah: int) -> str | None:
    """Sourced Arabic text of one ayah (cache-first) — for callers that must inject AUTHENTIC text
    into prompts instead of letting a model generate Quranic Arabic (the constitutional rule).
    Returns None when the source is unreachable and no cache exists; NEVER generates."""
    if not (1 <= surah <= 114 and 1 <= ayah <= _AYAH_COUNTS[surah]):
        return None
    key = f"ayah_{surah}_{ayah}_quran-uthmani"
    cached = _cache_read(key)
    if cached:
        return (cached["data"].get("data") or {}).get("text")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{_QURAN_API}/ayah/{surah}:{ayah}/quran-uthmani")
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return None
    _cache_write(key, data)
    return (data.get("data") or {}).get("text")


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
    ayaat = [
        {
            "number_in_surah": a["numberInSurah"],
            "text_arabic": a["text"],
        }
        for a in surah_data.get("ayahs", [])
    ]
    return {
        "surah_number": number,
        "name_arabic": surah_data.get("name", ""),
        "name_english": surah_data.get("englishNameTranslation", ""),
        "ayah_count": len(ayaat),
        "ayaat": ayaat,
        "edition": edition,
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
    return {
        "ref": ref,
        "text_arabic": ayah.get("text", ""),
        "surah_name": ayah.get("surah", {}).get("name", ""),
        "juz": ayah.get("juz", 0),
        "page": ayah.get("page", 0),
        "source": "alquran.cloud",
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

    return {
        "rule": req.rule_name,
        "level": req.level,
        "lesson_plan": lesson,
        "served_by": served_by,
        "is_external": bool(meta.get("is_external")),
        "floor_served": floor_served,
        **({"floor_note": ("the deterministic native floor served this — it is a structured "
                           "OUTLINE composed from the request, not scholarly content; treat it as "
                           "a study checklist and verify every rule with a qualified teacher")}
           if floor_served else {}),
        "ai_assisted": True,
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
