import yaml
import asyncio
import argparse
from vsb_constitutional import TruthEngine, DecaVeritasOrchestrator

class CoreBusinessIntelligence:
    """Core Business Process Intelligence Phenotype."""
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        # In a real setup, we would load the base_schema and merge
        self.orchestrator = DecaVeritasOrchestrator(self.config, {})

    async def run(self, input_data: dict):
        # Load business patterns
        from .patterns.business_patterns import BUSINESS_PATTERNS
        self.orchestrator.config["jaiza"]["constitutional_pattern_library"]["domain_patterns"] = BUSINESS_PATTERNS

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
