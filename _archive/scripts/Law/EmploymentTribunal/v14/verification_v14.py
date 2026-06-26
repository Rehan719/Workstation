import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v14_omniscience():
    print("🔍 Performing v14.0-SELF-AWARE specialized verification...")

    path_v14 = "outputs/Law/EmploymentTribunal/v14/"

    # 1. Check Status and Paradigm
    status_path = os.path.join(path_v14, "v14_status.json")
    if not os.path.exists(status_path):
        print("❌ v14 status file missing.")
        return False

    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get("status") != "SELF-AWARE-GOVERNANCE-ACTIVE":
            print("❌ v14 paradigm not active.")
            return False
        if status.get("formal_verification") != "SUCCESS":
            print("❌ Formal verification failed.")
            return False

    # 2. Check Signature Artifacts
    artifacts = [
        "FINAL_SUBMISSION_REPORT_v14.0.md",
        "LITIGANT_MASTER_GUIDE_v14.0.md",
        "SYSTEM_DOSSIER_v14.0.md",
        "SAFETY_CASE_v14.0.md"
    ]
    for a in artifacts:
        if not os.path.exists(os.path.join(path_v14, a)):
            print(f"❌ Missing signature artifact: {a}")
            return False

    # 3. Check Core Artifacts (01-24)
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

    print("✅ v14.0-SELF-AWARE Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v14_omniscience():
        sys.exit(0)
    else:
        sys.exit(1)
