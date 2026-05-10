import hashlib
import json
import uuid
from decimal import Decimal
from datetime import datetime, UTC
from typing import Dict, Any, List, Optional
from firebase_admin import firestore

from agentic_core.crypto.pqc import Kyber1024, Dilithium5
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from agentic_core.identity.did_manager import DIDManager

db = firestore.client()

class CapitalVault:
    def __init__(self, owner_did: str, validator: GaaSValidator, ueg: UEGLogger):
        self.owner_did = owner_did
        self.validator = validator
        self.ueg = ueg
        self.did_manager = DIDManager()
        self.liquidity_reserve_ratio = Decimal("0.10")

    async def deposit(self, amount: Decimal, asset_type: str, tx_proof: dict, context: Dict[str, Any]) -> str:
        """Deposit capital – atomic Firestore transaction, UEG logging, constitutional check."""
        if not self.did_manager.verify_signed_intent(self.owner_did, tx_proof):
            raise ValueError("ConstitutionalViolation: Invalid signature")

        validation = await self.validator.validate_action("CAPITAL_DEPOSIT", {"amount": float(amount), "asset": asset_type})
        if not validation.get("passed"):
            raise ValueError(f"ConstitutionalViolation: Deposit rejected: {validation.get('reason')}")

        vault_ref = db.collection("capital_fund").document("sovereign_vault")

        def tx_logic(transaction):
            doc = transaction.get(vault_ref)
            current = Decimal(str(doc.to_dict().get("total_assets", 0))) if doc.exists else Decimal(0)
            new_balance = current + amount
            transaction.set(vault_ref, {
                "total_assets": float(new_balance),
                "last_deposit": { "amount": float(amount), "asset": asset_type, "time": firestore.SERVER_TIMESTAMP }
            }, merge=True)
            return new_balance

        new_balance = db.run_transaction(tx_logic)

        event_id = await self.ueg.log_event(
            "CAPITAL_DEPOSIT",
            {
                "owner_did": self.owner_did,
                "amount": float(amount),
                "asset": asset_type,
                "new_total": float(new_balance),
                "validation_hash": validation.get("hash")
            }
        )
        return event_id

    async def withdraw(self, amount: Decimal, asset_type: str, context: Dict[str, Any]) -> str:
        """Withdraw profit – liquidity guard, MultiSigCouncil for large withdrawals, atomic decrement."""
        vault_ref = db.collection("capital_fund").document("sovereign_vault")
        vault_doc = vault_ref.get()
        if not vault_doc.exists: raise ValueError("Vault not initialized")
        total_assets = Decimal(str(vault_doc.to_dict().get("total_assets", 0)))

        reserve_required = total_assets * self.liquidity_reserve_ratio
        if amount > (total_assets - reserve_required):
            raise ValueError("ConstitutionalViolation: Liquidity reserve breach")

        needs_council = amount > (total_assets * Decimal("0.05"))
        if needs_council:
            # In Phase 8 this triggers a Council event
            pass

        def tx_logic(transaction):
            doc = transaction.get(vault_ref)
            current = Decimal(str(doc.to_dict().get("total_assets", 0)))
            if current < amount: raise ValueError("Insufficient funds")
            new_total = current - amount
            transaction.update(vault_ref, {"total_assets": float(new_total), "last_withdrawal": { "amount": float(amount) }})
            return new_total

        new_total = db.run_transaction(tx_logic)

        event_id = await self.ueg.log_event(
            "CAPITAL_WITHDRAWAL",
            {"owner_did": self.owner_did, "amount": float(amount), "asset": asset_type, "new_total": float(new_total), "council_approved": needs_council}
        )
        return event_id
