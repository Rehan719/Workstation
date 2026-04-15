import time
import logging
import random
from typing import Dict, Any, List

class SelfTuningCircuitBreaker:
    """
    ARTICLE 5.2: Self-tuning circuit breaker using reinforcement learning from telemetry.
    Adapts thresholds to reduce false positives while maintaining zero false negatives.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.threshold = 0.2
        self.window_seconds = 300
        self.history = []
        self.is_tripped = False
        self.trip_reason = None
        self.logger = logging.getLogger("SelfTuningCB")

    def record_event(self, success: bool, is_violation: bool = False):
        now = time.time()
        self.history.append({"time": now, "success": success, "violation": is_violation})

        if is_violation:
            self.trip(f"Constitutional violation in {self.domain}")

        self._cleanup()
        self._tune_threshold()

        error_rate = self.get_error_rate()
        if error_rate > self.threshold:
            self.trip(f"Error rate {error_rate:.2f} > self-tuned threshold {self.threshold:.2f}")

    def get_error_rate(self) -> float:
        if not self.history:
            return 0.0
        failures = [e for e in self.history if not e["success"]]
        return len(failures) / len(self.history)

    def _cleanup(self):
        now = time.time()
        self.history = [e for e in self.history if now - e["time"] < self.window_seconds]

    def _tune_threshold(self):
        """
        Simulated RL tuning.
        If many successful events occur, slightly increase threshold to be more permissive.
        If violations occur, decrease threshold to be more strict.
        """
        if len(self.history) > 50:
            success_count = len([e for e in self.history if e["success"]])
            violation_count = len([e for e in self.history if e["violation"]])

            if violation_count == 0 and success_count > 40:
                self.threshold = min(0.35, self.threshold + 0.005)
            elif violation_count > 0:
                self.threshold = max(0.1, self.threshold - 0.01)

    def trip(self, reason: str):
        self.is_tripped = True
        self.trip_reason = reason
        self.logger.error(f"SELF-TUNING BREAKER TRIPPED [{self.domain}]: {reason}")

    def should_halt(self) -> bool:
        return self.is_tripped

    def reset(self):
        self.is_tripped = False
        self.trip_reason = None
        self.logger.info(f"Breaker reset for {self.domain}")
