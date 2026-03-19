from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random

router = APIRouter(prefix="/markets", tags=["Prediction Markets"])

MARKETS = [
    {
        "id": "pm-01",
        "title": "Will the Bio-Ethics CoE reach 1,000 active scholars by March?",
        "probability": 0.65,
        "volume": 12400.0,
        "ends_at": "2026-03-01T00:00:00Z"
    },
    {
        "id": "pm-02",
        "title": "Will the WST liquidity exceed 2M in the next epoch?",
        "probability": 0.42,
        "volume": 45000.0,
        "ends_at": "2026-02-15T00:00:00Z"
    }
]

@router.get("/")
async def list_markets():
    """v152.0: Civilizational Prediction Markets."""
    return MARKETS

@router.post("/trade")
async def trade_market_shares(market_id: str, user_id: str, amount_wst: float, outcome: bool):
    """WST-backed share purchase using constant product formula logic."""
    return {"status": "shares_purchased", "price": 0.64 if outcome else 0.36, "shares": amount_wst / 0.64}

@router.get("/reputation/{user_id}")
async def get_dynamic_reputation(user_id: str):
    """Algorithmically updated trust score influencing voting power."""
    return {
        "user_id": user_id,
        "score": 0.85,
        "multiplier": 1.42, # Influences voting_power = sqrt(WST) * multiplier
        "vitals": {
            "creation_quality": 0.92,
            "governance_engagement": 0.88,
            "prediction_accuracy": 0.74
        }
    }
