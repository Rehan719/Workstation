import pytest
import asyncio
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17

@pytest.mark.asyncio
async def test_full_cycle():
    organism = JulesOmegaOrganismV17()
    await organism.initialize()
    await organism.run_cycle()
    assert organism.is_running is True
    await organism.shutdown()
    assert organism.is_running is False

@pytest.mark.asyncio
async def test_vsb_ueg_integrity():
    organism = JulesOmegaOrganismV17()
    await organism.initialize()
    await organism.run_cycle()
    assert organism.ueg.verify_chain() is True
    await organism.shutdown()
