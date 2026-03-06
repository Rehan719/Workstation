import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TransitionStateMonitor:
    """
    ARTICLE 77/89: Transition State Monitor.
    Provides continuous, real-time feedback on the rebalancing progress.
    """
    def __init__(self):
        self.telemetry_log: List[Dict[str, Any]] = []

    def record_state(self, phase: int, metrics: Dict[str, Any]):
        """Logs current transition metrics."""
        record = {
            "phase": phase,
            "metrics": metrics,
            "timestamp": metrics.get("timestamp", 0)
        }
        self.telemetry_log.append(record)
        logger.info(f"MONITOR: Phase {phase} telemetry recorded.")

    def analyze_trend(self) -> str:
        """Analyzes performance trends during transition."""
        if len(self.telemetry_log) < 2:
            return "STABLE"

        last = self.telemetry_log[-1]["metrics"].get("fidelity", 1.0)
        prev = self.telemetry_log[-2]["metrics"].get("fidelity", 1.0)

        if last < prev - 0.05:
            return "DEGRADING"
        return "STABLE"

class RollbackController:
    """
    ARTICLE 77/89: Rollback Controller.
    Reverts the system to a previous stable state if degradation is detected.
    """
    def __init__(self, manager_instance):
        self.manager = manager_instance

    def execute_rollback(self):
        """Decrements the current phase to restore stability."""
        if self.manager.current_phase > 0:
            logger.warning(f"ROLLBACK: Reverting from phase {self.manager.current_phase} to {self.manager.current_phase - 1}")
            self.manager.current_phase -= 1
            return True
        logger.error("ROLLBACK: Already at baseline phase 0. Cannot revert further.")
        return False
