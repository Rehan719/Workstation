import numpy as np
import time
import logging
from scipy.signal import hilbert

logger = logging.getLogger(__name__)

class IgnitionDetector:
    """
    ARTICLE DB: Ignition of Global Broadcast.
    Uses power envelope monitoring of gamma-band activity.
    Target latency: <250 ms.
    """
    def __init__(self, power_threshold: float = 1.5):
        self.power_threshold = power_threshold
        self.is_ignited = False
        self.last_ignition_event = 0.0

    def detect_ignition(self, gamma_signal: np.ndarray) -> bool:
        """
        Detects sudden widespread emergence of coherent neural activity.
        """
        # Analytic signal amplitude (power envelope)
        analytic_signal = hilbert(gamma_signal)
        envelope = np.abs(analytic_signal)
        mean_power = np.mean(envelope)

        if mean_power > self.power_threshold:
            if not self.is_ignited:
                self.is_ignited = True
                self.last_ignition_event = time.time()
                logger.info(f"IGNITION: Conscious broadcast detected. Power: {mean_power:.2f}")
            return True
        else:
            self.is_ignited = False
            return False
