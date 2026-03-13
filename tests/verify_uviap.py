import asyncio
import logging
from agentic_core.synthesis.uviap import UVIAP

logging.basicConfig(level=logging.INFO)

async def test_uviap_evolution():
    uviap = UVIAP()
    print("Starting UVIAP Full Evolution...")
    blueprints = await uviap.run_full_pipeline()

    print(f"Blueprints Generated: {len(blueprints)}")
    for bp in blueprints:
        print(f" - [{bp['status']}] {bp['target']}: {bp['action']}")

    import os
    if os.path.exists("docs/knowledge/last_uviap_run.json"):
        print("Success: UVIAP Report generated.")
    else:
        print("Error: UVIAP Report missing.")

if __name__ == "__main__":
    asyncio.run(test_uviap_evolution())
