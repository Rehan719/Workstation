import pytest
import asyncio
from agentic_core.orchestrator import Orchestrator
from agents.research.literature_synthesizer import LiteratureSynthesizer
from agents.writing.manuscript_architect import ManuscriptArchitect
from agentic_core.pc_agent.manager_agent import ManagerAgent
from agentic_core.memory.crdt_store import CRDTStore

@pytest.mark.asyncio
async def test_orchestrator_integration():
    # Initialize orchestrator
    orchestrator = Orchestrator()

    # Register workers
    lit_agent = LiteratureSynthesizer()
    write_agent = ManuscriptArchitect()

    orchestrator.register_worker(lit_agent)
    orchestrator.register_worker(write_agent)

    # Define a mock task
    task = {
        "goal": "Write a paper about hybrid agentic systems"
    }

    # Execute
    result = await orchestrator.execute(task)

    # Verify
    assert result["status"] == "completed"
    assert "lit_review" in result["components"]
    assert "drafting" in result["components"]
    assert result["components"]["lit_review"]["status"] == "success"
    assert "sections" in result["components"]["drafting"]

    print("Integration test passed successfully!")

@pytest.mark.asyncio
async def test_pc_agent_hierarchy():
    manager = ManagerAgent()
    task = {"goal": "Test hierarchical decomposition"}
    result = await manager.execute(task)
    assert result["status"] == "planned"
    assert len(result["subtasks"]) > 0

def test_crdt_consistency():
    store = CRDTStore()
    store.update_project("p1", "title", "v1")
    t1 = store.state["p1"]["fields"]["title"]["timestamp"]

    # Remote update with later timestamp
    remote_state = {
        "p1": {
            "fields": {"title": {"value": "v2", "timestamp": t1 + 100}},
            "node_id": "remote"
        }
    }
    store.merge(remote_state)
    assert store.get_project("p1")["title"] == "v2"

    # Remote update with earlier timestamp (should be ignored)
    remote_state_old = {
        "p1": {
            "fields": {"title": {"value": "v0", "timestamp": t1 - 100}},
            "node_id": "remote"
        }
    }
    store.merge(remote_state_old)
    assert store.get_project("p1")["title"] == "v2"

if __name__ == "__main__":
    asyncio.run(test_orchestrator_integration())
