import pytest
import asyncio
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17

@pytest.mark.asyncio
async def test_macro_cycle():
    organism = JulesOmegaOrganismV17()
    await organism.initialize()
    await organism.run_macro_cycle()
    assert organism.cycle_id == 1
    assert organism.is_running is True
    await organism.shutdown()
