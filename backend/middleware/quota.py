from fastapi import Depends, HTTPException
from ..usage.meter import async_check_quota
from ..usage.context_engine import ContextEngine

# This is a placeholder for real auth; assuming a function get_current_user_id exists
async def get_current_user_id():
    return "test_user_id"

def require_quota(operation: str):
    """
    FastAPI dependency to enforce atomic quotas with geospheric context.
    """
    async def dependency(uid: str = Depends(get_current_user_id)):
        # 1. Atomic Quota Check
        base_allowed = await async_check_quota(uid, operation)

        # 2. Geospheric/Biomimetic Context Adjustment (Extension Point)
        final_allowed = await ContextEngine.evaluate_context_rules(uid, operation, base_allowed)

        if not final_allowed:
            raise HTTPException(
                status_code=429,
                detail=f"Quota exceeded for {operation}. Upgrade at /pricing to continue."
            )
        return True
    return dependency
