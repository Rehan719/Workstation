"""
MultiTenantInvestorManager – enables external investors to join the fund with pro‑rata rights,
sub‑ledger accounting, KYC/AML via GaaS v4, and constitutional profit sharing.
"""
import uuid
from decimal import Decimal
from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
from firebase_admin import firestore
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from products.capital_fund.core.vault import CapitalVault

db = firestore.client()

class InvestorAccount:
    """Represents a sub-ledger account for an external investor."""
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("investor_id")
        self.uid = data.get("uid")
        self.balance = Decimal(str(data.get("balance", "0.0")))
        self.initial_deposit = Decimal(str(data.get("initial_deposit", "0.0")))
        self.profit_sharing_rate = Decimal(str(data.get("profit_sharing_rate", "0.15"))) # Default 15% to fund
        self.status = data.get("status", "pending")
        self.onboarded_at = data.get("onboarded_at")

class MultiTenantInvestorManager:
    """
    Manages onboarding, sub-ledgers, and profit distribution for multiple investors.
    Enforces owner sovereignty (Article 1135).
    """
    def __init__(self, owner_uid: str):
        self.owner_uid = owner_uid
        self.validator = GaaSValidator(
            genome_path="config/constraints/absolute_constraints.yaml",
            legal_path="config/constraints/absolute_constraints.yaml"
        )
        self.ueg = UEGLogger()
        self.vault = CapitalVault(owner_uid)

    async def onboard_investor(
        self,
        investor_uid: str,
        initial_deposit: Decimal,
        kyc_payload: Dict[str, Any]
    ) -> InvestorAccount:
        """
        Onboard a new investor after GaaS v4 validation.
        Creates an atomic sub-ledger record.
        """
        # 1. Constitutional & KYC Validation
        validation = await self.validator.validate_intent(
            {"type": "INVESTOR_ONBOARDING", "amount": float(initial_deposit), "investor_uid": investor_uid},
            {"domain": "capital", "kyc_data": kyc_payload}
        )
        if not validation.get("passed"):
            await self.ueg.log_event("INVESTOR_REJECTED", {"uid": investor_uid, "reason": validation.get("reason", "Constitutional Violation")})
            raise ValueError(f"Constitutional Violation: {validation.get('reason', 'KYC/AML Failed')}")

        # 2. Atomic Account Creation
        investor_id = f"inv_{uuid.uuid4().hex[:8]}"
        investor_ref = db.collection("capital_investors").document(investor_uid)

        def tx_logic(transaction):
            doc = transaction.get(investor_ref)
            if doc.exists:
                raise ValueError("Investor already onboarded")

            investor_data = {
                "investor_id": investor_id,
                "uid": investor_uid,
                "balance": float(initial_deposit),
                "initial_deposit": float(initial_deposit),
                "profit_sharing_rate": 0.15,
                "status": "active",
                "onboarded_at": firestore.SERVER_TIMESTAMP,
                "last_updated": firestore.SERVER_TIMESTAMP
            }
            transaction.set(investor_ref, investor_data)
            return investor_data

        data = db.run_transaction(tx_logic)

        # 3. Log to UEG
        await self.ueg.log_event(
            "INVESTOR_ONBOARDED",
            {
                "investor_id": investor_id,
                "uid": investor_uid,
                "amount": float(initial_deposit),
                "merkle_root": validation.get("merkle_root")
            }
        )

        return InvestorAccount(data)

    async def get_investor_account(self, investor_uid: str) -> Optional[InvestorAccount]:
        """Retrieve investor sub-ledger data."""
        doc = db.collection("capital_investors").document(investor_uid).get()
        if not doc.exists:
            return None
        return InvestorAccount(doc.to_dict())

    async def calculate_pro_rata_share(self, investor_uid: str) -> Decimal:
        """
        Calculate investor's share of total AUM.
        Owner sovereignty ensured as this is read-only.
        """
        account = await self.get_investor_account(investor_uid)
        if not account:
            return Decimal("0.0")

        total_aum = await self.vault._get_total_fund_value()
        if total_aum == 0:
            return Decimal("0.0")

        return account.balance / total_aum

    async def distribute_profit(self, total_profit: Decimal) -> Dict[str, Decimal]:
        """
        Distribute realised profit across all active investors pro-rata.
        The fund (owner) takes their sharing rate from each investor's profit.
        Uses WriteBatch for atomic, efficient updates across multiple investors.
        """
        investors_ref = db.collection("capital_investors").where("status", "==", "active")
        docs = list(investors_ref.stream())

        total_aum = await self.vault._get_total_fund_value()
        distributions = {}

        # Firestore batch supports up to 500 operations. Process in chunks.
        batch = db.batch()
        count = 0

        for doc in docs:
            data = doc.to_dict()
            inv_uid = data["uid"]
            inv_balance = Decimal(str(data["balance"]))
            sharing_rate = Decimal(str(data.get("profit_sharing_rate", "0.15")))

            share = inv_balance / total_aum
            gross_profit = total_profit * share
            fee = gross_profit * sharing_rate
            net_profit = gross_profit - fee

            inv_ref = db.collection("capital_investors").document(inv_uid)
            batch.update(inv_ref, {
                "balance": firestore.Increment(float(net_profit)),
                "total_profit_earned": firestore.Increment(float(net_profit))
            })

            distributions[inv_uid] = net_profit
            count += 1

            # Commit and start new batch if limit reached
            if count % 500 == 0:
                batch.commit()
                batch = db.batch()

        if count % 500 != 0:
            batch.commit()

        await self.ueg.log_event("PROFIT_DISTRIBUTION_COMPLETED", {
            "total_profit": float(total_profit),
            "investor_count": len(distributions)
        })

        return distributions
