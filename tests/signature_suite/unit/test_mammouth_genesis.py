import pytest
import asyncio
from agentic_core.orchestration.mammouth_genesis import MammouthDomainGenesis

@pytest.mark.asyncio
async def test_mammouth_genesis_v140():
    genesis = MammouthDomainGenesis()
    res = await genesis.generate_domain("Optimize medical diagnostic pipeline")
    assert res["generation_status"] == "certified_v140"
    assert "orchestrator" in res["swarm"]
    assert len(res["constitutional_rules"]) >= 2
