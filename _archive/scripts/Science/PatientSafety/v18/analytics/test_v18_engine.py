import unittest
import numpy as np
from scripts.Science.PatientSafety.v18.analytics.omnia_veritas_engine import OmniaVeritasEngine, TruthDimension

class TestOmniaVeritasEngine(unittest.TestCase):
    def setUp(self):
        self.engine = OmniaVeritasEngine()

    def test_calculate_convergence_structure(self):
        report = self.engine.calculate_convergence({}, {"assimilation_ratio": 0.98})
        self.assertIn('overall_convergence_score', report)
        self.assertIn(TruthDimension.CONVERGENT, report['dimension_scores'])
        self.assertEqual(len(report['dimension_scores']), 7)

    def test_high_convergence_score(self):
        # With high base evidence and high assimilation, score should be high
        base_evidence = {
            'objective': 0.95,
            'subjective': 0.98,
            'procedural': 0.90,
            'temporal': 0.92,
            'predictive': 0.95,
            'ethical': 0.96
        }
        report = self.engine.calculate_convergence(base_evidence, {"assimilation_ratio": 1.0})
        self.assertGreater(report['overall_convergence_score'], 0.9)

if __name__ == '__main__':
    unittest.main()
