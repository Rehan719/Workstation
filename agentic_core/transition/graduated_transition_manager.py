import logging
import time
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GraduatedTransitionManager:
    """
    ARTICLE 77/89: Graduated Balanced Transition Protocol.
    Manages the 5-cycle resource rebalancing from Triad-focus to 22-pillar balance.
    """
    def __init__(self, total_phases: int = 5):
        self.total_phases = total_phases
        self.current_phase = 0
        self.allocation_history = []

    def get_current_allocation(self) -> Dict[str, float]:
        """Calculates current resource weights based on transition progress."""
        progress = self.current_phase / self.total_phases
        # Transition from 60% Triad focus to 4.5% per pillar (1/22nd)
        triad_weight = 0.60 - (0.555 * progress)
        # Handle v93+ 22-pillar target: triad_weight should converge to 3/22 (~0.136)
        # progress=1.0 -> triad_weight = 0.60 - 0.555 = 0.045 (wait, 0.045*22=0.99)
        # So at progress 1.0, each of the 22 pillars gets 0.04545 (1/22)
        other_weight = (1.0 - triad_weight) / 19 if self.current_phase < self.total_phases else (1.0 / 22)

        return {
            "triad_aggregate": round(triad_weight, 4),
            "per_pillar": round(1.0 / 22, 4) if self.current_phase == self.total_phases else round(other_weight, 4),
            "progress_percent": progress * 100
        }

    def advance_cycle(self, gate_metrics: Dict[str, Any]) -> bool:
        """Attempts to advance to the next transition cycle."""
        if self.current_phase >= self.total_phases:
            logger.info("Transition complete. 22-Pillar Balance achieved.")
            return True

        # Validation gates
        if gate_metrics.get("fidelity", 0) < 0.95:
            logger.warning(f"Gate failure in phase {self.current_phase}: Low fidelity.")
            return False

        if gate_metrics.get("stability", 0) < 0.90:
            logger.warning(f"Gate failure in phase {self.current_phase}: Stability below threshold.")
            return False

        self.current_phase += 1
        logger.info(f"Transition Advanced to Cycle {self.current_phase}/{self.total_phases}")
        return True
