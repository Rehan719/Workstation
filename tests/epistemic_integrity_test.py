import asyncio
import unittest
import os
import json
from agentic_core.orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0
from agentic_core.genetics.genomic_registry import GenomicRegistry

class TestV70Organism(unittest.IsolatedAsyncioTestCase):

    async def test_v70_organism_pulse(self):
        """Verifies full hierarchical pulse of the v70 digital organism."""
        organism = ConsciousOrganismV70_0()

        # Test pulse with high dwell time (normal state)
        result = organism.run_lifecycle_pulse(user_dwell_ms=800, user_latency_ms=100)

        self.assertEqual(result["modality"], "SCIENTIFIC_DISCOVERY")
        self.assertGreater(result["fidelity"], 0.95)
        self.assertIn("p53_phase", result["triad"])

        # Test stress state (low dwell time)
        stress_result = organism.run_lifecycle_pulse(user_dwell_ms=50, user_latency_ms=500)
        # High ROS should lead to repair or conservation
        self.assertNotEqual(stress_result["mce"]["action"], "SCIENTIFIC_DISCOVERY")

    async def test_lamarckian_heritability(self):
        """Verifies DC-II: Heritability of acquired traits."""
        if os.path.exists("meta/genome_ledger_test.json"):
            os.remove("meta/genome_ledger_test.json")

        registry = GenomicRegistry(persistence_path="meta/genome_ledger_test.json")
        traits = {"optimized_vqe": "0.998"}
        registry.commit_mutation(traits, "zkp:test")

        # Reload to simulate new generation
        new_registry = GenomicRegistry(persistence_path="meta/genome_ledger_test.json")
        self.assertEqual(new_registry.current_genome["traits"]["optimized_vqe"], "0.998")
        self.assertEqual(new_registry.get_genome_depth(), 1)

if __name__ == "__main__":
    unittest.main()
