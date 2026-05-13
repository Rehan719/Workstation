from enum import Enum
from typing import Dict, Any, Type, List

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
    _engines = {}
    @classmethod
    def register(cls, engine_type, engine_instance): cls._engines[engine_type] = engine_instance
    @classmethod
    def get(cls, engine_type):
        if engine_type not in cls._engines: raise ValueError(f"Engine {engine_type} not found")
        return cls._engines[engine_type]
