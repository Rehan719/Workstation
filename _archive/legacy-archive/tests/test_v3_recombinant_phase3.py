import pytest
import asyncio
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l11_civilisation.civilisation import mesh_controller
from agentic_core.layers.l2_hardware.inference import inference_engine
from agentic_core.layers.l1_identity.genome_engine import genome_engine
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator

def test_global_mesh_scale():
    status = mesh_controller.get_mesh_status()
    assert status["total_nodes"] >= 100
    assert "APAC-SOUTH" in status["regions"]
    assert status["p99_latency_ms"] < 30

def test_cl1_workload_offloading():
    # Run multiple inferences to check offloading stats
    for _ in range(10):
         inference_engine.run_inference("grn_inference", "data", priority="low_energy")

    # Should show CL1 activity
    assert inference_engine.workload_stats["cl1"] > 0
    assert "CL1-Biological-Cluster" in str(inference_engine.run_inference("grn_inference", "data"))

def test_genome_self_modification():
    patch = {"id": 1115, "title": "Experimental", "content": "Transcendence test."}
    prop_id = genome_engine.propose_mutation("ceo-agent", patch)

    # Apply authorized mutation
    success = genome_engine.apply_mutation(prop_id, patch, authorized=True)
    assert success == True
    assert any(a["id"] == 1115 for a in genome_engine.genome["constitution"]["articles"])

    # Test Rollback
    genome_engine.rollback()
    assert not any(a["id"] == 1115 for a in genome_engine.genome["constitution"]["articles"])

@pytest.mark.asyncio
async def test_autonomous_workflow_threshold():
    # Article 1112: 95% autonomy for low risk
    res = await swarm_orchestrator.execute_swarm_workflow("Auto task", risk_level="low")
    assert res["autonomy"] == True
    assert swarm_orchestrator.autonomy_stats["autonomous"] > 0

def test_floor_23_transcendence_gaas():
    # Article 1111: Rollback required
    res = validator_l1.validate_action("amend_genome", {"rollback_ready": False})
    assert res["valid"] == False

    res = validator_l1.validate_action("amend_genome", {"rollback_ready": True})
    assert res["valid"] == True

if __name__ == "__main__":
    test_global_mesh_scale()
    test_cl1_workload_offloading()
    test_genome_self_modification()
    asyncio.run(test_autonomous_workflow_threshold())
    test_floor_23_transcendence_gaas()
    print("v3.0 Recombinant Phase 3 Transcendence Tests PASSED.")
