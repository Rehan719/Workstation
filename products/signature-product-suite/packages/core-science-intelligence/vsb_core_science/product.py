import yaml
import asyncio
from vsb_constitutional import DecaVeritasOrchestrator
from vsb_multi_agent import MammouthConstitutionalOrchestrator

class CoreScienceIntelligence:
    """Core Science Process Intelligence Phenotype v10.0."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})
        self.swarm_orchestrator = MammouthConstitutionalOrchestrator(self.config, self.orchestrator.governance)

    async def run(self, input_data: dict):
        # Enhance input with science-specific parameters
        if "queries" not in input_data:
             input_data["queries"] = ["scientific method automation", "reproducibility crisis"]

        # Load science patterns
        from .patterns.science_patterns import SCIENCE_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = SCIENCE_PATTERNS

        # Execute via Super-Agent Swarm
        goal = input_data.get("goal", "Execute core science process intelligence")
        swarm_id = "science-intelligence-swarm"
        swarm_result = await self.swarm_orchestrator.orchestrate_swarm(swarm_id, goal, input_data)

        if swarm_result["status"] == "HALTED":
             return {"error": "Execution halted by policy gate", "reason": swarm_result["reason"]}

        return await self.orchestrator.orchestrate_core_process(input_data)
