import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReflexArc:
    """CP-I & Article 48: Peripheral Nervous System Reflex Arc (<50ms latency)."""

    def process_reflex(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        start_ns = time.perf_counter_ns()

        # Rule-governed, fast response
        response = {"action": "quarantine", "reason": "reflex_trigger"} if stimulus.get("danger") else {"action": "pass"}

        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if latency_ms > 50:
            logger.error(f"NERVOUS: Reflex latency violation! {latency_ms:.2f}ms")
        else:
            logger.debug(f"NERVOUS: Reflex executed in {latency_ms:.2f}ms")

        return {"response": response, "latency_ms": latency_ms}
