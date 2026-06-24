import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ReferralEngine:
    """
    ARTICLE 208: Referral Program Automation.
    Tracks unique referral links and applies credits to invoices.
    """
    def __init__(self):
        self.referrals: Dict[str, str] = {} # referee_id: referrer_id
        self.credits: Dict[str, float] = {} # referrer_id: credit_amount

    def track_referral(self, referee_id: str, referrer_id: str):
        self.referrals[referee_id] = referrer_id
        self.credits[referrer_id] = self.credits.get(referrer_id, 0.0) + 50.0 # 0 credit
        logger.info(f"REFERRAL: User {referrer_id} referred {referee_id}. 0 credit applied.")

    def get_credit(self, referrer_id: str) -> float:
        return self.credits.get(referrer_id, 0.0)
