import pytest
import asyncio
from agentic_core.gaas.v5.uci_v2 import UCIv2Omega

@pytest.mark.asyncio
async def test_uci_v2_pipeline():
    uci = UCIv2Omega("opus_v139_1")

    async def valid_action():
        return {"data": "verified"}

    context = {
        "jurisdiction": "uk_employment",
        "payload": "Equality Act 2010, ERA 1996, ACAS Code are included",
        "ethical_framework": "islamic_khayr"
    }

    res = await uci.execute_gated_action("Legal Task", valid_action, context)
    assert res["status"] == "success"
    assert res["node"] == "opus_v139_1"

@pytest.mark.asyncio
async def test_uci_v2_legal_failure():
    uci = UCIv2Omega("opus_v139_1")
    async def dummy(): return {}
    context = {"jurisdiction": "gdpr", "payload": "missing statutes"}

    with pytest.raises(ValueError) as exc:
        await uci.execute_gated_action("Sensitive Task", dummy, context)
    assert "Legal precision check failed" in str(exc.value)
