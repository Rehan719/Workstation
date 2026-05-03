import pytest
from agentic_core.gaas.adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from core.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
import torch

@pytest.fixture
def gaas_adapter():
    base = GaaSValidatorV4("configs/constitutional_genome_v138.yaml", "configs/legal_precision.yaml")
    legal = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    return EntropyRegularisedGaaS(base, legal)

@pytest.mark.asyncio
async def test_gaas_entropy_regularisation(gaas_adapter):
    # Intent with low transport cost (high similarity to uniform constitution)
    intent_ok = {
        "type": "doc_gen",
        "confidence": 0.95,
        "profile": [0.1]*10 # Matches uniform baseline
    }
    context = {"layer": "L9_Orchestration", "domain": "general", "entropy_threshold": 0.5}

    res = await gaas_adapter.validate_intent(intent_ok, context)
    assert res["passed"]
    assert res["transport_cost"] < 0.1

@pytest.mark.asyncio
async def test_gaas_entropy_breach_suggestion(gaas_adapter):
    # Intent with high transport cost (divergent from uniform constitution)
    intent_bad = {
        "type": "doc_gen",
        "confidence": 0.95,
        "profile": [0.9]*10 # Divergent
    }
    # Tight threshold
    context = {"layer": "L9_Orchestration", "domain": "general", "entropy_threshold": 0.05}

    res = await gaas_adapter.validate_intent(intent_bad, context)

    # In Phase 1, we flag but don't necessarily block general intents unless cost > 2*threshold
    # But here cost (0.9-0.1)^2 * 10 = 0.64 * 10 = 6.4 which is > 2*0.05
    assert not res["passed"]
    assert res["reason"] == "ENTROPY_THRESHOLD_EXCEEDED"
    assert "suggested_profile" in res
