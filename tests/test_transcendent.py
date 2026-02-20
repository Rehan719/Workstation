import pytest
import asyncio
from agentic_core.transcendent import TranscendentLayer

@pytest.mark.asyncio
async def test_transcendent_layer():
    transcendent = TranscendentLayer()

    # Test consolidation
    task = {"action": "consolidate"}
    result = await transcendent.execute(task)
    assert result["status"] == "success"

    # Test cross-project insight
    task = {"action": "cross_project_insight", "query": "quantum", "projects": ["P1", "P2"]}
    result = await transcendent.execute(task)
    assert result["status"] == "success"
    assert "insights" in result

if __name__ == "__main__":
    asyncio.run(test_transcendent_layer())
