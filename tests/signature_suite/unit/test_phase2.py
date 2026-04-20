import pytest
import asyncio
from agentic_core.cognitive.cascade import BiomimeticCascade
from agentic_core.cognitive.meta_cognition import MetaCognitionEngine
from agentic_core.collaboration.arms_length import ArmsLengthAgency

@pytest.mark.asyncio
async def test_cognitive_cascade():
    cascade = BiomimeticCascade()
    res = await cascade.run_cascade("initial_signal")
    assert len(res) == 6
    assert res[-1]["engine"] == "iman"

@pytest.mark.asyncio
async def test_meta_cognition():
    meta = MetaCognitionEngine()
    intro = await meta.introspect({"internal": "state"})
    extro = await meta.extrospect({"external": "market"})
    retro = await meta.retrospect([{"past": "event"}])
    assert intro["health"] == 1.0
    assert extro["market_fit"] > 0.8
    assert retro["optimization_found"] is True

@pytest.mark.asyncio
async def test_arms_length_collaboration():
    agency = ArmsLengthAgency("node_0")
    bid = await agency.send_briefing("agent_1", {"task": "solve"})
    assert bid is not None
    assert await agency.receive_debriefing(bid, {"outcome": "success"}) is True
