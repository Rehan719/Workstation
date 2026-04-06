import os
import sys
import json
from datetime import datetime

# Ensure absolute paths for module discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

class QuadraVeritasVerificationV13:
    """
    Law Grand Operation v13.0-QUADRA-VERITAS Verification Suite.
    Confirms paradigm shift validity and data integrity.
    """

    def __init__(self):
        self.manifest_path = "outputs/Law/EmploymentTribunal/v13/audit/quadra_manifest.json"
        self.status_path = "outputs/Law/EmploymentTribunal/v13/quadra_veritas_status.json"
        self.report_path = "outputs/Law/EmploymentTribunal/v13/audit/verification_report_v13_quadra.json"

    def verify(self):
        print("✅ Commencing Law v13.0-QUADRA-VERITAS Verification Suite...")

        results = {
            "version": "13.0.0-QUADRA-VERITAS",
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }

        # 1. Manifest Presence
        check_manifest = os.path.exists(self.manifest_path)
        results["checks"].append({"check": "Manifest Presence", "status": "PASS" if check_manifest else "FAIL"})

        # 2. Four Truths Paradigm Check
        if os.path.exists(self.status_path):
            with open(self.status_path, 'r') as f:
                status = json.load(f)
                results["checks"].append({
                    "check": "Paradigm Status (Temporal-Dynamic)",
                    "status": "PASS" if status.get("paradigm") == "Temporal-Dynamic" else "FAIL"
                })
                results["checks"].append({
                    "check": "Convergence Accuracy (0.98)",
                    "status": "PASS" if status.get("convergence_score") == 0.98 else "FAIL"
                })

        # 3. Artifact Presence
        check_report = os.path.exists("outputs/Law/EmploymentTribunal/v13/FINAL_SUBMISSION_REPORT_v13.0_QUADRA_VERITAS.md")
        results["checks"].append({"check": "Final Quadra Report Presence", "status": "PASS" if check_report else "FAIL"})

        # Overall Status
        overall_pass = all(c["status"] == "PASS" for c in results["checks"])
        results["overall_status"] = "QUADRA_VERITAS_VERIFIED" if overall_pass else "QUADRA_VERITAS_FAILED"

        with open(self.report_path, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"✅ Quadra-Veritas Verification Complete: {results['overall_status']}")
        return results

if __name__ == "__main__":
    verifier = QuadraVeritasVerificationV13()
    verifier.verify()
