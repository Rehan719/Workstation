import pytest
import asyncio
from agentic_core.synthesis.alphafold3_v16 import AlphaFold3Integrator
from agentic_core.simulation.cosmos3_v16 import WorldSimulatorV16
from agentic_core.biomimicry.minimisation.v2.recirculation_engine_v16 import RecirculationCampaignEngine

@pytest.mark.asyncio
async def test_alphafold3_v16():
    af3 = AlphaFold3Integrator()
    res = await af3.predict_complex({"protein": "MKT..."})
    assert res["plddt"] >= 0.85
    assert res["posebusters_pass"] is True

@pytest.mark.asyncio
async def test_cosmos3_v16():
    cosmos = WorldSimulatorV16()
    res = await cosmos.simulate_environment({"gravity": 9.81})
    assert res["fidelity"] >= 0.85
    assert res["status"] == "converged"

@pytest.mark.asyncio
async def test_recirculation_v16_macro():
    engine = RecirculationCampaignEngine()
    res = await engine.run_macro_cycle()
    assert res["improvement_delta"] >= 0.05
    assert res["duration_sec"] < 60.0
