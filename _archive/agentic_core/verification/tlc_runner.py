from typing import Any
class TLCRuntimeChecker:
    async def verify_amendment(self, amendment: Any) -> bool:
        if "VIOLATION" in str(amendment): return False
        return True
