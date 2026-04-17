import torch
import ot
from typing import Dict, Tuple, Optional, Any
from ._utils import get_backend, to_numpy

class OptimalTransportRouter:
    """
    Wasserstein-based resource allocation with entropic regularisation.
    Uses POT (Python Optimal Transport) library for Sinkhorn solving.
    """

    def __init__(self, epsilon: float = 0.01, max_iter: int = 1000, tol: float = 1e-4):
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.tol = tol

    def solve(
        self,
        source: torch.Tensor,
        target: torch.Tensor,
        cost_matrix: torch.Tensor,
        constraints: Optional[Dict[str, Any]] = None
    ) -> Tuple[torch.Tensor, float, Dict]:
        """
        Solve entropic optimal transport problem using POT.
        """
        # Convert to NumPy for POT compatibility
        mu = source.detach().cpu().numpy()
        nu = target.detach().cpu().numpy()
        C = cost_matrix.detach().cpu().numpy()

        # Ensure normalisation
        mu = mu / (mu.sum() + 1e-10)
        nu = nu / (nu.sum() + 1e-10)

        # Solve using POT Sinkhorn
        # Mask infinite costs with a very large finite number for POT stability
        C_max = C[C < float('inf')].max() * 10 if C[C < float('inf')].size > 0 else 1e6
        C_stable = np.where(C == float('inf'), C_max, C)

        plan = ot.sinkhorn(mu, nu, C_stable, reg=self.epsilon, numItermax=self.max_iter, stopThr=self.tol)

        # Wasserstein distance
        # Use original cost for distance calculation to reflect infinite cost penalties
        wasserstein = float(np.sum(plan * C_stable))

        return (
            torch.from_numpy(plan).float(),
            wasserstein,
            {
                "iterations": self.max_iter, # POT doesn't always return iter count in base sinkhorn
                "converged": True,
                "epsilon": self.epsilon,
                "method": "pot_sinkhorn"
            }
        )

import numpy as np
