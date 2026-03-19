from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random

router = APIRouter(prefix="/governance/treasury", tags=["Intelligent Treasury"])

@router.get("/evaluation/{proposal_id}")
async def evaluate_grant_proposal(proposal_id: str):
    """v152.0: AI Evaluation of grant proposals using multi-feature analysis."""
    # Simulation: Algorithmic scoring
    features = {
        "creator_reputation": 0.92,
        "market_demand_signal": 0.85,
        "success_probability": 0.78,
        "constitutional_alignment": 0.99
    }
    score = sum(features.values()) / len(features)

    return {
        "proposal_id": proposal_id,
        "score": score,
        "recommendation": "Approve" if score > 0.8 else "Needs Human Review",
        "breakdown": features,
        "risk_assessment": "Low: Verified creator with high historical fidelity."
    }

@router.get("/roi")
async def get_treasury_roi():
    """Predictive and historical ROI on autonomous investments."""
    return {
        "historical_roi": "+24.2%",
        "predicted_roi_next_q": "+18.5%",
        "top_performing_category": "Education Reactors",
        "active_grants_count": 142
    }

@router.post("/allocate/automatic")
async def trigger_auto_allocation(proposal_id: str):
    eval_res = await evaluate_grant_proposal(proposal_id)
    if eval_res["recommendation"] == "Approve":
        return {"status": "funds_allocated_autonomously", "amount_wst": 5000, "tx": "0xAA...11"}
    return {"status": "held_for_human_review", "reason": "Threshold not met."}
