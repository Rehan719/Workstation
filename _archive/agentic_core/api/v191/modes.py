from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/modes", tags=["Mission Modes"])

MODES = {
    "strategic": {
        "name": "Strategic",
        "description": "Executive oversight and treasury monitoring.",
        "nav": ["dashboard", "ceo", "introspection", "evolution", "settings"],
        "primary_agent": "VSB AI CEO"
    },
    "research": {
        "name": "Research",
        "description": "Deep extrospection and scholarly synthesis.",
        "nav": ["extrospection", "coe", "evolution"],
        "primary_agent": "Scholar Meta-Analyzer"
    },
    "operational": {
        "name": "Operational",
        "description": "System health and QEP engine orchestration.",
        "nav": ["dashboard", "qep", "introspection", "bto"],
        "primary_agent": "COO Agent"
    }
}

@router.get("/")
async def get_modes():
    return MODES

@router.get("/{mode_id}")
async def get_mode_config(mode_id: str):
    return MODES.get(mode_id, MODES["strategic"])
