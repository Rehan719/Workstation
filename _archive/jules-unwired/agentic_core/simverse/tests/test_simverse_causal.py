import pytest
import numpy as np
from agentic_core.simverse.causal_simulator import SimVerseCausalSimulator, DynamoInference
from agentic_core.ueg.logger import VSBUEGLogger
from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger

@pytest.mark.asyncio
async def test_simverse_causal_fidelity():
    ueg = VSBUEGLogger()
    sim = SimVerseCausalSimulator(ueg)

    scenario = {"id": "scenario_drift", "physically_grounded": True, "horizon_steps": 50}
    state = {"target_metric": 0.95}

    res = await sim.run_causal_forecast(scenario, state)
    assert res["fidelity"] >= 0.90
    assert "csl_attestation" in res
    assert "metering" in res

@pytest.mark.asyncio
async def test_dynamo_disaggregated_scheduling():
    tfel = ThermodynamicFreeEnergyLedger()
    dynamo = DynamoInference(tfel)

    batch = [{"id": 1}, {"id": 2}]
    res = await dynamo.schedule_disaggregated(batch)

    assert res["latency_ms"] < 100
    assert "metering" in res
    assert res["disaggregation_mode"] == "layer_parallel_emulated"
