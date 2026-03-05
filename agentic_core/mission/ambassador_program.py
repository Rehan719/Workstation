import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MissionAmbassadorProgram:
    """
    ARTICLE 227: Mission Ambassador Program.
    Recruits clients as ambassadors to share Dawah and impact stories.
    """
    def __init__(self):
        self.ambassadors = {} # client_id: stats

    def recruit_ambassador(self, client_id: str):
        self.ambassadors[client_id] = {
            "referrals": 0,
            "stories_shared": 0,
            "credits": 0.0
        }
        logger.info(f"MISSION: Recruited client {client_id} as a Mission Ambassador.")

    def log_ambassador_activity(self, client_id: str, activity: str):
        if client_id in self.ambassadors:
            if activity == "STORY":
                self.ambassadors[client_id]["stories_shared"] += 1
                self.ambassadors[client_id]["credits"] += 10.0
            logger.info(f"MISSION: Logged {activity} for ambassador {client_id}.")
