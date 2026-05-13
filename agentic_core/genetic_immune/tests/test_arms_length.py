import pytest
from agentic_core.genetic_immune.unified_defense import UnifiedDefenseOrchestrator
from agentic_core.genetic_immune.arms_length_audit import ArmsLengthAudit
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_arms_length_veto():
    ueg = VSBUEGLogger()
    orchestrator = UnifiedDefenseOrchestrator(ueg)
    audit = ArmsLengthAudit(orchestrator, ueg)

    # Audit should pass if the subsystem can successfully veto a high-risk forced action
    assert await audit.test_veto_integrity() is True
