import pytest
import asyncio
import torch
from agentic_core.change_control.reconfigulator import Reconfigulator
from agentic_core.change_control.regulator import Regulator
from agentic_core.defense.immune_system import ImmuneDefense
from agentic_core.mjm.hyperdimensional import MJMv4OmniLearner

@pytest.mark.asyncio
async def test_reconfigulator_replication():
    rc = Reconfigulator()
    genome = "{\"identity\": \"AgentOpus\", \"layers\": 12}"
    ghash = await rc.replicate_genome(genome)
    assert ghash is not None
    assert await rc.translate_to_runtime(ghash) is True

@pytest.mark.asyncio
async def test_regulator_repair():
    reg = Regulator()
    corrupted = {"cpu_limit": None, "memory": 1024}
    repaired = await reg.repair_corrupted_state(corrupted, repair_tier="HDR")
    assert repaired["cpu_limit"] == "recovered_from_template"

@pytest.mark.asyncio
async def test_immune_defense():
    imm = ImmuneDefense()
    detector = await imm.vdj_recombine(["V1", "D2", "J3"])
    assert detector is not None
    # Threat simulation
    threat = {"id": "rogue_1", "action": "exfiltrate"}
    # Verify scan_agent_activity (the correct method name)
    assert await imm.scan_agent_activity("agent_0", threat) is False # No matches yet

@pytest.mark.asyncio
async def test_hd_omni_learner():
    mjm = MJMv4OmniLearner(dimension=100)
    source = torch.randn(100)
    transferred = await mjm.project_to_domain(source, "biotech")
    assert transferred.shape == (100,)
