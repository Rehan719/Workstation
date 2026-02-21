import pytest
from agents.quantum.intelligent_quantum_orchestrator_agent import IntelligentQuantumOrchestratorAgent
from agents.quantum.quantum_federated_learning_agent import QuantumFederatedLearningAgent

@pytest.mark.asyncio
async def test_tier1_orchestrator():
    orchestrator = IntelligentQuantumOrchestratorAgent()
    task = {"circuit": "gate_set_1", "noise_level": "high"}
    result = await orchestrator.execute(task)

    assert result["status"] == "success"
    assert result["optimizer"] == "CMA-ES"
    assert len(result["shannon_entropy_path"]) > 0

@pytest.mark.asyncio
async def test_tier2_qfl_stigmergy():
    agent = QuantumFederatedLearningAgent()
    task = {"domain": "healthcare"}
    result = await agent.execute(task)

    assert result["status"] == "success"
    assert "stigmergic_inference" in result
    assert result["privacy_metric"] == "secure_parameter_sharing_active"
