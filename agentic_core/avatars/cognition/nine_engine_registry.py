"""
Avatar Engine Registry (vΩ∞-AVATAR-OMNISYNTHESIS).
Management of the 9-engine distributed nervous system.
"""
from typing import Dict, Any, List, Optional
import logging
from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType

logger = logging.getLogger(__name__)

class EngineRegistry9:
    """
    IDBO Layer 9: Orchestration.
    Lifecycle management for Inkashaf, Aqal, Samajh, Hoshiyari, Soch, Iman, Tawazun, Niyyah, Tafakkur.
    """
    def __init__(self, ueg_logger: Any, enforcement: Any):
        self.ueg = ueg_logger
        self.enforcement = enforcement
        self.registry = CognitiveEngineRegistry()

        # Canonical 9-engine map
        self.engine_types = {
            "inkashaf": EngineType.INKASHAF,
            "aqal": EngineType.AQAL,
            "samajh": EngineType.SAMAJH,
            "hoshiyari": EngineType.HOSHIYARI,
            "soch": EngineType.SOCH,
            "iman": EngineType.IMAN,
            "tawazun": EngineType.TAWAZUN,
            "niyyah": EngineType.NIYYAH,
            "tafakkur": EngineType.TAFAKKUR
        }

    async def get_engine_response(self, engine_id: str, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through a specific cognitive engine."""
        etype = self.engine_types.get(engine_id)
        if not etype:
            raise ValueError(f"Cognitive Engine '{engine_id}' not found in registry.")

        engine = self.registry.get(etype)
        # W531 (FU-320) — this called `engine.process(input_data, context, self.enforcement)`. NO ENGINE
        # IMPLEMENTS process: the consultation contract's entry point is consult(ConsultationRequest), and
        # that is true of all twelve registered engines. Once W520 populated the registry this reader
        # stopped failing with "Engine not found" and started failing with AttributeError instead — it
        # resolved an engine and then called a method that does not exist.
        from agentic_core.consultation.interface import ConsultationRequest
        res = await engine.consult(ConsultationRequest(
            engine=engine_id,
            query=str(input_data),
            context=context if isinstance(context, dict) else {},
        ))
        return {
            "engine": res.engine,
            "answer": res.answer,
            # the provenance travels, as it does on every other output surface here
            "served_by": res.served_by,
            "is_external": res.is_external,
            "confidence": res.confidence,
            "confidence_basis": res.confidence_basis,
            "result": res.metadata or {},
            "constitutional_validation": {
                "passed": res.constitutional_validation.passed,
                "basis": res.constitutional_validation.basis,
            },
        }

    def get_types(self, ids: List[str]) -> List[EngineType]:
        """Convert engine ID strings to typed enums."""
        return [self.engine_types[eid] for etid in ids if (eid := etid.lower()) in self.engine_types]
