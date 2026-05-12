import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from agentic_core.capital.quota_manager import CapitalQuotaManager

@pytest.mark.asyncio
async def test_quota_manager_batching():
    with patch("agentic_core.capital.quota_manager.db") as mock_db:
        mock_batch = MagicMock()
        mock_db.batch.return_value = mock_batch

        manager = CapitalQuotaManager("user_1")

        # Log 10 operations
        for i in range(10):
            await manager.log_operation("TEST", {"i": i})

        assert manager.ops_in_batch == 10
        mock_batch.commit.assert_not_called()

        # Flush
        await manager.flush_batch()
        mock_batch.commit.assert_called_once()
        assert manager.ops_in_batch == 0

@pytest.mark.asyncio
async def test_quota_manager_fallback():
    with patch("agentic_core.capital.quota_manager.db") as mock_db:
        mock_batch = MagicMock()
        mock_db.batch.return_value = mock_batch

        manager = CapitalQuotaManager("user_1")

        # Force quota near limit
        with patch.object(manager, "_get_daily_usage", return_value=19500):
            await manager.log_operation("LOW_PRIO", {"data": "secret"}, priority="LOW")

            # Verify it used compact payload
            args, _ = mock_batch.set.call_args
            data = args[1]
            assert data["quota_fallback"] is True
            assert "data" not in data
            assert "hash" in data
