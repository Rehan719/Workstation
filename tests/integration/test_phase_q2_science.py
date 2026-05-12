import sys
import types
from unittest.mock import MagicMock

# Mock problematic dependencies
for mod in ['shap', 'yaml', 'jwt']:
    sys.modules[mod] = MagicMock()

sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.domains.science.product import ScienceProductGenerator
from agentic_core.omnimedia.factory import OutputFormat
import os

def test_science_product():
    print("Testing Science Domain Product Generation (Q2)...")
    generator = ScienceProductGenerator()

    input_data = {
        "grade_matrix": {
            "outcomes": ["Death", "Hospitalization"],
            "certainty": "Low",
            "importance": "Critical",
            "evidence_summary": "Limited data from phase 1."
        },
        "regulatory_info": "FDA Secondary Malignancy Alert 2024",
        "ich_alignment": {"consent": True}
    }

    result = generator.produce_safety_intelligence_package(input_data, [OutputFormat.PDF, OutputFormat.HTML])
    print(f"Result: {result['status']}")
    if result['status'] == 'SUCCESS':
        for fmt, path in result['files'].items():
            print(f"  Generated {fmt}: {path}")
            if os.path.exists(path):
                print(f"  Verified {fmt} exists.")
            else:
                print(f"  FAILED: {path} not found.")

if __name__ == "__main__":
    test_science_product()
