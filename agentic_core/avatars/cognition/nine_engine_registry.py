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
        result = await engine.process(input_data, context, self.enforcement)
        return getattr(result, 'payload', {}) or {}

    def get_types(self, ids: List[str]) -> List[EngineType]:
        """Convert engine ID strings to typed enums."""
        return [self.engine_types[eid] for etid in ids if (eid := etid.lower()) in self.engine_types]
