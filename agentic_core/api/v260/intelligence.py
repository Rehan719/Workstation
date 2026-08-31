from fastapi import APIRouter
from typing import Dict, Any, List
from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/civilization", tags=["Civilization Intelligence"])

@router.get("/recommendations")
async def get_civilization_recommendations(user_id: str):
    """No personalised recommendations are computed.

    W413 - this took a user_id, ignored it completely, and returned three fixed items with invented
    relevance scores (0.95, 0.88, 0.92) - one of them pointing at "AMD-146", an amendment that does
    not exist. Every user received the same three, and the scores implied a personalisation engine
    that was never consulted.
    """
    return {
        "user_id": user_id,
        "recommendations": [],
        "detail": ("No recommendation engine is wired to this deployment. Three fixed items with "
                   "invented relevance scores were previously returned for every user."),
    }
@router.post("/assistant/query")
async def assistant_query(query: str):
    ai_response = await gateway.query(query)
    return {
        "response": ai_response,
        "confidence": 0.99,
        "actions": ["/fed-portal", "/evolution-dashboard"]
    }
