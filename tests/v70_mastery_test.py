import asyncio
import unittest
import os
import json
from agentic_core.orchestration.conscious_organism_v70_0 import ConsciousOrganismV70_0

class TestV70Mastery(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.organism = ConsciousOrganismV70_0()

    async def asyncTearDown(self):
        self.organism.shutdown()

    async def test_organism_pulse_mastery(self):
        """Verifies v70 organism pulse and fidelity-based suspension."""
        # 1. Normal state pulse
        result = self.organism.run_lifecycle_pulse(user_dwell_ms=800, user_latency_ms=100)
        self.assertEqual(result["modality"], "SCIENTIFIC_DISCOVERY")
        self.assertGreaterEqual(result["fidelity"], 0.95)
        self.assertEqual(result["fidelity_report"]["is_suspended"], False)

        # 2. Trigger suspension via high ROS (simulated via low dwell time)
        stress_result = self.organism.run_lifecycle_pulse(user_dwell_ms=50, user_latency_ms=10)
        self.assertEqual(stress_result["modality"], "SUSPENDED")
        self.assertTrue(stress_result["fidelity_report"]["is_suspended"])
        self.assertEqual(stress_result["fidelity"], 0.5)

    def test_commercial_modules(self):
        """Verifies functional commercial mastery modules."""
        abstract = self.organism.design_studio.create_graphical_abstract("Room temperature superconductivity found in LK-99")
        self.assertEqual(abstract["status"], "ready")

        video = self.organism.content_gen.generate_video_presentation("Mastery script")
        self.assertEqual(video["narration"], "enabled")

        pipeline = self.organism.rd_pipeline.execute_pipeline("Graphene Synthesis")
        self.assertIn("ThermoFisher_Centrifuge", pipeline["instrument_logs"])

if __name__ == "__main__":
    unittest.main()
