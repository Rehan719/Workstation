import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GamificationEngine:
    """
    ARTICLE 1022: Gamification & Engagement Standard v133.0.
    Handles points, badges, levels, and leaderboards to drive user engagement.
    """
    def __init__(self):
        self.user_stats = {}

    def award_points(self, user_id: str, points: int, reason: str):
        """Awards points to a user and checks for level-ups."""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {"points": 0, "level": 1, "badges": [], "history": []}

        stats = self.user_stats[user_id]
        stats["points"] += points
        stats["history"].append({"points": points, "reason": reason})

        # Simple level up logic
        new_level = (stats["points"] // 1000) + 1
        if new_level > stats["level"]:
            stats["level"] = new_level
            logger.info(f"Gamification: User {user_id} leveled up to {new_level}!")

        logger.info(f"Gamification: Awarded {points} points to {user_id} for {reason}.")

    def award_badge(self, user_id: str, badge_id: str):
        """Awards a unique badge to a user."""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {"points": 0, "level": 1, "badges": [], "history": []}

        if badge_id not in self.user_stats[user_id]["badges"]:
            self.user_stats[user_id]["badges"].append(badge_id)
            logger.info(f"Gamification: User {user_id} earned badge '{badge_id}'!")

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        return self.user_stats.get(user_id, {"status": "NEW_USER"})

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Returns the top users sorted by points."""
        sorted_users = sorted(
            [{"user_id": k, **v} for k, v in self.user_stats.items()],
            key=lambda x: x["points"],
            reverse=True
        )
        return sorted_users[:10]
