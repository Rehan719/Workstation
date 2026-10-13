"""THE REVIEW CELL'S RECORDS - the door by which a review is recorded, and the answers that read them.

OWNER RULING 2026-10-12 (the review cell, clauses 1, 2, 3 and 5). A review is a RECORD. This router is the one
door that writes one, and it is the administrator's:

  POST /api/v1/review/record      record a rule check, an agent's review or a person's signature for one tool
  GET  /api/v1/review/tier/{tool} what that tool's answers say about review, by the function they all use
  GET  /api/v1/review/records     every record, each with whether it counts and why not

WHAT THE DOOR REFUSES AND WHAT IT KEEPS
- A record that falls short of its tier's rule is REFUSED, in the rule's own words, and nothing is stored: a rule
  check naming no test, an agent's review naming no checklist or source, a signature with no name, no credential
  as stated, no statement of what was reviewed, or no lapse date that is still ahead.
- ONE record that does not count IS kept: the review of an agent that has not been calibrated. The ruling asks
  that such a review be labelled, not hidden - so it is stored, reported beside the tool, and raises nothing.
- A signature is entered by the administrator and is the PERSON'S statement: the credential is stored as stated
  and every answer says this platform did not verify it. Who entered it is recorded beside it.
- Nothing here composes a review. An agent's review is recorded by whoever ran it, with the model that reviewed.

No tier, record or sentence claims a professional's role for an agent.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from agentic_core.api import _review_tier as _rt
from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/api/v1/review", tags=["review-cell"])


class ReviewRecord(BaseModel):
    model_config = {"extra": "forbid"}
    tool: str
    tier: str
    date: str
    # checked by rule
    rule: Optional[str] = None
    test: Optional[str] = None
    # reviewed by Workstation's specialist agent
    checklist: Optional[str] = None
    sources_read: Optional[List[str]] = None
    model: Optional[str] = None
    agent_calibrated: Optional[bool] = None
    could_not_check: Optional[str] = None
    # signed by a qualified person
    name: Optional[str] = None
    credential_as_stated: Optional[str] = None
    reviewed: Optional[str] = None
    lapses_on: Optional[str] = None
    note: Optional[str] = None


def _entered_by(user: Any) -> str:
    #  who entered the record: the signed-in name, or the single-user label when authentication is off
    return (user.get("username") if isinstance(user, dict) else None) or "single-user-mode"


@router.post("/record")
async def record_review(req: ReviewRecord, user: dict | None = Depends(get_current_user)):
    if not str(req.tool or "").strip():
        raise HTTPException(status_code=422, detail="a record names the tool it is for")
    rec = {k: v for k, v in req.model_dump().items() if v is not None}
    verdict = _rt.counts(rec)
    kept_though_not_counted = bool(verdict.get("uncalibrated_agent_review"))
    if not verdict["counts"] and not kept_though_not_counted:
        #  refused where the caller receives it, before anything is written
        raise HTTPException(status_code=422, detail=(
            f"Not recorded: {verdict['why_not']}. A record is stored only when it meets the rule of the tier "
            f"it claims."))
    if rec.get("tier") == _rt.REVIEWED_BY_AGENT and not str(rec.get("model") or "").strip():
        raise HTTPException(status_code=422, detail="Not recorded: an agent's review names the model that reviewed.")
    rec["record_id"] = f"rev-{uuid.uuid4().hex[:10]}"
    rec["entered_by"] = _entered_by(user)
    rec["entered_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    from agentic_core.config import mutate_json

    def _add(existing):
        rows = existing if isinstance(existing, list) else []
        rows.append(rec)
        return rows
    mutate_json(_rt._path(), _add, list)
    return {"recorded": True, "record_id": rec["record_id"], "counts": verdict["counts"],
            "why_not": verdict.get("why_not"),
            "kept_though_not_counted": kept_though_not_counted,
            "kept_basis": ("the review of an agent that has not been calibrated is kept and shown, labelled, and "
                           "does not raise the tool's tier") if kept_though_not_counted else None,
            "tool_now_says": _rt.review_statement(rec["tool"])}


@router.get("/tier/{tool}")
async def tier_of(tool: str):
    return {"tool": tool, **_rt.review_statement(tool)}


@router.get("/records")
async def all_records():
    recs = _rt._records()
    if recs is None:
        raise HTTPException(status_code=503, detail=(
            "The record of reviews exists and could not be read whole. Nothing is shown from it, and no tool is "
            "treated as reviewed."))
    rows: List[Dict[str, Any]] = []
    for r in recs:
        v = _rt.counts(r)
        rows.append({**r, "counts": v["counts"], "why_not": v.get("why_not")})
    tools = sorted({str(r.get("tool")) for r in recs if r.get("tool")})
    return {"records": rows, "total": len(rows), "counted": sum(1 for r in rows if r["counts"]),
            "tools": {t: _rt.review_statement(t)["label"] for t in tools},
            "credential_basis": _rt.NOT_VERIFIED,
            "basis": ("every stored record, each judged now by the rule of the tier it claims; a signature that "
                      "has lapsed since it was entered no longer counts")}
