from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import uuid

router = APIRouter(prefix="/treaties", tags=["Civilizational Governance"])

DRAFTS = []

@router.post("/draft")
async def draft_treaty(node_a: str, node_b: str, terms: str):
    draft = {
        "id": f"tr-{uuid.uuid4().hex[:6]}",
        "nodes": [node_a, node_b],
        "terms": terms,
        "status": "drafting",
        "signatures": []
    }
    DRAFTS.append(draft)
    return draft

@router.get("/active")
async def list_active_treaties():
    return [
        {"id": "tr-alpha-beta", "nodes": ["Alpha", "Beta"], "type": "Data Sharing", "status": "enforced"},
        {"id": "tr-gamma-alpha", "nodes": ["Gamma", "Alpha"], "type": "Compute Exchange", "status": "negotiating"}
    ]

@router.post("/{treaty_id}/sign")
async def sign_treaty(treaty_id: str, node_id: str):
    return {"status": "signed", "treaty": treaty_id, "node": node_id}
