import time
import logging

logger = logging.getLogger(__name__)

class IgnitionDetector:
    """
    ARTICLE DB: Detects 'ignition' of global broadcast.
    Latency target: <250 ms.
    """
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.last_ignition_time = 0.0

    def detect_ignition(self, workspace_entropy: float) -> bool:
        """
        Ignition occurs when entropy drops (information integration).
        """
        if workspace_entropy < self.threshold:
            self.last_ignition_time = time.time()
            logger.info(f"CONSCIOUSNESS: Ignition detected. Entropy: {workspace_entropy:.3f}")
            return True
        return False
