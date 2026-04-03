import json
import os
from datetime import datetime, timezone

class AchievementTracker:
    """
    Achievement Tracking System for Quran Education Platform
    Domain: RELIGION::QEP::ENTERPRISE
    v8.4: Enhanced with Cross-Domain Adapter (Tier 10) support.
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
                "version": "8.4.0",
                "last_updated": None,
                "statistics": {
                    "total_students": 0,
                    "total_hifz_completers": 0,
                    "total_teachers_certified": 0,
                    "total_community_moderations": 0,
                    "total_community_contributions": 0,
                    "total_cross_domain_adaptations": 0
                },
                "student_achievements": [],
                "teacher_achievements": [],
                "community_achievements": [],
                "cross_domain_achievements": []
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

    def award_community_badge(self, user_id, tier, badge_name, criteria_met=None):
        """Awards a community-specific badge, including Tier 9 Community Guardian"""
        achievement = {
            "user_id": user_id,
            "tier": tier,
            "badge_name": badge_name,
            "criteria_met": criteria_met,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-QEP-C-{user_id}-{tier}"
        }
        if "community_achievements" not in self.data:
            self.data["community_achievements"] = []
        self.data["community_achievements"].append(achievement)
        self._save_tracker()
        print(f"Awarded Community Badge: {badge_name} (Tier {tier}) to User {user_id}")
        return achievement

    def award_cross_domain_badge(self, user_id, tier, badge_name, domain=None):
        """Awards a cross-domain specific badge, including Tier 10 Cross-Domain Adapter"""
        achievement = {
            "user_id": user_id,
            "tier": tier,
            "badge_name": badge_name,
            "target_domain": domain,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-QEP-XD-{user_id}-{tier}"
        }
        if "cross_domain_achievements" not in self.data:
            self.data["cross_domain_achievements"] = []
        self.data["cross_domain_achievements"].append(achievement)
        self._save_tracker()
        print(f"Awarded Cross-Domain Badge: {badge_name} (Tier {tier}) to User {user_id}")
        return achievement

    def evaluate_community_guardian_tier_9(self, user_id, moderation_actions, quality_score, trust_score):
        """Automated evaluation for Tier 9 Community Guardian"""
        if moderation_actions >= 50 and quality_score >= 0.95 and trust_score >= 0.90:
            return self.award_community_badge(user_id, 9, "Community Guardian",
                                             {"moderation": moderation_actions, "quality": quality_score, "trust": trust_score})
        return None

    def evaluate_cross_domain_adapter_tier_10(self, user_id, adaptation_count, target_domain):
        """Automated evaluation for Tier 10 Cross-Domain Adapter"""
        if adaptation_count >= 1: # Criteria: successfully adapt to at least one other domain
            return self.award_cross_domain_badge(user_id, 10, "Cross-Domain Adapter", target_domain)
        return None

    def evaluate_ai_ethics_steward_tier_10(self, user_id, ethics_audit_count, explainability_score):
        """Automated evaluation for Tier 10 AI Ethics Steward (v8.6)"""
        if ethics_audit_count >= 10 and explainability_score >= 0.95:
            return self.award_community_badge(user_id, 10, "AI Ethics Steward",
                                             {"ethics_audits": ethics_audit_count, "explainability": explainability_score})
        return None

    def update_stats(self, key, value):
        if key in self.data["statistics"]:
            self.data["statistics"][key] = value
            self._save_tracker()
        elif key not in self.data["statistics"]:
            self.data["statistics"][key] = value
            self._save_tracker()

if __name__ == "__main__":
    tracker = AchievementTracker()
    tracker.award_student_badge(101, 1, "Beginner (Mubtadi)")
    tracker.evaluate_cross_domain_adapter_tier_10(303, 1, "Science")
