import pytest
import time
from agentic_core.homeostasis.orchestrator_v136 import HomeostaticOrchestratorV136

def test_homeostatic_orchestrator_initialization():
    orchestrator = HomeostaticOrchestratorV136()
    status = orchestrator.get_status()
    assert status["888_HOLD"] == False
    assert "network_latency" in status["metrics"]
    assert status["setpoints"]["network_latency"] == 50.0

def test_homeostatic_regulation_cycle():
    orchestrator = HomeostaticOrchestratorV136()
    # Simulate mild high latency (within hold threshold)
    orchestrator.ingest_telemetry({"network_latency": 54.0})
    cycle_result = orchestrator.run_regulation_cycle()

    assert cycle_result["status"] == "ACTIVE"
    assert "network_latency" in cycle_result["adjustments"]
    # For latency, output = setpoint (50) - current (150) = -100.
    # _map_output_to_action returns ROUTE_TRAFFIC_TO_EDGE if output < 0.
    assert cycle_result["adjustments"]["network_latency"] == "ROUTE_TRAFFIC_TO_EDGE"

def test_888_hold_trigger():
    orchestrator = HomeostaticOrchestratorV136()
    # Trigger massive deviation
    orchestrator.ingest_telemetry({
        "network_latency": 500.0,
        "task_throughput": 0.0,
        "anomaly_score": 0.9,
        "trust_score": 0.1
    })

    status = orchestrator.get_status()
    assert status["888_HOLD"] == True

    cycle_result = orchestrator.run_regulation_cycle()
    assert cycle_result["status"] == "HOLD"
    assert "SUSPEND_NON_CRITICAL_OPERATIONS" in cycle_result["action"]

def test_888_hold_release():
    orchestrator = HomeostaticOrchestratorV136()
    orchestrator.ingest_telemetry({"network_latency": 500.0}) # Trigger hold
    assert orchestrator.is_holding == True

    # Restore stability
    orchestrator.ingest_telemetry({"network_latency": 52.0})
    assert orchestrator.is_holding == False

    cycle_result = orchestrator.run_regulation_cycle()
    assert cycle_result["status"] == "ACTIVE"
