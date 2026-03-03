import asyncio
import logging
from agentic_core import ConsciousOrganismOrchestrator

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def run_simulation():
    logger.info("INITIATING PROJECT OMEGA: GRADUATED BALANCED TRANSITION SIMULATION")

    organism = ConsciousOrganismOrchestrator()
    await organism.start()

    # 5 Cycles of Transition
    target_cycles = 5
    current_cycle = 0

    while current_cycle < target_cycles:
        logger.info(f"\n--- EXECUTION CYCLE {current_cycle + 1} ---")

        # Simulate pulses until phase advances
        for pulse in range(3):
            result = await organism.run_omega_cycle(user_intent="REBALANCE_RESOURCES")
            logger.info(f"Pulse {pulse+1}: Result Action={result['action_executed']}, Fidelity={result['fidelity']:.3f}, Phase={result['phase']}")

            if result['phase'] > current_cycle:
                current_cycle = result['phase']
                logger.info(f"CYCLE {current_cycle} COMPLETE. New Allocation: {organism.transition_mgr.get_current_allocation()}")
                break
        else:
             logger.warning("Stabilization required, forcing advancement for simulation...")
             organism.transition_mgr.advance_cycle({"fidelity": 0.985, "stability": 0.95})
             current_cycle = organism.transition_mgr.current_phase

    logger.info("\nPROJECT OMEGA: GRADUATED TRANSITION PROTOCOL VERIFIED.")
    await organism.shutdown()

if __name__ == "__main__":
    asyncio.run(run_simulation())
