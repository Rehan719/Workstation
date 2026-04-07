import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v16_omnipotent():
    print("🔍 Performing v16.0-OMNIPOTENT definitive verification...")

    path_v16 = "outputs/Law/EmploymentTribunal/v16/"

    # 1. Check Artifact Presence (31+)
    # 24 core + 4 signature + status + manifest + verification_log
    expected_md = 28
    md_files = [f for f in os.listdir(path_v16) if f.endswith(".md")]
    print(f"Detected {len(md_files)} MD artifacts.")
    if len(md_files) < expected_md:
        print(f"❌ Missing artifacts. Expected {expected_md}, found {len(md_files)}")
        return False

    # 2. Check Primary Master Guide for Template 1-3
    guide_path = os.path.join(path_v16, "LITIGANT_MASTER_GUIDE_v16.0_OMNIPOTENT.md")
    with open(guide_path, 'r') as f:
        content = f.read()
        if all(t in content for t in ["Template 1", "Template 2", "Template 3"]):
            print("✅ Templates 1-3 detected in Master Guide.")
        else:
            print("❌ Templates 1-3 missing from Master Guide.")
            return False
        if "blockchain" in content.lower():
            print("✅ Blockchain integrity anchors referenced.")
        else:
            print("❌ Blockchain reference missing.")
            return False

    # 3. Check status and convergence
    status_path = os.path.join(path_v16, "v16_status.json")
    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get("status") == "OMNIPOTENT-DEVELOPMENT-ACTIVE":
             print(f"✅ Status active. Convergence: {status.get('convergence_score')}")
        else:
             print("❌ Invalid status.")
             return False

    print("✅ v16.0-OMNIPOTENT Definitive Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v16_omnipotent():
        sys.exit(0)
    else:
        sys.exit(1)
