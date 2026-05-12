import asyncio
import pytest
from agentic_core.pulse.pulse_clock import PulseClock
from agentic_core.survival.survival_engine import SurvivalEngineV2

@pytest.mark.asyncio
async def test_survival_v2():
    clock = PulseClock()
    engine = SurvivalEngineV2(clock)

    # 1. Test Priority Veto
    action = {"target_subsystem": "immune"}
    # nervous (rank 1) cannot override immune (rank 0)
    res = engine.request_action("nervous", action)
    assert res is False
    assert len(engine.veto_history) == 1
    assert engine.veto_history[0]["reason"] == "Hierarchy Violation"

    # 2. Test Threshold Veto
    safe_action = {"deviation": 0.5}
    assert engine.request_action("immune", safe_action) is True

    dangerous_action = {"deviation": 0.95}
    assert engine.request_action("immune", dangerous_action) is False
    assert engine.veto_history[-1]["reason"].startswith("Threshold Breach")

    print("Survival Engine v2.0 verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_survival_v2())
