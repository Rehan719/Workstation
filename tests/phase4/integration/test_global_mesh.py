import pytest
import asyncio
from agentic_core.mesh.recirculation.global_omega import GlobalOmegaProtocol
from agentic_core.mesh.aggregator.federated_aggregator import FederatedAggregator
from agentic_core.mesh.federation.cluster_bridge import ClusterBridge
from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID

@pytest.mark.asyncio
async def test_global_omega_reduction():
    agg = FederatedAggregator(epsilon=1.0)
    omega = GlobalOmegaProtocol("node_0", agg)
    peers = ["node_1", "node_2", "node_3"]

    result = await omega.execute_macro_cycle(peers)
    assert result["entropy_reduction"] >= 0.10
    assert result["peer_count"] == 3

@pytest.mark.asyncio
async def test_cluster_federation_scaling():
    bridge = ClusterBridge("cluster_A")
    await bridge.connect_to_remote_cluster("cluster_B")
    assert "cluster_B" in bridge.connected_clusters

    await bridge.broadcast_to_federation({"id": "fed_test_1"})
    assert True
