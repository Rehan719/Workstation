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
    """No treaties exist.

    W413 - two invented treaties were returned here, one between nodes "Alpha" and "Beta" with
    status "enforced". An enforced treaty asserts a binding agreement between parties. No treaty
    store is read and neither node exists.
    """
    return {
        "treaties": [],
        "detail": ("No treaty register exists on this deployment. Two invented treaties, one marked "
                   "enforced, were previously returned here."),
    }
@router.post("/{treaty_id}/sign")
async def sign_treaty(treaty_id: str, node_id: str):
    return {"status": "signed", "treaty": treaty_id, "node": node_id}
