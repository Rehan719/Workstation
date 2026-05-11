from dataclasses import dataclass
from typing import List, Any, Dict, Optional

@dataclass
class SimulationResult:
    trajectory: List[Any]
    confidence: float

@dataclass
class EvolutionReport:
    learning: float
    corrections: int

@dataclass
class ControlDecision:
    approved: bool
    reason: Optional[str] = None
    adjusted_setpoints: Optional[Dict[str, float]] = None
    efficiency_score: Optional[float] = None
