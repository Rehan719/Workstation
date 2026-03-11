import os
import re
import logging
from typing import Dict, Any, List
from agentic_core.synthesis.collation.base_collator import BaseCollator

logger = logging.getLogger(__name__)

class WorkstationCollator(BaseCollator):
    """v100.1: Enhanced Workstation Collator with incremental update logic."""
    def __init__(self):
        self.version_pattern = re.compile(r"v(\d+\.\d+\.?\d*)")
        self.variation_keywords = {
            "alpha": 0.5, "beta": 0.7, "stable": 1.0,
            "experimental": 0.3, "patch": 0.9, "variant": 0.6
        }
        self.indexed_files = set()

    async def collate(self, source_dir: str) -> Dict[str, Any]:
        logger.info(f"QMS: Running Full Collation for {source_dir}")
        return await self._scan_path(source_dir)

    async def incremental_update(self, file_paths: List[str]) -> Dict[str, Any]:
        """QMS: Processes only a subset of changed files."""
        logger.info(f"QMS: Running Incremental Update for {len(file_paths)} files.")
        return await self._scan_files(file_paths)

    async def _scan_path(self, source_dir: str) -> Dict[str, Any]:
        files_to_scan = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".txt") or file.endswith(".py"):
                    files_to_scan.append(os.path.join(root, file))
        return await self._scan_files(files_to_scan)

    async def _scan_files(self, file_paths: List[str]) -> Dict[str, Any]:
        results = {"versions": [], "variations": [], "confidence_avg": 0.0}
        confidences = []

        for path in file_paths:
            if not os.path.exists(path): continue
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
                versions = self.version_pattern.findall(content)
                results["versions"].extend(list(set(versions)))

                filename = os.path.basename(path)
                for kw, conf in self.variation_keywords.items():
                    if kw in filename.lower() or kw in content.lower():
                        results["variations"].append({"file": filename, "tag": kw, "confidence": conf})
                        confidences.append(conf)
            self.indexed_files.add(path)

        results["versions"] = sorted(list(set(results["versions"])))
        if confidences:
            results["confidence_avg"] = sum(confidences) / len(confidences)

        return results
