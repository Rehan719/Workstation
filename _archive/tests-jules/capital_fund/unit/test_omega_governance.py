import pytest
from agentic_core.governance.ai_governor import AIGovernor
from agentic_core.governance.live_council_router import LiveCouncilRouter

@pytest.mark.asyncio
async def test_ai_governor_proposal():
    governor = AIGovernor(owner_uid="owner_1")
    proposal_id = await governor.propose_autonomous_amendment("TEST_DRIFT", {"psi": 0.82})
    assert proposal_id.startswith("amend_")

@pytest.mark.asyncio
async def test_council_router_veto():
    router = LiveCouncilRouter()

    # Valid proposal
    proposal = {"proposal_id": "p1", "proposed_change": "OPTIMIZE_LIQUIDITY_RESERVE", "magnitude": 0.02}
    status = await router.route_governance_proposal(proposal)
    assert status == "ROUTED"

    # Invalid (Veto)
    bad_proposal = {"proposal_id": "p2", "proposed_change": "OPTIMIZE_LIQUIDITY_RESERVE", "magnitude": 0.08}
    status_veto = await router.route_governance_proposal(bad_proposal)
    assert status_veto == "VETOED"

@pytest.mark.asyncio
async def test_council_quorum_lifecycle():
    router = LiveCouncilRouter()
    proposal = {"proposal_id": "p3", "proposed_change": "STRATEGY_SHIFT", "magnitude": 0.0}
    await router.route_governance_proposal(proposal)

    # Cast 3 votes (Quorum = 3)
    await router.cast_council_vote("p3", "did:1", True)
    await router.cast_council_vote("p3", "did:2", True)
    reached = await router.cast_council_vote("p3", "did:3", True)

    assert reached is True
    assert router.active_votes["p3"]["status"] == "APPROVED"
