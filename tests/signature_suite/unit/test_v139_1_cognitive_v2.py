import pytest
import asyncio
from agentic_core.cognitive.v2.engines_v2 import InkashafV2
from agentic_core.cognitive.v2.meta_cognition_v2 import MetaCognitionEngineV2
from agentic_core.cognitive.v2.cascade_controller_v2 import BiomimeticCascadeControllerV2

@pytest.mark.asyncio
async def test_cognitive_fidelity_v2():
    engine = InkashafV2()
    res = await engine.unveil("test_data")
    assert res["fidelity"] >= 0.92
    assert res["status"] == "processed"

@pytest.mark.asyncio
async def test_meta_cognition_v2_latency():
    meta = MetaCognitionEngineV2("node_0")
    res = await meta.introspect({"confidence": 0.98})
    assert res["confidence"] == 0.98
    # Micro latency < 80ms
    assert meta.cycle_latencies["micro"] < 80

@pytest.mark.asyncio
async def test_cascade_controller_v2():
    controller = BiomimeticCascadeControllerV2()
    res = await controller.execute_cascade("Establish planetary peace")
    assert res["fidelity"] >= 0.92
    assert "result" in res
    assert res["divine_alignment"]["engine"] == "iman"
