import logging
import asyncio
from typing import Dict, Any, List, Optional
from .registry import TeamRegistry
from .negotiation import RoleNegotiationProtocol
from .memory import CollectiveMemory
from .conflict import ConflictResolutionModule
from .formation import TeamFormationOptimizer

logger = logging.getLogger(__name__)

class BiomimeticTeamOrchestrator:
    """
    v100.0: Master Biomimetic Team Orchestrator (BTO).
    Governs Virtual Task Force (VTF) formation, negotiation, and memory.
    Governed by Articles 314-317.
    """
    def __init__(self):
        self.registry = TeamRegistry()
        self.negotiation = RoleNegotiationProtocol()
        self.memory = CollectiveMemory()
        self.conflict = ConflictResolutionModule()
        self.formation = TeamFormationOptimizer()
        logger.info("BTO: Biomimetic Team Orchestrator Awakened.")

    async def form_vtf(self, intent_id: str, domain: str, requirements: List[str]) -> str:
        """
        Orchestrates the formation of a new Virtual Task Force.
        1. Optimize Composition -> 2. Register -> 3. Negotiate Roles
        """
        # 1. Optimal composition based on intent and history
        best_strategies = self.memory.query_best_strategies(domain)
        agent_ids = self.formation.find_optimal_team(requirements)

        team_id = f"vtf_{intent_id}_{domain}"
        self.registry.register_team(team_id, f"Mission for {domain}", agent_ids)

        # 2. Mocking agent profiles for negotiation
        # In full production, these come from sub-reactor registries
        agents = []
        for aid in agent_ids:
            agents.append({
                "id": aid,
                "expertise": [domain, "general"],
                "confidence": 0.85 + (np.random.random() * 0.1 if 'np' in globals() else 0.05)
            })

        # 3. Role Negotiation
        roles = await self.negotiation.negotiate(team_id, agents)

        self.registry.active_teams[team_id]["roles"] = roles
        self.registry.update_status(team_id, "OPERATIONAL")

        logger.info(f"BTO: VTF {team_id} is OPERATIONAL with {len(agent_ids)} agents.")
        return team_id

    def record_vtf_success(self, team_id: str, domain: str, strategy: str, result: Dict[str, Any]):
        self.memory.record_outcome(team_id, domain, strategy, result, success=True)
        self.registry.update_status(team_id, "COMPLETED")

    def record_vtf_failure(self, team_id: str, domain: str, strategy: str, error: str):
        self.memory.record_outcome(team_id, domain, strategy, {"error": error}, success=False)
        self.registry.update_status(team_id, "FAILED")
