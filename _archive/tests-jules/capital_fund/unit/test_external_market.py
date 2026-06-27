import pytest
from decimal import Decimal
from unittest.mock import patch, AsyncMock
from products.capital_fund.adapters.external_market import ExternalMarketAdapter

@pytest.mark.asyncio
async def test_external_market_trade_disabled():
    with patch("agentic_core.governance.gaas.gaas_validator.GaaSValidatorV4"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger"):

        adapter = ExternalMarketAdapter(AsyncMock(), AsyncMock())
        # Ensure disabled by default
        adapter.external_markets_enabled = False

        with pytest.raises(ValueError, match="External markets are currently disabled"):
            await adapter.execute_trade("user_1", "BTC", "BUY", Decimal("0.1"), "key_1")

@pytest.mark.asyncio
async def test_external_market_trade_execution():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        mock_validator = AsyncMock()
        mock_validator.validate_action = AsyncMock(return_value={"passed": True, "hash": "abc"})

        adapter = ExternalMarketAdapter(mock_validator, mock_ueg.return_value)
        adapter.external_markets_enabled = True
        adapter.ueg.log_event = AsyncMock()

        receipt = await adapter.execute_trade("user_1", "ETH", "BUY", Decimal("1.0"), "key_2")

        assert receipt["symbol"] == "ETH"
        assert receipt["status"] == "EXECUTED"
        assert receipt["price"] == 3500.0
        assert adapter.ueg.log_event.called
