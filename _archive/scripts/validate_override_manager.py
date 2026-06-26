import asyncio
from agentic_core.governance.override_manager import OverrideManager
async def main():
    mgr = OverrideManager()
    pay = await mgr.request_override("a1", {"v": "t"})
    sig = mgr.sign_override(pay)
    assert await mgr.apply_override("a1", sig, pay) is True
    print("OverrideManager cryptographic audit: PASSED")
if __name__ == "__main__":
    asyncio.run(main())
