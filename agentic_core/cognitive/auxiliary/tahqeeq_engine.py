"""Tahqeeq — output verification against the hard constraints it is GIVEN, or a refusal naming what was missing.

P3.16 (architecture doc C6). Tahqeeq is gate 5 of the constitutional clearance chain, and until W525 that gate
read `verified` with a default that meant approval, so an engine returning nothing cleared it. The gate was
fixed there; this is the engine behind it, which did not exist at all — `EngineType.TAHQEEQ` was declared and
had no module, and before W523 the enum did not even declare it.

WHAT IT COMPUTES. Each supplied constraint is evaluated against the output and reported individually with its
own verdict and reason. `verified` is the conjunction: true only when every constraint passed. Nothing is
inferred about constraints that were not supplied.

WHAT IT REFUSES. An absent or empty constraint list — because "verified against nothing" is the shape that
made gate 5 approve by default, and a verification with no criteria is not a weak verification, it is not one.
An unknown constraint KIND is also a refusal rather than a skip: silently ignoring a constraint a caller asked
for would report a pass over a check that never ran.
"""
from typing import Any, Dict, List

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)

ENGINE_ID = "tahqeeq"
BIOLOGICAL_ANALOGUE = "prefrontal_verification"

#  The kinds this engine knows how to evaluate. A kind outside this set is a REFUSAL, never a skip.
KINDS = ("required_field", "forbidden_text", "max_chars", "min_chars", "non_empty")


class TahqeeqEngine:
    """Output verification. Reports per constraint; verifies only what it was asked to check."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def verify_output(self, output: Any, constraints: Any) -> Dict[str, Any]:
        if constraints is None:
            return {"assessable": False,
                    "basis": ("no constraints were supplied, so there is nothing to verify against. "
                              "A verification with no criteria is not a weak verification - it is not one, "
                              "and reporting it as a pass is what made this chain's gate 5 approve by "
                              "default before W525")}
        if not isinstance(constraints, list) or not constraints:
            return {"assessable": False,
                    "basis": (f"constraints must be a non-empty list; received "
                              f"{type(constraints).__name__} with "
                              f"{len(constraints) if isinstance(constraints, list) else 'no'} entries")}

        unknown = [c.get("kind") if isinstance(c, dict) else repr(c) for c in constraints
                   if not isinstance(c, dict) or c.get("kind") not in KINDS]
        if unknown:
            return {"assessable": False,
                    "basis": (f"constraint kind(s) {unknown} are not implemented by this engine "
                              f"(known: {list(KINDS)}). Skipping an unknown constraint would report a pass "
                              "over a check that never ran")}

        text = output if isinstance(output, str) else str(output or "")
        results: List[Dict[str, Any]] = []

        for c in constraints:
            kind = c["kind"]
            if kind == "required_field":
                field = c.get("field")
                present = isinstance(output, dict) and field in output
                results.append({"kind": kind, "field": field, "passed": bool(present),
                                "reason": (f"field {field!r} is present" if present else
                                           f"field {field!r} is absent from the output")})
            elif kind == "forbidden_text":
                needle = str(c.get("text") or "")
                hit = bool(needle) and needle in text
                results.append({"kind": kind, "text": needle, "passed": not hit,
                                "reason": (f"forbidden text {needle!r} appears in the output" if hit else
                                           f"forbidden text {needle!r} does not appear")})
            elif kind == "max_chars":
                limit = c.get("limit")
                ok = isinstance(limit, int) and len(text) <= limit
                results.append({"kind": kind, "limit": limit, "measured": len(text), "passed": bool(ok),
                                "reason": f"{len(text)} characters against a maximum of {limit}"})
            elif kind == "min_chars":
                limit = c.get("limit")
                ok = isinstance(limit, int) and len(text) >= limit
                results.append({"kind": kind, "limit": limit, "measured": len(text), "passed": bool(ok),
                                "reason": f"{len(text)} characters against a minimum of {limit}"})
            else:                                       # non_empty
                ok = bool(text.strip())
                results.append({"kind": kind, "passed": ok,
                                "reason": ("the output holds characters" if ok else
                                           "the output is empty or whitespace only")})

        failed = [r for r in results if not r["passed"]]
        return {
            "assessable": True,
            "verified": not failed,
            "constraints_checked": len(results),
            "constraints_failed": len(failed),
            "results": results,
            "basis": (f"{len(results) - len(failed)} of {len(results)} supplied constraint(s) passed"
                      + (f"; failed: {[r['kind'] for r in failed]}" if failed else "")),
            "what_this_does_not_establish": (
                "anything about constraints that were not supplied. This verifies the criteria it was "
                "given, so `verified: true` means 'every criterion the caller named was met', not 'this "
                "output is correct'"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.verify_output(ctx.get("output", request.query), ctx.get("constraints"))
        ok = res.get("assessable") is True
        answer = (f"Not assessable: {res['basis']}" if not ok else
                  f"{'VERIFIED' if res['verified'] else 'NOT verified'}: {res['basis']}")
        return ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            confidence=None,
            confidence_basis=(
                "not applicable: verification is a conjunction of the supplied criteria, not an estimate"
                if ok else f"nothing was verified: {res['basis']}"),
            served_by="native-computed" if ok else "native-refused",
            is_external=False,
            constitutional_validation=ValidationResult(
                passed=None,
                basis=("no constitutional check ran: this engine verifies an output against the caller's "
                       "constraints and performs no constitutional validation of its own")),
            reasoning_trace=res["basis"],
            metadata=res,
        )
