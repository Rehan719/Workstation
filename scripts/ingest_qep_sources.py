import asyncio
import os
import sys
import logging
from agentic_core.synthesis.uviap import UVIAP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting v130.1.0 Ingestion Pipeline...")
    uviap = UVIAP()

    # Run full ingestion modes
    modes = ["ingest-urls", "ingest-local", "rectify-qep-insights", "cognitive", "phylogenetic"]

    try:
        blueprints = await uviap.run_full_pipeline(modes=modes)
        logger.info(f"Ingestion complete. Generated {len(blueprints)} blueprints.")

        # Verify simulated report
        report_path = "docs/knowledge/simulated_sources_v130.md"
        if os.path.exists(report_path):
            logger.info(f"High-fidelity simulation report generated at {report_path}")

    except Exception as e:
        logger.error(f"Ingestion pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
