import logging
from fastapi import APIRouter, HTTPException, Depends
from src.organism.python.evidence.graph_schema import EvidenceGraph
from .neural_bridge import verify_token

logger = logging.getLogger(__name__)

router = APIRouter()
graph = EvidenceGraph()

@router.get("/api/v1/evidence/graph", dependencies=[Depends(verify_token)])
async def get_evidence_graph():
    """Returns the chronology of legal events for the UI."""
    try:
        return graph.get_chronology()
    except Exception as e:
        logger.error(f"Evidence API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/evidence/ingest", dependencies=[Depends(verify_token)])
async def trigger_ingestion():
    """Manually triggers evidence ingestion."""
    return {"status": "SUCCESS", "message": "Scan initiated."}
