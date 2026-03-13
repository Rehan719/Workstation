import logging
import datetime
import uuid
from typing import Dict, Any, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class UserTier(Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"

class TokenLedger:
    """
    ARTICLE 591-595: Tokenisation & Tiered Pricing Infrastructure.
    Manages Workstation Tokens (WST) and usage tracking.
    """
    def __init__(self):
        # In a production environment, this would be a database table
        self.ledgers: Dict[str, Dict[str, Any]] = {}
        self.transactions: List[Dict[str, Any]] = []
        self._default_allowances = {
            UserTier.FREE: 1000,
            UserTier.PRO: 50000,
            UserTier.ENTERPRISE: 1000000
        }

    def initialize_user(self, user_id: str, tier: UserTier = UserTier.FREE):
        if user_id not in self.ledgers:
            self.ledgers[user_id] = {
                "balance": self._default_allowances[tier],
                "tier": tier,
                "total_consumed": 0,
                "last_refill": datetime.datetime.now().isoformat()
            }
            logger.info(f"TokenLedger: Initialized user {user_id} with {tier.value} tier.")

    def consume_tokens(self, user_id: str, amount: int, activity: str) -> bool:
        """Consumes tokens from the user's ledger."""
        if user_id not in self.ledgers:
            self.initialize_user(user_id)

        ledger = self.ledgers[user_id]
        if ledger["balance"] < amount:
            logger.warning(f"TokenLedger: Insufficient balance for user {user_id}. Required: {amount}, Available: {ledger['balance']}")
            return False

        ledger["balance"] -= amount
        ledger["total_consumed"] += amount

        transaction = {
            "tx_id": str(uuid.uuid4()),
            "user_id": user_id,
            "amount": amount,
            "activity": activity,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.transactions.append(transaction)
        logger.info(f"TokenLedger: User {user_id} consumed {amount} WST for {activity}.")
        return True

    def get_balance(self, user_id: str) -> int:
        return self.ledgers.get(user_id, {}).get("balance", 0)

    def get_tier(self, user_id: str) -> UserTier:
        return self.ledgers.get(user_id, {}).get("tier", UserTier.FREE)

    def add_tokens(self, user_id: str, amount: int):
        if user_id in self.ledgers:
            self.ledgers[user_id]["balance"] += amount
            logger.info(f"TokenLedger: Added {amount} WST to user {user_id}.")

    def upgrade_tier(self, user_id: str, new_tier: UserTier):
        if user_id in self.ledgers:
            self.ledgers[user_id]["tier"] = new_tier
            # Refill to new tier default
            self.ledgers[user_id]["balance"] = self._default_allowances[new_tier]
            logger.info(f"TokenLedger: User {user_id} upgraded to {new_tier.value}.")
