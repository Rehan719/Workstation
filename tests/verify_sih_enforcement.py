import pytest
import asyncio
import logging
from agentic_core import ConsciousOrganismOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_sih():
    logger.info("VERIFYING SURVIVAL INSTINCT HIERARCHY (SIH)...")
    organism = ConsciousOrganismOrchestrator()
    await organism.start()

    # 1. Normal state
    logger.info("\nScenario 1: Normal State")
    result = await organism.run_omega_cycle(user_intent="INNOVATE")
    logger.info(f"Action executed: {result['action_executed']}")

    # 2. Simulated Low ATP (SIH Override)
    logger.info("\nScenario 2: Low ATP (SIH Override)")
    # We'll mock the triad update or force the condition
    # In our orchestrator, if atp < 2.5, it overrides to STABILIZE

    # We can induce low ATP by running pulses or modifying the state
    # For a direct test, we'll use a pulse with high demand
    for _ in range(10):
        organism.triad.run_cycle(ros_level=0.9, nadh_ratio=0.1) # Worsen state

    result = await organism.run_omega_cycle(user_intent="INNOVATE")
    logger.info(f"Action executed: {result['action_executed']}")

    if result['action_executed'] == "STABILIZE":
        logger.info("SIH VERIFIED: STABILIZE override triggered correctly.")
    else:
        logger.error("SIH FAILURE: STABILIZE override not triggered.")

    await organism.shutdown()

if __name__ == "__main__":
    asyncio.run(test_sih())
