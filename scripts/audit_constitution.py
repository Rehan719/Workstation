import os
import re

def audit_constitution():
    constitution_path = "CONSTITUTION_v99.0.0.md"
    with open(constitution_path, "r") as f:
        content = f.read()

    articles = re.findall(r"ARTICLE (\d+):", content)
    total_articles = len(articles)

    print(f"--- CONSTITUTIONAL AUDIT v99.0 ---")
    print(f"Total Codified Articles: {total_articles}")

    # Check for specific critical articles
    mandatory = ["47", "60", "150", "236", "237", "247", "280", "297"]
    for art in mandatory:
        if art in articles:
            print(f"✅ Article {art} is codified.")
        else:
            print(f"❌ Article {art} is MISSING!")

    # Check for No-Stubs adherence (informational)
    stubs = os.popen('grep -r "NotImplementedError" agentic_core/ src/').read()
    if not stubs:
        print("✅ Article 60: No-Stubs compliance verified in core logic.")
    else:
        print("⚠️ Article 60: Stubs detected!")

    print("Audit Complete.")

if __name__ == "__main__":
    audit_constitution()
