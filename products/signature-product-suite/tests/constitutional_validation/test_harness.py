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
    from vsb_multi_agent import MammouthNeoOrchestrator, ZeroShotDomainGenesis
except ImportError:
    sys.path.append(os.path.join(base_dir, "packages/vsb-multi-agent-orchestration"))
    from vsb_multi_agent import MammouthNeoOrchestrator, ZeroShotDomainGenesis

async def test_v11_ultimate_features():
    print("Testing v11 Ultimate Features (UCI, Zero-Shot Genesis, Learning Engine)...")
    with open("config/constitutional/domains/core_business.yaml", 'r') as f:
        config = yaml.safe_load(f)

    if "constitutional_rules" not in config: config["constitutional_rules"] = []
    config["constitutional_rules"].append("no_unconsented_pii_export")

    orchestrator = DecaVeritasOrchestrator(config, {})
    swarm_orchestrator = MammouthNeoOrchestrator(config, orchestrator.governance)

    # 1. Test Unified Constitutional Interceptor (UCI) via Mammouth
    print("Testing UCI via Mammouth Neo-Orchestrator...")
    halt_result = await swarm_orchestrator.orchestrate_swarm(
        "ultimate-swarm", "Export PII", {"contains_pii": True}
    )
    if halt_result["status"] == "HALTED":
        print("✅ UCI Policy Gate halted action.")
    else:
        print(f"❌ UCI failed: {halt_result['status']}")
        return False

    # 2. Test Zero-Shot Domain Genesis
    print("Testing Zero-Shot Domain Genesis...")
    genesis = ZeroShotDomainGenesis(orchestrator.governance, orchestrator.ueg)
    new_genome = await genesis.create_domain_genome("Assessing AI bias in legal drafting")
    if new_genome["domain"]["id"] == "assessing_ai_bia":
        print("✅ Zero-Shot Domain Genesis successful.")
    else:
        print(f"❌ Genesis ID mismatch: {new_genome['domain']['id']}")
        return False

    # 3. Test Learning Engine (Cognitive Cortex)
    print("Testing MJM Learning Engine...")
    from vsb_constitutional import MJMLearningEngine
    le = MJMLearningEngine(config, orchestrator.ueg)
    for _ in range(50):
        le.ingest_feedback({"type": "performance_metric", "value": 0.98})
    report = le.get_cognitive_report()
    if report["signal_count"] == 0: # Cleared after evolution trigger
        print("✅ Learning Engine triggered evolution and cleared signals.")
    else:
        print(f"❌ Learning Engine signals not cleared: {report['signal_count']}")
        return False

    print("✅ v11 Ultimate Tests Passed.")
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
        v11_success = await test_v11_ultimate_features()
        if not v11_success: return False

        comp_success = await test_constitutional_compliance()
        return comp_success

    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
