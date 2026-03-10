import logging
import numpy as np
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DemandPredictor:
    """LSTM-inspired demand forecasting for v100.0 baseline."""
    def __init__(self, history_size: int = 100):
        self.history_size = history_size
        self.data = []

    def observe(self, value: float):
        self.data.append(value)
        if len(self.data) > self.history_size:
            self.data.pop(0)

    def predict_next(self) -> float:
        """Simple moving average with momentum for v100.0 baseline."""
        if not self.data:
            return 0.0
        if len(self.data) < 5:
            return self.data[-1]

        # Simple linear trend prediction
        recent = self.data[-5:]
        trend = np.mean(np.diff(recent))
        prediction = recent[-1] + trend
        return max(0.0, prediction)

    def get_forecast_error(self, actual: float, predicted: float) -> float:
        if actual == 0: return 0.0
        return abs(actual - predicted) / actual
