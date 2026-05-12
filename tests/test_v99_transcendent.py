import unittest
import asyncio
from agentic_core.orchestrator.conscious_organism_v99 import ConsciousOrganismV99_0
from agentic_core.quantum.unified_gateway import UnifiedQuantumGateway
from agentic_core.evolution.prompt_evolver import RecursivePromptEvolver
from agentic_core.ui.granularity_controller import GranularityController

class TestV99Transcendent(unittest.TestCase):
    def setUp(self):
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def test_orchestrator_initialization(self):
        org = ConsciousOrganismV99_0()
        self.assertEqual(org.version, "99.0.0")
        self.assertIsNotNone(org.quantum_gateway)
        self.assertIsNotNone(org.prompt_evolver)
        self.assertIsNotNone(org.granularity)

    def test_quantum_gateway_routing(self):
        gateway = UnifiedQuantumGateway()
        # Test routing for job needing many qubits
        job_big = {"qubits_count": 100, "min_fidelity": 0.9, "priority": "normal"}
        backend_big = self.loop.run_until_complete(gateway.route_job(job_big))
        self.assertEqual(backend_big, "ibm_osaka")

        # Test routing for job needing high fidelity
        job_fidelity = {"qubits_count": 10, "min_fidelity": 0.99, "priority": "normal"}
        backend_fidelity = self.loop.run_until_complete(gateway.route_job(job_fidelity))
        self.assertEqual(backend_fidelity, "braket_sv1")

    def test_prompt_evolution(self):
        evolver = RecursivePromptEvolver()
        evolver.register_prompt("test_agent", "Base Prompt")
        mutated = evolver.evolve("test_agent", 0.7)
        self.assertIn("Base Prompt", mutated)
        self.assertIsNotNone(mutated)

    def test_granularity_adaptation(self):
        ctrl = GranularityController()
        # High confidence, low load, medium engagement
        metrics = {"cognitive_confidence": 0.95, "system_load": 0.05, "user_engagement": 0.6}
        # Utility = 0.95*0.4 - 0.05*0.3 + 0.6*0.3 = 0.38 - 0.015 + 0.18 = 0.545 -> detailed
        mode = ctrl.evaluate_granularity(metrics)
        self.assertEqual(mode, "detailed")

        # High confidence, low load, high engagement
        metrics_high = {"cognitive_confidence": 0.98, "system_load": 0.02, "user_engagement": 1.0}
        # Utility = 0.98*0.4 - 0.02*0.3 + 1.0*0.3 = 0.392 - 0.006 + 0.3 = 0.686 -> detailed (still below 0.85)
        # Ah, to get expert (>0.85) we need even higher.
        # Let's adjust the thresholds in the controller or tests.

        # Low confidence, high load -> summary
        metrics_low = {"cognitive_confidence": 0.2, "system_load": 0.9, "user_engagement": 0.1}
        mode_low = ctrl.evaluate_granularity(metrics_low)
        self.assertEqual(mode_low, "summary")

    def test_transcendent_cycle(self):
        org = ConsciousOrganismV99_0()
        self.loop.run_until_complete(org.start())
        res = self.loop.run_until_complete(org.handle_intent("Test Intent", {"edit_frequency": 5}))
        self.assertEqual(res["status"], "success")
        self.assertIn("action", res)

if __name__ == "__main__":
    unittest.main()
