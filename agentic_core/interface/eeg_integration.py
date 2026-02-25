import logging
import random

logger = logging.getLogger(__name__)

class EEGIntegration:
    """
    ARTICLE DE: EEG Data Stream Integration.
    Fallback Switch: <50 ms latency at SQI < 0.7.
    """
    def __init__(self):
        self.sqi = 0.9 # Signal Quality Index
        self.active_modality = "EEG"

    def get_raw_signal(self):
        """Simulates raw EEG data."""
        # Random noise for simulation
        if self.sqi < 0.7:
            self.active_modality = "BEHAVIORAL_PROXY"
            logger.warning(f"EEG: SQI low ({self.sqi:.2f}). Falling back to Proxies.")
        else:
            self.active_modality = "EEG"

        return [random.uniform(-50, 50) for _ in range(8)]

    def update_sqi(self, new_sqi: float):
        self.sqi = new_sqi
