import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v16_implementation_cycle():
    print("🔍 Performing v16.0-OMNIPOTENT Implementation Cycle Verification...")

    path_v16 = "outputs/Law/EmploymentTribunal/v16/"

    # 1. Milestone Status Verification
    phases = ["phase1", "phase2", "phase3"]
    for phase in phases:
        status_file = os.path.join(path_v16, f"v16_implementation_cycle_{phase}_status.json")
        if not os.path.exists(status_file):
            print(f"❌ Status file for {phase} missing.")
            return False
        with open(status_file, 'r') as f:
            status = json.load(f)
            if status.get("convergence_score") < 0.95:
                print(f"❌ Convergence score too low in {phase}: {status.get('convergence_score')}")
                return False

    # 2. Artifact Content Verification
    guide_path = os.path.join(path_v16, "LITIGANT_MASTER_GUIDE_v16.0_OMNIPOTENT.md")
    with open(guide_path, 'r') as f:
        content = f.read()
        if "BSTS-based impact attribution" not in content:
            print("❌ BSTS attribution missing from Master Guide.")
            return False
        if "STL verification confirms" not in content:
            print("❌ STL verification text missing from Master Guide.")
            return False

    # 3. Component Presence
    required_scripts = [
        "causal_disclosure_engine.py",
        "sovereign_realm_core.py",
        "causal_synthesis_engine.py",
        "third_party_audit_interface.py",
        "emergent_capability_discovery.py",
        "final_integrator_v16.py"
    ]
    for script in required_scripts:
        if not os.path.exists(os.path.join("scripts/Law/EmploymentTribunal/v16/", script)):
            print(f"❌ Required script missing: {script}")
            return False

    print("✅ v16.0-OMNIPOTENT Implementation Cycle Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v16_implementation_cycle():
        sys.exit(0)
    else:
        sys.exit(1)
