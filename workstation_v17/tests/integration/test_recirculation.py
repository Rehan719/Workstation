import pytest
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17

@pytest.mark.asyncio
async def test_full_recirculation_cycle():
    organism = JulesOmegaOrganismV17(config_path="config/constitutional_genome_v17.yaml")
    await organism.initialize()

    input_data = {"text": "v17.0 test run"}
    result = await organism.run_recirculation_cycle(input_data)

    assert result["status"] == "EVOLVED"
    assert "gain" in result
    assert "new_paradigm" in result

    await organism.shutdown()
