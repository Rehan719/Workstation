from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class ControlDecision:
    approved: bool
    reason: Optional[str] = None
    adjusted_setpoints: Optional[Dict[str, float]] = None
    efficiency_score: Optional[float] = None

class SimulationResult:
    def __init__(self, trajectory, confidence):
        self.trajectory = trajectory
        self.confidence = confidence

class EvolutionReport:
    def __init__(self, learning, corrections):
        self.learning = learning
        self.corrections = corrections
