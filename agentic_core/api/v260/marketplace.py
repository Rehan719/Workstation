from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])

class DeveloperAnalytics(BaseModel):
    product_id: str
    views: int
    installs: int
    resonance_earned: float
    engagement_score: float

@router.get("/analytics/{developer_id}")
async def get_developer_analytics(developer_id: str):
    # Simulated v146.0 analytics
    return [
        {"product_id": "p-1", "views": 1420, "installs": 85, "resonance_earned": 420.5, "engagement_score": 0.92},
        {"product_id": "p-2", "views": 850, "installs": 12, "resonance_earned": 14.2, "engagement_score": 0.45}
    ]

@router.get("/payouts/{developer_id}")
async def get_payout_history(developer_id: str):
    return [
        {"month": "January 2026", "amount": 1250.0, "status": "paid"},
        {"month": "December 2025", "amount": 980.5, "status": "paid"}
    ]
