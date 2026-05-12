import asyncio
import os
import pytest
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine

@pytest.mark.asyncio
async def test_grand_synthesis_cycle():
    # Ensure directories exist for the test environment
    os.makedirs("agentic_core/constitution", exist_ok=True)
    os.makedirs("meta", exist_ok=True)

    engine = GrandSynthesisEngine(["."])
    # Target 117.0 for the current era
    results = await engine.run_synthesis(target_version="117.0.0")

    assert results["orchestration_mode"] == "multidisciplinary_product_enterprise"
    assert os.path.exists("agentic_core/constitution/CONSTITUTION_v117.0.0.md")

if __name__ == "__main__":
    asyncio.run(test_grand_synthesis_cycle())
    print("Grand Synthesis test PASSED.")
