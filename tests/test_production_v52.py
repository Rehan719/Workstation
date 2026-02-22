import pytest
import asyncio
import os
from src.orchestrator.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_production_v52_orchestrator_initialization():
    orchestrator = Orchestrator()
    assert orchestrator.ueg is not None
    assert orchestrator.neuro_symbolic is not None
    assert orchestrator.quantum is not None

@pytest.mark.asyncio
async def test_production_v52_execution_flow():
    orchestrator = Orchestrator()
    user_profile = {"expertise": "expert"}
    # The task now performs actual logic
    result = await orchestrator.execute_task("Investigate factor X", user_profile)

    assert "result" in result
    assert "verification" in result
    assert result["verification"]["overall_status"] == "PASSED"
    assert "explanation" in result
    assert "narrative" in result["explanation"]

@pytest.mark.asyncio
async def test_production_v52_constitution_exists():
    assert os.path.exists("meta/CONSTITUTION_v52.0.md")
