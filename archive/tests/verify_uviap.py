import asyncio
import logging
import os
from agentic_core.synthesis.uviap import UVIAP

logging.basicConfig(level=logging.INFO)

async def test_uviap_evolution():
    uviap = UVIAP()
    print("Starting UVIAP Full Evolution...")
    blueprints = await uviap.run_full_pipeline()

    print(f"Blueprints Generated: {len(blueprints)}")
    for bp in blueprints:
        # v120.0 blueprints use 'trait' instead of 'target'
        trait = bp.get('trait') or bp.get('target', 'unknown')
        print(f" - [{bp['status']}] {trait}: {bp['action']}")

    if os.path.exists("docs/knowledge/unified_assimilation_v120.json"):
        print("Success: UVIAP Report generated.")
    else:
        print("Error: UVIAP Report missing.")

if __name__ == "__main__":
    asyncio.run(test_uviap_evolution())
