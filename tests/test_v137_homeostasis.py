import pytest
from agentic_core.homeostasis.orchestrator_v137 import HomeostaticOrchestratorV137

def test_v137_homeostasis_initialization():
    orchestrator = HomeostaticOrchestratorV137()
    status = orchestrator.get_status()
    assert "civilizational" in status["layers"]
    assert status["is_holding"] == False

def test_v137_regulation_cycle():
    orchestrator = HomeostaticOrchestratorV137()
    # Test multi-layer regulation
    telemetry = {
        "civilizational": {"node_count": 40}, # Target 50
        "mycelial": {"latency": 0.100} # Target 0.05
    }
    result = orchestrator.regulation_cycle(telemetry)

    assert result["status"] == "ACTIVE"
    assert "civilizational" in result["adjustments"]
    assert "node_count" in result["adjustments"]["civilizational"]
    assert result["adjustments"]["civilizational"]["node_count"] > 0

def test_v137_888_hold():
    orchestrator = HomeostaticOrchestratorV137()
    # Massive deviation triggers hold
    telemetry = {
        "mycelial": {"latency": 10.0}
    }
    result = orchestrator.regulation_cycle(telemetry)
    assert result["status"] == "HOLD"
    assert orchestrator.is_holding == True
