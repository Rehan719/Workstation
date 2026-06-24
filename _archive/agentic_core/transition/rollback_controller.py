import logging

logger = logging.getLogger(__name__)

class RollbackController:
    """Automatic reversal mechanism if transition degradation is detected."""

    def __init__(self, degradation_threshold: float = 0.04, min_fidelity: float = 0.96):
        self.threshold = degradation_threshold
        self.min_fidelity = min_fidelity

    def should_rollback(self, current_fidelity: float, trend: float) -> bool:
        if current_fidelity < self.min_fidelity:
            logger.error(f"ROLLBACK TRIGGERED: Fidelity {current_fidelity} below guardrail {self.min_fidelity}")
            return True
        if trend < -self.threshold:
            logger.error(f"ROLLBACK TRIGGERED: Degradation trend {trend} exceeds threshold {self.threshold}")
            return True
        return False
