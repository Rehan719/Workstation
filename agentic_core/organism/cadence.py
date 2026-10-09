"""§17.3 cadence — the Strategic and Action-Plan layers refresh themselves, and say why they did.

WHY THIS FILE EXISTS. §17.3 promises a Living Business System whose Strategic layer refreshes quarterly
or on a market signal, and whose Action-Plan layer refreshes weekly or on a KPI trigger. Measured before
building (W585): the cadence existed only as PROMPT TEXT. The four occurrences of strategic / cadence /
quarterly / weekly in `api/management_systems.py` are all inside a request to a model — a
`planning_horizon` field whose comment lists the options, a "You are a strategic management consultant"
line, a "## Performance Review Cadence (daily/weekly/monthly/quarterly rhythms)" heading and a RACI line.
Nothing fired. `api/board.py` already published a `ceo_action_plan`, and it came from a model call made
at pack time (`:442`), which is the shape clause (3) is written against: a pack that reads elsewhere looks
identical whatever the refreshes say.

THE TRIGGER IS A PURE PREDICATE, and that is the design decision the bar forces. P3.3 clause (1) says
each refresh is "driven by FORCING the trigger rather than waiting for it", so the due-check cannot be
wall-clock arithmetic buried in the beat — a guard would have to freeze time, and a guard that cannot
drive a trigger ends up asserting the source instead of the behaviour. `due()` takes `now` and the
signals as ARGUMENTS. The beat passes the real clock; a guard passes its own.

AND THE HISTORY KEEPS WHAT WAS REPLACED. Clause (2) says a refresh that overwrites without a history
entry fails, so every entry carries the content it wrote AND the content it displaced. An Owner's
strategy paragraph is not lost by a quarterly refresh landing on top of it; it is still readable in the
entry that replaced it.

WHAT A REFRESH DOES NOT DO. It does not invent a market signal or a KPI breach — both are supplied by
whoever observed them, and a refresh with neither says it fired on elapsed time. It does not call a model
on the beat: the heartbeat's own comments hold its work to "Cheap + deterministic + virtual", so the
default composition is derived from the plan's own state and its provenance says exactly that. A
model-composed refresh is possible through the route, and then the provenance names the resource that
served it.
"""
from __future__ import annotations

import calendar
import time
import uuid
from typing import Any, Dict, List, Optional

from agentic_core.config import atomic_write_json, store_lock

STRATEGIC = "strategic"
ACTION_PLAN = "action_plan"
LAYERS = (STRATEGIC, ACTION_PLAN)

#  §17.3's own periods. Named so a reader can see them and a guard can compute with them rather than
#  re-deriving a number this module happens to use.
QUARTER_SECONDS = 91 * 24 * 60 * 60
WEEK_SECONDS = 7 * 24 * 60 * 60
PERIOD_SECONDS = {STRATEGIC: QUARTER_SECONDS, ACTION_PLAN: WEEK_SECONDS}
PERIOD_NAME = {STRATEGIC: "quarterly", ACTION_PLAN: "weekly"}

#  the second trigger for each layer — the one that does not wait for the clock
SIGNAL_NAME = {STRATEGIC: "market signal", ACTION_PLAN: "KPI trigger"}

#  which field of the plan each layer writes
PLAN_FIELD = {STRATEGIC: "strategy", ACTION_PLAN: "action_plan"}

#  W620 (FU-492, M2 v8 R3.5) — the cadence said a market signal or KPI trigger "would fire it regardless", and
#  nothing in this repository observes a market or a KPI: the only producer of a signal is the refresh route's
#  own `signal` parameter. The trigger is real; the observer is absent, and every reason that names the signal
#  now says which.
SIGNALS_OBSERVED_BY = ("nothing in this platform observes markets or KPIs, so a signal fires only when someone "
                       "supplies one (POST /api/v1/organism/cadence/refresh?layer=...&signal=...)")

TRIGGER_ELAPSED = "elapsed"
TRIGGER_SIGNAL = "signal"
TRIGGER_NEVER_REFRESHED = "never_refreshed"


def _now() -> float:
    return time.time()


def _stamp(ts: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts))


def _parse_stamp(s: Any) -> Optional[float]:
    """A stored ISO stamp back to epoch seconds, or None when there is nothing to parse.

    None means NEVER REFRESHED, which is its own state and never "refreshed long ago": the two produce
    the same `due` answer today but different reasons, and the reason is what a reader acts on.
    """
    if not s:
        return None
    try:
        #  W639 (ledger v14 R3.3 / R4.6 / R6.3 — one bug, found by three regions). The stamp is written with
        #  gmtime, and this read it back with mktime (LOCAL time) less time.timezone. time.timezone is the
        #  NON-daylight offset, so during summer time the result was an hour early and every "time since the
        #  last refresh" read an hour long. A UTC stamp is parsed as UTC.
        return float(calendar.timegm(time.strptime(str(s), "%Y-%m-%dT%H:%M:%SZ")))
    except Exception:
        return None


def due(layer: str, last_refresh_at: Any, now: Optional[float] = None,
        signal: Optional[str] = None) -> Dict[str, Any]:
    """Is this layer due a refresh? A PURE function of its arguments — no clock, no store, no I/O.

    `now` and `signal` are arguments precisely so a guard can FORCE either trigger, which is what clause
    (1) of P3.3 requires. Returns the three things a caller needs and a history entry has to record:
    whether it is due, WHICH trigger fired, and a reason in words.
    """
    if layer not in LAYERS:
        raise ValueError(f"unknown cadence layer {layer!r}; expected one of {LAYERS}")
    now = _now() if now is None else float(now)
    last = _parse_stamp(last_refresh_at)
    period = PERIOD_SECONDS[layer]

    #  A SIGNAL FIRES REGARDLESS OF THE CLOCK. That is the whole point of the second trigger: a market
    #  signal or a breached KPI is not willing to wait out the rest of a quarter or a week.
    if signal:
        return {"due": True, "trigger": TRIGGER_SIGNAL, "signal": str(signal),
                "reason": f"{SIGNAL_NAME[layer]}: {signal}",
                "last_refresh_at": last_refresh_at or None,
                "elapsed_seconds": None if last is None else round(now - last, 3),
                "period_seconds": period}

    if last is None:
        return {"due": True, "trigger": TRIGGER_NEVER_REFRESHED, "signal": None,
                "reason": (f"this layer has NEVER been refreshed, which is not the same as refreshed "
                           f"long ago - there is no previous {PERIOD_NAME[layer]} refresh to measure from"),
                "last_refresh_at": None, "elapsed_seconds": None, "period_seconds": period}

    elapsed = now - last
    if elapsed >= period:
        return {"due": True, "trigger": TRIGGER_ELAPSED, "signal": None,
                "reason": (f"{PERIOD_NAME[layer]} period elapsed: {round(elapsed / 86400, 2)} day(s) "
                           f"since the last refresh, period is {round(period / 86400)} day(s)"),
                "last_refresh_at": last_refresh_at, "elapsed_seconds": round(elapsed, 3),
                "period_seconds": period}
    return {"due": False, "trigger": None, "signal": None,
            "reason": (f"not due: {round(elapsed / 86400, 2)} day(s) since the last refresh, "
                       f"{PERIOD_NAME[layer]} period is {round(period / 86400)} day(s). A "
                       f"{SIGNAL_NAME[layer]} would fire it regardless, but only one a caller SUPPLIES - "
                       f"{SIGNALS_OBSERVED_BY}"),
            "last_refresh_at": last_refresh_at, "elapsed_seconds": round(elapsed, 3),
            "period_seconds": period}


# ── the plan, read and written through business_plan's own helpers so there is one store ────────────
def _plan_path(scope: str):
    from agentic_core.api.business_plan import _path
    return _path(scope)


def _read_plan(scope: str) -> Dict[str, Any]:
    """STRICT, through business_plan's own loader: an unreadable plan raises rather than being replaced.

    This matters more here than almost anywhere, because a refresh WRITES. A tolerant read would hand
    this module a fresh empty plan and the next refresh would atomically overwrite the Owner's real one
    with it — the FU-395 class, where a tolerant read is never a write base.
    """
    from agentic_core.api.business_plan import _load
    return _load(scope)


def last_refresh_at(plan: Dict[str, Any], layer: str) -> Optional[str]:
    """When this layer was last refreshed, from the history — or None for never."""
    for entry in reversed(plan.get("refreshes") or []):
        if isinstance(entry, dict) and entry.get("layer") == layer:
            return entry.get("at")
    return None


def history(scope: str, layer: Optional[str] = None) -> List[Dict[str, Any]]:
    rows = (_read_plan(scope).get("refreshes") or [])
    if layer is not None:
        rows = [r for r in rows if isinstance(r, dict) and r.get("layer") == layer]
    return list(rows)


def latest(scope: str, layer: str) -> Optional[Dict[str, Any]]:
    #  W615 (FU-487) — the latest refresh that was WRITTEN. A proposal kept beside an Owner's edit is in the
    #  history, but it is not the layer's content, and the Board Pack assembles its strategic layer from this.
    rows = [r for r in history(scope, layer) if r.get("applied", True) is not False]
    return rows[-1] if rows else None


def _compose(plan: Dict[str, Any], layer: str) -> Dict[str, Any]:
    """The default composition: DERIVED from the plan's own state, and it says so.

    No model is called here. The heartbeat's own comments hold its work to cheap and deterministic, and a
    refresh that quietly called a model on every beat would be neither. The provenance records that this
    is the deterministic floor, so nothing downstream can read a derived paragraph as a composed one.
    """
    objectives = [o for o in (plan.get("objectives") or []) if isinstance(o, dict)]
    aims = [a for a in (plan.get("aims") or []) if a]
    if layer == STRATEGIC:
        #  W635 (FU-581) - derived text goes stale between quarterly refreshes, so it carries the time it was derived
        body = (f"[as of {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}] "
                f"Strategic position derived from the plan itself: {len(aims)} aim(s) and "
                f"{len(objectives)} objective(s) on the roadmap"
                + (f"; vision on record: {str(plan.get('vision'))[:160]}" if plan.get("vision") else
                   "; no vision is on record")
                + (f"; mission on record: {str(plan.get('mission'))[:160]}" if plan.get("mission") else
                   "; no mission is on record") + ".")
    else:
        _open = [o for o in objectives if str(o.get("status") or "") != "done"]

        def _pct(o: Dict[str, Any]) -> Optional[int]:
            """This objective's progress, or None when the stored value is not a number.

            W589 — this was `int(o.get("progress_pct") or 0)`, and ONE objective carrying a non-numeric
            progress raised ValueError out of _compose, out of refresh, and stopped the ENTIRE cadence for
            every layer (verified: "half" raises invalid literal for int()). The cadence does not own that
            field and is not its validator, so a value it cannot read is reported as unknown rather than
            counted as zero progress - which would also be a lie, since an unreadable progress is not a
            measured nought.
            """
            try:
                return int(o.get("progress_pct") or 0)
            except (TypeError, ValueError):
                return None

        _stalled = [o for o in _open if _pct(o) == 0]
        _unknown = [o for o in _open if _pct(o) is None]
        body = (f"Action position derived from the plan itself: {len(_open)} open objective(s), of which "
                f"{len(_stalled)} record no progress at all"
                #  an unreadable progress is named rather than folded into the stalled count
                + (f", and {len(_unknown)} record a progress this module cannot read as a number"
                   if _unknown else "")
                + ("; " + "; ".join(
                    f"{str(o.get('title'))[:60]} "
                    f"({'unknown' if _pct(o) is None else _pct(o)}%)"
                    for o in _open[:5]) if _open else
                   "; the roadmap carries no open objective") + ".")
    return {
        "content": body,
        "served_by": "deterministic-floor",
        "is_external": False,
        "provenance_basis": ("DERIVED from the plan's own stored state by this module - no model composed "
                             "it, and nothing here is an analysis of the business. A model-composed "
                             "refresh carries the resource that served it instead"),
    }


def refresh(scope: str, layer: str, *, now: Optional[float] = None, signal: Optional[str] = None,
            content: Optional[str] = None, served_by: Optional[str] = None,
            is_external: Optional[bool] = None, provenance_basis: Optional[str] = None,
            force: bool = False) -> Dict[str, Any]:
    """Refresh one layer, write it to the plan, and append a history entry that keeps what it replaced.

    Returns `{"refreshed": False, "due": {...}}` without writing when the layer is not due, so a caller
    that runs on every beat does not have to decide. `force=True` refreshes regardless and the entry
    records that it was forced — a forced refresh that looked like a due one would make the history lie.
    """
    if layer not in LAYERS:
        raise ValueError(f"unknown cadence layer {layer!r}; expected one of {LAYERS}")
    now = _now() if now is None else float(now)

    with store_lock(_plan_path(scope)):
        plan = _read_plan(scope)
        verdict = due(layer, last_refresh_at(plan, layer), now=now, signal=signal)
        if not verdict["due"] and not force:
            return {"refreshed": False, "layer": layer, "scope": scope, "due": verdict,
                    "entry": None, "proposed": False, "basis": verdict["reason"]}

        if content is not None:
            composed = {"content": str(content),
                        "served_by": served_by or "caller-supplied",
                        "is_external": bool(is_external),
                        "provenance_basis": provenance_basis or
                        "supplied by the caller; this module did not compose it"}
        else:
            composed = _compose(plan, layer)

        field = PLAN_FIELD[layer]
        replaced = plan.get(field)
        entry = {
            "id": f"refresh-{uuid.uuid4().hex[:10]}",
            "layer": layer,
            "at": _stamp(now),
            "trigger": TRIGGER_SIGNAL if signal else (verdict["trigger"] or "forced"),
            "forced": bool(force and not verdict["due"]),
            "reason": (verdict["reason"] if verdict["due"] else
                       f"FORCED while not due - {verdict['reason']}"),
            "signal": verdict.get("signal"),
            "plan_field": field,
            "content": composed["content"],
            #  WHAT IT DISPLACED. Clause (2) forbids an overwrite with no history entry, and an entry
            #  that recorded only the new text would still lose the old one.
            "replaced": replaced if replaced not in ("", None) else None,
            "replaced_was_empty": replaced in ("", None),
            "served_by": composed["served_by"],
            "is_external": composed["is_external"],
            "provenance_basis": composed["provenance_basis"],
        }
        #  W615 (FU-487, M1 v8 R3.0) — THE OWNER'S OWN WORDS ARE NEVER OVERWRITTEN BY A CADENCE. The refresh
        #  replaced plan[field] whatever its source, so a Strategy the Owner wrote was replaced by floor-derived
        #  text while `owner_edits.strategy` stayed set and the page still badged it "owner-edited". A field
        #  the Owner edited is theirs: the refresh is RECORDED as a proposal (so the layer is not re-proposed
        #  every beat) and the plan is left as the Owner wrote it.
        _owner_edited = bool((plan.get("owner_edits") or {}).get(field))
        entry["applied"] = not _owner_edited
        entry["withheld_reason"] = (("the Owner edited this field, so the cadence PROPOSES and does not "
                                     "overwrite it; the Owner's text stands") if _owner_edited else None)
        if not _owner_edited:
            plan[field] = composed["content"]
        plan.setdefault("refreshes", []).append(entry)
        plan["updated_at"] = _stamp(now)
        atomic_write_json(_plan_path(scope), plan)

    if _owner_edited:
        return {"refreshed": False, "layer": layer, "scope": scope, "entry": entry, "due": verdict,
                "proposed": True,
                "basis": (f"{layer} composed and RECORDED AS A PROPOSAL: the Owner edited the plan's {field!r} "
                          f"field, so it was not overwritten. Trigger: {entry['trigger']} - {entry['reason']}")}
    return {"refreshed": True, "layer": layer, "scope": scope, "entry": entry, "due": verdict,
            "proposed": False,
            "basis": (f"{layer} refreshed and written to the plan's {field!r} field, with a history "
                      f"entry keeping what it replaced. Trigger: {entry['trigger']} - {entry['reason']}")}


def state(scope: str) -> Dict[str, Any]:
    """Both layers: when each was last refreshed, whether each is due now, and how many refreshes exist.

    Three-state throughout: a layer that has never been refreshed says so rather than reporting a zero
    age, because "never" and "just now" are opposite facts.
    """
    plan = _read_plan(scope)
    out: Dict[str, Any] = {"scope": scope, "layers": {}}
    for layer in LAYERS:
        last = last_refresh_at(plan, layer)
        rows = [r for r in (plan.get("refreshes") or [])
                if isinstance(r, dict) and r.get("layer") == layer]
        out["layers"][layer] = {
            "period": PERIOD_NAME[layer],
            "signal_trigger": SIGNAL_NAME[layer],
            "plan_field": PLAN_FIELD[layer],
            "last_refresh_at": last,
            "refresh_count": len(rows),
            "ever_refreshed": bool(rows),
            "due": due(layer, last),
            "latest": rows[-1] if rows else None,
        }
    #  W620 (FU-492, M2 v8 R3.5) — the signal triggers are real but nothing in the platform PRODUCES a signal, and
    #  the state now says so wherever it is read, beside the elapsed-time trigger that does fire on its own.
    out["signals_basis"] = SIGNALS_OBSERVED_BY
    out["basis"] = ("each layer reports when it was last refreshed, how many refreshes are on record and "
                    "whether it is due now. A layer that has NEVER been refreshed says so rather than "
                    "reporting an age of zero - never and just-now are opposite facts")
    return out
