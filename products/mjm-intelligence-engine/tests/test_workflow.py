import pytest
import os
import shutil
from core.workflow_orchestrator import MJMWorkflowOrchestrator
from core.models import MJMPhase

@pytest.fixture
def orchestrator():
    config = {
        "checkpoints_dir": "test_checkpoints"
    }
    yield MJMWorkflowOrchestrator(config)
    if os.path.exists("test_checkpoints"):
        shutil.rmtree("test_checkpoints")

def test_workflow_end_to_end(orchestrator):
    # 1. Mushahida
    m_id = orchestrator.run_mushahida(["test query"], "user1")
    assert m_id.startswith("CHK-MUS-")

    # 2. Jaiza
    j_id = orchestrator.run_jaiza(m_id, "user1")
    assert j_id.startswith("CHK-JAI-")

    # 3. Muaina
    mu_id = orchestrator.run_muaina(j_id, "opt-1", "user1")
    assert mu_id.startswith("CHK-MUA-")

    # Verify state
    state = orchestrator._load_checkpoint(mu_id)
    assert state.phase == MJMPhase.MUAINA
    assert "proposal_package" in state.data
