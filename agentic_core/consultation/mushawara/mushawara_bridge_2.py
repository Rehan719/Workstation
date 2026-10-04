import asyncio, time, logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
from agentic_core.consultation.mushawara.perspective_aggregator import PerspectiveAggregator
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

@dataclass
class ConsultationQuery:
    id: str; query: str; domain: str; context: Dict[str, Any]

class MushawaraBridge2:
    def __init__(self, ueg, registry=None):
        self.ueg, self.registry = ueg, registry or CognitiveEngineRegistry()
        self.agg = PerspectiveAggregator(None)
        self.enf = OmniEnforcementPatternSupreme({"fail_on_missing_validator": False}, {"task": "mushawara"})
    async def consult(self, task: Dict[str, Any], mode: str = "sync") -> Dict[str, Any]:
        """Backward compatible consult API."""
        query = ConsultationQuery(
            id=task.get("id", "q1"),
            query=task.get("task", "Analyze proposal"),
            domain=task.get("domain", "general"),
            context=task.get("context", {})
        )
        # Default to foundational engines for Phase 4
        engines = [EngineType.INKASHAF, EngineType.AQAL, EngineType.SAMAJH]
        return await self.deliberate(query, engines, mode=mode)

    async def deliberate(self, query, engines, mode="sync"):
        start = time.time()
        if mode == "sync": ps = await asyncio.gather(*[self._get_p(query, e) for e in engines])
        else: ps = [await self._get_p(query, e) for e in engines]
        agg = await self.agg.synthesize(ps)
        # W533 — the status was a LITERAL here, so this deliberation had exactly one possible outcome, and
        # clearance GATE 1 clears on it: `status != "APPROVED"` in avatars/core/clearance_chain.py. W530
        # taught that gate to refuse instead of rubber-stamping; the gate was honest and its input was not.
        # It is now derived from the verdicts the perspectives actually returned, and an unassessed
        # deliberation is NOT a cleared one.
        _verdicts = [(p.get("trace") or {}).get("passed") for p in ps]
        _unassessed = sum(1 for v in _verdicts if v is None)
        if False in _verdicts:
            _status = "BLOCKED"
            _reason = (f"{_verdicts.count(False)} of {len(_verdicts)} perspective(s) returned a failing "
                       "constitutional verdict")
        elif _unassessed:
            _status = "NOT ASSESSED"
            # W582 — THE CAUSE NAMED HERE WAS WRONG, and a basis asserting a cause measurement
            # contradicts is the defect this programme removes everywhere else. It said the engines
            # "refuse for want of a model path". MEASURED: ollama is reachable with three local models
            # installed, and the verdict is not a refusal at all — it is a hardcoded `passed=None` whose
            # own basis reads "no constitutional check ran: this engine performs none". So no model, on
            # any hardware, changes this outcome, and a reader told otherwise waits for the wrong thing.
            # This matters downstream: the avatar path is HELD on a release condition phrased as a model
            # path, and a hold whose condition cannot be met by what it names is permanent.
            _reason = (f"{_unassessed} of {len(_verdicts)} perspective(s) supplied no constitutional "
                       "verdict, so this deliberation did not clear; an unassessed outcome is not an "
                       "approval. The perspectives did not refuse for want of a model: they perform no "
                       "constitutional check at all, so this outcome is unchanged by any model being "
                       "available and is released only by a check being implemented")
        else:
            _status = "APPROVED"
            _reason = f"all {len(_verdicts)} perspective(s) returned a passing constitutional verdict"
        res = {"status": _status, "reason": _reason, "status_basis": _reason,
               "outcome": agg, "duration_ms": (time.time()-start)*1000}
        if self.ueg: await self.ueg.log_minimisation_event("mushawara_complete", res)
        return res
    async def _get_p(self, q, et):
        # W533 (FU-320, second caller) — this called .process(), which NO engine implements; the
        # contract is consult(ConsultationRequest). W531 fixed the caller in nine_engine_registry
        # and its guard scanned only THAT file, so this one survived and stopped stage ANALYZE.
        # It also read res.constitutional_trace, which ConsultationResponse does not have (the
        # field is constitutional_validation, a three-state verdict with a basis).
        from agentic_core.consultation.interface import ConsultationRequest as _CReq
        res = await self.registry.get(et).consult(_CReq(
            engine=et.value, query=str(q.query),
            context=q.context if isinstance(q.context, dict) else {}))
        return {
            "engine": et.value,
            "confidence": res.confidence,
            "confidence_basis": res.confidence_basis,
            "served_by": res.served_by,
            "trace": {"passed": res.constitutional_validation.passed,
                      "basis": res.constitutional_validation.basis},
            # W533 — a 10000-element vector of ones used to sit here, presented as an embedding.
            # Nothing computed it. It is reported as absent rather than fabricated; registered.
            "vector": None,
            "vector_basis": ("no embedding is computed for a deliberative position on this "
                             "platform, so none is reported"),
        }
