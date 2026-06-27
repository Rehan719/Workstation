import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from products.capital_fund.immune.capital_immune import CapitalImmuneSystem

@pytest.mark.asyncio
async def test_capital_immune_response():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("agentic_core.genetic_immune.anomaly_scorer.RealTimeAnomalyScorer") as mock_anomaly:

        mock_twin = MagicMock()
        immune = CapitalImmuneSystem("user_1", mock_twin)
        immune.ueg.log_event = AsyncMock()
        immune.reconfigulator.propose_enhancement = AsyncMock()
        mock_anomaly.return_value.score_message.return_value = 0.85

        # Scenario: Drawdown 0.18 (>0.15 threshold)
        metrics = {"drawdown": 0.18}
        result = await immune.monitor_and_act(metrics)

        assert result["status"] == "THREAT_DETECTED"
        assert result["immune_response_active"] is True
        assert immune.ueg.log_event.called

        # Scenario: Drawdown 0.22 (>0.20 threshold for mutation)
        metrics = {"drawdown": 0.22}
        await immune.monitor_and_act(metrics)
        assert immune.reconfigulator.propose_enhancement.called
