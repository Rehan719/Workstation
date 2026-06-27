import pytest
from decimal import Decimal
from products.capital_fund.adapters.mainnet_settlement import MainnetSettlementEngine
from products.capital_fund.adapters.institutional_banking import InstitutionalBankingAdapter

@pytest.mark.asyncio
async def test_mainnet_settlement_gas_limit():
    engine = MainnetSettlementEngine()

    # 1000 USDC, 40 USDC Gas (4%) -> PASS
    assert engine.estimate_gas_feasibility(Decimal("1000"), Decimal("40")) is True

    # 1000 USDC, 60 USDC Gas (6%) -> FAIL
    assert engine.estimate_gas_feasibility(Decimal("1000"), Decimal("60")) is False

@pytest.mark.asyncio
async def test_institutional_fx_validation():
    adapter = InstitutionalBankingAdapter()

    # Market 1.0, Bank 1.004 (0.4%) -> PASS
    assert adapter.validate_fx_spread(Decimal("1.0"), Decimal("1.004")) is True

    # Market 1.0, Bank 1.01 (1%) -> FAIL
    assert adapter.validate_fx_spread(Decimal("1.0"), Decimal("1.01")) is False

@pytest.mark.asyncio
async def test_swift_transfer_logging():
    adapter = InstitutionalBankingAdapter()
    transfer_id = await adapter.execute_swift_transfer(Decimal("5000"), "USD", "DE123456789")
    assert transfer_id.startswith("SWIFT_")
