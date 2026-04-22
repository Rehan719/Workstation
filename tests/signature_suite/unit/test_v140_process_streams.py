import pytest
import asyncio
from agentic_core.enterprise.engine import CoreProcessEngineV140

@pytest.mark.asyncio
async def test_v140_business_stream():
    engine = CoreProcessEngineV140("business", "node_b1")
    context = {"jurisdiction": "uk_employment", "payload": "Equality Act 2010, ERA 1996, ACAS Code included"}
    res = await engine.execute_process("Risk Assessment", "Optimise supply chain", context)
    assert res["status"] == "success"
    assert "business" in str(res["result"])
