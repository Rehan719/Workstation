import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class InterruptHandler:
    """ARTICLE BS-II: Kernel-mode interrupt handlers."""
    def handle_tick(self):
        timestamp_ns = time.perf_counter_ns()
        logger.debug(f"INTERRUPT: Handling tick at {timestamp_ns}")
        return {"tick": timestamp_ns, "status": "SYNCHRONIZED"}

class VetoInterrupt(InterruptHandler):
    def trigger(self, reason: str):
        logger.warning(f"VETO INTERRUPT TRIGGERED: {reason}")
        return {"action": "HALT_NON_CRITICAL", "reason": reason, "time": datetime.now(timezone.utc).isoformat()}
