import pytest
import asyncio
from agentic_core.orchestrator.conscious_organism_v93 import ConsciousOrganismV93_0

@pytest.mark.asyncio
async def test_v93_task_execution():
    organism = ConsciousOrganismV93_0()
    await organism.start()

    task_data = {"type": "manuscript"}
    user_profile = {"expertise": "expert"}

    result = await organism.execute_task(task_data, user_profile)

    assert result["framework_used"] == "AutoGen"
    assert "artifact_json" in result
    assert "Honesty Metric" in result["explanation"]

    # Test Fallback
    task_data_fail = {"type": "failure_test"} # Mapped to CrewAI in router logic if added, or force it
    # Forcing CrewAI for failure test
    result_fail = await organism.execute_task({"type": "failure_test"}, user_profile)
    assert result_fail["framework_used"] == "PC-Agent"

    await organism.shutdown()

@pytest.mark.asyncio
async def test_v93_framework_routing():
    organism = ConsciousOrganismV93_0()

    assert await organism.select_framework("video") == "LangGraph"
    assert await organism.select_framework("data_analysis") == "CrewAI"
    assert await organism.select_framework("unknown") == "PC-Agent"

@pytest.mark.asyncio
async def test_v93_polymath_cycle():
    organism = ConsciousOrganismV93_0()
    await organism.start()

    result = await organism.run_polymath_cycle()

    assert result["status"] == "active"
    assert result["strategy"] in ["BO", "RL"]
    assert "reasoning_depth" in result

    await organism.shutdown()
