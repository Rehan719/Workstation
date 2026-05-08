import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from decimal import Decimal
from products.capital_fund.adapters.institutional_market import InstitutionalMarketConnector
from products.capital_fund.adapters.defi_yield import DeFiYieldAdapter

@pytest.mark.asyncio
async def test_institutional_market_connector_mock():
    # Enabled
    conn = InstitutionalMarketConnector(feature_enabled=True)
    prices = await conn.get_realtime_prices(["AAPL", "BTC/USD"])
    assert prices["AAPL"] == Decimal("190.254321")
    assert prices["BTC/USD"] == Decimal("65000.789012")

    # Disabled
    conn_disabled = InstitutionalMarketConnector(feature_enabled=False)
    prices_base = await conn_disabled.get_realtime_prices(["AAPL"])
    assert prices_base["AAPL"] == Decimal("100.00")

@pytest.mark.asyncio
async def test_defi_yield_allocation_limit():
    adapter = DeFiYieldAdapter()
    adapter.validator.validate_intent = AsyncMock(return_value={"passed": True})

    # Total AUM 1000, 20% limit = 200. Request 250 -> Fail.
    with pytest.raises(ValueError, match="exceeds 20% limit"):
        await adapter.deploy_to_protocol("uid", "Aave", "USDC", Decimal("250.0"), Decimal("1000.0"))

@pytest.mark.asyncio
async def test_defi_yield_deployment_success():
    adapter = DeFiYieldAdapter()
    adapter.validator.validate_intent = AsyncMock(return_value={"passed": True})

    # Total AUM 1000, 20% limit = 200. Request 100 -> Success.
    receipt = await adapter.deploy_to_protocol("uid", "Aave", "USDC", Decimal("100.0"), Decimal("1000.0"))
    assert receipt["status"] == "COMPLETED"
    assert receipt["protocol"] == "Aave"
    assert "0xdefi_aave" in receipt["tx_hash"]
