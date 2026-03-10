import pytest
import asyncio
from agentic_core.orchestrator.synergy import SynergyOrchestrator
from agentic_core.reactor.science.physics import PhysicsReactor
from agentic_core.reactor.religion.tafsir import TafsirReactor
from agentic_core.reactor.ecosystem.registry import ReactorRegistry

@pytest.mark.asyncio
async def test_v100_mega_twin_synergy():
    # ARTICLE 320: Mega-Twin Synergy Verification
    registry = ReactorRegistry()

    # 1. Register Sub-Reactors
    physics = PhysicsReactor()
    tafsir = TafsirReactor()
    registry.register(physics)
    registry.register(tafsir)

    orchestrator = SynergyOrchestrator()

    # 2. Execute Mega-Twin (Cross-Domain)
    objective = "Analyze Quantum Biology from Islamic Perspective"
    reactors = ["science:physics", "religion:tafsir"]

    result = await orchestrator.execute_mega_twin(objective, reactors, "user_jules")

    # 3. Validation
    assert result["status"] == "SUCCESS"
    assert result["objective"] == objective
    assert len(result["results"]) == 2
    assert "SUCCESS" in [res.get("status") for res in result["results"]]

    print(f"Synergy Test Result: {result['message']}")

@pytest.mark.asyncio
async def test_drad_fabric_assembly():
    # ARTICLE 318: Dynamic Resource Fabric Verification
    orchestrator = SynergyOrchestrator()
    fabric = orchestrator.fabric

    initial_inv = fabric.get_inventory_status()
    initial_compute = initial_inv["compute"]["available"]

    # Assemble pool
    reqs = {"compute": 10, "api_quotas": 100}
    pool_id = fabric.assemble_pool(reqs)

    current_inv = fabric.get_inventory_status()
    assert current_inv["compute"]["available"] == initial_compute - 10

    # Disassemble pool
    fabric.disassemble_pool(pool_id)
    final_inv = fabric.get_inventory_status()
    assert final_inv["compute"]["available"] == initial_compute
