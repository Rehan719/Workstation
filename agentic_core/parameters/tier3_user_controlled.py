from typing import Dict, Any

class Tier3UserControlled:
    """CP-III: User-Controlled Parameters."""

    def __init__(self):
        # Maps user-facing names to Tier 2 internal keys
        self.controllable_map = {
            "synaptic_tau": "synaptic_scaling_tau_h",
            "detection_threshold": "anomaly_threshold",
            "explanation_detail": "xai_sensitivity"
        }
        self.overrides = {}

    def is_controllable(self, name: str) -> bool:
        return name in self.controllable_map

    def set_parameter(self, name: str, value: Any):
        internal_key = self.controllable_map[name]
        self.overrides[internal_key] = value

    def get_overrides(self) -> Dict[str, Any]:
        return self.overrides
