import asyncio
import pytest
import numpy as np
from agentic_core.simulation.engine import EnvironmentalSimulator
from agentic_core.simulation.registry import TwinRegistry

@pytest.fixture
def ese():
    return EnvironmentalSimulator()

@pytest.fixture
def registry():
    return TwinRegistry(db_path=":memory:")

@pytest.mark.asyncio
async def test_physics_simulation_fidelity():
    simulator = EnvironmentalSimulator()
    # Mock registry with memory DB for testing if needed,
    # but here we'll use the default and just verify logic

    twin_id = "test_physics_twin"
    reactor_id = "science:physics"
    initial_state = {
        "data": {
            "bodies": [
                {"id": "p1", "position": [0, 10, 0], "velocity": [1, 0, 0], "acceleration": [0, -9.81, 0]}
            ]
        }
    }

    simulator.registry.register_twin(twin_id, reactor_id, initial_state)

    # Run 100 steps
    result = await simulator.run_simulation(twin_id, steps=100, mode="physics")

    assert result["status"] == "SUCCESS"
    assert result["fidelity"] >= 0.95

    final_pos = result["state"]["data"]["bodies"][0]["position"]
    # x = x0 + v0*t = 0 + 1 * (100 * 0.01) = 1.0
    # y = y0 + v0y*t + 0.5*a*t^2 = 10 + 0 - 0.5 * 9.81 * 1^2 = 5.095
    assert np.isclose(final_pos[0], 1.0, atol=0.1)
    assert np.isclose(final_pos[1], 5.095, atol=0.1)

@pytest.mark.asyncio
async def test_abm_simulation_summary():
    simulator = EnvironmentalSimulator()
    twin_id = "test_abm_twin"
    initial_state = {
        "data": {
            "agents": [
                {"id": "a1", "attributes": {"strategy": "cooperate", "utility": 0}},
                {"id": "a2", "attributes": {"strategy": "opportunistic", "utility": 0}}
            ]
        }
    }
    simulator.registry.register_twin(twin_id, "social:market", initial_state)

    result = await simulator.run_simulation(twin_id, steps=10, mode="abm")

    assert result["status"] == "SUCCESS"
    summary = result["state"]["data"]["summary"]
    assert summary["total_agents"] == 2
    assert summary["tick"] == 10
    assert summary["avg_utility"] > 0
