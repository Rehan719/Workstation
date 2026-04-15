import yaml
import asyncio
from vsb_constitutional import DecaVeritasOrchestrator

class CoreScholarshipIntelligence:
    """Core Scholarship Process Intelligence Phenotype."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})

    async def run(self, input_data: dict):
        # Enhance input with scholarship-specific parameters
        if "queries" not in input_data:
             input_data["queries"] = ["literature synthesis", "citation integrity"]

        # Load scholarship patterns
        from .patterns.scholarship_patterns import SCHOLARSHIP_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = SCHOLARSHIP_PATTERNS

        return await self.orchestrator.orchestrate_core_process(input_data)
