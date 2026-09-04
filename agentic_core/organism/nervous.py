"""
IDBO Nervous System — event routing and signal propagation.

Maps the biological nervous system to real system events:
  - Sensory neurons  → incoming requests (system receives signals)
  - Motor neurons    → outgoing AI responses (system acts)
  - Synaptic relay   → WebSocket broadcast to connected clients
  - Reflex arcs      → auto-triggered responses to threshold events

The nervous system sits above the cardiovascular (CPU/memory) and immune
(error tracking) systems, routing signals and triggering adaptive responses.

Exposed via:
  GET  /api/v1/organism/nervous/status   — current nervous system state
  GET  /api/v1/organism/nervous/signals  — last N signals received
  POST /api/v1/organism/nervous/stimulate — manually inject a signal (testing/demo)
"""
from __future__ import annotations

import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Callable, Literal

from fastapi import APIRouter, Depends

from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])


@dataclass
class Signal:
    ts: float
    signal_type: str    # "sensory" | "motor" | "reflex" | "cognitive"
    source: str         # endpoint or agent name
    payload: str        # brief description
    intensity: float    # 0.0–1.0


class NervousSystem:
    """
    Event bus that records all system signals and propagates them.
    Thread-safe ring buffer. Reflex arcs fire callbacks when thresholds crossed.
    """

    SIGNAL_WINDOW = 200  # keep last 200 signals

    def __init__(self):
        self._signals: Deque[Signal] = deque(maxlen=self.SIGNAL_WINDOW)
        self._lock = threading.Lock()
        self._reflex_arcs: list[dict] = []  # {trigger_type, threshold, callback, name}
        # W438 — totals count EVERY type dynamically: the old three named counters silently
        # omitted the whole "cognitive" class (fired by 12+ live sites), so a field named
        # total_signals claimed a totality it did not have
        self._totals: dict[str, int] = {}
        self._process_started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def fire(self, signal_type: str, source: str, payload: str = "", intensity: float = 0.5) -> None:
        sig = Signal(
            ts=time.monotonic(),
            signal_type=signal_type,
            source=source,
            payload=payload,
            intensity=max(0.0, min(1.0, intensity)),
        )
        with self._lock:
            self._signals.append(sig)
            self._totals[signal_type] = self._totals.get(signal_type, 0) + 1

        # Check reflex arcs (outside lock to avoid deadlock in callbacks)
        self._check_reflexes(sig)

    def register_reflex(self, name: str, trigger_type: str, threshold: int,
                        callback: Callable[[Signal], None]) -> None:
        """Register a reflex arc that fires when threshold signals of trigger_type accumulate."""
        self._reflex_arcs.append({
            "name": name,
            "trigger_type": trigger_type,
            "threshold": threshold,
            "callback": callback,
            "last_fired": 0.0,
            "cooldown": 60.0,  # won't fire more than once per minute
        })

    def _check_reflexes(self, signal: Signal) -> None:
        now = time.monotonic()
        recent_cutoff = now - 60.0  # last 60 seconds
        with self._lock:
            signals_snap = list(self._signals)

        for arc in self._reflex_arcs:
            if signal.signal_type != arc["trigger_type"]:
                continue
            if now - arc["last_fired"] < arc["cooldown"]:
                continue
            recent_count = sum(
                1 for s in signals_snap
                if s.signal_type == arc["trigger_type"] and s.ts > recent_cutoff
            )
            if recent_count >= arc["threshold"]:
                arc["last_fired"] = now
                try:
                    arc["callback"](signal)
                except Exception:
                    pass

    def recent_signals(self, n: int = 50) -> list[dict]:
        with self._lock:
            signals = list(self._signals)[-n:]
        now = time.monotonic()
        return [
            {
                "age_seconds": round(now - s.ts, 1),
                "signal_type": s.signal_type,
                "source": s.source,
                "payload": s.payload,
                "intensity": s.intensity,
            }
            for s in reversed(signals)
        ]

    def status(self) -> dict:
        with self._lock:
            signals = list(self._signals)

        now = time.monotonic()
        recent_60s = [s for s in signals if s.ts > now - 60]
        recent_by_type: dict[str, int] = {}
        for s in recent_60s:
            recent_by_type[s.signal_type] = recent_by_type.get(s.signal_type, 0) + 1

        # Signal rate
        signal_rate = len(recent_60s) / 60.0  # signals per second

        # Arousal state based on signal rate
        if signal_rate > 2.0:
            arousal = "HYPERACTIVE"
        elif signal_rate > 0.5:
            arousal = "ALERT"
        elif signal_rate > 0.1:
            arousal = "RESTING"
        else:
            arousal = "DORMANT"

        return {
            "arousal_state": arousal,
            # the thresholds behind the arousal label, so the verdict is re-derivable
            "arousal_thresholds": {"HYPERACTIVE": "> 2.0/s", "ALERT": "> 0.5/s",
                                   "RESTING": "> 0.1/s", "DORMANT": "<= 0.1/s"},
            "signal_rate_per_second": round(signal_rate, 3),
            "signals_last_60s": len(recent_60s),
            "by_type_last_60s": recent_by_type,
            "total_signals": dict(self._totals),
            "reflex_arcs_registered": len(self._reflex_arcs),
            "buffer_size": len(signals),
            "buffer_capacity": self.SIGNAL_WINDOW,
            "scope": "in-memory, this server process since start",
            "process_started_at": self._process_started_at,
        }


# Singleton
nervous = NervousSystem()


# ── API endpoints ─────────────────────────────────────────────────────────────

@router.get("/nervous/status")
async def nervous_status():
    return nervous.status()


@router.get("/nervous/signals")
async def nervous_signals(n: int = 50):
    # W438 — `count` used to echo the REQUESTED cap (7 stored signals, n=50 -> count 50), and
    # n=0 / negative n produced absurd slices; count is now what was actually returned
    requested = n
    n = max(1, min(n, 200))
    sigs = nervous.recent_signals(n)
    # `requested` carries the caller's RAW value (a field named requested holding the post-clamp
    # value was the name-vs-content cousin); `limit` is what was actually applied
    return {"signals": sigs, "count": len(sigs), "requested": requested, "limit": n}


from pydantic import BaseModel, Field

class StimulateRequest(BaseModel):
    signal_type: Literal["sensory", "motor", "reflex", "cognitive"] = "sensory"
    source: str = "manual"
    payload: str = ""
    intensity: float = Field(default=0.5, ge=0.0, le=1.0)


@router.post("/nervous/stimulate")
async def stimulate(req: StimulateRequest,
                    user: dict | None = Depends(get_current_user)):
    """Manually inject a signal — testing/demonstration. The injection is honest about itself:
    the recorded source is always prefixed `manual:` so an injected signal can never masquerade
    as an organic one in the feed, and the type is validated against the four real classes."""
    source = req.source if req.source.startswith("manual") else f"manual:{req.source}"
    nervous.fire(req.signal_type, source, req.payload, req.intensity)
    return {"fired": True, "signal_type": req.signal_type, "source": source,
            "note": "manually injected — the recorded source always begins with 'manual'"}
