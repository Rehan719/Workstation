import pytest
from agentic_core.mesh.consensus.consensus import MeshConsensus
@pytest.mark.asyncio
async def test_consensus():
    c = MeshConsensus("A", {"A": 0.9, "B": 0.9})
    assert await c.reach_consensus({"id": "p1"}, ["B"]) is True
    assert await c.reach_consensus({"id": "fail"}, ["B"]) is False
