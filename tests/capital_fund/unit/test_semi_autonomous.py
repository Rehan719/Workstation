import pytest
from decimal import Decimal
from unittest.mock import patch, AsyncMock, MagicMock
from products.capital_fund.orchestration.semi_autonomous import SemiAutonomousExecutor

@pytest.mark.asyncio
async def test_semi_autonomous_toggle():
    with patch("agentic_core.ueg.logger.VSBUEGLogger"):
        mock_orch = MagicMock()
        mock_vault = MagicMock()
        executor = SemiAutonomousExecutor("owner_1", mock_orch, mock_vault)
        executor.ueg.log_event = AsyncMock()

        # Valid toggle
        await executor.toggle_autonomous_mode("owner_1", True)
        assert executor.enabled is True

        # Unauthorized toggle
        with pytest.raises(ValueError, match="Unauthorized"):
            await executor.toggle_autonomous_mode("other_1", False)

@pytest.mark.asyncio
async def test_low_risk_autonomous_execution():
    with patch("agentic_core.ueg.logger.VSBUEGLogger"):
        mock_orch = AsyncMock()
        mock_vault = AsyncMock()
        mock_vault._get_total_fund_value = AsyncMock(return_value=Decimal("10000.0"))

        # Mock low risk allocation
        mock_orch.step = AsyncMock(return_value=[{"amount": 500.0, "risk_score": 0.1}])

        executor = SemiAutonomousExecutor("owner_1", mock_orch, mock_vault)
        executor.enabled = True
        executor.ueg.log_event = AsyncMock()

        result = await executor.execute_low_risk_rebalance({"market": "stable"})

        assert result["status"] == "EXECUTED"
        assert result["autonomous"] is True
        assert executor.ueg.log_event.called

@pytest.mark.asyncio
async def test_high_risk_execution_blocked():
    with patch("agentic_core.ueg.logger.VSBUEGLogger"):
        mock_orch = AsyncMock()
        mock_vault = AsyncMock()
        mock_vault._get_total_fund_value = AsyncMock(return_value=Decimal("10000.0"))

        # Mock high risk allocation (risk 0.3 > 0.2)
        mock_orch.step = AsyncMock(return_value=[{"amount": 500.0, "risk_score": 0.3}])

        executor = SemiAutonomousExecutor("owner_1", mock_orch, mock_vault)
        executor.enabled = True
        executor.ueg.log_event = AsyncMock()

        result = await executor.execute_low_risk_rebalance({"market": "volatile"})

        assert result["status"] == "APPROVAL_REQUIRED"
        assert "Risk score too high" in result["reason"] or "exceeds autonomous safety" in result["reason"]
