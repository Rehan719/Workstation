import os
import json

def verify_omnisynthesis():
    path = "outputs/Law/EmploymentTribunal/v12/"
    files_to_check = [
        "FINAL_SUBMISSION_REPORT_v12.0_OMNISYNTHESIS.md",
        "LITIGANT_MASTER_GUIDE_v12.0_OMNISYNTHESIS.md",
        "manifest.json"
    ]

    print("🔍 Verifying v12.0-OMNISYNTHESIS Deployment...")

    missing = []
    for f in files_to_check:
        if not os.path.exists(os.path.join(path, f)):
            missing.append(f)

    if missing:
        print(f"❌ Missing critical files: {missing}")
        return False

    # Check for templates in Master Guide
    with open(os.path.join(path, "LITIGANT_MASTER_GUIDE_v12.0_OMNISYNTHESIS.md"), 'r') as f:
        content = f.read()
        if "Template 1" in content and "Template 2" in content and "Template 3" in content:
            print("✅ Templates detected in Master Guide.")
        else:
            print("❌ Templates missing from Master Guide.")
            return False

    print("✅ v12.0-OMNISYNTHESIS Verification PASSED.")
    return True

if __name__ == "__main__":
    verify_omnisynthesis()
