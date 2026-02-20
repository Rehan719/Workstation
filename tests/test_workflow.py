import pytest
import asyncio
import os
import yaml
from agentic_core.orchestrator import Orchestrator
from agents.research.literature_synthesizer import LiteratureSynthesizer
from agents.writing.manuscript_architect import ManuscriptArchitect
from agents.quality.vlm_critic import VLMCritic

@pytest.mark.asyncio
async def test_workflow_execution():
    orchestrator = Orchestrator()

    # Register workers
    orchestrator.register_worker(LiteratureSynthesizer())
    orchestrator.register_worker(ManuscriptArchitect())
    orchestrator.register_worker(VLMCritic())

    # Define a task that uses a YAML workflow
    task = {
        "type": "scientific_publication",
        "goal": "Write a paper on quantum gravity"
    }

    # Execute
    result = await orchestrator.execute(task)

    # Verify
    assert result["status"] == "completed"
    assert "lit_review" in result["components"]
    assert "drafting" in result["components"]
    assert "quality_scan" in result["components"]

    print("Workflow execution test passed!")

if __name__ == "__main__":
    asyncio.run(test_workflow_execution())
