import pytest
import asyncio
from agentic_core.mesh.consensus.consensus import MeshConsensus

class MockHealth:
    def __init__(self, reps): self.reps = reps
    def get_reputation(self, p): return self.reps.get(p, 0.5)

@pytest.mark.asyncio
async def test_byzantine_success_with_minor_faults():
    # Scenario: Majority are healthy.
    # root (1.0) + node_1 (1.0) = 2.0 agreed
    # faulty_1 (0.1) votes False
    # Total: 1.0 + 1.0 + 0.1 = 2.1
    # 2.0 / 2.1 = 0.95 > 0.67
    health = MockHealth({"root": 1.0, "node_1": 1.0, "faulty_1": 0.1})
    consensus = MeshConsensus("root", health)
    peers = ["node_1", "faulty_1"]
    result = await consensus.reach_consensus({"id": "p1"}, peers)
    assert result is True

@pytest.mark.asyncio
async def test_byzantine_failure_with_high_rep_malicious_nodes():
    # Scenario: Two high-reputation nodes are Byzantine (maliciously voting False)
    # root (1.0) agrees.
    # byzantine_1 (1.0) votes False.
    # byzantine_2 (1.0) votes False.
    # Total: 1.0 + 1.0 + 1.0 = 3.0
    # Agreed: 1.0
    # 1.0 / 3.0 = 0.33 < 0.67
    health = MockHealth({"root": 1.0, "byzantine_1": 1.0, "byzantine_2": 1.0})
    consensus = MeshConsensus("root", health)
    peers = ["byzantine_1", "byzantine_2"]
    result = await consensus.reach_consensus({"id": "p2"}, peers)
    assert result is False

@pytest.mark.asyncio
async def test_byzantine_failure_with_weak_proposer():
    # Scenario: Proposer has low reputation, healthy peers cannot save it if they are outnumbered
    # root (0.1) agrees.
    # node_1 (0.5) votes True.
    # byzantine_1 (1.0) votes False.
    # Total: 0.1 + 0.5 + 1.0 = 1.6
    # Agreed: 0.1 + 0.5 = 0.6
    # 0.6 / 1.6 = 0.375 < 0.67
    health = MockHealth({"root": 0.1, "node_1": 0.5, "byzantine_1": 1.0})
    consensus = MeshConsensus("root", health)
    peers = ["node_1", "byzantine_1"]
    result = await consensus.reach_consensus({"id": "p3"}, peers)
    assert result is False
