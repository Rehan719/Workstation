import pytest
import asyncio
from agentic_core.cognitive.v2.meta_cognition_v2 import MetaCognitionEngineV2

@pytest.mark.asyncio
async def test_meta_v2_telemetry_introspection():
    meta = MetaCognitionEngineV2("opus_node")
    # Feed telemetry for L1 (Identity) and L5 (Resilience)
    meta.update_telemetry("L1", 10.5, 0.02)
    meta.update_telemetry("L5", 55.0, 0.08)

    insight = await meta.introspect({"confidence": 0.99})
    assert insight["core_health"] > 0
    assert insight["confidence"] == 0.99
    assert meta.cycle_latencies["micro"] < 80
