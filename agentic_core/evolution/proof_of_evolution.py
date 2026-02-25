import logging
import random
from typing import Dict, List

logger = logging.getLogger(__name__)

class ProofOfEvolution:
    """
    DC-VI, DH: Proof-of-Evolution Consensus.
    Quorum-based consensus (>= 2/3) for genomic edits.
    Coupled to simulated redox/metabolic health.
    """
    def __init__(self, threshold: float = 0.66):
        self.threshold = threshold
        self.node_voting_weights: Dict[str, float] = {}

    def calculate_voting_weight(self, agent_id: str, energy_ratio: float, ros_level: float) -> float:
        """
        DH: Voting weight is tied to simulated physiological health.
        Healthy nodes (energy high, ROS low) have higher influence.
        """
        # Weight = (ATP/ADP / 5.0) * (1.0 - (ROS / 4.0))
        health_multiplier = (energy_ratio / 5.0) * max(0.1, 1.0 - (ros_level / 4.0))
        weight = 1.0 * health_multiplier
        self.node_voting_weights[agent_id] = weight
        logger.info(f"EVO_CONSENSUS: Node {agent_id} Weight: {weight:.2f}")
        return weight

    def run_consensus(self, trait_id: str, votes: Dict[str, bool]) -> bool:
        """Determines if a mutation quorum is reached."""
        total_weight = sum(self.node_voting_weights.values())
        if total_weight == 0: return False

        weighted_votes_yes = sum(self.node_voting_weights[aid] for aid, v in votes.items() if v)
        quorum_ratio = weighted_votes_yes / total_weight

        reached = quorum_ratio >= self.threshold
        logger.info(f"EVO_CONSENSUS: Trait={trait_id}, Quorum={reached} ({quorum_ratio*100:.1f}%)")
        return reached
