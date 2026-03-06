import logging
from typing import Dict

logger = logging.getLogger(__name__)

class VotingWeight:
    """
    DC-VI, DH: Voting weight calculation based on node contribution and energy.
    Rewards nodes that contribute positively to the ecosystem.
    """
    def calculate_weight(self, trust_score: float, residual_energy: float) -> float:
        # Weight is a function of trust and health (ATP/ADP ratio)
        weight = trust_score * (residual_energy / 5.0)
        logger.info(f"GOVERNANCE: Calculated voting weight: {weight:.2f}")
        return max(0.1, weight)
