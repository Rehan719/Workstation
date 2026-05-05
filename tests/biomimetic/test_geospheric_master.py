import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from agentic_core.biomimicry.geospheric.orchestrator import GeosphericHomeostaticOrchestrator

@pytest.mark.asyncio
async def test_geospheric_homeostasis_convergence():
    validator = MagicMock()
    mjm = MagicMock()
    ueg = AsyncMock()
    orchestrator = GeosphericHomeostaticOrchestrator(validator, ueg)

    # Mock system state - exactly at setpoints to ensure stability
    class SystemState:
        def __init__(self):
            # Mocking state for coupling logic
            class CycleState:
                def __init__(self, val, setpoint):
                    self.current = val
                    self.setpoint = setpoint
            self.water_state = CycleState(75.0, 75.0)
            self.carbon_state = CycleState(50.0, 50.0)
            self.nitrogen_state = CycleState(10.0, 10.0)
            self.oxygen_state = CycleState(60.0, 60.0)
            self.phosphorus_state = CycleState(80.0, 80.0)
            self.sulfur_state = CycleState(1.0, 1.0)

    state = SystemState()
    decision = await orchestrator.step(state)

    assert decision.approved is True
    results = decision.adjusted_setpoints

    # At setpoints, coupling effects (current values * matrix) should be some value
    # But since all deviations are 0, it should be approved.
    assert "water" in results

    # Verify UEG logging
    ueg.log_event.assert_called()
