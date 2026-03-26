import os
import json
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BackgroundTextIndexer:
    """
    ARTICLE 357: Knowledge Extraction Pipeline.
    Scans repository for text artifacts and indexes system objectives.
    """
    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        self.extensions = [".md", ".txt", ".yaml", ".json"]
        self.ignore_dirs = ["node_modules", ".git", "dist", "build"]

    def index_all_text(self) -> Dict[str, Any]:
        logger.info("Indexer: Scanning repository for background text...")
        index = {}

        for root, dirs, files in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in self.extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", errors="ignore") as f:
                            content = f.read()
                            index[path] = {
                                "objectives": self._extract_objectives(content),
                                "features": self._extract_features(content),
                                "phases": self._extract_phases(content),
                                "qep_content": self._extract_qep(content)
                            }
                    except Exception as e:
                        logger.error(f"Failed to read {path}: {e}")

        return index

    def _extract_objectives(self, text: str) -> List[str]:
        patterns = [r"Objective:\s*(.*)", r"Goal:\s*(.*)", r"Purpose:\s*(.*)"]
        results = []
        for p in patterns:
            results.extend(re.findall(p, text, re.IGNORECASE))
        return results[:5]

    def _extract_features(self, text: str) -> List[str]:
        # Simple extraction of bullet points under features
        match = re.search(r"##\s*Features(.*?)(?=\n##|$)", text, re.DOTALL | re.IGNORECASE)
        if match:
            return [f.strip("- ").strip() for f in match.group(1).split("\n") if f.strip().startswith("-")]
        return []

    def _extract_phases(self, text: str) -> List[str]:
        return re.findall(r"Phase\s*\d+[:\s]*(.*)", text, re.IGNORECASE)

    def _extract_qep(self, text: str) -> List[str]:
        qep_keywords = ["ESE", "ARO", "BTO", "DRAD", "Pillar", "Quad Engine"]
        return [line.strip() for line in text.split("\n") if any(k in line for k in qep_keywords)]

    def generate_markdown_report(self, index: Dict[str, Any]):
        report = "# WORKSTATION BACKGROUND TEXT INDEX\n\n"
        report += "| File Path | Objectives | Key Features | QEP Alignment |\n"
        report += "|-----------|------------|--------------|---------------|\n"

        for path, data in index.items():
            if data["objectives"] or data["features"] or data["qep_content"]:
                rel_path = os.path.relpath(path, self.root_path)
                obj = ", ".join(data["objectives"][:2])
                feat = ", ".join(data["features"][:2])
                qep = "YES" if data["qep_content"] else "NO"
                report += f"| {rel_path} | {obj} | {feat} | {qep} |\n"

        with open("BACKGROUND_TEXT_INDEX.md", "w") as f:
            f.write(report)
        logger.info("Indexer: BACKGROUND_TEXT_INDEX.md generated.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    indexer = BackgroundTextIndexer()
    data = indexer.index_all_text()
    with open("docs/knowledge/background_text_extracts.json", "w") as f:
        json.dump(data, f, indent=2)
    indexer.generate_markdown_report(data)
