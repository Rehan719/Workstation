import logging

logger = logging.getLogger(__name__)

class RecoveryTimeMonitor:
    """
    DG-II: Perturbation Recovery Time.
    Quantifies milliseconds-to-seconds resilience after simulated stress.
    Empirical baseline: 14.2 +/- 3.1 seconds.
    """
    BASELINE = 14.2
    TOLERANCE = 0.20 # 20% tolerance

    def verify_recovery(self, recovery_time: float) -> float:
        """
        Returns a score based on how close recovery_time is to the baseline.
        """
        lower_bound = self.BASELINE * (1 - self.TOLERANCE)
        upper_bound = self.BASELINE * (1 + self.TOLERANCE)

        if lower_bound <= recovery_time <= upper_bound:
            score = 1.0
        else:
            diff = abs(recovery_time - self.BASELINE)
            score = max(0.0, 1.0 - (diff / self.BASELINE))

        logger.info(f"VERIFICATION: Recovery Time Score: {score:.4f} (Actual: {recovery_time:.2f}s)")
        return score
