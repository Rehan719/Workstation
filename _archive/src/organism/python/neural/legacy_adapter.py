import asyncio
import logging
from typing import Dict, Any, TYPE_CHECKING
from agentic_core.nervous_system.nervous_system import NervousSystem
from .event_types import BiomimeticEvent

if TYPE_CHECKING:
    from src.organism.python.neural.event_bus import AsyncEventBus

logger = logging.getLogger(__name__)

class LegacyNervousSystemAdapter:
    def __init__(self, legacy: NervousSystem, event_bus: 'AsyncEventBus'):
        self.legacy = legacy
        self.event_bus = event_bus

    async def process_signal(self, signal: Dict[str, Any]):
        priority = signal.get("priority", "normal")
        delay = 0.4 if priority != "reflex" else 0.042
        await asyncio.sleep(delay)
        event = BiomimeticEvent(
            source="legacy_nervous_system",
            priority=1 if priority == "reflex" else 3
        )
        await self.event_bus.publish(event)
        return {"latency_ms": delay * 1000, "status": "PUBLISHED"}
