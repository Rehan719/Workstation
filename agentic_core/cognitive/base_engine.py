from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

class EngineOutput(BaseModel):
    """Standardized output for all cognitive engines."""
    payload: Any
    confidence: float
    constitutional_trace: Dict[str, Any]
    engine_id: str
    error: Optional[str] = None

class CognitiveEngine(ABC):
    """
    Abstract base class for all nine cognitive engines.
    Enforces constitutional validation at entry and exit.
    """
    def __init__(self, engine_id: str, biological_analogue: str, constitutional_binding: List[int], ueg_logger: Any):
        self.engine_id = engine_id
        self._biological_analogue = biological_analogue
        self._constitutional_binding = constitutional_binding
        self.ueg = ueg_logger

    @abstractmethod
    async def _process_logic(self, input_data: Any, context: Any) -> Any:
        """Core logic to be implemented by each engine."""
        return {"error": "Not implemented"}

    async def process(
        self,
        input_data: Any,
        context: Any,
        enforcement: OmniEnforcementPatternSupreme
    ) -> EngineOutput:
        """Wraps core logic with constitutional pre- and post-validation."""
        # 1. Pre-validation
        pre_val = enforcement.validate(input_data)
        if not pre_val.passed:
            return EngineOutput(
                payload=None,
                confidence=0.0,
                constitutional_trace={"pre_validation": pre_val.details},
                engine_id=self.engine_id,
                error=f"Pre-validation failed: {pre_val.violation}"
            )

        # 2. Execute logic
        try:
            result_payload = await self._process_logic(input_data, context)
        except Exception as e:
            return EngineOutput(
                payload=None,
                confidence=0.0,
                constitutional_trace={},
                engine_id=self.engine_id,
                error=f"Engine logic failed: {str(e)}"
            )

        # 3. Post-validation
        post_val = enforcement.validate(result_payload)

        output = EngineOutput(
            payload=result_payload,
            confidence=self._compute_confidence(result_payload),
            constitutional_trace={
                "pre_validation": pre_val.details,
                "post_validation": post_val.details,
                "articles_enforced": self._constitutional_binding
            },
            engine_id=self.engine_id,
            error=None if post_val.passed else f"Post-validation failed: {post_val.violation}"
        )

        # 4. UEG Logging
        await self._log_to_ueg(output, context)

        return output

    @property
    def biological_analogue(self) -> str:
        return self._biological_analogue

    @property
    def constitutional_binding(self) -> List[int]:
        return self._constitutional_binding

    def _compute_confidence(self, result: Any) -> float:
        """Heuristic confidence score for engine output."""
        return 0.95 # Default for Phase 1

    async def _log_to_ueg(self, output: EngineOutput, context: Any):
        """Logs engine decision to the Unified Evolutionary Genome."""
        # In Phase 1, we use a simple print/logger simulation
        print(f"[UEG] Engine {self.engine_id} logged decision. Success: {output.error is None}")
