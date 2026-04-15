import os
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator
from core.models import MJMOutputBundle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MJM-API")

app = FastAPI(title="MJM Intelligence Engine API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared orchestrator instance
orchestrator = MJMWorkflowOrchestrator()

class PipelineRequest(BaseModel):
    domain_id: str
    queries: List[str]
    contributor: str = "anonymous"

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[Dict[str, Any]] = None

# In-memory job store (for v1.0 simplicity)
jobs: Dict[str, Dict[str, Any]] = {}

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "MJM v1.0"}

@app.post("/pipeline/execute")
async def execute_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    job_id = f"JOB-{os.urandom(4).hex()}"
    jobs[job_id] = {"status": "processing", "request": request.dict()}

    background_tasks.add_task(run_workflow, job_id, request)

    return {"job_id": job_id, "status": "processing"}

async def run_workflow(job_id: str, request: PipelineRequest):
    try:
        logger.info(f"Starting workflow for job {job_id}")
        bundle = await orchestrator.execute_pipeline(request.dict())
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = bundle.model_dump()
        logger.info(f"Workflow completed for job {job_id}")
    except Exception as e:
        logger.error(f"Workflow failed for job {job_id}: {str(e)}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.get("/pipeline/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/checkpoints")
async def list_checkpoints():
    # Simple logic to list generated checkpoint files
    checkpoint_dir = "checkpoints"
    if not os.path.exists(checkpoint_dir):
        return []
    return [f for f in os.listdir(checkpoint_dir) if f.endswith(".json")]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
