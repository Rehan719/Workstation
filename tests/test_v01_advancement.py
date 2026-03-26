import pytest
from agentic_core.api.v138.ceo import tool_registry, ChatRequest
from agentic_core.ai_ceo.memory_v01 import memory_v01, meeting_log
from agentic_core.layers.l1_identity.genome_engine import genome_engine
from agentic_core.reactor.domains.weaver import domain_weaver
from agentic_core.reactor.ecosystem.marketplace import marketplace
from agentic_core.layers.l5_resilience.resilience import resilience_manager

@pytest.mark.asyncio
async def test_semantic_memory():
    memory_v01.add_exchange("Hello CEO", "Greetings Guardian")
    res = memory_v01.query("Hello")
    assert len(res) > 0
    assert "Hello CEO" in res[0]

@pytest.mark.asyncio
async def test_meeting_log():
    meeting_log.post_argument("CEvO", "Growth is priority", "APPROVE")
    debate = meeting_log.get_recent_debate()
    assert "CEvO (APPROVE): Growth is priority" in debate

@pytest.mark.asyncio
async def test_evolution_behavioral_params():
    # Simulate a mutation that should trigger rigid mode
    genome_engine.genome["constitution"]["articles"].append({"id": 42, "content": "transparency is rigid"})
    params = genome_engine.get_behavioral_params()
    assert params["temperature"] == 0.4
    assert "Rigid Mode" in params["system_prompt"]

@pytest.mark.asyncio
async def test_domain_weaver():
    res = await domain_weaver.synthesize("justice", ["law", "religion"])
    assert "Synthesis for 'justice'" in res["synthesis"]
    assert "LAW" in res["synthesis"]

@pytest.mark.asyncio
async def test_marketplace_registry():
    bp = {"name": "test-agent", "type": "LLM"}
    agent_id = marketplace.publish_agent(bp, "tester")
    agents = marketplace.list_agents()
    assert any(a["id"] == agent_id for a in agents)

@pytest.mark.asyncio
async def test_predictive_resilience():
    # Simulate failures
    for _ in range(5):
        resilience_manager.handle_failure("test-node", "CHECKSUM_ERROR", {})
    assert resilience_manager.predict_failure("test-node") is True
