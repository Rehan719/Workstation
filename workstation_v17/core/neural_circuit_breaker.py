"""Neural circuit breaker with state preservation and rollback."""
import asyncio
import logging
from typing import Callable, Any, Dict
from datetime import datetime

logger = logging.getLogger("CircuitBreaker")

class NeuralCircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: int, on_trip: Callable):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.on_trip = on_trip
        self.state = "closed"  # closed, open, half_open
        self.failure_count = 0
        self.last_failure_time = None

    def reset(self):
        self.state = "closed"
        self.failure_count = 0
        self.last_failure_time = None

    async def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        if self.failure_count >= self.failure_threshold and self.state == "closed":
            self.state = "open"
            logger.error(f"Circuit breaker opening after {self.failure_count} failures")
            await self.on_trip()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "open":
            if (datetime.utcnow() - self.last_failure_time).seconds >= self.recovery_timeout:
                self.state = "half_open"
                logger.info("Circuit breaker half-open – attempting recovery")
            else:
                raise RuntimeError("Circuit breaker is open")
        try:
            result = await func(*args, **kwargs)
            if self.state == "half_open":
                self.reset()
                logger.info("Circuit breaker closed after successful recovery")
            return result
        except Exception as e:
            await self.record_failure()
            raise e
