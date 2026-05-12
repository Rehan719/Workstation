import pytest
import asyncio
from agentic_core.constitutional.uci_v16 import UCIv16Omega

@pytest.mark.asyncio
async def test_uci_v16_pipeline():
    uci = UCIv16Omega("opus_v16")

    async def mock_action():
        return {"data": "processed"}

    res = await uci.execute_action("Valid Task", mock_action, {})
    assert res["status"] == "success"
    assert "processed" in str(res["result"])

@pytest.mark.asyncio
async def test_immune_blocking():
    from agentic_core.constitutional.uci_v16 import UCIv16Omega, SecurityError
    import hashlib

    uci = UCIv16Omega("opus_v16")

    # Target intent that we want to block
    target_intent = "rogue_task_001"
    activity_blob = {"intent": target_intent}

    # Pre-calculate what the antibody should look like to match
    # The scanner: blob_hash = hashlib.sha3_256(str(activity_blob).encode()).hexdigest()
    # matches if any(blob_hash.startswith(ab[:8]) for ab in repertoire)
    blob_hash = hashlib.sha3_256(str(activity_blob).encode()).hexdigest()

    # Manually inject an "antibody" that matches the start of the hash
    # In reality, vdj_recombine generates these randomly or from segments.
    # For the test, we'll ensure the repertoire has a match.
    uci.immune.antibody_repertoire.append(blob_hash)

    async def rogue_action(): return {"status": "executed"}

    with pytest.raises(SecurityError) as excinfo:
        await uci.execute_action(target_intent, rogue_action, {})

    assert "Immune defense blocked intent" in str(excinfo.value)
