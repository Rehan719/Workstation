import pytest
import asyncio
from decimal import Decimal
from unittest.mock import MagicMock, patch, AsyncMock
from products.capital_fund.orchestration.investment_orchestrator import InvestmentOrchestrator

@pytest.mark.asyncio
async def test_investment_orchestrator_allocation():
    with patch("agentic_core.mjm.hd_omni_learner.MJMv4OmniLearner"), \
         patch("agentic_core.consultation.mushawara.consultation_orchestrator.ConsultationOrchestrator"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:

        orchestrator = InvestmentOrchestrator()
        orchestrator.ueg.log_event = AsyncMock(return_value="event_123")

        # Mocking reactors
        for reactor in orchestrator.reactors.values():
            reactor.deploy_capital = AsyncMock(return_value={"status": "ACTIVE"})

        deployments = await orchestrator.allocate_capital("user_1", Decimal("1000.0"))

        assert len(deployments) == 4
        assert deployments[0]["status"] == "ACTIVE"
        assert orchestrator.ueg.log_event.call_count >= 4 # 4 deployments
