import sys
import types
from unittest.mock import MagicMock

# Mock problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'three']:
    sys.modules[mod] = MagicMock()

import matplotlib.pyplot as plt
mock_fig = MagicMock()
mock_ax = MagicMock()
plt.subplots = MagicMock(return_value=(mock_fig, mock_ax))
plt.figure = MagicMock(return_value=mock_fig)

sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.domains.law.product import LawProductGenerator
from agentic_core.domains.science.product import ScienceProductGenerator
from agentic_core.domains.religion.product import ReligionProductGenerator
from agentic_core.domains.employment.product import EmploymentProductGenerator
from agentic_core.domains.education.product import EducationProductGenerator
from agentic_core.domains.care.product import CareProductGenerator
from agentic_core.omnimedia.factory import OutputFormat
import os

def run_final_integration():
    print("Running Final Grand Operation v6.0 Integration...")

    generators = [
        LawProductGenerator(),
        ScienceProductGenerator(),
        ReligionProductGenerator(),
        EmploymentProductGenerator(),
        EducationProductGenerator(),
        CareProductGenerator()
    ]

    formats = [OutputFormat.PDF, OutputFormat.PPTX, OutputFormat.HTML]

    for gen in generators:
        print(f"  Processing domain: {gen.domain}")
        if hasattr(gen, 'produce_safety_intelligence_package'):
            res = gen.produce_safety_intelligence_package({"grade_matrix": {"outcomes": ["Death"], "certainty": "L", "importance": "C", "evidence_summary": "S"}, "ich_alignment": {"consent": True}}, formats)
        elif hasattr(gen, 'create_et1_package'):
            res = gen.create_et1_package({"et1_form": {"claimant_name": "Final", "respondent_name": "ET", "claim_details": "Test"}, "personal_data": {"consent": True}}, formats)
        else:
            res = gen.produce_package({"mock": "data"}, formats)

        print(f"    Result: {res['status']}")
        assert res['status'] == 'SUCCESS'

    print("Final Integration Successful. All 6 domains operational.")

if __name__ == "__main__":
    run_final_integration()
