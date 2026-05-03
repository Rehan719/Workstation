import pytest
import torch
from agentic_core.minimisation.recirculation.omega_protocol import OmegaProtocol
from agentic_core.minimisation.recirculation.meta_rl_tuner import MetaRLTuner
from agentic_core.minimisation.recirculation.self_amendment import SelfAmendmentGenerator
from agentic_core.minimisation.pipeline import MinimisationPipeline
from agentic_core.orchestration.adapters.legal_aware_ot_router import LegalAwareOptimalTaskRouter
from agentic_core.evolution.adapters.schrodinger_evolution_adapter import BridgeGuidedEvolution
from agentic_core.recombination.adapters.diffusion_merge_adapter import DiffusionMergeAdapter
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.biomimicry.minimisation.core.diffusion_engine import ScoreBasedDiffusion
from agentic_core.gaas.adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from core.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.ueg.logger import VSBUEGLogger
import torch.nn as nn

class MockScoreNet(nn.Module):
    def forward(self, y, t): return -y

@pytest.fixture
def macro_system():
    ueg = VSBUEGLogger("data/test_phase2.log")
    ot_core = OptimalTransportRouter()
    sb_core = SchrödingerBridgeEngine()
    legal_engine = UKLegalPrecisionEngineImpl("configs/legal_precision.yaml")
    base_gaas = GaaSValidatorV4("configs/constitutional_genome_v138.yaml", "configs/legal_precision.yaml")
    gaas = EntropyRegularisedGaaS(base_gaas, legal_engine)

    ot_router = LegalAwareOptimalTaskRouter(ot_core, legal_engine, ueg)
    sb_evolution = BridgeGuidedEvolution(sb_core, gaas, ueg)

    score_net = MockScoreNet()
    diffusion_model = ScoreBasedDiffusion(score_net)
    diffusion_merge = DiffusionMergeAdapter(diffusion_model, legal_engine, ueg)

    pipeline = MinimisationPipeline(ot_router, sb_evolution, diffusion_merge, ueg)

    return OmegaProtocol(pipeline, ueg), ueg, sb_core

@pytest.mark.asyncio
async def test_omega_protocol_macro_cycle(macro_system):
    protocol, ueg, _ = macro_system

    res = await protocol.execute_macro_cycle({"state": "demo"})

    assert res.macro_cycle_id == "MC-0001"
    assert res.entropy_reduction >= 0.15 # Bootstrap value
    assert res.legal_coverage == 1.0
    assert "free_energy" in res.weights_updated

@pytest.mark.asyncio
async def test_meta_rl_tuner_update():
    tuner = MetaRLTuner()
    initial_weights = tuner.get_weights()

    # Simulate high reward
    tuner.update(reward=1.0, entropy_reduction=0.20)
    new_weights = tuner.get_weights()

    # Weights should have shifted
    assert initial_weights != new_weights
    assert sum(new_weights.values()) == pytest.approx(1.0)

@pytest.mark.asyncio
async def test_self_amendment_generation(macro_system):
    _, ueg, sb_core = macro_system
    generator = SelfAmendmentGenerator(sb_core, ueg)

    target_objectives = torch.ones(10) / 10.0
    proposal = await generator.generate_amendment_proposal({}, target_objectives, {"context": "optimization"})

    assert proposal["type"] == "constitutional_amendment"
    assert proposal["status"] == "AWAITING_MULTISIG"
    assert "mathematical_justification" in proposal
