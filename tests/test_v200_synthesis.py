import pytest
from agentic_core.layers.l1_genomic.validator import validator_l1
from agentic_core.layers.l5_recombination.merger import recombination_engine

def test_v3_validation():
    assert validator_l1.validate_action("recombine", {"fitness_score": 0.9}) is True
    # Should log warning but return True (based on current implementation)
    assert validator_l1.validate_action("recombine", {}) is True

def test_v3_recombination():
    res = recombination_engine.execute_merging(["llama", "phi"], "TIES")
    assert res["strategy_used"] == "TIES"
    assert "result_hash" in res

if __name__ == "__main__":
    pytest.main([__file__])
