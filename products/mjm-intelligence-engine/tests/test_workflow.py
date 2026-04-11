import pytest
import os
import shutil
import asyncio
from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator
from core.models import MJMPhase

@pytest.fixture
def orchestrator():
    config = {
        "checkpoints_dir": "test_checkpoints",
        "genomes_dir": "config/domains"
    }
    yield MJMWorkflowOrchestrator(config)
    if os.path.exists("test_checkpoints"):
        shutil.rmtree("test_checkpoints")

@pytest.mark.asyncio
async def test_workflow_end_to_end(orchestrator):
    # 1. Mushahida
    m_id = await orchestrator.run_mushahida("patient_safety", ["test query"], "user1")
    assert m_id.startswith("CHK-MUS-")

    # 2. Jaiza
    j_id = await orchestrator.run_jaiza(m_id, "user1")
    assert j_id.startswith("CHK-JAI-")

    # 3. Muaina
    mu_id = await orchestrator.run_muaina(j_id, "opt-1", "user1")
    assert mu_id.startswith("CHK-MUA-")

    # Verify state
    state = orchestrator._load_checkpoint(mu_id)
    assert state.phase == MJMPhase.MUAINA
    assert "proposal_package" in state.data
