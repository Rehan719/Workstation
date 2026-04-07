import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_definitive_v14():
    print("🔍 Performing v14.0-SELF-AWARE Definitive Verification...")

    path_v14 = "outputs/Law/EmploymentTribunal/v14/"

    # 1. Check Status and Definitive Paradigm
    status_path = os.path.join(path_v14, "v14_definitive_status.json")
    if not os.path.exists(status_path):
        print("❌ v14 definitive status file missing.")
        return False

    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get("paradigm") != "7-Dimensional Omniscience":
            print(f"❌ Invalid paradigm: {status.get('paradigm')}")
            return False
        if status.get("convergence_score") != 0.96:
            print(f"❌ Convergence score mismatch: {status.get('convergence_score')}")
            return False

    # 2. Check Signature Artifacts (Definitive)
    artifacts = [
        "FINAL_SUBMISSION_REPORT_v14.0_SELF_AWARE.md",
        "LITIGANT_MASTER_GUIDE_v14.0_SELF_AWARE.md",
        "SYSTEM_DOSSIER_v14.0.md",
        "SAFETY_CASE_v14.0.md"
    ]
    for a in artifacts:
        if not os.path.exists(os.path.join(path_v14, a)):
            print(f"❌ Missing signature artifact: {a}")
            return False

    # 3. Check Templates in Master Guide
    with open(os.path.join(path_v14, "LITIGANT_MASTER_GUIDE_v14.0_SELF_AWARE.md"), 'r') as f:
        content = f.read()
        if "Template 1" not in content or "Template 2" not in content or "Template 3" not in content:
            print("❌ Templates missing from primary guide.")
            return False
        if "Conciliator (Gary)" not in content:
            print("❌ Gary reference missing from template 3.")
            return False
        if "Omniscience Metadata" not in content:
            print("❌ Metadata missing from primary guide.")
            return False

    # 4. Check Core 24 Artifacts Presence
    for i in range(1, 25):
        if i == 7: continue
        filename = f"{str(i).zfill(2)}"
        found = False
        for f in os.listdir(path_v14):
            if f.startswith(filename):
                found = True
                break
        if not found:
            print(f"❌ Missing core v14 artifact: {filename}")
            return False

    print("✅ v14.0-SELF-AWARE Definitive Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_definitive_v14():
        sys.exit(0)
    else:
        sys.exit(1)
