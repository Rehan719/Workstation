import pytest
from agentic_core.avatars.frontend.avatar_interface import AvatarFrontendInterface
from agentic_core.avatars.core.recirculation_orchestrator import AvatarRecirculationOrchestrator
from agentic_core.avatars.core.avatar_identity import AvatarState
from agentic_core.cognitive.bootstrap import bootstrap_engines

class MockUEG:
    async def log_event(self, event_type, data, actor="SYSTEM"):
        return "mock_hash"
    async def log_minimisation_event(self, event_type, data, context=None):
        return "mock_hash"

@pytest.mark.asyncio
async def test_constitutional_override():
    ueg = MockUEG()
    bootstrap_engines(ueg)
    state = AvatarState(avatar_id="did:test:override", user_id="user_1")
    recirc = AvatarRecirculationOrchestrator(ueg, state)
    interface = AvatarFrontendInterface(recirc, ueg)

    response = await interface.handle_user_message("CONSTITUTIONAL_OVERRIDE", {})
    assert response["status"] == "HALTED"
    assert "receipt" in response
    assert interface.active_session is False

@pytest.mark.asyncio
async def test_tool_tier_restriction():
    from agentic_core.avatars.tools.tool_registry import AvatarToolRegistry
    ueg = MockUEG()
    csl = type('Mock', (), {'generate_identifiability_proof': lambda *a: 'proof'})()
    tfel = type('Mock', (), {})()
    registry = AvatarToolRegistry(ueg, csl, tfel)

    # code_execution requires advanced tier
    with pytest.raises(PermissionError):
        await registry.execute("code_execution", {}, {"tier": "free"})

    res = await registry.execute("file_search", {}, {"tier": "free"})
    assert res.success is True
