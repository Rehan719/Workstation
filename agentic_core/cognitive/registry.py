from enum import Enum
from typing import Dict, Any, Type, List
from agentic_core.cognitive.base_engine import CognitiveEngine

class EngineType(str, Enum):
    INKASHAF = "inkashaf"
    AQAL = "aqal"
    SAMAJH = "samajh"
    HOSHIYARI = "hoshiyari"
    SOCH = "soch"
    IMAN = "iman"
    TAWAZUN = "tawazun"
    NIYYAH = "niyyah"
    TAFAKKUR = "tafakkur"

class CognitiveEngineRegistry:
    """
    Registry for discovering and instantiating cognitive engines.
    """
    _engines: Dict[EngineType, CognitiveEngine] = {}

    @classmethod
    def register(cls, engine_type: EngineType, engine_instance: CognitiveEngine):
        cls._engines[engine_type] = engine_instance

    @classmethod
    def get(cls, engine_type: EngineType) -> CognitiveEngine:
        engine = cls._engines.get(engine_type)
        if not engine:
            raise ValueError(f"Engine {engine_type} not found in registry.")
        return engine

    @classmethod
    def list_active(cls) -> List[EngineType]:
        return list(cls._engines.keys())
