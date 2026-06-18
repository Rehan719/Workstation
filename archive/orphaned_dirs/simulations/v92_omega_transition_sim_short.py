import asyncio
import logging
from agentic_core import ConsciousOrganismOrchestrator

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def run_simulation():
    logger.info("INITIATING SHORT PROJECT OMEGA SIMULATION")
    organism = ConsciousOrganismOrchestrator()
    await organism.start()

    for i in range(3):
        result = await organism.run_omega_cycle(user_intent="TEST")
        logger.info(f"Pulse {i+1}: Action={result['action_executed']}, Fidelity={result['fidelity']:.3f}")

    await organism.shutdown()
    logger.info("SHORT SIMULATION COMPLETE")

if __name__ == "__main__":
    asyncio.run(run_simulation())
