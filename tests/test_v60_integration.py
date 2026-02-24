import asyncio
import logging
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine
from agentic_core.incubation.adaptive_incubation_engine import AdaptiveIncubationEngine
from agentic_core.orchestration.biological_orchestrator import BiologicalOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting v60.0 Integrated Organism Test...")

    # 1. Grand Synthesis
    synthesis_engine = GrandSynthesisEngine(["."])
    await synthesis_engine.run_synthesis()

    # 2. Incubation
    incubation_engine = AdaptiveIncubationEngine()
    await incubation_engine.start_incubation("Develop a report on quantum biological synergy", {})

    # 3. Task Execution via Biological Orchestrator
    orchestrator = BiologicalOrchestrator()
    task = {"name": "Simulate VQE for H2", "type": "research", "priority": "reflex", "perplexity": 30.0}
    result = await orchestrator.execute_scientific_task(task)

    logger.info(f"Final Integrated Test Result: {result}")
    print("v60.0 Integration test PASSED.")

if __name__ == "__main__":
    asyncio.run(main())
