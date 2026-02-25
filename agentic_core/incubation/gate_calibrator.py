from typing import Dict

class GateCalibrator:
    """Manages the application of calibrated thresholds to approval gates."""

    def __init__(self):
        self.current_thresholds = {
            "approval_threshold": 0.7,
            "replication_gate": 0.8
        }

    def apply_thresholds(self, thresholds: Dict[str, float]):
        self.current_thresholds.update(thresholds)

    def should_pass(self, score: float, gate_name: str) -> bool:
        threshold = self.current_thresholds.get(gate_name, 1.0)
        return score >= threshold
