import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from decimal import Decimal
from products.capital_fund.orchestration.full_autonomy import FullAutonomyDelegationEngine

@pytest.fixture
def mock_db():
    with patch("products.capital_fund.orchestration.full_autonomy.db") as mock:
        yield mock

@pytest.fixture
def engine():
    return FullAutonomyDelegationEngine(owner_uid="owner_123")

@pytest.mark.asyncio
async def test_configure_autonomy(engine, mock_db):
    config = await engine.configure_autonomy(enabled=True, risk_tolerance=0.3)
    assert config["enabled"] is True
    assert config["risk_tolerance"] == 0.3
    engine.config_ref.set.assert_called_once()

@pytest.mark.asyncio
async def test_run_autonomous_cycle_disabled(engine, mock_db):
    engine.config_ref.get().exists = True
    engine.config_ref.get().to_dict.return_value = {"enabled": False}

    result = await engine.run_autonomous_cycle({})
    assert result["status"] == "SKIPPED"
    assert "disabled" in result["reason"]

@pytest.mark.asyncio
async def test_run_autonomous_cycle_execution(engine, mock_db):
    # Setup mocks
    engine.config_ref.get().exists = True
    engine.config_ref.get().to_dict.return_value = {"enabled": True}
    engine.vault._get_total_fund_value = AsyncMock(return_value=Decimal("1000.0"))

    # 900.0 available
    engine.orchestrator.step = AsyncMock(return_value=[
        {"reactor": "science", "amount": 500.0},
        {"reactor": "law", "amount": 400.0}
    ])

    result = await engine.run_autonomous_cycle({"market": "stable"})

    assert result["status"] == "COMPLETED"
    assert result["deployments_count"] == 2
    assert result["total_deployed"] == 900.0
    engine.orchestrator.step.assert_called_once_with("owner_123", Decimal("900.0"), {"market": "stable"})

@pytest.mark.asyncio
async def test_emergency_halt(engine, mock_db):
    with patch.object(FullAutonomyDelegationEngine, "configure_autonomy", new_callable=AsyncMock) as mock_config:
        await engine.emergency_halt()
        mock_config.assert_called_once_with(enabled=False)
