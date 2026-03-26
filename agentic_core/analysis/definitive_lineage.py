import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DefinitiveLineageBuilder:
    """
    ULTIMATE VERSION SYNTHESIS v2.0.
    Reconciles external milestones and internal Git commits into the canonical record.
    """
    def __init__(self):
        self.master_data = "docs/knowledge/forensic_master/civilization_master.json"
        self.commit_data = "docs/knowledge/commit_analysis_exhaustive.json"

    def build(self):
        logger.info("Lineage: Assembling definitive timeline...")

        with open(self.master_data, "r") as f:
            master = json.load(f)
        with open(self.commit_data, "r") as f:
            commits = json.load(f)

        content = "# WORKSTATION DEFINITIVE VERSION LINEAGE\n\n"
        content += "## 🧬 The Evolutionary DAG\n\n"
        content += "```mermaid\ngraph TD\n"
        content += "    v0.1[v0.1: Initial Proto-Organism] --> v1.0[v1.0: Foundation]\n"
        content += "    v1.0 --> v99.0[v99.0: Autonomous Base]\n"
        content += "    v99.0 --> v120.0[v120.0: Apotheosis Synthesis]\n"
        content += "    v120.0 --> v125.0[v125.0: QEP Excellence]\n"
        content += "    v125.0 --> v138.0[v138.0: Galactic Era]\n"
        content += "    v138.0 --> Main0[Main 0.0: Canonical Baseline]\n"

        # Branch Visualization
        content += "    subgraph \"Development Branches\"\n"
        for c in commits[:5]:
            content += f"        {c['hash'][:8]}[Commit: {c['hash'][:8]}] --> Main0\n"
        content += "    end\n"
        content += "```\n\n"

        content += "## 📜 The Chronological Archive (v1.0 - v1000.0+)\n\n"
        content += "| Milestones | Attributes | Features Introduced | Provenance |\n"
        content += "|------------|------------|-------------------|------------|\n"

        # Versions from Master
        for ver, data in master["versions"].items():
            content += f"| {ver} | Milestone | {', '.join(data['features'][:2])} | External URL |\n"

        # Commits from Audit
        for c in commits:
            content += f"| {c['hash'][:8]} | {c['intent']} | {c['message'][:60]} | {c['branches'][0] if c['branches'] else 'Main'} |\n"

        with open("VERSION_LINEAGE_FINAL.md", "w") as f:
            f.write(content)

        logger.info("Lineage: VERSION_LINEAGE_FINAL.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    builder = DefinitiveLineageBuilder()
    builder.build()
