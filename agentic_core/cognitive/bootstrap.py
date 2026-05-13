from agentic_core.cognitive.registry import CognitiveEngineRegistry, EngineType
from agentic_core.ueg.logger import VSBUEGLogger
from agentic_core.cognitive.foundational.aqal_engine import AqalEngine
from agentic_core.cognitive.foundational.hoshiyari_engine import HoshiyariEngine
from agentic_core.cognitive.foundational.iman_engine import ImanEngine
from agentic_core.cognitive.foundational.inkashaf_engine import InkashafEngine
from agentic_core.cognitive.foundational.samajh_engine import SamajhEngine
from agentic_core.cognitive.foundational.soch_engine import SochEngine
from agentic_core.cognitive.meta.niyyah_engine import NiyyahEngine
from agentic_core.cognitive.meta.tafakkur_engine import TafakkurEngine
from agentic_core.cognitive.meta.tawazun_engine import TawazunEngine

def bootstrap_engines(ueg_logger=None):
    ueg = ueg_logger or VSBUEGLogger()
    registry = CognitiveEngineRegistry()
    registry.register(EngineType.AQAL, AqalEngine(ueg))
    registry.register(EngineType.HOSHIYARI, HoshiyariEngine(ueg))
    registry.register(EngineType.IMAN, ImanEngine(ueg))
    registry.register(EngineType.INKASHAF, InkashafEngine(ueg))
    registry.register(EngineType.SAMAJH, SamajhEngine(ueg))
    registry.register(EngineType.SOCH, SochEngine(ueg))
    registry.register(EngineType.NIYYAH, NiyyahEngine(ueg))
    registry.register(EngineType.TAFAKKUR, TafakkurEngine(ueg))
    registry.register(EngineType.TAWAZUN, TawazunEngine(ueg))
    return registry
