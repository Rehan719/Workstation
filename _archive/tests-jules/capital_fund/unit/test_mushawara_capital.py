import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from products.capital_fund.consultation.mushawara_capital import CapitalMushawaraConsultant

@pytest.mark.asyncio
async def test_mushawara_capital_validation():
    with patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.consultation.mushawara.consultation_orchestrator.ConsultationOrchestrator"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:

        consultant = CapitalMushawaraConsultant()
        consultant.ueg.log_event = AsyncMock()

        proposal = {"amount": 5000.0, "asset": "Science"}
        result = await consultant.validate_high_stakes_allocation("user_1", proposal, {})

        assert result["approved"] is True
        assert result["consensus_score"] >= 0.80
        assert "inkashaf" in result["engine_traces"]
        assert consultant.ueg.log_event.called
