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
    results = await engine.run_synthesis()

    assert results["orchestration_mode"] == "unified_accessible_enterprise"
    assert os.path.exists("agentic_core/constitution/CONSTITUTION_v99.0.0.md")
    assert os.path.exists("meta/ueg_graph.json")

if __name__ == "__main__":
    asyncio.run(test_grand_synthesis_cycle())
    print("Grand Synthesis test PASSED.")
