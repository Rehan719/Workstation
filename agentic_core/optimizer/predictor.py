import logging
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DemandPredictor:
    """
    ARTICLE 311: Demand Predictor.
    Forecasts resource needs based on history using probabilistic models.
    """
    def predict_demand(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predicts expected CPU and Agent demand for the next window.
        Uses a weighted moving average with variance-based confidence.

        W767 (FU-1134) - NOTHING CALLS THIS: AdaptiveResourceOptimizer builds a DemandPredictor and never asks it.
        The host CPU figure can be None since W746 (an unread reading); a None is skipped and COUNTED, never
        averaged as 0, and a history with no readable CPU figure predicts nothing rather than a typed default.
        """
        cpu_vals = [h.get("cpu_percent") for h in (history or [])]
        skipped = sum(1 for v in cpu_vals if not isinstance(v, (int, float)) or isinstance(v, bool))
        cpu_vals = [float(v) for v in cpu_vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if not cpu_vals:
            return {"expected_cpu": None, "expected_agents": None, "confidence": None,
                    "readings_used": 0, "readings_skipped": skipped,
                    "basis": "no readable CPU figure in the history, so nothing is predicted"}

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
            "confidence": float(confidence),
            "readings_used": len(cpu_vals), "readings_skipped": skipped,
        }
