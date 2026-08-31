import torch
import torch.nn as nn
try:
    import torchsde  # optional: SDE solver for the structural-evolution diffusion engine
except Exception:  # pragma: no cover - keeps the module import-safe without the optional dep
    torchsde = None
from typing import Callable, Optional, Tuple

class SDEWrapper(nn.Module):
    """Bridge between functional drift/diffusion and torchsde Interface."""
    def __init__(self, drift: Callable, diffusion: Callable, sde_type: str = "ito"):
        super().__init__()
        self.drift_fn = drift
        self.diffusion_fn = diffusion
        self.sde_type = sde_type
        self.noise_type = "diagonal"

    def f(self, t, y):
        return self.drift_fn(t, y)

    def g(self, t, y):
        return self.diffusion_fn(t, y)

class DiffusionEngine:
    """
    SDE integrator for structural evolution using torchsde.
    Supports Itô and Stratonovich integration.
    """

    def __init__(self, drift: Callable, diffusion: Callable):
        self.sde = SDEWrapper(drift, diffusion)

    def integrate(
        self,
        y0: torch.Tensor,
        t_span: torch.Tensor,
        dt: float = 0.01,
        adaptive: bool = True
    ) -> torch.Tensor:
        """
        Integrate SDE using torchsde's optimized solvers.
        """
        if torchsde is None:
            raise RuntimeError("DiffusionEngine.integrate requires the optional 'torchsde' package "
                               "(pip install torchsde).")
        # Ensure y0 has batch dimension for torchsde
        if y0.dim() == 1:
            y_in = y0.unsqueeze(0)
        else:
            y_in = y0

        trajectory = torchsde.sdeint(
            self.sde,
            y_in,
            t_span,
            dt=dt,
            adaptive=adaptive,
            method="srk" # Strong order 1.5 solver
        )

        # Remove batch dim if it was added
        if y0.dim() == 1:
            return trajectory.squeeze(1)
        return trajectory

class ScoreBasedDiffusion(nn.Module):
    """
    Score-based generative model for structural adaptation using torchsde.
    Inverse-diffusion implementation (Art. 1106).
    """
    def __init__(self, score_network: nn.Module, beta_min: float = 0.1, beta_max: float = 20.0):
        super().__init__()
        self.score_net = score_network
        self.beta_min = beta_min
        self.beta_max = beta_max

    def _get_beta(self, t: float) -> float:
        return self.beta_min + t * (self.beta_max - self.beta_min)

    def reverse_step(self, y: torch.Tensor, t: float, dt: float) -> torch.Tensor:
        """Perform a single reverse diffusion step (discrete approximation)."""
        beta = self._get_beta(t)
        # Score network grad log p(y)
        score = self.score_net(y, torch.tensor(t, device=y.device))

        # Reverse SDE drift: f_rev = -0.5 * beta * (y + 2 * score)
        drift = -0.5 * beta * (y + 2 * score)
        diffusion = beta ** 0.5

        dw = torch.randn_like(y) * (abs(dt) ** 0.5)
        return y + drift * dt + diffusion * dw

    def rollback(self, y_final: torch.Tensor, steps: int = 50) -> torch.Tensor:
        """Explicit Article 1106 Reversibility implementation."""
        y = y_final
        dt = -1.0 / steps
        for i in range(steps, 0, -1):
            t = i / steps
            y = self.reverse_step(y, t, dt)
        return y
