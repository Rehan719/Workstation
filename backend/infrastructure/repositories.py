from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

class UsageRepository(ABC):
    @abstractmethod
    async def get_subscription(self, uid: str) -> Optional[Dict[str, Any]]:
        """Retrieve subscription data for user."""
        return None

    @abstractmethod
    async def increment_quota(self, uid: str, operation: str, limit: int) -> Tuple[bool, int]:
        """Atomically increment quota and return (allowed, new_count)."""
        return False, 0

class BillingRepository(ABC):
    @abstractmethod
    async def get_subscription(self, uid: str) -> Optional[Dict[str, Any]]:
        """Retrieve subscription data for user."""
        return None

    @abstractmethod
    async def activate_subscription(self, uid: str, data: Dict[str, Any]) -> None:
        """Create or update subscription record."""
        return

    @abstractmethod
    async def cancel_subscription(self, subscription_id: str) -> None:
        """Mark subscription as canceled."""
        return

    @abstractmethod
    async def register_webhook_event(self, event_id: str) -> bool:
        """Returns True if successfully registered, False if already exists."""
        return False
