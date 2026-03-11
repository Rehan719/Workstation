import os
import re
import logging
from typing import Dict, Any, List
from .base_collator import BaseCollator

logger = logging.getLogger(__name__)

class WorkstationCollator(BaseCollator):
    """v100.1: Extracts versions and variations from Workstation artifacts."""
    def __init__(self):
        self.version_pattern = re.compile(r"v(\d+\.\d+\.?\d*)")
        self.variation_keywords = ["alpha", "beta", "experimental", "patch", "variant"]

    async def collate(self, source_dir: str) -> Dict[str, Any]:
        logger.info(f"WorkstationCollator: Scanning {source_dir}")
        results = {"versions": [], "variations": [], "source": source_dir}

        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".txt") or file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()
                        versions = self.version_pattern.findall(content)
                        results["versions"].extend(list(set(versions)))

                        for kw in self.variation_keywords:
                            if kw in file.lower() or kw in content.lower():
                                results["variations"].append({"file": file, "tag": kw})

        results["versions"] = sorted(list(set(results["versions"])))
        return results
