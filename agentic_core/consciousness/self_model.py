import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class UnifiedSelfModel:
    """
    Unified representation of the organism's state.
    Derived from subsystem state vectors.
    """
    def __init__(self):
        # Body Schema / State
        self.self_image = {
            "allostatic_health": 1.0,
            "resource_map": {},
            "capabilities": []
        }
        # Prospective Memory
        self.temporal_horizon = {
            "future_load_forecast": 0.0,
            "aging_risk": 0.0
        }
        # Limbic System Weights
        self.value_system = {
            "survival": 0.95,
            "efficiency": 0.7,
            "curiosity": 0.5
        }
        # Salience Network
        self.attention_focus = "STEADY_STATE"

    def update_from_workspace(self, workspace_data: Dict[str, Any]):
        """Reconstructs self-model from global broadcast."""
        # Focus on Molecular Triad for health grounding (Layer DN)
        triad_entry = workspace_data.get("molecular_triad", {}).get("data", {})
        if triad_entry:
            energy = triad_entry.get("atp_adp_ratio", 5.0)
            ros = triad_entry.get("ros_level", 0.3)

            # Update health metric
            self.self_image["allostatic_health"] = max(0.0, 1.0 - (ros / 4.0) + (energy / 20.0))

            # Dynamic attention shift
            if ros > 1.2:
                self.attention_focus = "STRESS_RESPONSE"
            elif energy < 2.0:
                self.attention_focus = "METABOLIC_CONSERVATION"
            else:
                self.attention_focus = "TASK_EXECUTION"

        logger.debug(f"SELF_MODEL: Health={self.self_image['allostatic_health']:.2f}, Focus={self.attention_focus}")
