import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from backend.usage.meter import check_quota

@pytest.mark.asyncio
async def test_quota_atomic_with_repo():
    # 1. Setup Mock Repository
    mock_repo = AsyncMock()

    # Simulate user has a free plan
    mock_repo.get_subscription.return_value = {"status": "active", "plan": "free"}

    # Case A: Within limit
    mock_repo.increment_quota.return_value = (True, 10)
    allowed = await check_quota("user123", "executions", mock_repo)
    assert allowed is True
    mock_repo.increment_quota.assert_called_with("user123", "executions", 50)

    # Case B: Exceeds limit
    mock_repo.increment_quota.return_value = (False, 50)
    allowed = await check_quota("user456", "executions", mock_repo)
    assert allowed is False

@pytest.mark.asyncio
async def test_quota_predictive_buffer():
    mock_repo = AsyncMock()
    mock_repo.get_subscription.return_value = {"status": "active", "plan": "free"}
    mock_repo.increment_quota.return_value = (True, 52)

    # Twin predicts upgrade: should use 10% buffer (50 -> 55)
    prediction = {"likelihood_to_upgrade": 0.85}
    allowed = await check_quota("user789", "executions", mock_repo, twin_prediction=prediction)

    assert allowed is True
    mock_repo.increment_quota.assert_called_with("user789", "executions", 55)
