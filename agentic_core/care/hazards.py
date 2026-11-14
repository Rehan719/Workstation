"""W863 (FU-1056; OWNER RULING 2026-10-12) - THE CARE TOOLS' HAZARD LOG: an open log, one entry per hazard, each linked
to its guard or marked unguarded.

Each guard is named as module:symbol and resolved when the log is read, so a guard that has been renamed or removed is
reported as missing and its hazard counted unguarded: the log cannot claim protection the code no longer has. An entry
with no guard says UNGUARDED and why - an instruction written into a prompt is not a guard, because what a model
returns is not decided by what it was asked."""
from __future__ import annotations

import importlib
from typing import Any, Dict, List

HAZARDS: List[Dict[str, Any]] = [
    {"id": "CARE-HZ-01", "tool": "care-plan",
     "hazard": "the draft states medicines or doses, risk management, consent or capacity, or what to do in a crisis",
     "guard": "agentic_core.api.religion:_withhold_sections",
     "how": ("any section of those kinds the composer writes is cut from the text and named in it, against "
             "agentic_core.api.care.CLINICIAN_ONLY_SECTIONS; the prompt asks for them only as questions for a professional"),
     "residual": "a clinical statement written outside such a section, under another heading, is not cut"},
    {"id": "CARE-HZ-02", "tool": "care-plan",
     "hazard": "a history, a preference, a responsible person or a date is invented",
     "guard": None,
     "how": ("UNGUARDED: the prompt says to write NOT SUPPLIED and invent nothing, and nothing checks the draft against "
             "what was supplied"),
     "residual": None},
    {"id": "CARE-HZ-03", "tool": "care-plan",
     "hazard": "the draft is read as a care plan that someone reviewed",
     "guard": "agentic_core.api.care:CARE_PLAN_NOTE",
     "how": "a note that it is a draft organiser reviewed by nobody is appended to the text itself, so it travels with a copy",
     "residual": None},
    {"id": "CARE-HZ-04", "tool": "risk-assess",
     "hazard": "a score is stated that differs from the published table's",
     "guard": "agentic_core.care.scoring:compute_score",
     "how": ("the score is computed in-house from the published table and returned first, and the narrative is told "
             "not to recompute it"),
     "residual": "the narrative's own figures are not checked against the computed score"},
    {"id": "CARE-HZ-05", "tool": "risk-assess",
     "hazard": "a retired instrument (the falls count) is used",
     "guard": "agentic_core.care.scoring:FALLS_RETIRED",
     "how": "the request is refused, naming the replacement its publisher issued; nothing is computed or composed",
     "residual": None},
    {"id": "CARE-HZ-06", "tool": "risk-assess",
     "hazard": "an instrument this platform does not hold is interpreted under a name nobody published",
     "guard": "agentic_core.api.care:_TOOLS",
     "how": "an id the catalogue does not hold is refused, listing the tools it does hold",
     "residual": None},
    {"id": "CARE-HZ-07", "tool": "risk-assess",
     "hazard": "a score withheld on its owner's terms is computed",
     "guard": "agentic_core.care.scoring:withheld_sentence",
     "how": "the request is refused with the owner's terms; nothing is computed or composed",
     "residual": None},
    {"id": "CARE-HZ-08", "tool": "safeguarding",
     "hazard": "a person in immediate danger reads process guidance before calling for help",
     "guard": "agentic_core.api.care:IMMEDIATE_DANGER_FIRST",
     "how": "the emergency line opens the text, fixed and never composed, whatever served the rest",
     "residual": None},
    {"id": "CARE-HZ-09", "tool": "safeguarding",
     "hazard": "a concern about a child is handled on the adult route",
     "guard": "agentic_core.api.care:ADULT_ROUTE_ONLY",
     "how": "the text says, second, that this form is the adult route and where a child's concern goes instead",
     "residual": "nothing reads the concern to detect that it is about a child"},
    {"id": "CARE-HZ-10", "tool": "safeguarding",
     "hazard": "the route of another nation or framework is given as England's",
     "guard": "agentic_core.api.care:SAFEGUARDING_JURISDICTION",
     "how": "any other jurisdiction is refused, with where to turn instead",
     "residual": None},
    {"id": "CARE-HZ-11", "tool": "safeguarding",
     "hazard": "a specific individual is identified or accused as a conclusion",
     "guard": None,
     "how": "UNGUARDED: only the prompt asks for no individual to be identified or accused; nothing checks the text",
     "residual": None},
    {"id": "CARE-HZ-12", "tool": "handover",
     "hazard": "a detail is invented, or a part that was not supplied is filled",
     "guard": None,
     "how": "UNGUARDED: the prompt asks for NOT SUPPLIED and invents nothing; nothing checks the draft against what was supplied",
     "residual": None},
    {"id": "CARE-HZ-13", "tool": "handover",
     "hazard": "the draft is taken as sent, received or a clinical record",
     "guard": "agentic_core.api._ai_provenance:disclaimer_for",
     "how": "every answer says it has not been reviewed, sent or received and is not a clinical record",
     "residual": None},
    {"id": "CARE-HZ-14", "tool": "all four",
     "hazard": "a person's own text is read as an instruction, or a heading in it as a section the answer must have",
     "guard": "agentic_core.api.care:_material",
     "how": "what the person recorded is handed over as material, marked as data, and cut only at the helper (W859)",
     "residual": "a model may still follow an instruction inside the material; marking it as data does not prevent that"},
]


def _resolve(guard: str) -> bool:
    mod, _, name = str(guard).partition(":")
    try:
        return hasattr(importlib.import_module(mod), name)
    except Exception:                                   # noqa: BLE001 - a guard that cannot be imported is missing
        return False


def hazard_log() -> Dict[str, Any]:
    """The log with each guard resolved now: present, missing (and so counted unguarded), or none named."""
    rows = []
    for h in HAZARDS:
        present = _resolve(h["guard"]) if h.get("guard") else None
        rows.append({**h, "guard_present": present, "guarded": bool(present)})
    unguarded = [r["id"] for r in rows if not r["guarded"]]
    missing = [r["id"] for r in rows if r.get("guard") and r["guard_present"] is False]
    return {
        "hazards": rows, "count": len(rows), "unguarded": unguarded, "guard_missing": missing,
        "tools": sorted({r["tool"] for r in rows}),
        "basis": (f"{len(rows)} hazards across the Care tools: {len(rows) - len(unguarded)} linked to a guard found "
                  f"in the code now, {len(unguarded)} unguarded"
                  + (f" ({len(missing)} of them because the guard named is no longer present)" if missing else "")
                  + ". An instruction written into a prompt is not counted as a guard. Open log (Owner ruling "
                    "2026-10-12): an entry is added when a hazard is found."),
    }
