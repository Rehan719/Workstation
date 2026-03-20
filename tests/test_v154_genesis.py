import pytest
from agentic_core.layers.l1_genomic.validator import validator_l1
from agentic_core.layers.l5_recombination.merger import model_merger

def test_l1_validation():
    assert validator_l1.validate_action("recombine", {"models": ["m1", "m2"]}) is True
    assert validator_l1.validate_action("allocate_treasury", {}) is False
    assert validator_l1.validate_action("allocate_treasury", {"explanation": "For science"}) is True

def test_l5_merge():
    res = model_merger.ties_merge(["m1", "m2"], [0.5, 0.5])
    assert res["merge_strategy"] == "TIES"
    assert "new_model_id" in res

if __name__ == "__main__":
    pytest.main([__file__])
