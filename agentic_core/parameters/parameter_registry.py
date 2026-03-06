import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ParameterRegistry:
    """
    BU-I: Three-Tier Control Hierarchy.
    T1: Foundationally Fixed, T2: Environmentally Tunable, T3: User-Controlled.
    """
    def __init__(self):
        self.registry = {
            "reflex_latency_ms": {"tier": 1, "value": 50.0},
            "crypto_key_size": {"tier": 1, "value": 384},
            "synaptic_scaling_tau": {"tier": 2, "value": 18.6},
            "learning_rate": {"tier": 2, "value": 0.001},
            "dashboard_theme": {"tier": 3, "value": "dark"},
            "xai_sensitivity": {"tier": 3, "value": 0.5}
        }

    def get_parameter(self, name: str) -> Any:
        return self.registry.get(name, {}).get("value")

    def update_parameter(self, name: str, value: Any, requester_tier: int = 3) -> bool:
        param = self.registry.get(name)
        if not param: return False

        # BU-VI: Runtime Guard Enforcement
        if param["tier"] == 1:
            logger.error(f"RUNTIME VETO: Attempt to mutate Tier 1 parameter '{name}'")
            return False

        if requester_tier > param["tier"]:
            logger.warning(f"ACCESS DENIED: Tier {requester_tier} cannot mutate Tier {param['tier']} parameter")
            return False

        param["value"] = value
        logger.info(f"PARAMETER UPDATED: {name} = {value}")
        return True
