import pytest
import asyncio
from agentic_core.jules_omega_organism_v138 import JulesOmegaOrganismV138

@pytest.mark.asyncio
async def test_macro_cycle():
    organism = JulesOmegaOrganismV138()
    await organism.initialize()
    await organism.run_macro_cycle()
    assert organism.macro_cycle_count == 1
    assert organism.is_running is True
    await organism.shutdown()
