from fastapi import Depends, HTTPException
from ..usage.meter import async_check_quota
from ..usage.context_engine import ContextEngine
# from .auth import get_current_user_id # Real implementation would import this

def require_quota(operation: str):
    async def dependency(uid: str = "mock_uid"): # Depends(get_current_user_id)
        base_allowed = await async_check_quota(uid, operation)
        final_allowed = await ContextEngine.evaluate_context_rules(uid, operation, base_allowed)
        if not final_allowed:
            raise HTTPException(429, f"Quota exceeded for {operation}. Upgrade at /pricing")
        return True
    return dependency
