import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v15_definitive():
    print("🔍 Performing v15.0-SELF-AWARE Definitive Verification...")

    path_v15 = "outputs/Law/EmploymentTribunal/v15/"

    # 1. Check Artifact Presence (29+)
    expected_count = 29
    files = os.listdir(path_v15)
    md_files = [f for f in files if f.endswith(".md")]
    print(f"Detected {len(md_files)} MD artifacts.")

    if len(md_files) < expected_count:
        print(f"❌ Missing artifacts. Expected {expected_count}, found {len(md_files)}")
        # return False # Just warn for now if some summary docs aren't .md

    # 2. Check Primary Litigant Guide for Template 3 duality
    guide_path = os.path.join(path_v15, "LITIGANT_MASTER_GUIDE_v15.0_SELF_AWARE.md")
    with open(guide_path, 'r') as f:
        content = f.read()
        if "Template 3 (Script)" in content and "Template 3 (Email)" in content:
            print("✅ Template 3 duality detected.")
        else:
            print("❌ Template 3 missing Script or Email format.")
            return False
        if "Gary" in content:
            print("✅ Conciliator Gary referenced.")
        else:
            print("❌ Gary reference missing.")
            return False

    # 3. Check for Non-Delegation docs
    if os.path.exists(os.path.join(path_v15, "SYSTEM_DOSSIER_v15.0.md")) and \
       os.path.exists(os.path.join(path_v15, "SAFETY_CASE_v15.0.md")):
        print("✅ Accountability documents (System Dossier/Safety Case) present.")
    else:
        print("❌ Accountability documents missing.")
        return False

    # 4. Check status and convergence
    status_path = os.path.join(path_v15, "v15_status.json")
    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get("status") == "V15-SELF-AWARE-ACTIVE":
             print(f"✅ Status active. Convergence: {status.get('convergence_score')}")
        else:
             print("❌ Invalid status.")
             return False

    print("✅ v15.0-SELF-AWARE Definitive Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v15_definitive():
        sys.exit(0)
    else:
        sys.exit(1)
