import pytest
import asyncio
from agentic_core.constitutional.uci import UCIv139Omega

@pytest.mark.asyncio
async def test_uci_full_pipeline():
    uci = UCIv139Omega("opus_prime")

    async def mock_action():
        return {"data": "synthesized_knowledge"}

    # Use 'serve' keyword to satisfy DivineAlignmentEngine mock logic
    intent = "Serve humanity by optimizing vaccine protein folding"
    report = await uci.execute_sovereign_action(intent, mock_action, {"priority": "high"})

    assert report["status"] == "success"
    assert report["metrics"]["sincerity"] > 0.9
    assert report["cascade_depth"] == 6
    assert "eternal_value" in report["metrics"]

@pytest.mark.asyncio
async def test_uci_repair_flow():
    uci = UCIv139Omega("opus_prime")

    async def failing_action():
        raise RuntimeError("System Overload")

    # Use 'help' keyword to satisfy DivineAlignmentEngine mock logic
    intent = "Help process critical diagnostic data"
    report = await uci.execute_sovereign_action(intent, failing_action, {})

    # Result should contain the repair output from Regulator
    assert "fixed_via_MMR" in str(report["result"])
