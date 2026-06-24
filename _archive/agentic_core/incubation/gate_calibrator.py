import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GateCalibrator:
    """Applies and enforces calibrated gates."""

    def __init__(self):
        self.current_thresholds = {"approval_threshold": 0.7}

    def apply_thresholds(self, thresholds: Dict[str, float]):
        logger.info(f"Applying new thresholds: {thresholds}")
        self.current_thresholds.update(thresholds)

    def calibrate(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Legacy compatibility."""
        return self.current_thresholds
from typing import Dict

class GateCalibrator:
    """Dynamically adjusts approval thresholds based on ML risk predictions."""

    def calibrate(self, metrics: Dict[str, float]) -> Dict[str, float]:
        # Calibration logic: higher metrics -> stricter thresholds
        perplexity = metrics.get("perplexity", 0)

        # CO-III: IC50 calibrated to perplexity > 42.3
        threshold = 0.5
        if perplexity > 42.3:
            threshold = 0.8

        return {"approval_threshold": threshold}
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
