import pytest
import asyncio
from agentic_core.external.gateway import ExternalResourceGateway
from agentic_core.self_improvement.twin_analyst import TwinAnalyst
from agentic_core.qep.sub_reactor import QEPSubReactor
from agentic_core.qep.agents import QuranicScholar

@pytest.mark.asyncio
async def test_external_gateway_assimilation():
    gateway = ExternalResourceGateway()
    response = await gateway.call_platform("huggingface", "tafsir", {"verse": "1:1"})
    assert response["status"] == "success"
    await gateway.close()

def test_twin_driven_optimization():
    analyst = TwinAnalyst()
    improvement = analyst.simulate_optimization("aro_engine", {"new_window": 250})
    assert improvement > 0

@pytest.mark.asyncio
async def test_converged_qep_reactor():
    reactor = QEPSubReactor()
    scholar = QuranicScholar()
    reactor.add_agent(scholar)
    result = await reactor.execute_scholarly_workflow("2:255")
    assert "tafsir" in result
    assert result["confidence"] >= 0.99
