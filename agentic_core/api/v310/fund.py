from fastapi import APIRouter
from typing import Dict, Any, List
from agentic_core.evolution.economic_pipeline import economic_engine

router = APIRouter(prefix="/fund", tags=["Creator Fund"])

@router.get("/epoch-synthesis")
async def get_epoch_summary():
    """v151.0 Periodic AI CEO economic report."""
    return economic_engine.generate_epoch_synthesis()

@router.get("/grants/active")
async def list_active_grants():
    return [
        {"id": "g-001", "title": "Bio-Reactor Optimization", "recipient": "@NatureBuild", "amount": 5000, "status": "funded"},
        {"id": "g-002", "title": "Legal Graph Synthesis", "recipient": "@JusticeBot", "amount": 2500, "status": "voting"}
    ]
