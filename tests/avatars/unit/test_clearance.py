import pytest
from agentic_core.avatars.core.clearance_chain import ConstitutionalClearanceChain
from agentic_core.avatars.cognition.mushawara_bridge import AvatarCognitiveOrchestrator
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme
from agentic_core.cognitive.bootstrap import bootstrap_engines

class MockUEG:
    async def log_event(self, event_type, data, actor="SYSTEM"):
        return "mock_hash"
    async def log_minimisation_event(self, event_type, data, context=None):
        return "mock_hash"

@pytest.mark.asyncio
async def test_clearance_chain_success():
    ueg = MockUEG()
    bootstrap_engines(ueg)
    enforcement = OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {"task": "test"})
    orchestrator = AvatarCognitiveOrchestrator(ueg, enforcement)
    chain = ConstitutionalClearanceChain(ueg, orchestrator)

    emission = {"id": "emit_1", "text": "Helpful instruction for building a database."}
    context = {"user_id": "user_1"}

    result = await chain.validate_emission(emission, context)
    assert result.passed is True
    assert "tahqeeq" in result.attestations

@pytest.mark.asyncio
async def test_clearance_chain_failure_placeholder():
    ueg = MockUEG()
    bootstrap_engines(ueg)
    enforcement = OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {"task": "test"})
    orchestrator = AvatarCognitiveOrchestrator(ueg, enforcement)
    chain = ConstitutionalClearanceChain(ueg, orchestrator)

    emission = {"id": "emit_2", "text": "Instruction with TODO placeholder."}
    context = {"user_id": "user_1"}

    result = await chain.validate_emission(emission, context)
    assert result.passed is False
    assert "Zero-placeholder 'TODO' detected" in result.reason
