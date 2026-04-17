import pytest
import torch
import torch.nn as nn
from agentic_core.recombination.adapters.diffusion_merge_adapter import DiffusionMergeAdapter, Adapter
from agentic_core.biomimicry.minimisation.core.diffusion_engine import ScoreBasedDiffusion
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.ueg.logger import VSBUEGLogger

class MockScoreNet(nn.Module):
    def forward(self, y, t): return -y

@pytest.fixture
def merge_system():
    score_net = MockScoreNet()
    diffusion_model = ScoreBasedDiffusion(score_net)
    legal_engine = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    ueg_logger = VSBUEGLogger("data/test_week7_merge.log")
    return DiffusionMergeAdapter(diffusion_model, legal_engine, ueg_logger)

@pytest.mark.asyncio
async def test_diffusion_module_pruning_and_token(merge_system):
    # Setup small params to ensure thresholding
    a = Adapter(params=torch.randn(100) * 0.05, domain="legal")
    b = Adapter(params=torch.randn(100) * 0.05, domain="legal")

    context = {"type": "merge", "domain": "legal", "required_statutes": ["EqualityAct2010"], "jurisdiction": "UK"}

    merged = await merge_system.merge_adapters(a, b, context, timesteps=5)

    # Verify parameter reduction (via manual check of pruning logic)
    pruned, reduction = merge_system._entropy_prune(torch.tensor([0.001, 0.5]), threshold=0.01)
    assert reduction == 0.5

    # Verify UEG log contains rollback token
    with open("data/test_week7_merge.log", "r") as f:
        last_event = f.readlines()[-1]
        assert "rollback_token" in last_event
        assert "params_reduced_pct" in last_event
