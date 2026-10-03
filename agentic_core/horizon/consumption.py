"""What a run consumed — and, for every figure, WHAT MEASURED IT (P2.15).

THE RULE THIS MODULE IS BUILT ON: a zero that means "not measured" is the defect, not the absence of a
number. Every field below is three-state — a measured value, or None with a basis naming what did not
measure it — and `calls: 0` is reserved for a run that genuinely made no call, which is a different fact
from a run whose provenance map nobody populated.

EVERY FIELD NAMES ITS SOURCE, and the sources are DECLARED rather than described. FIELDS below is the
closed set of things this record computes, each mapped to the thing that measures it. A record cannot
carry a computed field that is not in FIELDS, which is what makes the A.9.5 check a check on the BINDING
rather than on a word list: adding a `barakah_score` would mean adding it here, naming what measures it,
and failing the guard — rather than slipping past a grep because the forbidden word sits in a comment.

THE OWNER'S OWN FIELDS ARE NOT COMPUTED AT ALL. `used_well` and `what_was_formed` are the Owner's words
about their own run. They stay None until the Owner writes them, no default is persisted, nothing is
suggested, and nothing is inferred from the run's figures — a platform that guessed what a person had
formed would be doing precisely what Ruling A.9.5 forbids, with a friendlier vocabulary.
"""
from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, data_path, read_json_strict, store_lock

#  The closed set of COMPUTED fields, each naming what measures it. Nothing outside this set is computed
#  onto a record, and the guard asserts that by comparing a built record's keys against it.
FIELDS: Dict[str, str] = {
    "wall_ms": (
        "the elapsed time around the handler, measured by the observing seam's own clock "
        "(agentic_core/horizon/membrane.py). It is wall time, not CPU time, and it includes whatever "
        "the handler waited on"),
    "calls": (
        "the number of entries in the run's provenance map — the record of model calls this platform "
        "already keeps. It counts CALLS RECORDED, which is not the same as calls made if something "
        "failed to record one"),
    "served_by": (
        "who served each recorded call, read from that same provenance map. A call whose server was "
        "not recorded appears as null rather than being attributed to the floor"),
    "stores_read": (
        "the JSON stores a run opened, as the run itself reported them. Nothing instruments the "
        "filesystem, so this is a declaration by the caller and not an observation of it"),
    "whose_data": (
        "the account the run was attributed to, from the owner id threaded through the call. None "
        "means the run was not attributed — which is the ordinary state on the 52 gateway sites that "
        "thread no owner id (FU-276), not a claim that the data belonged to nobody"),
}

#  The Owner's own fields. NOT in FIELDS, because nothing computes them.
OWNER_FIELDS: Dict[str, str] = {
    "used_well": "what the Owner judges was used well in this run. Their words, written by them, or empty",
    "what_was_formed": "what the Owner judges was formed by this run. Their words, written by them, or empty",
}

OWNER_FIELD_BASIS = (
    "NOT FILLED: this is the Owner's own field and nothing but the Owner may write it. There is no "
    "default, no suggestion is persisted as a value, and nothing is inferred from the run's figures — a "
    "platform that guessed what a person had formed would be doing what Ruling A.9.5 forbids in a "
    "friendlier vocabulary. Empty here means the Owner has not written it, and nothing else"
)

#  Concepts that may never become a computed field. The guard asserts no FIELDS entry concerns any of
#  them — on the binding, so a comment mentioning one cannot satisfy it and adding one cannot hide.
NEVER_COMPUTED = ("virtue", "gratitude", "barakah", "spiritual", "piety", "sincerity", "fitrah",
                  "righteous", "devotion", "faith_level")

_CAP = 2000


def _store():
    return data_path("horizon/consumption.json")


def _read() -> List[Dict[str, Any]]:
    return read_json_strict(_store(), missing=[], expect=list)


def _measured(value: Any, field: str) -> Dict[str, Any]:
    """One field's value AND what measured it — or None and why it was not measured."""
    if value is None:
        return {"value": None, "measured": False,
                "basis": f"NOT MEASURED ({field}): {FIELDS[field]} — and nothing supplied it for this "
                         f"run. This is not zero"}
    return {"value": value, "measured": True, "basis": FIELDS[field]}


def build(run_id: Optional[str] = None, *, wall_ms: Optional[float] = None,
          provenance: Optional[Dict[str, Any]] = None, stores_read: Optional[List[str]] = None,
          whose_data: Optional[str] = None, intent_id: Optional[str] = None) -> Dict[str, Any]:
    """A ConsumptionRecord. EVERY computed field carries what measured it, or says it was not measured.

    THE PROVENANCE MAP IS THE CASE THE BAR NAMES. An EMPTY map and an ABSENT map are different facts: a
    run that made no calls genuinely made none (calls = 0), and a run nobody instrumented has no map at
    all (calls = None, "not measured"). Reporting the second as 0 is the defect — it is a figure nobody
    computed, wearing the shape of one that was.
    """
    _calls: Optional[int] = None
    _served: Optional[Dict[str, Any]] = None
    if isinstance(provenance, dict):
        #  A MAP THAT EXISTS AND IS EMPTY IS A MEASUREMENT: nought calls were recorded.
        _calls = len(provenance)
        _served = {k: (v.get("served_by") if isinstance(v, dict) else v) for k, v in provenance.items()}

    rec: Dict[str, Any] = {
        "consumption_id": f"consumed-{uuid.uuid4().hex[:12]}",
        "run_id": run_id,
        "intent_id": intent_id,
        "created_at": time.time(),
        "wall_ms": _measured(wall_ms, "wall_ms"),
        "calls": _measured(_calls, "calls"),
        "served_by": _measured(_served, "served_by"),
        "stores_read": _measured(stores_read, "stores_read"),
        "whose_data": _measured(whose_data, "whose_data"),
    }
    #  THE OWNER'S FIELDS, EMPTY, with the same basis on each. They are set only through the route.
    for _f in OWNER_FIELDS:
        rec[_f] = None
        rec[f"{_f}_basis"] = OWNER_FIELD_BASIS
        rec[f"{_f}_by"] = None
    rec["computed_fields"] = sorted(FIELDS)
    rec["owner_fields"] = sorted(OWNER_FIELDS)
    rec["basis"] = (
        f"{sum(1 for f in FIELDS if rec[f]['measured'])} of {len(FIELDS)} computed field(s) were "
        f"measured for this run; the rest say what did not measure them rather than reporting zero. The "
        f"{len(OWNER_FIELDS)} Owner field(s) are the Owner's own words and are computed by nothing")
    return rec


def set_owner_field(consumption_id: str, field: str, text: Optional[str], by: str) -> Dict[str, Any]:
    """Set or CLEAR an Owner field. Nothing but a user may call this.

    `by` must name a user, for the same reason the reflection tag does: a value written here by an agent
    would be the platform's account of what a person formed, asserted in their own field.
    """
    if field not in OWNER_FIELDS:
        return {"ok": False, "reason": f"{field!r} is not an Owner field; the Owner fields are "
                                       f"{sorted(OWNER_FIELDS)}"}
    if not str(by or "").startswith("user:"):
        return {"ok": False, "reason": (
            f"REFUSED: {by!r} does not name a user. This field holds the Owner's own words about their "
            f"own run, and a value written by an agent would be the platform's account of what a person "
            f"formed — which Ruling A.9.5 forbids")}
    _text = (text or "").strip() or None
    with store_lock(_store()):
        rows = _read()
        for r in rows:
            if r.get("consumption_id") == consumption_id:
                r[field] = _text
                r[f"{field}_by"] = by if _text else None
                r[f"{field}_at"] = time.time() if _text else None
                r[f"{field}_basis"] = (
                    f"set by {by}" if _text else OWNER_FIELD_BASIS)
                atomic_write_json(_store(), rows[-_CAP:])
                return {"ok": True, "record": r}
    return {"ok": False, "reason": f"no consumption record {consumption_id!r}"}


def save(record: Dict[str, Any]) -> Dict[str, Any]:
    with store_lock(_store()):
        rows = _read()
        rows.append(record)
        atomic_write_json(_store(), rows[-_CAP:])
    return record


def listing(limit: int = 50) -> List[Dict[str, Any]]:
    return _read()[-limit:][::-1]


def for_intent(intent_id: str) -> Optional[Dict[str, Any]]:
    return next((r for r in reversed(_read()) if r.get("intent_id") == intent_id), None)


def states() -> Dict[str, Any]:
    """Every computed field with what measures it, the Owner's fields, and what is never computed."""
    return {
        "computed_fields": dict(FIELDS),
        "owner_fields": dict(OWNER_FIELDS),
        "owner_field_basis": OWNER_FIELD_BASIS,
        "never_computed": list(NEVER_COMPUTED),
        "never_computed_basis": (
            "Ruling A.9.5 — the Fitrah Spectrum is never a measurement and no AI verdict is passed on "
            "anyone's spiritual state. These are not a word filter: the record's COMPUTED set is closed "
            "to the fields above, so a field about any of them would have to be declared there, naming "
            "what measures it. A guard asserts the closure, which a comment cannot satisfy"),
        "zero_is_not_absence": (
            "a measured zero and an unmeasured field are different states and are reported differently. "
            "calls=0 means a run whose provenance map was present and empty; calls=null means nothing "
            "recorded a map at all. Collapsing the second into the first is the defect this item names"),
        "store_cap": _CAP,
    }
