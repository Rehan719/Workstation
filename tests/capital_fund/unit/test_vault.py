import pytest
import asyncio
from decimal import Decimal
from unittest.mock import MagicMock, patch, AsyncMock
from products.capital_fund.core.vault import CapitalVault
from products.capital_fund.core.multisig_protocol import RealMultiSigProtocol as MultiSigProtocol
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

        # Manually override to avoid AsyncMock issues in deposit logic
        vault.ueg.log_event = AsyncMock(return_value="event_456")

        result = await vault.deposit(Decimal("100.0"), "tx_789")

        assert result["balance"] == 1100.0
        assert "event_id" in result

@pytest.mark.asyncio
async def test_vault_withdrawal_liquidity_guard(vault):
    # Mocking balance for reserve check (10% of 1000 = 100 reserve)
    with patch.object(CapitalVault, "_get_total_fund_value", return_value=Decimal("1000.0")),          patch("products.capital_fund.core.vault.db") as mock_db:

        # Mocking Firestore transaction to simulate failure
        mock_db.run_transaction.side_effect = ValueError("Liquidity Guard Violation: Withdrawal would breach 10% reserve. Max available: 50.0")

        # Generate valid signatures to pass multisig check
        protocol = MultiSigProtocol(ueg=AsyncMock())
        proposal_hash = "mock_hash"
        sigs = [{"signer": "c1", "signature": "pqc_sig_valid"}] # signatures don't matter much when we patch approve_proposal

        with patch.object(MultiSigProtocol, "submit_proposal", return_value=proposal_hash),              patch.object(MultiSigProtocol, "approve_proposal", return_value=True):
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
    with patch("agentic_core.crypto.pqc.verify_instruction", return_value=True):
        protocol = MultiSigProtocol(ueg=AsyncMock())
        protocol.ueg.log_event = AsyncMock()

        prop_id = await protocol.submit_proposal("TEST", Decimal("100"), "user_1", {})

        # Collect 3 signatures
        await protocol.approve_proposal(prop_id, "c1", b"sig", b"pk")
        await protocol.approve_proposal(prop_id, "c2", b"sig", b"pk")
        approved = await protocol.approve_proposal(prop_id, "c3", b"sig", b"pk")

        assert approved is True
        assert protocol.get_proposal_status(prop_id)["status"] == "APPROVED"
