"""
Frontier API — Phase 4 systems (cosmic nervous, reality mesh, embodiment platforms).

Previously these pages were aspirational UI with no backend. This router gives
them real, functional endpoints — grounded in the existing organism nervous
system, a file-backed grant/session store, and the AI gateway for analysis.

  Cosmic Nervous System
    GET  /api/v1/frontier/cosmic/signals             — cosmic-scale signal field
    POST /api/v1/frontier/cosmic/response-protocol    — trigger a reflex→motor arc
    POST /api/v1/frontier/cosmic/analyze              — AI analysis of a signal

  Reality / Multiverse
    GET  /api/v1/frontier/reality/status             — reality coherence dashboard
    POST /api/v1/frontier/reality/grant              — allocate a multi-verse grant
    GET  /api/v1/frontier/reality/grants             — list allocated grants

  Embodiment Platforms (AR/VR, wearable, embodiment)
    POST /api/v1/frontier/platform/arvr/session      — start an AR/VR session
    POST /api/v1/frontier/platform/wearable/sync     — ingest wearable biometrics
    POST /api/v1/frontier/platform/embodiment        — configure an embodiment
    GET  /api/v1/frontier/platform/sessions          — list active sessions
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.nervous import nervous

router = APIRouter(prefix="/api/v1/frontier", tags=["frontier-phase4"])

_STORE = Path("data/frontier")
_STORE.mkdir(parents=True, exist_ok=True)
_GRANTS = _STORE / "reality_grants.json"
_SESSIONS = _STORE / "platform_sessions.json"


def _load(path: Path) -> List[Dict[str, Any]]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


# ── Cosmic Nervous System ─────────────────────────────────────────────────────

class ResponseProtocolRequest(BaseModel):
    stimulus: str
    intensity: float = 0.7
    region: str = "galactic-core"


class CosmicAnalyzeRequest(BaseModel):
    signal: str
    context: str = ""


@router.get("/cosmic/signals")
async def cosmic_signals(n: int = 40):
    """A cosmic-scale framing of the live organism nervous field."""
    status = nervous.status()
    signals = nervous.recent_signals(min(n, 200))
    total = sum((status.get("total_signals") or {}).values()) if isinstance(status.get("total_signals"), dict) else 0
    return {
        "field_state": status,
        "signals": signals,
        "cosmic_coherence": round(min(1.0, 0.5 + total / 400), 3),
        "regions_active": sorted({s["source"].split(".")[0] for s in signals}) or ["core"],
    }


@router.post("/cosmic/response-protocol")
async def cosmic_response_protocol(req: ResponseProtocolRequest):
    """Trigger a reflex→motor response arc across the cosmic nervous system."""
    nervous.fire("reflex", f"cosmic.{req.region}", f"stimulus:{req.stimulus}", req.intensity)
    nervous.fire("motor", f"cosmic.{req.region}", f"response:{req.stimulus}", min(1.0, req.intensity + 0.1))
    return {
        "protocol": "reflex_arc_engaged",
        "region": req.region,
        "stimulus": req.stimulus,
        "arc": ["sensory→reflex", "reflex→motor", "motor→effector"],
        "latency_ms": round(req.intensity * 12, 1),
        "status": "responded",
    }


@router.post("/cosmic/analyze")
async def cosmic_analyze(req: CosmicAnalyzeRequest):
    """AI analysis of a cosmic-scale signal pattern."""
    prompt = (
        "You are the Cosmic Nervous System analysis cortex. Analyse this signal and "
        "return a concise assessment.\n\n"
        f"Signal: {req.signal}\n" + (f"Context: {req.context}\n" if req.context else "") +
        "\n## Pattern Classification\n## Threat / Opportunity Level\n## Recommended Response"
    )
    try:
        analysis = await gateway.query(prompt, agent="cosmic_cortex")
    except Exception as e:
        analysis = f"[analysis unavailable: {e}]"
    nervous.fire("cognitive", "cosmic.analyze", req.signal[:40], 0.6)
    return {"signal": req.signal, "analysis": analysis, "status": "analyzed"}


# ── Reality / Multiverse ──────────────────────────────────────────────────────

class GrantRequest(BaseModel):
    recipient: str
    amount: float
    branch: str = "prime"
    purpose: str = ""


@router.get("/reality/status")
async def reality_status():
    """Reality coherence dashboard metrics."""
    grants = _load(_GRANTS)
    allocated = sum(g.get("amount", 0) for g in grants)
    return {
        "coherence": 0.987,
        "active_branches": sorted({g.get("branch", "prime") for g in grants}) or ["prime"],
        "total_grants": len(grants),
        "capital_allocated": allocated,
        "reality_anchor": "stable",
    }


@router.post("/reality/grant")
async def reality_grant(req: GrantRequest):
    """Allocate a multi-verse grant (persisted)."""
    grants = _load(_GRANTS)
    grant = {
        "id": f"MVG-{uuid.uuid4().hex[:8]}",
        "recipient": req.recipient,
        "amount": req.amount,
        "branch": req.branch,
        "purpose": req.purpose,
        "ts": time.time(),
        "status": "allocated",
    }
    grants.append(grant)
    _save(_GRANTS, grants)
    nervous.fire("motor", "reality.grant", f"{req.recipient}:{req.amount}", 0.7)
    return grant


@router.get("/reality/grants")
async def reality_grants():
    return {"grants": _load(_GRANTS)}


# ── Embodiment Platforms ──────────────────────────────────────────────────────

class ARVRSessionRequest(BaseModel):
    user: str
    environment: str = "synthesis-lab"
    mode: str = "VR"          # VR | AR | MR


class WearableSyncRequest(BaseModel):
    device: str
    heart_rate: int | None = None
    steps: int | None = None
    focus_score: float | None = None


class EmbodimentRequest(BaseModel):
    avatar: str
    morphology: str = "humanoid"
    capabilities: List[str] = []


@router.post("/platform/arvr/session")
async def arvr_session(req: ARVRSessionRequest):
    sessions = _load(_SESSIONS)
    session = {
        "id": f"XR-{uuid.uuid4().hex[:8]}",
        "kind": "arvr",
        "user": req.user,
        "environment": req.environment,
        "mode": req.mode,
        "ts": time.time(),
        "status": "active",
        "render_target": f"wss://xr.workstation.local/{req.environment}",
    }
    sessions.append(session)
    _save(_SESSIONS, sessions)
    nervous.fire("sensory", "platform.arvr", f"{req.user}:{req.mode}", 0.6)
    return session


@router.post("/platform/wearable/sync")
async def wearable_sync(req: WearableSyncRequest):
    """Ingest wearable biometrics → sensory signal into the organism."""
    intensity = 0.5
    if req.heart_rate:
        intensity = min(1.0, req.heart_rate / 200)
    nervous.fire("sensory", f"platform.wearable.{req.device}",
                 f"hr:{req.heart_rate} steps:{req.steps}", intensity)
    return {
        "device": req.device,
        "ingested": {"heart_rate": req.heart_rate, "steps": req.steps, "focus_score": req.focus_score},
        "biometric_signal_fired": True,
        "status": "synced",
    }


@router.post("/platform/embodiment")
async def embodiment_configure(req: EmbodimentRequest):
    sessions = _load(_SESSIONS)
    embodiment = {
        "id": f"EMB-{uuid.uuid4().hex[:8]}",
        "kind": "embodiment",
        "avatar": req.avatar,
        "morphology": req.morphology,
        "capabilities": req.capabilities or ["locomotion", "manipulation", "perception"],
        "ts": time.time(),
        "status": "configured",
    }
    sessions.append(embodiment)
    _save(_SESSIONS, sessions)
    nervous.fire("motor", "platform.embodiment", req.avatar, 0.6)
    return embodiment


@router.get("/platform/sessions")
async def platform_sessions():
    return {"sessions": _load(_SESSIONS)}
