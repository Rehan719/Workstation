import asyncio
import pytest
from agentic_core.orchestrator.synergy import SynergyOrchestrator
from agentic_core.reactor.science.physics import PhysicsReactor
from agentic_core.reactor.ecosystem.registry import ReactorRegistry

@pytest.fixture
def synergy():
    return SynergyOrchestrator()

@pytest.fixture
def registry():
    return ReactorRegistry()

@pytest.mark.asyncio
async def test_mega_twin_workflow_startup(synergy, registry):
    # Register required reactors
    registry.register(PhysicsReactor()) # Using physics as a stand-in for science component

    # Workflow 1: Startup Ecosystem Mega-Twin
    # Involves Business, Law, Finance, Career
    reactors = ["science:physics", "law:contract"] # Simplified for test
    objective = "Startup Ecosystem Simulation"
    user_id = "founder_001"

    result = await synergy.execute_mega_twin(objective, reactors, user_id, domain="business", tier="pro")

    assert result["status"] == "SUCCESS"
    assert "team_id" in result
    assert "pool_id" in result
    assert len(result["results"]) > 0
    assert result["message"] == "Mega-Twin Synergy Apotheosis Achieved."

@pytest.mark.asyncio
async def test_mega_twin_workflow_bio_research(synergy, registry):
    # Workflow 5: Computational Biology Research Workflow
    reactors = ["science:physics", "science:biology"]
    objective = "Genomic ML Model Validation"

    result = await synergy.execute_mega_twin(objective, reactors, "scientist_001", domain="science")

    assert result["status"] == "SUCCESS"
    assert any(r.get("fidelity", 0) >= 0.95 for r in result["results"])
