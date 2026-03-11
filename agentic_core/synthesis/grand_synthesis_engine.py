import asyncio
import logging
from typing import List, Dict, Any
import os
import sys
import json

# Ensure parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentic_core.synthesis.historical_analyzer import HistoricalAnalyzer
from agentic_core.synthesis.conflict_resolver import ConflictResolver
from agentic_core.synthesis.pattern_extractor import PatternExtractor
from agentic_core.synthesis.dna_generator import DNAGenerator
from agentic_core.synthesis.evolutionary_memory import EvolutionaryMemory

logger = logging.getLogger(__name__)

class GrandSynthesisEngine:
    """
    ARTICLE 73: The Grand Synthesis Engine.
    Analyzes and consolidates 100 generations of evolution into Apotheosis.
    """
    def __init__(self, history_paths: List[str] = None):
        if history_paths is None:
            history_paths = ["sources/background", "docs/historical/background"]
        self.history_paths = history_paths
        self.analyzer = HistoricalAnalyzer(self.history_paths)
        self.resolver = ConflictResolver()
        self.extractor = PatternExtractor()
        self.dna_gen = DNAGenerator()
        self.memory = EvolutionaryMemory()
        self.is_synthesized = False

    async def run_synthesis(self, output_path: str = "meta/synthesis_v100.json"):
        """Executes the full v100.x grand synthesis cycle (APOTHEOSIS)."""
        logger.info("Starting v100.x Grand Synthesis Cycle (APOTHEOSIS)...")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # CN-I. Comprehensive Historical Analysis (v1-v100)
        raw_insights = await self.analyzer.analyze_all()
        logger.info(f"Analyzed {len(raw_insights)} historical and research artifacts.")

        if not raw_insights:
            logger.warning(f"No historical insights found during analysis in {self.history_paths}")

        # CN-III. Optimal Pattern Extraction
        patterns = self.extractor.extract_patterns(raw_insights)
        logger.info(f"Extracted {len(patterns)} architectural patterns.")

        # CN-II. Conflict Resolution
        resolved_config = self.resolver.resolve_conflicts(patterns)
        # Force v100.1 version for this cycle
        resolved_config["version"] = "100.1.0"
        resolved_config["patterns"] = patterns

        # Save synthesis results
        with open(output_path, 'w') as f:
            json.dump(resolved_config, f, indent=4)
        logger.info(f"Synthesis results saved to {output_path}")

        # CN-V. Evolutionary Memory Storage
        self.memory.store_synthesis_results(resolved_config)

        self.is_synthesized = True
        logger.info("v100.x Grand Synthesis complete. APOTHEOSIS baseline established.")
        return resolved_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = GrandSynthesisEngine(["docs/historical/background"])
    asyncio.run(engine.run_synthesis())
