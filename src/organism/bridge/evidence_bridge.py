import logging
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from src.organism.python.evidence.graph_schema import EvidenceGraph

logger = logging.getLogger(__name__)

router = APIRouter()
graph = EvidenceGraph()

@router.get("/api/v1/evidence/graph")
async def get_evidence_graph():
    """Returns the chronology of legal events for the UI."""
    try:
        return graph.get_chronology()
    except Exception as e:
        logger.error(f"Evidence API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/evidence/ingest")
async def trigger_ingestion():
    """Manually triggers evidence ingestion (placeholder for watcher)."""
    # This would call EvidenceIngestionAgent.scan_and_ingest()
    return {"status": "SUCCESS", "message": "Scan initiated."}
