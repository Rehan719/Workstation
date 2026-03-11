import unittest
from agentic_core.enterprise.engine import EnterpriseEvolutionEngine
from agentic_core.strategy.engine import StrategicPlanningModule, ResourceManagementModule, PerformanceManagementModule
from agentic_core.entity.ceo_interface import EntityCEOInterface
from agentic_core.self_improvement.strategic_introspection import BusinessAnalystAgent, GovernanceAnalystAgent, PurposeAnalystAgent, StrategicReflector
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.purpose.evaluator import PurposeAlignmentEvaluator
from agentic_core.enterprise.c_suite import VirtualCSuite
from agentic_core.enterprise.coe_manager import COEManager
from agentic_core.enterprise.transformation_engine import TransformationEngine
from agentic_core.enterprise.iemf import IEMFIntegrator

class TestFinalSynthesis(unittest.TestCase):
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

    def test_interface_extended(self):
        interface = EntityCEOInterface()
        interface.send_purpose_alert("Alert")
        interface.provide_spiritual_guidance("Guidance")
        interface.purpose_check("p1", {"data": "test"})
        import json
        with open(interface.log_path, 'r') as f:
            log = json.load(f)
            types = [e["type"] for e in log]
            self.assertIn("PURPOSE_ALERT", types)
            self.assertIn("SPIRITUAL_GUIDANCE", types)
            self.assertIn("PURPOSE_CHECK", types)

    def test_c_suite(self):
        suite = VirtualCSuite()
        report = suite.gather_executive_council({})
        self.assertIn("CSO", report)
        self.assertIn("CTO", report)

    def test_coe_manager(self):
        manager = COEManager()
        hub = manager.synthesize_strategic_hub_input({})
        self.assertEqual(hub["inter_coe_synergy"], "HIGH")

    def test_transformation_engine(self):
        engine = TransformationEngine()
        res = engine.analyze_structural_efficiency({"tech_debt_index": 0.3})
        types = [p["type"] for p in res["proposals"]]
        self.assertIn("VERTICAL_INTEGRATION_AUDIT", types)

    def test_iemf_unified(self):
        iemf = IEMFIntegrator()
        audit = iemf.run_unified_audit()
        self.assertEqual(audit["purpose_alignment_verification"], "PASSED")

    def test_vga_m7(self):
        vga = VGAEngine()
        self.assertTrue(vga.validate_action("magnificent_seven", {"operational_profile": "frugal", "resource_waste": 0.02}))
        self.assertFalse(vga.validate_action("magnificent_seven", {"operational_profile": "frugal", "resource_waste": 0.10}))

if __name__ == "__main__":
    unittest.main()
