import pytest
from agentic_core.avatars.modes.mode_manager import AvatarModeManager, AvatarMode
from agentic_core.avatars.adaptation.skill_profiler import SkillProfiler

class MockUEG:
    async def log_event(self, event_type, data, actor="SYSTEM"):
        return "mock_hash"

@pytest.mark.asyncio
async def test_mode_switching():
    ueg = MockUEG()
    manager = AvatarModeManager(ueg)
    assert manager.current_mode == AvatarMode.INSTRUCTOR

    await manager.switch_mode(AvatarMode.COPILOT, "Testing transition")
    assert manager.current_mode == AvatarMode.COPILOT
    config = manager.get_current_config()
    assert config.tone == "collaborative_partner"

@pytest.mark.asyncio
async def test_skill_profiling():
    ueg = MockUEG()
    profiler = SkillProfiler(ueg)
    user_id = "user_456"

    # Initial level should be beginner
    assert profiler.get_skill_level(user_id, "coding") == "beginner"

    # Update with several successes
    for _ in range(10):
        await profiler.update_skill(user_id, "coding", True)

    level = profiler.get_skill_level(user_id, "coding")
    assert level in ["builder", "mastery"]
