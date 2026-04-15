import yaml
import asyncio
import argparse
from vsb_constitutional import TruthEngine, DecaVeritasOrchestrator
from vsb_multi_agent import MammouthConstitutionalOrchestrator

class CoreBusinessIntelligence:
    """Core Business Process Intelligence Phenotype v10.0."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # v10.0 Multi-Agent Orchestration
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})
        self.swarm_orchestrator = MammouthConstitutionalOrchestrator(self.config, self.orchestrator.governance)

    async def run(self, input_data: dict):
        # 1. Load business patterns
        from .patterns.business_patterns import BUSINESS_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = BUSINESS_PATTERNS

        # 2. Execute via Super-Agent Swarm
        goal = input_data.get("goal", "Execute core business process intelligence")
        swarm_id = "business-intelligence-swarm"

        swarm_result = await self.swarm_orchestrator.orchestrate_swarm(swarm_id, goal, input_data)

        if swarm_result["status"] == "HALTED":
             return {"error": "Execution halted by policy gate", "reason": swarm_result["reason"]}

        # 3. Finalize via standard Deca-Veritas Orchestrator
        return await self.orchestrator.orchestrate_core_process(input_data)

async def main():
    parser = argparse.ArgumentParser(description="Core Business Intelligence CLI")
    parser.add_argument("--input", required=True, help="Input specification JSON")
    parser.add_argument("--config", default="config/constitutional/domains/core_business.yaml", help="Domain genome YAML")
    args = parser.parse_args()

    # Mock input data
    input_data = {"queries": ["market trends 2026", "competitor analysis"]}

    bi = CoreBusinessIntelligence(args.config)
    result = await bi.run(input_data)
    print(f"Process complete. Proposal ID: {result['proposal']['id']}")
    print(f"Generated outputs: {list(result['outputs'].keys())}")

if __name__ == "__main__":
    asyncio.run(main())
