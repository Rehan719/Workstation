import sys
import types
from unittest.mock import MagicMock

# Mock problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'matplotlib', 'matplotlib.pyplot', 'three']:
    sys.modules[mod] = MagicMock()

sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.omnimedia.decision_engine import OmnimediaDecisionEngine
import os

def test_truth_v():
    print("Testing Truth V Predictive Asset Selection...")
    engine = OmnimediaDecisionEngine("outputs/test_q3_truth_v.db")

    # Record some history
    engine.record_outcome("Law", "judge", "video", "pdf", 90.0, True)
    engine.record_outcome("Law", "judge", "video", "pdf", 95.0, True)
    engine.record_outcome("Law", "judge", "video", "pdf", 88.0, True)
    engine.record_outcome("Law", "judge", "infographic", "pdf", 40.0, True)
    engine.record_outcome("Law", "judge", "video", "pdf", 92.0, True)

    # Predict
    best = engine.predict_optimal_asset("Law", "judge")
    print(f"Predicted best asset for Law/Judge: {best}")
    assert best == "video"

if __name__ == "__main__":
    test_truth_v()
