import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CuriosityDrive:
    """
    CQ-II: Curiosity-Driven Exploration.
    Triggers active exploration when novel stimuli are detected.
    """
    def __init__(self):
        self.curiosity_score = 0.5

    def evaluate_stimulus(self, novelty_score: float):
        """Increases curiosity and triggers exploration if novelty is high."""
        if novelty_score > 0.8:
            logger.info("CURIOSITY: Novel stimulus detected. Triggering active exploration.")
            self.curiosity_score = min(1.0, self.curiosity_score + 0.1)
            return True

        self.curiosity_score = max(0.1, self.curiosity_score - 0.05)
        return False
