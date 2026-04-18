import pytest
from agentic_core.mesh.negotiation.treaty_negotiation import TreatyNegotiator
@pytest.mark.asyncio
async def test_neg():
    n = TreatyNegotiator("A")
    res = await n.negotiate([{"id": "i1", "profile": [0,1]}], [{"id": "p1", "profile": [0,1]}])
    assert res["proposer"] == "A"
