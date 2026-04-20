import pytest
from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID
from agentic_core.mesh.aggregator.federated_aggregator import FederatedAggregator

@pytest.mark.asyncio
async def test_weight_sync_integration():
    d = MeshDiscovery(PeerID("root"))
    # High epsilon to minimize noise
    a = FederatedAggregator(discovery=d, epsilon=100.0)
    peers = await d.discover_peers("weights")
    res = a.aggregate([a.weights] * len(peers))
    # Check it's close to 0.30 (free_energy default)
    assert abs(res["free_energy"] - 0.30) < 0.05
