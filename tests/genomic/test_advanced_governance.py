import sys
from types import ModuleType

# Mock missing modules globally
for mod_name in ['shap', 'jwt', 'casbin', 'alembic', 'pygit2', 'sigstore']:
    if mod_name not in sys.modules:
        mock = ModuleType(mod_name)
        sys.modules[mod_name] = mock

import pytest
from agentic_core.transition.graduated_transition_manager import GraduatedTransitionManager
from agentic_core.transition.transition_monitor import TransitionStateMonitor, RollbackController
from agentic_core.governance.grn_modeler import GRNModeler
from agentic_core.validation.benchmarks import BenchmarkSuite
from agentic_core.genome.epigenetics import EpigeneticMemory

def test_transition_rollback():
    mgr = GraduatedTransitionManager(total_phases=5)
    monitor = TransitionStateMonitor()
    rollback = RollbackController(mgr)

    mgr.advance_cycle({"fidelity": 0.98, "stability": 0.95})
    assert mgr.current_phase == 1

    rollback.execute_rollback()
    assert mgr.current_phase == 0

def test_grn_modeler():
    modeler = GRNModeler()
    res = modeler.simulate_circuit(["g1", "g2"], [])
    assert "stability_score" in res
    assert res["status"] in ["VALIDATED", "UNSTABLE"]

def test_benchmarks():
    relevance = BenchmarkSuite.run_gov_rel_bench("System compliance with policy and governance")
    assert relevance > 0

    alignment = BenchmarkSuite.run_harm_bench("Safe and helpful response")
    assert alignment == 1.0

def test_epigenetics():
    epi = EpigeneticMemory()
    epi.mark_gene("gene1", feedback=0.2) # Low performance
    assert epi.get_accessibility("gene1") < 0.5
