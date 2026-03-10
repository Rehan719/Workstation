import os
import glob
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

ENGINE_PATTERNS = {
    'twinning': ['digital twin', 'incubator', 'environmental simulation', 'twin fidelity', 'shadow system'],
    'aro': ['adaptive resource', 'resource allocation', 'cost-aware', 'demand prediction', 'LSTM', 'Prophet', 'priority tier'],
    'bto': ['biomimetic team', 'agent negotiation', 'task force', 'emergent collaboration', 'collective memory', 'swarm'],
    'drad': ['dynamic assembly', 'resource fabric', 'composable', 'zero-waste', 'ephemeral', 'Resource Assembly Language']
}

class HistoricalAnalyzer:
    """Analyzes historical documentation and code patterns with active engine extraction."""
    def __init__(self, paths: List[str]):
        self.paths = paths
        self.version_pattern = re.compile(r"v(\d+\.\d+)")

    async def analyze_all(self) -> List[Dict[str, Any]]:
        """CN-I: Comprehensive Historical Analysis."""
        insights = []
        files_to_analyze = []
        for path in self.paths:
            # Recursively find all documentation and source code
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

            # Extract engine associations
            engines = []
            for engine, keywords in ENGINE_PATTERNS.items():
                if any(kw.lower() in content.lower() for kw in keywords):
                    engines.append(engine)

            return {
                "source": filepath,
                "type": "code" if filepath.endswith(".py") else "doc",
                "length": len(content),
                "versions": list(set(versions)),
                "key_terms": self._extract_key_terms(content),
                "engines": engines,
                "domain": self._determine_domain(filepath)
            }
        except Exception as e:
            logger.error(f"Failed to analyze {filepath}: {e}")
            return {}

    def _determine_domain(self, filepath: str) -> str:
        if "QEP" in filepath:
            return "qep"
        if "Tools_scripts" in filepath or "scripts" in filepath:
            return "tools"
        return "core"

    def _extract_key_terms(self, content: str) -> List[str]:
        terms = [
            "Quantum", "Neuro-Symbolic", "Verification", "Blockchain", "UEG",
            "Immune", "Nervous", "Minimax", "Qwen", "Retro-Causal",
            "Balanced Foundationalism", "Graduated Transition", "Rollback",
            "CRDT", "Y.js", "Framework Router", "ScholarlyObject", "Sigstore",
            "Recursive Prompt", "Universal Provenance", "Behavior-Driven",
            "Transcendent", "POLYMATH"
        ]
        # Add engine keywords to terms
        for keywords in ENGINE_PATTERNS.values():
            terms.extend(keywords)

        return [t for t in terms if t.lower() in content.lower()]
