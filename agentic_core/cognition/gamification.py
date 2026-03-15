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
        self.ranks = [
            (1, "Novice Learner"),
            (5, "AI Explorer"),
            (10, "Developer Practitioner"),
            (15, "AI Orchestrator"),
            (25, "Strategic Architect"),
            (50, "Sovereign Master")
        ]
        self.platform_quests = {
            "microsoft": "Copilot Challenge: Complete 5 AI-assisted tasks",
            "google": "Gemini Quest: Reach 'AI Pro' student status",
            "amazon": "Bedrock Builder: Optimize 3 non-urgent workloads via Flex",
            "meta": "Llama Hackathon: Contribute to an open-source model",
            "apple": "Swift Challenge: Deploy an on-device privacy-first app",
            "nvidia": "GPU Racing: Optimize a CUDA kernel for 10% gain",
            "tesla": "FSD Simulation: Achieve zero-intervention drive"
        }

    def award_points(self, user_id: str, points: int, reason: str):
        """Awards points to a user and checks for level-ups and rank changes."""
        if user_id not in self.user_stats:
            self.user_stats[user_id] = {
                "points": 0,
                "level": 1,
                "rank": "Novice Learner",
                "badges": [],
                "history": [],
                "retention_score": 100
            }

        stats = self.user_stats[user_id]
        stats["points"] += points
        stats["history"].append({"points": points, "reason": reason, "timestamp": "now"})

        # Level up logic
        new_level = (stats["points"] // 1000) + 1
        if new_level > stats["level"]:
            stats["level"] = new_level
            # Update rank based on level
            for min_lv, rank_name in reversed(self.ranks):
                if new_level >= min_lv:
                    stats["rank"] = rank_name
                    break
            logger.info(f"Gamification: User {user_id} reached Level {new_level} ({stats['rank']})!")

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
