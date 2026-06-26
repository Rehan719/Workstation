import sys
import types
from unittest.mock import MagicMock

# Mock problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'matplotlib', 'matplotlib.pyplot', 'three']:
    sys.modules[mod] = MagicMock()

sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.omnimedia.decision_engine import OmnimediaDecisionEngine
from agentic_core.utils.data_governance import DataGovernanceModule
import os

def test_q3_foundations():
    print("Testing Phase Q3 Foundations (Data Governance + Cross-Domain)...")

    # 1. Test Data Governance
    gov = DataGovernanceModule()
    metadata = {
        "domain": "Care",
        "governance": {"sensitive_fields": ["patient_name"]}
    }

    # Allowed: Care -> Science (per default exceptions)
    res_sci = gov.check_data_governance(metadata, "Science")
    print(f"Care -> Science: {res_sci['allowed']}")

    # Blocked: Care -> Law
    res_law = gov.check_data_governance(metadata, "Law")
    print(f"Care -> Law: {res_law['allowed']} (Reason: {res_law.get('reason')})")

    # 2. Test Cross-Domain Learning (Audience similarity)
    print("Testing Cross-Domain Learning Transfer...")
    engine = OmnimediaDecisionEngine("outputs/test_q3_transfer.db")
    # Record success in Science for 'executive' audience
    engine.record_outcome("Science", "executive", "all", "html", 95.0, True)

    # Law has no history for 'executive', but should transfer from Science via audience-avg
    formats = engine.select_output_formats("Law", "executive")
    print(f"Law formats for 'executive' (transfer from Science): {[f.value for f in formats]}")

if __name__ == "__main__":
    test_q3_foundations()
