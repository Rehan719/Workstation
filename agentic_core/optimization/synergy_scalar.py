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
        """Calculates synergy based on communication overhead and cross-layer metrics."""
        # CR-II: Cross-Layer Synergy Metrics
        overhead = subsystem_metrics.get("comm_overhead", 0.0)
        binding_accuracy = subsystem_metrics.get("perceptual_binding_accuracy", 1.0)
        social_alignment = subsystem_metrics.get("social_alignment", 1.0)

        # Synergy increases with accuracy and decreases with overhead
        # Updated formula to align with test: base_synergy - overhead/2 - contention/2
        contention = subsystem_metrics.get("resource_contention", 0.0)
        base_synergy = (binding_accuracy + social_alignment) / 2
        self.scalar = round(max(0.0, base_synergy - (overhead + contention) / 2), 4)

        if self.scalar < 0.6:
            logger.warning(f"LOW SYNERGY DETECTED: {self.scalar}. Triggering optimization.")

        return self.scalar
