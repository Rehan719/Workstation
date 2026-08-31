from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/contribute", tags=["User Empowerment"])

FEEDBACK = []

@router.post("/feedback")
async def submit_feedback(data: Dict[str, Any]):
    FEEDBACK.append(data)
    # W413 — every submission came back with "resonance": 0.99 regardless of content. Nothing
    # scores feedback; the number said only that the request had been received.
    return {"status": "ingested", "received": len(FEEDBACK)}

@router.post("/vote")
async def vote_enhancement(proposal_id: str):
    return {"status": "recorded", "proposal": proposal_id}
