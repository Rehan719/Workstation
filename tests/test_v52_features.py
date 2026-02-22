import pytest
import asyncio
from agentic_core.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_v52_orchestrator_initialization():
    # Pass no ID to use the default or verify the passed ID
    orchestrator = Orchestrator()
    assert orchestrator.agent_id == "orchestrator.v52"
    assert orchestrator.self_improvement is not None
    assert orchestrator.observatory is not None

@pytest.mark.asyncio
async def test_v52_signals_capture():
    orchestrator = Orchestrator()
    telemetry = await orchestrator.observatory.capture_live_telemetry()
    assert "error_rate" in telemetry
    assert "latency_ms" in telemetry

@pytest.mark.asyncio
async def test_v52_batch_analysis_trigger():
    orchestrator = Orchestrator()
    task = {
        "goal": "self_optimize",
        "trigger_batch_analysis": True
    }
    result = await orchestrator.execute(task)
    assert result["status"] == "completed"

@pytest.mark.asyncio
async def test_v52_regulatory_alignment():
    # Verify constitution exists
    import os
    assert os.path.exists("meta/CONSTITUTION_v52.md")
    assert os.path.exists("meta/REGULATORY_COMPLIANCE.md")
