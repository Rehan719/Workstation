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
    """W967 (P5.10 clause 4) - this answered "signed" for any id and read or wrote nothing. A treaty is signed only
    where a draft this process holds exists to sign: the node is added to its signatures, which are returned. Any
    other id is refused, and nothing is signed."""
    for d in DRAFTS:
        if d.get("id") == treaty_id:
            if node_id not in d["signatures"]:
                d["signatures"].append(node_id)
            return {"status": "signed", "treaty": treaty_id, "node": node_id, "signatures": list(d["signatures"]),
                    "kept": "in this process's memory only: drafts and their signatures are lost when it restarts"}
    raise HTTPException(status_code=404, detail=(
        f"No draft treaty {treaty_id} is held by this process, so nothing was signed. No treaty register exists on "
        "this deployment."))
