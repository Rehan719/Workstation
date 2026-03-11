import asyncio
import logging
from typing import List, Dict, Any
import os
import sys

# Ensure parent directory is in sys.path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .historical_analyzer import HistoricalAnalyzer
from .conflict_resolver import ConflictResolver
from .pattern_extractor import PatternExtractor
from .dna_generator import DNAGenerator
from .pattern_recognizer import PatternRecognizer
from .evolutionary_memory import EvolutionaryMemory

logger = logging.getLogger(__name__)

class GrandSynthesisEngine:
    """
    ARTICLE 73: The Grand Synthesis Engine.
    Analyzes and consolidates ninety-nine generations of evolution.
    """
    def __init__(self, history_paths: List[str] = None):
        if history_paths is None:
            history_paths = ["."]
        self.analyzer = HistoricalAnalyzer(history_paths)
        self.resolver = ConflictResolver()
        self.recognizer = PatternRecognizer()
        self.extractor = PatternExtractor()
        self.dna_gen = DNAGenerator()
        self.memory = EvolutionaryMemory()
        self.is_synthesized = False

    async def run_synthesis(self, target_version: str = None):
        """Executes the full grand synthesis cycle."""
        logger.info(f"Starting Grand Synthesis Cycle for {target_version or 'detected version'}...")

        raw_insights = await self.analyzer.analyze_all()
        logger.info(f"Analyzed {len(raw_insights)} historical and research artifacts.")

        patterns = self.extractor.extract_patterns(raw_insights)
        logger.info(f"Extracted {len(patterns)} architectural patterns.")

        resolved_config = self.resolver.resolve_conflicts(patterns)

        version = target_version or resolved_config.get("version")
        if version == "105.0.0":
            constitution_path = self.dna_gen.generate_v105_constitution(resolved_config)
            logger.info(f"v105.0 Constitution generated at {constitution_path}")
        elif version == "104.0.0":
            constitution_path = self.dna_gen.generate_v104_constitution(resolved_config)
            logger.info(f"v104.0 Constitution generated at {constitution_path}")
        elif version == "103.0.0":
            constitution_path = self.dna_gen.generate_v103_constitution(resolved_config)
            logger.info(f"v103.0 Constitution generated at {constitution_path}")
        elif version == "101.0.0":
            constitution_path = self.dna_gen.generate_v101_constitution(resolved_config)
            logger.info(f"v101.0 Constitution generated at {constitution_path}")
        else:
            constitution_path = self.dna_gen.generate_v99_constitution(resolved_config)
            logger.info(f"v99.0 Constitution generated at {constitution_path}")

        self.memory.store_synthesis_results(resolved_config)
        self.is_synthesized = True
        logger.info("Grand Synthesis complete.")
        return resolved_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = GrandSynthesisEngine(["."])
    asyncio.run(engine.run_synthesis())
