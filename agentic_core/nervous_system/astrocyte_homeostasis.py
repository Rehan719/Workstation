import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class AstrocyteHomeostasis:
    """Article 48: Regulates firing rates within ±5% of biological baselines."""

    def __init__(self, baseline_rate: float = 1.0):
        self.baseline_rate = baseline_rate
        self.history = []

    def monitor_firing(self, current_rate: float):
        self.history.append(current_rate)
        deviation = abs(current_rate - self.baseline_rate) / self.baseline_rate

        if deviation > 0.05:
            logger.warning(f"HOMEOSTASIS: Baseline deviation detected! ({deviation*100:.1f}%)")
            return self._correct_firing(current_rate)

        return current_rate

    def _correct_firing(self, current_rate: float) -> float:
        # Move back towards baseline
        adjustment = (self.baseline_rate - current_rate) * 0.5
        new_rate = current_rate + adjustment
        logger.info(f"HOMEOSTASIS: Corrected rate to {new_rate:.2f}")
        return new_rate
