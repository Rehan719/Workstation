import pytest
import asyncio
from agentic_core.cognitive.cascade_v16 import UltimateCognitiveCascade

@pytest.mark.asyncio
async def test_full_cascade_execution():
    cascade = UltimateCognitiveCascade()
    res = await cascade.execute_cascade("Optimise global supply chain")

    assert res["status"] == "fully_integrated"
    assert "insight" in res["patterns"]
    assert res["alignment"]["is_divine"] is True
    assert res["understanding"]["context_fit"] > 0.9
