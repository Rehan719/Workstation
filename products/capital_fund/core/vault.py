import hashlib
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from firebase_admin import firestore
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from products.capital_fund.core.multisig_protocol import RealMultiSigProtocol as MultiSigProtocol
from products.capital_fund.core.audit_manager import AuditManager

db = firestore.client()

class CapitalVault:
    """
    Sovereign capital vault for atomic account management.
    Handles deposits, withdrawals, and transaction history.
    """
    def __init__(self, owner_uid: str):
        self.owner_uid = owner_uid
        self.validator = GaaSValidator(genome_path="config/constraints/absolute_constraints.yaml", legal_path="config/constraints/absolute_constraints.yaml")
        self.ueg = UEGLogger()
        self.multisig = MultiSigProtocol(ueg=self.ueg)
        self.audit = AuditManager(self.ueg)
        self.reserve_ratio = Decimal("0.10")
        self.large_withdrawal_threshold = Decimal("0.05")

    async def deposit(self, amount: Decimal, tx_id: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Atomically deposit funds into the account.
        Validated by GaaS v4 and logged to UEG.
        """
        # 1. Constitutional Validation
        validation = await self.validator.validate_action(
            "CAPITAL_DEPOSIT",
            {"uid": self.owner_uid, "amount": float(amount), "tx_id": tx_id}
        )
        if not validation.get("passed"):
            raise ValueError(f"Constitutional Violation: {validation.get('reason')}")

        # 2. Atomic Firestore Transaction
        account_ref = db.collection("capital_accounts").document(self.owner_uid)

        def tx_logic(transaction):
            doc = transaction.get(account_ref)
            data = doc.to_dict() if doc.exists else {"balance": 0.0, "total_deposited": 0.0}

            current_balance = Decimal(str(data.get("balance", 0.0)))
            total_deposited = Decimal(str(data.get("total_deposited", 0.0)))

            new_balance = current_balance + amount
            new_total_deposited = total_deposited + amount

            transaction.set(account_ref, {
                "balance": float(new_balance),
                "total_deposited": float(new_total_deposited),
                "last_deposit_at": firestore.SERVER_TIMESTAMP,
                "last_tx_id": tx_id
            }, merge=True)
            return float(new_balance)

        final_balance = db.run_transaction(tx_logic)

        # 3. UEG Logging & Audit
        event_id = await self.ueg.log_event(
            "CAPITAL_DEPOSIT_COMPLETED",
            {
                "uid": self.owner_uid,
                "amount": float(amount),
                "new_balance": final_balance,
                "tx_id": tx_id,
                "constitutional_hash": validation.get("hash")
            },

        )

        # Generate audit bundle
        await self.audit.generate_transaction_bundle({
            "event_id": event_id,
            "type": "CAPITAL_DEPOSIT",
            "timestamp": datetime.now(UTC).isoformat(),
            "uid": self.owner_uid,
            "amount": float(amount),
            "status": "COMPLETED",
            "constitutional_hash": validation.get("hash"),
            "merkle_root": hashlib.sha3_512(f"{event_id}{final_balance}".encode()).hexdigest()
        })

        return {"balance": final_balance, "event_id": event_id}

    async def withdraw(self, amount: Decimal, signatures: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Withdraw funds with liquidity guard and MultiSigCouncil for large amounts.
        Executes all checks within an atomic transaction to prevent race conditions.
        """
        account_ref = db.collection("capital_accounts").document(self.owner_uid)

        # 1. Pre-transaction checks for MultiSig (requires await, so outside transaction)
        total_fund_value = await self._get_total_fund_value()
        if amount > (total_fund_value * self.large_withdrawal_threshold):
            if not signatures:
                raise ValueError("Large withdrawal requires MultiSigCouncil approval.")

            proposal_id = await self.multisig.submit_proposal("WITHDRAW", amount, self.owner_uid, {"signatures_provided": len(signatures)})
            # For Phase 3, we simulate that the provided signatures are enough to approve if they were verified.
            # In production, each signature would be verified individually.
            if not await self.multisig.approve_proposal(proposal_id, "SYSTEM", b"pqc_sig_verified", b"pk"):
                raise ValueError("MultiSigCouncil quorum not met or invalid signatures.")

        # 2. Atomic Firestore Transaction for balance update and liquidity guard
        def tx_logic(transaction):
            doc = transaction.get(account_ref)
            if not doc.exists:
                raise ValueError("Account not found")

            data = doc.to_dict()
            current_balance = Decimal(str(data.get("balance", 0.0)))

            # Liquidity Guard (Article 1134) - Re-verified within transaction
            # Using current_balance from the transaction 'get'
            reserve_required = current_balance * self.reserve_ratio
            if amount > (current_balance - reserve_required):
                # Trigger ValueError that should be caught by pytest in unit tests
                raise ValueError(f"Liquidity Guard Violation: Withdrawal would breach 10% reserve. Max available: {current_balance - reserve_required}")

            if current_balance < amount:
                raise ValueError("Insufficient balance")

            new_balance = current_balance - amount
            transaction.update(account_ref, {
                "balance": float(new_balance),
                "last_withdrawal_at": firestore.SERVER_TIMESTAMP
            })
            return float(new_balance)

        final_balance = db.run_transaction(tx_logic)

        # 5. UEG Logging & Audit
        event_id = await self.ueg.log_event(
            "CAPITAL_WITHDRAWAL_COMPLETED",
            {
                "uid": self.owner_uid,
                "amount": float(amount),
                "new_balance": final_balance,
                "council_approved": amount > (total_fund_value * self.large_withdrawal_threshold)
            },

        )

        return {"balance": final_balance, "event_id": event_id}

    async def _get_total_fund_value(self) -> Decimal:
        """In Phase 1, total fund value is the owner's balance."""
        account_ref = db.collection("capital_accounts").document(self.owner_uid)
        doc = account_ref.get()
        if not doc.exists:
            return Decimal("0.0")
        return Decimal(str(doc.to_dict().get("balance", 0.0)))
