import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DigestiveSystem:
    """
    L-C-VI: Digestive System with Appetite-Driven Growth.
    Quantitative ingestion weighting for scientific sources.
    """
    def __init__(self):
        self.hunger_level = 0.5
        self.satiety = 1.0
        self.tau_h = 18.6 # Tier 2 tunable

    def ingest(self, source_type: str, data: Dict[str, Any]) -> float:
        """Evaluates nutritional value of incoming data."""
        logger.info(f"Ingesting data from {source_type}...")

        # Quantitative Weighting
        weight = 0.0
        if source_type == "github":
            weight = 0.4 * data.get("citation_velocity", 1) + 0.35 * data.get("test_coverage", 0.8)
        elif source_type == "arxiv":
            weight = 0.6 * data.get("citation_velocity", 1) + 0.4 * data.get("recency", 1)

        self.satiety += weight * 0.1
        self.hunger_level -= weight * 0.05

        return weight

    def excrete(self):
        """Removes obsolete or low-value patterns from memory."""
        logger.info("Digestive excretion cycle: purging low-value artifacts.")
