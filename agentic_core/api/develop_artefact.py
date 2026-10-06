"""P3.1 (§4.6 Develop) — the buildable artefact, and a check that can actually FAIL.

DESTINATION: agentic_core/api/develop_artefact.py (new file, LF). Prepared in W596's suite wait.

WHY A COSTED BILL OF MATERIALS. The item names three acceptable artefacts — a costed bill of materials, a
runnable prototype spec, or a parameterised model via factory/forge. There is no `factory` or `forge`
package in this repository (measured W596), and a "runnable prototype spec" has no checkable property
without a runner. A BOM has one that is arithmetic: DO THE LINE ITEMS SUM TO THE STATED TOTAL. That is a
pass/fail over the artefact's content, which is what clause (3) demands.

WHY THAT MATTERS MORE THAN IT SOUNDS. Every existing journey stage is verified by `_verify_stage`, whose own
docstring records that its proxies CANNOT FAIL on floor output: the floor emits the headings it was asked
for, so coverage is always 1.0 and structure always ≥1.0, and the composite lands exactly on the threshold.
This check reads the artefact instead, so it can fail on a model-served BOM whose numbers do not add up —
the first verification in this journey that fails on SUBSTANCE rather than on structure.

AND THE FLOOR REFUSES. The deterministic floor composes prose from labelled fields; it cannot cost a
component. Clause (4) requires it to say "not buildable on the floor" and record NO pass, so a floor run
produces no artefact and the stage reports that — `verified: None`, which is this journey's existing
not-assessable shape rather than a new one.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple

NOT_BUILDABLE_ON_THE_FLOOR = "not buildable on the floor"

#  a BOM line: a quantity, a unit cost and a line total. Parsed from the model's own table or list.
_LINE = re.compile(
    r"^\s*[-*|]?\s*(?P<item>[^|]{2,80}?)\s*[|:]\s*"
    r"(?P<qty>\d+(?:\.\d+)?)\s*[|x×]\s*"
    r"(?P<unit>\d+(?:[,\s]\d{3})*(?:\.\d+)?)\s*[|]?\s*"
    r"(?P<total>\d+(?:[,\s]\d{3})*(?:\.\d+)?)?\s*\|?\s*$",
    re.M,
)
_STATED_TOTAL = re.compile(r"(?:total|sum)\D{0,20}?(\d+(?:[,\s]\d{3})*(?:\.\d+)?)", re.I)


def _num(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    cleaned = re.sub(r"[,\s]", "", raw)
    try:
        return float(cleaned)
    except ValueError:
        return None


def _store():
    from agentic_core.config import data_path
    return data_path("journey_artefacts")


def _path(journey_id: str):
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(journey_id or "unknown"))[:80]
    return _store() / f"{safe}.json"


def parse_bom(text: str) -> Dict[str, Any]:
    """Pull the line items and the stated total out of a develop stage's own text.

    Returns the parse, never a verdict. Parsing and checking are kept apart because a parse that found
    nothing and a BOM whose numbers disagree are different facts, and only the second is a failure.
    """
    lines: List[Dict[str, Any]] = []
    for m in _LINE.finditer(text or ""):
        qty, unit = _num(m.group("qty")), _num(m.group("unit"))
        if qty is None or unit is None:
            continue
        stated = _num(m.group("total"))
        lines.append({"item": m.group("item").strip(" -*|"), "quantity": qty, "unit_cost": unit,
                      "line_total_stated": stated, "line_total_computed": round(qty * unit, 2)})
    st = _STATED_TOTAL.search(text or "")
    return {"lines": lines, "stated_total": _num(st.group(1)) if st else None,
            "computed_total": round(sum(ln["line_total_computed"] for ln in lines), 2) if lines else None}


def check_bom(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """A REAL pass/fail over the artefact's own arithmetic — three states, never a score.

      · no lines parsed        → NOT ASSESSABLE (there is no bill of materials to check)
      · no stated total        → NOT ASSESSABLE (nothing claims a total, so nothing can disagree)
      · stated == computed     → PASS
      · stated != computed     → FAIL, naming both figures

    A tolerance is deliberately NOT applied beyond rounding to the penny: inventing one would make this a
    threshold over a number, and a threshold over a number is the gate that cannot refuse.
    """
    lines, stated, computed = parsed.get("lines") or [], parsed.get("stated_total"), parsed.get("computed_total")
    if not lines:
        return {"passed": None, "basis": ("no bill of materials was found in this stage's output, so there "
                                          "is no artefact to check - which is not the same as an artefact "
                                          "that failed")}
    if stated is None:
        return {"passed": None, "lines": len(lines), "computed_total": computed,
                "basis": (f"{len(lines)} line item(s) were parsed and they sum to {computed}, but the "
                          f"output states no total, so there is no claim for the arithmetic to disagree "
                          f"with")}
    ok = abs(round(stated, 2) - round(computed, 2)) < 0.005
    #  a line whose own stated total disagrees with its quantity × unit cost is named too: the overall sum
    #  can be right while an individual line is wrong, and reporting only the total would hide it
    bad_lines = [ln["item"] for ln in lines
                 if ln["line_total_stated"] is not None
                 and abs(round(ln["line_total_stated"], 2) - ln["line_total_computed"]) >= 0.005]
    return {
        "passed": bool(ok and not bad_lines),
        "lines": len(lines),
        "stated_total": stated,
        "computed_total": computed,
        "lines_whose_own_total_disagrees": bad_lines,
        "basis": (
            (f"the {len(lines)} line item(s) sum to {computed}, which matches the stated total"
             + (f" - but {len(bad_lines)} line(s) state a total that disagrees with their own quantity x "
                f"unit cost ({bad_lines[:4]}), so the bill is not internally consistent" if bad_lines
                else "") )
            if ok else
            (f"the {len(lines)} line item(s) sum to {computed} and the output states {stated} - the bill "
             f"does not add up, so this is a FAIL rather than a missing check")),
    }


def record(journey_id: str, text: str, floor_served: bool) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Produce, store and check the develop artefact. Returns (artefact, verification).

    THE ARTEFACT IS STORED so clause (2) can be satisfied by its EXISTENCE rather than by the stage having
    run — the item is explicit that those are different things.
    """
    from agentic_core.config import atomic_write_json, store_lock
    if floor_served:
        verification = {
            "verified": None, "ran": True, "checks": "none",
            "artefact": None,
            "basis": (f"{NOT_BUILDABLE_ON_THE_FLOOR}: the deterministic floor composes prose from the "
                      f"request's labelled fields and cannot cost a component, so no bill of materials "
                      f"was produced and NO pass is recorded. This is not a failure of the solution - it "
                      f"is this platform saying what it cannot do without an owned model."),
        }
        return ({}, verification)

    parsed = parse_bom(text)
    checked = check_bom(parsed)
    artefact = {
        "journey_id": str(journey_id),
        "kind": "costed_bill_of_materials",
        "produced_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **parsed,
        "check": checked,
    }
    try:
        p = _path(journey_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        with store_lock(p):
            atomic_write_json(p, artefact)
        artefact["stored_at"] = str(p.name)
    except Exception as e:                           # noqa: BLE001 — a storage fault is SAID, not hidden
        artefact["stored_at"] = None
        artefact["storage_error"] = e.__class__.__name__

    verification = {
        #  PASS/FAIL FROM THE ARTEFACT'S OWN ARITHMETIC, not from a proxy over headings. Every other stage
        #  in this journey is verified by section coverage, whose own docstring records that it cannot fail
        #  on floor output; this one can fail on a model-served bill whose numbers do not add up.
        "verified": checked["passed"],
        "ran": True,
        "checks": "bill-of-materials arithmetic",
        "artefact": {k: artefact.get(k) for k in ("kind", "stored_at", "lines", "stated_total",
                                                  "computed_total")},
        "basis": checked["basis"],
    }
    return (artefact, verification)


def load(journey_id: str) -> Optional[Dict[str, Any]]:
    """The stored artefact, or None. Clause (2) is checked by this returning something."""
    p = _path(journey_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                # noqa: BLE001
        return None
