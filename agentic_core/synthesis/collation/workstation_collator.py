import os
import re
import logging
from typing import Dict, Any, List
from agentic_core.synthesis.collation.base_collator import BaseCollator

logger = logging.getLogger(__name__)

class WorkstationCollator(BaseCollator):
    """v101.0: Extracts versions and variations with confidence scoring."""
    def __init__(self):
        self.version_pattern = re.compile(r"v(\d+\.\d+\.?\d*)")
        self.variation_keywords = {
            "alpha": 0.5, "beta": 0.7, "stable": 1.0,
            "experimental": 0.3, "patch": 0.9, "variant": 0.6
        }

    async def collate(self, source_dir: str) -> Dict[str, Any]:
        logger.info(f"QMS: Running Collation for {source_dir}")
        results = {"versions": [], "variations": [], "source": source_dir, "confidence_avg": 0.0}

        confidences = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".txt") or file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()
                        versions = self.version_pattern.findall(content)
                        results["versions"].extend(list(set(versions)))

                        for kw, conf in self.variation_keywords.items():
                            if kw in file.lower() or kw in content.lower():
                                results["variations"].append({"file": file, "tag": kw, "confidence": conf})
                                confidences.append(conf)

        results["versions"] = sorted(list(set(results["versions"])))
        if confidences:
            results["confidence_avg"] = sum(confidences) / len(confidences)

        return results
