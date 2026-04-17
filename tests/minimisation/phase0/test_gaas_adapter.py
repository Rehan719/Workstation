import pytest
import asyncio
from agentic_core.gaas.adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from agentic_core.organism.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
import yaml
import os

@pytest.fixture
def mock_configs(tmp_path):
    genome = tmp_path / "genome.yaml"
    genome.write_text(yaml.dump({
        "gaas_v4_config": {"min_confidence_score": 0.9}
    }))

    legal = tmp_path / "legal.yaml"
    legal.write_text(yaml.dump({
        "rules": [],
        "statutes": {}
    }))

    return str(genome), str(legal)

@pytest.mark.asyncio
async def test_entropy_regularised_gaas_legal_gate(mock_configs):
    genome_path, legal_path = mock_configs
    base_validator = GaaSValidatorV4(genome_path, legal_path)
    legal_engine = UKLegalPrecisionEngineImpl(legal_path)

    adapter = EntropyRegularisedGaaS(base_validator, legal_engine)

    # 1. Non-legal domain should pass base validation
    intent_non_legal = {"type": "general", "confidence": 0.95}
    context_non_legal = {"layer": "L7_Library", "domain": "general"}

    res1 = await adapter.validate_intent(intent_non_legal, context_non_legal)
    assert res1["passed"]

    # 2. Legal domain with jurisdiction mismatch should fail
    intent_legal = {
        "type": "legal_doc",
        "confidence": 0.95,
        "jurisdiction": "England_Wales"
    }
    context_legal = {
        "layer": "L12_Policy",
        "domain": "legal",
        "required_statutes": ["EqualityAct2010"],
        "jurisdiction": "Scotland" # Mismatch
    }

    res2 = await adapter.validate_intent(intent_legal, context_legal)
    assert not res2["passed"]
    assert res2["reason"] == "LEGAL_PRECISION_VIOLATION"

    # 3. High entropy should be logged (Article 1104)
    intent_high_entropy = {"type": "general", "confidence": 0.95, "entropy": 0.9}
    context_high_entropy = {"layer": "L7_Library", "domain": "general", "entropy_threshold": 0.5}
    res3 = await adapter.validate_intent(intent_high_entropy, context_high_entropy)
    assert res3["passed"]
    assert res3["entropy"] == 0.9
