import logging
import asyncio
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class CostAwareScheduler:
    """
    ARTICLE 311: Cost-Aware Scheduler.
    Enforces zero-cost constraints for free tiers.
    Includes circuit breakers for API quotas.
    """
    def __init__(self, monitor: Optional[Any] = None):
        self.queue = asyncio.Queue()
        self.monitor = monitor
        self.circuit_open = False
        self.usage_threshold = 0.80 # Alert at 80% usage

    async def schedule_task(self, task: Dict[str, Any], tier: str) -> Dict[str, Any]:
        """
        Schedules a task based on priority and current resource availability.
        """
        if self.circuit_open and tier == "free":
            logger.warning("Scheduler: Circuit Open. Free-tier task rejected.")
            return {"status": "REJECTED", "reason": "CIRCUIT_BREAKER_ACTIVE"}

        if tier == "free":
            # Check current usage
            if self.monitor:
                usage = self.monitor.get_current_usage()
                if usage.get("api_quota_remaining", 1.0) < (1.0 - self.usage_threshold):
                    logger.warning(f"Scheduler: 80% Usage threshold reached. Activating circuit breaker.")
                    self.circuit_open = True
                    return {"status": "QUEUED", "id": task.get("id")}

            # ARTICLE 310: Mandatory queueing for free-tier to ensure zero-cost compliance
            await self.queue.put(task)
            logger.info(f"Scheduler: Queued free-tier task {task.get('id')}")
            return {"status": "QUEUED", "id": task.get("id")}
        else:
            # High priority / Paid tier
            logger.info(f"Scheduler: Immediate execution for {tier} task {task.get('id')}")
            return {"status": "EXECUTING", "id": task.get("id")}

    def reset_circuit(self):
        self.circuit_open = False
        logger.info("Scheduler: Circuit Breaker Reset.")
