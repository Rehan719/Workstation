import os
import glob
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class HistoricalAnalyzer:
    """Analyzes historical documentation and code patterns."""
    def __init__(self, paths: List[str]):
        self.paths = paths

    async def analyze_all(self) -> List[Dict[str, Any]]:
        """CN-I: Comprehensive Historical Analysis."""
        insights = []
        # Find all background text files, current code, and version maps
        files_to_analyze = []
        for path in self.paths:
            # Recursively find all documentation and source code
            files_to_analyze.extend(glob.glob(os.path.join(path, "**/*.txt"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "agentic_core/**/*.py"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "meta/**/*.md"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "docs/**/*.md"), recursive=True))

        # Explicitly include the version history map
        version_map = "docs/planning/version_history_map.md"
        if os.path.exists(version_map) and version_map not in files_to_analyze:
            files_to_analyze.append(version_map)

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

            # Simulated pattern extraction logic
            return {
                "source": filepath,
                "type": "code" if filepath.endswith(".py") else "doc",
                "length": len(content),
                "key_terms": self._extract_key_terms(content)
            }
        except Exception as e:
            logger.error(f"Failed to analyze {filepath}: {e}")
            return {}

    def _extract_key_terms(self, content: str) -> List[str]:
        # Simple keyword-based extraction for simulation
        terms = ["Quantum", "Neuro-Symbolic", "Verification", "Blockchain", "UEG", "Immune", "Nervous"]
        return [t for t in terms if t.lower() in content.lower()]
