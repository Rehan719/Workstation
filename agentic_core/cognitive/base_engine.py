from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from agentic_core.validation.omni_enforcement_pattern_supreme import OmniEnforcementPatternSupreme

class EngineOutput(BaseModel):
    payload: Any; confidence: float; constitutional_trace: Dict[str, Any]; engine_id: str; error: Optional[str] = None

class CognitiveEngine(ABC):
    def __init__(self, engine_id: str, biological_analogue: str, constitutional_binding: List[int], ueg_logger: Any):
        self.engine_id, self._biological_analogue, self._constitutional_binding, self.ueg = engine_id, biological_analogue, constitutional_binding, ueg_logger
    @abstractmethod
    async def _process_logic(self, input_data: Any, context: Any) -> Any: return {"status": "abstract_interface"}
    async def process(self, input_data: Any, context: Any, enforcement: OmniEnforcementPatternSupreme) -> EngineOutput:
        pre = enforcement.validate(input_data)
        if not pre.passed: return EngineOutput(payload=None, confidence=0.0, constitutional_trace={"pre": pre.details}, engine_id=self.engine_id, error="Pre-val fail")
        try: res = await self._process_logic(input_data, context)
        except Exception as e: return EngineOutput(payload=None, confidence=0.0, constitutional_trace={}, engine_id=self.engine_id, error=str(e))
        post = enforcement.validate(res)
        out = EngineOutput(payload=res, confidence=0.95, constitutional_trace={"pre": pre.details, "post": post.details, "articles": self._constitutional_binding}, engine_id=self.engine_id, error=None if post.passed else "Post-val fail")
        return out
    @property
    def constitutional_binding(self) -> List[int]: return self._constitutional_binding
