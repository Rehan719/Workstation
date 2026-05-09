import pytest
from agentic_core.edge.sovereignty_deployer import EdgeSovereigntyDeployer

@pytest.mark.asyncio
async def test_edge_sovereignty_lifecycle():
    deployer = EdgeSovereigntyDeployer(node_id="edge_001")

    # 1. TPM
    success = await deployer.verify_tpm_attestation(b"pcr_data", b"TRUSTED_TPM_SIG_ABC")
    assert success is True
    assert deployer.attestation_verified is True

    # 2. PQC Handshake
    handshake = await deployer.initiate_pqc_handshake(b"peer_pk")
    assert handshake["status"] == "HANDSHAKE_COMPLETE"
    assert deployer.pqc_handshake_complete is True

    # 3. Offline
    await deployer.activate_offline_fallback()

    assert deployer.get_sovereignty_score() == 1.0

@pytest.mark.asyncio
async def test_edge_pqc_without_tpm_fails():
    deployer = EdgeSovereigntyDeployer(node_id="edge_002")
    with pytest.raises(RuntimeError, match="before TPM attestation"):
        await deployer.initiate_pqc_handshake(b"pk")
