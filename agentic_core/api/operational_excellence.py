"""
Operational Excellence — the learning loop over Workstation's OWN resources.

Records the real OUTCOME of every meaningful run (native swarm cascades, deliverable
production/regeneration, transformation orchestrations) — which OWNED resource served it,
how long it took, and whether it succeeded — then aggregates those outcomes into honest
per-resource RANKINGS (success rate, speed, in-house rate, recency). This is the feedback
substrate the platform learns from: resources that perform are surfaced and can be preferred.

Honest by construction: only real, recorded runs are aggregated — nothing is fabricated, and
an empty store reports zero (never invented numbers).

  POST /api/v1/operations/record      — record an outcome (also callable in-process)
  GET  /api/v1/operations/outcomes     — recent outcomes (?resource= / ?vsb_id= / ?kind=)
  GET  /api/v1/operations/rankings     — per-resource aggregates, ranked
  GET  /api/v1/operations/summary      — platform-wide operational summary
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/operations", tags=["operational-excellence"])

_STORE = Path("data/operations_outcomes.json")
_CAP = 2000


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(rows: List[Dict[str, Any]]) -> None:
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(rows[-_CAP:], indent=2), encoding="utf-8")


def record_outcome(kind: str, resource: str, *, served_by: str = "native",
                   is_external: bool = False, duration_ms: int = 0, success: bool = True,
                   ref: Optional[str] = None, vsb_id: Optional[str] = None) -> Dict[str, Any]:
    """Append one real run outcome. Reusable in-process (the run paths call this best-effort)
    and via the /record endpoint. Never raises into a caller — recording is non-critical."""
    outcome = {
        "id": f"op-{uuid.uuid4().hex[:8]}",
        "kind": kind,
        "resource": resource,
        "served_by": served_by,
        "is_external": bool(is_external),
        "duration_ms": int(duration_ms),
        "success": bool(success),
        "ref": ref,
        "vsb_id": vsb_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        rows = _load()
        rows.append(outcome)
        _save(rows)
    except Exception:
        pass
    return outcome


def _rankings(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    agg: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        key = r.get("resource", "unknown")
        a = agg.setdefault(key, {"resource": key, "kind": r.get("kind"), "runs": 0, "successes": 0,
                                 "total_ms": 0, "in_house": 0, "last_seen": ""})
        a["runs"] += 1
        a["successes"] += 1 if r.get("success") else 0
        a["total_ms"] += int(r.get("duration_ms", 0))
        a["in_house"] += 0 if r.get("is_external") else 1
        a["last_seen"] = max(a["last_seen"], r.get("created_at", ""))
    out = []
    for a in agg.values():
        runs = a["runs"] or 1
        out.append({
            "resource": a["resource"], "kind": a["kind"], "runs": a["runs"],
            "success_rate": round(a["successes"] / runs, 3),
            "avg_duration_ms": round(a["total_ms"] / runs),
            "in_house_rate": round(a["in_house"] / runs, 3),
            "last_seen": a["last_seen"],
        })
    # best operational performers first: success, then in-house, then speed, then volume
    out.sort(key=lambda x: (x["success_rate"], x["in_house_rate"], -x["avg_duration_ms"], x["runs"]), reverse=True)
    return out


def model_health() -> Dict[str, Dict[str, Any]]:
    """Per-model-resource health from recorded model attempts (kind="model_attempt"), keyed by the
    model name (served_by). The native orchestrator uses this to ADAPT selection — deprioritise a
    model resource with a clearly-poor recent track record. Honest: only real recorded attempts."""
    agg: Dict[str, Dict[str, Any]] = {}
    for r in _load():
        if r.get("kind") != "model_attempt":
            continue
        name = r.get("served_by", "")
        a = agg.setdefault(name, {"runs": 0, "successes": 0, "total_ms": 0})
        a["runs"] += 1
        a["successes"] += 1 if r.get("success") else 0
        a["total_ms"] += int(r.get("duration_ms", 0))
    return {name: {"runs": a["runs"],
                   "success_rate": round(a["successes"] / a["runs"], 3) if a["runs"] else 0.0,
                   "avg_ms": round(a["total_ms"] / a["runs"]) if a["runs"] else 0}
            for name, a in agg.items()}


class RecordRequest(BaseModel):
    kind: str
    resource: str
    served_by: str = "native"
    is_external: bool = False
    duration_ms: int = 0
    success: bool = True
    ref: Optional[str] = None
    vsb_id: Optional[str] = None


@router.post("/record")
async def record(req: RecordRequest):
    return record_outcome(req.kind, req.resource, served_by=req.served_by, is_external=req.is_external,
                          duration_ms=req.duration_ms, success=req.success, ref=req.ref, vsb_id=req.vsb_id)


@router.get("/outcomes")
async def outcomes(resource: Optional[str] = None, vsb_id: Optional[str] = None,
                   kind: Optional[str] = None, limit: int = 100):
    rows = _load()
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    else:
        rows = [r for r in rows if r.get("kind") != "model_attempt"]   # infra-level; hidden by default
    if resource:
        rows = [r for r in rows if r.get("resource") == resource]
    if vsb_id:
        rows = [r for r in rows if r.get("vsb_id") == vsb_id]
    return {"outcomes": rows[-limit:][::-1], "total": len(rows)}


@router.get("/rankings")
async def rankings():
    return {"rankings": _rankings([r for r in _load() if r.get("kind") != "model_attempt"])}


@router.get("/summary")
async def summary():
    rows = [r for r in _load() if r.get("kind") != "model_attempt"]
    n = len(rows)
    successes = sum(1 for r in rows if r.get("success"))
    in_house = sum(1 for r in rows if not r.get("is_external"))
    ranks = _rankings(rows)
    return {
        "total_runs": n,
        "success_rate": round(successes / n, 3) if n else 0.0,
        "in_house_rate": round(in_house / n, 3) if n else 0.0,
        "distinct_resources": len(ranks),
        "top_resource": ranks[0]["resource"] if ranks else None,
        "kinds": sorted({r.get("kind") for r in rows if r.get("kind")}),
    }
