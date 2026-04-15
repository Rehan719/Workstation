import logging
import time
from typing import Dict, Any, Optional, Callable, Awaitable

logger = logging.getLogger("CircuitBreaker")

class CircuitBreaker:
    """
    ARTICLE 5.1: Constitutional Circuit Breaker for agentic execution.
    Halts execution on constitutional violations or high error rates.
    """
    def __init__(self, domain: str, threshold: float = 0.2, window_seconds: int = 300):
        self.domain = domain
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.errors = [] # List of (timestamp, is_violation)
        self.is_tripped = False
        self.trip_reason = None

    def record_event(self, success: bool, is_violation: bool = False):
        """Records an execution event."""
        now = time.time()
        self.errors.append((now, success, is_violation))
        self._cleanup()

        if is_violation:
            self.trip(f"Constitutional violation detected in {self.domain}")

        error_rate = self.get_error_rate()
        if error_rate > self.threshold:
            self.trip(f"Error rate {error_rate:.2f} exceeded threshold {self.threshold}")

    def get_error_rate(self) -> float:
        self._cleanup()
        if not self.errors:
            return 0.0
        failures = [e for e in self.errors if not e[1]]
        return len(failures) / len(self.errors)

    def _cleanup(self):
        now = time.time()
        self.errors = [e for e in self.errors if now - e[0] < self.window_seconds]

    def trip(self, reason: str):
        self.is_tripped = True
        self.trip_reason = reason
        logger.error(f"CIRCUIT BREAKER TRIPPED: {reason}")

    def reset(self):
        self.is_tripped = False
        self.trip_reason = None
        self.errors = []
        logger.info(f"Circuit breaker for {self.domain} reset.")

    def should_halt(self) -> bool:
        return self.is_tripped
