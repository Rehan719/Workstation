import pytest
from agentic_core.synthesis.recombiner_v137 import CapabilityRecombinerV137

def test_v137_recombination_logic():
    recombiner = CapabilityRecombinerV137()
    predictions = [{"platform": "microsoft", "trend": "AI_Studio"}]
    gaps = ["multi_hop_rag"]

    proposals = recombiner.recombine(predictions, gaps)

    assert len(proposals) > 0
    assert proposals[0]["v137_certified"] == True
    assert "REC_" in proposals[0]["proposal_id"]
