import pytest
from unittest.mock import patch, AsyncMock
from agentic_core.simulations.fund_digital_twin import FundDigitalTwin

@pytest.mark.asyncio
async def test_fund_digital_twin_healing():
    with patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:

        twin = FundDigitalTwin()
        # The instance will have its own logger mocked
        twin.ueg.log_event = AsyncMock()

        # Simulation with drawdown > 0.25 (simulated trajectory is downward)
        result = await twin.simulate_weekly_performance({"balance": 1000.0})

        assert result["needs_healing"] is True
        assert twin.ueg.log_event.call_count >= 2 # 1 for simulation, 1 for trigger
