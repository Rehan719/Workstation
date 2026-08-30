import logging
import datetime
import uuid
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from enum import Enum
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

logger = logging.getLogger(__name__)

class UserTier(Enum):
    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"

class TokenLedger:
    """
    ARTICLE 591-595: Tokenisation & Tiered Pricing Infrastructure.
    Manages Workstation Tokens (WST) and usage tracking with a robust, cryptographically signed database ledger.
    Includes Merkle-tree style hashing for transaction history and non-repudiation.
    """
    def __init__(self):
        self.ledgers: Dict[str, Dict[str, Any]] = {}
        self.transactions: List[Dict[str, Any]] = []
        self._default_allowances = {
            UserTier.FREE: 1000,
            UserTier.PRO: 50000,
            UserTier.ENTERPRISE: 1000000
        }
        self._snapshot_path = Path(os.getenv("DATA_DIR", "data")) / "token_ledger_snapshot.json"
        # Generate a system private key for signing transactions (simulating a central mint/validator)
        self._system_private_key = ed25519.Ed25519PrivateKey.generate()
        self._system_public_key = self._system_private_key.public_key()
        self.last_tx_hash = hashlib.sha256(b"GENESIS").hexdigest()
        self._load_snapshot()

    def _load_snapshot(self):
        """Restore balances/tiers from disk on boot."""
        try:
            if self._snapshot_path.exists():
                data = json.loads(self._snapshot_path.read_text())
                for uid, rec in data.get("ledgers", {}).items():
                    tier = UserTier(rec.get("tier", "FREE"))
                    self.ledgers[uid] = {
                        "balance": rec.get("balance", 0.0),
                        "tier": tier,
                        "total_consumed": rec.get("total_consumed", 0.0),
                        "last_refill": rec.get("last_refill", datetime.datetime.now().isoformat()),
                        "created_at": rec.get("created_at", datetime.datetime.now().isoformat()),
                        "public_key": rec.get("public_key", ""),
                    }
                self.last_tx_hash = data.get("last_tx_hash", self.last_tx_hash)
        except Exception as exc:
            logger.warning("TokenLedger: could not load snapshot: %s", exc)

    def _save_snapshot(self):
        """Persist balances/tiers to disk after any mutation."""
        try:
            self._snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            serializable = {
                uid: {
                    "balance": rec["balance"],
                    "tier": rec["tier"].value if isinstance(rec["tier"], UserTier) else rec["tier"],
                    "total_consumed": rec["total_consumed"],
                    "last_refill": rec["last_refill"],
                    "created_at": rec["created_at"],
                    "public_key": rec.get("public_key", ""),
                }
                for uid, rec in self.ledgers.items()
            }
            # §12 (W348) — ATOMIC + LOUD: the balance snapshot is money-shaped (virtual WST) —
            # a torn write or a silently-swallowed failure loses charges (audit: 17 confirmed
            # sales, ONE charge persisted). atomic_write_json + re-raise; callers holding the
            # purchase lock decide how to surface it.
            from agentic_core.config import atomic_write_json
            atomic_write_json(self._snapshot_path,
                              {"ledgers": serializable, "last_tx_hash": self.last_tx_hash})
        except Exception as exc:
            logger.error("TokenLedger: snapshot persistence FAILED: %s", exc)
            raise

    def initialize_user(self, user_id: str, tier: UserTier = UserTier.FREE, airdrop_bonus: float = 100.0):
        if user_id not in self.ledgers:
            # In a real system, each user would have their own keypair
            user_private_key = ed25519.Ed25519PrivateKey.generate()
            user_public_key = user_private_key.public_key()

            initial_balance = self._default_allowances[tier] + airdrop_bonus

            self.ledgers[user_id] = {
                "balance": initial_balance,
                "tier": tier,
                "total_consumed": 0,
                "last_refill": datetime.datetime.now().isoformat(),
                "created_at": datetime.datetime.now().isoformat(),
                "public_key": user_public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                ).hex()
            }
            logger.info(f"TokenLedger: Initialized user {user_id} with {tier.value} tier and cryptographic identity.")
            self._save_snapshot()

    def consume_tokens(self, user_id: str, amount: float, activity: str) -> bool:
        if user_id not in self.ledgers:
            self.initialize_user(user_id)

        ledger = self.ledgers[user_id]
        if ledger["balance"] < amount:
            logger.warning(f"TokenLedger: Insufficient balance for user {user_id}. Required: {amount}, Available: {ledger['balance']}")
            return False

        ledger["balance"] -= amount
        ledger["total_consumed"] += amount

        tx_data = {
            "user_id": user_id,
            "amount": -amount,
            "activity": activity,
            "timestamp": datetime.datetime.now().isoformat(),
            "prev_hash": self.last_tx_hash
        }

        # Sign the transaction
        tx_json = json.dumps(tx_data, sort_keys=True).encode()
        signature = self._system_private_key.sign(tx_json)

        # Calculate new hash (Merkle-link)
        new_hash = hashlib.sha256(tx_json + signature).hexdigest()
        self.last_tx_hash = new_hash

        transaction = {
            "tx_id": str(uuid.uuid4()),
            "data": tx_data,
            "signature": signature.hex(),
            "hash": new_hash
        }

        self.transactions.append(transaction)
        logger.info(f"TokenLedger: User {user_id} consumed {amount} WST. TX Hash: {new_hash[:10]}...")
        self._save_snapshot()
        return True

    def mint(self, to_user: str, amount: float, reason: str = "Admin Minting") -> bool:
        """ARTICLE 591: Administrative minting of tokens."""
        if to_user not in self.ledgers:
            self.initialize_user(to_user)

        self.ledgers[to_user]["balance"] += amount

        tx_data = {
            "to": to_user,
            "amount": amount,
            "activity": reason,
            "timestamp": datetime.datetime.now().isoformat(),
            "prev_hash": self.last_tx_hash,
            "type": "mint"
        }

        tx_json = json.dumps(tx_data, sort_keys=True).encode()
        signature = self._system_private_key.sign(tx_json)
        new_hash = hashlib.sha256(tx_json + signature).hexdigest()
        self.last_tx_hash = new_hash

        self.transactions.append({
            "tx_id": str(uuid.uuid4()),
            "data": tx_data,
            "signature": signature.hex(),
            "hash": new_hash
        })
        logger.info(f"TokenLedger: Minted {amount} WST for {to_user}. Hash: {new_hash[:10]}...")
        self._save_snapshot()
        return True

    async def deduct_tokens(self, user_id: str, amount: float, reason: str) -> bool:
        """Alias for consume_tokens to match ReasoningGate expectations."""
        return self.consume_tokens(user_id, amount, reason)

    async def credit_tokens(self, user_id: str, amount: float, reason: str):
        if user_id not in self.ledgers:
            self.initialize_user(user_id)

        ledger = self.ledgers[user_id]
        ledger["balance"] += amount

        tx_data = {
            "user_id": user_id,
            "amount": amount,
            "activity": reason,
            "timestamp": datetime.datetime.now().isoformat(),
            "prev_hash": self.last_tx_hash
        }

        tx_json = json.dumps(tx_data, sort_keys=True).encode()
        signature = self._system_private_key.sign(tx_json)
        new_hash = hashlib.sha256(tx_json + signature).hexdigest()
        self.last_tx_hash = new_hash

        self.transactions.append({
            "tx_id": str(uuid.uuid4()),
            "data": tx_data,
            "signature": signature.hex(),
            "hash": new_hash
        })
        self._save_snapshot()

    def transfer(self, from_user: str, to_user: str, amount: float, reason: str = "P2P Transfer") -> bool:
        """ARTICLE 626: Secure token transfer between users."""
        if from_user not in self.ledgers or to_user not in self.ledgers:
            return False

        if self.ledgers[from_user]["balance"] < amount:
            return False

        self.ledgers[from_user]["balance"] -= amount
        self.ledgers[to_user]["balance"] += amount

        tx_data = {
            "from": from_user,
            "to": to_user,
            "amount": amount,
            "activity": reason,
            "timestamp": datetime.datetime.now().isoformat(),
            "prev_hash": self.last_tx_hash
        }

        tx_json = json.dumps(tx_data, sort_keys=True).encode()
        signature = self._system_private_key.sign(tx_json)
        new_hash = hashlib.sha256(tx_json + signature).hexdigest()
        self.last_tx_hash = new_hash

        self.transactions.append({
            "tx_id": str(uuid.uuid4()),
            "data": tx_data,
            "signature": signature.hex(),
            "hash": new_hash
        })
        self._save_snapshot()
        return True

    def get_ledger_report(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.ledgers:
            return {"error": "User not found"}

        ledger = self.ledgers[user_id]
        # Transactions where user is sender or receiver
        user_txs = [
            tx for tx in self.transactions
            if tx["data"].get("user_id") == user_id or tx["data"].get("from") == user_id or tx["data"].get("to") == user_id
        ]

        return {
            "user_id": user_id,
            "balance": ledger["balance"],
            "tier": ledger["tier"].value,
            "total_consumed": ledger["total_consumed"],
            "public_key": ledger["public_key"],
            "transaction_count": len(user_txs),
            "recent_transactions": user_txs[-10:],
            "system_integrity_hash": self.last_tx_hash
        }

    def verify_transaction(self, tx: Dict[str, Any]) -> bool:
        """Verify the signature of a transaction."""
        try:
            tx_json = json.dumps(tx["data"], sort_keys=True).encode()
            signature = bytes.fromhex(tx["signature"])
            self._system_public_key.verify(signature, tx_json)
            return True
        except Exception:
            return False
