import pytest, json
from agentic_core.governance.override_manager import OverrideManager
@pytest.mark.asyncio
async def test_override_flow():
    mgr = OverrideManager(None)
    pay = await mgr.request_override("a1", {"v": "t"})
    sig = mgr.sign_override(pay)
    assert await mgr.apply_override("a1", sig, pay) is True
