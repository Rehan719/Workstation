from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter(prefix="/federation", tags=["Federated Symbiosis"])

TWINS = [
    {"id": "twin-001", "node": "Workstation-Alpha", "status": "synced", "last_sync": "2m ago"},
    {"id": "twin-002", "node": "Workstation-Beta", "status": "diverged", "last_sync": "14h ago"}
]

@router.get("/twins")
async def get_twins():
    return TWINS

@router.post("/spawn-twin")
async def spawn_twin(node_id: str):
    new_twin = {
        "id": f"twin-new",
        "node": node_id,
        "status": "initializing",
        "last_sync": "JUST_NOW"
    }
    TWINS.append(new_twin)
    return new_twin
