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
    assert orchestrator.translator is not None
    assert orchestrator.broker is not None

@pytest.mark.asyncio
async def test_production_v52_execution_flow():
    orchestrator = Orchestrator()
    # The v52 workstation uses specialized discovery workflows
    result = await orchestrator.psc_discovery_simulation("test_user")

    assert result["status"] == "MASTERED"
    assert "findings" in result
    assert result["verification_report"] == "PASSED"
    assert "manuscript_preview" in result
    assert "orchestration" in result
    assert result["orchestration"]["framework"] == "AutoGen"

@pytest.mark.asyncio
async def test_production_v52_constitution_exists():
    assert os.path.exists("meta/CONSTITUTION_v52.0.md")
