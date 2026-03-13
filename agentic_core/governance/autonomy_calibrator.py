import logging
import time
from typing import Dict, Any, List, Optional
from enum import IntEnum

logger = logging.getLogger(__name__)

class AutonomyLevel(IntEnum):
    L0_MANUAL = 0
    L1_ASSISTED = 1
    L2_SEMI_AUTONOMOUS = 2
    L3_CONDITIONAL = 3
    L4_FULL = 4

class TrustRegistry:
    """
    ARTICLE 606: Tracks Performance History and Explainability to calculate Trust.
    """
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}

    def update_performance(self, agent_id: str, success: bool, score: float):
        record = self.registry.setdefault(agent_id, {"performance_history": [], "explainability": 0.8})
        record["performance_history"].append({"timestamp": time.time(), "success": success, "score": score})
        # Keep last 100 records
        if len(record["performance_history"]) > 100:
            record["performance_history"].pop(0)

    def set_explainability(self, agent_id: str, score: float):
        record = self.registry.setdefault(agent_id, {"performance_history": [], "explainability": 0.8})
        record["explainability"] = score

    def calculate_trust(self, agent_id: str) -> float:
        record = self.registry.get(agent_id)
        if not record: return 0.5

        history = record["performance_history"]
        if not history: return record["explainability"] * 0.5

        avg_perf = sum(r["score"] for r in history) / len(history)
        # Trust = 70% Performance + 30% Explainability
        return (avg_perf * 0.7) + (record["explainability"] * 0.3)

class AutonomyCalibrator:
    """
    ARTICLE 606: Dynamically calibrates autonomy level.
    """
    def __init__(self):
        self.trust_registry = TrustRegistry()

    def calibrate(self, agent_id: str, task_complexity: float, domain_risk: float) -> AutonomyLevel:
        trust_score = self.trust_registry.calculate_trust(agent_id)

        # Heuristic: Autonomy = Trust / (Complexity * Risk)
        weighted_score = trust_score / (task_complexity * domain_risk)

        if weighted_score >= 1.2: return AutonomyLevel.L4_FULL
        if weighted_score >= 0.9: return AutonomyLevel.L3_CONDITIONAL
        if weighted_score >= 0.6: return AutonomyLevel.L2_SEMI_AUTONOMOUS
        if weighted_score >= 0.3: return AutonomyLevel.L1_ASSISTED
        return AutonomyLevel.L0_MANUAL
