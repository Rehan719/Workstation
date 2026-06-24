import logging
import asyncio
import numpy as np
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class RoleNegotiationProtocol:
    """
    ARTICLE 314: Role Negotiation Protocol.
    Agents negotiate roles based on capabilities, workload, and task requirements.
    Uses weighted confidence scores for consensus.
    """
    async def negotiate(self, team_id: str, agents: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Simulates decentralized role negotiation.
        Each agent proposes a role based on its expertise and current confidence.
        """
        logger.info(f"Negotiation: Starting role assignment for VTF {team_id}")

        # 1. Capability Matching
        # agents = [{"id": "phys_1", "expertise": ["quantum", "math"], "confidence": 0.9}, ...]
        roles = {}

        # Sort by confidence to pick a leader
        sorted_agents = sorted(agents, key=lambda x: x.get("confidence", 0.5), reverse=True)

        # 2. Sequential Role Claiming
        for i, agent in enumerate(sorted_agents):
            agent_id = agent["id"]
            expertise = agent.get("expertise", [])

            if i == 0:
                roles[agent_id] = "LEADER"
            elif "verification" in expertise or "review" in expertise:
                roles[agent_id] = "REVIEWER"
            elif i == 1 and len(sorted_agents) > 2:
                roles[agent_id] = "COORDINATOR"
            else:
                roles[agent_id] = "SPECIALIST"

            logger.debug(f"Negotiation: Agent {agent_id} accepted role {roles[agent_id]}")
            await asyncio.sleep(0.01) # Simulated negotiation latency

        return roles

    def build_consensus(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        ARTICLE 314: Consensus Building.
        Weighted voting based on confidence scores.
        """
        # proposals = [{"option": "A", "confidence": 0.8}, {"option": "B", "confidence": 0.9}]
        if not proposals:
            return {}

        votes = {}
        for p in proposals:
            opt = p["option"]
            weight = p.get("confidence", 1.0)
            votes[opt] = votes.get(opt, 0.0) + weight

        best_option = max(votes, key=votes.get)
        total_weight = sum(votes.values())

        return {
            "winner": best_option,
            "confidence": votes[best_option] / total_weight,
            "consensus_reached": (votes[best_option] / total_weight) > 0.6
        }
