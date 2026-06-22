"""
Collective Intelligence API — surfaces Workstation's OWN truth-consensus engine
(`agentic_core.collective.consensus.TruthConsensusEngine`) into the live pipeline. Previously
orphaned; now reachable + a first-class Resource-Fabric resource. Real, honest logic: reputation-
weighted confidence aggregation over the SUBMITTED claims (no fabricated data) — accepts a claim
when the weighted consensus confidence clears the threshold. Useful for cross-swarm / cross-VSB
agreement on ground truth.

  POST /api/v1/collective/consensus — reputation-weighted truth consensus over a set of claims
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/collective", tags=["collective-intelligence"])


class Claim(BaseModel):
    claim: str
    confidence: float = 0.8     # 0..1 — the observer's confidence in the claim
    reputation: float = 1.0     # the observer's reputation weight


class ConsensusRequest(BaseModel):
    claims: List[Claim]
    threshold: float = 0.85


@router.post("/consensus")
async def consensus(req: ConsensusRequest):
    """Reputation-weighted truth consensus over the submitted claims (real engine logic — operates
    only on the inputs, fabricates nothing)."""
    from agentic_core.collective.consensus.truth_consensus import TruthConsensusEngine
    engine = TruthConsensusEngine(threshold=req.threshold)
    claims = [{"claim": c.claim, "confidence": c.confidence, "reputation": c.reputation} for c in req.claims]
    results = await engine.reach_truth_consensus(claims)
    return {
        "threshold": req.threshold,
        "claims": len(results),
        "accepted": sum(1 for r in results if r["accepted"]),
        "results": results,
        "method": "reputation-weighted confidence aggregation",
    }
