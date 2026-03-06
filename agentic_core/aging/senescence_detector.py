import logging
from .telomere_tracker import TelomereTracker

logger = logging.getLogger(__name__)

class SenescenceDetector:
    """Article 49: Detects aging/obsolete components."""

    def __init__(self, tracker: TelomereTracker, threshold: float = 0.2):
        self.tracker = tracker
        self.threshold = threshold

    def is_senescent(self, component_id: str) -> bool:
        health = self.tracker.get_health(component_id)
        if health < self.threshold:
            logger.warning(f"AGING: Component {component_id} is senescent (Health: {health:.2f})")
            return True
        return False
