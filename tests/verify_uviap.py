import asyncio
import logging
import os
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine

async def verify_uviap():
    logging.basicConfig(level=logging.INFO)
    engine = GrandSynthesisEngine(["."])

    # Run synthesis with UVIAP
    results = await engine.run_synthesis(target_version="120.0.0")

    print(f"Synthesis Result Version: {results['version']}")
    assert results["version"] == "120.0.0"

    # Check for UVIAP reports
    reports = os.listdir("docs/knowledge/")
    print(f"Generated UVIAP reports: {reports}")
    assert any("github_analysis" in r for r in reports)
    assert any("learning_reflection" in r for r in reports)

    print("UVIAP Verification SUCCESSFUL.")

if __name__ == "__main__":
    asyncio.run(verify_uviap())
