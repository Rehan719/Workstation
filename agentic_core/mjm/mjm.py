import asyncio
import json
import math
from collections import Counter
from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.cognitive.cascade_v16 import UltimateCognitiveCascade
from agentic_core.consultation.interface import ConsultationRequest, ConsultationResponse, ValidationResult
from agentic_core.consultation.constitutional_screen import screen as _constitutional_screen

class MJMOrchestratorV4:
    """
    Mushahida-Jaiza-Muaina (MJM) v4.0.
    Integrated with Ultimate Cognitive Cascade and Systems Biology Analogues.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()
        self.cascade = UltimateCognitiveCascade(self.ueg)

    @staticmethod
    def _signal_entropy_bits_per_byte(signal: Any):
        """Shannon entropy of the serialised signal, in bits per byte, or None when there is nothing to measure.

        W538 (FU-328) — this step returned a TYPED entropy of 0.12 on every call, reaching two public routes.
        0.12 was not a measurement that came out low; it was the absence of one written as a number. Entropy
        over the signal's own byte distribution IS computable, so it is computed, and the key names exactly
        what it measures: the SIGNAL's information content, not anything about the platform's observation of
        it. Maximum 8.0 bits per byte.
        """
        try:
            blob = json.dumps(signal, sort_keys=True, default=str).encode("utf-8")
        except Exception:                      # noqa: BLE001 — see below; this is on a public route
            # W538 — BROADER THAN TypeError/ValueError ON PURPOSE. `default=str` makes almost anything
            # serialisable, so the reachable failure is not a type error: a CIRCULAR REFERENCE raises
            # ValueError (measured), and an object whose own __str__ raises propagates whatever that raises
            # (measured: RuntimeError). This method is reached from /api/v1/cognitive, so an input that
            # cannot be described must yield "not computed" rather than a 500.
            return None
        if not blob:
            return None
        n = len(blob)
        bits = -sum((c / n) * math.log2(c / n) for c in Counter(blob).values())
        # `+ 0.0` normalises NEGATIVE ZERO: a single-symbol payload computes -0.0, and a figure served as
        # -0.0 reads like a measurement that went wrong rather than one that came out at zero. Measured on
        # json.dumps("") -> '""', two identical bytes.
        return round(bits + 0.0, 4)

    async def mushahida(self, signal: Any) -> Dict[str, Any]:
        """Sense/Observation: capture the signal and measure what is actually measurable about it."""
        _entropy = self._signal_entropy_bits_per_byte(signal)
        observation = {
            "signal_captured": signal,
            "shannon_entropy_bits_per_byte": _entropy,
            "entropy_basis": ("Shannon entropy of the serialised signal over its own byte distribution, in "
                              "bits per byte, maximum 8.0. It measures the SIGNAL's information content and "
                              "says nothing about the quality of any observation performed on it"
                              if _entropy is not None else
                              "NOT COMPUTED: the signal could not be serialised, or was empty"),
            "observation_performed": False,
            "observation_basis": ("no observation beyond capture and a measurement of the signal itself is "
                                 "performed here; this step records what arrived, not a judgement of it"),
        }
        await self.ueg.log_minimisation_event("mjm_mushahida_observed", observation)
        return observation

    async def jaiza(self, observation: Dict) -> Dict[str, Any]:
        """Analyze/Assessment: Cognitive Processing via Cascade"""
        analysis = await self.cascade.execute_cascade(observation)
        await self.ueg.log_minimisation_event("mjm_jaiza_analyzed", {"depth": "v16_cascade"})
        return analysis

    async def muaina(self, analysis: Dict) -> Dict[str, Any]:
        """Act/Inspection: record the analysis reached. Nothing is executed or assessed in this step.

        W538 (FU-328) — this returned a TYPED compliance of 1.0 and a result of "optimised", both reaching
        api/cognitive.py's response as-is. A perfect compliance was the ABSENCE of a compliance assessment
        written as its best possible outcome, and nothing in this method optimises anything: it logs and
        returns. Both are now None with a basis, which is the honest shape and is what api/cognitive.py will
        serve, because fixing a reader instead would have left the other caller lying.
        """
        action = {
            "result": None,
            "result_basis": ("nothing is executed or optimised in this step: it records the analysis reached "
                             "and logs it. A result of 'optimised' claimed an action nobody took"),
            "compliance": None,
            "compliance_basis": ("NOT ASSESSED: no compliance check runs here, against the constitution or "
                                 "anything else. A compliance of 1.0 was the absence of an assessment written "
                                 "as its best possible outcome"),
            "impact": analysis.get("status", "unknown"),
        }
        await self.ueg.log_minimisation_event("mjm_muaina_acted", action)
        return action

    async def run_lifecycle(self, initial_signal: Any) -> Dict[str, Any]:
        obs = await self.mushahida(initial_signal)
        analysis = await self.jaiza(obs)
        result = await self.muaina(analysis)
        return result

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        """Standardized Mushawara consultation implementation for MJM v4.0."""
        res = await self.run_lifecycle(request.query)
        _resp = ConsultationResponse(
            engine="mjm",
            answer=f"MJM Lifecycle Result: {res.get('result', 'unknown')}",
            # P3.12 - a stated refusal, not a fabricated figure. MJM is a lifecycle, not a cognitive
            # engine, and it computed no confidence either.
            confidence=None,
            confidence_basis=("not computed: the MJM lifecycle returns a fixed marker and does not score its own judgement (P3.12)"),
            served_by="native-fixed-marker",
            is_external=False,
            constitutional_validation=ValidationResult(),
            reasoning_trace="Recursive MJM v4.0 (Mushahida-Jaiza-Muaina) lifecycle execution."
        )
        #  P3.28 clause (1) — the verdict is COMPUTED by gaas.v5's own checks over the request and
        #  this answer, replacing a literal that said no check ran. A screen may refuse, never clear:
        #  a non-refusal keeps passed=None and states its coverage (consultation/constitutional_screen.py).
        _resp.constitutional_validation = _constitutional_screen("mjm", request.query, _resp.answer)
        return _resp
