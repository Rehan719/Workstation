import asyncio
import logging
import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.getcwd())

from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine

async def main():
    logging.basicConfig(level=logging.INFO)
    # Using relative paths for historical analysis
    engine = GrandSynthesisEngine(["docs", "agentic_core", "background_files"])
    await engine.run_synthesis()

if __name__ == "__main__":
    asyncio.run(main())
