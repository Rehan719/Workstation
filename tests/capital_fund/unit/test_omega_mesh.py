import pytest
from agentic_core.federation.mesh_activator import SovereignMeshActivator

@pytest.mark.asyncio
async def test_mesh_activation_lifecycle():
    activator = SovereignMeshActivator(privacy_budget=0.1)
    bootstrap = ["/dns/seed1", "/dns/seed2"]

    result = await activator.activate_sovereign_mesh(bootstrap)

    assert result["status"] == "ACTIVE"
    assert result["epsilon"] == 0.1
    assert result["connected_peers"] == 2
    assert activator.is_active is True

@pytest.mark.asyncio
async def test_federated_broadcast_privacy():
    activator = SovereignMeshActivator(privacy_budget=0.1)
    await activator.activate_sovereign_mesh([])

    insight = {"alpha_roi": 0.12, "strategy": "long_science"}
    # Should not raise error
    await activator.broadcast_federated_insight("global_benchmarks", insight)

@pytest.mark.asyncio
async def test_mesh_decommission():
    activator = SovereignMeshActivator()
    await activator.activate_sovereign_mesh([])
    await activator.decommission_node()
    assert activator.is_active is False
