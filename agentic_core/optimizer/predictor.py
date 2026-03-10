import logging
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DemandPredictor:
    """
    ARTICLE 311: Demand Predictor.
    Forecasts resource needs based on history using probabilistic models.
    """
    def predict_demand(self, history: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Predicts expected CPU and Agent demand for the next window.
        Uses a weighted moving average with variance-based confidence.
        """
        if not history:
            return {"expected_cpu": 30.0, "expected_agents": 5.0, "confidence": 0.5}

        cpu_vals = [h.get("cpu_percent", 0) for h in history]

        # Simple weighted moving average (favoring recent data)
        weights = np.linspace(0.1, 1.0, len(cpu_vals))
        expected_cpu = np.average(cpu_vals, weights=weights)

        # Predicted agent demand correlates with CPU usage + base load
        expected_agents = (expected_cpu / 10.0) + 2.0

        variance = np.var(cpu_vals)
        confidence = 1.0 / (1.0 + variance) # Higher variance -> lower confidence

        return {
            "expected_cpu": float(expected_cpu),
            "expected_agents": float(expected_agents),
            "confidence": float(confidence)
        }
