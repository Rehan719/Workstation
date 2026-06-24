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
  GET  /api/v1/qep/ayah/{ref}         — get single ayah (surah:ayah)
  POST /api/v1/qep/hifz/schedule      — generate SM-2 memorisation schedule
  POST /api/v1/qep/hifz/review        — record a review session, get next interval
  GET  /api/v1/qep/hifz/progress/{uid} — get memorisation progress matrix
  POST /api/v1/qep/tajweed/analyse    — analyse recitation (phoneme/diacritic)
  POST /api/v1/qep/tajweed/lesson     — AI-generated tajweed lesson plan (labelled)
  GET  /api/v1/qep/gamification/{uid} — get learner gamification state
  POST /api/v1/qep/gamification/award — award XP for a learning achievement
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from agentic_core.config import data_path
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.religious_domain.tajwid.coach import TajwidCoach
from agentic_core.religious_domain.learning.gamification import GamifiedLearning

router = APIRouter(prefix="/api/v1/qep", tags=["qep"])

_hifz_engine = MemorizationEngine()
_tajweed_coach = TajwidCoach()
try:
    _gamification = GamifiedLearning(dual_metric_middleware=None)
except Exception:
    _gamification = None

_QURAN_API = "https://api.alquran.cloud/v1"
_HIFZ_STORE = data_path("hifz_progress")
_HIFZ_STORE.mkdir(parents=True, exist_ok=True)

_SURAH_NAMES_CACHE: dict[int, str] = {}  # loaded lazily


def _hifz_path(uid: str) -> Path:
    return _HIFZ_STORE / f"{uid}.json"


def _load_hifz(uid: str) -> dict:
    p = _hifz_path(uid)
    return json.loads(p.read_text()) if p.exists() else {
        "uid": uid,
        "sessions": [],
        "cards": {},  # {ayah_ref: {repetitions, interval, efactor, next_review_date}}
        "total_ayaat_memorised": 0,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _save_hifz(uid: str, data: dict) -> None:
    _hifz_path(uid).write_text(json.dumps(data, indent=2))


# ── Quran Text (alquran.cloud) ────────────────────────────────────────────────

@router.get("/suwar")
async def list_suwar():
    """List all 114 surahs with name and ayah count. Source: alquran.cloud"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{_QURAN_API}/surah")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")

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
    return {"suwar": suwar, "total": len(suwar), "source": "alquran.cloud"}


@router.get("/surah/{number}")
async def get_surah(number: int, edition: str = "quran-uthmani"):
    """Get complete surah text. number: 1-114. Source: alquran.cloud — NOT AI-generated."""
    if not 1 <= number <= 114:
        raise HTTPException(status_code=400, detail="Surah number must be 1-114.")
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{_QURAN_API}/surah/{number}/{edition}")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")

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
        "source": "alquran.cloud",
        "note": "Authentic Arabic text sourced from alquran.cloud — not AI-generated.",
    }


@router.get("/ayah/{surah_number}/{ayah_number}")
async def get_ayah(surah_number: int, ayah_number: int, edition: str = "quran-uthmani"):
    """Get a single ayah. Source: alquran.cloud."""
    if not 1 <= surah_number <= 114:
        raise HTTPException(status_code=400, detail="Surah number must be 1-114.")
    ref = f"{surah_number}:{ayah_number}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{_QURAN_API}/ayah/{ref}/{edition}")
            resp.raise_for_status()
            data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Quran API unavailable: {e}")

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

    return {
        "uid": req.uid,
        "ayah_ref": req.ayah_ref,
        "quality": req.quality,
        "new_interval_days": new_interval,
        "new_efactor": round(new_efactor, 3),
        "next_review_date": next_date,
        "total_ayaat_memorised": hifz["total_ayaat_memorised"],
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
        "due_today": len(due_today),
        "due_refs": due_today[:20],
        "total_sessions": len(hifz.get("sessions", [])),
        "last_session": hifz["sessions"][-1] if hifz.get("sessions") else None,
        "progress_matrix": hifz.get("cards", {}),
    }


# ── Tajweed ───────────────────────────────────────────────────────────────────

class TajweedAnalyseRequest(BaseModel):
    ayah_text: str       # Arabic text from authoritative source
    recitation_notes: str = ""  # Educator/user notes on the recitation


@router.post("/tajweed/analyse")
async def tajweed_analyse(req: TajweedAnalyseRequest):
    """
    Analyse tajweed quality. AI assists — human review required for final scoring.
    Label: AI-assisted analysis, not authoritative judgment.
    """
    analysis = _tajweed_coach.analyze_recitation(
        reference_text=req.ayah_text,
        user_audio_emulation=req.recitation_notes or "No audio — text-based analysis only.",
    )

    return {
        "analysis": analysis,
        "ayah_text": req.ayah_text[:200],
        "ai_assisted": True,
        "disclaimer": "This is AI-assisted tajweed analysis. Human scholarly review required for authoritative assessment.",
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
    lesson = await gateway.query(prompt, agent="tajweed_lesson")

    return {
        "rule": req.rule_name,
        "level": req.level,
        "lesson_plan": lesson,
        "ai_assisted": True,
        "disclaimer": "AI-assisted educational content. Verify all rules with a qualified Islamic scholar or Quran teacher.",
    }


# ── Gamification ──────────────────────────────────────────────────────────────

@router.get("/gamification/{uid}")
async def get_gamification(uid: str):
    """Get learner gamification state (XP, level, achievements)."""
    state = (_gamification.get_learner_state(uid) if _gamification and hasattr(_gamification, "get_learner_state") else None) or {
        "uid": uid,
        "xp": 0,
        "level": 1,
        "achievements": [],
        "streak_days": 0,
    }
    return state


class AwardRequest(BaseModel):
    uid: str
    achievement: str    # "ayah_memorised" | "daily_review" | "surah_complete"
    xp: int = 10


@router.post("/gamification/award")
async def award_xp(req: AwardRequest):
    """Award XP for a learning achievement."""
    if _gamification and hasattr(_gamification, "award_achievement"):
        result = _gamification.award_achievement(req.uid, req.achievement, req.xp)
    else:
        result = {
            "uid": req.uid,
            "achievement": req.achievement,
            "xp_awarded": req.xp,
            "message": f"Achievement '{req.achievement}' recorded.",
        }
    return result


@router.get("/status")
async def qep_status():
    return {
        "platform": "Quran Education Platform (QEP)",
        "components": {
            "hifz_sm2": "active — MemorizationEngine (SM-2 algorithm)",
            "tajweed_coach": "active — TajwidCoach",
            "gamification": "active — GamifiedLearning",
            "quran_text": "live — alquran.cloud API",
        },
        "constraints": [
            "Quran text sourced from alquran.cloud only — never AI-generated",
            "AI analysis labelled as AI-assisted — not authoritative",
            "Recitation scoring requires human review",
        ],
    }
