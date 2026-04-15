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
    intent = {
        "type": "intent_test",
        "potential_flags": ["EMP-001"], # Direct discrimination
        "confidence": 0.99
    }
    result = await validator.validate_intent(intent, {})
    assert result["passed"] is False
    assert result["blocked"] is True

@pytest.mark.asyncio
async def test_constitutional_alignment(validator):
    intent = {"type": "neutral_analysis", "confidence": 0.96}
    result = await validator.validate_intent(intent, {})
    assert result["passed"] is True
