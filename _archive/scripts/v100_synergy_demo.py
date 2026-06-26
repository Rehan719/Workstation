import asyncio
import logging
import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.getcwd())

from agentic_core.reactor import initialize_reactor_ecosystem
from agentic_core.orchestrator.synergy import SynergyOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SynergyDemo")

async def run_v100_demo():
    logger.info("--- v100.0 Synergy Demonstration Starting ---")

    # 1. Initialize Ecosystem
    logger.info("Initializing Reactor Ecosystem...")
    initialize_reactor_ecosystem()

    # 2. Initialize Orchestrator
    orchestrator = SynergyOrchestrator()

    # 3. Demonstrate Biophysics Research (Synergy across Science:Biology, Science:Physics, Science:CompSci)
    logger.info("Executing 'Biophysics Research' Synergy Workflow...")
    result = await orchestrator.demonstrate_biophysics_research()

    logger.info(f"Workflow Status: {result['status']}")
    logger.info(f"VTF Participants: {result['vtf_participants']}")
    logger.info(f"Truth Consensus: {result['truth_consensus']}")

    # 4. Demonstrate a custom multi-domain workflow
    logger.info("Executing 'Islamic Finance Legal Strategy' Synergy Workflow...")
    # Requires: religion:islamic_finance, law:contract, law:regulatory
    custom_task = {
        "requirements": ["religion:islamic_finance", "law:contract", "law:regulatory"],
        "input": "Sharia-compliant Sukuk structure for infrastructure project",
        "params": {"jurisdiction": "Global/AAOIFI"}
    }
    custom_result = await orchestrator.execute_synergy_workflow("Sukuk Legal Structuring", custom_task)

    logger.info(f"Custom Workflow Status: {custom_result['status']}")
    logger.info(f"Custom VTF Participants: {custom_result['vtf_participants']}")

    logger.info("--- v100.0 Synergy Demonstration Completed Successfully ---")

if __name__ == "__main__":
    asyncio.run(run_v100_demo())
