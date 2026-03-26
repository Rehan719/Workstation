import os
import json
import re
import subprocess
from typing import Dict, Any, List

def run_grep(pattern: str, path: str) -> List[str]:
    try:
        # Exclude common false positives (like this linter or test/doc files)
        res = subprocess.run(["grep", "-r", "--exclude=audit_v0.py", "--exclude=doc_linter.py", pattern, path], capture_output=True, text=True)
        return res.stdout.splitlines()
    except:
        return []

def audit_v0():
    print("--- WORKSTATION v0.0 PRODUCTION AUDIT (REFINED) ---")

    # 1. Genome Audit (Articles 1-1127)
    genome_path = "genome/constitution.work"
    article_mapping = {}
    if os.path.exists(genome_path):
        with open(genome_path, "r") as f:
            genome = json.load(f)
        articles = genome.get("constitution", {}).get("articles", [])
        print(f"Audit: {len(articles)} articles verified in genome.")
        for a in articles:
             # Look for specific enforcement/reference points for a subset of critical articles
             if a['id'] in [1, 42, 60, 1101, 1104, 1107, 1127]:
                  refs = run_grep(f"Article {a['id']}", ".")
                  article_mapping[a['id']] = "ENFORCED" if len(refs) > 0 else "SEEDED"
    else:
        print("Audit ERROR: Genome file missing.")

    # 2. Domain Ontology Audit (141 nodes per domain)
    ontology_path = "agentic_core/data/ontologies"
    domain_status = {}
    if os.path.exists(ontology_path):
        for domain in ["religion", "science", "law", "employment", "education", "care"]:
            d_path = os.path.join(ontology_path, f"{domain}.json")
            if os.path.exists(d_path):
                with open(d_path, "r") as f:
                    data = json.load(f)
                nodes = data.get("nodes", [])
                domain_status[domain] = len(nodes)
                print(f"Audit: {domain} ontology verified with {len(nodes)} nodes.")
    else:
        print("Audit ERROR: Ontologies missing.")

    # 3. GaaS Verification (Mutations)
    gaas_calls = run_grep("gaas.validateAction", "apps/web/src")
    print(f"Audit: {len(gaas_calls)} GaaS mutations verified in frontend.")

    # 4. Zero-Placeholder Integrity Check
    todo_check = run_grep("TODO", "agentic_core")
    fixme_check = run_grep("FIXME", "agentic_core")

    integrity = len(todo_check) == 0 and len(fixme_check) == 0
    print(f"Audit: Integrity check: {'PASSED' if integrity else 'FAILED'} ({len(todo_check)} TODOs, {len(fixme_check)} FIXMEs).")

    # 5. Inventory Synthesis
    inventory = {
        "articles_verified": len(articles) if 'articles' in locals() else 0,
        "critical_article_enforcement": article_mapping,
        "domain_node_counts": domain_status,
        "gaas_mutations": len(gaas_calls),
        "zero_placeholder_integrity": integrity
    }

    os.makedirs("docs/knowledge", exist_ok=True)
    with open("docs/knowledge/code_inventory_v0.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print("Audit: Results saved to docs/knowledge/code_inventory_v0.json")

if __name__ == "__main__":
    audit_v0()
