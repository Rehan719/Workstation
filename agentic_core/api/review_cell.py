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
    #  W691 - the agent is NAMED; whether it is calibrated is read from its recorded run, never sent here
    agent: Optional[str] = None
    discipline: Optional[str] = None
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


class CalibrationRun(BaseModel):
    model_config = {"extra": "forbid"}
    agent: str
    discipline: str = "care"
    model: str
    configuration: str                     # "model" or "floor" - what was serving when the agent was run
    date: str
    flags: Dict[str, List[str]]            # {case id: the reasons the agent flagged}; a rate is never sent


@router.post("/calibration/run")
async def record_calibration_run(req: CalibrationRun, user: dict | None = Depends(get_current_user)):
    """Record what a reviewer agent flagged on each case of a calibration set. THE RATES ARE COMPUTED HERE, from
    the flags and the set; a caller cannot assert one."""
    from agentic_core.api import _review_calibration as _cal
    the_set = _cal.load_set(req.discipline)
    if not the_set:
        raise HTTPException(status_code=422, detail=f"Not recorded: no calibration set exists for {req.discipline!r}.")
    if not the_set.get("runnable"):
        #  refused where the caller receives it: a run on cases that are only described measured nothing
        raise HTTPException(status_code=409, detail=(
            "Not recorded: " + str(the_set.get("runnable_basis") or "this calibration set cannot be run yet") + "."))
    if req.configuration not in _cal.CONFIGURATIONS:
        raise HTTPException(status_code=422, detail=f"configuration is one of {list(_cal.CONFIGURATIONS)}")
    if not str(req.agent).strip() or not str(req.model).strip() or _rt._date(req.date) is None:
        raise HTTPException(status_code=422, detail="Not recorded: a run names its agent, its model and its date.")
    known = {c["id"] for c in the_set.get("cases") or []}
    unknown = sorted(set(req.flags) - known)
    if unknown:
        raise HTTPException(status_code=422, detail=f"Not recorded: {unknown} are not cases of this set.")
    run = {"run_id": f"cal-{uuid.uuid4().hex[:10]}", "agent": req.agent.strip(), "discipline": req.discipline,
           "model": req.model.strip(), "configuration": req.configuration, "date": req.date,
           "set_version": the_set.get("version"), "flags": req.flags,
           "entered_by": _entered_by(user), "entered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    from agentic_core.config import mutate_json

    def _add(existing):
        rows = existing if isinstance(existing, list) else []
        rows.append(run)
        return rows
    mutate_json(_cal._runs_path(), _add, list)
    return {"recorded": True, "run_id": run["run_id"], "score": _cal.score(the_set["cases"], req.flags),
            "agent_now": _cal.calibration_of(run["agent"], req.discipline)}


@router.get("/calibration/{agent}")
async def calibration_of_agent(agent: str, discipline: str = "care"):
    from agentic_core.api import _review_calibration as _cal
    return {"agent": agent, "discipline": discipline, **_cal.calibration_of(agent, discipline)}


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
