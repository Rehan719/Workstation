import torch
from typing import Dict, Tuple, Optional
from ._utils import get_backend, to_numpy

class SchrödingerBridgeEngine:
    """
    Entropy-regularised optimal transport on path spaces.
    Solves the Schrödinger Bridge problem: min_π KL(π||K) s.t. π0=source, π1=target
    using Iterative Proportional Fitting (IPF) / Sinkhorn (Léonard 2014, Chen et al. 2021).
    """

    def compute_bridge(
        self,
        source_dist: torch.Tensor,
        target_dist: torch.Tensor,
        cost_matrix: torch.Tensor,
        epsilon: float = 0.01,
        max_iter: int = 100,
        tol: float = 1e-6
    ) -> Tuple[torch.Tensor, float, Dict]:
        """
        Compute the optimal transport plan (Schrödinger Bridge).

        Args:
            source_dist: Source distribution (marginal at t=0)
            target_dist: Target distribution (marginal at t=1)
            cost_matrix: Cost matrix (e.g., squared Euclidean distance)
            epsilon: Regularisation parameter (diffusion intensity)
            max_iter: Maximum number of IPF iterations
            tol: Convergence tolerance

        Returns:
            Tuple containing (transport_plan, kl_divergence, convergence_info)
        """
        xp = get_backend()

        # Convert torch tensors to backend arrays (CuPy or NumPy)
        mu = xp.array(source_dist.detach().cpu().numpy())
        nu = xp.array(target_dist.detach().cpu().numpy())
        C = xp.array(cost_matrix.detach().cpu().numpy())

        # Numerical stability guard: epsilon flooring
        epsilon = max(epsilon, 1e-8)

        # Gibbs kernel: K = exp(-C / epsilon) with stability guards
        K = xp.exp(-C / epsilon)

        # Iterative Proportional Fitting (IPF) / Sinkhorn iterations
        u = xp.ones_like(mu)
        v = xp.ones_like(nu)

        converged = False
        for iteration in range(max_iter):
            u_prev = u.copy()

            # Forward projection: match source marginal
            u = mu / (K @ v + 1e-30)

            # Backward projection: match target marginal
            v = nu / (K.T @ u + 1e-30)

            # Convergence check
            err = xp.max(xp.abs(u - u_prev))
            if err < tol:
                converged = True
                break

        # Compute optimal transport plan: π = diag(u) K diag(v)
        # More memory efficient implementation: u[:, None] * K * v[None, :]
        plan = u[:, None] * K * v[None, :]

        # Compute KL Divergence: KL(π||K) = <π, log(π/K)>
        # plan / K = u @ v.T
        # log(plan / K) = log(u) + log(v).T
        kl_div = float(xp.sum(plan * (xp.log(u + 1e-30)[:, None] + xp.log(v + 1e-30)[None, :])))

        # Return as torch tensor and metadata
        return (
            torch.from_numpy(to_numpy(plan)),
            kl_div,
            {
                "iterations": iteration + 1,
                "converged": converged,
                "error": float(to_numpy(err)),
                "epsilon": epsilon
            }
        )
