"""
IDBO Self-Healing System — circuit-breaker pattern for endpoint health.

When an endpoint fails repeatedly, the circuit opens and returns a graceful
degraded response rather than hammering a broken provider.

States:
  CLOSED   — normal operation, requests pass through
  OPEN     — too many failures, requests short-circuit immediately
  HALF_OPEN — testing recovery, one request allowed through

Also provides the /api/v1/organism/self-healing/status endpoint.
"""
from __future__ import annotations

import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/organism", tags=["idbo-organism"])


@dataclass
class _CircuitState:
    failures: int = 0
    last_failure: float = 0.0
    state: str = "CLOSED"   # CLOSED | OPEN | HALF_OPEN
    last_success: float = field(default_factory=time.monotonic)
    total_calls: int = 0
    total_failures: int = 0


class SelfHealingSystem:
    """
    Per-endpoint circuit breaker.

    Thresholds (configurable):
      failure_threshold  — failures within window before opening (default 5)
      window_seconds     — rolling window to count failures in (default 60)
      recovery_timeout   — seconds to wait in OPEN before trying HALF_OPEN (default 30)
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        window_seconds: float = 60.0,
        recovery_timeout: float = 30.0,
    ):
        self._threshold = failure_threshold
        self._window = window_seconds
        self._recovery = recovery_timeout
        self._circuits: dict[str, _CircuitState] = defaultdict(_CircuitState)
        self._lock = threading.Lock()
        self._healing_log: list[dict] = []  # last 50 healing events

    def record_success(self, endpoint: str) -> None:
        with self._lock:
            c = self._circuits[endpoint]
            c.total_calls += 1
            c.last_success = time.monotonic()
            if c.state in ("OPEN", "HALF_OPEN"):
                c.state = "CLOSED"
                c.failures = 0
                self._log_event(endpoint, "CLOSED", "Circuit recovered after successful call")

    def record_failure(self, endpoint: str) -> None:
        with self._lock:
            c = self._circuits[endpoint]
            c.total_calls += 1
            c.total_failures += 1
            now = time.monotonic()

            # Reset failure count if outside window
            if now - c.last_failure > self._window:
                c.failures = 0

            c.failures += 1
            c.last_failure = now

            if c.state == "CLOSED" and c.failures >= self._threshold:
                c.state = "OPEN"
                self._log_event(endpoint, "OPEN", f"{c.failures} failures in {self._window}s window")
            elif c.state == "HALF_OPEN":
                c.state = "OPEN"
                self._log_event(endpoint, "OPEN", "Half-open test failed — re-opening circuit")

    def is_open(self, endpoint: str) -> bool:
        with self._lock:
            c = self._circuits[endpoint]
            if c.state == "OPEN":
                # Try half-open after recovery timeout
                if time.monotonic() - c.last_failure > self._recovery:
                    c.state = "HALF_OPEN"
                    self._log_event(endpoint, "HALF_OPEN", "Testing recovery")
                    return False  # allow one request through
                return True
            return False

    def attempt_heal(self) -> dict:
        """Proactive self-healing: actively probe circuits that have been OPEN past the recovery window
        (flip them to HALF_OPEN so the next call tests recovery) rather than only waiting passively for the
        next request to trigger it. Called autonomously on the circadian heartbeat — the immune→self-healing
        reflex (§3 'defends and heals itself'). Returns which circuits were probed."""
        probed: list[str] = []
        with self._lock:
            now = time.monotonic()
            for ep, c in self._circuits.items():
                if c.state == "OPEN" and now - c.last_failure > self._recovery:
                    c.state = "HALF_OPEN"
                    self._log_event(ep, "HALF_OPEN", "Proactive heal — organism probing recovery (heartbeat)")
                    probed.append(ep)
        return {"probed": probed, "count": len(probed)}

    def _log_event(self, endpoint: str, new_state: str, reason: str) -> None:
        self._healing_log.append({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "endpoint": endpoint,
            "state": new_state,
            "reason": reason,
        })
        if len(self._healing_log) > 50:
            self._healing_log.pop(0)

    def status(self) -> dict:
        with self._lock:
            circuits = {}
            for ep, c in self._circuits.items():
                # Refresh OPEN → HALF_OPEN check
                state = c.state
                if state == "OPEN" and time.monotonic() - c.last_failure > self._recovery:
                    state = "HALF_OPEN (pending test)"
                circuits[ep] = {
                    "state": state,
                    "failures_in_window": c.failures,
                    "total_failures": c.total_failures,
                    "total_calls": c.total_calls,
                    "failure_rate": round(c.total_failures / c.total_calls, 3) if c.total_calls else 0.0,
                }

            open_count = sum(1 for c in circuits.values() if "OPEN" in c["state"])
            health = max(0.0, 1.0 - (open_count / max(len(circuits), 1)))

            return {
                "overall_health": round(health, 3),
                "circuits": circuits,
                "open_circuits": open_count,
                "healing_log": self._healing_log[-10:],  # last 10 events
                "thresholds": {
                    "failure_threshold": self._threshold,
                    "window_seconds": self._window,
                    "recovery_timeout": self._recovery,
                },
            }


# Singleton
self_healer = SelfHealingSystem()


# ── Status endpoint ───────────────────────────────────────────────────────────

@router.get("/self-healing/status")
async def self_healing_status():
    """Return circuit breaker status for all tracked endpoints."""
    return self_healer.status()


@router.get("/self-healing/log")
async def self_healing_log():
    """Return the last 50 healing events."""
    return {"events": self_healer._healing_log, "total": len(self_healer._healing_log)}
