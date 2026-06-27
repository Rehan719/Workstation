import pytest
from decimal import Decimal
from unittest.mock import patch, AsyncMock, MagicMock
from agentic_core.constitutional.evolution_manager import ConstitutionalEvolutionManager
from products.capital_fund.core.multisig_protocol import RealMultiSigProtocol

@pytest.mark.asyncio
async def test_constitutional_evolution():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg, \
         patch("agentic_core.governance.gaas.gaas_validator.GaaSValidatorV4"), \
         patch("agentic_core.genetic_immune.reconfigulator.ConstitutionalReconfigulator"):

        manager = ConstitutionalEvolutionManager(mock_ueg.return_value, AsyncMock(), AsyncMock())
        manager.ueg.log_event = AsyncMock()

        amend_id = await manager.propose_amendment("1130", "Limit changed to 25%", "Better yield", "owner_1")

        # Cast 3 votes
        await manager.cast_vote(amend_id, "council_1", "pqc_sig_1")
        await manager.cast_vote(amend_id, "council_2", "pqc_sig_2")
        res = await manager.cast_vote(amend_id, "council_3", "pqc_sig_3")

        assert res["status"] == "ENACTED"
        assert manager.ueg.log_event.called

@pytest.mark.asyncio
async def test_real_multisig_pqc_verification():
    with patch("agentic_core.ueg.logger.VSBUEGLogger") as mock_ueg:
        protocol = RealMultiSigProtocol(mock_ueg.return_value)
        protocol.ueg.log_event = AsyncMock()

        prop_id = await protocol.submit_proposal("WITHDRAW", Decimal("5000"), "owner_1", {})

        # Use valid simulated signatures (pqc module returns True if starts with b'pqc_sig_')
        sig = b"pqc_sig_valid"
        pk = b"mock_pk"

        # Collect 3 signatures
        await protocol.approve_proposal(prop_id, "c1", sig, pk)
        await protocol.approve_proposal(prop_id, "c2", sig, pk)
        approved = await protocol.approve_proposal(prop_id, "c3", sig, pk)

        assert approved is True
        assert protocol.get_proposal_status(prop_id)["status"] == "APPROVED"
