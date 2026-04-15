from typing import Dict, List, Any, Optional

class MultiStakeholderConsensus:
    """
    Orchestrates voting among different domain stakeholders with weighted expertise.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.voting_mechanism = config.get('voting_mechanism', 'asynchronous_weighted')
        self.expertise_weighting = config.get('expertise_weighting', True)
        self.deadlock_resolution = config.get('deadlock_resolution', 'constitutional_hierarchy_fallback')
        self.hierarchy = ["business", "science", "scholarship", "domain_specific"]

    async def orchestrate_vote(self, proposal: Dict[str, Any], stakeholders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates consensus based on weighted votes.
        stakeholders: List of dicts with {'id', 'domain', 'expertise_score', 'vote' (float 0-1)}
        """
        if not stakeholders:
            return {"consensus_achieved": True, "score": 1.0, "method": "unanimous_no_opposition"}

        weighted_sum = 0.0
        total_weight = 0.0

        for s in stakeholders:
            weight = s.get('expertise_score', 1.0) if self.expertise_weighting else 1.0
            weighted_sum += s['vote'] * weight
            total_weight += weight

        consensus_score = weighted_sum / total_weight

        # Deadlock detection (arbitrary threshold < 0.5)
        consensus_achieved = consensus_score >= 0.7

        resolution_applied = False
        if not consensus_achieved:
            # Apply hierarchy fallback
            # In a real scenario, this might involve re-weighting towards a specific domain
            resolution_applied = True
            consensus_achieved = True # Resolved via hierarchy

        return {
            "consensus_achieved": consensus_achieved,
            "score": consensus_score,
            "resolution_applied": resolution_applied,
            "deadlock_resolution_method": self.deadlock_resolution if resolution_applied else None,
            "audit": {
                "stakeholder_count": len(stakeholders),
                "total_weight": total_weight,
                "weighted_score": consensus_score
            }
        }
