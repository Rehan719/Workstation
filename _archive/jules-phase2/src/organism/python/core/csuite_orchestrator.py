import logging
from typing import Dict, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.organism.python.neural.event_bus import AsyncEventBus
    from src.organism.python.core.state_kernel import SovereignState

from src.organism.python.neural.event_types import (
    IntentGenerated, GovernanceValidated, ActionExecuted
)

logger = logging.getLogger(__name__)

class CSuiteOrchestrator:
    """
    Central coordination layer embodying AI CEO logic.
    Routes intents through validation to execution.
    """
    def __init__(self, event_bus: 'AsyncEventBus', state_kernel: 'SovereignState'):
        self.event_bus = event_bus
        self.state_kernel = state_kernel
        self.organs: Dict[str, Any] = {}
        self.is_running = False

    async def initialize_organs(self, nematron: Any, nemoclaw: Any, openclaw: Any):
        """Initializes and connects the three core organs."""
        logger.info("CSuiteOrchestrator: Awakening Organs...")

        self.organs['nematron'] = nematron
        self.organs['nemoclaw'] = nemoclaw
        self.organs['openclaw'] = openclaw

        # Subscribe to canonical flow events
        self.event_bus.subscribe(IntentGenerated, self._handle_intent)
        self.event_bus.subscribe(GovernanceValidated, self._handle_validation)
        self.event_bus.subscribe(ActionExecuted, self._handle_execution)

        self.is_running = True
        logger.info("CSuiteOrchestrator: Organs functional.")

    async def _handle_intent(self, event: IntentGenerated):
        """Phase 1: Intent Received → Route to Validation (Nemoclaw)"""
        if event.source == "nemoclaw" or event.source == "openclaw":
             return

        logger.info(f"CSuiteOrchestrator: Routing Intent '{event.intent.goal}' from {event.source} to Nemoclaw validation.")
        await self.organs['nemoclaw'].validate_action(event)

    async def _handle_validation(self, event: GovernanceValidated):
        """Phase 2: Validation Received → If Passed, Route to Execution (OpenClaw)"""
        if event.validation_result.is_valid:
            logger.info(f"CSuiteOrchestrator: Validation PASSED for action {event.action_id}. Dispatching to OpenClaw.")
            await self.organs['openclaw'].execute_action(
                action_id=event.action_id,
                tool_name="DEFAULT_TOOL",
                parameters={"intent_id": event.action_id}
            )
        else:
            logger.warning(f"CSuiteOrchestrator: Validation FAILED for action {event.action_id}: {event.validation_result.reason}")

    async def _handle_execution(self, event: ActionExecuted):
        """Phase 3: Execution Result → Update State and Notify System"""
        status = event.result.status
        logger.info(f"CSuiteOrchestrator: Action {event.action_id} completed with status: {status}")

        await self.state_kernel.set_value(
            session_id=event.action_id,
            key="execution_result",
            value=event.result.output
        )

    async def shutdown_organs(self):
        """Gracefully shuts down the organism's organs."""
        self.is_running = False
        logger.info("CSuiteOrchestrator: Shutting down organs...")

    async def health_check(self) -> Dict[str, Any]:
        """Returns the health status of all organs."""
        return {
            "status": "HEALTHY" if self.is_running else "OFFLINE",
            "organs": {name: "ACTIVE" for name in self.organs},
            "timestamp": datetime.now().isoformat()
        }
