import pytest
from agentic_core.simverse.causal_simulator import SimVerseCausalSimulator, DynamoInference
from agentic_core.ueg.logger import VSBUEGLogger
from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger

@pytest.mark.asyncio
async def test_simverse_fidelity():
    ueg = VSBUEGLogger()
    simulator = SimVerseCausalSimulator(ueg)

    scenario = {"id": "s1", "physically_grounded": True, "horizon_steps": 5}
    initial_state = {"target_metric": 100.0}

    res = await simulator.run_causal_forecast(scenario, initial_state)
    assert res["fidelity"] >= 0.90
    assert "csl_attestation" in res

@pytest.mark.asyncio
async def test_dynamo_metering():
    tfel = ThermodynamicFreeEnergyLedger(budget_bits=1e12)
    dynamo = DynamoInference(tfel)

    tasks = [{"id": "t1"}, {"id": "t2"}]
    res = await dynamo.schedule_disaggregated(tasks)

    assert res["status"] == "SUCCESS"
    assert "metering" in res
