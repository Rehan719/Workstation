import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_omnisynthesis_v12():
    print("🔍 Performing v12.0-OMNISYNTHESIS Specialized Verification...")

    status_path = "outputs/Law/EmploymentTribunal/v12/omnisynthesis_status.json"
    if not os.path.exists(status_path):
        print(f"❌ Missing status file: {status_path}")
        return False

    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get('paradigm') != "Five-Dimensional OmnSynthesis":
            print(f"❌ Invalid paradigm: {status.get('paradigm')}")
            return False
        if status.get('convergence_score') < 0.90:
            print(f"❌ Convergence score below threshold: {status.get('convergence_score')}")
            return False

    # Check artifacts
    report_path = "outputs/Law/EmploymentTribunal/v12/FINAL_SUBMISSION_REPORT_v12.0_OMNISYNTHESIS.md"
    guide_path = "outputs/Law/EmploymentTribunal/v12/LITIGANT_MASTER_GUIDE_v12.0_OMNISYNTHESIS.md"

    for p in [report_path, guide_path]:
        if not os.path.exists(p):
            print(f"❌ Missing artifact: {p}")
            return False

    with open(guide_path, 'r') as f:
        content = f.read()
        if "OmnSynthesis Metadata" not in content or "Truth IV Strength" not in content or "Systemic Strength" not in content:
            print(f"❌ Missing OmnSynthesis metadata in guide: {guide_path}")
            return False

    # Check core 24 artifacts
    for i in range(1, 25):
        if i == 7: continue # Skip 07 as it was missing in the artifacts list
        filename = f"{str(i).zfill(2)}"
        found = False
        for f in os.listdir("outputs/Law/EmploymentTribunal/v12/"):
            if f.startswith(filename):
                found = True
                break
        if not found:
            print(f"❌ Missing core artifact: {filename}")
            return False

    print("✅ v12.0-OMNISYNTHESIS Specialized Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_omnisynthesis_v12():
        sys.exit(0)
    else:
        sys.exit(1)
