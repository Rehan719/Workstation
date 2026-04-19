import pytest
from agentic_core.mesh.ledger.treaty_ledger import TreatyLedger
@pytest.mark.asyncio
async def test_ledger():
    l = TreatyLedger("A")
    t = await l.propose_treaty("B", {"k": "v"})
    assert t.status == "proposed"
    await l.sign_treaty(t.id, "sA")
    assert await l.sign_treaty(t.id, "sB") is True
