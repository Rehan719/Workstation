import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from agentic_core.biomimicry.geospheric.digital_twin_orchestrator import DigitalTwinOrchestrator
from agentic_core.simulations.digital_twin_controller import DigitalTwinController
from agentic_core.mjm.self_reflection_engine import SelfReflectionEngine

@pytest.fixture
def mock_ueg():
    ueg = AsyncMock()
    ueg.log_event = AsyncMock()
    ueg.get_last_entries = AsyncMock(return_value=[])
    return ueg

@pytest.fixture
def mock_mjm():
    mjm = MagicMock()
    mjm.get_confidence.return_value = 0.92
    mjm.predict_next = AsyncMock(return_value={
        "constitutional_compliance": 1.0,
        "psi_health": 0.95,
        "cycle_states": {},
        "subscription_state": {},
        "simulation_confidence": 0.91,
        "timestamp": datetime.utcnow().isoformat()
    })
    mjm.update = AsyncMock(return_value=0.03)
    return mjm

@pytest.fixture
def twin_setup(mock_ueg, mock_mjm):
    validator = MagicMock()
    # In orchestrator, cycles are initialized in __init__
    orchestrator = DigitalTwinOrchestrator(validator, mock_mjm, mock_ueg)

    reflection_engine = SelfReflectionEngine(validator, MagicMock())
    immune_defense = MagicMock()
    immune_defense.scan_threats = AsyncMock(return_value=0.1)

    controller = DigitalTwinController(orchestrator, reflection_engine, immune_defense)

    return controller, orchestrator

@pytest.mark.asyncio
async def test_twin_reflection_cycle(twin_setup):
    controller, orchestrator = twin_setup

    result = await controller.step()

    assert result["status"] == "SUCCESS"
    assert "reflection" in result
    assert "evolution" in result
    assert result["reflection"]["score"] >= 0

    # Verify UEG logging
    orchestrator.ueg.log_event.assert_called()

@pytest.mark.asyncio
async def test_twin_state_capture(twin_setup):
    controller, orchestrator = twin_setup

    state = await orchestrator.capture_state()

    assert state.psi_health > 0
    assert state.state_checksum is not None
    assert state.previous_checksum is not None
    assert orchestrator.ueg.log_event.called

@pytest.mark.asyncio
async def test_predictive_simulation(twin_setup):
    controller, orchestrator = twin_setup

    simulation = await orchestrator.simulate_future(horizon_seconds=300)

    assert len(simulation.trajectory) > 0
    assert simulation.confidence >= 0.7 # Hard-stop threshold in code
