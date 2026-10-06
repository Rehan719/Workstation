"""P3.24 — STAGED SIMULATION, PROCEDURAL FIRST. A schedule, never a forecast.

DESTINATION: agentic_core/simulation/staged.py (new package + file, LF). Prepared in W596's suite wait.

THE OWNER'S RULING OF 2026-10-03c (option (a)) IS THE FRAME, and it is spent — a later round may not reopen
it on its own judgement: **the platform computes schedules and assembles evidence and NEVER FORECASTS AN
OUTCOME.** No outcome dataset exists here, no judge data, and a settlement range shown to someone in a live
matter is a number they will act on however it is labelled.

THE DESIGN DECISION THAT MATTERS MOST: THE RULES ARE AN INPUT, NOT KNOWLEDGE THIS PLATFORM ASSERTS.

A procedural timeline needs rules — "the claim must be presented within N days of the event". The tempting
implementation is to encode those rules here. That would make this file a statement about what the law IS,
which is legal advice in a data structure, and the item says plainly that nothing the platform produces is
legal advice. So a caller SUPPLIES the rules it wants applied, each with its own citation, and this module
does only the arithmetic and names the rule it used. Every date is then traceable to a rule the caller
stated, and the platform asserts nothing about the law at all.

FOUR STAGES, AND THREE OF THEM HAVE NO INPUT HERE:

  1 PROCEDURAL — rules and arithmetic over the case's own dates. BUILT.
  2 RETRIEVAL over real precedent — NO INPUT: no precedent index exists (that is P3.22, and the archive's
    only candidate fabricates its citations).
  3 CAUSAL GRAPH — NO INPUT: none exists.
  4 SHADOW — never on a surface. An attempt to surface it is REFUSED, and the refusal says why.

A stage with no input SAYS SO rather than returning an empty timeline, because an empty result and an
unavailable stage are different facts.
"""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Optional

STAGE_PROCEDURAL = 1
STAGE_RETRIEVAL = 2
STAGE_CAUSAL = 3
STAGE_SHADOW = 4

NO_INPUT = "NO INPUT"
SHADOW_ONLY = "shadow-only"

#  the words a legal-outcome forecast would use. Nothing here produces them; the guard greps the module and
#  the responses for them, and this list exists so the refusal can NAME what was asked for.
FORECAST_TERMS = ("probability", "likelihood", "win rate", "settlement range", "expected award",
                  "predicted outcome", "chance of success", "odds")


def _parse_date(value: str) -> Optional[datetime.date]:
    """ISO only. A date this module cannot parse is reported, never guessed at."""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(value or "").strip())
    if not m:
        return None
    try:
        return datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def procedural_timeline(events: Dict[str, str], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Stage 1 — a SCHEDULE computed from the caller's own rules and the case's own dates.

    `events`  : {event_name: "YYYY-MM-DD"} — the case's dates, as the caller recorded them.
    `rules`   : [{id, citation, from_event, offset_days, description}] — the rules the CALLER applies.

    Every returned date carries the rule id, the citation the caller gave, the event it counted from and the
    arithmetic in words, so the date can be checked by hand. A rule whose event is missing or unparseable is
    reported as not computable with the reason — never silently dropped, and never estimated.

    THIS MODULE ASSERTS NOTHING ABOUT THE LAW. It applies rules it was handed and says whose they were.
    """
    computed: List[Dict[str, Any]] = []
    not_computable: List[Dict[str, Any]] = []
    for r in rules or []:
        if not isinstance(r, dict):
            continue
        rid = str(r.get("id") or "")
        frm = str(r.get("from_event") or "")
        raw = (events or {}).get(frm)
        base = _parse_date(raw) if raw is not None else None
        offset = r.get("offset_days")
        if raw is None:
            not_computable.append({"rule": rid, "why": f"the case records no event named {frm!r}"})
            continue
        if base is None:
            not_computable.append({"rule": rid,
                                   "why": f"the date for {frm!r} ({raw!r}) is not an ISO date, so it was "
                                          f"NOT guessed at"})
            continue
        if not isinstance(offset, int):
            not_computable.append({"rule": rid,
                                   "why": f"the rule states no whole-day offset ({offset!r}), and this "
                                          f"module does not invent one"})
            continue
        due = base + datetime.timedelta(days=offset)
        computed.append({
            "rule": rid,
            "citation": str(r.get("citation") or "(the caller supplied no citation)"),
            "description": str(r.get("description") or ""),
            "from_event": frm,
            "from_date": base.isoformat(),
            "offset_days": offset,
            "date": due.isoformat(),
            "arithmetic": f"{base.isoformat()} + {offset} day(s) = {due.isoformat()}",
            "stage": STAGE_PROCEDURAL,
        })
    computed.sort(key=lambda e: e["date"])
    return {
        "stage": STAGE_PROCEDURAL,
        "stage_name": "procedural",
        "timeline": computed,
        "not_computable": not_computable,
        "basis": (
            f"{len(computed)} date(s) computed as arithmetic over rules the CALLER supplied, each naming "
            f"its rule, its citation, the event it counted from and the sum in words so it can be checked "
            f"by hand. This platform asserts nothing about what the law requires - it applies the rules it "
            f"was given. This is a SCHEDULE, not a forecast: no date here predicts an outcome."
            + (f" {len(not_computable)} rule(s) could not be computed and are listed with the reason "
               f"rather than estimated." if not_computable else "")),
    }


def stage(number: int, **inputs: Any) -> Dict[str, Any]:
    """Any stage. Stages 2-4 have no input on this deployment and say so rather than returning emptiness."""
    if number == STAGE_PROCEDURAL:
        return procedural_timeline(inputs.get("events") or {}, inputs.get("rules") or [])
    if number == STAGE_RETRIEVAL:
        return {"stage": STAGE_RETRIEVAL, "stage_name": "retrieval over real precedent",
                "status": NO_INPUT, "timeline": None,
                "basis": ("NO INPUT: no precedent index exists on this deployment, so there is nothing to "
                          "retrieve over. An empty result and an unavailable stage are different facts, and "
                          "this is the second. Building the index is P3.22.")}
    if number == STAGE_CAUSAL:
        return {"stage": STAGE_CAUSAL, "stage_name": "causal graph", "status": NO_INPUT, "timeline": None,
                "basis": ("NO INPUT: no causal graph exists on this deployment. Nothing here infers one "
                          "from a timeline - a sequence of dates is not a cause.")}
    if number == STAGE_SHADOW:
        return {"stage": STAGE_SHADOW, "stage_name": "shadow", "status": SHADOW_ONLY, "timeline": None,
                "basis": ("SHADOW ONLY: stage 4 never reaches a surface. Use surface_stage_4() to see the "
                          "refusal and its reason.")}
    return {"stage": number, "status": NO_INPUT,
            "basis": f"there is no stage {number}; the staged simulation has four"}


def surface_stage_4(reason: str = "") -> Dict[str, Any]:
    """Attempting to put stage 4 on a surface. ALWAYS REFUSED, and the refusal says why.

    Clause (4) requires a guard that drives this attempt and sees it refused, so the refusal is a real
    mechanism rather than a convention somebody could forget. It takes the caller's stated reason and
    refuses it anyway: there is no reason that makes a shadow stage surfaceable, and accepting an override
    parameter would be a gate that cannot refuse.
    """
    return {
        "surfaced": False,
        "refused": True,
        "stage": STAGE_SHADOW,
        "reason_given": str(reason or "")[:200] or None,
        "basis": ("REFUSED: stage 4 is shadow-only and never reaches a surface, whatever reason is given. "
                  "The Owner's ruling of 2026-10-03c (option (a)) settled this and the standing offer in "
                  "the decision row is spent - it would take a NEW ruling, not a reassessment. No outcome "
                  "dataset exists here, no judge data, and a settlement range shown to someone in a live "
                  "matter is a number they will act on however it is labelled."),
    }


def forecast(*_args: Any, **_kwargs: Any) -> Dict[str, Any]:
    """There is no forecast. This exists so that asking for one gets an answer instead of an AttributeError.

    A caller that reaches for a prediction is told plainly that this platform does not make one, and why -
    which is more useful than a missing attribute, and it means the refusal is discoverable rather than
    implicit in an absence.
    """
    return {
        "forecast": None,
        "refused": True,
        "basis": ("This platform does NOT forecast a legal outcome and does not produce a settlement range. "
                  "Owner ruling 2026-10-03c: no outcome dataset exists here, no judge data, and judge "
                  "tendencies from public rulings are neither available nor a proper basis for advice to a "
                  "party. What it does instead: computes a SCHEDULE from rules the caller supplies, and "
                  "assembles evidence. Nothing it produces is legal advice."),
    }
