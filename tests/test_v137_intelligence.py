import pytest
from agentic_core.knowledge.production_rag_v137 import ProductionGraphRAG, WorkflowAutonomyManager

def test_production_graph_rag():
    rag = ProductionGraphRAG()
    rag.ingest_production_concept(
        "M7_NVIDIA",
        "Blackwell Architecture",
        {"source": "NVDA_PR", "confidence": 1.0},
        ["M7_AI_COMPUTE"]
    )
    rag.ingest_concept("M7_AI_COMPUTE", "Accelerated computing", [])

    trace = rag.query_with_reasoning_trace("M7_NVIDIA", "What follows Blackwell?")
    assert trace["latency_ms"] < 500.0
    assert len(trace["results"]) > 0

def test_workflow_autonomy_low_risk():
    manager = WorkflowAutonomyManager()
    action = {"type": "TELEMETRY_ADJUSTMENT", "risk_score": 0.2}
    result = manager.execute_workflow("wf_001", action)
    assert result["status"] == "EXECUTED"
    assert result["approval_tier"] == "AUTONOMOUS"

def test_workflow_autonomy_high_risk():
    manager = WorkflowAutonomyManager()
    action = {"type": "CODE_MODIFICATION", "risk_score": 0.9}
    result = manager.execute_workflow("wf_002", action)
    assert result["status"] == "PENDING_VETO"
    assert result["approval_tier"] == "HUMAN_VETO"
