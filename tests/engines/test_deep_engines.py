import pytest
import time
from agentic_core.twinning.reactor_twin import ReactorTwin
from agentic_core.twinning.twin_registry import TwinRegistry
from agentic_core.optimization.aro_engine import AROEngine
from agentic_core.optimization.demand_predictor import DemandPredictor
from agentic_core.teams.team_orchestrator import TeamOrchestrator
from agentic_core.teams.team_health import TeamHealthMonitor
from agentic_core.drad.assembler import DRADAssembler
from agentic_core.drad.ral_parser import RALParser

def test_twinning_registry_integration():
    registry = TwinRegistry(":memory:")
    registry.register_twin("twin_01", "physics", 0.95)
    twin_data = registry.get_twin("twin_01")
    assert twin_data["reactor_id"] == "physics"
    assert twin_data["fidelity_target"] == 0.95

def test_aro_demand_prediction():
    predictor = DemandPredictor(history_size=10)
    for v in [1.0, 1.2, 1.4, 1.6, 1.8]:
        predictor.observe(v)
    prediction = predictor.predict_next()
    assert prediction > 1.8 # Upward trend

def test_bto_health_monitoring():
    monitor = TeamHealthMonitor(threshold=0.9)
    # Healthy team
    health = monitor.compute_health({"latency": 100, "error_rate": 0.05, "resonance": 0.95})
    assert monitor.is_healthy(health)
    # Unhealthy team
    health_bad = monitor.compute_health({"latency": 1500, "error_rate": 0.5, "resonance": 0.5})
    assert not monitor.is_healthy(health_bad)

def test_drad_ral_parsing():
    parser = RALParser()
    spec_yaml = """
kind: EphemeralPool
metadata:
  name: test-pool
spec:
  resources: {cpu: 2, mem: 4Gi}
  network: {type: bridge}
"""
    spec = parser.parse_spec(spec_yaml)
    assert spec['kind'] == 'EphemeralPool'
    plan = parser.generate_assembly_plan(spec)
    assert len(plan) == 3
    assert plan[0]['step'] == "provision_compute"
