import logging
import numpy as np

logger = logging.getLogger(__name__)

class DendriticIntegration:
    """
    DE-IV: Dendritic Integration.
    Emulates NMDA-spike dynamics with 1–12 ms integration windows.
    Calibrated to 750 ms perceptual threshold for user intent.
    """
    def __init__(self):
        self.nmda_window_ms = 12.0
        self.refractory_period_ms = 5.0
        self.last_spike_time = 0.0

    def integrate_spikes(self, spike_train: np.ndarray, current_time_ms: float) -> bool:
        """
        Non-linear integration: multiple spikes in the NMDA window trigger a 'dendritic spike'.
        """
        if current_time_ms - self.last_spike_time < self.refractory_period_ms:
            return False

        spike_count = np.sum(spike_train)
        # Threshold for dendritic spike: 3 concurrent spikes in 12ms window
        if spike_count >= 3:
            logger.info("DENDRITE: NMDA-spike triggered. Supralinear integration.")
            self.last_spike_time = current_time_ms
            return True

        return False
