import json
import os
from datetime import datetime, timezone

class AchievementTracker:
    """
    Achievement Tracking System for Quran Education Platform
    Domain: RELIGION::QEP::ENTERPRISE
    """
    def __init__(self, tracker_path="outputs/Religion/QuranEducation/achievements/tracker.json"):
        self.tracker_path = tracker_path
        self._load_tracker()

    def _load_tracker(self):
        if os.path.exists(self.tracker_path):
            with open(self.tracker_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "version": "8.0.0",
                "last_updated": None,
                "statistics": {
                    "total_students": 0,
                    "total_hifz_completers": 0,
                    "total_teachers_certified": 0
                },
                "student_achievements": [],
                "teacher_achievements": []
            }
            self._save_tracker()

    def _save_tracker(self):
        self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
        os.makedirs(os.path.dirname(self.tracker_path), exist_ok=True)
        with open(self.tracker_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def award_student_badge(self, student_id, tier, badge_name):
        """Awards a badge to a student and updates the tracker"""
        achievement = {
            "student_id": student_id,
            "tier": tier,
            "badge_name": badge_name,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-QEP-S-{student_id}-{tier}"
        }
        self.data["student_achievements"].append(achievement)
        self._save_tracker()
        print(f"Awarded Badge: {badge_name} (Tier {tier}) to Student {student_id}")
        return achievement

    def update_stats(self, key, value):
        if key in self.data["statistics"]:
            self.data["statistics"][key] = value
            self._save_tracker()

if __name__ == "__main__":
    tracker = AchievementTracker()
    tracker.award_student_badge(101, 1, "Beginner (Mubtadi)")
    tracker.update_stats("total_students", 1)
