import asyncio
import logging
from typing import List, Dict, Any
from .historical_analyzer import HistoricalAnalyzer
from .conflict_resolver import ConflictResolver
from .pattern_extractor import PatternExtractor
from .dna_generator import DNAGenerator
from .evolutionary_memory import EvolutionaryMemory

logger = logging.getLogger(__name__)

class GrandSynthesisEngine:
    """
    ARTICLE CN: The Grand Synthesis Engine.
    Analyzes and consolidates all elements from versions v1-v60.
    """
    def __init__(self, history_paths: List[str]):
        self.analyzer = HistoricalAnalyzer(history_paths)
        self.resolver = ConflictResolver()
        self.extractor = PatternExtractor()
        self.dna_gen = DNAGenerator()
        self.memory = EvolutionaryMemory()
        self.is_synthesized = False

    async def run_synthesis(self):
        """Executes the full grand synthesis cycle (CN-I to CN-V)."""
        logger.info("CN: Starting Grand Synthesis Cycle...")

        # CN-I. Comprehensive Historical Analysis
        raw_insights = await self.analyzer.analyze_all()
        logger.info(f"CN-I: Analyzed {len(raw_insights)} historical artifacts.")

        # CN-III. Optimal Pattern Extraction
        patterns = self.extractor.extract_patterns(raw_insights)
        logger.info(f"CN-III: Extracted {len(patterns)} optimal architectural patterns.")

        # CN-II. Conflict Resolution via Contextual Evaluation
        resolved_config = self.resolver.resolve_conflicts(patterns)
        logger.info("CN-II: Conflicts resolved via contextual evaluation.")

        # CN-IV. Immutable DNA Generation
        constitution_path = self.dna_gen.generate_v60_constitution(resolved_config)
        logger.info(f"CN-IV: v60.0 Constitution generated at {constitution_path}")

        # CN-V. Evolutionary Memory Storage
        self.memory.store_synthesis_results(resolved_config)
        logger.info("CN-V: Synthesis insights stored in UEG.")

        self.is_synthesized = True
        logger.info("Grand Synthesis complete. Immutable DNA established.")
        return resolved_config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    engine = GrandSynthesisEngine(["."])
    asyncio.run(engine.run_synthesis())
