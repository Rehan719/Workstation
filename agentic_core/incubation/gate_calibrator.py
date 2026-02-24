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
