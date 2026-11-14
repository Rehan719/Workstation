"""WHO ANSWERS WHEN AN AUTONOMOUS ENTITY IS WRONG (P5.3) - part 1: a claim against a deliverable, recorded with what
the deliverable was, filed with Change Control at a tier only a person decides, logged to the UEG, and OPEN until a
person answers it.

OWNER RULING 2026-09-27 (P5.3): a tenant raises that an output is wrong; the claim is recorded against the artefact
with its provenance; it routes to the arms-length agency (Change Control) the way every other change does; and its
resolution is UEG-logged. ACCEPT: a raised claim reaches a named owner through an executing path (not a comment); the
artefact's provenance is part of the record; the UEG entry is hash-chained like the rest; and a claim nobody has
answered is visible as OPEN, never closed by a timer.

    POST /api/v1/support/claims         raise a claim against one of the caller's deliverables, or (W964) an answer
    GET  /api/v1/support/claims         every claim the caller may read, each OPEN or ANSWERED as Change Control says
    GET  /api/v1/support/claims/{id}    one claim, with the change it was filed as

- The claim keeps what the deliverable was when it was raised: its title, entity, type and version, what served it
  (ai_provenance), its quality gate and compliance verdict, and the sha256 of its text.
- It is filed with Change Control as a support_claim, which is CRITICAL there: never decided by a model's review or
  the health rule, held until a person's explicit decision. Which tier a claim is filed under is the Owner's to rule;
  it is put to the Owner with this recommendation (an OWNER DECISION row).
- Its named owner is the one the entity's record names; with sign-in off, the Owner answers every claim.
- support.claim_raised is attested and appended to the UEG, hash-chained like every entry, and the answer says
  whether it reached the ledger.
- Its state is read from the change on every read: OPEN until a person approves or rejects the change, then ANSWERED
  with that decision. Nothing reads the clock to change it.
Claims raised by anyone but the Owner wait for sign-in (P4.1); so does accepting a delivery (FU-1003).

W964 (FU-1190, P5.20 clause 6) - A CLAIM AGAINST AN ANSWER THAT WAS NEVER SAVED. Until now a claim named only a saved
deliverable, so an answer a domain tool gave (a Law research answer, a Care draft) had no way to reach a person. A
claim may now name an answer: artefact_kind "answer", artefact_id the sha256 of its text as it was shown (computed
where it was shown), the endpoint that gave it, and what served it as the answer said. This platform keeps no answer
it was not asked to save, so the text is never sent and never kept (P5.12's boundary): the claim holds the tool
declared at that endpoint (review_options.tool_at, the declaration every domain route carries), the fingerprint, and
what the page reported. An endpoint that declares no tool is refused, so a claim always names a real tool. An answer
belongs to no entity: with sign-in off the Owner answers it, and with sign-in on an administrator does.
"""
from __future__ import annotations

import hashlib
import re
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from agentic_core.auth.core import get_current_user, user_can_access

router = APIRouter(prefix="/api/v1/support", tags=["support-claims"])

STORE = "support_claims.json"
ARTEFACT_KINDS = ("deliverable", "answer")
#  W964 - an answer is named by the sha256 of its text as it was shown; the text is never sent
ANSWER_SHA256 = re.compile(r"^[0-9a-f]{64}$")
SERVED_BY_MOST = 120
ANSWER_BASIS = ("This platform keeps no answer it was not asked to save, so this claim holds what the page reported: "
                "the route that gave the answer and the tool declared there, what served it as the answer said, and "
                "the sha256 of its text as it was shown, computed where it was shown. The text itself was never sent "
                "and is not kept; whoever answers the claim matches it against a copy by that fingerprint.")
CLAIM_CHANGE_TYPE = "support_claim"
BASIS = ("A claim is OPEN until a person decides the change it was filed as, and then ANSWERED with that decision; "
         "its state is read from Change Control on every read and nothing reads the clock to change it.")


class ClaimRequest(BaseModel):
    model_config = {"extra": "forbid"}
    artefact_kind: str
    artefact_id: str
    what_is_wrong: str
    #  W964 - an answer's claim only: the route that gave it, and what served it as the answer said
    endpoint: Optional[str] = None
    served_by: Optional[str] = None


def _path():
    from agentic_core.config import data_path
    return data_path(STORE)


def _read() -> List[Dict[str, Any]]:
    p = _path()
    if not p.exists():
        return []
    from agentic_core.config import read_json_strict
    try:
        data = read_json_strict(p, list, expect=list)
    except Exception as e:                              # noqa: BLE001 - said, never read as "no claims"
        raise HTTPException(status_code=503, detail=(
            f"The claims could not be read ({type(e).__name__}), so none is shown and none is raised."))
    return [c for c in (data or []) if isinstance(c, dict)]


def _who(user: Any) -> str:
    return (user.get("username") if isinstance(user, dict) else None) or "single-user-mode"


def _deliverable(artefact_id: str, user: Any) -> Dict[str, Any]:
    from agentic_core.api import deliverables as _dl
    u = user if isinstance(user, dict) else None
    for d in _dl._load():
        if d.get("id") == artefact_id and user_can_access(u, d.get("owner_id")):
            return d
    raise HTTPException(status_code=404, detail=f"Deliverable {artefact_id} not found, so no claim is raised against it.")


def _named_owner(d: Dict[str, Any]) -> Dict[str, Any]:
    """Who answers the claim: the owner the entity's record names; with sign-in off, the Owner."""
    from agentic_core.auth.core import auth_enabled
    owner = None
    try:
        from agentic_core.api.vsb import _load_vsb
        owner = (_load_vsb(d.get("vsb_id")) or {}).get("owner_id") if d.get("vsb_id") else None
    except Exception:                                   # noqa: BLE001 - an unreadable record names nobody
        owner = None
    owner = owner or d.get("owner_id")
    if not auth_enabled():
        return {"owner": owner or "the Owner", "basis": (
            "sign-in is off, so the Owner answers every claim; the owner shown is the one the entity's record names")}
    if owner:
        return {"owner": owner, "basis": "the owner the entity's record names"}
    return {"owner": None, "basis": "the entity's record names no owner, so an administrator answers the claim"}


def _answer(req: ClaimRequest, request: Request) -> Dict[str, Any]:
    """W964 - what a claim against an answer holds: the tool declared at the endpoint that gave it, what served it as
    the answer said, and the fingerprint of its text. Refused when the fingerprint is not a sha256 or the endpoint
    declares no tool."""
    sha = str(req.artefact_id or "").strip()
    if not ANSWER_SHA256.match(sha):
        raise HTTPException(status_code=422, detail=(
            "Not raised: an answer is named by the sha256 of its text as it was shown, 64 lowercase hexadecimal "
            "characters; its text is never sent."))
    endpoint = str(req.endpoint or "").strip()
    from agentic_core.api.review_options import tool_at
    tool = tool_at(request.app, endpoint) if endpoint else None
    if not tool:
        raise HTTPException(status_code=422, detail=(
            f"Not raised: no tool is declared at '{endpoint}', so the answer cannot be placed. A claim against an "
            "answer names the route that gave it."))
    served = str(req.served_by or "").strip()
    if len(served) > SERVED_BY_MOST:
        raise HTTPException(status_code=422, detail=(
            f"Not raised: what served the answer is said in at most {SERVED_BY_MOST} characters, as the answer said it."))
    return {"endpoint": endpoint, "tool": tool, "served_by_as_reported": served or None, "content_sha256": sha,
            "text_kept": False, "basis": ANSWER_BASIS}


def _answer_owner() -> Dict[str, Any]:
    """Who answers a claim against an answer: it belongs to no entity, so the Owner with sign-in off, and an
    administrator with it on."""
    from agentic_core.auth.core import auth_enabled
    if not auth_enabled():
        return {"owner": "the Owner", "basis": "sign-in is off, so the Owner answers every claim; an answer belongs to no entity"}
    return {"owner": None, "basis": "an answer belongs to no entity and names no owner, so an administrator answers the claim"}


def _state(claim: Dict[str, Any]) -> Dict[str, Any]:
    """OPEN or ANSWERED, read from the change the claim was filed as - never from the clock."""
    from agentic_core.api.change_control import _load_change, effective_tier
    change = _load_change(str(claim.get("cca_id") or ""))
    if change is None:
        return {"state": "OPEN", "change": None, "state_basis": (
            "the change this claim was filed as could not be read, so it is not known to be answered; it is OPEN")}
    status = change.get("status") or "submitted"
    summary = {"cca_id": change.get("cca_id"), "status": status, "impact_tier": effective_tier(change),
               "decision_source": change.get("decision_source")}
    if status in ("approved", "rejected", "implemented"):
        #  W942 - whether the decision reached the ledger, read from the change's own audit trail (Change Control
        #  writes every decision to the constitutional ledger and marks the record whether or not it got there)
        logged = [e for e in (change.get("audit_trail") or []) if isinstance(e, dict) and e.get("event") == "ueg_written"
                  and str(e.get("event_type") or "").startswith("cca.change_")]
        return {"state": "ANSWERED", "decision": status, "change": summary, "state_basis": (
            f"a person decided the change this claim was filed as: {status}"),
            "answer_logged": bool(logged), "answer_logged_basis": (
                f"the decision is in the constitutional ledger as {logged[-1]['event_type']}" if logged else
                "the decision has no ledger entry on the change's record, so this answer is not logged; Change "
                "Control marks such a gap for reconciliation")}
    return {"state": "OPEN", "change": summary, "state_basis": (
        f"the change is {status} and no person has decided it; a claim nobody has answered stays OPEN")}


def _may_read(claim: Dict[str, Any], user: Any) -> bool:
    from agentic_core.auth.core import auth_enabled
    if not auth_enabled():
        return True
    u = user if isinstance(user, dict) else None
    if u and (u.get("role") == "admin" or u.get("username") == claim.get("raised_by")):
        return True
    return bool(u) and user_can_access(u, (claim.get("named_owner") or {}).get("owner"))


@router.post("/claims")
async def raise_claim(req: ClaimRequest, request: Request, user: dict | None = Depends(get_current_user)):
    """Raise a claim that one of the caller's deliverables, or an answer the caller was shown, is wrong. Refused, with
    nothing written, when the artefact is neither, the claim says nothing of what is wrong, the deliverable is not the
    caller's, or the answer is not named by its fingerprint and the route that gave it."""
    kind, wrong = str(req.artefact_kind or "").strip(), str(req.what_is_wrong or "").strip()
    if kind not in ARTEFACT_KINDS:
        raise HTTPException(status_code=422, detail=(
            f"Not raised: a claim is raised against a deliverable or an answer, and '{kind}' is neither."))
    if not wrong:
        raise HTTPException(status_code=422, detail="Not raised: a claim says what is wrong.")
    if kind == "answer":
        artefact = _answer(req, request)
        artefact_id, owner, vsb_id = artefact["content_sha256"], _answer_owner(), None
        title = f"[support claim] an answer from {artefact['tool']}"
        description = f"A claim that an answer from {artefact['tool']} ({artefact['endpoint']}) is wrong: {wrong}"
        affected = [f"answer:{artefact['tool']}:{artefact_id[:12]}"]
    else:
        if req.endpoint is not None or req.served_by is not None:
            raise HTTPException(status_code=422, detail=(
                "Not raised: an endpoint and what served it name an answer; a deliverable is named by its id alone."))
        d = _deliverable(str(req.artefact_id or "").strip(), user)
        q = ((d.get("quality_assurance") or {}).get("quality") or {})
        artefact = {"title": d.get("title"), "vsb_id": d.get("vsb_id"), "type": d.get("type"),
                    "version": len(d.get("versions") or []) or 1, "ai_provenance": d.get("ai_provenance"),
                    "qms_gate_passed": q.get("qms_gate_passed"), "compliance_overall": (q.get("compliance") or {}).get("overall"),
                    "content_sha256": hashlib.sha256(str(d.get("content") or "").encode("utf-8")).hexdigest()}
        artefact_id, owner, vsb_id = d["id"], _named_owner(d), d.get("vsb_id")
        title = f"[support claim] {d.get('title') or d['id']}"
        description = f"A claim that deliverable {d['id']} is wrong: {wrong}"
        affected = [f"deliverable:{d['id']}"]
    _read()                                              # an unreadable store refuses before anything is filed
    raiser = _who(user)
    from agentic_core.api.change_control import SubmitChangeRequest, submit_change
    filed = await submit_change(SubmitChangeRequest(
        title=title[:200], change_type=CLAIM_CHANGE_TYPE, description=description, rationale=wrong,
        affected_systems=affected, submitted_by=raiser, vsb_id=vsb_id), principal=raiser)
    claim = {"claim_id": f"claim-{uuid.uuid4().hex[:10]}", "artefact_kind": kind, "artefact_id": artefact_id,
             "what_is_wrong": wrong, "raised_by": raiser, "raised_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "named_owner": owner, "artefact": artefact, "cca_id": filed.get("cca_id")}
    from agentic_core.api.support import _attest_and_log
    ueg = await _attest_and_log("claim_raised", {"claim_id": claim["claim_id"], "artefact_kind": kind, "artefact_id": artefact_id, "cca_id": claim["cca_id"], "content_sha256": artefact["content_sha256"], "named_owner": owner["owner"]}, actor=raiser)
    claim["ueg"] = {"recorded": bool(ueg.get("recorded")), "entry": ueg.get("ledger_entry"), "basis": ueg.get("basis")}
    from agentic_core.config import mutate_json

    def _add(existing):
        rows = existing if isinstance(existing, list) else []
        rows.append(claim)
        return rows
    mutate_json(_path(), _add, list)
    return {**claim, **_state(claim), "basis": BASIS}


@router.get("/claims")
async def list_claims(user: dict | None = Depends(get_current_user)):
    rows = [{**c, **_state(c)} for c in _read() if _may_read(c, user)]
    return {"claims": rows[::-1], "open": sum(1 for c in rows if c["state"] == "OPEN"), "basis": BASIS}


@router.get("/claims/{claim_id}")
async def get_claim(claim_id: str, user: dict | None = Depends(get_current_user)):
    for c in _read():
        if c.get("claim_id") == claim_id and _may_read(c, user):
            return {**c, **_state(c), "basis": BASIS}
    raise HTTPException(status_code=404, detail=f"Claim {claim_id} not found.")
