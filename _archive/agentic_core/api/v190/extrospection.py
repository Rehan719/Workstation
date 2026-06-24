from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/extrospection", tags=["Cognitive Extrospection"])

@router.get("/signals", response_model=List[Dict[str, Any]])
async def get_signals():
    return [
        {"id": 1, "type": "research", "source": "arXiv", "title": "Large Multi-Agentic Systems in Biomimetic OS", "relevance": 0.98},
        {"id": 2, "type": "market", "source": "Signals-Global", "title": "WST Token Liquidity Surge", "relevance": 0.95},
        {"id": 3, "type": "social", "source": "UEG-Resonance", "title": "Sovereign Digital Life Adoption Trends", "relevance": 0.92}
    ]
