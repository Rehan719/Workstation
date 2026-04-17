import pytest
import torch
import torch.nn as nn
from agentic_core.biomimicry.minimisation.core.diffusion_engine import ScoreBasedDiffusion

class StableScoreNet(nn.Module):
    def forward(self, y, t):
        # Lipschitz continuous score function
        return -0.5 * y

@pytest.mark.asyncio
async def test_diffusion_stability_and_rollback():
    score_net = StableScoreNet()
    model = ScoreBasedDiffusion(score_net)

    y0 = torch.randn(10)
    # Forward-like step
    y1 = model.reverse_step(y0, t=1.0, dt=0.01)

    assert not torch.isnan(y1).any()
    assert not torch.isinf(y1).any()

    # Verify rollback (Art. 1106)
    # Note: due to SDE randomness, it won't be exact, but should be stable
    y_recovered = model.rollback(y1, steps=10)
    assert y_recovered.shape == y0.shape
    assert not torch.isnan(y_recovered).any()
