import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from src.organism.python.ai_gateway import gateway

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/v1/ai/completion")
async def ai_completion(request: Dict[str, Any]):
    """
    Exposes the Sovereign AI Gateway to the UI.
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
