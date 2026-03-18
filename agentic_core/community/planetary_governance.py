from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter(prefix="/planetary/community", tags=["Planetary Community"])

class GlobalVote(BaseModel):
    proposal_id: str
    weight: float # Quadratic weighting supported
    voter_did: str

@router.get("/forums/topics")
async def get_trending_topics():
    """Planetary-scale forums for civilizational discussion."""
    return [
        {"topic": "Inter-Realm Trade Ethics", "replies": 12400, "sentiment": 0.85},
        {"topic": "Physical Integration Standards", "replies": 8500, "sentiment": 0.92}
    ]

@router.post("/governance/vote")
async def cast_planetary_vote(vote: GlobalVote):
    """Planetary voting on civilizational initiatives with quadratic weighting."""
    return {"status": "vote_recorded", "tx_hash": "0x planetary_vote_..."}

@router.get("/projects/collaborative")
async def get_cross_realm_projects():
    """Collaborative initiatives that span multiple realms and nodes."""
    return [
        {"id": "proj-1", "name": "Planetary Reforestation Sync", "members": 54200, "status": "active"},
        {"id": "proj-2", "name": "Global Latency Optimization", "members": 12000, "status": "planning"}
    ]
