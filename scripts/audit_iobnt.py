import sys
import os
import logging
from agentic_core.simulation.iobnt import IoBNTIntegrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IoBNT_Audit")

def main():
    print("🧬 Jules AI: Running IoBNT Compliance Audit (v125.1)...")
    integrator = IoBNTIntegrator()
    audit_results = integrator.run_compliance_audit()

    print(f"Compliance Score: {audit_results['compliance_score']}")
    for scheme, status in audit_results['verified_schemes'].items():
        print(f" - {scheme.capitalize()}: {status}")

    if audit_results['compliance_score'] == 1.0:
        print("✅ IoBNT Protocols Verified.")
        sys.exit(0)
    else:
        print("❌ Compliance Audit FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
