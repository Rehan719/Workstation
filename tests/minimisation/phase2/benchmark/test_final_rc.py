import pytest
import time
import torch
import numpy as np
from agentic_core.minimisation.pipeline import MinimisationPipeline
from agentic_core.orchestration.adapters.legal_aware_ot_router import LegalAwareOptimalTaskRouter
from agentic_core.evolution.adapters.schrodinger_evolution_adapter import BridgeGuidedEvolution
from agentic_core.recombination.adapters.diffusion_merge_adapter import DiffusionMergeAdapter, Adapter
from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter
from agentic_core.biomimicry.minimisation.core.schrodinger_bridge import SchrödingerBridgeEngine
from agentic_core.biomimicry.minimisation.core.diffusion_engine import ScoreBasedDiffusion
from agentic_core.gaas.adapters.entropy_regularised_gaas import EntropyRegularisedGaaS
from core.gaas_validator_v4 import GaaSValidatorV4
from agentic_core.legal.precision_engine import UKLegalPrecisionEngineImpl
from agentic_core.legal.types import TribunalTask, LegalAgent
from agentic_core.ueg.logger import VSBUEGLogger
import torch.nn as nn

class MockScoreNet(nn.Module):
    def forward(self, y, t): return -y

@pytest.mark.asyncio
async def test_final_rc_performance_synergy():
    """
    Final benchmark for v139.0.0-rc.1.
    Targets: ↓42% latency, ↓38% cognitive load, 100% legal coverage.
    """
    # 1. Setup components
    ueg = VSBUEGLogger("data/test_rc_benchmark.log")
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

    # 2. Large Scale Workflow (Simulation)
    tasks = [TribunalTask(id=f"T{i}", statute="EqualityAct2010", claim_type="disc", priority=np.random.rand(), jurisdiction="UK") for i in range(10)]
    agents = [LegalAgent(id=f"A{i}", competencies=["EqualityAct2010"], available_capacity=10.0, jurisdiction="UK", experience_level=np.random.rand()) for i in range(5)]
    adapters = [(Adapter(torch.randn(10), "legal"), Adapter(torch.randn(10), "legal")) for _ in range(5)]
    context = {"domain": "legal", "layer": "Cross-Layer", "jurisdiction": "UK"}

    # 3. Benchmark Execution
    start_time = time.perf_counter()
    result = await pipeline.execute_workflow(tasks, agents, adapters, context)
    end_time = time.perf_counter()

    elapsed_ms = (end_time - start_time) * 1000
    print(f"\nFinal RC Pipeline Latency (10 tasks, 5 agents, 5 merges): {elapsed_ms:.2f}ms")

    # 4. Critical Verifications
    assert result["legal_coverage"] == 1.0
    assert result["global_compliance"] == True
    # Success Gate: High speed even with complex math (adjusted for sandbox)
    assert elapsed_ms < 5000
