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

    def _queue_disclosure(self) -> Dict[str, Any]:
        """W492 (refutation) - "QUEUED" reads as "your task is pending and will run". It is not: this
        queue is an asyncio.Queue on THIS scheduler instance, the optimiser that owns it is constructed
        per request, and nothing anywhere calls get() on it. The task is recorded and then discarded with
        the response. Said here rather than implied by a status word."""
        return {
            "pending": False,
            "queue_depth": self.queue.qsize(),
            "queue_basis": ("queued on this request's own in-process queue, which nothing drains and "
                            "which is discarded when the response returns - the work was NOT scheduled "
                            "for later execution and nothing is pending"),
        }

    async def schedule_task(self, task: Dict[str, Any], tier: str,
                            queued: bool | None = None) -> Dict[str, Any]:
        """
        Schedules a task based on priority and current resource availability.
        """
        # W492 (FU-183/S4.21) - `queued` comes from the tier DECLARATION the allocator resolved, so the
        # scheduling and the share can no longer be inferred separately from the same tier name. The
        # `tier == "free"` fallback remains for direct callers that pass no declaration.
        if queued is None:
            queued = (tier == "free")
        if self.circuit_open and queued:
            logger.warning("Scheduler: Circuit Open. Free-tier task rejected.")
            return {"status": "REJECTED", "reason": "CIRCUIT_BREAKER_ACTIVE"}

        if queued:
            # Check current usage
            if self.monitor:
                usage = self.monitor.get_current_usage()
                if usage.get("api_quota_remaining", 1.0) < (1.0 - self.usage_threshold):
                    logger.warning(f"Scheduler: 80% Usage threshold reached. Activating circuit breaker.")
                    self.circuit_open = True
                    return {"status": "QUEUED", "id": task.get("id"), **self._queue_disclosure()}

            # ARTICLE 310: Mandatory queueing for free-tier to ensure zero-cost compliance
            await self.queue.put(task)
            logger.info(f"Scheduler: Queued {tier}-tier task {task.get('id')} (declared queued)")
            return {"status": "QUEUED", "id": task.get("id"), **self._queue_disclosure()}
        else:
            # High priority / Paid tier
            logger.info(f"Scheduler: Immediate execution for {tier} task {task.get('id')}")
            return {"status": "EXECUTING", "id": task.get("id")}

    def reset_circuit(self):
        self.circuit_open = False
        logger.info("Scheduler: Circuit Breaker Reset.")
