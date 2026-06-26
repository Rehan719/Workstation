import json
import os
from datetime import datetime, timezone

class LawAchievementTracker:
    """
    Achievement Tracking System for Law Grand Operation v9.0-ULTIMATE
    Domain: LAW::EMPLOYMENT_TRIBUNAL::ENTERPRISE
    Implements 10 tiers from Claimant to Sovereign Integrator.
    Execution Date: Sunday, April 05, 2026
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
                "execution_date": "2026-04-05",
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

    def award_litigant_badge(self, litigant_id, tier, badge_name, icon=None, criteria=None):
        """Awards a badge to a litigant and updates the tracker, avoiding duplicates for the same tier."""
        if any(a["litigant_id"] == litigant_id and a["tier"] == tier for a in self.data["litigant_achievements"]):
             print(f"⚠️ Litigant {litigant_id} already has a Tier {tier} badge.")
             return None

        achievement = {
            "litigant_id": litigant_id,
            "tier": tier,
            "badge_name": badge_name,
            "icon": icon,
            "criteria": criteria,
            "awarded_at": datetime.now(timezone.utc).isoformat(),
            "certification_id": f"CERT-LAW-L-{litigant_id}-{tier}"
        }
        self.data["litigant_achievements"].append(achievement)
        self._save_tracker()
        print(f"⚖️ Awarded Law Badge: {badge_name} {icon or ''} (Tier {tier}) to Litigant {litigant_id}")
        return achievement

    def award_ultimate_tiers(self, litigant_id):
        """Helper to award all 10 tiers for the ultimate integration simulation."""
        tiers = [
            (1, "Claimant (Mudda'i)", "📋", "Complete orientation + file ET1"),
            (2, "Prepared Litigant (Musta'id)", "🗂️", "Complete disclosure + evidence mapping"),
            (3, "Active Litigant (Fa''al)", "⚖️", "Complete witness statement + ACAS engagement"),
            (4, "Advanced Litigant (Mutaqaddim)", "🎯", "Complete skeleton argument + cross-exam prep"),
            (5, "Hearing Candidate (Murashshaḥ)", "🎭", "Complete bundle + pre-hearing simulation"),
            (6, "Successful Litigant (Nājiḥ)", "👑", "Favorable tribunal outcome + costs recovery"),
            (7, "Legal Mentor (Murshid)", "🏛️", "Certified to guide other litigants"),
            (8, "Pipeline Architect", "🔧", "Contribute reusable litigation pipeline mechanisms"),
            (9, "Community Guardian", "🛡️", "Moderate expert contributions + ensure quality"),
            (10, "Sovereign Integrator", "🌐", "Successfully integrate litigation platform across cases")
        ]
        for tier, name, icon, crit in tiers:
            self.award_litigant_badge(litigant_id, tier, name, icon, crit)

    def update_stats(self, key, increment=1):
        if key in self.data["statistics"]:
            self.data["statistics"][key] += increment
        else:
            self.data["statistics"][key] = increment
        self._save_tracker()

if __name__ == "__main__":
    tracker = LawAchievementTracker()
    tracker.award_ultimate_tiers("L-001")
    print("Law Achievement Tracker v9.0-ULTIMATE Initialized.")
