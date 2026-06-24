import logging
from typing import Dict, Any, List
from .tier1_immutable import Tier1Immutable
from .tier2_tunable import Tier2Tunable
from .tier3_user_controlled import Tier3UserControlled
from .safe_range_enforcer import SafeRangeEnforcer
from .workload_profiler import WorkloadProfiler
from .veto_handler import VetoHandler

logger = logging.getLogger(__name__)

class TieredParameterManager:
    """
    ARTICLE CP: Tiered Biological Parameterization.
    Balances foundational stability with dynamic adaptability.
    """
    def __init__(self):
        self.tier1 = Tier1Immutable()
        self.tier2 = Tier2Tunable()
        self.tier3 = Tier3UserControlled()
        self.enforcer = SafeRangeEnforcer()
        self.profiler = WorkloadProfiler()
        self.veto = VetoHandler()

    def configure_for_workload(self, workload_type: str):
        """CP-V: Workload-Aware Tuning."""
        logger.info(f"CP: Configuring parameters for workload: {workload_type}")

        # 1. Profile workload
        profile = self.profiler.get_profile(workload_type)

        # 2. Apply Tier 2 adjustments within safe bounds
        proposed_tier2 = self.tier2.propose_adjustments(profile)
        validated_tier2 = self.enforcer.validate_ranges(proposed_tier2)

        self.tier2.apply(validated_tier2)
        logger.info(f"CP-V: Tier 2 parameters optimized for {workload_type}.")

    def user_override(self, parameter: str, value: Any):
        """CP-III: User-Controlled parameters via dashboard."""
        if self.tier3.is_controllable(parameter):
            if self.enforcer.is_safe(parameter, value):
                self.tier3.set_parameter(parameter, value)
                logger.info(f"CP-III: User override applied to {parameter}.")
            else:
                logger.warning(f"CP-IV: Blocked unsafe override for {parameter}.")
        else:
            # CP-I: Foundationally Fixed veto
            self.veto.trigger_veto(f"Attempted override of Tier 1 parameter: {parameter}")

    def get_synaptic_scaling(self) -> float:
        """CP-II: Environmentally Tunable synaptic scaling τ_H."""
        return self.tier2.get_parameter("synaptic_scaling_tau_h")
