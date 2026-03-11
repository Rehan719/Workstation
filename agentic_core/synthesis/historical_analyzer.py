import os
import glob
import logging
import re
import json
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

ENGINE_PATTERNS = {
    'twinning': [
        'digital twin', 'incubator', 'environmental simulation', 'twin fidelity',
        'shadow system', 'twin lifecycle', 'reactor twin'
    ],
    'aro': [
        'adaptive resource', 'resource allocation', 'cost-aware', 'demand prediction',
        'LSTM', 'Prophet', 'priority tier', 'resource monitor'
    ],
    'bto': [
        'biomimetic team', 'agent negotiation', 'task force', 'emergent collaboration',
        'collective memory', 'role negotiation', 'swarm intelligence', 'team health'
    ],
    'drad': [
        'dynamic assembly', 'resource fabric', 'composable', 'zero-waste',
        'ephemeral pool', 'Resource Assembly Language', 'disassembly', 'scale-up'
    ],
    'platforms': [
        'Hugging Face', 'GitHub', 'OpenAI', 'Vercel', 'Render', 'API Gateway',
        'External Resource', 'Cloud service'
    ]
}

class HistoricalAnalyzer:
    """Analyzes historical documentation, code patterns, and telemetry for active meta-evolution."""
    def __init__(self, paths: List[str]):
        self.paths = paths
        self.version_pattern = re.compile(r"v(\d+\.\d+)")

    async def analyze_all(self) -> List[Dict[str, Any]]:
        """CN-I: Comprehensive Historical Analysis including Telemetry."""
        insights = []
        files_to_analyze = []
        for path in self.paths:
            logger.info(f"Scanning path: {path}")
            # Recursively find all documentation and source code
            files_to_analyze.extend(glob.glob(os.path.join(path, "**/*.txt"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "agentic_core/**/*.py"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "meta/**/*.md"), recursive=True))
            files_to_analyze.extend(glob.glob(os.path.join(path, "docs/**/*.md"), recursive=True))

        # Include telemetry logs if available
        telemetry_logs = glob.glob("meta/*.log")
        files_to_analyze.extend(telemetry_logs)

        logger.info(f"Found {len(files_to_analyze)} files/logs to analyze.")
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

            # Extract engine associations and parameters
            engines = []
            extracted_params = {}
            for engine, keywords in ENGINE_PATTERNS.items():
                if any(kw.lower() in content.lower() for kw in keywords):
                    engines.append(engine)
                    # Simple parameter extraction (e.g., "fidelity >= 95%")
                    if engine == 'twinning':
                        match = re.search(r"fidelity\s*[>=]+\s*(\d+)%", content, re.I)
                        if match: extracted_params['fidelity_target'] = int(match.group(1)) / 100.0

            # Telemetry extraction
            if filepath.endswith(".log"):
                if "waste" in content.lower():
                    match = re.search(r"waste[:\s]*(\d+\.?\d*)%", content, re.I)
                    if match: extracted_params['observed_waste'] = float(match.group(1)) / 100.0

            return {
                "source": filepath,
                "type": self._determine_type(filepath),
                "length": len(content),
                "versions": list(set(versions)),
                "key_terms": self._extract_key_terms(content),
                "engines": engines,
                "extracted_params": extracted_params,
                "domain": self._determine_domain(filepath)
            }
        except Exception as e:
            logger.error(f"Failed to analyze {filepath}: {e}")
            return {}

    def _determine_type(self, filepath: str) -> str:
        if filepath.endswith(".py"): return "code"
        if filepath.endswith(".log"): return "telemetry"
        return "doc"

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
