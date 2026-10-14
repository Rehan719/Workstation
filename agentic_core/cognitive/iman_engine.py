from typing import Dict, Any, Optional
from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import ConsultationRequest, ConsultationResponse, ValidationResult
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen
from agentic_core.cognitive.model_path import floor_basis, serve

def _marker(res: Dict) -> str:
    """The floor's answer, from what the check returned: a refusal with its reason, a figure only when one
    was computed, and otherwise that nothing was assessed (W730 - this said `Alignment: 0.0` for a refusal)."""
    if res.get("status") == "REJECTED":
        return f"Alignment: rejected ({res.get('reason')})"
    _v = res.get("alignment")
    if isinstance(_v, (int, float)) and not isinstance(_v, bool):
        return f"Alignment: {_v}"
    return "Alignment: not assessed - nothing here computes one"


class ImanEngine:
    def __init__(self, ueg=None):
        self.ueg = ueg
    """INTEGRATION: Coupled with Sulfur Cycle (Error value alignment)."""
    @constitutional_guard
    async def validate_values(self, action: Dict, sulfur_metrics: Optional[Dict] = None):
        if sulfur_metrics and sulfur_metrics.get("error_rate", 0.01) > 0.05:
            return {"status": "REJECTED", "reason": "High toxicity"}
        #  W730 (FU-854) - this returned one fixed alignment for any action. Nothing here computes one,
        #  so the key stays (a reader indexing it does not break) and holds None, with the reason beside it.
        return {"status": "NOT_ASSESSED", "alignment": None,
                "alignment_basis": ("NOT ASSESSED: nothing here computes an alignment - this engi"
                                    "ne has no instrument for one, so it returns no figure rather than a fixed one")}

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        """Standardized Mushawara consultation implementation."""
        res = await self.validate_values({"query": request.query})
        #  W560 (FU-275) — THE MODEL PATH. Measured before this round: a grep for a gateway,
        #  an orchestrator or a generate call across all six engines returned ZERO, so the
        #  architecture routed and the cognition did not compute. The engine asks the tier
        #  router now; on this machine the walk ends at the deterministic floor, and the
        #  difference from before is that it can say WHY rather than simply not having asked.
        _text, _prov = await serve("iman", request.query)
        _resp = ConsultationResponse(
            engine="iman",
            #  the model's text when one served, and the engine's own marker when none did —
            #  never a blend, so a reader is not left guessing which they are looking at
            answer=(_text if _text else _marker(res)),
            # P3.12 - the bar permits a REFUSAL instead of a computed value, and a required numeric
            # field is what forced the invention. None means nothing computed it.
            confidence=None,
            #  W560 — THE OLD SENTENCE HERE SAID THIS ENGINE HAS NO PATH TO A MODEL. That was
            #  measured and true when P3.12 wrote it, and it stopped being true in W560; a
            #  basis that keeps asserting a fixed absence after the absence is gone is the
            #  stale-claim defect this programme removes everywhere else. Still no confidence:
            #  nothing computes one, and having a path is not a reason to start inventing it.
            confidence_basis=floor_basis(_prov),
            served_by=(_prov.get("served_by") or "native-fixed-marker"),
            is_external=bool(_prov.get("is_external")),
            constitutional_validation=ValidationResult(),
            reasoning_trace="Ethical value alignment and conviction via Iman Engine."
        )
        #  P3.28 clause (1) — the verdict is COMPUTED by gaas.v5's own checks over the request and
        #  this answer, replacing a literal that said no check ran. A screen may refuse, never clear:
        #  a non-refusal keeps passed=None and states its coverage (consultation/constitutional_screen.py).
        _resp.constitutional_validation = _constitutional_screen("iman", request.query, _resp.answer)
        return _resp
