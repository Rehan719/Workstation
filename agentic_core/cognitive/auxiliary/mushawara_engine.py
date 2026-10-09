"""Mushāwara — deliberation: consensus counted across DISTINCT engine opinions, or a refusal.

P3.16 (architecture doc C6). Mushāwara is gate 1 of the constitutional clearance chain, which consults it
across three engines and until W525 indexed its `status` field directly and RAISED KeyError when it was
absent — neither clearing nor refusing. The gate was fixed there; this is the engine behind it, which did not
exist. NOT to be confused with Mushāhida, MJM's observation stage: one letter apart in transliteration,
different tiers, different work.

WHAT IT COMPUTES. Opinions are grouped by the engine that gave them, abstentions are separated from
positions, and the status is APPROVED only when at least the required number of DISTINCT engines took a
position and none of them objected. Every count is reported so a reader can see what the status was computed
over.

WHAT IT REFUSES. No opinions; fewer DISTINCT engines than required; an opinion with no engine named; an
unrecognised verdict. The quorum is NEVER defaulted — the architecture names three, and that number is
reported as the architecture's stated minimum rather than silently assumed, because the number of agreeing
parties IS the verdict.

ABSTENTIONS DO NOT COUNT AS AGREEMENT. Three abstentions are three engines that did not approve, so they
cannot clear this gate; a count of "no objections" over nobody taking a position is how a quorum becomes a
formality.
"""
from typing import Any, Dict, List

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen

ENGINE_ID = "mushawara"
BIOLOGICAL_ANALOGUE = "deliberative_council"

#  The architecture states "deliberative consensus (>= 3 engines)". Named, reported, and overridable by the
#  caller — but never defaulted silently, because the number of agreeing parties is the whole verdict.
ARCHITECTURE_MINIMUM_ENGINES = 3
VERDICTS = ("approve", "object", "abstain")


class MushawaraEngine:
    """Deliberation. Counts distinct positions; approves only on positions actually taken."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def deliberate(self, opinions: Any, minimum_engines: Any = None) -> Dict[str, Any]:
        if opinions is None:
            return {"assessable": False,
                    "basis": ("no opinions were supplied, so there is no deliberation to assess. An absent "
                              "record is not a consensus")}
        if not isinstance(opinions, list) or not opinions:
            return {"assessable": False,
                    "basis": f"opinions must be a non-empty list; received {type(opinions).__name__}"}

        minimum = (minimum_engines if isinstance(minimum_engines, int)
                   and not isinstance(minimum_engines, bool) and minimum_engines > 0
                   else ARCHITECTURE_MINIMUM_ENGINES)
        minimum_source = ("stated by the caller" if minimum is not ARCHITECTURE_MINIMUM_ENGINES
                          or isinstance(minimum_engines, int) and not isinstance(minimum_engines, bool)
                          else f"the architecture's stated minimum of {ARCHITECTURE_MINIMUM_ENGINES}")

        positions: Dict[str, str] = {}
        problems: List[str] = []
        for i, op in enumerate(opinions):
            if not isinstance(op, dict):
                problems.append(f"opinion at position {i} is not a record")
                continue
            engine = str(op.get("engine") or "").strip()
            verdict = op.get("verdict")
            if not engine:
                problems.append(f"opinion at position {i} names no engine, so it cannot be counted")
                continue
            if verdict not in VERDICTS:
                problems.append(f"engine {engine!r} gave verdict {verdict!r}, not one of {list(VERDICTS)}")
                continue
            positions[engine] = verdict            # one position per engine; a later one supersedes

        if problems:
            return {"assessable": False, "basis": "; ".join(problems)}

        approvals = sorted(e for e, v in positions.items() if v == "approve")
        objections = sorted(e for e, v in positions.items() if v == "object")
        abstentions = sorted(e for e, v in positions.items() if v == "abstain")
        took_position = approvals + objections

        #  APPROVED needs enough engines to have taken a position AND nobody to have objected. Abstentions
        #  are counted and reported but never contribute to agreement.
        enough = len(took_position) >= minimum
        approved = enough and not objections

        return {
            "assessable": True,
            "status": "APPROVED" if approved else "BLOCKED",
            "approved": approved,
            "engines_heard": sorted(positions),
            "engines_took_position": took_position,
            "approvals": approvals,
            "objections": objections,
            "abstentions": abstentions,
            "minimum_engines": minimum,
            "minimum_engines_source": minimum_source,
            "basis": (
                f"{len(approvals)} approval(s) and {len(objections)} objection(s) from "
                f"{len(took_position)} engine(s) that took a position, against a minimum of {minimum}"
                + (f"; {len(abstentions)} abstention(s) counted but not treated as agreement"
                   if abstentions else "")
                + ("" if enough else
                   f". BLOCKED: only {len(took_position)} engine(s) took a position")
                + (f". BLOCKED: {objections} objected" if objections else "")),
            "abstentions_are_not_agreement": (
                "an engine that abstained did not approve. Counting 'no objections' over nobody taking a "
                "position is how a quorum becomes a formality"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.deliberate(ctx.get("opinions"), ctx.get("minimum_engines"))
        ok = res.get("assessable") is True
        answer = (f"Not assessable: {res['basis']}" if not ok else
                  f"{res['status']}: {res['basis']}")
        _resp = ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            confidence=None,
            confidence_basis=(
                "not applicable: a consensus is a count over the positions supplied, not an estimate"
                if ok else f"nothing was counted: {res['basis']}"),
            served_by="native-computed" if ok else "native-refused",
            is_external=False,
            constitutional_validation=ValidationResult(),
            reasoning_trace=res["basis"],
            metadata=res,
        )
        #  P3.28 clause (1) — the verdict is COMPUTED by gaas.v5's own checks over the request and
        #  this answer, replacing a literal that said no check ran. A screen may refuse, never clear:
        #  a non-refusal keeps passed=None and states its coverage (consultation/constitutional_screen.py).
        _resp.constitutional_validation = _constitutional_screen(ENGINE_ID, request.query, _resp.answer)
        return _resp
