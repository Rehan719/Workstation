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

# W408 — two invented proposals used to be seeded here, complete with vote tallies
#   "Allocate 50,000 WST to Education Reactor R&D"      12,400 for / 1,200 against
#   "Adopt v151.0 Economic Sovereignty Manifesto"        45,000 for / 0 against
# proposed by "Scholar-DID-782" and "Guardian-Alpha". Nobody proposed them and no vote was ever
# cast: the tallies were literals. Worse, /vote adds REAL votes on top of that baseline, so every
# genuine vote would have been reported inside a fabricated total — the fabrication would have
# laundered itself through real participation.
#
# The list starts empty. A governance surface with no proposals is a true statement about a system
# nobody has proposed anything in.
PROPOSALS: List[Dict[str, Any]] = []

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
    """The real capital fund, reported as what it is.

    W408 - this was documented as a "Real-time public treasury ledger view" and returned
    balance_wst 1,240,500, total_grants_distributed 250,000 and two "recent_inflow" records with
    timestamps and named sources ("Marketplace-Fees", "Sovereign-Bond-Issuance"). Every value was a
    literal; nothing read any store. The timestamps are what made the inflows read as records of
    things that happened.

    There is a real pool - the capital fund - so it is reported, labelled as the capital fund rather
    than as a separate treasury, and in virtual WST. No inflow history is claimed, because none is
    recorded anywhere.
    """
    try:
        from agentic_core.api.capital_fund import _load_fund
        fund = _load_fund() or {}
    except Exception as exc:
        return {"source": "capital_fund", "available_wst": None,
                "detail": "The capital fund could not be read: " + str(exc)[:160]}
    return {
        "source": "capital_fund",
        "currency": "WST (virtual)",
        "total_capital_wst": fund.get("total_capital"),
        "allocated_wst": fund.get("allocated"),
        "available_wst": fund.get("available"),
        "allocation_count": len(fund.get("allocations") or []),
        "note": ("These are the capital fund's real figures. No separate treasury ledger and no "
                 "inflow history exist, so none are reported."),
    }
