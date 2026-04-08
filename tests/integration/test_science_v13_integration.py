import unittest
import os
import sys

# Ensure absolute paths for module discovery
# The test is in tests/integration/ (2 levels down)
# Repo root is 3 levels up from this script (or 2 if tests/ is in root)
# Let's use a more robust way to find the root.
def find_repo_root():
    path = os.path.abspath(__file__)
    while not os.path.exists(os.path.join(os.path.dirname(path), 'README.md')) and os.path.dirname(path) != path:
        path = os.path.dirname(path)
    return os.path.dirname(path) if os.path.exists(os.path.join(os.path.dirname(path), 'README.md')) else os.path.dirname(path)

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if repo_root not in sys.path:
    sys.path.append(repo_root)

from scripts.Science.PatientSafety.v13.core.facilities import TemporalSynthesisEngine
from scripts.Science.PatientSafety.v13.integrations.adapters import PubMedAdapter

class TestScienceV13Integration(unittest.TestCase):
    def setUp(self):
        self.config = {
            'temporal_weights': {'truth_I': 0.30, 'truth_II': 0.25, 'truth_III': 0.25, 'truth_IV': 0.20}
        }
        self.engine = TemporalSynthesisEngine(self.config)
        self.pubmed = PubMedAdapter()

    def test_temporal_synthesis_engine(self):
        evidence_set = {
            "truth_I_reliability": 1.0,
            "truth_II_credibility": 1.0,
            "truth_III_compliance": 1.0,
            "truth_IV_accuracy": 1.0
        }
        report = self.engine.analyze_evidence(evidence_set)
        # 0.3 + 0.25 + 0.25 + 0.20 + 0.15*0.92 = 1.0 + 0.138 = 1.138 -> capped at 1.0
        self.assertEqual(report['overall_score'], 1.0)
        self.assertEqual(report['dimension_scores']['I'], 1.0)

    def test_pubmed_adapter_mock_data(self):
        results = self.pubmed.search_literature("AAV")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['author'], "Wu et al.")

if __name__ == '__main__':
    unittest.main()
