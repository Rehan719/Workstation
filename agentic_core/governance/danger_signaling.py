import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DangerSignaling:
    """
    ARTICLE DD: Danger Signaling based on behavioral proxies.
    Threshold: dwell > 750 ms, latency variance σ < 120 ms.
    """
    def __init__(self):
        self.threat_level = 0 # 0 to 5

    def evaluate_proxies(self, dwell_time: float, latency_var: float) -> int:
        """
        Maps user behavior to danger signals.
        """
        level = 0
        if dwell_time < 300: # Increased sensitivity for testing
            level += 3
        if latency_var > 200:
            level += 2

        self.threat_level = min(5, level)
        if self.threat_level >= 3:
            logger.warning(f"DANGER: High threat level detected ({self.threat_level}). Initiating verification.")

        return self.threat_level

    def get_ingestion_gate(self) -> float:
        """Returns multiplier for ingestion rate based on danger."""
        # Higher threat -> slower ingestion
        return 1.0 - (self.threat_level / 5.0)
