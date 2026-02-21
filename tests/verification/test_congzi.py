import pytest
import asyncio
from agentic_core.reasoning.congzi_engine import CongziEngine

@pytest.mark.asyncio
async def test_congzi_verification_harness():
    engine = CongziEngine()
    report = await engine.run_verification_harness()

    assert "measured_accuracy" in report
    assert report["claim_validated"] is True
    assert report["total_questions"] == 3
    assert report["hallucination_rate"] < 0.10

@pytest.mark.asyncio
async def test_congzi_reasoning_trace():
    engine = CongziEngine()
    resp = await engine.reason("What is the speed of light in vacuum?")

    assert "reasoning_trace" in resp
    assert "chain_of_thought" in resp["reasoning_trace"]
    assert resp["reasoning_trace"]["epistemic_integrity_score"] > 0.90
