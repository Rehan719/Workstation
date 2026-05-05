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

    # Mock system state
    class SystemState:
        def __init__(self):
            self.water_metric = 80.0 # 5 above setpoint 75
            self.carbon_metric = 45.0 # 5 below setpoint 50
            self.nitrogen_metric = 10.0
            self.oxygen_metric = 60.0
            self.phosphorus_metric = 80.0
            self.sulfur_metric = 1.0

    state = SystemState()
    decision = await orchestrator.step(state)

    assert decision.approved is True
    results = decision.adjusted_setpoints

    # Water setpoint 75, metric 80 -> error -5 -> correction should be negative (kp=1.2)
    assert results["water"] < 0
    # Carbon setpoint 50, metric 45 -> error 5 -> correction should be positive (kp=1.0)
    assert results["carbon"] > 0

    # Verify UEG logging
    ueg.log_event.assert_called()
