import pytest
from decimal import Decimal
from products.capital_fund.mesh.federation_manager import FederationManager

@pytest.fixture
def manager():
    return FederationManager(fund_id="workstation_001")

@pytest.mark.asyncio
async def test_mesh_treaty_lifecycle(manager):
    peer_id = "workstation_002"
    terms = {"liquidity_sharing": True, "risk_hedging": False}

    # 1. Sign
    treaty_id = await manager.sign_treaty(peer_id, terms)
    assert treaty_id.startswith("treaty_")
    assert peer_id in manager.active_treaties

    # 2. Benchmark
    benchmarks = await manager.fetch_federated_benchmarks()
    assert len(benchmarks) > 0

    # 3. Contribute
    contribution = await manager.contribute_to_shared_pool(peer_id, Decimal("5000.0"))
    assert contribution["amount"] == 5000.0
    assert "zk_proof" in contribution

    # 4. Revoke
    await manager.revoke_treaty(peer_id)
    assert peer_id not in manager.active_treaties

@pytest.mark.asyncio
async def test_mesh_contribution_no_treaty(manager):
    with pytest.raises(ValueError, match="No active treaty"):
        await manager.contribute_to_shared_pool("stranger_fund", Decimal("100.0"))
