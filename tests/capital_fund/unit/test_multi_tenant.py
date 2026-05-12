import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from decimal import Decimal
from products.capital_fund.investors.multi_tenant_manager import MultiTenantInvestorManager

@pytest.fixture
def mock_db():
    with patch("products.capital_fund.investors.multi_tenant_manager.db") as mock:
        yield mock

@pytest.fixture
def manager():
    return MultiTenantInvestorManager(owner_uid="owner_123")

@pytest.mark.asyncio
async def test_onboard_investor_success(manager, mock_db):
    # Setup mocks
    manager.validator.validate_intent = AsyncMock(return_value={"passed": True, "merkle_root": "abc"})
    mock_db.run_transaction = MagicMock(return_value={
        "investor_id": "inv_123",
        "uid": "investor_456",
        "balance": 1000.0,
        "status": "active"
    })

    account = await manager.onboard_investor("investor_456", Decimal("1000.0"), {"kyc": "ok"})

    assert account.id == "inv_123"
    assert account.balance == Decimal("1000.0")
    assert account.status == "active"
    manager.validator.validate_intent.assert_called_once()

@pytest.mark.asyncio
async def test_onboard_investor_rejected(manager, mock_db):
    manager.validator.validate_intent = AsyncMock(return_value={"passed": False, "reason": "KYC Failed"})

    with pytest.raises(ValueError, match="KYC Failed"):
        await manager.onboard_investor("investor_bad", Decimal("1000.0"), {})

@pytest.mark.asyncio
async def test_calculate_pro_rata_share(manager, mock_db):
    # Mock investor balance 500, Total AUM 1000 -> 0.5
    with patch.object(MultiTenantInvestorManager, "get_investor_account") as mock_get:
        mock_get.return_value = MagicMock(balance=Decimal("500.0"))
        manager.vault._get_total_fund_value = AsyncMock(return_value=Decimal("1000.0"))

        share = await manager.calculate_pro_rata_share("investor_456")
        assert share == Decimal("0.5")

@pytest.mark.asyncio
async def test_distribute_profit(manager, mock_db):
    # Setup mock investors
    mock_inv1 = MagicMock()
    mock_inv1.to_dict.return_value = {"uid": "inv1", "balance": 500.0, "profit_sharing_rate": 0.1}
    mock_inv2 = MagicMock()
    mock_inv2.to_dict.return_value = {"uid": "inv2", "balance": 500.0, "profit_sharing_rate": 0.2}

    mock_db.collection().where().stream.return_value = [mock_inv1, mock_inv2]
    manager.vault._get_total_fund_value = AsyncMock(return_value=Decimal("1000.0"))

    # Total profit 100. inv1 gets 50, fee 5 -> 45. inv2 gets 50, fee 10 -> 40.
    distributions = await manager.distribute_profit(Decimal("100.0"))

    assert distributions["inv1"] == Decimal("45.0")
    assert distributions["inv2"] == Decimal("40.0")
