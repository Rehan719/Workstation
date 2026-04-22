import numpy as np
from ...biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
import torch

class ClimateDomainAdapter:
    """Climate domain minimisation adapter (Phase 8)."""
    def __init__(self, ot_router: OptimalTransportRouter):
        self.ot = ot_router

    def optimise_carbon_trajectory(self, emissions: list, reduction_target: float):
        source = torch.tensor(emissions).float()
        target = source * (1.0 - reduction_target)

        # Flattened cost matrix for 1D distribution transport
        cost_matrix = torch.abs(source.unsqueeze(1) - target.unsqueeze(0))

        plan, dist, info = self.ot.solve(source, target, cost_matrix, epsilon=0.01)
        return {"optimised_path": plan.sum(dim=0).tolist(), "wasserstein_dist": dist}
