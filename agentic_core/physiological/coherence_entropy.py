import numpy as np
import logging
from scipy.stats import entropy

logger = logging.getLogger(__name__)

class CoherenceEntropy:
    """
    DH-II: Coherence Entropy Bounds.
    Shannon entropy of system-wide signaling coherence (H < 0.35 nats).
    """
    BOUND = 0.35

    def calculate_entropy(self, distributions: np.ndarray) -> float:
        """
        Calculates Shannon entropy of the signaling distribution.
        """
        h = entropy(distributions)
        is_within_bounds = h < self.BOUND

        logger.info(f"PHYSIOLOGICAL: Coherence Entropy: {h:.4f} nats (Within Bounds: {is_within_bounds})")
        return h
