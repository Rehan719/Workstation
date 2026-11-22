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
- TWO KINDS of record that do not count ARE kept: the review of an agent that has not been calibrated, and
  (W1195c) a calibrated agent's review that the run calibrating it does not hold. The ruling asks that such a review
  be labelled, not hidden - so it is stored, reported beside the tool with its reason, and raises nothing.
- A signature is entered by the administrator and is the PERSON'S statement: the credential is stored as stated
  and every answer says this platform did not verify it. Who entered it is recorded beside it.
- Nothing here composes a review. An agent's review is recorded by whoever ran it, with the model that reviewed;
  Workstation's own Care reviewer (care_reviewer.py, W1100) is run over the calibration set by its own route.
- W1183: only a run made by that route, dated the day it is made, calibrates the agent. A run typed through
  /calibration/run is a person's account of what was flagged: it is kept, says which door it came by, and
  calibrates nothing.
- W1195c: a run made by that route records the digest of what its reviewer was shown, and each case answered in
  another form than the one asked for; it starts only when the context the local runtime reports for its model holds
  the longest prompt the set sends. An agent's review counts only when the model and build it names are those of
  the run that calibrated it, and it is dated on or after that run.

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
    #  W921 (P5.15 clause 2) - each source read is {"source": a register id, "page": what was read, "read_on": a date};
    #  a bare string is accepted at the door only so the refusal can say what it lacks
    sources_read: Optional[List[Any]] = None
    tool_version: Optional[str] = None
    model: Optional[str] = None
    #  W1195c (FU-1821) - the build of the model that reviewed, as its runtime reports it: a review counts only when its
    #  model and build are those of the run that calibrated its agent
    build: Optional[str] = None
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
    #  W1195c (FU-1821) - and a calibrated agent's review that its calibrated run does not hold is kept the same way
    kept_though_not_counted = bool(verdict.get("uncalibrated_agent_review") or verdict.get("not_held_to_run"))
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
            "kept_basis": (("the review of an agent that has not been calibrated is kept and shown, labelled, and "
                            "does not raise the tool's tier") if verdict.get("uncalibrated_agent_review") else
                           (f"the review of a calibrated agent that is not held to the run that calibrated it "
                            f"({verdict.get('not_held_because')}) is kept and shown, labelled, and does not raise the "
                            f"tool's tier") if kept_though_not_counted else None),
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
    if req.configuration not in _cal.CONFIGURATIONS:
        raise HTTPException(status_code=422, detail=f"configuration is one of {list(_cal.CONFIGURATIONS)}")
    if not str(req.agent).strip() or not str(req.model).strip() or _rt._date(req.date) is None:
        raise HTTPException(status_code=422, detail="Not recorded: a run names its agent, its model and its date.")
    #  W1099 (FU-1054) - WHETHER THE SET CAN BE RUN ON THE RUN'S DATE IS COMPUTED, never read from a flag, and every
    #  reason it cannot is said where the caller receives it: a run on cases not written out, or on sources not
    #  read, measured nothing
    can = _cal.runnable(the_set, on=_rt._date(req.date))
    if not can["runnable"]:
        raise HTTPException(status_code=409, detail=(
            f"Not recorded: the calibration set cannot be run on {can['on']}: " + "; ".join(can["why_not"]) + "."))
    known = {c["id"] for c in the_set.get("cases") or []}
    unknown = sorted(set(req.flags) - known)
    if unknown:
        raise HTTPException(status_code=422, detail=f"Not recorded: {unknown} are not cases of this set.")
    return _store_run(the_set, user, agent=req.agent.strip(), discipline=req.discipline, model=req.model.strip(),
                      configuration=req.configuration, date=req.date, flags=req.flags, door=_cal.TYPED_DOOR)


def _store_run(the_set: Dict[str, Any], user: Any, **fields: Any) -> Dict[str, Any]:
    """W1100 - the one way a run is kept, whoever entered its flags: with the set's version, who entered it and when,
    and the rates computed here from the flags. W1183 - with the door it came by, and the digest of the set as it
    stood, so a case edited under the same version voids it."""
    from agentic_core.api import _review_calibration as _cal
    from agentic_core.config import mutate_json
    run = {"run_id": f"cal-{uuid.uuid4().hex[:10]}", **fields, "set_version": the_set.get("version"),
           "set_digest": _cal.set_digest(the_set),
           "entered_by": _entered_by(user), "entered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    def _add(existing):
        rows = existing if isinstance(existing, list) else []
        rows.append(run)
        return rows
    mutate_json(_cal._runs_path(), _add, list)
    return {"recorded": True, "run_id": run["run_id"], "score": _cal.score(the_set["cases"], fields["flags"]),
            "agent_now": _cal.calibration_of(run["agent"], fields["discipline"])}


def _context_refusal(ctx: Dict[str, Any], longest: Dict[str, Any]) -> str:
    """W1195c (FU-1831) - why a run does not start, in the words its caller receives: what the runtime reported of the
    context it gives the run's model, and the rule a run starts by. The rule is a bound, not a size: the figure is
    bytes, and the prompt is fewer tokens than that."""
    needs = (f"a context of at least {longest.get('needs')} tokens: the bytes of the longest prompt the set sends "
             f"({longest.get('case')}, {longest.get('prompt_bytes')} bytes) and of the reply that flags each of the "
             f"set's reasons once ({longest.get('reply_bytes')} bytes), since no token is shorter than one byte; the "
             "prompt's own token count is not read here")
    n = ctx.get("context_length")
    if isinstance(n, int) and not isinstance(n, bool):
        return (f"Not run: the local runtime gives {ctx.get('model')} a context of {n} tokens, and a run starts only "
                f"with {needs}. Give the model a longer context (with Ollama, OLLAMA_CONTEXT_LENGTH) and run again; "
                "nothing was asked of it.")
    return (f"Not run: {ctx.get('basis')}. A run starts only when the runtime reports, for its model, {needs}; "
            "nothing was asked of it.")


class AgentRun(BaseModel):
    model_config = {"extra": "forbid"}
    discipline: str = "care"
    date: str                              # the day the run is made: the set must be runnable on it


@router.post("/calibration/agent-run")
async def run_reviewer_agent(req: AgentRun, user: dict | None = Depends(get_current_user)):
    """W1100 (FU-1054 part 2) - Workstation's reviewer agent over every case of the set, what it flagged recorded as
    one run. Nothing is asked of a model unless the set can be run on the date. A case the floor answered is no
    review, and a run is one model's: a run with either is refused, and nothing is kept."""
    from agentic_core.api import _review_calibration as _cal
    from agentic_core.api import care_reviewer as _cr
    if req.discipline != "care":
        raise HTTPException(status_code=422, detail=(
            f"Not run: Workstation has no reviewer agent for {req.discipline!r}; Care's is the first."))
    the_set, day = _cal.load_set("care"), _rt._date(req.date)
    if not the_set or day is None:
        raise HTTPException(status_code=422, detail="Not run: a run names its date, on a set that exists.")
    can = _cal.runnable(the_set, on=day)
    if not can["runnable"]:
        raise HTTPException(status_code=409, detail=(
            f"Not run: the calibration set cannot be run on {can['on']}: " + "; ".join(can["why_not"]) + "."))
    #  W1183 - A RUN IS DATED THE DAY IT IS MADE: a run said to be of another day is refused before a model is asked
    today = _cal._today()
    if day != today:
        raise HTTPException(status_code=422, detail=(
            f"Not run: a run is dated the day it is made ({today.isoformat()}), not {day.isoformat()}."))
    #  W1195c (FU-1831) - THE RUN STARTS ONLY WHEN ITS MODEL'S CONTEXT HOLDS EVERY PROMPT. The context the local runtime
    #  gives the model the reviewer is served by (the runtime's default, as the orchestrator resolves it) is read as the
    #  runtime reports it, before any model is asked. The run is refused while that context is shorter than the longest
    #  prompt the set sends with the reply that flags each reason once, counted in bytes (no token is shorter than a
    #  byte, so the figure is a bound and not the prompt's size), or while the runtime reports none: a prompt cut to fit
    #  would leave the run saying what its reviewer was shown while it read less
    import asyncio
    from agentic_core.ai.native import model_resource as _mr
    longest = _cr.longest_prompt(the_set)
    ctx = await asyncio.to_thread(_mr.context_given, "ollama")
    n_ctx = ctx.get("context_length")
    if not isinstance(n_ctx, int) or isinstance(n_ctx, bool) or n_ctx < longest["needs"]:
        raise HTTPException(status_code=409, detail=_context_refusal(ctx, longest))
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    #  W1195c (FU-1821) - what the reviewer is shown, over its fixed probe, taken before any model is asked
    shown = _cr.shown_digest(the_set)
    got = await _cr.run_on_set(the_set)
    finished = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if got["floor_answered"]:
        raise HTTPException(status_code=409, detail=(
            f"Not recorded: no model served {len(got['floor_answered'])} of the set's case(s) "
            f"({', '.join(got['floor_answered'])}), and the floor cannot review; nothing was flagged for them."))
    if len(got["models"]) != 1:
        raise HTTPException(status_code=409, detail=(
            f"Not recorded: the cases were reviewed by {len(got['models'])} models "
            f"({', '.join(got['models']) or 'none'}); a run is one model's."))
    #  W1183 - KEPT WHOLE: the door, what each case was answered with beyond its flags, the cases not answered, which
    #  model and build reviewed, and when the run began and ended
    from agentic_core.ai.gateway import served_identity_of
    out = _store_run(the_set, user, agent=_cr.AGENT, discipline="care", model=got["models"][0],
                     configuration="model", date=day.isoformat(), flags=got["flags"], door=_cal.AGENT_DOOR,
                     per_case=got["per_case"], not_answered=got["not_answered"],
                     not_in_form=got["not_in_form"], shown_digest=shown,
                     served_identity=served_identity_of(got["models"][0]),
                     runtime_context={"model": ctx.get("model"), "context_length": n_ctx, "basis": ctx.get("basis"),
                                      "runtime_version": ctx.get("runtime_version"),
                                      "needs": longest["needs"], "longest_case": longest["case"],
                                      "longest_prompt_bytes": longest["prompt_bytes"],
                                      "longest_reply_bytes": longest["reply_bytes"]},
                     started_at=started, finished_at=finished)
    return {**out, "lines_not_read_as_flags": got["lines_not_read_as_flags"], "not_answered": got["not_answered"],
            "not_in_form": got["not_in_form"]}


@router.get("/calibration/{agent}")
async def calibration_of_agent(agent: str, discipline: str = "care"):
    from agentic_core.api import _review_calibration as _cal
    said = _cal.calibration_statement(agent, discipline)
    #  W1183 - the statement every page reads, the days the set can be run, and the server's own date, so a run can
    #  be asked for on the day the server will date it
    return {"agent": agent, "discipline": discipline, **_cal.calibration_of(agent, discipline), "statement": said,
            "window": said["set"]["window"], "today": _cal._today().isoformat()}


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
