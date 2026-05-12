from fastapi import Depends, HTTPException
from backend.usage.usage_meter import async_check_quota, evaluate_context_rules
# from .auth import get_current_user_id # Mock or use existing

def require_quota(operation: str):
    async def dependency(uid: str = "mock_uid"): # Depends(get_current_user_id)
        base_allowed = await async_check_quota(uid, operation)
        if not base_allowed:
            raise HTTPException(status_code=429, detail=f"Quota exceeded for {operation}. Upgrade at /pricing")
        # Context engine can return adjusted quota or recommendations (not hard blocks)
        ctx = await evaluate_context_rules(uid)
        return True
    return dependency
