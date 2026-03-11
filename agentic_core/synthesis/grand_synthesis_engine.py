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
from .url_ingestor import URLIngestor
from .documentation_generator import DocumentationGenerator

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
        self.ingestor = URLIngestor()
        self.doc_gen = DocumentationGenerator()
        self.is_synthesized = False

    def _get_url_list(self) -> List[str]:
        """Retrieves the list of URLs for ingestion."""
        return [
            "https://agent.minimax.io/share/375389193781515?chat_type=2",
            "https://chat.qwen.ai/s/2066eeac-6fb0-4209-8854-72e35212d4c7?fev=0.2.12",
            "https://chat.deepseek.com/share/ru5rr1j9bljzx4goer",
            "https://chat.deepseek.com/share/sfbnb1lq4ag5a86vbd",
            "https://chat.deepseek.com/share/ze6lm6it7tyae6ktpg",
            "https://chat.deepseek.com/share/a1n9r454ydkw9w6xbw",
            "https://chat.deepseek.com/share/0gtpohpctv3e36itep",
            "https://chat.deepseek.com/share/r3xt3bk45x67aieslg",
            "https://chat.deepseek.com/share/asvwahxqw00djlpik7",
            "https://chat.deepseek.com/share/nmt425u55b99vjahmr",
            "https://chat.deepseek.com/share/scgothk1isu5yib7yy",
            "https://chat.deepseek.com/share/uwfc3ew5jusujy4ju6",
            "https://chat.deepseek.com/share/7l5sbd7m12u6tzq7hm",
            "https://chat.deepseek.com/share/ehac1l4bvnn94z6m2t",
            "https://chat.deepseek.com/share/f6z9lz0yvxov1yc14k",
            "https://chat.deepseek.com/share/crunut0z3684jmzhke",
            "https://chat.deepseek.com/share/5hfiqi3ta18416xmsg",
            "https://chat.deepseek.com/share/ts0cajbla50flyvtxr",
            "https://chat.deepseek.com/share/ajpaqyg7rdfu048x5a",
            "https://chat.deepseek.com/share/85405lhv6fz6dmslii",
            "https://chat.deepseek.com/share/63rpvd5uc66rmipilg",
            "https://chat.deepseek.com/share/cnp1ehtoivmieqrgbi",
            "https://chat.deepseek.com/share/j5qn1ng5w46tb3jyqp",
            "https://chat.deepseek.com/share/axny0044p636wl2qs7",
            "https://jules.google.com/task/6690716826982580951",
            "https://jules.google.com/task/8321344421938616475",
            "https://jules.google.com/task/11229942869047369169",
            "https://jules.google.com/task/2012505508984346594",
            "https://jules.google.com/task/11093918825021929606",
            "https://jules.google.com/task/2966620505238613254",
            "https://jules.google.com/task/7374493318076149204",
            "https://jules.google.com/task/15734730789908784640",
            "https://jules.google.com/task/16112838550523477002",
            "https://jules.google.com/task/18302280291944395270",
            "https://jules.google.com/task/16640222564934956138",
            "https://jules.google.com/task/13385116039194951359"
        ]

    async def run_synthesis(self, target_version: str = None):
        """Executes the full grand synthesis cycle."""
        logger.info(f"Starting Grand Synthesis Cycle for {target_version or 'detected version'}...")

        # Mode: Ingest URLs (Article 356)
        ingested_knowledge = []
        if "--ingest-urls" in sys.argv:
            urls = self._get_url_list()
            ingested_knowledge = await self.ingestor.ingest_urls(urls)
            logger.info(f"Ingested knowledge from {len(ingested_knowledge)} URLs.")

        raw_insights = await self.analyzer.analyze_all()
        logger.info(f"Analyzed {len(raw_insights)} historical and research artifacts.")

        # Merge ingested knowledge into insights for pattern extraction
        for item in ingested_knowledge:
            raw_insights.append({
                "source": item["source_url"],
                "type": "external_knowledge",
                "content": item["transcript"],
                "key_terms": ["Ingested", item["platform"]]
            })

        patterns = self.extractor.extract_patterns(raw_insights)
        logger.info(f"Extracted {len(patterns)} architectural patterns.")

        resolved_config = self.resolver.resolve_conflicts(patterns)

        version = target_version or resolved_config.get("version")
        if version == "107.0.0":
            constitution_path = self.dna_gen.generate_v107_constitution(resolved_config)
            logger.info(f"v107.0 Constitution generated at {constitution_path}")
            if "--generate-docs" in sys.argv:
                logger.info("Documentation Generation Mode active for v107.0")
                self.doc_gen.generate_suite(resolved_config)
        elif version == "106.0.0":
            constitution_path = self.dna_gen.generate_v106_constitution(resolved_config)
            logger.info(f"v106.0 Constitution generated at {constitution_path}")
        elif version == "105.0.0":
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
