import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LineageBuilder:
    """
    ARTICLE 621: Evolutionary Topology Mapping.
    Synthesizes the complete version lineage from Foundation to vFinal.
    """
    def __init__(self):
        self.master_data = "docs/knowledge/forensic_master/civilization_master.json"
        self.git_data = "docs/knowledge/git_forensic_deep_analysis.json"

    def build_lineage_report(self):
        logger.info("LineageBuilder: Constructing civilizational timeline...")

        with open(self.master_data, "r") as f:
            master = json.load(f)
        with open(self.git_data, "r") as f:
            git_history = json.load(f)

        report = "# WORKSTATION VERSION LINEAGE - vFinal\n\n"
        report += "## 🧬 Civilisational Evolution Tree\n\n"
        report += "```mermaid\ngraph TD\n"
        report += "    v1.0[v1.0: Foundation] --> v99.0[v99.0: Autonomous Base]\n"
        report += "    v99.0 --> v120.0[v120.0: Apotheosis Synthesis]\n"
        report += "    v120.0 --> v125.0[v125.0: QEP Excellence]\n"
        report += "    v125.0 --> v138.0[v138.0: Galactic Era]\n"
        report += "    v138.0 --> vFinal[Main 0.0: Canonical Baseline]\n"
        report += "```\n\n"

        report += "## 📜 Comprehensive Version Log\n\n"
        report += "| Version | Release Note | Key Advancements | Source |\n"
        report += "|---------|--------------|------------------|--------|\n"

        # Merge Git versions and Master versions
        all_versions = sorted(list(set(list(master["versions"].keys()) + [c["inferred_version"] for c in git_history if c["inferred_version"] != "v0.0.0"])))

        for ver in all_versions:
            features = master["versions"].get(ver, {}).get("features", ["System Update"])
            source = master["versions"].get(ver, {}).get("source", "Git History")
            report += f"| {ver} | Synthesis Milestone | {', '.join(features[:3])} | [Source]({source}) |\n"

        with open("VERSION_LINEAGE_FINAL.md", "w") as f:
            f.write(report)

        logger.info("LineageBuilder: VERSION_LINEAGE_FINAL.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    builder = LineageBuilder()
    builder.build_lineage_report()
