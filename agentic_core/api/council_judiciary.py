"""
Council Judiciary API — exposes the AI Constitutional Judge's dispute adjudication
and override workflow over HTTP for the Sovereign Judiciary frontend page.

Note: the original `ConstitutionalJudge` / `PrecedentRegistry` classes
(agentic_core/governance/ai_constitutional_judge.py, precedent_registry.py) depend on
a live Firestore connection that isn't configured in this environment (no
`firebase_admin.initialize_app()` call anywhere, no credentials). Rather than crash on
import or silently fake success, this module implements the same precedent-based
adjudication logic against an in-memory precedent/ruling store so the endpoint is
genuinely functional end-to-end.
"""
import datetime
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/council/judge", tags=["Council Judiciary"])

# Real (if locally-scoped) precedent set — analogous to the seed data the Firestore
# version would have loaded from data/sovereign_case_law/.
PRECEDENTS: List[Dict[str, Any]] = [
    {
        "precedent_id": "PREC-1132-A",
        "title": "Node Resource Over-Allocation Breach",
        "article": "Article 1132",
        "keywords": ["resource", "compute", "over-allocation", "quota"],
    },
    {
        "precedent_id": "PREC-1107-B",
        "title": "Credential Rotation Non-Compliance",
        "article": "Article 1107",
        "keywords": ["credential", "key", "rotation", "pqc"],
    },
    {
        "precedent_id": "PREC-1096-C",
        "title": "Cross-Node Data Sharing Without Treaty",
        "article": "Article 1096",
        "keywords": ["data", "sharing", "treaty", "federation"],
    },
]


def _match_precedent(description: str) -> Optional[Dict[str, Any]]:
    haystack = description.lower()
    best, best_score = None, 0
    for p in PRECEDENTS:
        score = sum(1 for kw in p["keywords"] if kw in haystack)
        if score > best_score:
            best, best_score = p, score
    return best


class DisputeRequest(BaseModel):
    dispute_id: Optional[str] = None
    description: str


class OverrideRequest(BaseModel):
    ruling_id: str
    reason: str = "Owner Emergency Veto"


_rulings: Dict[str, Dict[str, Any]] = {}


def _adjudicate(dispute_id: str, description: str) -> Dict[str, Any]:
    """Real precedent-matching adjudication, mirroring ConstitutionalJudge.adjudicate's
    contract but against the in-memory precedent set."""
    precedent = _match_precedent(description)
    ruling_id = f"RUL_{dispute_id}"
    ruling = {
        "ruling_id": ruling_id,
        "dispute_id": dispute_id,
        "status": "PENDING_RATIFICATION",
        "cited_precedent": precedent["precedent_id"] if precedent else "NONE",
        "decision": (
            f"Penalty applied based on {precedent['article']} breach."
            if precedent else "No violation found."
        ),
        "reasoning_trace": (
            f"Analogous to '{precedent['title']}' ({precedent['precedent_id']})."
            if precedent else "No matching precedent in registry; baseline ruling."
        ),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    _rulings[ruling_id] = ruling
    return ruling


def _seed_initial_rulings():
    """Seed a couple of real adjudicated rulings on startup so the page has genuine
    (not fabricated client-side) data on first load."""
    if _rulings:
        return
    _adjudicate("DSP-001", "Node exceeded its allocated compute quota for 3 consecutive epochs.")
    _adjudicate("DSP-002", "Node shared training data with an unrelated federation member without an active treaty.")


_seed_initial_rulings()


@router.get("/rulings")
async def list_rulings() -> List[Dict[str, Any]]:
    return list(_rulings.values())


@router.post("/disputes")
async def file_dispute(request: DisputeRequest) -> Dict[str, Any]:
    """Files a new dispute and returns the AI Judge's real adjudicated ruling."""
    dispute_id = request.dispute_id or f"DSP-{str(uuid.uuid4())[:8].upper()}"
    return _adjudicate(dispute_id, request.description)


@router.post("/override")
async def override_ruling(request: OverrideRequest) -> Dict[str, Any]:
    """Processes an owner veto of an AI ruling, mirroring
    ConstitutionalJudge.handle_override's contract."""
    ruling = _rulings.get(request.ruling_id)
    if not ruling:
        raise HTTPException(status_code=404, detail="Ruling not found")
    ruling["status"] = "OVERRIDDEN"
    ruling["override_reason"] = request.reason
    return {"status": "OVERRIDDEN", "ruling_id": request.ruling_id}
