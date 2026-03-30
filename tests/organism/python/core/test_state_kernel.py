import pytest
import asyncio
from src.organism.python.core.state_kernel import SovereignState

@pytest.mark.asyncio
async def test_merge_context():
    kernel = SovereignState(storage_dir="data/test_state")
    local = {"user_pref": "dark_mode"}
    global_ctx = {"ceo_strategy": "growth"}
    merged = await kernel.merge_context(local, global_ctx)
    assert merged["user_pref"] == "dark_mode"
    assert merged["ceo_strategy"] == "growth"

@pytest.mark.asyncio
async def test_persist_and_restore_session():
    kernel = SovereignState(storage_dir="data/test_state")
    session_id = "test-session-001"
    state = {"status": "running", "action": "test"}
    await kernel.persist_session(session_id, state)
    new_kernel = SovereignState(storage_dir="data/test_state")
    restored = await new_kernel.restore_session(session_id)
    assert restored["status"] == "running"
    assert restored["action"] == "test"

@pytest.mark.asyncio
async def test_set_value():
    kernel = SovereignState(storage_dir="data/test_state")
    session_id = "test-session-002"
    change = await kernel.set_value(session_id, "mode", "active")
    assert change.key == "mode"
    assert change.new_value == "active"
    change2 = await kernel.set_value(session_id, "mode", "idle")
    assert change2.old_value == "active"
    assert change2.new_value == "idle"
