import pytest
from decimal import Decimal
from unittest.mock import patch, AsyncMock, MagicMock
from products.capital_fund.adapters.crypto_gateway import CryptoGateway

@pytest.mark.asyncio
async def test_crypto_deposit_verification():
    with patch("products.capital_fund.core.vault.GaaSValidator"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("products.capital_fund.core.vault.db") as mock_db:

        mock_validator = AsyncMock()
        mock_validator.validate_action = AsyncMock(return_value={"passed": True, "hash": "abc"})
        mock_ueg.return_value.log_event = AsyncMock(return_value="event_123")

        # Mock Firestore transaction for vault deposit
        mock_db.run_transaction.return_value = 1000.0

        gateway = CryptoGateway("user_1", mock_validator, mock_ueg.return_value)

        # Manually override the vault inside the gateway
        gateway.vault.validator = mock_validator
        gateway.vault.ueg = mock_ueg.return_value
        gateway.vault.audit.ueg_logger = mock_ueg.return_value

        result = await gateway.verify_onchain_deposit("0xhash123", "USDC", Decimal("100.0"))

        assert result["status"] == "COMPLETED"
        assert result["new_balance"] == 1000.0
        assert mock_ueg.return_value.log_event.called

@pytest.mark.asyncio
async def test_crypto_withdrawal_gas_limit():
    with patch("products.capital_fund.core.vault.GaaSValidator"), \
         patch("agentic_core.ueg.logger.VSBUEGLogger"):

        gateway = CryptoGateway("user_1", AsyncMock(), AsyncMock())

        # $2.50 gas on $10 withdrawal = 25% (Limit is 5%)
        with pytest.raises(ValueError, match="Gas cost .* exceeds 5% reserve limit"):
            await gateway.execute_onchain_withdrawal(Decimal("10.0"), "ETH", "0xdest")
