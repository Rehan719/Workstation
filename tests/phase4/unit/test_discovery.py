import pytest
from agentic_core.mesh.discovery.discovery import MeshDiscovery, PeerID
@pytest.mark.asyncio
async def test_discovery():
    discovery = MeshDiscovery(PeerID("A"))
    peers = await discovery.discover_peers("test")
    assert len(peers) > 0
