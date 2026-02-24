import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class EthicalFitnessScalar:
    """
    BW-I: Dynamic 0.0–1.0 integrity metric.
    Updated from historical compliance, veto rates, and validation.
    """
    def __init__(self):
        self.scalar = 1.0
        self.history = []
        self.weights = {
            "compliance": 0.4,
            "veto_rate": 0.3,
            "user_feedback": 0.2,
            "verification": 0.1
        }

    def update_scalar(self, metrics: Dict[str, float]):
        """
        BW-II: Multi-source update.
        metrics keys: compliance_rate, veto_impact (1-rate), user_score, verify_score
        """
        new_val = (
            metrics.get("compliance_rate", 1.0) * self.weights["compliance"] +
            metrics.get("veto_impact", 1.0) * self.weights["veto_rate"] +
            metrics.get("user_score", 1.0) * self.weights["user_feedback"] +
            metrics.get("verify_score", 1.0) * self.weights["verification"]
        )

        self.scalar = round(max(0.0, min(1.0, new_val)), 4)
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "value": self.scalar,
            "metrics": metrics
        })

        if self.scalar < 0.7:
            logger.warning(f"ETHICAL FITNESS DEGRADED: {self.scalar}")

    def gate_decision(self, threshold: float = 0.5) -> bool:
        """BW-IV: Decision Gating."""
        return self.scalar >= threshold
