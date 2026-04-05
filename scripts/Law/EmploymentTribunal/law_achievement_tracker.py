import json
import os
from datetime import datetime, timezone

class LawAchievementTracker:
    """
    Achievement Tracking System for Law Grand Operation v9.0-ULTIMATE
    Domain: LAW::EMPLOYMENT_TRIBUNAL::ENTERPRISE
    Implements 10 tiers from Claimant to Sovereign Integrator.
    """
    def __init__(self, tracker_path="outputs/Law/EmploymentTribunal/achievements/tracker.json"):
        self.tracker_path = tracker_path
        self._load_tracker()

    def _load_tracker(self):
        if os.path.exists(self.tracker_path):
            with open(self.tracker_path, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {
                "version": "9.0.0-ULTIMATE",
                "domain": "LAW",
                "last_updated": None,
                "statistics": {
                    "total_litigants": 0,
                    "total_et1_filed": 0,
                    "total_disclosures_completed": 0,
                    "total_witness_statements_completed": 0,
                    "total_favorable_outcomes": 0,
                    "total_expert_contributions": 0,
                    "total_reusable_mechanisms_exported": 0,
                    "total_cross_case_adaptations": 0,
                    "total_production_deployments": 0,
                    "total_facility_integrations": 0
                },
                "litigant_achievements": [],
                "expert_achievements": [],
                "community_achievements": [],
                "cross_case_achievements": [],
                "production_achievements": [],
                "facility_achievements": []
            }
            self._save_tracker()

    def _save_tracker(self):
        self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
        os.makedirs(os.path.dirname(self.tracker_path), exist_ok=True)
        with open(self.tracker_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def award_litigant_badge(self, litigant_id, tier, badge_name):
        """Awards a badge to a litigant and updates the tracker, avoiding duplicates for the same tier."""
        # Check if already awarded
        if any(a["litigant_id"] == litigant_id and a["tier"] == tier for a in self.data["litigant_achievements"]):
             print(f"⚠️ Litigant {litigant_id} already has a Tier {tier} badge.")
             return None

        achievement = {
            "litigant_id": litigant_id,
            "tier": tier,
            "badge_name": badge_name,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-LAW-L-{litigant_id}-{tier}"
        }
        self.data["litigant_achievements"].append(achievement)
        self._save_tracker()
        print(f"⚖️ Awarded Law Badge: {badge_name} (Tier {tier}) to Litigant {litigant_id}")
        return achievement

    def award_expert_badge(self, expert_id, tier, badge_name):
        """Awards a badge to an expert contributor"""
        # Check if already awarded
        if any(a["expert_id"] == expert_id and a["tier"] == tier for a in self.data["expert_achievements"]):
             return None

        achievement = {
            "expert_id": expert_id,
            "tier": tier,
            "badge_name": badge_name,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-LAW-E-{expert_id}-{tier}"
        }
        self.data["expert_achievements"].append(achievement)
        self._save_tracker()
        print(f"🎓 Awarded Expert Badge: {badge_name} (Tier {tier}) to Expert {expert_id}")
        return achievement

    def award_cross_case_badge(self, user_id, tier, badge_name, target_case=None):
        """Awards a cross-case adaptation badge"""
        achievement = {
            "user_id": user_id,
            "tier": tier,
            "badge_name": badge_name,
            "target_case": target_case,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-LAW-CC-{user_id}-{tier}"
        }
        self.data["cross_case_achievements"].append(achievement)
        self._save_tracker()
        print(f"🔄 Awarded Cross-Case Badge: {badge_name} (Tier {tier}) to User {user_id}")
        return achievement

    def evaluate_tier_10_sovereign_integrator(self, user_id, cross_case_count, production_deployment_success):
        """Automated evaluation for Tier 10 Sovereign Integrator"""
        if cross_case_count >= 1 and production_deployment_success:
            return self.award_litigant_badge(user_id, 10, "Sovereign Integrator")
        return None

    def update_stats(self, key, increment=1):
        if key in self.data["statistics"]:
            self.data["statistics"][key] += increment
        else:
            self.data["statistics"][key] = increment
        self._save_tracker()

if __name__ == "__main__":
    tracker = LawAchievementTracker()
    tracker.award_litigant_badge("L-001", 1, "Claimant (Mudda'i)")
    print("Law Achievement Tracker Initialized.")
