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
from agentic_core.auth.core import get_current_user
from agentic_core.support import tickets

router = APIRouter(prefix="/api/v1/support", tags=["autonomous-support"])

#  The next step a ticket carries when its answer did not come through. "Not resolved" is never the end of
#  the record — the item's body requires an unresolved ticket to state what happens next.
_ESCALATION = ("escalated: a human reviewer picks this up. The platform did not answer, so nothing here "
               "claims it did")


class AskRequest(BaseModel):
    query: str = Field(min_length=1)
    tier: str = "standard"


class ConfirmRequest(BaseModel):
    ticket_id: str
    resolved: bool
    by: str = ""


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
    return {"ticket_id": rec["id"], "confirmed": rec["confirmed"], "confirmed_by": rec["confirmed_by"],
            "basis": ("recorded from a confirmation naming its source. Nothing on this platform confirms a "
                      "resolution on a user's behalf")}


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
