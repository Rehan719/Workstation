import logging
import random

logger = logging.getLogger(__name__)

class EEGIntegration:
    """
    DE-II: EEG Integration.
    Real-time EEG acquisition with SQI monitoring.
    """
    def __init__(self):
        self.device_connected = False
        self.sqi = 0.0

    def connect_bci(self):
        self.device_connected = True
        logger.info("EEG: BCI hardware connected.")

    def get_signal_quality(self) -> float:
        if not self.device_connected: return 0.0
        # Simulating fluctuations in signal quality
        self.sqi = 0.85 + random.uniform(-0.2, 0.1)
        return self.sqi

class HybridFallback:
    """
    DL, DE-IV: Hybrid Adaptive Fallback.
    Seamless switching between EEG and Behavioral Proxies.
    Switch latency target: < 50 ms.
    """
    def decide_modality(self, eeg_sqi: float) -> str:
        if eeg_sqi >= 0.7:
            return "BCI_EEG"
        logger.info("FALLBACK: Low SQI detected. Switching to BEHAVIORAL_PROXIES.")
        return "BEHAVIORAL_PROXIES"
