import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AppetitiveDigestiveSystem:
    """
    BX: Hunger-driven autonomous development.
    Evaluates information nutrition and lexical divergence.
    L-C-VI: Digestive System with Appetite-Driven Growth.
    """
    def __init__(self):
        self.hunger = 0.5
        self.satisfaction = 1.0
        self.divergence_threshold = 0.68  # BX-I
        self.salience_threshold = 0.75    # CK-I
        self.hunger_level = 0.5           # For backward compat
        self.tau_h = 18.6                 # Tier 2 tunable

    def evaluate_content(self, content: Dict[str, Any]) -> float:
        """BX-II: Information Nutrition Scoring."""
        divergence = content.get("lexical_divergence", 0.0)

        score = 0.0
        if divergence >= self.divergence_threshold:
            score += 0.5
            logger.info("APPETITE: High novelty content detected.")

        if content.get("alignment", 1.0) > 0.9:
            score += 0.5

        salience = content.get("sensory_salience", 0.0)
        if salience >= self.salience_threshold:
             logger.info("APPETITE: High salience sensory input detected.")
             score += 0.3

        self._update_appetite(score)
        return score

    def _update_appetite(self, score: float):
        if score > 0.8:
            self.satisfaction += 0.1
            self.hunger -= 0.1
        else:
            self.hunger += 0.05

        self.hunger = max(0.0, min(1.0, self.hunger))
        self.hunger_level = self.hunger
        self.satisfaction = max(0.0, min(2.0, self.satisfaction))

    def ingest(self, source_type: str, data: Dict[str, Any]) -> float:
        """L-C-VI: Quantitative ingestion weighting."""
        logger.info(f"Ingesting data from {source_type}...")

        weight = 0.0
        if source_type == "github":
            weight = 0.4 * data.get("citation_velocity", 1) + 0.35 * data.get("test_coverage", 0.8)
        elif source_type == "arxiv":
            weight = 0.6 * data.get("citation_velocity", 1) + 0.4 * data.get("recency", 1)

        self.satisfaction += weight * 0.1
        self.hunger -= weight * 0.05
        self.hunger_level = max(0.0, min(1.0, self.hunger))
        return weight

    def identify_waste(self, knowledge_base: List) -> List:
        """BX-IV: Waste Excretion."""
        # Identify low-quality or obsolete info
        return []

    def excrete(self):
        """L-C-VI: Excretion cycle."""
        logger.info("Digestive excretion cycle: purging low-value artifacts.")
        self.satisfaction = max(0.0, min(2.0, self.satisfaction))

# Backward compatibility alias
DigestiveSystem = AppetitiveDigestiveSystem
