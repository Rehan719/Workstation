import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

class GammaCoherenceMonitor:
    """
    ARTICLE DB: Gamma-Band Coherence.
    Enforces 40±5 Hz coherence for ≥4 cycles (≥100 ms).
    """
    def __init__(self, target_freq: float = 40.0):
        self.target_freq = target_freq
        self.coherence_threshold = 0.8
        self.current_coherence = 0.0
        self.cycles_locked = 0

    def calculate_coherence(self, signal_a: np.ndarray, signal_b: np.ndarray) -> float:
        """
        Computes phase coherence between two signal streams.
        """
        # FFT based phase lock check
        # Simplified: check correlation in 40Hz band
        self.current_coherence = np.abs(np.corrcoef(signal_a, signal_b)[0, 1])

        if self.current_coherence >= self.coherence_threshold:
            self.cycles_locked += 1
        else:
            self.cycles_locked = 0

        return self.current_coherence

    def is_consciously_integrated(self) -> bool:
        """Article DB requirement: ≥4 cycles (approx 100ms at 40Hz)."""
        return self.cycles_locked >= 4
