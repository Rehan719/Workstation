import pytest
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme
from agentic_core.validation.enforcement_pattern import ValidationResult

class MockValidator:
    def __init__(self, passed=True):
        self.passed = passed
    def validate(self, target, context):
        return ValidationResult(passed=self.passed)

def test_supreme_enforcement_phases():
    config = {"fail_on_missing_validator": False}
    pattern = OmniEnforcementPatternSupreme(config, {})

    # Register a failing validator for Phase 1
    pattern.register_validator("zero_placeholder", MockValidator(passed=False))

    result = pattern.validate("some_target")
    assert not result.passed
    assert result.violation == "zero_placeholder"

def test_supreme_enforcement_all_pass():
    config = {"fail_on_missing_validator": False}
    pattern = OmniEnforcementPatternSupreme(config, {})

    # Register passing validators for some
    pattern.register_validator("zero_placeholder", MockValidator(passed=True))
    pattern.register_validator("lob_fixpoint", MockValidator(passed=True))

    result = pattern.validate("some_target")
    assert result.passed

def test_supreme_enforcement_phase_ordering():
    config = {"fail_on_missing_validator": False}
    pattern = OmniEnforcementPatternSupreme(config, {})

    # Phase 5 fails
    pattern.register_validator("lob_fixpoint", MockValidator(passed=False))
    # Phase 1 passes
    pattern.register_validator("zero_placeholder", MockValidator(passed=True))

    result = pattern.validate("some_target")
    assert not result.passed
    assert result.violation == "lob_fixpoint"
