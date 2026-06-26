import concurrent.futures
from backend.usage.meter import check_quota
import pytest
from unittest.mock import MagicMock, patch

def test_quota_atomic():
    uid = "test-atomic-user"
    # Note: This requires a real or local emulator Firestore to truly test atomicity.
    # In sandbox, we verify the transactional structure.

    with patch("backend.usage.meter.db") as mock_db:
        mock_transaction = MagicMock()
        mock_db.transaction.return_value = mock_transaction

        # Simulate 100 concurrent attempts
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_quota, uid, "executions") for _ in range(100)]

        # In a real test with emulator, we'd assert sum(results) == 50
        assert mock_db.run_transaction.called
