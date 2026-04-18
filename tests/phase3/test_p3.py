import pytest
from agentic_core.adapters.domain.climate_adapter import ClimateDomainAdapter
@pytest.mark.asyncio
async def test_p3():
    assert await ClimateDomainAdapter().optimise_carbon_trajectory([100], 0.1) == [90]
