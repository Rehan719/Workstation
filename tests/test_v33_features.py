import pytest
import asyncio
from agentic_core.orchestrator import Orchestrator
from agentic_core.infrastructure.quantum_ir_compiler import QuantumIRCompiler
from agentic_core.collaboration.workspace_manager import WorkspaceManager
from agentic_core.quantum_ai.hierarchy_manager import CapabilityHierarchyManager

@pytest.mark.asyncio
async def test_v33_hierarchical_compiler():
    compiler = QuantumIRCompiler()

    # Layer 1: PennyLane -> Portable IR
    # Layer 2: Portable IR -> IBM Backend IR (with dynamic circuits)
    result = await compiler.compile(
        program=["RX", "CNOT"],
        framework="pennylane",
        target_backend="ibm",
        orchestrator_context={"allow_dynamic": True}
    )

    assert result['backend'] == "ibm"
    assert result['status'] == "optimized_for_dynamic"

@pytest.mark.asyncio
async def test_v33_sequential_collaboration():
    manager = WorkspaceManager()
    ws = await manager.create_workspace("alice", {"name": "Lab A"})

    # Synchronized editing
    await manager.propose_change(ws['id'], "alice", "circuit = [H, CNOT]")
    await manager.propose_change(ws['id'], "bob", "\nresult = execute(circuit)")

    assert "circuit = [H, CNOT]" in manager.workspaces[ws['id']]['code_state']

    # Sequential job submission
    job = await manager.submit_job(ws['id'], "alice", {"goal": "Optimize VQE"})
    assert len(manager.workspaces[ws['id']]['job_queue']) == 1
    assert job['code_snapshot'] == manager.workspaces[ws['id']]['code_state']

    # Execution
    executed_job = await manager.execute_next_job(ws['id'])
    assert executed_job['status'] == 'completed'
    assert len(manager.workspaces[ws['id']]['job_queue']) == 0

@pytest.mark.asyncio
async def test_v33_mandatory_tier1():
    hm = CapabilityHierarchyManager()

    # Tier 2 should fail if Tier 1 not stable
    with pytest.raises(PermissionError):
        await hm.ensure_tier_prerequisites('tier2')

    # Stabilize Tier 1
    hm.update_tier_metrics('tier1', {'convergence_rate': 0.95, 'error_rate': 0.01})
    assert await hm.check_tier_stability('tier1') is True

    # Now Tier 2 should pass
    assert await hm.ensure_tier_prerequisites('tier2') is True
