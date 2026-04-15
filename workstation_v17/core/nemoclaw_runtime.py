import logging
import asyncio
from typing import Callable, Any

class NemoclawRuntime:
    """
    IDBO Layer 5 Resilience Interceptor.
    Neural circuit breakers and runtime policy enforcement.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("Nemoclaw")
        self.failure_counter = 0
        self.tripped = False

    async def execute_tool(self, func: Callable, *args, **kwargs) -> Any:
        """
        Intercepts tool invocation and enforces safety policies.
        """
        if self.tripped:
            self.logger.critical("Nemoclaw: CIRCUIT BREAKER TRIPPED. Execution halted.")
            raise RuntimeError("Circuit breaker is OPEN.")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            return result
        except Exception as e:
            self.failure_counter += 1
            if self.failure_counter >= 3:
                self.tripped = True
            self.logger.error(f"Nemoclaw: Tool failure detected. Counter: {self.failure_counter}")
            raise e

    def reset_breaker(self):
        self.tripped = False
        self.failure_counter = 0
