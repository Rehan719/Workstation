"""Tafakkur — drift measured against a RECORDED baseline, or a refusal when there is no baseline to measure from.

P3.13. The archived version (_archive/jules-unwired/agentic_core/cognitive/meta/tafakkur_engine.py, 31 lines)
wrote the drift formula in a COMMENT and then assigned `drift = 0.003` — the formula sat directly above the
literal that replaced it — and returned a `loeb_proof` of three strings plus `lob_stable: True`. A proof is
not a label. None of that is recovered; only the metadata is kept (engine id, the default-mode-network
analogue, bindings 11/13/20).

WHAT IT COMPUTES: relative Euclidean drift over the keys the baseline and the current state SHARE, which is
`||current - baseline|| / ||current||`. The shared-key set is reported, because a drift computed over two of
forty keys is a different fact from one computed over all forty, and a bare number cannot say which it is.

WHAT IT REFUSES: no baseline recorded (the COMMON case — it is an answer, not a failure, and it is
first-class here rather than a fallback); no current state; no shared numeric keys; and a current state whose
norm is zero, which leaves a relative measure with no denominator.

THE THRESHOLD IS A DEFAULT UNTIL TUNED, and the record says so on every result. Nothing in this repository has
calibrated a drift threshold against its own history, so `stable` below the default is an aspiration rather
than a measurement — and the result states that in the same breath as the verdict.

NO FIXPOINT PROOF IS PERFORMED. There is no Löb-stability or mu-calculus check here, and the result says so
rather than leaving a reader to assume the engine's name implies one.
"""
import math
from typing import Any, Dict, List

from agentic_core.biomimicry.cycles.utils import constitutional_guard
from agentic_core.consultation.interface import (ConsultationRequest, ConsultationResponse,
                                                 ValidationResult)
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen

ENGINE_ID = "tafakkur"
BIOLOGICAL_ANALOGUE = "default_mode_network_audit"
CONSTITUTIONAL_BINDING = [11, 13, 20]

#  A default, not a tuned value. Named so a reader can find every use of it.
_DEFAULT_STABLE_BELOW = 0.01


def _numeric(d: Any) -> Dict[str, float]:
    if not isinstance(d, dict):
        return {}
    return {k: float(v) for k, v in d.items()
            if not isinstance(v, bool) and isinstance(v, (int, float))}


class TafakkurEngine:
    """Reflection as a drift measurement. Refuses without a baseline; claims no proof."""

    def __init__(self, ueg=None):
        self.ueg = ueg

    @constitutional_guard
    async def measure_drift(self, baseline: Any, current: Any, stable_below: Any = None) -> Dict[str, Any]:
        if baseline is None:
            return {"assessable": False,
                    "basis": ("no baseline is recorded, so there is nothing to measure drift FROM. This is "
                              "the common case for a state this platform has not yet snapshotted, and it is "
                              "an answer rather than a failure")}
        if current is None:
            return {"assessable": False, "basis": "no current state was supplied, so there is nothing to compare"}

        b, c = _numeric(baseline), _numeric(current)
        if not b:
            return {"assessable": False,
                    "basis": "the baseline holds no numeric values, so no distance can be computed from it"}
        if not c:
            return {"assessable": False,
                    "basis": "the current state holds no numeric values, so no distance can be computed to it"}

        shared: List[str] = sorted(set(b) & set(c))
        if not shared:
            return {"assessable": False,
                    "basis": (f"the baseline and the current state share no numeric key "
                              f"(baseline has {len(b)}, current has {len(c)}), so there is no common "
                              "dimension to measure drift along")}

        denom = math.sqrt(sum(c[k] ** 2 for k in shared))
        if denom == 0.0:
            return {"assessable": False,
                    "basis": ("every shared value in the current state is zero, so a RELATIVE drift has no "
                              "denominator. An absolute distance would be a different quantity and is not "
                              "reported under this name")}

        numer = math.sqrt(sum((c[k] - b[k]) ** 2 for k in shared))
        drift = numer / denom

        declared = stable_below is not None and not isinstance(stable_below, bool) \
            and isinstance(stable_below, (int, float))
        threshold = float(stable_below) if declared else _DEFAULT_STABLE_BELOW

        return {
            "assessable": True,
            "drift": drift,
            "stable": drift < threshold,
            "threshold": threshold,
            "threshold_is_a_default": not declared,
            "threshold_basis": (
                "stated by the caller" if declared else
                f"NOT TUNED: {_DEFAULT_STABLE_BELOW} is a default for this engine and nothing has "
                "calibrated it against this platform's own drift history, so 'stable' below it is an "
                "aspiration and not a measurement"),
            "keys_measured": shared,
            "keys_measured_count": len(shared),
            "baseline_keys_total": len(b),
            "current_keys_total": len(c),
            "coverage_basis": (
                f"drift was computed over the {len(shared)} key(s) the two states share, out of {len(b)} in "
                f"the baseline and {len(c)} in the current state; keys present in only one of them were not "
                "measured and are not counted as unchanged"),
            "basis": (f"relative Euclidean drift {drift:.6f} over {len(shared)} shared key(s), against a "
                      f"threshold of {threshold}" + ("" if declared else " which is an untuned default")),
            "no_fixpoint_proof": (
                "this engine performs NO fixpoint or mu-calculus check. The archived version returned "
                "strings naming one; naming a proof is not performing it, so nothing of the kind is claimed "
                "here"),
        }

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        ctx = request.context or {}
        res = await self.measure_drift(ctx.get("baseline"), ctx.get("current"), ctx.get("stable_below"))
        ok = res.get("assessable") is True

        if not ok:
            answer = f"Not assessable: {res['basis']}"
        else:
            answer = (f"Drift {res['drift']:.6f} over {res['keys_measured_count']} shared key(s) — "
                      f"{'within' if res['stable'] else 'above'} a threshold of {res['threshold']}"
                      + (" (an untuned default)" if res["threshold_is_a_default"] else ""))

        _resp = ConsultationResponse(
            engine=ENGINE_ID,
            answer=answer,
            confidence=None,
            confidence_basis=(
                "not applicable: the drift is a computed distance over the keys named in the result, not an "
                "estimate, so there is no confidence to state. Its COVERAGE is reported instead, which is "
                "the thing a reader would otherwise have to assume"
                if ok else f"nothing was measured: {res['basis']}"),
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
