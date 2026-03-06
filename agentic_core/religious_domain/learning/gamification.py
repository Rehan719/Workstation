import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class GamifiedLearning:
    """
    ARTICLE 243: Gamification Ethics Mandate.
    Handles achievements, XP (Nur Points), and streaks with ethical constraints.
    """
    def __init__(self, dual_metric_middleware: Any):
        self.middleware = dual_metric_middleware

    def award_nur_points(self, user_id: str, points: int, activity: str, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Awards Nur Points (XP) while enforcing ethical constraints via spiritual KPIs.
        """
        # ARTICLE 243: Check if gamification engagement is healthy
        eval_result = self.middleware.evaluate_operation(user_id, "GAMIFICATION_REWARD", current_context)

        if eval_result["decision"] == "CONSTRAIN":
            logger.warning(f"Gamification: Points constrained for {user_id} due to spiritual priority (Article 243).")
            return {
                "status": "CONSTRAINED",
                "message": eval_result["reasoning"]["spiritual"],
                "points_awarded": 0
            }

        return {
            "status": "SUCCESS",
            "user_id": user_id,
            "points_awarded": points,
            "activity": activity,
            "timestamp": datetime.now().isoformat()
        }

    def get_badges(self, user_id: str) -> List[str]:
        """Returns earned achievement badges."""
        return ["FAST_MEMORIZER", "CONSISTENT_DHIKR", "RAMADAN_WARRIOR"]
