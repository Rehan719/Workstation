import pytest
from agentic_core.avatars.core.instructor_loop import LivingInstructorLoop
from agentic_core.avatars.core.avatar_engine import AvatarState
from agentic_core.cognitive.bootstrap import bootstrap_engines

class MockUEG:
    async def log_event(self, event_type, data, actor="SYSTEM"):
        return "mock_hash"
    async def log_minimisation_event(self, event_type, data, context=None):
        return "mock_hash"

@pytest.mark.asyncio
async def test_avatar_recirculation_cycle():
    ueg = MockUEG()
    bootstrap_engines(ueg)

    state = AvatarState(avatar_id="did:test:123", user_id="user_789")
    orchestrator = LivingInstructorLoop(ueg, state)

    user_context = {"domain": "coding", "success": True, "input": "Explain recursion."}
    result = await orchestrator.execute_cycle(user_context)

    assert result["status"] == "SUCCESS"
    assert "tahqeeq" in result["output"]["attestations"]
