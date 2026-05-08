import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from agentic_core.biomimicry.capital.cycles import CapitalCycleOrchestrator

@pytest.mark.asyncio
async def test_capital_homeostasis_step():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        orchestrator = CapitalCycleOrchestrator("user_1")
        orchestrator.ueg.log_event = AsyncMock()

        # Scenario: Reserve ratio deviated to 0.12 (20% above 0.10 setpoint)
        metrics = {"reserve_ratio": 0.12, "growth_rate": 0.08, "drawdown": 0.05}
        result = await orchestrator.run_homeostasis_step(metrics)

        assert "water" in result["cycles"]
        assert result["cycles"]["water"]["within_tolerance"] is False
        assert result["cycles"]["carbon"]["within_tolerance"] is True
        assert orchestrator.ueg.log_event.called
