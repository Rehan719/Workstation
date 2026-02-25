import logging
from typing import Dict, Any
from .latency_arbiter import SystemTier, LatencyArbiter

logger = logging.getLogger(__name__)

class SurvivalEngineV3:
    """Article 50: Supreme meta-governor resolving conflicts via hierarchy."""

    HIERARCHY = [
        SystemTier.IMMUNE,
        SystemTier.NERVOUS,
        SystemTier.DIGESTIVE,
        SystemTier.AGING
    ]

    def __init__(self, latency_arbiter: LatencyArbiter):
        self.latency_arbiter = latency_arbiter
        self.active_signals = {} # Tier -> signal/state

    def resolve_conflict(self, tier_a: SystemTier, tier_b: SystemTier) -> SystemTier:
        """Resolves which tier takes priority."""
        idx_a = self.HIERARCHY.index(tier_a)
        idx_b = self.HIERARCHY.index(tier_b)

        winner = tier_a if idx_a < idx_b else tier_b
        logger.info(f"SURVIVAL: Conflict between {tier_a.value} and {tier_b.value}. Winner: {winner.value}")
        return winner

    def validate_action(self, tier: SystemTier, action_metadata: Dict[str, Any]) -> bool:
        """Mandatory check for any growth or adaptation action."""
        # Article 50: Security supersedes growth during threats
        if self.active_signals.get(SystemTier.IMMUNE) == "THREAT":
            if tier != SystemTier.IMMUNE:
                logger.error(f"SURVIVAL: VETO! Blocking {tier.value} action due to active IMMUNE threat.")
                return False
        return True

    def set_signal(self, tier: SystemTier, state: str):
        self.active_signals[tier] = state
        logger.debug(f"SURVIVAL: Signal from {tier.value} set to {state}")
