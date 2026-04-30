import math
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ImmuneCheckpoint:
    """
    ARTICLE 47: Multi-Layered Immune Defense.
    Uses sigmoidal checkpoint inhibition calibrated to perplexity > 42.3.
    """
    def __init__(self, ic50: float = 42.3):
        self.ic50 = ic50

    def calculate_inhibition(self, perplexity: float) -> float:
        """Sigmoidal inhibition curve."""
        # Inhibition = 1 / (1 + exp(-(x - ic50)))
        return 1.0 / (1.0 + math.exp(-(perplexity - self.ic50)))

    def evaluate_threat(self, data: Dict[str, Any]) -> float:
        perplexity = data.get("metrics", {}).get("perplexity", 20.0)
        inhibition = self.calculate_inhibition(perplexity)

        if inhibition > 0.8:
            logger.warning(f"IMMUNE: High threat detected (Inhibition {inhibition:.2f}). Triggering response.")

        return inhibition
