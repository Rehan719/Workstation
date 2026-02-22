import pytest
import asyncio
import torch
from agentic_core.orchestrator import Orchestrator
from agentic_core.evidence.unified_evidence_graph import UnifiedEvidenceGraph
from agentic_core.uncertainty.bayesian_engine import BayesianEngine
from agentic_core.workflow.composer import WorkflowComposer

@pytest.mark.asyncio
async def test_v47_orchestration_improved():
    orchestrator = Orchestrator()
    task = {
        "goal": "Test Goal",
        "discover_hypotheses": True,
        "uncertainty_quantification": True,
        "anchor_to_blockchain": True
    }
    result = await orchestrator.execute(task)
    assert result["status"] == "completed"
    assert "blockchain_receipt" in result

def test_bayesian_engine_improved():
    engine = BayesianEngine()
    x = torch.randn(10, 1)
    uncertainty = engine.quantify_uncertainty(x)
    assert "epistemic_std" in uncertainty
    confidence = engine.apply_conformal_calibration(uncertainty["predictive_variance"])
    assert 0 <= confidence <= 1.0

def test_workflow_composer_improved():
    composer = WorkflowComposer()
    nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
    edges = [{"from": "A", "to": "B"}, {"from": "B", "to": "C"}]
    result = composer.compose_workflow(nodes, edges)
    assert result["validation"] == "PASSED"
    assert len(result["parallel_execution_plan"]) == 3 # Serial path
