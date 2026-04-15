import asyncio
import yaml
import sys
import os

# Add relevant paths to sys.path for testing
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(base_dir, "packages/constitutional-core"))
sys.path.append(base_dir)

from vsb_constitutional import TruthEngine, GaaSValidatorV3, UEGLogger, DecaVeritasOrchestrator

async def test_constitutional_compliance():
    print("Starting Constitutional Validation Harness...")

    # Load Business genome
    with open("config/constitutional/domains/core_business.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Initialize Orchestrator
    orchestrator = DecaVeritasOrchestrator(config, {})

    # Run a test process
    print("Executing Core Business Process...")
    input_data = {"queries": ["strategic risk assessment 2026"]}
    bundle = await orchestrator.orchestrate_core_process(input_data)

    # Validate Compliance
    print("Validating GaaS v3 Compliance...")
    gov_report = bundle["governance_report"]
    if gov_report["compliant"]:
        print("✅ GaaS v3 Validation Passed.")
    else:
        print(f"❌ GaaS v3 Validation Failed: {gov_report['violations']}")
        return False

    # Validate Truth Dimensions
    print("Checking Truth Dimensions...")
    dimensions = bundle["truth_report"]["dimensions_applied"]
    required_dims = ["I_OBJECTIVE_RECORD", "III_PROCEDURAL", "VI_SYSTEMIC_ETHICAL"]
    for rd in required_dims:
        if rd not in dimensions:
             print(f"❌ Missing Truth Dimension: {rd}")
             return False
    print("✅ All required Truth Dimensions applied.")

    # Validate Omnimedia Injection
    print("Verifying Omnimedia Outputs...")
    for fmt in ["pdf", "docx", "html"]:
        if fmt not in bundle["outputs"]:
            print(f"❌ Missing format in outputs: {fmt}")
            return False
        if not os.path.exists(bundle["outputs"][fmt]):
            print(f"❌ Output file does not exist: {bundle['outputs'][fmt]}")
            return False
    print("✅ Omnimedia injection successful.")

    print("--- CONSTITUTIONAL VALIDATION SUCCESSFUL ---")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_constitutional_compliance())
    sys.exit(0 if success else 1)
