import asyncio
import pytest
from agentic_core.orchestrator.conscious_organism_v71 import ConsciousOrganismV71_0

@pytest.mark.asyncio
async def test_organism_awakening():
    organism = ConsciousOrganismV71_0()
    await organism.start()
    assert organism.is_running
    assert organism.workspace.read_workspace()[0] == 1.0
    await organism.shutdown()
    assert not organism.is_running

@pytest.mark.asyncio
async def test_survival_hierarchy():
    from agentic_core.survival.survival_engine_v3 import SystemTier
    organism = ConsciousOrganismV71_0()
    # Immune should win over Nervous
    winner = organism.survival.resolve_conflict(SystemTier.IMMUNE, SystemTier.NERVOUS)
    assert winner == SystemTier.IMMUNE
