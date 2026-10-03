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
                                   agent="horizon_compress", owner_id=_uid, augment=False)
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
    return {
        "records": rows,
        "total": len(rows),
        "not_compressed": _uncompressed,
        "basis": (f"{_uncompressed} of {len(rows)} record(s) were NOT compressed. That is the expected "
                  f"proportion on a deployment with no model provisioned, and it is reported rather than "
                  f"smoothed: a membrane that claimed to compress what it did not would make every "
                  f"decision below it rest on a sentence the platform invented"
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


@router.get("/guardrails")
async def horizon_guardrails(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """The three gates, their coverage, and the distress route field SHOWN AS UNFILLED.

    The route field is the dangerous one. An unfilled list shown as unfilled is safe; a placeholder is
    not, because a person in distress might act on it. So the key is always present and what it carries
    is None with the reason — never a default, never a service name, never a number.
    """
    from agentic_core.gaas.v5 import horizon_guardrails as _g
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
        "distress_routes": list(_g.DISTRESS_ROUTES) or None,
        "distress_routes_supplied": bool(_g.DISTRESS_ROUTES),
        "distress_routes_basis": _g.DISTRESS_ROUTES_BASIS,
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
    }
