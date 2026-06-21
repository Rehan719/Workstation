"""
Self-Tuning Circuit Breaker (RL) — GaaS v5.

Article 5.2. A circuit breaker whose error-rate threshold adapts from telemetry:
sustained clean operation gradually relaxes the threshold (fewer false
positives), while *any* constitutional violation tightens it (zero tolerance for
false negatives). Trips are recorded to the UEG for auditability.
"""
from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("gaas.v5.breaker")


class SelfTuningCircuitBreaker:
    """RL-tuned error-rate breaker with a rolling telemetry window."""

    def __init__(self, ueg: Any = None, domain: str = "global",
                 window_seconds: int = 300, base_threshold: float = 0.2):
        self.ueg = ueg
        self.domain = domain
        self.window_seconds = window_seconds
        self.threshold = base_threshold
        self.history: List[Dict[str, Any]] = []
        self.is_tripped = False
        self.trip_reason: Optional[str] = None

    # ── telemetry ───────────────────────────────────────────────────────────
    def record_event(self, success: bool, is_violation: bool = False) -> None:
        self.history.append({"time": time.time(), "success": success, "violation": is_violation})
        self._cleanup()

        if is_violation:
            self.trip(f"Constitutional violation in '{self.domain}'")
            return

        self._tune_threshold()
        rate = self.error_rate()
        if rate > self.threshold:
            self.trip(f"Error rate {rate:.2f} exceeds self-tuned threshold {self.threshold:.2f}")

    def error_rate(self) -> float:
        if not self.history:
            return 0.0
        failures = sum(1 for e in self.history if not e["success"])
        return failures / len(self.history)

    def _cleanup(self) -> None:
        cutoff = time.time() - self.window_seconds
        self.history = [e for e in self.history if e["time"] >= cutoff]

    def _tune_threshold(self) -> None:
        """Reinforcement-style tuning: reward clean streaks, punish violations."""
        if len(self.history) <= 50:
            return
        successes = sum(1 for e in self.history if e["success"])
        violations = sum(1 for e in self.history if e["violation"])
        if violations == 0 and successes > 40:
            self.threshold = min(0.35, self.threshold + 0.005)
        elif violations > 0:
            self.threshold = max(0.10, self.threshold - 0.01)

    # ── state machine ─────────────────────────────────────────────────────
    def trip(self, reason: str) -> None:
        self.is_tripped = True
        self.trip_reason = reason
        logger.error("SELF-TUNING BREAKER TRIPPED [%s]: %s", self.domain, reason)
        if self.ueg is not None:
            try:
                self.ueg.log_circuit_breaker_trip(self.domain, reason, self.state())
            except Exception:  # logging must never break the breaker
                pass

    def should_halt(self) -> bool:
        return self.is_tripped

    async def check_health(self, record: bool = False) -> bool:
        """Return True when the breaker is healthy (not tripped). Optionally record a probe."""
        if record:
            self.record_event(success=not self.is_tripped)
        return not self.is_tripped

    def reset(self) -> None:
        self.is_tripped = False
        self.trip_reason = None
        self.history.clear()

    def state(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "tripped": self.is_tripped,
            "reason": self.trip_reason,
            "threshold": round(self.threshold, 4),
            "error_rate": round(self.error_rate(), 4),
            "events_in_window": len(self.history),
        }
