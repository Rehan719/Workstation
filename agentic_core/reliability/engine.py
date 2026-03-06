import asyncio
import logging
from typing import Callable, Any, Dict, Optional

logger = logging.getLogger(__name__)

class ReliabilityEngine:
    """
    ARTICLE 91: Fault tolerance, retry logic, circuit breakers.
    Implements reliability patterns for external service calls and internal dependencies.
    """
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}

    async def execute_with_retry(self, operation: Callable, *args, **kwargs) -> Any:
        """
        Executes an operation with exponential backoff retry logic.
        """
        last_exception = None
        delay = self.retry_delay

        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(operation):
                    return await operation(*args, **kwargs)
                else:
                    return operation(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.max_retries:
                    logger.error(f"ReliabilityEngine: Operation failed after {self.max_retries} retries. Final error: {str(e)}")
                    break

                logger.warning(f"ReliabilityEngine: Attempt {attempt+1} failed. Retrying in {delay:.2f}s. Error: {str(e)}")
                await asyncio.sleep(delay)
                delay *= self.backoff_factor

        raise last_exception

    async def execute_with_circuit_breaker(self, service_name: str, operation: Callable, *args, **kwargs) -> Any:
        """
        Executes an operation protected by a circuit breaker pattern.
        """
        cb = self.circuit_breakers.get(service_name, {"status": "CLOSED", "failure_count": 0, "last_failure_time": 0})

        if cb["status"] == "OPEN":
            # Check if it should transition to HALF_OPEN (after 30 seconds)
            if asyncio.get_event_loop().time() - cb["last_failure_time"] > 30:
                cb["status"] = "HALF_OPEN"
                logger.info(f"ReliabilityEngine: Circuit breaker for {service_name} transitioning to HALF_OPEN.")
            else:
                logger.error(f"ReliabilityEngine: Circuit breaker for {service_name} is OPEN. Blocking request.")
                raise Exception(f"CIRCUIT_BREAKER_OPEN: {service_name}")

        try:
            if asyncio.iscoroutinefunction(operation):
                result = await operation(*args, **kwargs)
            else:
                result = operation(*args, **kwargs)
            # Reset failure count on success
            cb["failure_count"] = 0
            if cb["status"] == "HALF_OPEN":
                cb["status"] = "CLOSED"
                logger.info(f"ReliabilityEngine: Circuit breaker for {service_name} transitioned to CLOSED.")
            self.circuit_breakers[service_name] = cb
            return result
        except Exception as e:
            cb["failure_count"] += 1
            cb["last_failure_time"] = asyncio.get_event_loop().time()

            if cb["failure_count"] >= 5:
                cb["status"] = "OPEN"
                logger.error(f"ReliabilityEngine: Circuit breaker for {service_name} tripped and is now OPEN.")

            self.circuit_breakers[service_name] = cb
            raise e

    def get_service_health(self, service_name: str) -> Dict[str, Any]:
        """
        Returns the health status for a specific service.
        """
        return self.circuit_breakers.get(service_name, {"status": "CLOSED", "failure_count": 0, "last_failure_time": 0})
