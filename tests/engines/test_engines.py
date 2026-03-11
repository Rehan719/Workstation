import pytest
from agentic_core.twinning.reactor_twin import ReactorTwin
from agentic_core.optimization.aro_engine import AROEngine
from agentic_core.teams.team_orchestrator import TeamOrchestrator
from agentic_core.drad.assembler import DRADAssembler

def test_twinning_fidelity():
    twin = ReactorTwin("science_reactor")
    twin.sync_telemetry({"temp": 300, "pressure": 1.0})
    result = twin.run_simulation({"stress_test": "thermal"})
    assert result["confidence"] >= 0.95

def test_aro_waste_limit():
    aro = AROEngine(waste_limit=0.05)
    aro.allocate_resources("task_1", priority=1)
    waste = aro.compute_waste()
    assert waste <= 0.05

def test_bto_team_formation():
    orchestrator = TeamOrchestrator()
    team_id = orchestrator.form_team(["agent1", "agent2"], "data_synthesis")
    assert team_id is not None
    assert orchestrator.get_team_health(team_id) >= 0.9

def test_drad_scale_up_time():
    assembler = DRADAssembler(scale_up_limit=30)
    resource_id = assembler.assemble_resource({"type": "cpu_node"})
    assert resource_id.startswith("res_")
    assembler.disassemble_resource(resource_id)
    assert resource_id not in assembler.active_resources
