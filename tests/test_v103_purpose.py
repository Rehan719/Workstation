import unittest
import json
import os
from agentic_core.purpose.evaluator import PurposeAlignmentEvaluator
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.strategy.engine import StrategicPlanningModule, ResourceManagementModule
from agentic_core.self_improvement.strategic_introspection import PurposeAnalystAgent

class TestPurposeIntegration(unittest.TestCase):
    def test_purpose_evaluator(self):
        evaluator = PurposeAlignmentEvaluator()

        # Test spiritual-heavy intent
        spiritual_intent = {"description": "Launch a dawah scholarship and charity portal."}
        res = evaluator.evaluate_intent(spiritual_intent)
        self.assertGreaterEqual(res["purpose_alignment_score"], 0.95)

        # Test purely commercial intent
        commercial_intent = {"description": "Maximize profit revenue and growth efficiency."}
        res = evaluator.evaluate_intent(commercial_intent)
        self.assertLess(res["purpose_alignment_score"], 0.90)

    def test_vga_purpose_policy(self):
        vga = VGAEngine()
        valid_purpose = {"description": "Islamic scholarship tool for productivity."}
        invalid_purpose = {"description": "Maximize profit revenue and growth efficiency."}

        self.assertTrue(vga.validate_action("purpose", valid_purpose))
        self.assertFalse(vga.validate_action("purpose", invalid_purpose))

    def test_purpose_driven_bms(self):
        spm = StrategicPlanningModule(plan_path="docs/strategy/test_purpose_plan.md")
        draft = spm.generate_draft_plan({})
        self.assertIn("Divine Pleasure", draft["mission"])
        self.assertTrue(any("purpose_target" in obj for obj in draft["objectives"]))

        rm = ResourceManagementModule()
        priorities = [
            {"type": "DAWAH", "priority": "HIGH", "purpose_target": 0.95},
            {"type": "PROFIT", "priority": "LOW", "purpose_target": 0.50}
        ]
        allocation = rm.allocate_resources(priorities)
        self.assertGreater(allocation["DAWAH"], allocation["PROFIT"])

    def test_purpose_introspection(self):
        pa = PurposeAnalystAgent()
        history = [0.95, 0.96, 0.92, 0.88] # Declining PAS
        analysis = pa.analyze_purpose_drift(history)
        self.assertEqual(analysis["status"], "DRIFT_DETECTED")
        self.assertIn("Initiate purpose-alignment audit", analysis["recommendation"])

if __name__ == "__main__":
    unittest.main()
