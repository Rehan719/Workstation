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

from agentic_core.organism.heartbeat import heartbeat

router = APIRouter(prefix="/api/v1/heartbeat", tags=["organism-heartbeat"])


@router.get("/status")
async def status():
    return heartbeat.status()


@router.post("/beat")
async def beat():
    """Fire a single heartbeat now (cheap — pulse + homeostasis + transformation tick + UEG)."""
    return await heartbeat.beat()


@router.post("/start")
async def start():
    heartbeat.start()
    return {"running": heartbeat.running, "status": "started"}


@router.post("/stop")
async def stop():
    heartbeat.stop()
    return {"running": heartbeat.running, "status": "stopped"}


class ConfigureRequest(BaseModel):
    interval_seconds: Optional[int] = None
    auto_evolve: Optional[bool] = None      # opt-in: run AI evolution cycles autonomously
    auto_economy: Optional[bool] = None     # opt-in: run economy cycles autonomously
    auto_align: Optional[bool] = None       # opt-in: route vision gaps to tiers each beat (cheap)
    auto_compliance: Optional[bool] = None  # opt-in (§11, W288): re-screen living VSBs on the beat
    auto_ship: Optional[bool] = None        # opt-in (§13, W319): re-ship STALE repos on the beat


@router.post("/configure")
async def configure(req: ConfigureRequest):
    heartbeat.configure(req.interval_seconds, req.auto_evolve, req.auto_economy, req.auto_align,
                        auto_compliance=req.auto_compliance, auto_ship=req.auto_ship)
    return heartbeat.status()
