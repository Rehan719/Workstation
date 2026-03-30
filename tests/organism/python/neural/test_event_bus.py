import pytest
import asyncio
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    IntentGenerated, GovernanceValidated, ActionExecuted, StrategicIntent, ValidationResult, ExecutionResult
)

@pytest.mark.asyncio
async def test_canonical_flow():
    bus = AsyncEventBus()
    await bus.start()
    validation_called = False
    execution_called = False
    async def validate_handler(event: IntentGenerated):
        nonlocal validation_called
        validation_called = True
        await bus.publish(GovernanceValidated(
            action_id=event.id,
            validation_result=ValidationResult(True, "Approved", "ZK_ATTEST_001")
        ))
    async def execute_handler(event: GovernanceValidated):
        nonlocal execution_called
        execution_called = True
        await bus.publish(ActionExecuted(
            action_id=event.action_id,
            result=ExecutionResult("SUCCESS", {"output": "hello_world"})
        ))
    bus.subscribe(IntentGenerated, validate_handler)
    bus.subscribe(GovernanceValidated, execute_handler)
    intent = StrategicIntent("Test Goal", "GREET", {"name": "Jules"}, "First test")
    await bus.publish(IntentGenerated(intent=intent, source="human", priority=1))
    await asyncio.sleep(0.5)
    assert validation_called == True
    assert execution_called == True
    assert len(bus.get_history()) >= 3
    await bus.stop()

@pytest.mark.asyncio
async def test_priority_queueing():
    bus = AsyncEventBus()
    await bus.start()
    processed_order = []
    async def handler(event):
        processed_order.append(event.priority)
        await asyncio.sleep(0.1)
    bus.subscribe(IntentGenerated, handler)
    await bus.publish(IntentGenerated(priority=5))
    await bus.publish(IntentGenerated(priority=1))
    await asyncio.sleep(0.5)
    assert processed_order == [1, 5]
    await bus.stop()

@pytest.mark.asyncio
async def test_dead_letter_queue():
    bus = AsyncEventBus()
    await bus.start()
    async def failing_handler(event):
        raise ValueError("Simulated handler failure")
    bus.subscribe(IntentGenerated, failing_handler)
    await bus.publish(IntentGenerated(priority=1))
    await asyncio.sleep(0.1)
    dlq = bus.get_dlq()
    assert len(dlq) == 1
    assert dlq[0]["error"] == "Simulated handler failure"
    await bus.stop()
