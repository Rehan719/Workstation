import pytest
import asyncio
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l7_module_library.registry import module_registry
from agentic_core.layers.l8_recombination.merger import model_merger
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator
from agentic_core.layers.l11_civilisation.civilisation import federation_dht, fl_manager
from agentic_core.layers.l2_hardware.inference import inference_engine

def test_l7_real_ingestion():
    # Verify production models are registered
    modules = list(module_registry.storage.values())
    assert len(modules) >= 4
    assert any("Mistral" in m["name"] for m in modules)

def test_l8_mergekit_production():
    parents = [m["id"] for m in list(module_registry.storage.values())[:2]]
    res = model_merger.execute_merging(parents, strategy="TIES")
    assert res["performance"]["base_fitness"] > 0.8
    assert "pqc_status" in res

@pytest.mark.asyncio
async def test_l9_nats_etcd_production():
    goal = "Activate planetary mesh orchestration."
    swarm_id = await swarm_orchestrator.form_swarm(goal)
    assert "swarm-" in swarm_id
    assert swarm_orchestrator.active_swarms[swarm_id]["pqc_active"] == True

def test_l11_civilization_scaling():
    # Test DHT discovery scale
    peers = federation_dht.routing_table
    assert len(peers) == 50
    # Test Privacy (Article 1104)
    with pytest.raises(ValueError, match="Article 1104"):
        fl_manager.aggregate_gradients([], epsilon=0.5)

def test_l2_cl1_production():
    res = inference_engine.run_inference("test-agent", "input", backend="cl1")
    assert res["device"] == "CL1-Bio-Unit"
    assert res["energy_gain"] >= 10.0

if __name__ == "__main__":
    test_l7_real_ingestion()
    test_l8_mergekit_production()
    asyncio.run(test_l9_nats_etcd_production())
    test_l11_civilization_scaling()
    test_l2_cl1_production()
    print("v3.0 Recombinant Phase 2 Production Integration Tests PASSED.")
