from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l2_hardware.inference import inference_engine
from agentic_core.layers.l5_resilience.resilience import resilience_manager
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator
from agentic_core.layers.ueg import ueg

def test_l1_validation():
    print("Testing L1 Validation...")
    # Valid action
    assert validator_l1.validate_action("recombine", {"models": ["m1"], "fitness": 0.95}) == True
    # Invalid action (Article 1095)
    assert validator_l1.validate_action("recombine", {"models": ["m1"]}) == False
    print("L1 Validation passed.")

def test_l2_cl1_simulation():
    print("Testing L2 CL1 Simulation...")
    res = inference_engine.run_inference("test-model", "test-input", backend="cl1")
    assert res["device"] == "CL1-Bio-Compute"
    assert "spike_count" in res
    assert res["latency_ms"] < 10
    print("L2 CL1 Simulation passed.")

def test_l5_resilience_t1():
    print("Testing L5 Resilience T1...")
    data = "corrupt-data"
    expected_hash = "correct-hash"
    # Tier 1 should detect failure
    res = resilience_manager.handle_failure("l2-inference", "CHECKSUM_ERROR", {"data": data, "expected_hash": expected_hash})
    assert res == False
    assert len(resilience_manager.repair_history) > 0
    print("L5 Resilience T1 passed.")

def test_l9_orchestration():
    print("Testing L9 Orchestration...")
    swarm_id = swarm_orchestrator.form_swarm("Conduct a research on biomimetic AI.")
    assert "swarm-" in swarm_id
    assert swarm_id in swarm_orchestrator.active_swarms
    print("L9 Orchestration passed.")

def test_ueg_logging():
    print("Testing UEG Logging...")
    ueg.set_level("FULL")
    ueg.log_event("L12", "TEST", "UNIT_TEST", {"status": "ok"})
    events = ueg.get_events(event_type="UNIT_TEST")
    assert len(events) > 0
    assert events[0]["layer"] == "L12"
    print("UEG Logging passed.")

if __name__ == "__main__":
    test_l1_validation()
    test_l2_cl1_simulation()
    test_l5_resilience_t1()
    test_l9_orchestration()
    test_ueg_logging()
    print("All v154.0 Genesis Phase 1 Integration Tests Passed.")
