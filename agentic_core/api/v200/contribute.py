from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

router = APIRouter(prefix="/contribute", tags=["User Empowerment"])

FEEDBACK = []

@router.post("/feedback")
async def submit_feedback(data: Dict[str, Any]):
    FEEDBACK.append(data)
    # W413 — every submission came back with "resonance": 0.99 regardless of content. Nothing
    # scores feedback; the number said only that the request had been received.
    return {"status": "ingested", "received": len(FEEDBACK)}

VOTE_REFUSED = ("No enhancement proposal register exists on this deployment, so there is nothing to vote on and "
                "no vote is recorded.")


@router.post("/vote")
async def vote_enhancement(proposal_id: str):
    """W967 (P5.10 clause 4) - this answered "recorded" for any proposal id and kept nothing. Nothing records a
    vote, so it is refused with that sentence."""
    raise HTTPException(status_code=404, detail=f"{VOTE_REFUSED} (Asked: {proposal_id}.)")
