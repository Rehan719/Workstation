import pytest
import asyncio
import sys
from unittest.mock import MagicMock

# Mock problematic dependencies before they are imported via agentic_core
sys.modules['shap'] = MagicMock()
sys.modules['qiskit'] = MagicMock()
sys.modules['pennylane'] = MagicMock()
sys.modules['camel_tools'] = MagicMock()
sys.modules['oqs'] = MagicMock()
sys.modules['web3'] = MagicMock()
sys.modules['firebase_admin'] = MagicMock()

from agentic_core.biomimicry.cycles.geospheric_orchestrator import GeosphericHomeostaticOrchestrator

@pytest.mark.asyncio
async def test_orchestrator_homeostasis():
    orchestrator = GeosphericHomeostaticOrchestrator()
    inputs = {
        "current_temp": 348.15,
        "heat_load": 50.0,
        "raw_data_size": 10.0,
        "input_count": 5,
        "process_load": 20.0,
        "data_to_memory": 0.1,
        "error_severity": 0.01
    }
    context = {
        "intent": "maintain_stability",
        "system_metrics": {"free_energy": 0.95},
        "legal_compliance": 1.0,
        "closed_loop_waste": 0.0,
        "biomimetic_fidelity": 1.0,
        "genetic_integrity": 1.0
    }

    res = await orchestrator.step(inputs, context)

    assert res["psi_score"] > 0.8
    assert res["status"] in ["HOMEOSTATIC", "PERTURBED"]
    assert "cycle_scores" in res
    assert res["divine_score"] >= 0.8

@pytest.mark.asyncio
async def test_orchestrator_violation():
    orchestrator = GeosphericHomeostaticOrchestrator()
    inputs = {}
    # Force legal violation
    context = {
        "legal_compliance": 0.5
    }

    res = await orchestrator.step(inputs, context)
    assert res["psi_score"] == float('-inf')
    assert res["status"] == "CONSTITUTIONAL_VIOLATION"
