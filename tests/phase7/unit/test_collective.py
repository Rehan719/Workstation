import pytest
import asyncio
import numpy as np
import torch
from agentic_core.collective.swarm.hypothesis_generator import SwarmHypothesisGenerator
from agentic_core.collective.knowledge.hd_synthesizer import HDKnowledgeSynthesizer
from agentic_core.collective.consensus.truth_consensus import TruthConsensusEngine
from agentic_core.collective.meta.cross_swarm_learner import CrossSwarmMetaLearner

@pytest.mark.asyncio
async def test_hypothesis_generation():
    gen = SwarmHypothesisGenerator()
    hs = await gen.generate_hypotheses("How to minimize network latency?")
    assert len(hs) == 3
    assert hs[0]["testability_score"] >= hs[1]["testability_score"]

@pytest.mark.asyncio
async def test_hd_synthesis():
    syn = HDKnowledgeSynthesizer(dimension=1024)
    v1 = np.random.choice([-1, 1], size=1024)
    v2 = np.random.choice([-1, 1], size=1024)

    synthetic = syn.synthesize([v1, v2])
    assert synthetic.shape == (1024,)
    assert np.all(np.isin(synthetic, [-1, 1]))

@pytest.mark.asyncio
async def test_truth_consensus():
    engine = TruthConsensusEngine(threshold=0.8)
    claims = [
        {"claim": "X is True", "confidence": 0.9, "reputation": 1.0},
        {"claim": "X is True", "confidence": 0.1, "reputation": 0.1}, # Low rep outlier
        {"claim": "Y is True", "confidence": 0.5, "reputation": 1.0}
    ]
    res = await engine.reach_truth_consensus(claims)

    # Claim X should pass
    claim_x = next(r for r in res if r["claim"] == "X is True")
    assert claim_x["accepted"] is True

    # Claim Y should fail
    claim_y = next(r for r in res if r["claim"] == "Y is True")
    assert claim_y["accepted"] is False

@pytest.mark.asyncio
async def test_cross_swarm_meta_learning():
    learner = CrossSwarmMetaLearner()
    experiences = [{"swarm": "research", "success": True}, {"swarm": "economic", "success": False}]
    weights = await learner.update_global_strategy(experiences)
    assert weights.shape == (5,)
