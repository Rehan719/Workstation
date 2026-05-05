import concurrent.futures
import pytest
from unittest.mock import MagicMock, patch
from backend.usage.meter import check_quota

@pytest.mark.asyncio
async def test_quota_atomic_simulation():
    # Mocking firestore client and transaction
    mock_db = MagicMock()
    mock_transaction = MagicMock()

    # Simulate free tier limit 50
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"count": 49}

    mock_transaction.get.return_value = mock_doc

    # We mock the db.run_transaction to just call our logic
    def run_tx(logic):
        return logic(mock_transaction)

    mock_db.run_transaction = run_tx

    with patch("backend.usage.meter.db", mock_db):
        with patch("backend.usage.meter._get_effective_plan", return_value="free"):
            # Should succeed for the 50th call
            assert check_quota("user123", "executions") is True

            # Now mock 50 calls
            mock_doc.to_dict.return_value = {"count": 50}
            assert check_quota("user123", "executions") is False
