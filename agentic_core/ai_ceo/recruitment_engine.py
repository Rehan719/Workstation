import logging
import random
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class RecruitmentEngine:
    """
    ARTICLE 280: Immune-Inspired Agent Recruitment.
    Uses constraint-weighted activation (T-cell thresholds).
    """
    def __init__(self):
        # Weights for activation thresholds
        self.weights = {
            "regulatory_risk": 0.4,
            "compute_cost": 0.2,
            "data_provenance": 0.3,
            "coherence": 0.1
        }

    def recruit_agents(self, project_context: Dict[str, Any], agent_pool: List[Dict[str, Any]]) -> List[str]:
        """Activates agents only when context matches specialized profiles."""
        activated_ids = []

        for agent in agent_pool:
            score = self._calculate_activation_score(project_context, agent)
            # Threshold modeled after T-cell recognition
            if score > 0.75:
                logger.info(f"Recruitment: Agent {agent['id']} ACTIVATED (Score: {score:.2f})")
                activated_ids.append(agent["id"])
            else:
                logger.debug(f"Recruitment: Agent {agent['id']} remains INACTIVE.")

        return activated_ids

    def _calculate_activation_score(self, context: Dict[str, Any], agent: Dict[str, Any]) -> float:
        # Specialized profile matching
        match_score = 0.0
        if context.get("domain") == agent.get("specialization"):
            match_score += 0.5

        # Risk weighting
        risk_penalty = context.get("risk_level", 0) * self.weights["regulatory_risk"]

        return min(1.0, match_score + random.random() * 0.5 - risk_penalty)

class SpanControlEngine:
    """ARTICLE 280: Dynamic supervisory adjustment."""
    def __init__(self, max_ratio: int = 8):
        self.max_ratio = max_ratio

    def get_optimal_dispatch_limit(self, system_load: float) -> int:
        """Throttles supervisor span based on real-time resource utilization."""
        if system_load > 0.8:
            return 3
        if system_load > 0.5:
            return 5
        return self.max_ratio
