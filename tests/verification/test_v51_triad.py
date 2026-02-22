import pytest
import asyncio
from agentic_core.orchestrator import Orchestrator

@pytest.mark.asyncio
async def test_v51_triad_orchestration():
    orchestrator = Orchestrator()

    task = {
        "goal": "discovery_of_quantum_materials",
        "reasoning_mode": "neuro_symbolic",
        "qml_task": {"framework": "PennyLane"},
        "generate_explanation": True,
        "stakeholder_role": "expert",
        "strict_verification": True,
        "anchor_to_blockchain": True
    }

    result = await orchestrator.execute(task)

    assert result["status"] == "completed"
    assert "reasoning" in task
    assert task["reasoning"]["status"] == "PROVED"
    assert "qml_results" in task
    assert task["qml_results"]["val_accuracy"] == 0.945
    assert "explanation" in task
    assert "narrative" in task["explanation"]
    assert "verification_report" in result
    assert result["verification_report"]["overall_status"] == "VERIFIED"
    assert "blockchain_receipt" in result

@pytest.mark.asyncio
async def test_neuro_symbolic_extraction():
    orchestrator = Orchestrator()
    rule = await orchestrator.neuro_symbolic.extract_symbolic_knowledge("model_X")
    assert rule["expression"] == "E = m * c^2"
    assert "E_mc2" in orchestrator.ueg.get_nodes()

@pytest.mark.asyncio
async def test_qml_kernels():
    from agentic_core.quantum_ml.quantum_kernels import QuantumKernels
    qk = QuantumKernels()
    res = await qk.compute_qsvm_kernel({"data": [1, 2, 3]})
    assert res["status"] == "COMPUTED"
    assert res["advantage_score"] > 0.5
