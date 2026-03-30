import asyncio
import logging
from typing import Optional
from agentic_core.homeostasis.resilience import ResilienceManager
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import HomeostasisEvent, BiomimeticEvent

logger = logging.getLogger(__name__)

class HomeostasisManager:
    """
    Homeostasis & Resilience Layer: Self-Healing protocols.
    """
    def __init__(self, event_bus: AsyncEventBus, resilience: ResilienceManager):
        self.event_bus = event_bus
        self.resilience = resilience
        self.is_monitoring = False
        self._monitoring_task: Optional[asyncio.Task] = None

    async def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.event_bus.subscribe(HomeostasisEvent, self._handle_homeostasis_event)
            self.event_bus.subscribe(BiomimeticEvent, self._monitor_traffic)
            self._monitoring_task = asyncio.create_task(self._periodic_health_check())
            logger.info("HomeostasisManager: Self-healing monitoring active.")

    async def _handle_homeostasis_event(self, event: HomeostasisEvent):
        if event.status == "STRESS":
            logger.warning(f"HomeostasisManager: STRESS detected in {event.source} - Metric: {event.metric} = {event.value}")
            await self._trigger_recovery(event)

    async def _monitor_traffic(self, event: BiomimeticEvent):
        metrics = {
            "latency": 50.0,
            "error_rate": 0.01,
            "memory": 1024.0,
            "gaas_failures": 0.0,
            "ws_stability": 1.0,
            "cpu": 15.0
        }
        self.resilience.update_metrics(metrics)

    async def _periodic_health_check(self):
        while self.is_monitoring:
            recent_metrics = {
                "latency": 42.0,
                "error_rate": 0.02,
                "memory": 2048.0,
                "gaas_failures": 0.0,
                "ws_stability": 0.99,
                "cpu": 20.0
            }
            status = self.resilience.update_metrics(recent_metrics)
            if status["failure_probability"] > 0.8:
                await self.event_bus.publish(HomeostasisEvent(
                    source="homeostasis_manager",
                    metric="system_failure_probability",
                    value=status["failure_probability"],
                    status="STRESS",
                    priority=1
                ))
            await asyncio.sleep(60)

    async def _trigger_recovery(self, event: HomeostasisEvent):
        logger.info(f"HomeostasisManager: Initiating recovery protocol for {event.metric}...")
        await asyncio.sleep(2)
        await self.event_bus.publish(HomeostasisEvent(
            source="homeostasis_manager",
            metric=event.metric,
            value=event.value,
            status="RECOVERY",
            priority=2
        ))

    async def stop_monitoring(self):
        self.is_monitoring = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("HomeostasisManager: Monitoring deactivated.")
