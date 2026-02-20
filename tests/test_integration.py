import pytest
import asyncio
from agentic_core.orchestrator import Orchestrator
from agents.research.literature_synthesizer import LiteratureSynthesizer
from agents.writing.manuscript_architect import ManuscriptArchitect

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

if __name__ == "__main__":
    asyncio.run(test_orchestrator_integration())
