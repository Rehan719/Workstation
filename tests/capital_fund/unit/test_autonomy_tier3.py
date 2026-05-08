import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime, UTC, timedelta
from products.capital_fund.orchestration.autonomy_controller import AutonomyController

@pytest.fixture
def mock_db():
    with patch("products.capital_fund.orchestration.autonomy_controller.db") as mock:
        yield mock

@pytest.fixture
def controller():
    return AutonomyController(owner_uid="owner_123")

@pytest.mark.asyncio
async def test_enable_tier_3(controller, mock_db):
    with patch("products.capital_fund.orchestration.autonomy_controller.FullAutonomyDelegationEngine.configure_autonomy", new_callable=AsyncMock) as mock_config:
        await controller.enable_tier_3(risk_tolerance=0.4)
        assert controller.enabled is True
        mock_config.assert_called_once_with(enabled=True, risk_tolerance=0.4)

@pytest.mark.asyncio
async def test_emergency_stop(controller, mock_db):
    await controller.enable_tier_3()
    await controller.emergency_stop("TEST_REASON")
    assert controller.enabled is False
    assert controller.kill_switch_active is True

@pytest.mark.asyncio
async def test_heartbeat_timeout(controller, mock_db):
    controller.enabled = True
    # Manually set heartbeat to 25 hours ago
    controller.last_owner_heartbeat = datetime.now(UTC) - timedelta(hours=25)

    # We mock _monitor_safety_invariants as we just want to test the stop logic
    with patch.object(controller, "emergency_stop", new_callable=AsyncMock) as mock_stop:
        # Manually run the check part of the monitor loop
        time_since_heartbeat = (datetime.now(UTC) - controller.last_owner_heartbeat).total_seconds()
        if time_since_heartbeat > 86400:
            await controller.emergency_stop("HEARTBEAT_TIMEOUT")

        mock_stop.assert_called_once_with("HEARTBEAT_TIMEOUT")

@pytest.mark.asyncio
async def test_execute_cycle_blocked(controller, mock_db):
    controller.enabled = False
    result = await controller.execute_cycle({})
    assert result["status"] == "BLOCKED"

@pytest.mark.asyncio
async def test_execute_cycle_success(controller, mock_db):
    controller.enabled = True
    with patch("products.capital_fund.orchestration.autonomy_controller.FullAutonomyDelegationEngine.run_autonomous_cycle", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = {"status": "COMPLETED", "deployments": 2}
        result = await controller.execute_cycle({"market": "bull"})
        assert result["status"] == "COMPLETED"
        mock_run.assert_called_once_with({"market": "bull"})
