"""Tawazun — balance as a Pareto frontier over NAMED objectives, or a refusal that says what was missing.

P3.13. The archived version (_archive/jules-unwired/agentic_core/cognitive/meta/tawazun_engine.py, 7 lines)
returned `{"balance_score": 0.95, "resource_allocation": "OPTIMAL"}` — a graded literal and a superlative over
nothing at all. That is the defect class P3.12 removed from the six foundational engines in W520, so it is NOT
recovered; only its metadata is kept (engine id, the hypothalamus analogue, constitutional bindings 7/12/16).

WHAT IT COMPUTES. The non-dominated set of the candidates it is given, under the directions it is given. One
candidate dominates another when it is no worse on every objective and strictly better on at least one. That
is a decision procedure over the inputs, not an estimate — which is why there is no balance_score here: a
frontier is a SET, and collapsing it to a single number is exactly what invited the literal.

WHAT IT REFUSES, each naming what was missing: absent objectives; absent candidates; an objective with no
stated direction (a direction cannot be guessed, because guessing it INVERTS the frontier); a candidate with
no numeric value for an objective. An empty candidate list is a REFUSAL rather than an empty frontier,
because "nothing dominates anything" and "nothing was supplied" are different facts and a reader cannot tell
them apart from an empty list.
"""
from typing import Any, Dict, List, Optional

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)

ENGINE_ID = "tawazun"
BIOLOGICAL_ANALOGUE = "hypothalamus"
CONSTITUTIONAL_BINDING = [7, 12, 16]
_DIRECTIONS = ("max", "min")


class TawazunEngine:
    """Balance. Computes a frontier or says why it cannot; it never scores."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def balance(self, objectives: Any, candidates: Any) -> Dict[str, Any]:
        """The frontier, or `assessable: False` with every problem found — not just the first."""
        problems: List[str] = []

        if not isinstance(objectives, list) or not objectives:
            problems.append("no objectives were supplied, so there is nothing to balance against")
        if not isinstance(candidates, list) or not candidates:
            problems.append("no candidates were supplied, so there is no set to take a frontier of")

        named: List[tuple] = []
        if isinstance(objectives, list):
            for obj in objectives:
                if not isinstance(obj, dict) or not str(obj.get("name") or "").strip():
                    problems.append(f"an objective has no name: {obj!r}")
                    continue
                name = str(obj["name"]).strip()
                if obj.get("direction") not in _DIRECTIONS:
                    problems.append(
                        f"objective {name!r} states no direction (expected one of {list(_DIRECTIONS)}); "
                        "a direction cannot be assumed, because assuming it inverts the frontier")
                    continue
                named.append((name, obj["direction"]))

        if isinstance(candidates, list) and named:
            for idx, cand in enumerate(candidates):
                if not isinstance(cand, dict):
                    problems.append(f"candidate at position {idx} is not a record: {cand!r}")
                    continue
                for name, _d in named:
                    val = cand.get(name)
                    if isinstance(val, bool) or not isinstance(val, (int, float)):
                        problems.append(
                            f"candidate {cand.get('id', idx)!r} has no numeric value for objective {name!r}")

        if problems:
            return {"assessable": False, "basis": "; ".join(problems)}

        ids = [str(c.get("id") or f"candidate-{i}") for i, c in enumerate(candidates)]

        def dominates(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
            strictly_better = False
            for name, direction in named:
                av, bv = a[name], b[name]
                if direction == "min":
                    av, bv = -av, -bv
                if av < bv:
                    return False
                if av > bv:
                    strictly_better = True
            return strictly_better

        frontier = [ids[i] for i, c in enumerate(candidates)
                    if not any(dominates(o, c) for j, o in enumerate(candidates) if j != i)]
        dominated = [i for i in ids if i not in frontier]

        return {
            "assessable": True,
            "frontier": frontier,
            "dominated": dominated,
            "objectives": [{"name": n, "direction": d} for n, d in named],
            "basis": (f"the non-dominated set of {len(candidates)} candidate(s) under {len(named)} "
                      f"objective(s), by pairwise dominance: {len(frontier)} on the frontier, "
                      f"{len(dominated)} dominated"),
            "what_this_is_not": ("a frontier is a set of incomparable options, not a ranking and not a "
                                 "score: nothing here says which member of the frontier is best, because "
                                 "that is the trade-off the caller has to make"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.balance(ctx.get("objectives"), ctx.get("candidates"))
        ok = res.get("assessable") is True

        if not ok:
            answer = f"Not assessable: {res['basis']}"
        elif res["frontier"]:
            answer = f"Frontier ({len(res['frontier'])} of {len(res['frontier']) + len(res['dominated'])}): " \
                     + ", ".join(res["frontier"])
        else:
            answer = "Frontier: empty"

        return ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            # A frontier is computed, but it is not an estimate, so there is no confidence to report.
            # Putting a number here would be describing nothing — the defect this engine was rebuilt to avoid.
            confidence=None,
            confidence_basis=(
                "not applicable: a Pareto frontier is a decision procedure over the inputs given rather "
                "than an estimate, so there is no confidence to state. A number here would describe nothing"
                if ok else f"nothing was computed: {res['basis']}"),
            served_by="native-computed" if ok else "native-refused",
            is_external=False,
            constitutional_validation=ValidationResult(
                passed=None,
                basis=("no constitutional check ran: this engine computes a frontier and performs no "
                       "constitutional validation, so neither a pass nor a failure is claimed. Its "
                       f"declared bindings are articles {CONSTITUTIONAL_BINDING} and nothing enforces them "
                       "here")),
            reasoning_trace=res["basis"],
            metadata=res,
        )
