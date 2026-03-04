import asyncio
import logging
from agentic_core.orchestrator.conscious_organism_v93 import ConsciousOrganismV93_0

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("v93_Simulation")

async def run_v93_simulation():
    logger.info("Initializing POLYMATH v93.0 Organism...")
    organism = ConsciousOrganismV93_0()
    await organism.start()

    # 1. Test Task Execution with Provenance and XAI
    logger.info("TEST 1: Multi-Agent Task Execution (Manuscript Generation)")
    task_data = {"type": "manuscript", "topic": "Next-Gen AI Ethics"}
    user_profile = {"user_id": "architect_01", "expertise": "expert"}

    result = await organism.execute_task(task_data, user_profile)
    logger.info(f"Task Result: Framework={result['framework_used']}")
    logger.info(f"XAI Narrative: {result['explanation']}")

    # 2. Test Polymath Cognitive Cycle
    logger.info("TEST 2: Running v93 Polymath Cognitive Cycle")
    cycle_result = await organism.run_polymath_cycle(user_intent="SYNC_ALL_NODES")
    logger.info(f"Cycle Result: Strategy={cycle_result['strategy']}, Action={cycle_result['action']}")

    # 3. Test Collaborative Sync (Manual trigger)
    logger.info("TEST 3: Testing CRDT Sync Logic")
    organism.minimax.threshold = -1.0 # Force Sync action for testing
    cycle_result = await organism.run_polymath_cycle(user_intent="SYNC")

    await organism.shutdown()
    logger.info("v93.0 Simulation complete.")

if __name__ == "__main__":
    asyncio.run(run_v93_simulation())
