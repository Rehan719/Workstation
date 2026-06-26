import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FitnessFunction:
    """
    CC-I: Multi-Objective Fitness Function.
    Combines success, latency, ethics, synergy, and user feedback.
    """
    def compute_fitness(self, agent_metrics: Dict[str, Any]) -> float:
        # CJ-I: Multi-objective fitness enhanced with perceptual metrics
        weights = {
            "success_rate": 0.25,
            "latency_score": 0.15,
            "ethical_scalar": 0.2,
            "synergy_score": 0.15,
            "perceptual_accuracy": 0.15, # New
            "binding_success": 0.1         # New
        }

        score = (
            agent_metrics.get("success_rate", 1.0) * weights["success_rate"] +
            self._calc_latency_score(agent_metrics.get("latency_ms", 50)) * weights["latency_score"] +
            agent_metrics.get("ethical_scalar", 1.0) * weights["ethical_scalar"] +
            agent_metrics.get("synergy_score", 1.0) * weights["synergy_score"] +
            agent_metrics.get("perceptual_accuracy", 1.0) * weights["perceptual_accuracy"] +
            agent_metrics.get("binding_success", 1.0) * weights["binding_success"]
        )

        return round(score, 4)

    def _calc_latency_score(self, latency_ms: float) -> float:
        # Lower latency -> higher score (max 1.0)
        if latency_ms <= 50: return 1.0
        if latency_ms >= 500: return 0.0
        return 1.0 - (latency_ms - 50) / 450
