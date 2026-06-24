from typing import Dict, Any

class SafeRangeEnforcer:
    """CP-IV: Safe Range Enforcement."""

    def __init__(self):
        self.safe_ranges = {
            "synaptic_scaling_tau_h": (12.0, 25.0), # Article CP-II
            "learning_rate": (0.0001, 0.1),
            "anomaly_threshold": (0.5, 0.95),
            "peristaltic_delay": (50, 120) # Article CP-II
        }

    def validate_ranges(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        validated = {}
        for k, v in parameters.items():
            if k in self.safe_ranges:
                low, high = self.safe_ranges[k]
                validated[k] = max(low, min(high, v))
            else:
                validated[k] = v
        return validated

    def is_safe(self, parameter: str, value: Any) -> bool:
        if parameter in self.safe_ranges:
            low, high = self.safe_ranges[parameter]
            return low <= value <= high
        return True
