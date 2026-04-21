import pytest
import torch
from agentic_core.mjm.v5.omni_learner_v5 import MJMv5OmniLearner
from agentic_core.biomimicry.minimisation.v2.oam_qkd_v2 import OAMQKDSurrogateV2
from agentic_core.biomimicry.minimisation.v2.viral_mechanics import ViralMechanicsEngine

@pytest.mark.asyncio
async def test_mjm_v5_hd_transfer():
    learner = MJMv5OmniLearner(dimension=12000)
    source = torch.randn(12000)
    res = await learner.project_to_domain_v5(source, "quantum_biology")
    assert res.shape == (12000,)

@pytest.mark.asyncio
async def test_qkd_v2_fidelity():
    qkd = OAMQKDSurrogateV2(num_states=64)
    res = await qkd.generate_key_v2({})
    assert res["qber"] < 0.045
    assert res["key_rate"] > 6.0

@pytest.mark.asyncio
async def test_viral_pmf():
    viral = ViralMechanicsEngine()
    res = await viral.analyze_pmf("Workstation_v139_1", {})
    assert res["viral_coefficient"] > 1.2
