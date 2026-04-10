from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import time

router = APIRouter(prefix="/federation", tags=["Global Orchestration"])

NODES = {}

@router.post("/register")
async def register_node(node_data: Dict[str, Any]):
    node_id = node_data.get("id")
    if not node_id:
        raise HTTPException(status_code=400, detail="Node ID required")
    NODES[node_id] = {
        **node_data,
        "last_heartbeat": time.time(),
        "status": "online"
    }
    return {"status": "registered", "token": "signed-jwt-baseline"}

@router.get("/nodes", response_model=List[Dict[str, Any]])
async def list_nodes():
    current_time = time.time()
    # Auto-offline nodes older than 60s
    for nid in NODES:
        if current_time - NODES[nid]["last_heartbeat"] > 60:
            NODES[nid]["status"] = "offline"

    # Include some production nodes if empty for demo
    if not NODES:
        return [
            {"id": "Alpha-Live", "status": "online", "health": 0.99, "pos": [150, 250]},
            {"id": "Beta-Live", "status": "online", "health": 0.92, "pos": [350, 450]}
        ]
    return list(NODES.values())

@router.post("/heartbeat")
async def node_heartbeat(node_id: str):
    if node_id in NODES:
        NODES[node_id]["last_heartbeat"] = time.time()
        NODES[node_id]["status"] = "online"
        return {"status": "ack"}
    raise HTTPException(status_code=404, detail="Node not registered")
