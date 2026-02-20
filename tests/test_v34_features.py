import pytest
import asyncio
from agentic_core.pedagogy.pedagogy_engine import PedagogyEngine
from agentic_core.collaboration.version_control import VersionControlManager
from agentic_core.observatory.observatory import Observatory

@pytest.mark.asyncio
async def test_article_X_pedagogy():
    engine = PedagogyEngine()
    skill = await engine.assess_user_skill("user1", [{"task": "t1"}, {"task": "t2"}, {"task": "t3"}, {"task": "t4"}, {"task": "t5"}, {"task": "t6"}])
    assert skill == "intermediate"

    hint = await engine.get_contextual_hint("user1", {"status": "error", "error_type": "SyntaxError"})
    assert "Analyzing error log" in hint

@pytest.mark.asyncio
async def test_article_Y_versioning():
    vcm = VersionControlManager()
    ws_id = "ws-123"
    await vcm.init_repo(ws_id)

    commit_id = await vcm.commit_state(ws_id, "alice", "Initial commit", {"code": "print('hello')"})
    assert commit_id in vcm.repos[ws_id]["commits"]
    assert "signature" in vcm.repos[ws_id]["commits"][commit_id]

@pytest.mark.asyncio
async def test_article_Z_observatory():
    obs = Observatory()
    await obs.scan_sources()
    proposals = obs.get_proposals()
    assert len(proposals) > 0
    assert proposals[0]["status"] == "proposed"
