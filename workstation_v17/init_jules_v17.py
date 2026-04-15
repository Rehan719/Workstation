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
    logger.info("Initializing JULES v17.0 Production Beta Organism...")

    organism = JulesOmegaOrganismV17()
    await organism.initialize()

    recirculation = FractalRecirculation(organism)

    if args.dry_run:
        logger.info("Dry run: Executing one Macro cycle and shutting down.")
        await organism.run_macro_cycle({"dry_run": True})
        await organism.shutdown()
        return

    # Shutdown handlers
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
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--deploy", type=str, default="beta")
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except (KeyboardInterrupt, SystemExit):
        logger.info("Received exit signal.")
