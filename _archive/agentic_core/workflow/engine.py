import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EventBus:
    """ARTICLE 285: Global cross-domain event bus."""
    def __init__(self):
        self.subscribers = {}
        self.history = []

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: Dict[str, Any]):
        logger.info(f"EventBus: Publishing event {event_type}")
        self.history.append({"type": event_type, "data": data, "ts": datetime.now().isoformat()})

        if event_type in self.subscribers:
            for cb in self.subscribers[event_type]:
                await cb(data)

class WorkflowEngine:
    """ARTICLE 285: Declarative cross-domain workflow execution."""
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.workflows = {}

    def register_workflow(self, name: str, steps: List[Dict[str, Any]]):
        self.workflows[name] = steps
        logger.info(f"WorkflowEngine: Registered workflow '{name}'")

    async def trigger_workflow(self, name: str, initial_data: Dict[str, Any]):
        if name not in self.workflows:
             logger.error(f"Workflow {name} not found.")
             return

        logger.info(f"WorkflowEngine: Executing '{name}'...")
        current_data = initial_data

        for step in self.workflows[name]:
            # Simulate step execution (e.g., calling a reactor API)
            logger.info(f"Workflow {name}: Executing step {step['id']} -> {step['action']}")
            await asyncio.sleep(0.1)
            current_data[step["id"]] = "STEP_SUCCESS"

        return current_data
