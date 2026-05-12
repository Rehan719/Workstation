import pytest
from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID
@pytest.mark.asyncio
async def test_discovery_integration():
    d = MeshDiscovery(PeerID("root"))
    peers = await d.discover_peers("minimisation:weights")
    assert len(peers) >= 5
