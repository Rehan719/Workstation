import asyncio
import logging
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine
import sys
import os

async def verify_uviap():
    logging.basicConfig(level=logging.INFO)

    # Mock sys.argv to trigger UVIAP
    sys.argv.append("--full-evolution-pipeline")

    engine = GrandSynthesisEngine()
    result = await engine.run_synthesis()

    print(f"Synthesis Result Version: {result.get('version')}")

    # Check if reports were generated
    report_dir = "docs/knowledge"
    reports = [f for f in os.listdir(report_dir) if "github_analysis" in f or "learning_reflection" in f]
    print(f"Generated UVIAP reports: {reports}")
    assert len(reports) >= 2

    print("UVIAP Verification SUCCESSFUL.")

if __name__ == "__main__":
    asyncio.run(verify_uviap())
