import asyncio
import logging
import os
from typing import Dict, Any, List
from agentic_core.synthesis.collation.workstation_collator import WorkstationCollator
from agentic_core.ueg.version_graph import VersionGraph

logger = logging.getLogger(__name__)

class CollationOrchestrator:
    """v101.0: Coordinates category-wise collation and UEG storage."""
    def __init__(self, background_root: str = "docs/historical/background"):
        self.root = background_root
        self.vg = VersionGraph()
        self.collators = {
            "workstation": WorkstationCollator()
        }

    async def run_full_collation(self):
        logger.info("Starting Full v101.0 Collation...")
        unified_results = {}

        for category, collator in self.collators.items():
            source_path = os.path.join(self.root, category.capitalize())
            if not os.path.exists(source_path):
                source_path = self.root # Fallback

            results = await collator.collate(source_path)
            unified_results[category] = results

            # Save to UEG
            for v in results.get("versions", []):
                self.vg.add_version_node(f"{category}:{v}", {"category": category, "v": v})

        # Generate report
        report = "# Master Collation Report v101.0\n\n"
        for cat, res in unified_results.items():
            report += f"## {cat.capitalize()}\n"
            report += f"- Versions: {len(res['versions'])}\n"
            report += f"- Variations: {len(res['variations'])}\n\n"

        os.makedirs("docs/planning", exist_ok=True)
        with open("docs/planning/collation_report_v101.0.md", "w") as f:
            f.write(report)

        logger.info("Collation complete. Report generated.")
        return unified_results
