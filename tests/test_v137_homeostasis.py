import pytest
from agentic_core.homeostasis.orchestrator_v137 import HomeostaticOrchestratorV137

def test_v137_homeostasis_initialization():
    orchestrator = HomeostaticOrchestratorV137()
    status = orchestrator.get_layer_status()
    assert status["setpoints"]["civilizational"] == 50
    assert status["is_holding"] == False

def test_v137_regulation_cycle():
    orchestrator = HomeostaticOrchestratorV137()
    # Set other metrics close to setpoints to avoid 888_HOLD
    orchestrator.ingest_telemetry({
        "mycelial": 0.05,
        "ant_colony": 1000,
        "octopus": 0.2,
        "immune": 0.99,
        "symbiotic": 0.85,
        "civilizational": 46 # Close to 50
    })
    result = orchestrator.run_regulation_cycle()

    assert result["status"] == "ACTIVE"
    assert "civilizational" in result["adjustments"]
    # 50 - 10 = 40 (positive error). Map actuator returns PROVISION_NODE for output > 0.
    assert result["adjustments"]["civilizational"]["action"] == "PROVISION_NODE"

def test_v137_888_hold():
    orchestrator = HomeostaticOrchestratorV137()
    # Massive latency spike
    orchestrator.ingest_telemetry({"mycelial": 100.0}) # Setpoint is 0.05
    assert orchestrator.is_holding == True

    result = orchestrator.run_regulation_cycle()
    assert result["status"] == "HOLD"
