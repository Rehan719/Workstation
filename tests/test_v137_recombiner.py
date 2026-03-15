import pytest
from agentic_core.synthesis.recombiner_v137 import CapabilityRecombinerV137

def test_v137_recombination_analysis():
    recombiner = CapabilityRecombinerV137()
    market_data = {"microsoft": "Aggressive_AI", "google": "Stable"}
    proposals = recombiner.analyze_m7_trajectories(market_data)

    # One for Microsoft (Aggressive_AI) + One for global free_tier_stacking
    assert len(proposals) >= 2
    ids = [p["proposal_id"] for p in proposals]
    assert "REC_CAPABILITY_FUSION_MICROSOFT" in ids
    assert "REC_FREE_TIER_STACKING_ALL" in ids

def test_v137_simulation():
    recombiner = CapabilityRecombinerV137()
    proposal = {
        "proposal_id": "REC_TEST",
        "pattern": "gap_filling"
    }
    result = recombiner.simulate_recombination(proposal)
    assert result["simulation_result"] == "SUCCESS"
    assert result["predicted_roi"] == 0.74
