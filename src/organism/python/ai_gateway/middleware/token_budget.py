import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TokenBudgetManager:
    """
    Tracks per-model token usage and enforces free-tier limits.
    """
    def __init__(self, limits: Dict[str, Dict[str, Any]]):
        self.limits = limits
        # In production, this would be backed by Redis or the SovereignAuditLog
        self.usage: Dict[str, int] = {}

    def check_and_reserve(self, model: str, estimated_tokens: int) -> bool:
        """
        Returns True if the request can proceed within budget, False otherwise.
        """
        limit_info = self.limits.get(model, {})
        max_tokens = limit_info.get("monthly_tokens", float("inf"))

        current_usage = self.usage.get(model, 0)

        if current_usage + estimated_tokens > max_tokens:
            logger.warning(f"TokenBudget: Quota exceeded for {model} ({current_usage}/{max_tokens})")
            return False

        return True

    def update_usage(self, model: str, actual_tokens: int):
        """Updates the internal usage counter."""
        self.usage[model] = self.usage.get(model, 0) + actual_tokens
        logger.info(f"TokenBudget: {model} usage updated to {self.usage[model]}")

    def get_status(self, model: str) -> Dict[str, Any]:
        """Returns quota status for the dashboard."""
        limit_info = self.limits.get(model, {})
        max_tokens = limit_info.get("monthly_tokens", 0)
        used = self.usage.get(model, 0)

        return {
            "model": model,
            "used": used,
            "limit": max_tokens,
            "remaining": max(0, max_tokens - used),
            "health": "healthy" if used < max_tokens * 0.8 else "warning"
        }
