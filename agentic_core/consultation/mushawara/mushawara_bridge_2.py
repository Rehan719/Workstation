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
    async def deliberate(self, query, engines, mode="sync"):
        start = time.time()
        if mode == "sync": ps = await asyncio.gather(*[self._get_p(query, e) for e in engines])
        else: ps = [await self._get_p(query, e) for e in engines]
        agg = await self.agg.synthesize(ps)
        res = {"status": "APPROVED", "outcome": agg, "duration_ms": (time.time()-start)*1000}
        if self.ueg: await self.ueg.log_minimisation_event("mushawara_complete", res)
        return res
    async def _get_p(self, q, et):
        res = await self.registry.get(et).process(q.query, q.context, self.enf)
        return {"engine": et.value, "vector": [1]*10000, "confidence": res.confidence, "trace": res.constitutional_trace}
