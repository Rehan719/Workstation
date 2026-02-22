import pytest
import asyncio
from agentic_core.evidence.unified_evidence_graph import UnifiedEvidenceGraph
from agentic_core.hypothesis.prioritizer import HypothesisPrioritizer
from agentic_core.blockchain.ledger import BlockchainLedger
from agentic_core.assistant.personal_assistant import ResearchAssistant

@pytest.mark.asyncio
async def test_ueg_v48_features():
    ueg = UnifiedEvidenceGraph()
    assert ueg.version == "48.0"

    ueg.add_evidence("node1", "node2", "SUPPORT")
    ueg.add_causal_link("node1", "node2", "Mechanism X", 0.85)

    edges = ueg.get_edges()
    # One SUPPORT edge and one CAUSAL edge
    assert len(edges) == 1 # NetworkX graph.add_edge overwrites if same nodes unless MultiDiGraph
    # Actually add_causal_link also calls add_edge on the same nodes

    # Let's use different nodes to be sure
    ueg.add_causal_link("nodeA", "nodeB", "Mechanism Y", 0.9)
    assert ("nodeA", "nodeB") in ueg.get_edges()
    assert ueg.graph.edges["nodeA", "nodeB"]["relation"] == "CAUSALLY_INFLUENCES"

def test_hypothesis_prioritizer():
    prioritizer = HypothesisPrioritizer()
    hypotheses = [
        {"id": "H1", "novelty_score": 0.9, "feasibility_score": 0.4, "relevance_score": 0.5},
        {"id": "H2", "novelty_score": 0.6, "feasibility_score": 0.8, "relevance_score": 0.9}
    ]
    ranked = prioritizer.prioritize(hypotheses)
    assert len(ranked) == 2
    assert ranked[0]["quality_score"] >= ranked[1]["quality_score"]

@pytest.mark.asyncio
async def test_blockchain_v48_extensions():
    ledger = BlockchainLedger()
    receipt = await ledger.anchor_peer_review("MS123", "REV456", "Excellent work.")
    assert receipt["type"] == "peer_review"
    assert "artifact_id" in receipt

    archive_receipt = await ledger.archive_research_data("DS789", "ipfs://some_cid")
    assert archive_receipt["type"] == "data_archive"
    assert archive_receipt["ipfs_cid"] == "ipfs://some_cid"

def test_research_assistant_v48():
    ueg = UnifiedEvidenceGraph()
    ueg.add_evidence("data_point_1", "obs_1", "SUPPORT")

    assistant = ResearchAssistant("user_test")
    recs = assistant.generate_ueg_recommendations(ueg)

    assert len(recs) > 0
    assert "Investigate Causal Root" in recs[0]["title"]
