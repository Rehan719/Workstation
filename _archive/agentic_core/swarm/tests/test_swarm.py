import pytest
from agentic_core.swarm.swarm_orchestrator import SovereignSwarmCoordinator
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_swarm_spawn_and_consensus():
    ueg = VSBUEGLogger()
    orchestrator = SovereignSwarmCoordinator(ueg)

    # 1. Spawn
    agent_ids = await orchestrator.spawn_super_agent_swarm("Research target asset liquidity", size=5)
    assert len(agent_ids) == 5

    # 2. Consensus
    proposal = {"id": "p1", "action": "allocate_capital"}
    res = await orchestrator.hotstuff2_consensus(proposal, agent_ids)

    assert res["status"] in ["RATIFIED", "REJECTED", "INVALIDATED"]
