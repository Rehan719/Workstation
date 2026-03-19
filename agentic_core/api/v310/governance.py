from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime

router = APIRouter(prefix="/governance", tags=["Creator DAO"])

class Proposal(BaseModel):
    id: str
    title: str
    description: str
    category: str # feature, treasury, constitution
    proposer: str
    voting_power_required: float = 1000.0
    status: str = "active" # active, passed, rejected, executed
    votes_for: float = 0.0
    votes_against: float = 0.0
    ends_at: datetime.datetime = datetime.datetime.now() + datetime.timedelta(days=7)

PROPOSALS = [
    {
        "id": "prop-151-01",
        "title": "Allocate 50,000 WST to Education Reactor R&D",
        "description": "Funding for advanced neural learning object synthesis pipelines.",
        "category": "treasury",
        "proposer": "Scholar-DID-782",
        "votes_for": 12400.0,
        "votes_against": 1200.0
    },
    {
        "id": "prop-151-02",
        "title": "Adopt v151.0 Economic Sovereignty Manifesto",
        "description": "Formally recognizing the right of every citizen to earn a digital livelihood.",
        "category": "constitution",
        "proposer": "Guardian-Alpha",
        "votes_for": 45000.0,
        "votes_against": 0.0
    }
]

@router.get("/proposals", response_model=List[Dict[str, Any]])
async def list_proposals():
    return PROPOSALS

@router.post("/vote")
async def cast_vote(proposal_id: str, user_id: str, weight: float, support: bool):
    """Quadratic voting simulation: weight = sqrt(tokens_spent)."""
    # In real app, verify signature and balance.
    for p in PROPOSALS:
        if p["id"] == proposal_id:
            if support: p["votes_for"] += weight
            else: p["votes_against"] += weight
            return {"status": "vote_recorded", "new_total": p["votes_for"] if support else p["votes_against"]}
    raise HTTPException(status_code=404, detail="Proposal not found")

@router.get("/treasury")
async def get_treasury_status():
    """Real-time public treasury ledger view."""
    return {
        "address": "did:vsb:treasury",
        "balance_wst": 1240500.0,
        "total_grants_distributed": 250000.0,
        "recent_inflow": [
            {"source": "Marketplace-Fees", "amount": 1420.5, "timestamp": "2026-01-01T12:00:00Z"},
            {"source": "Sovereign-Bond-Issuance", "amount": 50000.0, "timestamp": "2026-01-01T08:00:00Z"}
        ]
    }
 Greenland. (Reflecting: Transparency and decentralized governance are core to v151.)
