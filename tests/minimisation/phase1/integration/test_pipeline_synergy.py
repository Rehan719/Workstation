import pytest
import torch
from agentic_core.minimisation.pipeline import MinimisationPipeline
from agentic_core.orchestration.adapters.legal_aware_ot_router import LegalAwareOptimalTaskRouter
from agentic_core.evolution.adapters.schrodinger_evolution_adapter import BridgeGuidedEvolution
from agentic_core.recombination.adapters.diffusion_merge_adapter import DiffusionMergeAdapter, Adapter
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.biomimicry.minimisation.core.diffusion_engine import ScoreBasedDiffusion
from agentic_core.gaas.adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from agentic_core.organism.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.ueg.logger import VSBUEGLogger
import torch.nn as nn

class MockScoreNet(nn.Module):
    def forward(self, y, t): return -y

@pytest.mark.asyncio
async def test_minimisation_pipeline_synergy():
    # 1. Setup components
    ueg = VSBUEGLogger("data/test_pipeline.log")
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

    # 2. Mock Data
    tasks = [TribunalTask(id="T1", statute="EqualityAct2010", claim_type="disc", priority=0.8, jurisdiction="UK")]
    agents = [LegalAgent(id="A1", competencies=["EqualityAct2010"], available_capacity=1.0, jurisdiction="UK", experience_level=0.8)]
    adapters = [(Adapter(torch.ones(10), "legal"), Adapter(torch.ones(10)*-1, "legal"))]
    context = {"domain": "legal", "layer": "Cross-Layer", "jurisdiction": "UK"}

    # 3. Execute
    result = await pipeline.execute_workflow(tasks, agents, adapters, context)

    # 4. Assertions
    assert result["assignments"]["T1"] == "A1"
    assert result["agent_parameter_updates"] == 1
    assert result["merged_modules"] == 1
    assert result["legal_coverage"] == 1.0
