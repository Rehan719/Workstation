import pytest
import asyncio
from agentic_core.mesh.recirculation.global_omega import GlobalOmegaProtocol
from agentic_core.mesh.aggregator.federated_aggregator import FederatedAggregator
from agentic_core.mesh.treaty.renegotiation import AutonomousRenegotiator
from agentic_core.mesh.federation.cluster_bridge import ClusterBridge
from agentic_core.collaboration.arms_length import ArmsLengthAgency

@pytest.mark.asyncio
async def test_global_omega_protocol():
    agg = FederatedAggregator(epsilon=0.5)
    proto = GlobalOmegaProtocol("node_1", agg)
    res = await proto.execute_macro_cycle(["node_2", "node_3"])
    assert res["entropy_reduction"] >= -1.0

@pytest.mark.asyncio
async def test_autonomous_renegotiation():
    # Ledger and negotiator are required. We mock the minimal attributes.
    class MockLedger: treaties = {"T1": {"terms": {}, "status": "active"}}
    class MockNegotiator:
        async def negotiate(self, i1, i2): return {"terms": {"new": "terms"}, "wasserstein": 0.01}

    renegot = AutonomousRenegotiator("node_1", ledger=MockLedger(), negotiator=MockNegotiator())
    # Renegotiate if delta > 0.05
    res = await renegot.renegotiate_if_needed("T1", 0.1)
    assert res is True

@pytest.mark.asyncio
async def test_cluster_bridge_sync():
    bridge = ClusterBridge("cluster_A")
    await bridge.connect_to_remote_cluster("cluster_B")
    await bridge.broadcast_to_federation({"id": "msg_001"})
    assert "cluster_B" in bridge.connected_clusters

@pytest.mark.asyncio
async def test_arms_length_collaboration():
    agency = ArmsLengthAgency("node_0")
    bid = await agency.issue_briefing("agent_1", {"task": "solve"}, constraints={})
    assert bid is not None
