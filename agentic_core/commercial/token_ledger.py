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
    Manages Workstation Tokens (WST) and usage tracking with automated replenishment logic.
    """
    def __init__(self):
        self.ledgers: Dict[str, Dict[str, Any]] = {}
        self.transactions: List[Dict[str, Any]] = []
        self._default_allowances = {
            UserTier.FREE: 1000,
            UserTier.PRO: 50000,
            UserTier.ENTERPRISE: 1000000
        }
        self._hourly_rates = {
            UserTier.FREE: 1.4, # Burn rate simulation
            UserTier.PRO: 124.0,
            UserTier.ENTERPRISE: 850.0
        }

    def initialize_user(self, user_id: str, tier: UserTier = UserTier.FREE):
        if user_id not in self.ledgers:
            self.ledgers[user_id] = {
                "balance": self._default_allowances[tier],
                "tier": tier,
                "total_consumed": 0,
                "last_refill": datetime.datetime.now().isoformat(),
                "created_at": datetime.datetime.now().isoformat()
            }
            logger.info(f"TokenLedger: Initialized user {user_id} with {tier.value} tier.")

    def consume_tokens(self, user_id: str, amount: int, activity: str) -> bool:
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

    def simulate_hourly_refill(self, user_id: str):
        """Simulates automated monthly/periodic replenishment (Article 591)."""
        if user_id in self.ledgers:
            ledger = self.ledgers[user_id]
            # Simple simulation: partial refill to maintain balance
            refill = self._default_allowances[ledger["tier"]] * 0.05
            ledger["balance"] += refill
            ledger["last_refill"] = datetime.datetime.now().isoformat()
            logger.info(f"TokenLedger: Simulated refill of {refill} WST for user {user_id}.")

    def get_ledger_report(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.ledgers:
            return {"error": "User not found"}

        ledger = self.ledgers[user_id]
        return {
            "balance": ledger["balance"],
            "tier": ledger["tier"].value,
            "burn_rate": self._hourly_rates[ledger["tier"]],
            "total_consumed": ledger["total_consumed"],
            "last_refill": ledger["last_refill"]
        }
