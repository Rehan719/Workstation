import asyncio
import yaml
import sys
import os

# Add relevant paths to sys.path for testing
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(base_dir, "packages/constitutional-core"))
sys.path.append(base_dir)

try:
    from vsb_constitutional import TruthEngine, GaaSValidatorV3, UEGLogger, DecaVeritasOrchestrator
except ImportError:
    sys.path.append(os.path.join(base_dir, "packages/constitutional-core"))
    from vsb_constitutional import TruthEngine, GaaSValidatorV3, UEGLogger, DecaVeritasOrchestrator

try:
    from vsb_multi_agent import MammouthConstitutionalOrchestrator
except ImportError:
    sys.path.append(os.path.join(base_dir, "packages/vsb-multi-agent-orchestration"))
    from vsb_multi_agent import MammouthConstitutionalOrchestrator

async def test_v10_circuit_breaker_and_policy():
    print("Testing v10 Constitutional Circuit Breaker and Policy Gate...")
    with open("config/constitutional/domains/core_business.yaml", 'r') as f:
        config = yaml.safe_load(f)

    # Enable a strict rule
    if "constitutional_rules" not in config:
        config["constitutional_rules"] = []
    config["constitutional_rules"].append("no_unconsented_pii_export")

    orchestrator = DecaVeritasOrchestrator(config, {})
    swarm_orchestrator = MammouthConstitutionalOrchestrator(config, orchestrator.governance)

    # 1. Test Policy Gate Halt
    print("Testing Policy Gate Halt (PII Export)...")
    halt_result = await swarm_orchestrator.orchestrate_swarm(
        "pii-swarm",
        "Export customer data",
        {"queries": ["export data"], "contains_pii": True}
    )

    # Since Mammouth mock calls _run_agent_interactions which doesn't check policy
    # but the orchestrator.orchestrate_swarm DOES check before running.
    # WAIT, I need to check how I implemented it in MammouthConstitutionalOrchestrator.

    if halt_result["status"] == "HALTED":
         print("✅ Policy Gate halted prohibited action.")
    else:
         print(f"❌ Policy Gate failed to halt action: {halt_result['status']}")
         return False

    # 2. Test Circuit Breaker Trip
    print("Testing Circuit Breaker Trip (Manual Violation)...")
    # Manually record violations to trip breaker
    orchestrator.governance.circuit_breaker.record_event(success=False, is_violation=True)

    if orchestrator.governance.circuit_breaker.should_halt():
        print("✅ Circuit Breaker tripped after violation.")
    else:
        print("❌ Circuit Breaker failed to trip.")
        return False

    print("✅ v10 Governance Tests Passed.")
    return True

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
    # Add packages to path
    sys.path.append(os.path.join(base_dir, "packages/constitutional-core"))
    sys.path.append(os.path.join(base_dir, "packages/vsb-multi-agent-orchestration"))

    async def run_all_tests():
        v10_success = await test_v10_circuit_breaker_and_policy()
        if not v10_success: return False

        comp_success = await test_constitutional_compliance()
        return comp_success

    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
