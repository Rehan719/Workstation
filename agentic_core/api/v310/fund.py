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
    """No grants have been awarded, and this says so.

    W408 - this returned two invented grants: {"id": "g-001", "title": "Bio-Reactor Optimization",
    "recipient": "@NatureBuild", "amount": 5000, "status": "funded"} and a second at 2,500 in
    "voting". An endpoint named grants/active returning a FUNDED grant to a named recipient asserts
    that money was awarded to someone. No grant store is read, no recipient exists, and the sibling
    endpoint on this same router does call a real engine - so a consumer had every reason to read
    this list as equally real.
    """
    return {
        "grants": [],
        "detail": ("No grant register exists on this deployment, so no grants are listed. Two "
                   "invented grants were previously returned here."),
    }
