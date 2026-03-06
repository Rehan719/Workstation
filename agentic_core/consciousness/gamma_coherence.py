import numpy as np
import logging
from scipy.signal import hilbert

logger = logging.getLogger(__name__)

class GammaCoherenceMonitor:
    """
    ARTICLE DB: Gamma-Band Coherence (40±5 Hz).
    Implements Phase Locking Value (PLV) monitoring.
    Target: ≥4 cycles (≥100 ms).
    """
    def __init__(self, target_freq: float = 40.0):
        self.target_freq = target_freq
        self.threshold = 0.8
        self.consecutive_integrated = 0

    def calculate_coherence(self, signal_a: np.ndarray, signal_b: np.ndarray) -> float:
        """
        Calculates Phase Locking Value (PLV) between two signals.
        """
        # Analytic signal via Hilbert transform
        analytic_a = hilbert(signal_a)
        analytic_b = hilbert(signal_b)

        # Extract phase
        phase_a = np.angle(analytic_a)
        phase_b = np.angle(analytic_b)

        # PLV = | (1/N) * sum( exp(i * (phi_a - phi_b)) ) |
        phase_diff = phase_a - phase_b
        plv = np.abs(np.mean(np.exp(1j * phase_diff)))

        if plv >= self.threshold:
            self.consecutive_integrated += 1
        else:
            self.consecutive_integrated = 0

        return float(plv)

    def is_consciously_integrated(self) -> bool:
        """Requirement: ≥4 cycles (approx 100ms at 40Hz)."""
        return self.consecutive_integrated >= 4
