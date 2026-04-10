
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from scripts.Science.PatientSafety.v17_1.core.septima_veritas_engine import SeptimaVeritasEngine, PeerReviewSimulator

def test_engine():
    engine = SeptimaVeritasEngine()
    evidence = {
        "truth_i_score": 0.95,
        "truth_ii_score": 0.90,
        "truth_iii_score": 0.92,
        "truth_iv_score": 0.88,
        "truth_v_score": 0.91,
        "truth_vi_score": 0.89,
        "truth_vii_score": 0.94,
        "methodological_quality": 0.95,
        "uncertainty_level": 0.05,
        "reproducibility": 0.98
    }

    report = engine.calculate_convergence(evidence)
    print(f"Overall Score: {report['overall_score']}")
    assert report['overall_score'] > 0.9
    assert report['status'] == "Verified Scientific Excellence"

    simulator = PeerReviewSimulator()
    review = simulator.simulate(report)
    print(f"Recommendation: {review['recommendation']}")
    assert review['recommendation'] == "Accept as is"
    print("Test Passed!")

if __name__ == "__main__":
    test_engine()
