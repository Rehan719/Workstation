from fastapi import APIRouter
from pydantic import BaseModel
from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/ai", tags=["AI Query"])


class QueryRequest(BaseModel):
    message: str
    agent: str = "solutions-platform"


@router.post("/query")
async def ai_query(req: QueryRequest):
    response = await gateway.query(req.message, agent=req.agent)
    return {"response": response}
