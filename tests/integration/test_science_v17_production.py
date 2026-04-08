import unittest
import sys
import os
import json

# Add v17 core to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../../scripts/Science/PatientSafety/v17/core"))

from sexta_veritas_synthesis_engine import SextaVeritasSynthesisEngine
from facilities import EthicalAIAuditEngine, SovereignDeploymentOrchestrator

class TestScienceV17Production(unittest.TestCase):
    def setUp(self):
        self.evidence = {
            "truth_i_score": 0.95,
            "truth_ii_score": 0.90,
            "truth_iii_score": 0.92,
            "truth_iv_score": 0.88,
            "truth_v_score": 0.94,
            "truth_vi_score": 0.91
        }
        self.engine = SextaVeritasSynthesisEngine()
        self.audit_engine = EthicalAIAuditEngine()
        self.orchestrator = SovereignDeploymentOrchestrator()

    def test_synthesis_engine_production(self):
        report = self.engine.calculate_convergence(self.evidence)
        self.assertIn("overall_score", report)
        self.assertGreater(report["overall_score"], 0.8)
        self.assertEqual(report["engine_version"], "v17.0-SEXTA-VERITAS")

        # Test correlation penalty
        low_procedural = self.evidence.copy()
        low_procedural["truth_iii_score"] = 0.5
        report_low = self.engine.calculate_convergence(low_procedural)
        self.assertEqual(report_low["correlation_penalty"], 0.05)

    def test_ethical_audit_production(self):
        audit_report = self.audit_engine.run_audit(self.evidence)
        self.assertEqual(audit_report["fairness_assessment"], "passed")
        self.assertTrue(audit_report["compliance"]["EU_AI_Act_2024"])
        self.assertIn("audit_id", audit_report)

    def test_sovereign_deployment_production(self):
        report = self.engine.calculate_convergence(self.evidence)
        package = self.orchestrator.package_for_deployment(report, "FDA")
        self.assertEqual(package["jurisdiction"], "FDA")
        self.assertEqual(package["compliance_checks"]["ltfu_requirement"], "15 years")

        with self.assertRaises(ValueError):
            self.orchestrator.package_for_deployment(report, "INVALID")

if __name__ == "__main__":
    unittest.main()
