import pytest
import asyncio
from agentic_core.pc_agent.manager_agent import ManagerAgent
from agentic_core.pc_agent.progress_agent import ProgressAgent
from agentic_core.pc_agent.decision_agent import DecisionAgent
from agentic_core.pc_agent.reflection_agent import ReflectionAgent

@pytest.mark.asyncio
async def test_pc_agent_hierarchy():
    manager = ManagerAgent()
    progress = ProgressAgent()
    decision = DecisionAgent()
    reflection = ReflectionAgent()

    # Mock task for Manager
    goal_task = {"goal": "Automate manuscript preparation"}
    manager_result = await manager.execute(goal_task)
    assert manager_result["status"] == "planned"
    assert len(manager_result["subtasks"]) > 0

    # Mock task for Progress
    progress_task = {"task_id": "task_1"}
    progress_result = await progress.execute(progress_task)
    assert progress_result["status"] == "monitoring"
    assert "progress" in progress_result

    # Mock task for Decision
    decision_task = {"action": "click_button", "params": {"name": "Generate"}}
    decision_result = await decision.execute(decision_task)
    assert decision_result["status"] == "executed"

    # Mock task for Reflection
    reflection_task = {"outcome": "Task failed to converge", "success": False}
    reflection_result = await reflection.execute(reflection_task)
    assert reflection_result["status"] == "reflected"
    assert reflection_result["should_retry"] is True

if __name__ == "__main__":
    asyncio.run(test_pc_agent_hierarchy())
