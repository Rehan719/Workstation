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
                 window_seconds: int = 300, base_threshold: float = 0.2,
                 violation_trip_count: int = 2):
        self.ueg = ueg
        self.domain = domain
        self.window_seconds = window_seconds
        self.threshold = base_threshold
        # W505 (FU-007) — how many violations inside the window trip the breaker. It used to be one, with no
        # threshold, on a breaker SHARED by every action on the node: a single keyword match in one generated
        # answer halted the whole node until somebody reset it by hand. A caller that knows a breach is
        # severe still trips on the first one by saying so (`severe=True`).
        self.violation_trip_count = max(1, int(violation_trip_count))
        self.history: List[Dict[str, Any]] = []
        self.is_tripped = False
        self.trip_reason: Optional[str] = None

    # ── telemetry ───────────────────────────────────────────────────────────
    def record_event(self, success: bool, is_violation: bool = False,
                     severe: bool = False, escalation: bool = False) -> None:
        """Record one outcome. `escalation` marks an action that did not run because a human approval is
        outstanding: kept in the history so it is auditable, and excluded from the error rate.

        W505 (FU-007, second pass) — the first pass stopped recording an escalation as a violation and still
        recorded it as `success=False`, so the ERROR-RATE branch below tripped instead: one event in the window
        makes the rate 1.00 against a 0.20 threshold, and the node was halted exactly as before. An action
        waiting for a person is neither an error nor a success, and counting it as an error poisons the measure
        that exists to detect things going wrong.
        """
        self.history.append({"time": time.time(), "success": success, "violation": is_violation,
                             "severe": bool(is_violation and severe), "escalation": bool(escalation)})
        self._cleanup()
        if escalation:
            logger.info("BREAKER [%s]: an action is awaiting human approval — recorded, not counted as an "
                        "error, and the node stays usable", self.domain)
            return

        if is_violation:
            # A violation ALWAYS tightens the threshold and is always in the window; whether it trips the
            # shared breaker on its own depends on whether the caller declared it severe.
            self._tune_threshold()
            n = self.violations_in_window()
            if severe:
                self.trip(f"Severe constitutional violation in '{self.domain}' (tripped on the first)")
            elif n >= self.violation_trip_count:
                self.trip(f"{n} constitutional violations in '{self.domain}' within "
                          f"{self.window_seconds}s (trip count {self.violation_trip_count})")
            else:
                logger.warning("BREAKER [%s]: violation %d of %d in window; threshold tightened to %.3f, "
                               "not tripped", self.domain, n, self.violation_trip_count, self.threshold)
            return

        self._tune_threshold()
        rate = self.error_rate()
        if rate > self.threshold:
            self.trip(f"Error rate {rate:.2f} exceeds self-tuned threshold {self.threshold:.2f}")

    def violations_in_window(self) -> int:
        """How many violations are inside the rolling window right now."""
        return sum(1 for e in self.history if e.get("violation"))

    def error_rate(self) -> float:
        """Failures over the ATTEMPTS in the window. W505 (FU-007) — escalations are excluded from both sides:
        an action awaiting a human approval never ran, so it is not evidence either way about whether this
        domain is working."""
        attempts = [e for e in self.history if not e.get("escalation")]
        if not attempts:
            return 0.0
        failures = sum(1 for e in attempts if not e["success"])
        return failures / len(attempts)

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
            # W505 (FU-007) — what it would take to trip, said rather than implied. A reader could not tell
            # from the old state dict that one violation was enough.
            "violations_in_window": self.violations_in_window(),
            "escalations_in_window": sum(1 for e in self.history if e.get("escalation")),
            "error_rate_basis": ("failures over the attempts in the window; escalations (actions awaiting a "
                                 "human approval) are in the history and counted on neither side"),
            "violation_trip_count": self.violation_trip_count,
            "trips_on_first_violation_only_if_declared_severe": True,
        }
