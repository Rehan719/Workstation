import pytest
import asyncio
from workstation_v17.core.gaas_validator_v4 import GaaSValidatorV4

@pytest.fixture
def validator():
    return GaaSValidatorV4(
        "workstation_v17/config/constitutional_genome_v17.yaml",
        "workstation_v17/config/legal_precision.yaml"
    )

@pytest.mark.asyncio
async def test_legal_blocking(validator):
    # Action with a known violation
    action = {
        "type": "dismissal",
        "category": "Employment",
        "potential_violations": ["EMP-001"] # Direct discrimination
    }
    result = await validator.validate_action(action, {})
    # It should be blocked because EMP-001 has enforcement_action: block
    assert result["passed"] is False
    assert result["legal_audit"]["blocked"] is True

@pytest.mark.asyncio
async def test_constitutional_alignment(validator):
    action = {"type": "neutral_analysis", "category": "General"}
    result = await validator.validate_action(action, {})
    assert result["passed"] is True
    assert result["confidence_score"] >= 0.85
