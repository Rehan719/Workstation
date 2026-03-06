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

    def get_v93_readiness(self) -> Dict[str, Any]:
        """Assesses readiness for v93.0 POLYMATH era."""
        if not self.telemetry: return {"status": "NO_DATA"}

        latest_fidelity = self.telemetry[-1]["metrics"].get("fidelity", 0)
        stability_trend = self.get_trend("stability")

        ready = latest_fidelity >= 0.98 and stability_trend >= 0

        return {
            "status": "READY" if ready else "IN_TRANSITION",
            "fidelity": latest_fidelity,
            "trend": stability_trend,
            "v93_gate": ready
        }
