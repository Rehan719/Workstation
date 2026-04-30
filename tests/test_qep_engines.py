import pytest
import asyncio
from agentic_core.simulation.ese import get_ese_instance
from agentic_core.optimization.aro import get_aro_instance
from agentic_core.biomimicry.geospheric.drad import get_drad_instance
from agentic_core.bto.religion_bto import get_religion_bto
from agentic_core.swarm.signaling_protocol import SignalingProtocol

@pytest.mark.asyncio
async def test_ese_simulation():
    ese = get_ese_instance(num_agents=50)
    results = await ese.run_simulation(steps=10)
    assert results["engine"] == "ESE"
    assert results["steps_completed"] == 10
    assert "final_avg_belief" in results
    assert len(results["history"]) == 10

def test_aro_optimization():
    aro = get_aro_instance()
    constraints = {"sim_demand": 0.7, "reason_demand": 0.3}
    results = aro.optimize(constraints)
    assert results["engine"] == "ARO"
    assert "allocation" in results
    assert abs(sum(results["allocation"].values()) - 1.0) < 1e-6

def test_drad_monitoring():
    drad = get_drad_instance()
    telemetry = {"latency": 250, "error_rate": 0.06}
    results = drad.monitor(telemetry)
    assert results["engine"] == "DRAD"
    assert results["status"] == "CRITICAL"
    assert len(results["active_adaptations"]) > 0

def test_religion_bto_orchestration():
    signaling = SignalingProtocol("TEST-SENDER")
    bto = get_religion_bto("TEST-BTO", signaling)
    results = bto.orchestrate_research("Quranic Ethics")
    assert results["engine"] == "BTO"
    assert results["tasks_created"] == 4
    assert results["status"] == "SWARM_ACTIVE"
