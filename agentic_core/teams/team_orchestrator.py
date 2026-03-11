import logging
import uuid
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TeamOrchestrator:
    """ARTICLE 116: Biomimetic Team Dynamics."""
    def __init__(self, health_target: float = 0.9):
        self.health_target = health_target
        self.active_teams = {}

    def form_team(self, agents: List[str], objective: str) -> str:
        """Forms a task force for a specific objective."""
        team_id = str(uuid.uuid4())
        self.active_teams[team_id] = {
            "agents": agents,
            "objective": objective,
            "health": 1.0,
            "roles": self._negotiate_roles(agents)
        }
        logger.info(f"Team {team_id} formed for {objective}")
        return team_id

    def _negotiate_roles(self, agents: List[str]) -> Dict[str, str]:
        roles = ["scout", "worker", "judge", "healer"]
        return {agent: roles[i % len(roles)] for i, agent in enumerate(agents)}

    def get_team_health(self, team_id: str) -> float:
        return self.active_teams.get(team_id, {}).get("health", 0.0)
