import argparse
import asyncio
import logging
import signal
import sys
from workstation_v17.core.jules_omega_organism_v17 import JulesOmegaOrganismV17
from workstation_v17.core.fractal_recirculation import FractalRecirculation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("InitJulesV17")

async def main(args):
    logger.info("Starting Workstation Sovereign Digital Organism v17.0...")

    organism = JulesOmegaOrganismV17()
    await organism.initialize()

    recirculation = FractalRecirculation(organism)

    if args.dry_run:
        logger.info("Dry run mode: Executing one cycle then exiting.")
        await organism.run_cycle()
        await organism.shutdown()
        return

    # Graceful shutdown handling
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(organism.shutdown()))

    try:
        await recirculation.start()
    except asyncio.CancelledError:
        logger.info("Organism task cancelled.")
    finally:
        await organism.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jules v17.0 Initializer")
    parser.add_argument("--dry-run", action="store_true", help="Run one cycle and exit")
    parser.add_argument("--role", type=str, default="opus_director")
    parser.add_argument("--vertical", type=str, default="biotech_materials")

    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received.")
