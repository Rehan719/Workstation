import pytest
import asyncio
import torch
from agentic_core.collective.swarm.hypothesis_generator import SwarmHypothesisGenerator
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.collective.consensus.truth_consensus import TruthConsensusEngine

@pytest.mark.asyncio
async def test_hypothesis_generation():
    sb = SchrödingerBridgeEngine()
    gen = SwarmHypothesisGenerator(sb)
    hypotheses = await gen.generate_hypotheses("Test Question", num_hypotheses=5)

    assert len(hypotheses) == 5
    assert hypotheses[0]["testability_score"] > 0.8
    assert hypotheses[0]["novelty_score"] > 0.7

@pytest.mark.asyncio
async def test_truth_consensus():
    engine = TruthConsensusEngine()
    claims = [
        {"claim": "Fact A", "confidence": 0.9, "reputation": 1.0},
        {"claim": "Fact A", "confidence": 0.8, "reputation": 0.5},
        {"claim": "Fact B", "confidence": 0.5, "reputation": 1.0}
    ]
    results = await engine.reach_consensus(claims)

    # Fact A should be accepted (weighted conf > 0.85)
    fact_a = next(r for r in results if r["claim"] == "Fact A")
    assert fact_a["accepted"] is True

    # Fact B should be rejected
    fact_b = next(r for r in results if r["claim"] == "Fact B")
    assert fact_b["accepted"] is False
