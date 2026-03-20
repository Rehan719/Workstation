from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import List, Dict, Any, Set
import asyncio
import json
import random
from agentic_core.layers.l1_genomic.validator import validator_l1
from agentic_core.layers.l2_runtime.inference import inference_engine
from agentic_core.layers.l4_library.registry import model_registry
from agentic_core.layers.l5_recombination.merger import model_merger

router = APIRouter(prefix="/v154", tags=["Genesis API"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.get("/status")
async def get_genesis_status():
    """LAYER 6: ORCHESTRATION - Real-time system vitals."""
    return {
        "entity": "Workstation Sovereign v200.0",
        "epoch": "Genesis (v154.0)",
        "layers": {
            "L1": "Active (Constitutional)",
            "L2": "Active (Edge Runtime)",
            "L3": "Standby",
            "L4": "Active (Library)",
            "L5": "Active (Recombination)",
            "L6": "Active (Orchestration)",
            "L7": "First Light"
        },
        "constitution_root": getattr(validator_l1, 'root_hash', 'genesis_root')
    }

@router.websocket("/ws/streams")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Simulate real-time stream data from agentic core
            data = {
                "type": "SYSTEM_VITALS",
                "payload": {
                    "cpu": random.uniform(20, 80),
                    "memory": random.uniform(10, 30),
                    "swarm_health": random.uniform(0.9, 1.0),
                    "active_agents": random.randint(15, 45)
                }
            }
            await websocket.send_text(json.dumps(data))

            # Simulate agent pheromone signals (Signal Channel)
            if random.random() > 0.7:
                signal = {
                    "type": "AGENT_SIGNAL",
                    "payload": {
                        "agent_id": f"agent_{random.randint(1,5)}",
                        "signal_type": random.choice(["discovery", "synthesis", "optimization"]),
                        "strength": random.random()
                    }
                }
                await websocket.send_text(json.dumps(signal))

            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/forge/recombine")
async def trigger_recombination(model_ids: List[str], strategy: str = "TIES"):
    """LAYER 6 -> LAYER 5: Trigger model recombination."""
    # Constitutional check
    if not validator_l1.validate_action("recombine", {"models": model_ids}):
        raise HTTPException(status_code=403, detail="Recombination blocked by Article 1095.")

    if strategy == "TIES":
        res = model_merger.ties_merge(model_ids, [0.5, 0.5])
    else:
        res = model_merger.dare_merge(model_ids)

    # Register result in L4
    new_agent_did = model_registry.register_composite(res)

    # Notify connected clients via WebSocket
    await manager.broadcast(json.dumps({
        "type": "EVOLUTION_EVENT",
        "payload": {"event": "recombination_complete", "agent_did": new_agent_did}
    }))

    return {"status": "recombined", "agent_did": new_agent_did, "metadata": res}

@router.get("/library/models")
async def list_models():
    return model_registry.registry

@router.get("/constitution/articles")
async def list_articles():
    return getattr(validator_l1, 'genome', {}).get('constitution', {}).get('articles', [])
