from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends
from typing import List, Dict, Any, Set
import asyncio
import json
import random

# v3.0 Unified Layer Imports
from agentic_core.layers.l1_identity.validator import validator_l1
from agentic_core.layers.l2_hardware.inference import inference_engine
from agentic_core.layers.l7_module_library.registry import module_registry
from agentic_core.layers.l8_recombination.merger import model_merger
from agentic_core.layers.l9_orchestration.orchestrator import swarm_orchestrator
from agentic_core.layers.ueg import ueg
from agentic_core.governance.dao import dao_framework
from agentic_core.reactor.ecosystem.marketplace import marketplace

router = APIRouter(prefix="/v154", tags=["Sovereign Genesis API"])

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
    """LAYER 12: UX - v3.0 Sovereign Genesis Status Report."""
    ueg.log_event("L12", "API", "STATUS_REQUEST", {"entity": "Workstation v3.0 Sovereign"})
    return {
        "entity": "Workstation Sovereign v3.0",
        "epoch": "Genesis (v154.0)",
        "layers": {f"L{i}": "Active (High Fidelity)" for i in range(1, 13)},
        "governance": dao_framework.legal_status,
        "merkle_root": validator_l1.merkle_root,
        "ueg_root": ueg.merkle_root
    }

# WebSocket moved to main.py to avoid router prefixing issues

@router.post("/forge/recombine")
async def trigger_recombination(model_ids: List[str], strategy: str = "TIES"):
    """LAYER 8: RECOMBINATION ENGINE - Article 1095 Recombination."""
    # GaaS Validation (L1)
    context = {"models": model_ids, "fitness": 0.9}
    validation = validator_l1.validate_action("recombine", context)
    if not validation["valid"]:
        ueg.log_event("L1", "GaaS", "ACTION_BLOCKED", {"action": "recombine", "validation": validation}, ["audit-required"])
        raise HTTPException(status_code=403, detail=validation["reason"])

    if strategy == "TIES":
        res = model_merger.ties_merge(model_ids, [0.5] * len(model_ids))
    else:
        res = model_merger.dare_merge(model_ids)

    # Register result in L7
    new_agent_did = module_registry.register_composite(res)

    ueg.log_event("L8", "Merger", "RECOMBINATION_COMPLETE", {"agent_did": new_agent_did, "mode": validation["mode"]})

    # Notify connected clients via WebSocket
    await manager.broadcast(json.dumps({
        "type": "EVOLUTION_EVENT",
        "payload": {"event": "recombination_complete", "agent_did": new_agent_did}
    }))

    return {"status": "recombined_sovereign", "agent_did": new_agent_did, "metadata": res}

@router.get("/library/models")
async def list_models():
    return module_registry.registry

@router.get("/constitution/articles")
async def list_articles():
    return validator_l1.genome.get('constitution', {}).get('articles', [])

@router.post("/orchestration/swarm")
async def start_swarm(goal: str):
    """LAYER 9: ORCHESTRATION - Initiate a v3.0 Swarm."""
    swarm_id = swarm_orchestrator.form_swarm(goal)
    ueg.log_event("L9", "Orchestrator", "SWARM_INITIATED", {"swarm_id": swarm_id, "goal": goal})
    return {"status": "sovereign_swarm_launched", "swarm_id": swarm_id}

@router.get("/marketplace/agents")
async def list_marketplace():
    return marketplace.list_agents()

@router.post("/marketplace/publish")
async def publish_agent(blueprint: Dict[str, Any], creator: str = "anonymous"):
    # GaaS Validation for publishing
    validation = validator_l1.validate_action("marketplace_publish", {"creator": creator})
    if not validation["valid"]:
         raise HTTPException(status_code=403, detail="GaaS: Publication blocked.")

    agent_id = marketplace.publish_agent(blueprint, creator)
    return {"status": "PUBLISHED", "id": agent_id}
