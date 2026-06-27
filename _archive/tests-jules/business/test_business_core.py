import pytest
import asyncio
from core.infrastructure.cost_guard import CostGuard, ThrottleLevel
from core.business.living_strategy_system import LivingStrategySystem
from core.business.referral_engine import ReferralEngine

@pytest.mark.asyncio
async def test_cost_guard_throttling():
    cg = CostGuard()
    # Test Green Level
    cg.usage_state["cloud_run_requests"] = 100000
    level = await cg.evaluate_risk()
    assert level == ThrottleLevel.GREEN

    # Test Critical Level (>95%)
    cg.usage_state["cloud_run_requests"] = 1950000
    level = await cg.evaluate_risk()
    assert level == ThrottleLevel.CRITICAL

@pytest.mark.asyncio
async def test_referral_engine_no_self_referral():
    re = ReferralEngine()
    success = await re.register_referral("did:pqc:owner", "did:pqc:owner")
    assert success is False
    assert re.get_workrep_score("did:pqc:owner") == 0.0

@pytest.mark.asyncio
async def test_referral_engine_valid_referral():
    re = ReferralEngine()
    success = await re.register_referral("did:pqc:owner", "did:pqc:user1")
    assert success is True
    assert re.get_workrep_score("did:pqc:owner") == 100.0

@pytest.mark.asyncio
async def test_living_strategy_cycle():
    lss = LivingStrategySystem()
    # Should run without error
    await lss.run_reflection_cycle()
    assert lss.current_plan_version == "1.0.0"
