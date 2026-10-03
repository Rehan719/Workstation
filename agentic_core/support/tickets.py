"""The support ticket store: answered and resolved are different states, and a rate nothing can fake.

THE ANTI-PATTERN THIS IS BUILT AGAINST is named in the package docstring and is worth restating where the
arithmetic lives: the archived `sla_monitor.py` computed `sum(1 for r in resolutions if r.success) / len(...)`
over tickets it had invented, against a `success` field that was an unconditional literal. Every step of that
division is real. The inputs are not. So the rule here is that the DENOMINATOR is the set of records somebody
actually confirmed, and a record nobody has confirmed is excluded from both sides rather than counted as a win.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

#  Resolution is THREE-STATE. The archive had one boolean for "answered" and "resolved" together, which is
#  what let an answer count as a resolution.
CONFIRMED_RESOLVED = True
CONFIRMED_UNRESOLVED = False
UNCONFIRMED = None


def _store():
    return data_path("support_tickets.json")


def _read() -> List[Dict[str, Any]]:
    """STRICT read: a store that cannot be read is an error, not an empty list.

    A tolerant read here would answer [] for a truncated store, and every figure computed from it — the
    resolution rate above all — would then describe a store nobody could read while looking like a measurement
    of a quiet week.
    """
    return read_json_strict(_store(), missing=[], expect=list)


def create_ticket(user_id: str, query: str, tier: str = "standard") -> Dict[str, Any]:
    """Open a ticket. It is NOT answered and NOT resolved, and both of those are recorded as such."""
    t = {
        "id": f"tkt-{uuid.uuid4().hex[:12]}",
        "user_id": user_id,
        "tier": tier,
        "query": query,
        "created_at": time.time(),
        "answer": None,
        "answered_at": None,
        # three-state from birth: nobody has confirmed anything about a ticket that was just opened
        "confirmed": UNCONFIRMED,
        "confirmed_at": None,
        "confirmed_by": None,
        "next_step": None,
    }
    with store_lock(_store()):
        rows = _read()
        rows.append(t)
        atomic_write_json(_store(), rows)
    return t


def record_answer(ticket_id: str, text: str, served_by: Optional[str], is_external: bool,
                  failed: bool, latency_ms: float, next_step: str) -> Dict[str, Any]:
    """Attach an answer with ITS PROVENANCE. Answering does not resolve anything.

    `failed` is carried rather than inferred from an empty string: a call that failed and a call that returned
    nothing are different facts, and a failed call must never read as an answer. `latency_ms` is the MEASURED
    duration of that call — nothing in this package sleeps to imitate work, which is precisely what the
    archived agent did to make its tiers look different.
    """
    with store_lock(_store()):
        rows = _read()
        for r in rows:
            if r.get("id") != ticket_id:
                continue
            r["answer"] = {
                "text": text,
                "served_by": served_by,
                "is_external": bool(is_external),
                "failed": bool(failed),
                "latency_ms": round(float(latency_ms), 1),
                "provenance_basis": (
                    f"served by {served_by or 'NOT RECORDED'}"
                    + (" (EXTERNAL)" if is_external else " (in-house)")
                    + ("; THE CALL FAILED, so this is not an answer" if failed else "")
                    + f"; {round(float(latency_ms), 1)}ms measured, not simulated"),
            }
            r["answered_at"] = time.time()
            #  An unresolved ticket carries its next step, so "not resolved" is never the end of the record.
            r["next_step"] = next_step
            atomic_write_json(_store(), rows)
            return r
    raise KeyError(f"no ticket {ticket_id}")


def confirm(ticket_id: str, resolved: bool, by: str) -> Dict[str, Any]:
    """Record a CONFIRMATION — the only way `resolved` is ever written.

    `by` is kept because a confirmation's source is part of the fact: a user saying their problem is fixed and
    a measured outcome saying so are both admissible, and a reader needs to know which one it was. Nothing in
    this package confirms itself.
    """
    if not isinstance(resolved, bool):
        raise TypeError("a confirmation is True or False; absence of a confirmation is simply not recording one")
    with store_lock(_store()):
        rows = _read()
        for r in rows:
            if r.get("id") != ticket_id:
                continue
            r["confirmed"] = resolved
            r["confirmed_at"] = time.time()
            r["confirmed_by"] = by
            atomic_write_json(_store(), rows)
            return r
    raise KeyError(f"no ticket {ticket_id}")


def rate() -> Dict[str, Any]:
    """The resolution rate, computed from confirmations only, and three-state when there are none.

    THE DENOMINATOR IS THE POINT. Only records whose `confirmed` is not None enter it. An answered but
    unconfirmed ticket is excluded from BOTH sides — it is not a success and not a failure, and counting it
    either way would be inventing the user's verdict. With no confirmations the rate is None with a basis,
    because 0.0 would read as "we resolve nothing" and 1.0 as the archived simulation's 100%.
    """
    try:
        rows = _read()
        unreadable = None
    except Exception as e:                       # noqa: BLE001 — the store's state is part of the answer
        return {"rate": None, "confirmed_resolved": None, "confirmed_unresolved": None,
                "unconfirmed": None, "answered": None, "tickets": None,
                "unreadable": f"{e.__class__.__name__}: {e}",
                "basis": ("NOT COMPUTED: the ticket store could not be read, so no rate is reported. An "
                          "unreadable store is not a quiet week")}
    resolved = sum(1 for r in rows if r.get("confirmed") is True)
    unresolved = sum(1 for r in rows if r.get("confirmed") is False)
    unconfirmed = sum(1 for r in rows if r.get("confirmed") is None)
    answered = sum(1 for r in rows if (r.get("answer") or {}).get("text") is not None
                   and not (r.get("answer") or {}).get("failed"))
    denom = resolved + unresolved
    return {
        "rate": (round(resolved / denom, 4) if denom else None),
        "confirmed_resolved": resolved,
        "confirmed_unresolved": unresolved,
        "unconfirmed": unconfirmed,
        "answered": answered,
        "tickets": len(rows),
        "unreadable": unreadable,
        "basis": (
            (f"{resolved} of {denom} CONFIRMED ticket(s) were confirmed resolved. {unconfirmed} ticket(s) "
             f"carry no confirmation and are excluded from both sides of this rate: an answered ticket is "
             f"not a resolved one, and counting an unconfirmed ticket either way would invent the user's "
             f"verdict")
            if denom else
            (f"NOT COMPUTED: none of {len(rows)} ticket(s) carries a confirmation, so there is no "
             f"denominator. This is not 0.0 and it is certainly not 1.0 — {answered} ticket(s) have an "
             f"answer, which is a different thing from a resolution")),
    }


def get(ticket_id: str) -> Optional[Dict[str, Any]]:
    return next((r for r in _read() if r.get("id") == ticket_id), None)


def listing(user_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    rows = _read()
    if user_id is not None:
        rows = [r for r in rows if r.get("user_id") == user_id]
    return rows[-limit:][::-1]
