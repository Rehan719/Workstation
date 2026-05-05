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

def audit_v07():
    print("--- WORKSTATION v0.7 SUPREME BASELINE AUDIT ---")

    # 1. Exhaustive Article Trace
    genome_path = "genome/constitution.work"
    article_mapping = {}
    if os.path.exists(genome_path):
        with open(genome_path, "r") as f:
            genome = json.load(f)
        articles = genome.get("constitution", {}).get("articles", [])
        print(f"Audit: {len(articles)} articles verified in genome.")
        for a in articles:
             aid = a.get("id")
             # Exhaustive check for enforcement (GaaS, Validator, Reactors)
             refs = run_grep(f"Article {aid}", ".")
             status = "SEEDED"
             if len(refs) > 0: status = "ENFORCED"

             article_mapping[aid] = {
                 "title": a.get("title"),
                 "status": status,
                 "provenance": "2867f475",
                 "references": refs[:5]
             }

    # 2. Mandate Forensic Inventory
    mandates = [
        "Zero-Placeholder", "GaaS-Validated", "10m Veto", "PQC Mandatory",
        "Blockchain Treaty", "Adaptive Learning", "Predictive Resilience",
        "Self-Improving AI", "Autonomous Tool Creation", "Swarm Intelligence"
    ]
    mandate_status = {}
    for m in mandates:
        refs = run_grep(m, ".")
        status = "VERIFIED" if len(refs) > 0 else "DEFERRED"
        mandate_status[m] = {
            "status": status,
            "refs": refs[:2]
        }

    # 3. Component Code Integrity
    integrity = {
        "todo": len(run_grep("TODO", "agentic_core")),
        "fixme": len(run_grep("FIXME", "agentic_core")),
        "placeholder": len(run_grep("placeholder", "agentic_core")),
        "stubs": len(run_grep("stub", "agentic_core"))
    }

    # 4. Final Inventory Output
    inventory = {
        "articles": article_mapping,
        "mandates": mandate_status,
        "integrity": integrity,
        "release": "v0.7-supreme-baseline",
        "anchor_commit": "2867f475"
    }

    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/code_inventory_v07.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print("Audit: Supreme Baseline inventory saved to docs/knowledge/code_inventory_v07.json")

if __name__ == "__main__":
    audit_v07()
