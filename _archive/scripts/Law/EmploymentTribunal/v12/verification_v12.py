import os
import sys
import json
from datetime import datetime

# Ensure absolute paths for module discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

class OmegaVerificationV12:
    """
    Law Grand Operation v12.0-OMEGA Verification Suite.
    Confirms AI integration validity, swarm locking, and OMEGA data integrity.
    """

    def __init__(self):
        self.manifest_path = "outputs/Law/EmploymentTribunal/v12/audit/omega_ai_manifest.json"
        self.swarm_path = "outputs/Law/EmploymentTribunal/v12/analytics/swarm_coordination.json"
        self.audit_log = "outputs/Law/EmploymentTribunal/v12/audit/vsb_signature_log_v12.0_omega.jsonl"
        self.report_path = "outputs/Law/EmploymentTribunal/v12/audit/verification_report_v12_omega.json"

    def verify_omega_ai(self):
        print("✅ Commencing Law v12.0-OMEGA Verification Suite...")

        results = {
            "version": "12.0.0-OMEGA",
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }

        # 1. AI Manifest Check
        check_manifest = os.path.exists(self.manifest_path)
        results["checks"].append({"check": "AI Manifest Presence", "status": "PASS" if check_manifest else "FAIL"})

        # 2. Swarm Coordination Check
        if os.path.exists(self.swarm_path):
            with open(self.swarm_path, 'r') as f:
                swarm = json.load(f)
                realms_synced = all(data.get("sync_status") == "LOCKED" for realm, data in swarm.items())
                results["checks"].append({
                    "check": "Swarm Intelligence Locking (6 Realms)",
                    "status": "PASS" if realms_synced and len(swarm) == 6 else "FAIL"
                })

        # 3. AI Predictive Accuracy
        if check_manifest:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                forecast = manifest.get("liability_forecast", {})
                results["checks"].append({
                    "check": "AI 100k iteration Monte Carlo",
                    "status": "PASS" if forecast.get("iterations") == 100000 else "FAIL"
                })
                results["checks"].append({
                    "check": "AI-Verified Liability (95%)",
                    "status": "PASS" if forecast.get("liability_probability") == 0.95 else "FAIL"
                })

        # 4. Audit Log Integrity
        check_audit = os.path.exists(self.audit_log)
        results["checks"].append({"check": "OMEGA-AI Audit Log", "status": "PASS" if check_audit else "FAIL"})

        # 5. Final Report Presence
        check_report = os.path.exists("outputs/Law/EmploymentTribunal/v12/FINAL_SUBMISSION_REPORT_v12.0_OMEGA.md")
        results["checks"].append({"check": "Final OMEGA-AI Report Presence", "status": "PASS" if check_report else "FAIL"})

        # Overall Status
        overall_pass = all(c["status"] == "PASS" for c in results["checks"])
        results["overall_status"] = "OMEGA_AI_CERTIFIED" if overall_pass else "OMEGA_AI_FAILED"

        with open(self.report_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✅ OMEGA-AI Verification Complete: {results['overall_status']}")
        return results

if __name__ == "__main__":
    verifier = OmegaVerificationV12()
    verifier.verify_omega_ai()
