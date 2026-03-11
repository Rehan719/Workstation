import asyncio
import os
import sys
from agentic_core.synthesis.grand_synthesis_engine import GrandSynthesisEngine

async def test_v107_synthesis_cycle():
    # Mock sys.argv to simulate --generate-docs
    sys.argv.append("--generate-docs")

    # Ensure directories exist
    os.makedirs("docs/guides", exist_ok=True)
    os.makedirs("docs/dcs", exist_ok=True)

    engine = GrandSynthesisEngine(["."])
    # Target v107.0.0 for the test
    results = await engine.run_synthesis(target_version="107.0.0")

    assert results["version"] == "107.0.0"
    assert os.path.exists("CONSTITUTION_v107.0.0.md")
    assert os.path.exists("docs/guides/repo_owner.md")
    assert os.path.exists("docs/dcs/repo_owner.md")

    # Check if doc generator worked
    with open("docs/guides/repo_owner.md", "r") as f:
        content = f.read()
        assert "v107.0" in content

    print("v107.0 Grand Synthesis & Documentation Test PASSED.")

if __name__ == "__main__":
    asyncio.run(test_v107_synthesis_cycle())
