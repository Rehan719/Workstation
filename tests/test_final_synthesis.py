import unittest
from agentic_core.enterprise.engine import EnterpriseEvolutionEngine
from agentic_core.strategy.engine import StrategicPlanningModule, ResourceManagementModule, PerformanceManagementModule
from agentic_core.entity.ceo_interface import EntityCEOInterface
from agentic_core.self_improvement.strategic_introspection import BusinessAnalystAgent, GovernanceAnalystAgent, PurposeAnalystAgent, StrategicReflector
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.purpose.evaluator import PurposeAlignmentEvaluator

class TestFullIntegration(unittest.TestCase):
    def test_purpose_evaluator(self):
        eval = PurposeAlignmentEvaluator()
        res = eval.evaluate_intent({"description": "Dawah and profit."})
        self.assertGreater(res["purpose_alignment_score"], 0.90)

    def test_vga_purpose(self):
        vga = VGAEngine()
        self.assertTrue(vga.validate_action("purpose", {"description": "Ethics and utility."}))

    def test_bms_p(self):
        spm = StrategicPlanningModule()
        draft = spm.generate_draft_plan({})
        self.assertIn("Purpose-Driven", draft["vision"])

    def test_introspection_p(self):
        pa = PurposeAnalystAgent()
        analysis = pa.analyze_purpose_drift([0.95, 0.96, 0.88])
        self.assertEqual(analysis["status"], "DRIFT_DETECTED")

if __name__ == "__main__":
    unittest.main()
