
import pytest
import asyncio
from agentic_core.transition.graduated_transition_manager import GraduatedTransitionManager
from agentic_core.transition.transition_monitor import RollbackController
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0

@pytest.mark.asyncio
async def test_deterministic_rollback_v99():
    print("\n1. Initializing ConsciousOrganismV99 with Graduated Transition Manager...")
    org = ConsciousOrganismV99_0(agent_id="test_agent")
    manager = org.transition_mgr
    rollback = org.rollback

    assert manager.current_phase == 0
    print(f"   Baseline Phase: {manager.current_phase}")

    print("2. Advancing transition to Phase 2...")
    manager.advance_cycle({"fidelity": 0.99, "stability": 0.99})
    manager.advance_cycle({"fidelity": 0.99, "stability": 0.99})
    assert manager.current_phase == 2
    print(f"   Current Phase: {manager.current_phase}")

    print("3. Simulating a deployment failure / stability degradation...")
    # In a real scenario, the monitor would detect this.
    # Here we trigger the rollback explicitly via the controller.

    success = rollback.execute_rollback()
    assert success == True
    assert manager.current_phase == 1
    print(f"   Rollback Successful. Reverted to Phase: {manager.current_phase}")

    print("4. Verifying Stage-Versioned Artifact (Deterministic State)...")
    # v99-gastrula or similar stage-versioning is reflected in the transition progress
    allocation = manager.get_current_allocation()
    print(f"   Current Resource Allocation (Phase 1): {allocation}")
    # Phase 1: progress = 1/5 = 0.2. triad_weight = 0.60 - (0.555 * 0.2) = 0.60 - 0.111 = 0.489
    assert allocation["triad_aggregate"] == 0.489

if __name__ == "__main__":
    asyncio.run(test_deterministic_rollback_v99())
