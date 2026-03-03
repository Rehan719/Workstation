import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TransitionMonitor:
    """Continuous tracking of rebalancing progress."""

    def __init__(self):
        self.telemetry = []

    def log_state(self, phase: int, metrics: Dict[str, Any]):
        entry = {
            "timestamp": time.time(),
            "phase": phase,
            "metrics": metrics
        }
        self.telemetry.append(entry)
        logger.info(f"Transition Monitor [Phase {phase}]: Fidelity={metrics.get('fidelity')}, Consistency={metrics.get('consistency')}")

    def get_trend(self, metric: str) -> float:
        """Calculates trend slope for a given metric."""
        if len(self.telemetry) < 2: return 0.0
        latest = self.telemetry[-1]["metrics"].get(metric, 0)
        previous = self.telemetry[-2]["metrics"].get(metric, 0)
        return latest - previous
