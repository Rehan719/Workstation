from fastapi import APIRouter, Depends
from pydantic import BaseModel
from agentic_core.ai.gateway import gateway
from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Query"])


class QueryRequest(BaseModel):
    message: str
    agent: str = "solutions-platform"


@router.post("/query")
async def ai_query(req: QueryRequest, user: dict | None = Depends(get_current_user)):
    # §17.5 invariant 1 (W343) — the caller's identity reaches the memory layer: without it,
    # authenticated chat landed in the shared platform namespace (scoping without teeth).
    owner = user.get("username") if isinstance(user, dict) else None
    # W506 (P2.2) - query_meta, so the reply says which OWNED resource served it. `owner_id` was already
    # threaded here (FU-276 attribution); `augment=False` is stated because a repo-wide guard requires the
    # recall decision at every call site rather than inherited from the default.
    _r = await gateway.query_meta(req.message, agent=req.agent, owner_id=owner, augment=False)
    return {"response": _r.get("output", ""),
            "served_by": _r.get("served_by"),
            "is_external": bool(_r.get("is_external")),
            "governance_checkpoint": _r.get("governance_checkpoint")}
