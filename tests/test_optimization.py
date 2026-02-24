from agentic_core.optimization.synergy_scalar import SynergyScalar
from agentic_core.optimization.lean_enforcer import LeanEnforcer
from agentic_core.optimization.free_resource_maximizer import FreeResourceMaximizer

def test_optimization_drive():
    synergy = SynergyScalar()
    enforcer = LeanEnforcer()
    maximizer = FreeResourceMaximizer()

    # 1. Synergy Calculation
    score = synergy.compute_synergy({"comm_overhead": 0.1, "resource_contention": 0.2})
    assert score == 0.85

    # 2. Lean Enforcement
    waste = enforcer.scan_for_waste([{"execution_time": 2000, "cached": False}])
    assert len(waste) == 1
    assert waste[0]["type"] == "redundant_calc"

    # 3. Resource Maximization
    res = maximizer.allocate_resource({"can_run_locally": True})
    assert res == "local_oss"

    print("Optimization Drive verification PASSED.")

if __name__ == "__main__":
    test_optimization_drive()
