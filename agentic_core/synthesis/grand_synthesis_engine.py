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
    Analyzes and consolidates 100+ generations of evolution into self-aware organisms.
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

    async def run_synthesis(self):
        """Executes the full grand synthesis cycle."""
        logger.info("Starting Grand Synthesis Cycle...")

    async def run_synthesis(self, output_path: str = "meta/synthesis_v101.json", introspect: bool = False):
        """Executes the full grand synthesis cycle with optional introspection (v101.0)."""
        mode_label = "INTROSPECTIVE" if introspect else "APOTHEOSIS"
        logger.info(f"Starting v101.x Grand Synthesis Cycle ({mode_label})...")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # CN-I. Historical & Telemetry Analysis
        raw_insights = await self.analyzer.analyze_all()
        logger.info(f"Analyzed {len(raw_insights)} artifacts and telemetry nodes.")

        patterns = self.extractor.extract_patterns(raw_insights)

        # v101.0 Meta-Cognitive Logic
        if introspect:
            logger.info("GSE: Performing deep self-analysis of pipeline telemetry.")
            patterns.append({"id": "meta_cognitive_loop", "confidence": 1.0, "article": 327})

        resolved_config = self.resolver.resolve_conflicts(patterns)

        version = resolved_config.get("version")
        if version == "103.0.0":
            constitution_path = self.dna_gen.generate_v103_constitution(resolved_config)
            logger.info(f"v103.0 Constitution generated at {constitution_path}")
        elif version == "101.0.0":
            constitution_path = self.dna_gen.generate_v101_constitution(resolved_config)
            logger.info(f"v101.0 Constitution generated at {constitution_path}")
        else:
            constitution_path = self.dna_gen.generate_v99_constitution(resolved_config)
            logger.info(f"v99.0 Constitution generated at {constitution_path}")
        resolved_config["version"] = "101.0.0" if introspect else "100.1.0"
        resolved_config["patterns"] = patterns
        resolved_config["mode"] = mode_label

        # Save synthesis results
        with open(output_path, 'w') as f:
            json.dump(resolved_config, f, indent=4)
        logger.info(f"Synthesis results saved to {output_path}")

        self.memory.store_synthesis_results(resolved_config)
        self.is_synthesized = True
        logger.info("Grand Synthesis complete.")
        logger.info(f"v101.x Grand Synthesis complete. {mode_label} baseline established.")
        return resolved_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Default to introspective run if called as main
    engine = GrandSynthesisEngine(["docs/historical/background"])
    asyncio.run(engine.run_synthesis(introspect=True))
