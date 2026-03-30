import pytest
import asyncio
from unittest.mock import MagicMock
from agentic_core.ai_ceo.c_suite import BiomimeticCSuite
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.immune.immune_system import ImmuneSystemV2
from agentic_core.tools.registry import ToolRegistry

from src.organism.python.core.state_kernel import SovereignState
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.core.csuite_orchestrator import CSuiteOrchestrator
from src.organism.python.organs.nematron_adapter import NematronAdapter
from src.organism.python.organs.nemoclaw_adapter import NemoclawAdapter
from src.organism.python.organs.openclaw_adapter import OpenClawAdapter
from src.organism.python.neural.event_types import (
    IntentGenerated, GovernanceValidated, ActionExecuted,
    StrategicIntent, ValidationResult, ExecutionResult
)

@pytest.mark.asyncio
async def test_integrated_organism_flow():
    bus = AsyncEventBus()
    state = SovereignState(storage_dir="data/test_state")
    await bus.start()
    legacy_csuite = BiomimeticCSuite()
    vga_engine = VGAEngine()
    immune_system = ImmuneSystemV2()
    tool_registry = ToolRegistry()
    tool_registry.register_tool(name="DEFAULT_TOOL", category="general", capabilities=["test"], config={})
    nematron = NematronAdapter(legacy_csuite, bus)
    nemoclaw = NemoclawAdapter(vga_engine, immune_system, bus)
    openclaw = OpenClawAdapter(tool_registry, bus)
    orchestrator = CSuiteOrchestrator(bus, state)
    await orchestrator.initialize_organs(nematron, nemoclaw, openclaw)
    intent = await nematron.generate_intent("Optimize system performance for v1.0 launch.")
    await asyncio.sleep(1.0)
    history = bus.get_history()
    intent_event = next(e for e in history if isinstance(e, IntentGenerated))
    action_id = intent_event.id
    restored = await state.restore_session(action_id)
    assert restored is not None
    assert restored["execution_result"]["status"] == "SUCCESS"
    assert restored["execution_result"]["tool"] == "DEFAULT_TOOL"
    await bus.stop()
    await orchestrator.shutdown_organs()

@pytest.mark.asyncio
async def test_nemoclaw_threat_rejection():
    bus = AsyncEventBus()
    await bus.start()
    vga_engine = VGAEngine()
    immune_system = ImmuneSystemV2()
    nemoclaw = NemoclawAdapter(vga_engine, immune_system, bus)
    intent = StrategicIntent("Dangerous Action", "HAZARD", {"perplexity": 100}, "Test failure")
    intent_event = IntentGenerated(id="hazard-action", intent=intent, source="nematron")
    validation_event = await nemoclaw.validate_action(intent_event)
    assert validation_event.validation_result.is_valid == False
    assert "Threat score" in validation_event.validation_result.reason
    await bus.stop()
