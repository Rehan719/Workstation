"""Autonomous technical support, told truthfully (P3.18).

The archived version of this surface slept a tier-shaped latency and returned a formatted string
announcing a simulated resolution of whatever was asked, with a confidence of 0.96 and success=True
always. Nothing here sleeps, nothing reports a
confidence, and nothing resolves itself.

THREE ROUTES AND WHAT EACH REFUSES TO CLAIM:
  POST /api/v1/support/ask      answers a question and records WHAT SERVED IT. A failed call is recorded as
                                failed and is never returned as an answer. The latency is the measured
                                duration of the call, because the archived agent's tier difference was a
                                sleep.
  POST /api/v1/support/confirm  the ONLY way `resolved` is ever written. A caller cannot confirm on the
                                platform's behalf without saying who confirmed.
  GET  /api/v1/support/sla      the resolution rate over CONFIRMED records only, three-state when none are
                                confirmed. The archived monitor computed 100% by dividing over invented
                                tickets whose success field was a literal; this one has no numerator unless
                                somebody actually said so.

SUPPORT LOGIC CHANGES GO THROUGH THE EXISTING CHANGE CONTROL AGENCY. There is deliberately no gate, no
approval field and no second governance path in this module: the item's body forbids one, and a governance
path invented here would be exactly the "second governance" it names.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.api._ai_provenance import ai_text
from agentic_core.attestation import attest
from agentic_core.auth.core import get_current_user
from agentic_core.support import tickets
from agentic_core.ueg.registry import ueg_ledger

router = APIRouter(prefix="/api/v1/support", tags=["autonomous-support"])

#  The next step a ticket carries when its answer did not come through. "Not resolved" is never the end of
#  the record — the item's body requires an unresolved ticket to state what happens next.
_ESCALATION = ("escalated: a human reviewer picks this up. The platform did not answer, so nothing here "
               "claims it did")


async def _attest_and_log(event: str, payload: Dict[str, Any], actor: str) -> Dict[str, Any]:
    """Attest a ticket event and append it to the UEG — and REPORT a failed append rather than assume it.

    The attestation is P3.15's real one (a keyed MAC over canonical bytes, with a named key source), not a
    literal string standing in for a signature. The honesty rule here is the same one the rest of this
    package is built on: an event that did NOT reach the ledger must not render as one that did, exactly as
    an unconfirmed ticket must not render as a resolved one. So the append is reported three ways — recorded
    with an entry, or not recorded with the reason — and the caller is never left to infer which.
    """
    att = attest(payload)
    try:
        entry = await ueg_ledger.log_event(f"support.{event}", {**payload, "attestation": att}, actor=actor)
        #  BOTH RETURNS CARRY THE SAME KEYS. A success branch that omitted `basis` would hand every reader
        #  a key that exists only on failure, so the page would read undefined on the normal path and the
        #  one branch a reader most needs to render would be the one it had no field for.
        #  AND THE BASIS READS THE ATTESTATION'S OWN STATE rather than asserting a property of it. This
        #  deployment configures no attestation key, so what gets appended is an unsigned digest: it still
        #  detects alteration, but it establishes no signer. Calling that "re-verifiable" would be a basis
        #  string claiming a guarantee the state does not supply — the defect class this whole item is about.
        return {"attestation": att, "ledger_entry": entry, "recorded": True,
                "basis": (f"appended to the ledger as support.{event}; the attestation is "
                          + ("signed, so it can be recomputed and attributed to its key"
                             if att.get("signed") else
                             f"an UNSIGNED digest ({att.get('key_source')}), so an altered record is "
                             f"detectable but no signer is established"))}
    except Exception as e:                       # noqa: BLE001 — the ledger's state is part of the answer
        return {"attestation": att, "ledger_entry": None, "recorded": False,
                "basis": (f"NOT RECORDED in the ledger ({e.__class__.__name__}: {e}). The attestation above "
                          f"is real and re-verifiable, but nothing was appended, so do not read this event "
                          f"as logged")}


class AskRequest(BaseModel):
    query: str = Field(min_length=1)
    tier: str = "standard"


class ConfirmRequest(BaseModel):
    ticket_id: str
    resolved: bool
    by: str = ""


class PolicyChangeRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    rationale: str = ""
    rollback_plan: str = ""


@router.post("/ask")
async def support_ask(req: AskRequest, user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Answer a support question, recording what served it and how long it really took."""
    _uid = (user or {}).get("username") or "anonymous"
    t = tickets.create_ticket(_uid, req.query, req.tier)

    started = time.monotonic()
    text, prov, failed = "", {}, False
    try:
        text, prov = await ai_text(
            f"A user of this platform asks for technical support:\n\n{req.query}\n\n"
            f"Answer plainly. If you do not know, say so and say what would establish it.",
            agent="support_answer", owner_id=_uid, augment=False)
        #  An empty completion is NOT an answer. The archived agent returned a formatted string whatever
        #  happened, which is why its success field could be a literal.
        failed = not str(text or "").strip()
    except Exception as e:                       # noqa: BLE001 — recorded as a failure, never as an answer
        failed, text = True, ""
        prov = {"served_by": None, "is_external": False, "error": f"{e.__class__.__name__}: {e}"}
    latency_ms = (time.monotonic() - started) * 1000.0

    next_step = _ESCALATION if failed else "confirm whether this resolved it, or reply with what still fails"
    rec = tickets.record_answer(t["id"], text if not failed else "", prov.get("served_by"),
                                bool(prov.get("is_external")), failed, latency_ms, next_step)
    _ledger = await _attest_and_log("answered", {
        "ticket_id": t["id"], "user_id": _uid, "served_by": prov.get("served_by"),
        "is_external": bool(prov.get("is_external")), "failed": failed,
        "latency_ms": round(latency_ms, 1),
        #  The ANSWER is not attested — its provenance and the ticket's outcome are. Attesting the text
        #  would make the ledger a second copy of the answer, and P3.19's rule against a second store of
        #  numbers has the same root: one place holds a fact, and everything else points at it.
        "resolved": None}, _uid)

    return {
        "ticket_id": t["id"],
        #  None rather than "" when the call failed: an absent answer and an empty answer read the same to a
        #  page, and only one of them is a failure.
        "answer": (rec["answer"]["text"] or None) if not failed else None,
        "answered": not failed,
        "provenance": {k: rec["answer"][k] for k in ("served_by", "is_external", "failed",
                                                     "latency_ms", "provenance_basis")},
        "resolved": None,
        "resolved_basis": ("NOT RESOLVED and not unresolved: resolving is recorded only from a confirmation, "
                           "so an answer alone never sets it. Post to /api/v1/support/confirm to record one"),
        "next_step": next_step,
        "escalated": failed,
        "ledger": _ledger,
    }


@router.post("/confirm")
async def support_confirm(req: ConfirmRequest,
                          user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Record a confirmation — the only writer of `resolved`."""
    _by = req.by.strip() or f"user:{(user or {}).get('username') or 'anonymous'}"
    try:
        rec = tickets.confirm(req.ticket_id, req.resolved, _by)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no ticket {req.ticket_id}")
    _ledger = await _attest_and_log("confirmed", {
        "ticket_id": rec["id"], "confirmed": rec["confirmed"], "confirmed_by": rec["confirmed_by"]}, _by)
    return {"ticket_id": rec["id"], "confirmed": rec["confirmed"], "confirmed_by": rec["confirmed_by"],
            "ledger": _ledger,
            "basis": ("recorded from a confirmation naming its source. Nothing on this platform confirms a "
                      "resolution on a user's behalf")}


@router.post("/policy-change")
async def support_policy_change(req: PolicyChangeRequest,
                                user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """File a change to support logic with the EXISTING Change Control Agency, and decide nothing here.

    The item's body requires support logic changes to go through the Change Control Agency rather than a
    second governance path. That rules out two things, not one: this module must not invent an approver,
    AND it must not leave support changes ungoverned, which is what having no filing surface at all would
    do. So this calls the same `submit_change` core the homeostasis regulator, the compliance screen and
    the evolution gate already call, and returns the CCA's own identifier and status untouched.

    `decided` is a constant False with a reason, because the only honest thing this route can say about the
    outcome is that the outcome is not its to report. A filing that rendered as an approval would be the
    second governance path the body forbids, built by accident.
    """
    from agentic_core.api.change_control import SubmitChangeRequest, submit_change
    _by = (user or {}).get("username") or "anonymous"
    #  Not swallowed: the one existing in-process caller wraps this in `except Exception: pass`, which
    #  means a change that was never filed is indistinguishable from one that was. An HTTPException from
    #  the Agency (a reserved title, an unappliable config) is the Agency's answer and belongs to the
    #  caller, so it propagates.
    change = await submit_change(SubmitChangeRequest(
        title=req.title,
        #  code_change is HIGH in the Agency's own tier map (Owner ruling FU-014). The tier is READ from
        #  the record below rather than asserted here, so a change to that map cannot be contradicted by
        #  a figure this module remembers.
        change_type="code_change",
        description=req.description,
        rationale=req.rationale,
        affected_systems=["agentic_core/support"],
        submitted_by=f"support:{_by}",
        rollback_plan=req.rollback_plan,
    ), principal=_by if user else None)
    return {
        "cca_id": change["cca_id"],
        "status": change["status"],
        "impact_tier": change["impact_tier"],
        "decided": False,
        #  NO SUPPORT-SIDE LEDGER ENTRY FOR THIS EVENT, deliberately. The Agency logs its own filing to the
        #  UEG and reports whether that append succeeded, so support re-logging it would put two records of
        #  one filing in the ledger and make a reader ask which is authoritative. The ticket events above
        #  have no other owner, which is why they carry their own. What travels here is the Agency's answer.
        "ledger_logged_by_the_agency": change.get("ueg_logged"),
        "basis": ("filed with the existing Change Control Agency under its own identifier. This module has "
                  "no approver, no gate and no apply path: whether this change happens is read from the "
                  "Agency's record, never from here"),
    }


@router.get("/sla")
async def support_sla(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """The resolution rate over confirmed records only — None when nothing is confirmed."""
    r = tickets.rate()
    return {
        **r,
        "simulated": False,
        "method": ("confirmed_resolved / (confirmed_resolved + confirmed_unresolved). Tickets with no "
                   "confirmation are excluded from BOTH sides rather than counted as successes, which is "
                   "the difference between this figure and the archived monitor's 100%: that one divided "
                   "over tickets it had invented, against a success field that was an unconditional literal"),
    }
