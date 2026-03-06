import pytest
import asyncio
import logging
from agentic_core import ConsciousOrganismOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_rollback():
    logger.info("VERIFYING TRANSITION ROLLBACK CONTROLLER...")
    organism = ConsciousOrganismOrchestrator()
    await organism.start()

    # 1. Advance to Cycle 1
    logger.info("\nStep 1: Advance to Cycle 1")
    organism.transition_mgr.advance_cycle({"fidelity": 0.985, "stability": 0.95})
    logger.info(f"Current Phase: {organism.transition_mgr.current_phase}")

    # 2. Simulate Fidelity Drop (< 96%)
    logger.info("\nStep 2: Simulate Fidelity Drop")
    # We'll mock the fidelity scorer to return a low value
    organism.fidelity_scorer.get_overall_fidelity = lambda: 0.94

    # Run a cycle which triggers rollback check
    result = await organism.run_omega_cycle()

    logger.info(f"Action: {result['action_executed']}, Phase after cycle: {result['phase']}")

    if result['phase'] == 0:
        logger.info("ROLLBACK VERIFIED: System reverted from Phase 1 to Phase 0 due to low fidelity.")
    else:
        logger.error(f"ROLLBACK FAILURE: System remained in Phase {result['phase']}.")

    await organism.shutdown()

if __name__ == "__main__":
    asyncio.run(test_rollback())
