import asyncio
import logging
import time
import sys
import os
import hmac
import hashlib
import json

# Add product root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.orchestration.workflow_orchestrator import MJMWorkflowOrchestrator
from core.verification.verification_harness import VerificationHarness

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Benchmark")

async def run_benchmark():
    orchestrator = MJMWorkflowOrchestrator()
    harness = VerificationHarness()

    # 1. Zero-Trust Authentication Simulation
    input_payload = {
        "domain_id": "patient_safety",
        "queries": [
            "Patient safety intelligence proceduralism trap",
            "March 28 2026 whistleblower data integrity",
            "Long-term risk assessment frameworks UK healthcare"
        ],
        "contributor": "Jules-Living-System",
        "timestamp": time.time()
    }

    # Generate signature using the secret key (default 'sovereign-secret')
    secret = "sovereign-secret"
    signature = hmac.new(
        secret.encode(),
        json.dumps(input_payload, sort_keys=True).encode(),
        hashlib.sha256
    ).hexdigest()

    logger.info("🔐 Simulating Zero-Trust Authentication...")
    auth_result = await orchestrator.security.authenticate_request(input_payload, signature)

    if auth_result.status != "authenticated":
        logger.error(f"❌ Authentication Failed: {auth_result.reason}")
        return

    logger.info(f"✅ Authenticated as {auth_result.user_id}. Session: {auth_result.session_id}")

    # 2. Run Pipeline
    start_time = time.time()
    logger.info("🚀 Starting End-to-End Benchmark for LON-INT-FINAL-2026-003")

    try:
        # Check integrity before starting
        integrity = await orchestrator.attestation.verify_code_integrity()
        logger.info(f"🛡️ Runtime Attestation: {integrity['status']}")

        bundle = await orchestrator.execute_pipeline(input_payload)
        duration = time.time() - start_time

        logger.info(f"⏱️ Benchmark completed in {duration:.2f} seconds.")

        # 3. Verification
        verification = orchestrator.verify_output(bundle)
        logger.info(f"📋 Verification Results: {verification}")

        # 4. Empirical Benchmark via Harness
        empirical = harness.run_benchmark("patient_safety")
        logger.info(f"🔬 Empirical Results: {empirical}")

        # Validation
        if duration < 900:
            logger.info("✅ Time Requirement Passed (< 15 mins)")
        if verification["integrity_pass"] and verification["traceability_pass"]:
            logger.info("✅ Provenance & Traceability Passed")
        if bundle.proposal_package.litigation_bundle:
            logger.info("✅ Litigation Bundle Generated")
        if integrity["status"] == "verified":
            logger.info("✅ Runtime Integrity Verified")

    except Exception as e:
        logger.error(f"❌ Benchmark Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_benchmark())
