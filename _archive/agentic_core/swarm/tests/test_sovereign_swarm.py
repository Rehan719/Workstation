import pytest
from agentic_core.swarm.swarm_orchestrator import SovereignSwarmCoordinator

@pytest.mark.asyncio
async def test_sovereign_swarm_consensus():
    coordinator = SovereignSwarmCoordinator()

    # 1. Spawn
    agents = await coordinator.spawn_super_agent_swarm("Simulate market shock v4", size=7)
    assert len(agents) == 7

    # 2. Consensus ( f < n/3, so 7 nodes can tolerate 2 faults. Quorum = 2*7/3 + 1 = 5)
    res = await coordinator.hotstuff2_consensus({"action": "rebalance"}, agents)
    assert res["quorum_target"] == 5
    assert res["status"] in ["RATIFIED", "REJECTED", "INVALIDATED"]
