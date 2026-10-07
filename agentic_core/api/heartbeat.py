"""
Organism Heartbeat API — observe and control the continuous-autonomy scheduler.

The heartbeat (agentic_core/organism/heartbeat.py) keeps the IDBO self-running:
a circadian rhythm pulsing the nervous system, checking homeostasis, ticking the
transformation engine, and UEG-logging every beat. Expensive AI cognition is
opt-in and paced.

  GET  /api/v1/heartbeat/status     — running state, beats, circadian phase, recent beats
  POST /api/v1/heartbeat/beat       — fire one beat now (cheap; for demo/manual control)
  POST /api/v1/heartbeat/start      — start the continuous rhythm
  POST /api/v1/heartbeat/stop       — stop it
  POST /api/v1/heartbeat/configure  — set cadence + opt-in autonomous AI cycles
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

#  W579 (FU-359) — THE MODULE, NOT THE ATTRIBUTE. `from ... import heartbeat` binds the singleton
#  OBJECT once at import, so when a test reloads agentic_core/organism/heartbeat.py (which re-runs
#  `heartbeat = OrganismHeartbeat()`) these routes keep the OLD object while the module attribute
#  points at a new one. Measured: after a reload the two references differ, and a flag written on the
#  module object reports False through /status. Three separate diagnoses have ended at that split.
#  Binding the module and resolving `.heartbeat` per call is what a singleton means, and in
#  production - where nothing reloads - the two forms are identical.
from agentic_core.organism import heartbeat as _hb_mod

router = APIRouter(prefix="/api/v1/heartbeat", tags=["organism-heartbeat"])


@router.get("/status")
async def status():
    return _hb_mod.heartbeat.status()


@router.post("/beat")
async def beat():
    """Fire a single heartbeat now (cheap — pulse + homeostasis + transformation tick + UEG)."""
    return await _hb_mod.heartbeat.beat()


@router.post("/start")
async def start():
    _hb_mod.heartbeat.start()
    return {"running": _hb_mod.heartbeat.running, "status": "started"}


@router.post("/stop")
async def stop():
    _hb_mod.heartbeat.stop()
    return {"running": _hb_mod.heartbeat.running, "status": "stopped"}


class ConfigureRequest(BaseModel):
    interval_seconds: Optional[int] = None
    auto_evolve: Optional[bool] = None      # opt-in: run AI evolution cycles autonomously
    auto_economy: Optional[bool] = None     # opt-in: run economy cycles autonomously
    auto_align: Optional[bool] = None       # opt-in: route vision gaps to tiers each beat (cheap)
    auto_compliance: Optional[bool] = None  # opt-in (§11, W288): re-screen living VSBs on the beat
    auto_ship: Optional[bool] = None        # opt-in (§13, W319): re-ship STALE repos on the beat
    auto_metabolic: Optional[bool] = None   # FU-367 (W609): run the recirculation loop on the beat (runtime only)
    metabolic_every: Optional[int] = None   # every N beats
    circadian_to_atp: Optional[bool] = None # FU-308 (W622): the circadian map reaches ATP (runtime only, default off)


@router.post("/configure")
async def configure(req: ConfigureRequest):
    _hb_mod.heartbeat.configure(req.interval_seconds, req.auto_evolve, req.auto_economy,
                                req.auto_align, auto_compliance=req.auto_compliance,
                                auto_ship=req.auto_ship, auto_metabolic=req.auto_metabolic,
                                metabolic_every=req.metabolic_every, circadian_to_atp=req.circadian_to_atp)
    return _hb_mod.heartbeat.status()
