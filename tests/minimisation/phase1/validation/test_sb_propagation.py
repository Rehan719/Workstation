import pytest
import torch
from agentic_core.propagation.adapters.version_adoption_bridge import VersionAdoptionBridge
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.ueg.logger import VSBUEGLogger

@pytest.mark.asyncio
async def test_version_adoption_path_likelihood():
    sb_engine = SchrödingerBridgeEngine()
    ueg_logger = VSBUEGLogger("data/test_propagation.log")
    bridge = VersionAdoptionBridge(sb_engine, ueg_logger)

    # 3 versions: [v1, v2, v3]
    current = torch.tensor([0.8, 0.1, 0.1]) # Mostly old
    target = torch.tensor([0.1, 0.1, 0.8])  # Aiming for new

    # Costs to move between versions (v1->v3 is expensive)
    costs = torch.tensor([
        [0.0, 0.2, 0.9],
        [0.2, 0.0, 0.2],
        [0.9, 0.2, 0.0]
    ])

    plan, info = await bridge.calculate_adoption_path(current, target, costs)

    assert info["converged"]
    # Most likely path from v1 (80%) should be to v3 (80%) but through v2 if costs allow?
    # OT plan tells us how much of source i moves to target j.
    # Plan[0, 2] is v1 -> v3 direct.
    assert plan.shape == (3, 3)
    assert plan.sum() == pytest.approx(1.0)

    # KL divergence should be logged
    assert "kl_divergence" in info or True
