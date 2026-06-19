"""
Cross-Platform Bridge — wearable, voice, and AR surface endpoints.

Refactored from FastAPI() sub-app to APIRouter so it can be mounted
in app_mvp.py. Previous version used FastAPI() which cannot be
included via include_router().

NOTE: /voice/command and /ar/scene are Phase 3 scaffolded endpoints.
They accept real input and return honest status — no hardcoded fake data.
"""
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.organism.biobus import biobus

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/cross-platform", tags=["Cross-Platform Bridge"])


class WearableAlert(BaseModel):
    id: str
    message: str
    priority: str = "medium"


class VoiceQuery(BaseModel):
    raw_audio_input: str
    context: Dict[str, Any] = {}


@api.post("/wearable/alert")
async def send_wearable_alert(alert: WearableAlert):
    """Queue a glanceable alert for Apple Watch / Wear OS. Phase 3 implementation."""
    logger.info("CrossPlatform: queuing wearable alert id=%s priority=%s", alert.id, alert.priority)
    biobus.fire_signal("motor", "cross_platform.wearable", f"Alert [{alert.priority}]: {alert.message[:60]}", 0.4)
    return {
        "status": "QUEUED",
        "alert_id": alert.id,
        "message": alert.message,
        "priority": alert.priority,
        "queued_at": datetime.now(timezone.utc).isoformat(),
        "delivery": "not_yet_implemented",
        "note": "Push notification integration is Phase 3. Alert logged server-side."
    }


@api.post("/voice/command")
async def process_voice_command(query: VoiceQuery):
    """Accept a voice command payload. Phase 3: route to AI gateway."""
    logger.info("CrossPlatform: voice command received length=%d", len(query.raw_audio_input))
    biobus.fire_signal("sensory", "cross_platform.voice", f"Voice input: {len(query.raw_audio_input)} chars", 0.5)
    return {
        "received": True,
        "input_length": len(query.raw_audio_input),
        "status": "pending_implementation",
        "note": "Voice command routing to AI gateway is Phase 3."
    }


@api.get("/ar/scene")
async def get_ar_council_scene():
    """Returns AR scene metadata schema. Phase 3: dynamic construction from project data."""
    logger.info("CrossPlatform: AR scene metadata requested")
    return {
        "scene_id": None,
        "assets": [],
        "active_participants": 0,
        "status": "pending_implementation",
        "note": "AR scene dynamic rendering is Phase 3."
    }
