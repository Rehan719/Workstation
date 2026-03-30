import pytest
import asyncio
from unittest.mock import MagicMock
from src.organism.python.core.csuite_orchestrator import CSuiteOrchestrator
from src.organism.python.core.state_kernel import SovereignState
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    IntentGenerated, GovernanceValidated, ActionExecuted,
    StrategicIntent, ValidationResult, ExecutionResult
)

@pytest.mark.asyncio
async def test_orchestrator_flow():
    bus = AsyncEventBus()
    state = SovereignState(storage_dir="data/test_state")
    orchestrator = CSuiteOrchestrator(bus, state)
    nematron = MagicMock()
    nemoclaw = MagicMock()
    openclaw = MagicMock()
    await bus.start()
    await orchestrator.initialize_organs(nematron, nemoclaw, openclaw)
    intent = StrategicIntent("Deploy App", "DEPLOY", {"version": "1.0.0"}, "Auto-deploy")
    await bus.publish(IntentGenerated(id="action-123", intent=intent, source="nematron"))
    await bus.publish(GovernanceValidated(action_id="action-123", validation_result=ValidationResult(True, "All good", "ZK_001")))
    await bus.publish(ActionExecuted(action_id="action-123", result=ExecutionResult("SUCCESS", {"url": "https://workstation.ai"})))
    await asyncio.sleep(0.5)
    restored = await state.restore_session("action-123")
    assert restored["execution_result"] == {"url": "https://workstation.ai"}
    await bus.stop()
    await orchestrator.shutdown_organs()

@pytest.mark.asyncio
async def test_orchestrator_validation_failure():
    bus = AsyncEventBus()
    state = SovereignState(storage_dir="data/test_state")
    orchestrator = CSuiteOrchestrator(bus, state)
    nematron = MagicMock()
    nemoclaw = MagicMock()
    openclaw = MagicMock()
    await bus.start()
    await orchestrator.initialize_organs(nematron, nemoclaw, openclaw)
    intent = StrategicIntent("Delete Prod", "DELETE", {"target": "prod"}, "Accident")
    await bus.publish(IntentGenerated(id="action-fail", intent=intent, source="nematron"))
    await bus.publish(GovernanceValidated(action_id="action-fail", validation_result=ValidationResult(False, "Unauthorized action")))
    await asyncio.sleep(0.3)
    restored = await state.restore_session("action-fail")
    assert restored is None
    await bus.stop()
    await orchestrator.shutdown_organs()
