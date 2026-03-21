import pytest
import asyncio
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l4_regulation.regulation import grn_engine
from agentic_core.layers.l8_recombination.merger import model_merger
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator
from agentic_core.layers.l12_ux.ux_engine import experience_engine

def test_l4_learner_optimization():
    # Pillar 1 check: Fatigue stress simulation
    metrics = {"interaction_speed": 1.8, "accuracy_rate": 0.6}
    plan = grn_engine.run_learner_optimization(metrics)
    assert plan["recommended_state"] == "RECUPERATE"
    assert plan["target_intensity"] < 0.5

def test_l8_nas_recombination():
    parents = ["did:vsb:module-m1", "did:vsb:module-m2"]
    # Should use NAS to find params since none provided
    res = model_merger.execute_merging(parents)
    assert res["merge_config"]["params"]["density"] == 0.4
    assert res["performance"]["base_fitness"] > 0

@pytest.mark.asyncio
async def test_l9_phi3_distributed_swarm():
    goal = "Synthesize a global energy research report."
    swarm_id = await swarm_orchestrator.form_distributed_swarm(goal)
    assert "swarm-" in swarm_id
    assert swarm_orchestrator.active_swarms[swarm_id]["status"] == "OPERATIONAL"

def test_l12_fabric_vitals():
    vitals = experience_engine.get_fabric_vitals()
    assert vitals["avatar"] == "WebRTC-Operational"
    assert vitals["signal"] == "libp2p-Gossip-Active"

def test_l1_live_validation():
    # Article 1104: ε check
    res = validator_l1.validate_action("federated_sync", {"epsilon": 0.5, "pqc_active": True})
    assert res["valid"] == False
    assert "Article 1104" in res["reason"]

if __name__ == "__main__":
    test_l4_learner_optimization()
    test_l8_nas_recombination()
    asyncio.run(test_l9_phi3_distributed_swarm())
    test_l12_fabric_vitals()
    test_l1_live_validation()
    print("v3.0 Phase 2 Enhanced Production Tests PASSED.")
