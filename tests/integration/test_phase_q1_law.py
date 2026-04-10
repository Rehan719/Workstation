import sys
import types
from unittest.mock import MagicMock

# Aggressive mocking of problematic dependencies
for mod in ['shap', 'yaml', 'jwt', 'matplotlib', 'matplotlib.pyplot', 'three']:
    sys.modules[mod] = MagicMock()

# Mock internal modules that have missing dependencies
sys.modules['agentic_core.triad.xai.explainer'] = MagicMock()
sys.modules['agentic_core.triad.xai.explainer'].AdaptiveXAI = object

from agentic_core.domains.law.product import LawProductGenerator
from agentic_core.omnimedia.factory import OutputFormat
import os
import json

def run_integration_test():
    print("Starting Phase Q1 Integration Test (Law Domain)...")
    generator = LawProductGenerator()

    # Valid data
    claimant_data = {
        "et1_form": {
            "claimant_name": "John Doe",
            "respondent_name": "ACME Corp",
            "claim_details": "Unfair dismissal claim..."
        },
        "acas_code": "R123456/78/90",
        "personal_data": {
            "consent": True
        }
    }

    # Test valid case
    print("Testing valid ET1 package generation...")
    result = generator.create_et1_package(claimant_data, [OutputFormat.PDF, OutputFormat.PPTX])
    print(f"Result: {result['status']}")
    if result['status'] == 'SUCCESS':
        for fmt, path in result['files'].items():
            print(f"  Generated {fmt}: {path}")
            if not os.path.exists(path):
                print(f"  FAILED: File {path} does not exist!")

    # Test invalid case with reject mode
    print("\nTesting invalid ET1 package (missing fields) in REJECT mode...")
    invalid_data = {"et1_form": {"claimant_name": "Jane Doe"}}
    result_invalid = generator.create_et1_package(invalid_data, [OutputFormat.PDF], mode="reject")
    print(f"Result: {result_invalid['status']}")
    print(f"Violations: {json.dumps(result_invalid.get('violations'), indent=2)}")

    # Test invalid case with warning mode
    print("\nTesting invalid ET1 package in WARNING mode...")
    result_warning = generator.create_et1_package(invalid_data, [OutputFormat.PDF], mode="warning")
    print(f"Result: {result_warning['status']}")

if __name__ == "__main__":
    run_integration_test()
