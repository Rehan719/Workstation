import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AppetiteEngine:
    """
    ARTICLE 46: Digestive System with Appetite-Driven Growth.
    Employs synaptic scaling with τ_H tunable.
    """
    def __init__(self, tau_h: float = 18.6):
        self.tau_h = tau_h # CP-II tunable 12-25s
        self.hunger = 1.0
        self.satisfaction = 0.0

    def evaluate_nutrition(self, source_metadata: Dict[str, Any]) -> float:
        """Evaluates nutritional value based on recency and credibility."""
        recency = source_metadata.get("recency_months", 12)
        score = 1.0
        if recency <= 6:
            score += 0.5 # Appetite for advanced recent developments
        return score

    def ingest(self, source: str, data: Dict[str, Any]):
        nutrition = self.evaluate_nutrition(data.get("metadata", {}))
        logger.info(f"DIGESTION: Ingested {source}. Nutrition Score: {nutrition:.2f}")
        self.satisfaction += nutrition
        self.hunger -= 0.1
        return nutrition
