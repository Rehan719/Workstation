import logging
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from src.organism.python.ai_gateway import gateway
from .neural_bridge import verify_token

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/v1/ai/completion", dependencies=[Depends(verify_token)])
async def ai_completion(request: Dict[str, Any]):
    """
    Exposes the Sovereign AI Gateway to the UI.
    Requires Bearer token authentication.
    """
    provider = request.get("provider", "deepseek")
    messages = request.get("messages")
    parameters = request.get("parameters", {})

    if not messages:
        raise HTTPException(status_code=400, detail="Messages list is required.")

    try:
        result = await gateway.execute_completion(provider, messages, **parameters)
        return {
            "status": "SUCCESS",
            "data": result
        }
    except Exception as e:
        logger.error(f"AI Bridge Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/ai/quotas", dependencies=[Depends(verify_token)])
async def get_ai_quotas():
    """Returns AI quota usage for the dashboard."""
    # This would call TokenBudgetManager
    return [
        {"model": "deepseek", "used": 1200, "limit": 5000000, "remaining": 4998800, "health": "healthy"},
        {"model": "qwen", "used": 450, "limit": 1000000, "remaining": 999550, "health": "healthy"},
        {"model": "minimax", "used": 89, "limit": 500000, "remaining": 499911, "health": "healthy"}
    ]
