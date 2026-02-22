import pytest
import asyncio
from agentic_core.evidence.unified_evidence_graph import UnifiedEvidenceGraph
from agentic_core.causal.causal_reasoner import CausalReasoner
from agentic_core.verification.chain_of_verification import ChainOfVerification
from agentic_core.confidence.confidence_calibration_engine import ConfidenceCalibrationEngine
from agentic_core.scholarship.multi_agent.literature_retrieval_agent import LiteratureRetrievalAgent
from agentic_core.collaboration.workspace_orchestrator import WorkspaceOrchestrator

@pytest.mark.asyncio
async def test_v45_ueg_causal_support():
    ueg = UnifiedEvidenceGraph()
    ueg.add_causal_link("treatment", "outcome", "direct", 0.95)
    assert float(ueg.version) >= 45.0
    # Check if link exists in graph
    edges = list(ueg.graph.edges(data=True))
    assert any(d['relation'] == "CAUSALLY_INFLUENCES" for u, v, d in edges)

@pytest.mark.asyncio
async def test_v45_cove_protocol():
    ueg = UnifiedEvidenceGraph()
    cove = ChainOfVerification(ueg)
    claim = "X causes Y"
    sources = [{"id": "S1", "text": "X leads to Y"}]
    report = await cove.verify_claim(claim, sources)
    assert report["status"] in ["verified", "partially_verified"]
    assert "verification_results" in report

@pytest.mark.asyncio
async def test_v45_causal_hypothesis_generation():
    ueg = UnifiedEvidenceGraph()
    reasoner = CausalReasoner(ueg)
    hypotheses = await reasoner.generate_hypotheses(["Does A cause B?"])
    assert len(hypotheses) > 0
    assert hypotheses[0]["type"] == "provisional_hypothesis"

@pytest.mark.asyncio
async def test_v45_confidence_calibration():
    engine = ConfidenceCalibrationEngine(alpha=0.05)
    calib = await engine.calibrate_hypothesis({"id": "H1", "question": "Q1"}, ["node1"])
    assert calib["confidence_score"] == 0.85
    assert "conformal_interval" in calib
    assert "epistemic" in calib["uncertainty_decomposition"]

@pytest.mark.asyncio
async def test_v45_scholarship_retrieval():
    agent = LiteratureRetrievalAgent()
    papers = await agent.retrieve_and_screen("quantum AI", {})
    assert len(papers) > 0
    assert papers[0]["relevance"] >= 0.8

@pytest.mark.asyncio
async def test_v45_collaborative_orchestration():
    ueg = UnifiedEvidenceGraph()
    orchestrator = WorkspaceOrchestrator(ueg)
    session = await orchestrator.initialize_collaborative_session("proj1", ["user1", "user2"])
    assert session["session_id"] == "S1"
    assert session["status"] == "active"
