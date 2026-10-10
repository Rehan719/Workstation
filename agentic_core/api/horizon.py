"""Horizon's surface: observe a request, compress it (or say nobody did), decide from stated terms.

P2.11's bar asks that each compression state and each decision state be REACHABLE. A state a guard can
only produce by calling an internal function is a state no user ever meets, so all of them are reachable
here:

  POST /api/v1/horizon/observe     records what arrived, compresses it, decides, and stores the record.
                                   On this deployment the honest result is NOT_COMPRESSED with a reason
                                   and a decision of ESCALATE — the ordinary path, not an edge case.
  POST /api/v1/horizon/reflection  sets or CLEARS the user's own reflection tag. Users only.
  GET  /api/v1/horizon/records     the stored records, each with its compression state and its terms.
  GET  /api/v1/horizon/states      every state this kernel can report, and what produces each — so the
                                   surface states its own limits rather than leaving them implied.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.api._ai_provenance import ai_text
from agentic_core.auth.core import get_current_user
from agentic_core.horizon import kernel

router = APIRouter(prefix="/api/v1/horizon", tags=["horizon-membrane"])

_COMPRESS_PROMPT = (
    "Compress this request into its intent. Answer ONLY these lines, omitting any you cannot determine:\n"
    "asked_for: <what is being asked for>\n"
    "domain: <the subject domain>\n"
    "stakes: <what turns on this>\n"
    "missing: <inputs that are needed and absent, separated by semicolons>\n"
    "escalations: <anything that must be escalated, separated by semicolons>\n\n"
    "OMIT A LINE YOU CANNOT DETERMINE. Do not guess, and do not write what the person 'really' means.\n\n"
    "The request:\n")


class ObserveRequest(BaseModel):
    raw_text: str = Field(min_length=1)
    source: str = "user"
    surface: str = "api"


class ReflectionRequest(BaseModel):
    intent_id: str
    #  None CLEARS it. The user decides whether their own words are kept.
    text: Optional[str] = None


@router.post("/observe")
async def horizon_observe(req: ObserveRequest,
                          user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Observe, compress (three-state), decide from stated terms, store."""
    _uid = (user or {}).get("username") or "anonymous"
    obs = kernel.observe(req.source, req.raw_text, req.surface)

    text, prov, failed = "", {}, False
    try:
        text, prov = await ai_text(_COMPRESS_PROMPT + req.raw_text,
                                   agent="horizon_compress", owner_id=_uid, augment=False,
                                   user_text=(req.raw_text or None))   # W651 (FU-675)
        failed = not str(text or "").strip()
    except Exception as e:                       # noqa: BLE001 — a failed call is not a compression
        failed, text = True, ""
        prov = {"served_by": None, "is_external": False, "error": f"{e.__class__.__name__}: {e}"}

    rec = kernel.build_record(obs, prov.get("served_by"), bool(prov.get("is_external")), failed, text)
    dec = kernel.decide(rec)
    row = kernel.save(rec, dec)
    return {"observation": obs, "record": row, "decision": dec}


@router.post("/reflection")
async def horizon_reflection(req: ReflectionRequest,
                             user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Set or clear the user's own reflection tag — the WRITE route the Owner's ruling requires.

    Every sizing of this item budgeted a read route only, which is why the spec now says so in both
    places a builder reads. The identity is taken from the authenticated user and prefixed `user:`, so a
    caller cannot present itself as one: an AI-written value here would be the platform's account of the
    person replacing the person's own.
    """
    _name = (user or {}).get("username") or "anonymous"
    try:
        row = kernel.set_reflection_tag(req.intent_id, req.text, f"user:{_name}")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no intent record {req.intent_id}")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"intent_id": row["intent_id"], "reflection_tag": row["reflection_tag"],
            "reflection_tag_by": row["reflection_tag_by"], "basis": row["reflection_tag_basis"]}


@router.get("/records")
async def horizon_records(limit: int = 50,
                          user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    rows = kernel.listing(limit)
    _uncompressed = sum(1 for r in rows if r.get("compression") == kernel.NOT_COMPRESSED)
    #  W554 — HOW MANY OF THESE WERE OBSERVED RATHER THAN ACTED ON. Once the seam writes rows, the store
    #  holds decisions nothing enforced beside decisions a user asked for, and they look identical in a
    #  listing. An ESCALATE nobody acted on must not be countable as an escalation.
    _observed = sum(1 for r in rows if r.get("gated") is False)
    return {
        "records": rows,
        "total": len(rows),
        "not_compressed": _uncompressed,
        "observed_not_enforced": _observed,
        "history_cap": kernel._CAP,
        "basis": (f"{_uncompressed} of {len(rows)} record(s) were NOT compressed. That is the expected "
                  f"proportion on a deployment with no model provisioned, and it is reported rather than "
                  f"smoothed: a membrane that claimed to compress what it did not would make every "
                  f"decision below it rest on a sentence the platform invented. "
                  f"{_observed} of them were written by the OBSERVING SEAM and nothing acted on their "
                  f"decision — each carries gated=False with the reason, because an ESCALATE nobody "
                  f"enforced is not an escalation. The stored history is capped at {kernel._CAP} rows, "
                  f"oldest dropped first, so the earliest row here is not necessarily the first thing "
                  f"that ever happened"
                  if rows else
                  "no request has been observed yet, which is not the same as none having been refused"),
    }


class ScreenRequest(BaseModel):
    text: str = Field(min_length=1)


@router.post("/screen")
async def horizon_screen(req: ScreenRequest,
                         user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Run the three guardrails over a text and report every gate WITH WHAT IT DID NOT LOOK AT.

    P2.12's bar: each gate's stated limit is on the surface. A verdict without its coverage is the thing
    this item exists to prevent — a screen that reads as a clearance because nothing matched.
    """
    from agentic_core.gaas.v5 import horizon_guardrails as _g
    return _g.screen_all(req.text)


class ScheduleRequest(BaseModel):
    """The caller supplies BOTH the case's dates and the rules to apply, each with its own citation.

    The rules are an input on purpose: encoding them here would make this platform state what the law
    requires, which is legal advice in a data structure. It applies the rules it is given and names them.
    """
    events: dict = {}
    rules: list = []


@router.post("/simulation/schedule")
async def horizon_schedule(req: ScheduleRequest):
    """P3.24 stage 1 — a SCHEDULE computed from the caller's rules and the case's own dates.

    Every date carries the rule, the citation the caller gave, the event it counted from and the sum in
    words, so it can be checked by hand. A rule that cannot be computed is listed with the reason and never
    estimated. THIS IS NOT A FORECAST and nothing here predicts an outcome.
    """
    from agentic_core.simulation.staged import procedural_timeline
    return procedural_timeline(req.events, req.rules)


@router.get("/simulation/stage/{number}")
async def horizon_stage(number: int):
    """Any of the four stages. Stages 2 and 3 report NO INPUT with the reason; stage 4 is shadow-only."""
    from agentic_core.simulation.staged import stage
    return stage(number)


@router.post("/simulation/surface-stage-4")
async def horizon_surface_stage_4(reason: str = ""):
    """ALWAYS REFUSED, and served rather than absent so the refusal is discoverable.

    Clause (4) requires a guard that drives an attempt to surface stage 4 and sees it refused. A 404 would
    satisfy nobody: it teaches a caller that the feature is missing rather than that it is refused, and it
    gives no reason they could dispute.
    """
    from agentic_core.simulation.staged import surface_stage_4
    return surface_stage_4(reason)


@router.post("/simulation/forecast")
async def horizon_forecast():
    """There is no forecast, and asking gets a REASON instead of a 404.

    The Owner's October ruling (option (a)) is the frame and it is now spent: no outcome dataset exists
    here, no judge data, and a settlement range shown to someone in a live matter is a number they will act
    on however it is labelled. A later round may not reopen this on its own judgement.

    NO DATE IS WRITTEN HERE, and that is deliberate rather than vagueness. Three guards scan this file for
    any digit run a person in distress could read as a number to dial — the rule is
    `(?:\\+?\\d[\\d\\s().-]{6,}\\d)|(?:\\b\\d{4,}\\b)`, which an ISO date matches, and so does a bare year.
    A fabricated helpline is the one fabrication no later correction reaches, so the file carries no digit
    runs at all and the ruling's full identifier lives in the plan, which is its canonical home.
    """
    from agentic_core.simulation.staged import forecast
    return forecast()


class VerifyRequest(BaseModel):
    output: str = ""
    citations: list = []


@router.post("/verify")
async def horizon_verify(req: VerifyRequest):
    """P3.21 — run the three checkable checks over an output's citations, and WITHHOLD on any UNMET.

    Checkable checks only: does the citation resolve to a document in this repository, is the quoted text
    at the cited line, does the cited figure appear in that document. Each returns MET / UNMET /
    NOT ASSESSABLE with its basis, and an UNMET WITHHOLDS the output naming the check that failed.

    THERE IS NO CONFIDENCE SCORE in this path. The roadmap proposed withholding when "verifier confidence
    < 0.8"; a threshold over an invented number is a gate that cannot refuse, and this platform already
    carried three of those. NOT ASSESSABLE is neither a pass nor a failure - it is reported so a check that
    could not be run never reads as one that passed.
    """
    from agentic_core.horizon.verifier import verify as _verify
    return _verify(req.output, req.citations)


@router.get("/guardrails")
async def horizon_guardrails(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """The three gates, their coverage, and the distress route field SHOWN AS UNFILLED.

    The route field is the dangerous one. An unfilled list shown as unfilled is safe; a placeholder is
    not, because a person in distress might act on it. So the key is always present and what it carries
    is None with the reason — never a default, never a service name, never a number.
    """
    from agentic_core.gaas.v5 import horizon_guardrails as _g
    _rt = _g.distress_routes()
    return {
        "gates": [
            {"gate": "religious_ruling",
             "refuses": "issuing a religious ruling; refers to a qualified human scholar",
             "limit": _g._COVERAGE,
             "certifies_absence": False},
            {"gate": "theological_proof",
             "refuses": "a claim that science proves or disproves a theological truth, in either direction",
             "limit": _g._COVERAGE,
             "certifies_absence": False},
            {"gate": "clinical_care",
             "refuses": ("giving counsel to someone in distress; states plainly that the platform is not "
                         "a person and shows the human route"),
             "limit": _g._COVERAGE,
             "certifies_absence": False},
        ],
        #  READ THROUGH THE VALIDATOR, NOT AROUND IT. This read `_g.DISTRESS_ROUTES` raw, so it would
        #  have published a record that `accept_route` refuses — one with no reviewer, no check date or
        #  no jurisdiction — and it could not tell a FRESH route from one nobody has checked in years.
        #  The gate on the same path already reads it this way; a second reader going round the back is
        #  how the same field comes to say two different things.
        **{"distress_routes": _rt["routes"],
           "distress_routes_supplied": _rt["routes"] is not None,
           "distress_routes_basis": _rt["basis"],
           "distress_routes_state": _rt["state"],
           "distress_routes_stale_count": _rt["stale_count"],
           "distress_routes_jurisdictions": _rt["jurisdictions"],
           "distress_routes_cover_anywhere": _rt["covers_anywhere"],
           "distress_routes_refused": _rt["refused"]},
        "not_a_person_statement": _g.NOT_A_PERSON,
        "escalation_defaults_on_when_undecidable": True,
        "basis": ("every gate reports a verdict AND what it did not look at. NONE OF THEM CAN CERTIFY AN "
                  "ABSENCE: each is an English phrase screen, so a non-match means its own patterns found "
                  "nothing rather than that the subject was not there. Where a screen cannot run at all "
                  "the escalation defaults ON, because a screen that did not run is not a screen that "
                  "passed"),
        "unchanged_refusals": [
            "Quran Arabic is never generated",
            "Quranic text comes only from quran.com, alquran.cloud or tanzil.net, with provenance",
            "recitation is never scored",
            "AI content is labelled",
            ("Ruling A.9.5 stands - the Fitrah Spectrum is never a measurement and no AI verdict is "
             "passed on a person's spiritual state"),
        ],
    }


@router.post("/archive/scan")
async def horizon_archive_scan(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Index the explicit inbox. Three states per file, the counts published, the bounds stated."""
    from agentic_core.horizon import archive
    return archive.scan()


@router.get("/archive")
async def horizon_archive(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """The manifest WITH a re-count of its own file list beside its published counts.

    P2.13's bar: the manifest's counts match a re-count. A count written beside the thing it counts is a
    claim; a count derived again from the list is a check, so both travel together and a reader does not
    have to take either on trust.
    """
    from agentic_core.horizon import archive
    _m = archive._read_index().get("manifest") or {}
    return {"manifest": _m, "recount": archive.recount()}


@router.get("/archive/search")
async def horizon_archive_search(term: str, limit: int = 20,
                                 user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Exact lexical search over the INDEXED files only, naming what it could not look inside."""
    from agentic_core.horizon import archive
    return archive.search(term, limit)


@router.get("/states")
async def horizon_states(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Every state this kernel can report and what produces it — the limits, stated not implied."""
    return {
        "compression_states": {
            kernel.COMPRESSED: ("a model served the compression and the record names which. Requires a "
                                "provisioned model; none is provisioned on this deployment"),
            kernel.NOT_COMPRESSED: ("nobody compressed the request, with the reason. THE ORDINARY PATH "
                                    "here: the deterministic floor composes structured output from the "
                                    "request and infers nothing, so a floor-served run has compressed "
                                    "nothing"),
        },
        "decision_states": {
            kernel.PROCEED: "no stated term fired",
            kernel.ESCALATE: "one or more stated terms fired; the record names which",
            kernel.NOT_ASSESSABLE: ("the record could not be read, so no term could be evaluated. This "
                                    "is not a quiet PROCEED"),
        },
        #  W554 — THE FOUR REASONS A RECORD IS NOT COMPRESSED, each a different fact. One sentence
        #  covering all of them would attribute the absence to whichever component the sentence named.
        "not_compressed_reasons": {
            "no_compressor_was_called": ("the OBSERVING SEAM wrote this record. No model was asked what "
                                        "the request meant, because a model call in front of every "
                                        "domain request would make each one wait on an LLM"),
            "served_by_a_non_compressor": ("a call was made and the deterministic floor (or a template) "
                                           "served it. It composes structured output from the request "
                                           "and infers nothing. THE ORDINARY PATH for /observe here"),
            "the_call_produced_no_text": "a call was made and came back empty, or raised",
            "compressed": ("not a reason — listed for contrast: a model served the compression and the "
                           "record names which one"),
        },
        "escalation_domains": list(kernel.ESCALATION_DOMAINS),
        "compression_fields": list(kernel._COMPRESSION_FIELDS),
        "no_blended_score": True,
        "basis": ("there is no score anywhere in this kernel. Three of the four terms the Owner's brief "
                  "wanted to blend have no instrument in this repository, and averaging an instrument "
                  "that does not exist with one that does produces a figure whose provenance nobody can "
                  "state. Each term is reported separately with its own basis, including the terms that "
                  "could not be evaluated — a term with no instrument is not a term that passed"),
        "reflection_tag": ("the user's own words, optional, user-set and user-cleared. No AI, agent or "
                           "engine may write it: the write route refuses an identity that does not name "
                           "a user"),
        "seam": "see GET /api/v1/horizon/seam — it observes and records; it does not gate",
    }


class LessonRequest(BaseModel):
    trigger: str = Field(description="raised_handler | refused_gate | owner_correction")
    evidence: Dict[str, Any] = Field(default_factory=dict)
    subject: Optional[str] = None
    disposition: str = Field(default="APPLIED_AND_LOGGED")
    candidate_cause: Optional[str] = None
    cause_basis: Optional[str] = None
    proposed_change: Optional[str] = None
    title: Optional[str] = None


@router.post("/lessons")
async def horizon_lesson(req: LessonRequest,
                         user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Write a LessonRecord, route it, and FILE IT THROUGH THE AGENCY if its disposition files a change.

    The three steps stay separate on purpose — observe, route, enact — because collapsing any two of them
    is how an observation becomes an unreviewed change. The refusal that matters is enforced here: a
    SUBMIT_ONLY lesson is submitted and NOT applied, and the response says so in the field a caller reads
    rather than only in prose.
    """
    from agentic_core.horizon import muhasabah

    _uid = (user or {}).get("username") or "system"
    rec = muhasabah.observe(req.trigger, req.evidence, subject=req.subject,
                            candidate_cause=req.candidate_cause, cause_basis=req.cause_basis,
                            proposed_change=req.proposed_change)
    routing = muhasabah.route(rec, req.disposition)
    may_apply, apply_basis = muhasabah.may_self_apply(routing)

    filed = None
    file_error = None
    if routing.get("files_change"):
        #  ONE REGISTER: the same submit_change every other governed change goes through. A second
        #  approval path here would be the fork this item's bar forbids.
        from agentic_core.api.change_control import SubmitChangeRequest, submit_change
        try:
            filed = await submit_change(SubmitChangeRequest(
                title=(req.title or f"[horizon] lesson from {rec['trigger']}")[:200],
                change_type=routing["change_type"],
                description=(req.proposed_change or "")
                or f"A lesson recorded by Horizon from {rec['trigger']}. Evidence: {rec['evidence']}",
                rationale=(f"candidate cause: {rec['candidate_cause']}"
                           + (f" — basis: {rec['cause_basis']}" if rec.get("cause_basis") else
                              ". Nothing in this repository infers a root cause, so none is asserted.")),
                submitted_by=f"horizon:{_uid}",
            ), principal=f"horizon:{_uid}")
        except HTTPException as e:               # a refusal by the Agency is an OUTCOME, not a crash
            file_error = {"status": e.status_code, "detail": e.detail}
        except Exception as e:                   # noqa: BLE001
            file_error = {"status": None, "detail": f"{e.__class__.__name__}: {e}"}

    row = muhasabah.save(rec, routing, filed if isinstance(filed, dict) else None)
    return {
        "lesson": row,
        "routing": routing,
        "may_self_apply": may_apply,
        "may_self_apply_basis": apply_basis,
        "filed": filed,
        "file_error": file_error,
        "file_error_basis": (
            "the Change Control Agency REFUSED this filing, and that refusal is an outcome rather than an "
            "error in Horizon: the lesson is kept with the refusal recorded on it" if file_error else None),
    }


@router.get("/lessons")
async def horizon_lessons(limit: int = 50,
                          user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    from agentic_core.horizon import muhasabah
    rows = muhasabah.listing(limit)
    _filed = sum(1 for r in rows if isinstance(r.get("filed"), dict) and r["filed"].get("cca_id"))
    _board = sum(1 for r in rows if r.get("reaches_board"))
    return {
        "lessons": rows,
        "total": len(rows),
        "filed_with_the_agency": _filed,
        "reaching_the_board": _board,
        "basis": (
            f"{_filed} of {len(rows)} lesson(s) were filed as a change with the Change Control Agency, and "
            f"{_board} of them reach the Board. THE DIFFERENCE IS THE POINT: a config_minor filing is "
            f"reviewable after the fact and never reaches the Board, so a count of filings is not a count "
            f"of escalations" if rows else
            "no lesson has been recorded yet, which is not the same as no friction having occurred"),
        "states": muhasabah.states(),
    }


class OwnerFieldRequest(BaseModel):
    consumption_id: str
    field: str = Field(description="used_well | what_was_formed")
    text: Optional[str] = None       # None or "" CLEARS it back to unfilled


@router.get("/consumption")
async def horizon_consumption(limit: int = 50,
                              user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """What runs consumed, with WHAT MEASURED each figure — or that nothing did."""
    from agentic_core.horizon import consumption
    rows = consumption.listing(limit)
    _fields = len(consumption.FIELDS)
    _measured = sum(1 for r in rows for f in consumption.FIELDS
                    if isinstance(r.get(f), dict) and r[f].get("measured"))
    _filled = sum(1 for r in rows for f in consumption.OWNER_FIELDS if r.get(f))
    return {
        "records": rows,
        "total": len(rows),
        "measured_fields": _measured,
        "possible_fields": len(rows) * _fields,
        "owner_fields_filled": _filled,
        "basis": (
            f"{_measured} of {len(rows) * _fields} computed field(s) across {len(rows)} record(s) were "
            f"measured; the rest name what did not measure them rather than reporting zero. A MEASURED "
            f"ZERO AND AN UNMEASURED FIELD ARE DIFFERENT STATES and are reported differently — calls=0 "
            f"is a run whose provenance map was present and empty, calls=null is a run nothing "
            f"instrumented. {_filled} Owner field(s) are filled; the rest are the Owner's to write and "
            f"are computed by nothing"
            if rows else
            "no run has been accounted for yet, which is not the same as no run having happened"),
        "states": consumption.states(),
    }


@router.post("/consumption/owner-field")
async def horizon_consumption_owner_field(req: OwnerFieldRequest,
                                          user: dict | None = Depends(get_current_user)
                                          ) -> Dict[str, Any]:
    """Set or CLEAR one of the Owner's own fields. USERS ONLY.

    The identity check is the same one the reflection tag uses and for the same reason: a value written
    here by an agent would be the platform's account of what a person formed, asserted in their field.
    """
    from agentic_core.horizon import consumption
    _uid = (user or {}).get("username")
    res = consumption.set_owner_field(req.consumption_id, req.field, req.text,
                                      f"user:{_uid}" if _uid else "anonymous")
    if not res.get("ok"):
        raise HTTPException(status_code=422, detail=res.get("reason"))
    return res


@router.get("/seam")
async def horizon_seam(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """What the Horizon seam watches, what it EXCLUDES, and what it has recorded (W554, P2.11).

    The seam is the item body's own sentence made real: a middleware in front of the domain routes plus a
    hook where the run paths already call operational_excellence.record_outcome. This route exists because
    a limit a user cannot read is a limit only its author knows — the excluded methods and the excluded
    run kind are reported here with their reasons, beside the counts of what was observed.

    IT DOES NOT GATE, and that is the first field. A stored ESCALATE that nothing acted on is the most
    misleading row this store can hold, so every row the seam writes carries gated=False with the reason.
    """
    from agentic_core.horizon import membrane
    return membrane.report()
