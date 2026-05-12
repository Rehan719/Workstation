import asyncio
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
from agentic_core.quality.vrpr_pipeline import VRPRPipeline

class ConsultationQuery(BaseModel):
    id: str
    payload: Any
    context: Any
    confidence_threshold: float = 0.95

class MushawaraOutcome(BaseModel):
    recommendation: str
    consensus_score: float
    engine_attestations: Dict[str, Any]
    vrpr_confidence: float
    latency_ms: float
    constitutional_articles: List[int]

class MushawaraBridge:
    """
    Deliberative consensus engine for cross-cognitive decisions.
    Synchronous mode: <500ms for operational recirculation.
    """
    SYNCHRONOUS_TIMEOUT_MS = 500
    MIN_PERSPECTIVES = 3

    def __init__(self, registry: CognitiveEngineRegistry, ueg: Any, enforcement: Any):
        self.registry = registry
        self.ueg = ueg
        self.enforcement = enforcement
        self.vrpr = VRPRPipeline(ueg, enforcement)

    async def sync_consult(
        self,
        query: ConsultationQuery,
        required_engines: List[EngineType],
        timeout_ms: Optional[int] = None
    ) -> MushawaraOutcome:
        """
        Execute Mushāwara deliberation with constitutional guarantees.
        Parallel invocation of ≥3 engines.
        """
        start_time = time.monotonic()
        timeout = timeout_ms or self.SYNCHRONOUS_TIMEOUT_MS

        # 1. Constitutional gate: minimum perspectives
        if len(required_engines) < self.MIN_PERSPECTIVES:
             raise ValueError(f"Mushāwara requires ≥{self.MIN_PERSPECTIVES} perspectives.")

        # 2. Parallel engine invocation
        tasks = []
        for engine_type in required_engines:
            engine = self.registry.get(engine_type)
            tasks.append(engine.process(query.payload, query.context, self.enforcement))

        try:
            # Gather perspectives within timeout
            perspectives = await asyncio.wait_for(asyncio.gather(*tasks), timeout=timeout/1000.0)
        except asyncio.TimeoutError:
            print(f"[UEG] Mushawara Timeout: Exceeded {timeout}ms")
            raise TimeoutError(f"Mushawara deliberation timed out after {timeout}ms")

        # 3. Consensus formation (simple weighted average for Phase 1)
        consensus_text = " | ".join([p.payload.get("conclusion", str(p.payload)) for p in perspectives if not p.error])
        avg_confidence = sum([p.confidence for p in perspectives]) / len(perspectives)

        attestations = {p.engine_id: p.constitutional_trace for p in perspectives}
        binding_articles = []
        for p in perspectives:
            binding_articles.extend(p.constitutional_trace.get("articles_enforced", []))

        # 4. VRPR clearance
        vrpr_result = await self.vrpr.process(consensus_text, query.context)

        latency_ms = (time.monotonic() - start_time) * 1000

        outcome = MushawaraOutcome(
            recommendation=vrpr_result.content,
            consensus_score=avg_confidence,
            engine_attestations=attestations,
            vrpr_confidence=vrpr_result.confidence_score,
            latency_ms=latency_ms,
            constitutional_articles=list(set(binding_articles))
        )

        await self._log_to_ueg(outcome, query)

        return outcome

    async def _log_to_ueg(self, outcome: MushawaraOutcome, query: ConsultationQuery):
        print(f"[UEG] Mushawara consultation {query.id} logged. Latency: {outcome.latency_ms:.2f}ms")
