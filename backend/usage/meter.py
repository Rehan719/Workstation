from datetime import datetime
from typing import Dict, Any, Optional
from ..infrastructure.repositories import UsageRepository

QUOTAS = {"free": {"executions": 50, "projects": 1},
          "pro": {"executions": 2000, "projects": 10},
          "team": {"executions": 10000, "projects": 999}}

async def _get_effective_plan(uid: str, repo: UsageRepository) -> str:
    """Determine user's effective plan considering trial status."""
    sub_data = await repo.get_subscription(uid)
    if not sub_data:
        return "free"
    if sub_data.get("status") != "active":
        return "free"
    trial_end = sub_data.get("trial_end")
    if trial_end and isinstance(trial_end, datetime) and datetime.utcnow() < trial_end:
        return "pro"
    return sub_data.get("plan", "free").lower()

async def check_quota(uid: str, operation: str, repo: UsageRepository, twin_prediction: Optional[Dict[str, Any]] = None) -> bool:
    """
    Atomic quota check using repository abstraction.
    Sovereignty-compliant and race-condition free.
    """
    plan = await _get_effective_plan(uid, repo)
    limit = QUOTAS.get(plan, {}).get(operation, 0)

    # Predictive Adjustment
    effective_limit = limit
    if twin_prediction and twin_prediction.get("likelihood_to_upgrade", 0) > 0.8:
        effective_limit = int(limit * 1.1)

    allowed, new_count = await repo.increment_quota(uid, operation, effective_limit)

    # UEG logging occurs OUTSIDE the transaction logic (handled by orchestrator or caller)
    return allowed

async def async_check_quota(uid: str, operation: str, repo: UsageRepository, twin_prediction: Optional[Dict[str, Any]] = None) -> bool:
    return await check_quota(uid, operation, repo, twin_prediction)
