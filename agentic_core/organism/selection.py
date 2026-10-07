"""Selection — and the two things it must never do: clear on an absence, or optimise toward a proxy.

WHY THIS FILE EXISTS. §8 promises an organism that is ever IMPROVING and EVOLVING, and names four
measures as continuously monitored: profitability, customer/user satisfaction, founder-alignment, live
compliance. Measured before building (W584): `organism/genome.py` has crossover, mutation and lineage,
and its own docstring says "NOTHING in this module evaluates fitness; the fields say so instead of
implying selection" — variation yes, inheritance yes, SELECTION NO, so evolution was impossible by
construction. This module is where selection becomes possible, and the first thing it does is REFUSE.

CLAUSE (3) IS THE WHOLE DESIGN. Selection refuses while any of the four measures is unmeasured, and the
refusal NAMES WHICH. That is not caution, it is the difference between two opposite facts: an entity
nobody has measured and an entity measured and found wanting. A selection that treated silence as a low
score would retire the unmeasured, and a selection that treated silence as fine would retire nobody —
both are decided by a missing number rather than by a record.

AND ONE OF THE FOUR HAS NO MECHANISM AT ALL. Founder-alignment is not implemented anywhere in this
repository, and this module does not invent it: it reports NOT MEASURED with that as the stated reason.
So selection refuses today, for a reason a reader can check, and will keep refusing until a founder
actually says something. That is the honest state of the organism and it is written down rather than
worked around.

CLAUSE (4) IS WHAT WORKS MEANWHILE. A hard FLOOR creates no optimisation pressure toward a proxy: it does
not rank anyone, it does not reward a high number, and it cannot be gamed by improving a metric, because
there is no metric to improve — there is a line, and an entity is either under it or not. An entity that
fails compliance outright is FLAGGED FOR REVIEW and the flag names the floor it failed. A flag is not a
retirement: nothing here removes anything, and death is governed through Change Control (P3.26).

WHAT THIS MODULE DOES NOT DO, and clause (1) of P3.27 is why the list is explicit. It computes, scores,
ranks and infers NOTHING about a spiritual state, sincerity, virtue, gratitude, barakah, tazkiyah, a
fitrah aspect or readiness, of anyone, ever (Ruling A.9.5). Every subject here is a VIRTUAL BUSINESS
ENTITY and every input is an economic or compliance record about that entity's own conduct. No field in
this module takes a person as its subject.

AND IT DOES NOT REUSE THE FUNDING SCORE (clause 5). Funding selects on POTENTIAL — §4 Stage 4 scores a
venture on outcome-success x value x benefit x feasibility x strategic-fit, which is a judgement about
what might happen. Survival selects on RECORD: what did happen. Conflating them would let a
well-pitched entity outlive a well-performing one, so this module reads none of those five fields and a
guard asserts it.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

#  The four §8 measures, named once so a caller cannot silently assess three of them.
MEASURES = ("profitability", "user_satisfaction", "founder_alignment", "live_compliance")

#  The §4 Stage 4 potential score's components. Selection must read NONE of these; the tuple exists so a
#  guard can assert the separation against a list this module itself declares.
FUNDING_POTENTIAL_FIELDS = ("outcome", "value", "benefit", "feasibility", "strategic_fit")

NOT_ASSESSABLE = "NOT_ASSESSABLE"
ASSESSABLE = "ASSESSABLE"

FLAGGED = "FLAGGED_FOR_REVIEW"
NOT_FLAGGED = "NOT_FLAGGED"


def _unmeasured(value: Any) -> bool:
    """A measure is unmeasured when nothing has been recorded for it. A recorded zero is a MEASUREMENT."""
    return value is None


def measure_entity(vsb_id: str) -> Dict[str, Any]:
    """Read the four §8 measures for one entity. Each carries its own `measured` flag and basis.

    Nothing is defaulted. Where a source has recorded nothing the value is None and `measured` is False
    with a basis saying why — which is the input clause (3) refuses on.
    """
    out: Dict[str, Any] = {"vsb_id": vsb_id, "measures": {}}

    #  ── 1. PROFITABILITY — the entity's own economic record, not a projection ───────────────────────
    entry: Optional[Dict[str, Any]] = None
    roster_error: Optional[str] = None
    try:
        from agentic_core.economy.living_vsbs import list_living
        roster = list_living()
        if roster.get("roster_unavailable"):
            roster_error = str(roster["roster_unavailable"])
        else:
            for r in (roster.get("living_vsbs") or []):
                if str(r.get("vsb_id")) == str(vsb_id):
                    entry = r
                    break
    except Exception as exc:                                     # pragma: no cover - defensive
        roster_error = f"{type(exc).__name__}: {exc}"

    if roster_error:
        out["measures"]["profitability"] = {
            "value": None, "measured": False,
            "basis": f"the living roster could not be read whole, so nothing is known: {roster_error}"}
    elif entry is None:
        out["measures"]["profitability"] = {
            "value": None, "measured": False,
            "basis": f"no entity {vsb_id!r} is on the living roster, so it has no economic record here"}
    else:
        dist = entry.get("last_distributable")
        #  W618 (FU-509, M2 v8 R6.5) — THE ROSTER'S FIGURE IS SCOPED TO THE CYCLES THE ROSTER RAN. A cycle run
        #  through any other path (POST /economy/cycle, a Genesis establish) is on the entity's books and not in
        #  `last_distributable`, so selection reported 0.0 WST as "measured" profitability beside books holding a
        #  305.83 WST distributable cycle. The books' own cycle count is compared with the roster's: when the
        #  books hold more, the figure is said to be the roster's last, not the entity's latest.
        _roster_cycles = int(entry.get("operating_cycles") or 0)
        _books_cycles, _books_err = None, None
        try:
            from agentic_core.economy.ledger import VirtualLedger as _VL618
            _books_cycles = _VL618(vsb_id)._cycles_posted().get("cycles_posted")
        except Exception as _le:                                  # pragma: no cover - defensive
            _books_err = f"{type(_le).__name__}: {_le}"
        _stale = isinstance(_books_cycles, int) and _books_cycles > _roster_cycles
        out["measures"]["profitability"] = {
            "value": dist, "measured": not _unmeasured(dist),
            "scope": "roster-operated cycles only",
            "roster_cycles": _roster_cycles, "books_cycles": _books_cycles,
            "basis": ((f"distributable profit of the last cycle the AUTONOMOUS ROSTER operated (virtual WST): {dist}"
                       + (f". STALE AS THE ENTITY'S FIGURE: its books record {_books_cycles} cycle(s) and the roster "
                          f"operated {_roster_cycles}, so a later cycle run by another path is not in this number"
                          if _stale else "")
                       + (f" (the books could not be read to compare: {_books_err})" if _books_err else ""))
                      if not _unmeasured(dist) else
                      "NOT MEASURED: no economic cycle has completed for this entity, so it has no "
                      "profitability record at all - which is not the same as a loss")}

    #  ── 2. USER SATISFACTION — explicit ratings only (Owner's ruling 2026-10-03c, option (a)) ───────
    try:
        from agentic_core.support import satisfaction
        s = satisfaction.summary()
        out["measures"]["user_satisfaction"] = {
            "value": s.get("mean"), "measured": s.get("state") == "measured",
            "basis": s.get("basis") or "no basis reported by the satisfaction store"}
    except Exception as exc:                                     # pragma: no cover - defensive
        out["measures"]["user_satisfaction"] = {
            "value": None, "measured": False,
            "basis": f"the satisfaction store could not be read: {type(exc).__name__}: {exc}"}

    #  ── 3. FOUNDER-ALIGNMENT — not implemented, and not invented here ───────────────────────────────
    #  §8 names it as continuously monitored. It is not implemented anywhere in this repository. This
    #  module reports that rather than substituting a proxy, because a proxy for a founder's judgement
    #  would be this platform deciding what its founder thinks, which is the one thing it must not do.
    out["measures"]["founder_alignment"] = {
        "value": None, "measured": False,
        "basis": ("NOT MEASURED: founder-alignment has no mechanism anywhere in this platform. §8 names "
                  "it as one of four continuously-monitored measures and nothing records it, so there is "
                  "no value to read. It is not substituted by a proxy: a stand-in for a founder's own "
                  "judgement would be this platform deciding what its founder thinks")}

    #  ── 4. LIVE COMPLIANCE — the entity's screening verdict; None means NEVER SCREENED ──────────────
    if entry is None:
        out["measures"]["live_compliance"] = {
            "value": None, "measured": False,
            "basis": (f"no entity {vsb_id!r} is on the living roster, so it carries no compliance verdict"
                      if not roster_error else
                      f"the living roster could not be read whole: {roster_error}")}
    else:
        comp = entry.get("compliance") or {}
        verdict = comp.get("verdict")
        out["measures"]["live_compliance"] = {
            "value": verdict, "measured": not _unmeasured(verdict),
            "screened_at": comp.get("screened_at"),
            "basis": (f"the entity's live compliance verdict: {verdict!r}"
                      if not _unmeasured(verdict) else
                      "NOT MEASURED: this entity has never been screened, so it has no verdict - an "
                      "unscreened entity is not a clean one")}

    return out


def assess(vsb_id: str) -> Dict[str, Any]:
    """Can selection act on this entity? It REFUSES while any of the four measures is unmeasured.

    Returns `status: NOT_ASSESSABLE` with `unmeasured` naming exactly which measures are missing, and a
    basis listing them. It never returns a score, a rank or a recommendation: the point of this function
    is that an absence stops selection rather than being read as either a pass or a failure.
    """
    m = measure_entity(vsb_id)
    unmeasured = [k for k in MEASURES if not m["measures"].get(k, {}).get("measured")]
    measured = [k for k in MEASURES if k not in unmeasured]

    if unmeasured:
        return {
            "vsb_id": vsb_id,
            "status": NOT_ASSESSABLE,
            "selected": None,
            "measures": m["measures"],
            "unmeasured": unmeasured,
            "measured": measured,
            "basis": (
                f"SELECTION REFUSES: {len(unmeasured)} of the {len(MEASURES)} measures §8 names are not "
                f"measured for this entity - " + ", ".join(unmeasured) + ". An entity nobody has measured "
                f"and an entity measured and found wanting are opposite facts, so no selection verdict is "
                f"produced for either. Each missing measure's own basis says why it is missing."),
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    return {
        "vsb_id": vsb_id,
        "status": ASSESSABLE,
        "selected": None,
        "measures": m["measures"],
        "unmeasured": [],
        "measured": measured,
        "basis": (
            f"all {len(MEASURES)} measures §8 names are measured for this entity, so selection is "
            f"assessable. No verdict is produced here: this function reports ASSESSABILITY, and what a "
            f"selection does with four measured values is a ruled decision rather than an arithmetic one."),
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


#  ── CLAUSE (4): THE HARD FLOOR ─────────────────────────────────────────────────────────────────────
#  Each floor is a LINE, not a score. A floor cannot be gamed by improving a number because it reads no
#  number to improve, and it creates no pressure toward a proxy because nothing is ranked against it.
#  A floor that cannot be assessed says so and never counts as passed - "a screen may refuse, never
#  clear" is this platform's rule and it applies to a floor exactly as it does to a screen.
_COMPLIANCE_FAILURE_VERDICTS = ("fail", "failed", "violation", "non_compliant", "noncompliant")


def negative_selection(vsb_id: str) -> Dict[str, Any]:
    """Flag an entity that is UNDER a hard floor. A flag is a review, never a retirement.

    Two floors are declared. One is assessable from what this platform records; the other is not, and
    says so rather than being quietly dropped — a floor list that counted an unassessable floor as
    passed would report a clean entity on a question nobody asked.
    """
    m = measure_entity(vsb_id)
    comp = m["measures"].get("live_compliance", {})
    floors: List[Dict[str, Any]] = []

    #  FLOOR 1 — fails compliance outright. Assessable: the verdict is recorded per entity.
    verdict = comp.get("value")
    if comp.get("measured"):
        failed = str(verdict).strip().lower() in _COMPLIANCE_FAILURE_VERDICTS
        floors.append({
            "floor": "live_compliance",
            "assessable": True,
            "under": failed,
            "basis": (f"the entity's recorded compliance verdict is {verdict!r}, which is a failure"
                      if failed else
                      f"the entity's recorded compliance verdict is {verdict!r}, which is not a failure")})
    else:
        floors.append({
            "floor": "live_compliance",
            "assessable": False,
            "under": None,
            "basis": ("NOT ASSESSABLE: this entity has no recorded compliance verdict, so whether it is "
                      "under this floor is unknown - and an unscreened entity is not a passing one")})

    #  FLOOR 2 — cannot meet its §8 obligations. NOT assessable, and the reason is named rather than
    #  substituted: there is no per-entity obligations ledger in this platform, so there is nothing to
    #  compare a balance against. Inventing a threshold would make this floor a proxy, which is the one
    #  thing clause (4) forbids.
    floors.append({
        "floor": "section_8_obligations",
        "assessable": False,
        "under": None,
        "basis": ("NOT ASSESSABLE: this platform records no per-entity obligations, so there is nothing "
                  "for a balance to fall short of. A threshold invented here would be a proxy, and a "
                  "floor exists precisely so that nothing optimises toward one")})

    breached = [f for f in floors if f.get("under") is True]
    unassessable = [f for f in floors if f.get("assessable") is False]
    status = FLAGGED if breached else NOT_FLAGGED

    return {
        "vsb_id": vsb_id,
        "status": status,
        "flagged": bool(breached),
        "floors": floors,
        "floors_breached": [f["floor"] for f in breached],
        "floors_not_assessable": [f["floor"] for f in unassessable],
        "retired": False,
        "basis": (
            (f"FLAGGED FOR REVIEW: this entity is under " + ", ".join(f["floor"] for f in breached)
             + ". A flag is a review and never a retirement - nothing here removes anything, and a "
               "removal is governed through Change Control."
             if breached else
             "not flagged: no assessable floor is breached.")
            + (" COVERAGE: " + ", ".join(f["floor"] for f in unassessable)
               + " could not be assessed, so this result does not clear the entity on "
               + ("them" if len(unassessable) > 1 else "it") + "."
               if unassessable else " Every declared floor was assessable.")),
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
