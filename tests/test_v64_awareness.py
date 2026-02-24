import asyncio
import logging
from agentic_core.psychology.self_awareness import SelfAwarenessModule
from agentic_core.psychology.user_model import UserModelEngine
from agentic_core.reflex.reflex_arc import ReflexArc
from agentic_core.reflex.priority_encoder import PriorityEncoder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_v64_awareness_flow():
    self_aware = SelfAwarenessModule()
    user_model = UserModelEngine()
    encoder = PriorityEncoder()
    reflex = ReflexArc()

    logger.info("Starting v64 Symbiotic Awareness Test...")

    # 1. User Interaction & Modeling
    user_id = "user_719"
    behavior = {"correction_rate": 0.3} # Novice/Struggling
    profile = user_model.update_user_profile(user_id, behavior)
    assert profile["expertise"] < 0.5

    # 2. Self-Modeling
    metrics = {"allostatic_load": 5.0, "success_rate": 0.95}
    state = self_aware.update_state(metrics)
    assert state["emotional_valence"] > 0.8

    # 3. Stimulus Processing & Reflex
    stimulus = {"type": "security_violation", "threat_score": 0.9}
    priority = encoder.encode_priority(stimulus)
    assert priority == "reflex"

    if priority == "reflex":
        res = reflex.trigger_reflex(stimulus)
        assert res["status"] == "reflex_executed"
        assert res["target_met"] is True

    print("v64 Symbiotic Awareness Flow verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_v64_awareness_flow())
