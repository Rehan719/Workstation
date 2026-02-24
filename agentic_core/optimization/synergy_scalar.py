import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SynergyScalar:
    """
    CB-I: Resource Synergy Scalar.
    Quantifies effective collaboration among subsystems (0.0 - 1.0).
    """
    def __init__(self):
        self.scalar = 1.0

    def compute_synergy(self, subsystem_metrics: Dict[str, Any]) -> float:
        """Calculates synergy based on communication overhead and resource contention."""
        # High contention or high overhead reduces synergy
        overhead = subsystem_metrics.get("comm_overhead", 0.0)
        contention = subsystem_metrics.get("resource_contention", 0.0)

        self.scalar = round(max(0.0, 1.0 - (overhead + contention) / 2), 4)

        if self.scalar < 0.6:
            logger.warning(f"LOW SYNERGY DETECTED: {self.scalar}. Triggering optimization.")

        return self.scalar
