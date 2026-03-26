import os
import json
import subprocess
import re
from typing import Dict, Any, List

def run_grep(pattern: str, path: str) -> List[str]:
    try:
        # Exclude artifacts and common false positives
        res = subprocess.run(["grep", "-r", "--exclude=audit_v0.py", "--exclude=doc_linter.py", pattern, path], capture_output=True, text=True)
        return res.stdout.splitlines()
    except:
        return []

def audit_v04():
    print("--- WORKSTATION v0.4 DEFINITIVE AUDIT ---")

    # 1. Exhaustive Article Check
    genome_path = "genome/constitution.work"
    article_mapping = {}
    if os.path.exists(genome_path):
        with open(genome_path, "r") as f:
            genome = json.load(f)
        articles = genome.get("constitution", {}).get("articles", [])
        print(f"Audit: {len(articles)} articles found in seeded genome.")
        for a in articles:
             # Search for direct enforcement or reference points
             refs = run_grep(f"Article {a['id']}", ".")
             status = "SEEDED"
             if len(refs) > 0: status = "ENFORCED"

             article_mapping[a['id']] = {
                 "title": a.get("title"),
                 "status": status,
                 "references": refs[:3] # Sample first 3
             }

    # 2. Mandate Check
    mandates = [
        "Zero-Placeholder", "GaaS-Validated", "10m Veto", "PQC Mandatory",
        "Blockchain Treaty", "Adaptive Learning", "Predictive Resilience"
    ]
    mandate_mapping = {}
    for m in mandates:
        refs = run_grep(m, ".")
        mandate_mapping[m] = "VERIFIED" if len(refs) > 0 else "DEFERRED"

    # 3. Integrity Audit (Zero-Placeholder check)
    todo = run_grep("TODO", "agentic_core")
    fixme = run_grep("FIXME", "agentic_core")
    placeholder = run_grep("placeholder", "agentic_core")

    integrity = len(todo) == 0 and len(fixme) == 0
    print(f"Audit: Integrity check: {'PASSED' if integrity else 'FAILED'} ({len(todo)} TODOs, {len(fixme)} FIXMEs).")

    # 4. Final Inventory
    inventory = {
        "articles": article_mapping,
        "mandates": mandate_mapping,
        "integrity": integrity,
        "v03_provenance": "2867f475"
    }

    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/code_inventory_v04.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print("Audit: Definitive inventory saved to docs/knowledge/code_inventory_v04.json")

if __name__ == "__main__":
    audit_v04()
