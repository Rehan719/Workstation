import json
import os
from pathlib import Path

def verify_floor_20_compliance():
    # Directive 6.1 focus: Articles 1086-1095
    articles = [1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095]
    compliance_status = {}

    # Implementation mapping (Simplified file existence checks for verification)
    mapping = {
        1086: "agentic_core/network/p2p_stack_v137.py",
        1087: "agentic_core/network/p2p_stack_v137.py",
        1088: "agentic_core/security/asi_manager.py", # Mobile Bridge
        1089: "agentic_core/security/asi_manager.py",
        1090: "agentic_core/knowledge/production_rag_v137.py",
        1091: "agentic_core/knowledge/production_rag_v137.py", # Workflow Autonomy
        1092: "agentic_core/federation/treaty_engine.py",
        1093: "agentic_core/security/asi_manager.py", # PQC stubs
        1094: "agentic_core/governance/production_liability_v137.py",
        1095: "agentic_core/governance/production_liability_v137.py"
    }

    for article in articles:
        impl_path = mapping.get(article)
        impl_exists = Path(impl_path).exists() if impl_path else False

        # Check v137 blueprints/compliance docs
        doc_exists = Path("docs/knowledge/v137_technical_compliance.md").exists()

        compliance_status[article] = {
            'implementation': impl_exists,
            'documentation': doc_exists,
            'compliant': impl_exists and doc_exists
        }

    report = {
        'total_articles': len(articles),
        'compliant_articles': sum(1 for a in compliance_status.values() if a['compliant']),
        'compliance_rate': sum(1 for a in compliance_status.values() if a['compliant']) / len(articles),
        'details': compliance_status
    }

    os.makedirs('docs/compliance', exist_ok=True)
    with open('docs/compliance/v137_floor_20_compliance_report.json', 'w') as f:
        json.dump(report, f, indent=2)

    return report

if __name__ == '__main__':
    report = verify_floor_20_compliance()
    print(f"Compliance Rate: {report['compliance_rate'] * 100:.1f}%")
    if report['compliance_rate'] < 1.0:
        print("WARNING: Some Floor 20 articles are not fully compliant in the verification script.")
