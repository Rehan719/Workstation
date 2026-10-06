"""Mudrik — the bridge to the transformation surface: it SHAPES a handover and refuses to carry an uncleared one.

P3.16 (architecture doc C6: "Mudrik as the bridge to the transformation surface"). Measured W527: there is no
`@router` route for a transformation surface, and `api/change_control.py` records that "the transformation
pipeline" calls IT. So the surface a cleared cognitive emission crosses into is the CHANGE CONTROL AGENCY,
which the delivery plan already names as the single governance path (P3.19's bar: "one governance path (the
existing Change Control Agency)"). This engine bridges to that, and to nothing else.

WHAT IT COMPUTES. A change-control-shaped proposal from an emission and the clearance result that accompanies
it, naming which gates cleared it and carrying their attestations through.

WHAT IT REFUSES, and this is the engine's reason to exist: an emission with NO clearance, or one whose
clearance did not pass. A bridge that carries an uncleared emission into governance is worse than no bridge —
it launders the absence of a decision into the appearance of one. It also refuses a clearance whose gate
records are missing, because "passed" with no gate record is a verdict with nothing behind it.

IT DOES NOT SUBMIT, and says so on every result. Shaping a proposal is a computation; submitting one to
governance is an act with consequences, and it belongs to the caller as an explicit step rather than to a
bridge as a side effect. A handover that happened invisibly is how a governance path stops being a decision.
"""
from typing import Any, Dict, List

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen

ENGINE_ID = "mudrik"
BIOLOGICAL_ANALOGUE = "corpus_callosum_bridge"
TARGET_SURFACE = "change_control_agency"


class MudrikEngine:
    """The bridge. Shapes a handover to Change Control; never carries an uncleared emission, never submits."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def bridge(self, emission: Any, clearance: Any) -> Dict[str, Any]:
        if not isinstance(emission, dict) or not emission:
            return {"assessable": False,
                    "basis": (f"no emission to carry (received {type(emission).__name__}), so there is "
                              "nothing to hand over")}
        if clearance is None:
            return {"assessable": False,
                    "basis": ("the emission carries NO clearance result, so it has not been through the "
                              "constitutional chain. A bridge that carries an uncleared emission into "
                              "governance launders the absence of a decision into the appearance of one")}
        if not isinstance(clearance, dict):
            return {"assessable": False,
                    "basis": f"the clearance result is a {type(clearance).__name__}, not a record"}

        gates = clearance.get("gates")
        if not isinstance(gates, list) or not gates:
            return {"assessable": False,
                    "basis": ("the clearance result carries no per-gate record, so 'passed' would be a "
                              "verdict with nothing behind it. P3.14 made the chain record every gate; a "
                              "result without those records did not come from it")}

        if clearance.get("passed") is not True:
            blocked = [g.get("gate") for g in gates if g.get("verdict") == "blocked"]
            return {"assessable": True,
                    "carried": False,
                    "basis": ("the emission was NOT cleared, so it is not carried. Blocked at: "
                              f"{blocked or 'unknown gate'}. Reason: {clearance.get('reason')}"),
                    "target_surface": TARGET_SURFACE,
                    "submitted": False,
                    "submission_basis": "nothing was shaped, because nothing is carried"}

        cleared = [g.get("gate") for g in gates if g.get("verdict") == "cleared"]
        not_evaluated = [g.get("gate") for g in gates if g.get("verdict") == "not_evaluated"]
        attestations = clearance.get("attestations") or {}
        signed = bool(clearance.get("attestations_signed"))

        proposal: Dict[str, Any] = {
            "target_surface": TARGET_SURFACE,
            "emission_id": emission.get("id"),
            "kind": emission.get("kind") or "cognitive_emission",
            "summary": str(emission.get("summary") or emission.get("content") or "")[:500],
            "cleared_by_gates": cleared,
            "gates_not_evaluated": not_evaluated,
            "attestations": attestations,
            "attestations_signed": signed,
            "attestations_basis": clearance.get("attestations_basis"),
        }

        return {
            "assessable": True,
            "carried": True,
            "proposal": proposal,
            "gates_cleared": len(cleared),
            "basis": (f"a proposal for the {TARGET_SURFACE} shaped from an emission cleared by "
                      f"{len(cleared)} gate(s)"
                      + ("" if signed else
                         "; its attestations are NOT SIGNED, because no attestation key is configured - "
                         "carried through rather than hidden, so governance sees what it is receiving")),
            #  stated on every result, not only in the docstring
            "submitted": False,
            "submission_basis": (
                "this engine SHAPES a handover and does not perform one. Submitting to governance is an act "
                "with consequences and belongs to the caller as an explicit step; a handover that happened "
                "invisibly is how a governance path stops being a decision"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.bridge(ctx.get("emission"), ctx.get("clearance"))
        ok = res.get("assessable") is True
        if not ok:
            answer = f"Not assessable: {res['basis']}"
        elif res.get("carried"):
            answer = f"Proposal shaped (NOT submitted): {res['basis']}"
        else:
            answer = f"Not carried: {res['basis']}"
        _resp = ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            confidence=None,
            confidence_basis=(
                "not applicable: shaping a handover is a transformation of the inputs given, not an estimate"
                if ok else f"nothing was shaped: {res['basis']}"),
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
