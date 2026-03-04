import os
import glob
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class HistoricalAnalyzer:
    """Analyzes historical documentation and code patterns for v92.0."""
    def __init__(self, paths: List[str]):
        self.paths = paths
        self.version_pattern = re.compile(r"v(\d+\.\d+)")

    async def analyze_all(self) -> List[Dict[str, Any]]:
        """CN-I: Comprehensive Historical Analysis for v1-v92."""
        insights = []
        files_to_analyze = []
        for path in self.paths:
            files_to_analyze.extend(glob.glob(os.path.join(path, "**/*.txt"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "agentic_core/**/*.py"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "meta/**/*.md"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "docs/**/*.md"), recursive=True))

        for filepath in files_to_analyze:
            if os.path.isfile(filepath):
                insight = self._analyze_file(filepath)
                if insight:
                    insights.append(insight)

        return insights

    def _analyze_file(self, filepath: str) -> Dict[str, Any]:
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()

            versions = self.version_pattern.findall(content)

            return {
                "source": filepath,
                "type": "code" if filepath.endswith(".py") else "doc",
                "length": len(content),
                "versions": list(set(versions)),
                "key_terms": self._extract_key_terms(content)
            }
        except Exception as e:
            logger.error(f"Failed to analyze {filepath}: {e}")
            return {}

    def _extract_key_terms(self, content: str) -> List[str]:
        terms = [
            "Quantum", "Neuro-Symbolic", "Verification", "Blockchain", "UEG",
            "Immune", "Nervous", "Minimax", "Qwen", "Retro-Causal",
            "Balanced Foundationalism", "Graduated Transition", "Rollback",
            "CRDT", "Y.js", "Framework Router", "ScholarlyObject", "Sigstore",
            "Recursive Prompt", "Universal Provenance", "Behavior-Driven",
            "Transcendent", "POLYMATH"
        ]
        return [t for t in terms if t.lower() in content.lower()]
