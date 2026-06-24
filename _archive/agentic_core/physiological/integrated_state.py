import numpy as np
import logging
from scipy.spatial.distance import mahalanobis

logger = logging.getLogger(__name__)

class IntegratedStateMonitor:
    """
    DH-IV: Integrated State Identification.
    Mahalanobis distance tracking deviation from reference population stats across 12+ biomarkers.
    """
    def __init__(self):
        # Reference mean and covariance (simulated based on empirical ranges)
        self.reference_mean = np.array([0.5] * 12)
        self.reference_inv_cov = np.eye(12) # Simplified

    def calculate_distance(self, current_biomarkers: np.ndarray) -> float:
        """
        Calculates Mahalanobis distance from healthy reference state.
        """
        if len(current_biomarkers) != 12:
            logger.error("PHYSIOLOGICAL: Invalid biomarker vector length.")
            return 999.0

        dist = mahalanobis(current_biomarkers, self.reference_mean, self.reference_inv_cov)
        logger.info(f"PHYSIOLOGICAL: Integrated State Mahalanobis Distance: {dist:.4f}")
        return dist
