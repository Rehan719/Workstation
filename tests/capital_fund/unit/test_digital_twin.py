import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from agentic_core.simulations.fund_digital_twin import FundDigitalTwin

@pytest.mark.asyncio
async def test_fund_digital_twin_healing():
    with patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("agentic_core.genetic_immune.regulator.Regulator"), \
         patch("agentic_core.genetic_immune.reconfigulator.ConstitutionalReconfigulator") as mock_recon:

        twin = FundDigitalTwin(owner_uid="test_user")
        twin.ueg.log_event = AsyncMock()
        twin.reconfigulator.propose_enhancement = AsyncMock()

        # Simulation with drawdown > 0.25 (simulated trajectory is downward)
        result = await twin.synchronize_and_simulate({"balance": 1000.0}, stress_test=True)

        assert result["needs_healing"] is True
        assert twin.ueg.log_event.call_count >= 3 # Sync, Simulation, Healing
        assert twin.reconfigulator.propose_enhancement.called
