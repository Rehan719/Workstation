import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from agentic_core.biomimicry.geospheric.orchestrator import HomeostaticOrchestrator

@pytest.mark.asyncio
async def test_geospheric_homeostasis_convergence():
    validator = MagicMock()
    mjm = MagicMock()
    ueg = AsyncMock()
    orchestrator = HomeostaticOrchestrator(validator, mjm, ueg)

    # Mock system state - exactly at setpoints to ensure stability
    # Setpoints: Water=75, Carbon=50, Nitrogen=10, Oxygen=60, Phosphorus=80, Sulfur=1
    # Metrics normalized to 100 in the orchestrator logic for Psi evaluation
    class SystemState:
        def __init__(self):
            self.water_metric = 75.0
            self.carbon_metric = 50.0
            self.nitrogen_metric = 10.0
            self.oxygen_metric = 60.0
            self.phosphorus_metric = 80.0
            self.sulfur_metric = 1.0

    state = SystemState()
    decision = await orchestrator.step(state)

    assert decision.approved is True
    results = decision.adjusted_setpoints

    # At setpoints, corrections should be 0.0
    assert results["water"] == 0.0
    assert results["carbon"] == 0.0

    # Verify UEG logging
    ueg.log_event.assert_called()
