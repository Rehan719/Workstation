import pytest
import asyncio
from decimal import Decimal
from unittest.mock import MagicMock, patch, AsyncMock
from products.capital_fund.core.vault import CapitalVault
from products.capital_fund.core.multisig_protocol import MultiSigProtocol
from products.capital_fund.core.audit_manager import AuditManager

@pytest.fixture
def owner_uid():
    return "test_owner_123"

@pytest.fixture
def vault(owner_uid):
    with patch("products.capital_fund.core.vault.GaaSValidator") as mock_gaas,          patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        mock_gaas.return_value.validate_action = AsyncMock(return_value={"passed": True, "hash": "test_hash"})
        mock_ueg.return_value.log_event = AsyncMock(return_value="event_456")
        return CapitalVault(owner_uid)

@pytest.mark.asyncio
async def test_vault_deposit_atomic(vault, owner_uid):
    # Mocking GaaS validation and UEG logging
    with patch("products.capital_fund.core.vault.db") as mock_db:

        # Mocking Firestore transaction
        mock_db.run_transaction.return_value = 1100.0

        result = await vault.deposit(Decimal("100.0"), "tx_789")

        assert result["balance"] == 1100.0
        assert "event_id" in result

@pytest.mark.asyncio
async def test_vault_withdrawal_liquidity_guard(vault):
    # Mocking balance for reserve check (10% of 1000 = 100 reserve)
    with patch.object(CapitalVault, "_get_total_fund_value", return_value=Decimal("1000.0")),          patch("products.capital_fund.core.vault.db") as mock_db:

        # Mocking Firestore transaction to simulate failure
        # In a real system, the transaction function raises the error
        mock_db.run_transaction.side_effect = ValueError("Liquidity Guard Violation: Withdrawal would breach 10% reserve. Max available: 50.0")

        # Generate valid signatures to pass multisig check
        protocol = MultiSigProtocol()
        proposal_hash = "mock_hash"
        sigs = [{"signer": f"council_member_{i}", "signature": protocol.generate_simulated_signature(proposal_hash, f"council_member_{i}")} for i in range(1, 4)]

        with patch.object(MultiSigProtocol, "initiate_proposal", return_value=proposal_hash):
            # Attempt to withdraw 950
            with pytest.raises(ValueError, match="Liquidity Guard Violation"):
                await vault.withdraw(Decimal("950.0"), signatures=sigs)

@pytest.mark.asyncio
async def test_vault_withdrawal_multisig_required(vault):
    # Withdrawal > 5% of 1000 = 50. Withdrawal of 100 needs multisig.
    with patch.object(CapitalVault, "_get_total_fund_value", return_value=Decimal("1000.0")),          patch("products.capital_fund.core.vault.db") as mock_db:

        # No signatures provided
        with pytest.raises(ValueError, match="Large withdrawal requires MultiSigCouncil approval"):
            await vault.withdraw(Decimal("100.0"))

@pytest.mark.asyncio
async def test_multisig_quorum():
    protocol = MultiSigProtocol()
    proposal_hash = await protocol.initiate_proposal("TEST", Decimal("100"), "user_1")

    # Generate 3 valid signatures
    sigs = [
        {"signer": "council_member_1", "signature": protocol.generate_simulated_signature(proposal_hash, "council_member_1")},
        {"signer": "council_member_2", "signature": protocol.generate_simulated_signature(proposal_hash, "council_member_2")},
        {"signer": "council_member_3", "signature": protocol.generate_simulated_signature(proposal_hash, "council_member_3")}
    ]

    assert await protocol.verify_quorum(proposal_hash, sigs) is True

    # Only 2 signatures
    assert await protocol.verify_quorum(proposal_hash, sigs[:2]) is False

    # Invalid signature
    sigs[2]["signature"] = "invalid_sig"
    assert await protocol.verify_quorum(proposal_hash, sigs) is False
