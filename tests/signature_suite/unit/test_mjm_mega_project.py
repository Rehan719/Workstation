import pytest
import asyncio
from agentic_core.organism.mjm_v4 import MJMOrchestratorV4
from agentic_core.mega_project.synthesizer import MegaProjectSynthesizer

@pytest.mark.asyncio
async def test_mjm_v4_lifecycle():
    mjm = MJMOrchestratorV4()
    res = await mjm.run_lifecycle("Initial Market Signal")
    assert res["compliance"] == 1.0
    assert res["result"] == "optimised"

def test_mega_project_synthesis():
    synth = MegaProjectSynthesizer()
    deliverables = synth.generate_deliverables("Quantum Bio-Foundry", {"market_gap": "Infinite"})
    assert "BUSINESS PLAN" in deliverables["business_plan"]
    assert "ROADMAP" in deliverables["roadmap"]
    assert "1.0" not in deliverables["business_plan"] # Just checking it's not a stub
