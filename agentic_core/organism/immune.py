"""
IDBO Immune System — error rate monitoring that feeds the organism's health state.

Tracks:
- Failed AI gateway calls per endpoint (sliding 5-minute window)
- HTTP 5xx error counts
- Rate-limit throttle events

Exposes read API for biometrics endpoint to incorporate immune health into organism vitals.
"""
from __future__ import annotations

import time
import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class _ErrorEvent:
    ts: float
    endpoint: str
    error_type: str  # "ai_failure" | "http_5xx" | "rate_limit" | "timeout"


class ImmuneSystem:
    """
    Ring-buffer of error events over a sliding window.
    Thread-safe — called from async FastAPI middleware and gateway.
    """

    WINDOW_SECONDS = 300  # 5-minute sliding window

    def __init__(self):
        self._events: Deque[_ErrorEvent] = deque()
        self._lock = threading.Lock()

    def record(self, endpoint: str, error_type: str = "ai_failure") -> None:
        with self._lock:
            self._events.append(_ErrorEvent(
                ts=time.monotonic(),
                endpoint=endpoint,
                error_type=error_type,
            ))
            self._purge()

    def _purge(self) -> None:
        cutoff = time.monotonic() - self.WINDOW_SECONDS
        while self._events and self._events[0].ts < cutoff:
            self._events.popleft()

    def status(self) -> dict:
        with self._lock:
            self._purge()
            events = list(self._events)

        total = len(events)
        by_type: dict[str, int] = {}
        by_endpoint: dict[str, int] = {}
        for e in events:
            by_type[e.error_type] = by_type.get(e.error_type, 0) + 1
            by_endpoint[e.endpoint] = by_endpoint.get(e.endpoint, 0) + 1

        # Immune health: 1.0 = fully healthy, degrades with error rate
        # 0 errors → 1.0; 10+ errors in window → 0.0
        health = max(0.0, 1.0 - (total / 10.0))

        # Threat level based on health
        if health >= 0.8:
            threat_level = "NOMINAL"
        elif health >= 0.5:
            threat_level = "ELEVATED"
        elif health >= 0.2:
            threat_level = "HIGH"
        else:
            threat_level = "CRITICAL"

        # Most affected endpoint.
        # §4.5 class (W433) — `max(by_endpoint, key=...)` returns the FIRST maximal key in dict
        # order, and these are INTEGER error counts in a 5-minute window, so ties are the norm
        # rather than the exception: two endpoints with one error each made the earlier-inserted one
        # "the most affected". The count was never reported either, so a single stray error read
        # exactly like a genuinely hot endpoint.
        hot_endpoint, hot_errors, hot_tied = None, 0, []
        if by_endpoint:
            hot_errors = max(by_endpoint.values())
            hot_tied = sorted(e for e, n in by_endpoint.items() if n == hot_errors)
            hot_endpoint = hot_tied[0] if len(hot_tied) == 1 else None

        return {
            "health": round(health, 3),
            "threat_level": threat_level,
            # the count travels with the name: one stray error is not a hot endpoint
            "hot_endpoint_errors": hot_errors,
            "hot_endpoint_tied": hot_tied if len(hot_tied) > 1 else [],
            "errors_in_window": total,
            "window_seconds": self.WINDOW_SECONDS,
            "by_type": by_type,
            "hot_endpoint": hot_endpoint,
            "response_playbook": _response_playbook(threat_level),
        }


def _response_playbook(threat_level: str) -> list[str]:
    """W438 — the old field `active_responses` returned constant strings claiming "Adaptive routing
    engaged" / "Fallback providers activated" / "Emergency quarantine mode" when nothing engages,
    activates, or checks any of those — advertising presented as live action. The rename + phrasing
    say what a threat-level lookup can honestly say: the RECOMMENDED posture. The one real response
    that exists (immune_quarantine containment) is CCA-governed and reported by self-healing, not
    invented here."""
    playbook = {
        "NOMINAL": ["recommended: passive surveillance"],
        "ELEVATED": ["recommended: increased monitoring", "recommended: review recent error patterns"],
        "HIGH": ["recommended: throttle metabolic load (CCA immune-reconfigure)",
                 "recommended: review failing endpoints before they trip breakers"],
        "CRITICAL": ["recommended: engage immune_quarantine via POST /api/v1/cca/immune-reconfigure",
                     "recommended: owner review — the organism is under sustained threat"],
    }
    return playbook.get(threat_level, [])


# Singleton — imported by gateway and middleware
immune = ImmuneSystem()
