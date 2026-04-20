import pytest
import asyncio
from agentic_core.mega_project.synthesizer import MegaProjectSynthesizer
from agentic_core.collaboration.review_gates import ReviewGate

@pytest.mark.asyncio
async def test_mega_project_synthesis():
    synth = MegaProjectSynthesizer("Biofoundry_X")
    deliverables = await synth.generate_deliverables()
    assert deliverables["project"] == "Biofoundry_X"
    assert deliverables["feasibility"]["market_fidelity"] > 0.9

@pytest.mark.asyncio
async def test_review_gate_approval():
    gate = ReviewGate("Strategic_Signoff")
    # Auto-pass if no feedback provided for simulation
    assert await gate.review_artifact({"plan": "v1"}) is True
    # Human rejection
    assert await gate.review_artifact({"plan": "v1"}, human_feedback="Reject: Needs more detail") is False
