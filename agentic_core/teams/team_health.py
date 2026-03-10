import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TeamHealthMonitor:
    """Computes and monitors team health score (Article 116)."""
    def __init__(self, threshold: float = 0.9):
        self.threshold = threshold

    def compute_health(self, performance_metrics: Dict[str, float]) -> float:
        """
        Computes health based on:
        - Latency (30%)
        - Error rate (40%)
        - Agent resonance (30%)
        """
        latency_score = 1.0 - min(performance_metrics.get('latency', 0) / 1000, 1.0)
        error_score = 1.0 - performance_metrics.get('error_rate', 0)
        resonance = performance_metrics.get('resonance', 1.0)

        health = (latency_score * 0.3) + (error_score * 0.4) + (resonance * 0.3)
        logger.info(f"Team Health computed: {health:.4f}")
        return health

    def is_healthy(self, health: float) -> bool:
        return health >= self.threshold
