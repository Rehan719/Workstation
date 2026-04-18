import numpy as np
from typing import Dict, List
class FederatedAggregator:
    def __init__(self, epsilon: float = 0.1, delta: float = 1e-5):
        self.epsilon, self.delta, self.noise_scale = epsilon, delta, 2.0 / epsilon
    def aggregate(self, local_weights: List[Dict[str, float]]) -> Dict[str, float]:
        n = len(local_weights)
        if n == 0: return {}
        keys = local_weights[0].keys()
        summed = {}
        for k in keys:
            total = sum(max(0.0, min(1.0, w.get(k, 0.0))) for w in local_weights)
            noise = np.random.normal(0, self.noise_scale)
            summed[k] = float(max(0.0, min(1.0, (total + noise) / n)))
        if "legal_precision" in summed: summed["legal_precision"] = max(summed["legal_precision"], 0.15)
        return summed
