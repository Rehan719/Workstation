import pytest
import asyncio
from workstation_v17.core.gaas_validator_v4 import GaaSValidatorV4

@pytest.fixture
def gaas_validator():
    genome = {"constitutional_genome": {"truth_dimensions": ["I", "II"]}}
    return GaaSValidatorV4(genome)

def test_gaas_pii_export(gaas_validator):
    payload = {"text": "exporting PII data"}
    valid, reason = gaas_validator.validate_agent_interaction("Agent", "Target", payload)
    assert not valid
    assert "PII" in reason

@pytest.mark.asyncio
async def test_gaas_neural_verify(gaas_validator):
    score = await gaas_validator.neural_verify("v17.0 validation")
    assert score > 0.9
