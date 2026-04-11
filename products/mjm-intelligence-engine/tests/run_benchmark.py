import asyncio
import logging
import time
import sys
import os

# Add product root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmark")

async def run_benchmark():
    orchestrator = MJMWorkflowOrchestrator()

    input_spec = {
        "domain_id": "patient_safety",
        "queries": [
            "Patient safety intelligence proceduralism trap",
            "March 28 2026 whistleblower data integrity",
            "Long-term risk assessment frameworks UK healthcare"
        ],
        "contributor": "Jules-Benchmark",
        "selected_option_id": "opt-regulatory-realignment"
    }

    start_time = time.time()
    logger.info("Starting End-to-End Benchmark for LON-INT-FINAL-2026-003")

    try:
        bundle = await orchestrator.execute_pipeline(input_spec)
        duration = time.time() - start_time

        logger.info(f"Benchmark completed in {duration:.2f} seconds.")

        # Verify Acceptance Criteria
        verification = orchestrator.verify_output(bundle)
        logger.info(f"Verification Results: {verification}")

        if duration < 900: # 15 minutes
            logger.info("✅ Time Requirement Passed (< 15 mins)")
        else:
            logger.error("❌ Time Requirement Failed (> 15 mins)")

        if verification["integrity_pass"] and verification["traceability_pass"]:
            logger.info("✅ Provenance & Traceability Passed")
        else:
            logger.error(f"❌ Verification Failed: {verification['checks']}")

        # Check for Litigation Bundle (UK Tribunal)
        if bundle.proposal_package.litigation_bundle:
            logger.info("✅ Litigation Bundle Generated")
        else:
            logger.error("❌ Litigation Bundle Missing")

    except Exception as e:
        logger.error(f"Benchmark Failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
