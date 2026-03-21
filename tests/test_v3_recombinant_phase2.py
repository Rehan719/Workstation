import pytest
import asyncio
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l7_module_library.registry import module_registry
from agentic_core.layers.l8_recombination.merger import model_merger
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator
from agentic_core.layers.l11_civilisation.civilisation import federation_manager

def test_l7_real_metadata_parsing():
    # Verify production-grade models
    modules = list(module_registry.storage.values())
    assert len(modules) >= 4
    assert any("Llama" in m["name"] for m in modules)

def test_l8_mergekit_simulation():
    parents = [m["id"] for m in list(module_registry.storage.values())[:2]]
    res = model_merger.execute_merging(parents, strategy="TIES")
    assert res["performance"]["base_fitness"] >= 0.8
    assert res["strategy"] == "TIES"

@pytest.mark.asyncio
async def test_l9_nats_etcd_orchestration():
    goal = "Establish a federated knowledge garden."
    swarm_id = await swarm_orchestrator.form_swarm(goal)
    assert "swarm-" in swarm_id
    assert swarm_orchestrator.active_swarms[swarm_id]["inter_agent_latency_ms"] < 10

def test_l11_federated_discovery():
    res = federation_manager.discover_cross_node("reasoning")
    assert len(res) > 0
    assert "node-42" in [r["peer"] for r in res]

def test_floor_22_gaas_enforcement():
    # Test Article 1104: ε≤0.1
    res = validator_l1.validate_action("federated_learning", {"epsilon": 0.5})
    assert res["valid"] == False
    assert "Article 1104" in res["reason"]

    # Test Article 1107: PQC active
    res = validator_l1.validate_action("inter_node_comm", {"pqc_active": False})
    assert res["valid"] == False

if __name__ == "__main__":
    test_l7_real_metadata_parsing()
    test_l8_mergekit_simulation()
    asyncio.run(test_l9_nats_etcd_orchestration())
    test_l11_federated_discovery()
    test_floor_22_gaas_enforcement()
    print("v3.0 Recombinant Phase 2 Production Tests PASSED.")
