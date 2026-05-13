import pytest
from agentic_core.consultation.mushawara.mushawara_bridge_2 import MushawaraBridge2, ConsultationQuery
from agentic_core.cognitive.bootstrap import bootstrap_engines
from agentic_core.cognitive.registry import EngineType
@pytest.mark.asyncio
async def test_mushawara():
    reg = bootstrap_engines()
    bridge = MushawaraBridge2(None, reg)
    res = await bridge.deliberate(ConsultationQuery("q1", "test?", "d", {"u": "o"}), [EngineType.AQAL, EngineType.IMAN, EngineType.TAWAZUN])
    assert res["status"] == "APPROVED"
