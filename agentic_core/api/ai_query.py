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
    response = await gateway.query(req.message, agent=req.agent, owner_id=owner)
    return {"response": response}
