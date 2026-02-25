from typing import Dict

class WeightedRatioAdjuster:
    """CQ-V: Weighted Adjustment Formula for the 70/30 split."""

    def __init__(self):
        # Initial weights for online RL optimization
        self.weights = {
            "complexity": 0.05,
            "degradation": 0.1,
            "engagement": 0.05,
            "novelty": 0.1
        }

    def calculate(self, baseline: float, scores: Dict[str, float]) -> float:
        adjustment = sum(scores[k] * self.weights[k] for k in scores)
        new_innovation = baseline + adjustment

        # Bounds: 0.2 to 0.5 (as per Article CQ)
        return max(0.2, min(0.5, new_innovation))
