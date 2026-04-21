import pytest
import numpy as np
from agentic_core.validation.constraint_gates import ConstraintGateFactory
from agentic_core.validation.biomimetic_v2 import BiomimeticValidatorV2
from agentic_core.validation.statistical_rigor_v2 import StatisticalValidatorV2

def test_gate_factory():
    config = {"jurisdiction": "uk", "statutes": ["EqA"], "coverage_threshold": 1.0}
    gate = ConstraintGateFactory.create_gate("legal_precision", config)
    res = gate.validate({})
    assert res["passed"] is True
    assert res["jurisdiction"] == "uk"

def test_biomimetic_v2():
    validator = BiomimeticValidatorV2(threshold=0.92)
    res = validator.validate_fidelity("inkashaf", {})
    assert res["fidelity_score"] >= 0.92
    assert res["passed"] is True

def test_statistical_v2_ci_96():
    validator = StatisticalValidatorV2(alpha=0.04)
    samples = [0.95, 0.96, 0.94, 0.97, 0.95, 0.96]
    res = validator.calculate_metrics(samples, target=0.90)
    assert res["passed"] is True
    assert res["ci_96"][0] < 0.96 < res["ci_96"][1]
