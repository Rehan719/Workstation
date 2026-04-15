import yaml
import asyncio
from vsb_constitutional import DecaVeritasOrchestrator
from vsb_multi_agent import MammouthConstitutionalOrchestrator

class CoreScholarshipIntelligence:
    """Core Scholarship Process Intelligence Phenotype v10.0."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})
        self.swarm_orchestrator = MammouthConstitutionalOrchestrator(self.config, self.orchestrator.governance)

    async def run(self, input_data: dict):
        # Enhance input with scholarship-specific parameters
        if "queries" not in input_data:
             input_data["queries"] = ["literature synthesis", "citation integrity"]

        # Load scholarship patterns
        from .patterns.scholarship_patterns import SCHOLARSHIP_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = SCHOLARSHIP_PATTERNS

        # Execute via Super-Agent Swarm
        goal = input_data.get("goal", "Execute core scholarship process intelligence")
        swarm_id = "scholarship-intelligence-swarm"
        swarm_result = await self.swarm_orchestrator.orchestrate_swarm(swarm_id, goal, input_data)

        if swarm_result["status"] == "HALTED":
             return {"error": "Execution halted by policy gate", "reason": swarm_result["reason"]}

        return await self.orchestrator.orchestrate_core_process(input_data)
