import asyncio
import logging
from agentic_core.enterprise.policy import PolicyCoE

async def verify_governance_systems():
    logging.basicConfig(level=logging.INFO)
    policy = PolicyCoE()

    # 1. Verify QMS
    print("Verifying QMS...")
    policy.qms.enforce_gate("CODE_QUALITY", "Jules", True, "Code looks good.")
    policy.qms.enforce_gate("NO_STUBS", "Jules", True, "No placeholders found.")
    cert = policy.qms.generate_provenance_certificate("Governance Verification")
    print(f"QMS Certificate: {cert['status']}")
    assert cert["status"] == "UNCERTIFIED" # Since not all gates are passed yet

    # 2. Verify DCS
    print("Verifying DCS...")
    policy.dcs.check_in("TEST_DOC", "Test Document", "Initial content", "Jules", "First commit")
    history = policy.dcs.get_document_history("TEST_DOC")
    print(f"DCS History Length: {len(history)}")
    assert len(history) == 1

    # 3. Verify BMS
    print("Verifying BMS...")
    policy.bms.add_okr("Deliver v120.0", [{"text": "Completion", "target": 1.0, "current": 0.5, "unit": "percentage"}])
    report = policy.bms.generate_performance_report()
    print(f"BMS Global PAS: {report['global_pas']}")
    assert report["global_pas"] >= 0.95

    # 4. Verify EMS
    print("Verifying EMS...")
    policy.ems.log_evolution_event("GOVERNANCE_START", "Initialized business systems", 0.9)
    policy.ems.track_sustainability(2.0, 100.0, True)
    evo_report = policy.ems.generate_evolution_report()
    print(f"EMS Status: {evo_report['sustainability_status']}")
    assert evo_report["sustainability_status"] == "OPTIMAL"

    # 5. Verify New CoEs
    print("Verifying new CoEs...")
    policy.webscrape_coe.optimize_sensory_gating(98.5)
    sec_status = policy.agentic_gov_coe.get_security_status()
    print(f"Security Fidelity: {sec_status['immune_system_fidelity']}")
    assert sec_status["immune_system_fidelity"] >= 0.99

    print("Governance Systems Verification SUCCESSFUL.")

if __name__ == "__main__":
    asyncio.run(verify_governance_systems())
