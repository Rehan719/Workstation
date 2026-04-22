import pytest
import asyncio
from agentic_core.gaas.v5.uci_v16_omega import UnifiedConstitutionalInterceptorV16Omega

@pytest.mark.asyncio
async def test_uci_v16_full_cycle():
    uci = UnifiedConstitutionalInterceptorV16Omega("omega_node_01")

    async def valid_action():
        return "The Equality Act 2010 provides protection from discrimination."

    context = {
        "jurisdiction": "uk_employment",
        # Must contain: "Equality Act 2010", "ERA 1996", "ACAS Code"
        "payload": "Equality Act 2010, ERA 1996, and ACAS Code are all respected.",
        "ethical_framework": "islamic_khayr",
        "intent": "Help with employment law"
    }

    res = await uci.intercept(context, valid_action)
    assert res["status"] == "success"
    assert "Equ" in res["result"]

@pytest.mark.asyncio
async def test_uci_v16_hallucination_repair():
    uci = UnifiedConstitutionalInterceptorV16Omega("omega_node_01")

    async def flawed_action():
        return "Unsupported claims."

    # Mocking hallucination validation to fail
    from unittest.mock import AsyncMock
    uci.hallucination.validate_output = AsyncMock(return_value={"passed": False})

    context = {"intent": "Informational research"}
    res = await uci.intercept(context, flawed_action)
    assert "[Verified" in res["result"]
