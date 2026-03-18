from fastapi import APIRouter
from pydantic import BaseModel
from agentic_core.ai.orchestrator import orchestrator

router = APIRouter(prefix="/ceo", tags=["Multi-Agent"])

class TaskRequest(BaseModel):
    agent: str
    task: str

@router.post("/delegate")
async def delegate_task(request: TaskRequest):
    res = await orchestrator.delegate_task(request.agent, request.task)
    return res
