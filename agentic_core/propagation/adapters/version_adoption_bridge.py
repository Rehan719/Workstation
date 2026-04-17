import torch
from typing import Dict, Any, List, Tuple
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.ueg.logger import VSBUEGLogger

class VersionAdoptionBridge:
    """
    IDBO Layer 6: Propagation.
    Determines optimal version adoption paths between agent groups
    using Schrödinger Bridges to minimise update friction (entropy).
    """

    def __init__(
        self,
        sb_engine: SchrödingerBridgeEngine,
        ueg_logger: VSBUEGLogger
    ):
        self.sb = sb_engine
        self.ueg = ueg_logger

    async def calculate_adoption_path(
        self,
        current_adoption: torch.Tensor,
        target_adoption: torch.Tensor,
        transition_costs: torch.Tensor,
        epsilon: float = 0.05
    ) -> Tuple[torch.Tensor, Dict[str, Any]]:
        """
        Find most-likely path from current version state to target.

        Args:
            current_adoption: Distribution of versions currently in the swarm
            target_adoption: Desired distribution of versions
            transition_costs: Matrix representing friction between version jumps
            epsilon: Regularisation (willingness to take non-optimal jumps)
        """
        # 1. Normalise marginals
        mu = current_adoption / current_adoption.sum()
        nu = target_adoption / target_adoption.sum()

        # 2. Solve Schrödinger Bridge (IPF)
        plan, kl_div, info = self.sb.compute_bridge(
            source_dist=mu,
            target_dist=nu,
            cost_matrix=transition_costs,
            epsilon=epsilon
        )

        # 3. Log propagation event to UEG
        await self.ueg.log_minimisation_event("version_propagation_path", {
            "kl_divergence": kl_div,
            "convergence": info,
            "mean_transition_cost": float((plan * transition_costs).sum().item()),
            "entropy_production": float(-torch.sum(plan * torch.log(plan + 1e-10)).item())
        }, context={"layer": "L6_Propagation", "strategy": "stochastic_bridge"})

        return plan, info
