import asyncio
import pytest
import numpy as np
from agentic_core.teams.engine import BiomimeticTeamOrchestrator

@pytest.fixture
def bto():
    return BiomimeticTeamOrchestrator()

@pytest.mark.asyncio
async def test_vtf_formation_and_negotiation(bto):
    intent_id = "test_001"
    domain = "science"
    requirements = ["physics_agent", "math_agent", "reviewer_agent"]

    team_id = await bto.form_vtf(intent_id, domain, requirements)

    assert team_id == f"vtf_{intent_id}_{domain}"
    team = bto.registry.active_teams[team_id]
    assert team["status"] == "OPERATIONAL"
    assert len(team["members"]) == 3
    assert "roles" in team

    # Verify at least one leader was assigned
    roles = team["roles"].values()
    assert "LEADER" in roles
    assert "REVIEWER" in roles or "SPECIALIST" in roles

@pytest.mark.asyncio
async def test_collective_memory_propagation(bto):
    team_id = "vtf_test_mem"
    domain = "law"
    strategy = "HIERARCHICAL_REVIEW"

    # Record a success
    bto.record_vtf_success(team_id, domain, strategy, {"summary": "Passed audit", "fidelity": 0.98})

    # Query best strategies
    best = bto.memory.query_best_strategies(domain)
    assert strategy in best

    insights = bto.memory.get_insights()
    assert insights["total_experiences"] >= 1
    assert domain in insights["domains_covered"]

def test_consensus_building(bto):
    proposals = [
        {"option": "Plan A", "confidence": 0.9},
        {"option": "Plan B", "confidence": 0.4},
        {"option": "Plan A", "confidence": 0.7}
    ]
    # Plan A total confidence = 1.6, Plan B = 0.4

    result = bto.negotiation.build_consensus(proposals)
    assert result["winner"] == "Plan A"
    assert result["consensus_reached"] is True
    assert result["confidence"] == 1.6 / 2.0
