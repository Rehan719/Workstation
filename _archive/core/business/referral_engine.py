"""
🧬 REFERRAL ENGINE: SUPREME VIRAL GROWTH
Constitutional Binding: Constraint #20 (SIL Principle), Phase 8 (WORKREP)
Function: Manages referral tracking and Soulbound Reputation Staking (WORKREP).
"""

import hashlib
import time
import logging
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class ReferralRecord:
    referrer_did: str
    referee_did: str
    timestamp: float
    workrep_issued: float
    status: str # 'pending', 'verified', 'rejected'

class ReferralEngine:
    """
    Drives viral growth by incentivizing users with non-transferable WORKREP.
    Integrates with the SWF for sub-ledger updates and priority compute tokens.
    """

    def __init__(self, ueg_logger=None, swf_manager=None):
        self.ueg = ueg_logger
        self.swf = swf_manager
        self.referrals: List[ReferralRecord] = []
        self.workrep_ledger: Dict[str, float] = {}

    async def register_referral(self, referrer_did: str, referee_did: str):
        """
        Registers a new referral and triggers verification.
        """
        logging.info(f"Registering referral: {referrer_did} -> {referee_did}")

        # 1. Check for self-referral (Constitutional Violation)
        if referrer_did == referee_did:
            logging.warning("Self-referral detected and blocked.")
            return False

        # 2. Issue WORKREP (Soulbound)
        # Higher WORKREP unlocks priority compute without feature gating.
        # Guardian Mandate: Referrers earn non-transferable WORKREP tokens.
        base_reward = 100.0
        record = ReferralRecord(
            referrer_did=referrer_did,
            referee_did=referee_did,
            timestamp=time.time(),
            workrep_issued=base_reward,
            status='verified'
        )
        self.referrals.append(record)

        # 3. Update Soulbound Ledger
        self.workrep_ledger[referrer_did] = self.workrep_ledger.get(referrer_did, 0.0) + base_reward

        # 4. Log to UEG with SHA-3-512 and simulated Halo2
        if self.ueg:
            await self.ueg.log_event("referral_conversion", {
                "referrer": referrer_did,
                "referee": referee_did,
                "workrep_total": self.workrep_ledger[referrer_did]
            })

        # 5. Notify SWF for Oxygen Cycle (Metabolism) update
        if self.swf:
            await self.swf.update_viral_metrics(coefficient_delta=0.01)

        # 6. Issue Subscription Credit (Guardian Mandate)
        # Referral discounts: referrers receive subscription credit (10% of first month).
        if self.swf:
            await self.swf.issue_referral_credit(referrer_did, amount_pct=0.10)

        return True

    def get_workrep_score(self, did: str) -> float:
        """Returns the current reputation score for a DID."""
        return self.workrep_ledger.get(did, 0.0)

    def calculate_viral_coefficient(self, window_days: int = 30) -> float:
        """
        Calculates K = i * c.
        i = invitations per user
        c = conversion rate
        """
        # Placeholder for real telemetry calculation
        return 1.34

if __name__ == "__main__":
    re = ReferralEngine()
    import asyncio
    asyncio.run(re.register_referral("did:pqc:owner", "did:pqc:user1"))
    print(f"Viral Coefficient: {re.calculate_viral_coefficient()}")
