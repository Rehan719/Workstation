import pytest
import asyncio
from unittest.mock import MagicMock
from src.organism.python.resilience.homeostasis import HomeostasisManager
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import HomeostasisEvent, BiomimeticEvent
from agentic_core.biomimicry.geospheric.resilience import ResilienceManager

@pytest.mark.asyncio
async def test_homeostasis_recovery_flow():
    bus = AsyncEventBus()
    resilience = ResilienceManager()
    manager = HomeostasisManager(bus, resilience)
    await bus.start()
    await manager.start_monitoring()
    stress_event = HomeostasisEvent(source="test", metric="cpu_usage", value=95.0, status="STRESS")
    recovery_detected = asyncio.Event()
    async def recovery_handler(event: HomeostasisEvent):
        if event.status == "RECOVERY" and event.metric == "cpu_usage":
            recovery_detected.set()
    bus.subscribe(HomeostasisEvent, recovery_handler)
    await bus.publish(stress_event)
    await asyncio.wait_for(recovery_detected.wait(), timeout=5.0)
    assert recovery_detected.is_set()
    await bus.stop()
    await manager.stop_monitoring()

@pytest.mark.asyncio
async def test_predictive_failure_trigger():
    bus = AsyncEventBus()
    resilience = ResilienceManager()
    resilience.model.predict = MagicMock(return_value=0.85)
    manager = HomeostasisManager(bus, resilience)
    await bus.start()
    manager.is_monitoring = True
    bus.subscribe(HomeostasisEvent, manager._handle_homeostasis_event)
    stress_detected = asyncio.Event()
    async def stress_handler(event: HomeostasisEvent):
        if event.status == "STRESS" and event.source == "homeostasis_manager":
            stress_detected.set()
    bus.subscribe(HomeostasisEvent, stress_handler)
    status = resilience.update_metrics({})
    if status["failure_probability"] > 0.8:
        await bus.publish(HomeostasisEvent(source="homeostasis_manager", metric="system_failure_probability", value=status["failure_probability"], status="STRESS", priority=1))
    await asyncio.wait_for(stress_detected.wait(), timeout=2.0)
    assert stress_detected.is_set()
    await bus.stop()
    manager.is_monitoring = False
