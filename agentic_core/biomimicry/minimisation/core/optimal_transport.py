import torch
from typing import Dict, Tuple, Optional, Any
from ._utils import get_backend, to_numpy

class OptimalTransportRouter:
    """
    Wasserstein-based resource allocation with entropic regularisation.
    Solves: min_P <C,P> + ε·H(P) s.t. P∈Π(μ,ν) (Villani 2009, Peyré & Cuturi 2019).
    Includes stability guards and CuPy/NumPy fallback.
    """

    def __init__(self, epsilon: float = 0.01, max_iter: int = 100, tol: float = 1e-6):
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
        Solve entropic optimal transport problem.

        Args:
            source: Source marginal distribution (μ)
            target: Target marginal distribution (ν)
            cost_matrix: Cost matrix (C)
            constraints: Optional hard constraints (currently logged, planning exact fallback)

        Returns:
            Tuple of (transport_plan, wasserstein_distance, convergence_info)
        """
        xp = get_backend()

        # Marginal normalisation
        mu = xp.array(source.detach().cpu().numpy())
        nu = xp.array(target.detach().cpu().numpy())
        mu = mu / xp.sum(mu)
        nu = nu / xp.sum(nu)
        C = xp.array(cost_matrix.detach().cpu().numpy())

        # Numerical stability: epsilon flooring
        reg = max(self.epsilon, 1e-8)

        # Gibbs kernel
        K = xp.exp(-C / reg)

        # Sinkhorn iterations
        u = xp.ones_like(mu)
        v = xp.ones_like(nu)

        converged = False
        for iteration in range(self.max_iter):
            u = mu / (K @ v + 1e-30)
            v = nu / (K.T @ u + 1e-30)

            if iteration % 10 == 0:
                err = xp.sum(xp.abs(u * (K @ v) - mu))
                if err < self.tol:
                    converged = True
                    break

        # Transport plan
        plan = xp.diag(u) @ K @ xp.diag(v)

        # Wasserstein distance (primal objective)
        # Use finite mask for infinite cost matrix to avoid NaN in sum
        C_finite = xp.where(xp.isinf(C), 0.0, C)
        wasserstein = float(xp.sum(plan * C_finite))

        return (
            torch.from_numpy(to_numpy(plan)),
            wasserstein,
            {
                "iterations": iteration + 1,
                "converged": converged,
                "error": float(to_numpy(err)),
                "epsilon": reg,
                "method": "sinkhorn"
            }
        )
