import pytest
from agentic_core.mesh.consensus.consensus import MeshConsensus

class MockHealth:
    def __init__(self, reps): self.reps = reps
    def get_reputation(self, p): return self.reps.get(p, 0.5)

@pytest.mark.asyncio
async def test_consensus():
    health = MockHealth({"A": 0.9, "B": 0.9})
    c = MeshConsensus("A", health)
    assert await c.reach_consensus({"id": "p1"}, ["B"]) is True
