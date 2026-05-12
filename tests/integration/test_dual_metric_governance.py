
import pytest
import asyncio
from agentic_core.religious_domain.governance.middleware import DualMetricMiddleware, TazkiyahEngine
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_dual_metric_governance_clash():
    # Setup
    middleware = DualMetricMiddleware()

    # Scenario: A business initiative (PAID_COURSE_RUSHED)
    # This initiative is VIABLE (High growth/retention) but causes LOW Tazkiyah

    user_id = "user_123"
    action_type = "PAID_COURSE_RUSHED"

    # Mock context where user's current Tazkiyah is low,
    # and the action doesn't help it (or we simulate the policy check)
    context = {
        "user_tazkiyah": 45.0, # Below the min threshold of 75.0
        "expected_roi": 5000.0,
        "dawah_ready": False
    }

    print(f"\n1. Evaluating operation: {action_type} for user with Tazkiyah {context['user_tazkiyah']}")
    result = middleware.evaluate_operation(user_id, action_type, context)

    print(f"   Spiritual Compliance: {result['spiritual_compliance']}")
    print(f"   Business Viability: {result['business_viability']}")
    print(f"   Decision: {result['decision']}")
    print(f"   Reasoning: {result['reasoning']}")

    # Assertions: Should be CONSTRAIN because spiritual < 75.0
    assert result["decision"] == "CONSTRAIN"
    assert result["spiritual_compliance"] == "CONSTRAINED"
    assert result["business_viability"] == "VIABLE"

    # Scenario 2: Compliant user
    context_compliant = {
        "user_tazkiyah": 80.0,
        "expected_roi": 1000.0,
        "dawah_ready": True
    }
    print(f"\n2. Evaluating operation: DAWAH_ACTIVITY for user with Tazkiyah {context_compliant['user_tazkiyah']}")
    result_compliant = middleware.evaluate_operation(user_id, "DAWAH_ACTIVITY", context_compliant)

    print(f"   Decision: {result_compliant['decision']}")
    assert result_compliant["decision"] == "PROCEED"

if __name__ == "__main__":
    asyncio.run(test_dual_metric_governance_clash())
