import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class TeamRegistry:
    """
    ARTICLE 314: Team Registry.
    Tracks active Virtual Task Forces (VTF).
    """
    def __init__(self):
        self.active_teams = {}

    def register_team(self, team_id: str, objective: str, members: List[str]):
        logger.info(f"Registry: Registering VTF {team_id} for {objective}")
        self.active_teams[team_id] = {
            "objective": objective,
            "members": members,
            "status": "ASSEMBLING"
        }

    def update_status(self, team_id: str, status: str):
        if team_id in self.active_teams:
            self.active_teams[team_id]["status"] = status
