import pytest
import asyncio
from agentic_core.governance.command_dispatch import AICommander, AIDispatcher
from agentic_core.religious_domain.finops.sharia_finops import IslamicFinanceAdapter
from agentic_core.religious_domain.governance.middleware import DualMetricMiddleware, TazkiyahEngine
from agentic_core.ai_ceo.marketing_agent import MarketingAgent
from agentic_core.ai_ceo.recruitment_engine import RecruitmentEngine
from agentic_core.governance.verifiable_governance import VGAEngine
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_ai_ceo_strategic_hierarchy():
    commander = AICommander()
    dispatcher = AIDispatcher()

    # 1. Commander defines a strategic objective
    objective = await commander.define_objective("Scale QEP User Base", {"max_cost": 0, "focus": "Global"})
    assert objective["objective_id"].startswith("OBJ_")

    # 2. Dispatcher allocates a task based on objective
    task_id = await dispatcher.dispatch_task(objective, {"agent": "marketing_1"})
    assert task_id.startswith("task_")
    assert dispatcher.active_tasks[task_id]["status"] == "RUNNING"

@pytest.mark.asyncio
async def test_sharia_finops_integration():
    ledger = MagicMock()
    profile = MagicMock()
    # Mock eligibility: Eligible for Zakat
    profile.calculate_zakat_eligibility.return_value = {
        "is_eligible": True,
        "zakat_due": 250.0
    }

    finops = IslamicFinanceAdapter(ledger, profile)

    # Process Zakat
    result = finops.process_zakat("user_786", 10000.0)
    assert result["status"] == "PROCESSED"
    assert result["amount_distributed"] == 250.0

    # Verify ledger was called
    ledger.log_sharia_transaction.assert_called_once()

@pytest.mark.asyncio
async def test_dual_metric_governance():
    middleware = DualMetricMiddleware()

    # Scenario 1: Low Tazkiyah score -> Should constrain
    context_low = {"user_tazkiyah": 10, "dawah_ready": False}
    res_low = middleware.evaluate_operation("user_123", "DAWAH_ACTIVITY", context_low)
    assert res_low["decision"] == "CONSTRAIN"

    # Scenario 2: High Tazkiyah + Dawah Ready -> Should proceed
    context_high = {"user_tazkiyah": 90, "dawah_ready": True}
    res_high = middleware.evaluate_operation("user_123", "DAWAH_ACTIVITY", context_high)
    assert res_high["decision"] == "PROCEED"

@pytest.mark.asyncio
async def test_marketing_and_recruitment():
    marketing = MarketingAgent("SOV_123")
    campaign = await marketing.generate_campaign("religion", "Global Ummah")
    assert campaign["status"] == "DRAFT"
    assert "assets" in campaign

    recruitment = RecruitmentEngine()
    agent_pool = [
        {"id": "agent_marketing_v1", "specialization": "marketing"},
        {"id": "agent_sharia_expert", "specialization": "religion"}
    ]
    # Context matches religion domain
    context = {"domain": "religion", "risk_level": 0.1}
    hired = recruitment.recruit_agents(context, agent_pool)
    assert "agent_sharia_expert" in hired

@pytest.mark.asyncio
async def test_verifiable_governance_sharia():
    vga = VGAEngine()

    # Intent with Riba (interest)
    bad_intent = {"action": "invest", "parameters": {"type": "interest_bearing_bond"}}
    assert vga.validate_action("shariah", bad_intent) is False

    # Intent that is Halal
    good_intent = {"action": "invest", "parameters": {"type": "equity_sharia_compliant"}}
    assert vga.validate_action("shariah", good_intent) is True
