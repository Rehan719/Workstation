import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v15_definitive_consolidation():
    print("🔍 Performing v15.0-SELF-AWARE Definitive Consolidation Verification...")

    path_v15 = "outputs/Law/EmploymentTribunal/v15/"

    # 1. Artifact Count (31)
    md_files = [f for f in os.listdir(path_v15) if f.endswith(".md")]
    print(f"Detected {len(md_files)} MD artifacts.")
    if len(md_files) < 31:
        print(f"❌ Missing artifacts. Expected 31, found {len(md_files)}")
        return False

    # 2. Template 3 Duality
    guide_path = os.path.join(path_v15, "LITIGANT_MASTER_GUIDE_v15.0_SELF_AWARE.md")
    with open(guide_path, 'r') as f:
        content = f.read()
        if "Format A: Script Format" in content and "Format B: Email Format" in content:
            print("✅ Template 3 duality verified.")
        else:
            print("❌ Template 3 duality missing.")
            return False

    # 3. PDF Ingestion Integration
    uuids = ["b24e44e2", "c96410cf", "faa2afad", "2c5f2e15", "bbedd08b", "0944deb9", "99cfd2ef"]
    for uuid in uuids:
        found = False
        # check executive summary or guide
        if uuid in content:
            found = True
        if not found:
            with open(os.path.join(path_v15, "01_executive_summary.md"), 'r') as f:
                if uuid in f.read():
                    found = True
        if not found:
            print(f"❌ PDF UUID {uuid} not cited in key artifacts.")
            return False
    print("✅ New Evidence integration verified.")

    # 4. Status Check
    status_path = os.path.join(path_v15, "v15_definitive_status.json")
    with open(status_path, 'r') as f:
        status = json.load(f)
        if status.get("status") == "V15-CONSOLIDATED-COMPLETE":
            print(f"✅ Definitive status active. Convergence: {status.get('convergence_score')}")
        else:
            print("❌ Invalid status.")
            return False

    print("✅ v15.0-SELF-AWARE Definitive Consolidation Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v15_definitive_consolidation():
        sys.exit(0)
    else:
        sys.exit(1)
