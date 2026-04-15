import yaml
import asyncio
from vsb_constitutional import DecaVeritasOrchestrator

class CoreScienceIntelligence:
    """Core Science Process Intelligence Phenotype."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})

    async def run(self, input_data: dict):
        # Enhance input with science-specific parameters
        if "queries" not in input_data:
             input_data["queries"] = ["scientific method automation", "reproducibility crisis"]

        # Load science patterns
        from .patterns.science_patterns import SCIENCE_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = SCIENCE_PATTERNS

        return await self.orchestrator.orchestrate_core_process(input_data)
