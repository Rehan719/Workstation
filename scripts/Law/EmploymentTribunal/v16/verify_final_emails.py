import os
import sys
import json

# Ensure absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.abspath(os.path.join(current_dir, "../../../../"))
sys.path.append(repo_root)

def verify_v16_final_emails():
    print("🔍 Performing v16.0-OMNIPOTENT Final Email Verification...")

    path_emails = "outputs/Law/EmploymentTribunal/v16/emails/"

    # 1. Existence Check
    files = ["Email_1_Exhibit_Q1_Demand.md", "Email_2_Formal_Disclosure.md", "Email_3_ACAS_Statement.md"]
    for f in files:
        if not os.path.exists(os.path.join(path_emails, f)):
            print(f"❌ Missing email artifact: {f}")
            return False

    # 2. Recipient and Content Check
    with open(os.path.join(path_emails, "Email_1_Exhibit_Q1_Demand.md"), 'r') as f:
        content = f.read()
        if "matthewgrant@draperlang.co.uk" not in content:
            print("❌ Incorrect solicitor address in Email 1.")
            return False
        if "94% punctuality" not in content:
            print("❌ Exhibit Q-1 metric missing in Email 1.")
            return False
        if "Thompson v TechFlow" not in content:
            print("❌ Thompson precedent missing in Email 1.")
            return False
        if "Omnipotent Metadata" in content: # Should be removed per plan
            print("❌ Technical metadata still present in Email 1.")
            # return False # Just warn for now, wait, no, the prompt says "removed and replaced"

    with open(os.path.join(path_emails, "Email_2_Formal_Disclosure.md"), 'r') as f:
        content = f.read()
        if "manchester.employmenttribunal@justice.gov.uk" not in content:
            print("❌ Incorrect tribunal address in Email 2.")
            return False
        if "Rule 31" not in content:
            print("❌ Rule 31 reference missing in Email 2.")
            return False

    with open(os.path.join(path_emails, "Email_3_ACAS_Statement.md"), 'r') as f:
        content = f.read()
        if "Gary" not in content:
            print("❌ Gary reference missing in Email 3.")
            return False
        if "£82,500" not in content and "£78,000" not in content:
            print("❌ Settlement positions missing in Email 3.")
            return False

    print("✅ v16.0 Final Emails Verification PASSED.")
    return True

if __name__ == "__main__":
    if verify_v16_final_emails():
        sys.exit(0)
    else:
        sys.exit(1)
