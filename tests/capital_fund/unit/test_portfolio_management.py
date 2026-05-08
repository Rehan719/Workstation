import pytest
from decimal import Decimal
from unittest.mock import patch, AsyncMock
from agentic_core.capital.realtime_feeds import RealtimeFeedManager
from products.capital_fund.portfolio.multi_asset_manager import MultiAssetPortfolioManager

@pytest.mark.asyncio
async def test_realtime_feeds_mock():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        manager = RealtimeFeedManager(mock_ueg.return_value)
        snapshot = await manager.get_market_snapshot()
        assert "BTC_USD" in snapshot
        assert snapshot["BTC_USD"] == 65420.50

@pytest.mark.asyncio
async def test_portfolio_concentration_limit():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        manager = MultiAssetPortfolioManager("user_1", mock_ueg.return_value)
        manager.ueg.log_event = AsyncMock()

        # Add some initial assets (bypass limits for initialization)
        await manager.update_position("SPY", Decimal("10"), Decimal("500"), "ETF", bypass_risk_limits=True) # 5000
        await manager.update_position("AAPL", Decimal("20"), Decimal("200"), "Stock", bypass_risk_limits=True) # 4000
        # Total AUM = 9000

        # Try to add large BTC position (10,000)
        # Concentration would be 10000 / 19000 = 52% (> 20%)
        with pytest.raises(ValueError, match="exceeds 20% limit"):
            await manager.update_position("BTC", Decimal("1"), Decimal("10000"), "Crypto")

@pytest.mark.asyncio
async def test_portfolio_diversity_score():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        manager = MultiAssetPortfolioManager("user_1", mock_ueg.return_value)
        manager.ueg.log_event = AsyncMock()

        res1 = await manager.update_position("A1", Decimal("1"), Decimal("10"), "Cat", bypass_risk_limits=True)
        assert res1["diversity_score"] == 0.2 # 1/5

        res2 = await manager.update_position("A2", Decimal("1"), Decimal("10"), "Cat", bypass_risk_limits=True)
        assert res2["diversity_score"] == 0.4 # 2/5
