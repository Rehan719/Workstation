import sys
import types
from unittest.mock import MagicMock

# Mock problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'matplotlib', 'matplotlib.pyplot', 'three']:
    sys.modules[mod] = MagicMock()

sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.constitutional.fallback import FallbackProtocol
from agentic_core.domains.law.product import LawProductGenerator
from agentic_core.omnimedia.factory import OutputFormat
import os

def test_chaos_scenario():
    print("Executing Phase Q3 Chaos Tests...")
    law_gen = LawProductGenerator()

    # Scenario: Rapid violations leading to suspension (Level 4)
    print("  Testing Level 4 Escalation (Suspension)...")
    invalid_data = {"et1_form": {"claimant_name": "Chaos User"}}

    # 10 violations trigger Level 4
    for i in range(10):
        res = law_gen.create_et1_package(invalid_data, [OutputFormat.PDF], mode="reject")
        if res["status"] == "SUSPENDED":
            print(f"  Domain suspended at iteration {i+1}. Success.")
            break

    assert res["status"] == "SUSPENDED"
    print("Chaos Tests Passed.")

if __name__ == "__main__":
    test_chaos_scenario()
