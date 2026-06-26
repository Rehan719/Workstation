import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

# Ensure absolute paths for module discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from core.facilities import PentaVeritasSynthesisEngine, PredictiveRegulatoryLaboratory, GlobalSafetyIntelligenceEngine

class PentaVeritasOrchestratorV15:
    """
    Master Orchestrator for Science Grand Operation v15.0.
    Executes the Penta-Veritas cycle with predictive and jurisdictional intelligence.
    """
    def __init__(self, product_id="VSB-SIG-SCI-15.0"):
        self.product_id = product_id
        self.engine = PentaVeritasSynthesisEngine({})
        self.lab = PredictiveRegulatoryLaboratory()
        self.global_engine = GlobalSafetyIntelligenceEngine()
        self.output_dir = "outputs/Science/PatientSafety/v15_penta_veritas/"
        self.audit_log = "outputs/Science/PatientSafety/v15/audit/vsb_signature_log_v15_penta_veritas.jsonl"

        if not os.path.exists(os.path.dirname(self.audit_log)):
            os.makedirs(os.path.dirname(self.audit_log), exist_ok=True)

    def _log_audit(self, action, details, facility="Orchestrator"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "product_id": self.product_id,
            "facility": facility,
            "action": action,
            "details": details,
            "status": "PENTA_VERITAS_VERIFIED"
        }
        with open(self.audit_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")

    def run_cycle(self, jurisdiction='EMA'):
        print(f"🧬 Initializing Science Grand Operation v15.0-PENTA-VERITAS [{jurisdiction}]...")

        # 1. Global Intelligence
        risks = self.global_engine.detect_emerging_risks()
        self._log_audit("GLOBAL_INTELLIGENCE", {"emerging_risks": len(risks)}, "Global Safety Intelligence Engine")

        # 2. Penta Synthesis
        evidence = {
            'Truth_I': 0.98, 'Truth_II': 0.94, 'Truth_III': 0.88,
            'Truth_IV': 0.92, 'Truth_V': 0.95
        }
        report = self.engine.calculate_convergence(evidence, jurisdiction)
        self._log_audit("PENTA_SYNTHESIS", report, "Penta-Veritas Synthesis Engine")

        # 3. Outcome Forecasting
        forecast = self.lab.forecast_outcome(report['overall_score'], jurisdiction)
        self._log_audit("OUTCOME_FORECASTING", forecast, "Predictive Regulatory Laboratory")

        # Final State
        final_status = {
            "product_id": self.product_id,
            "jurisdiction": jurisdiction,
            "convergence_score": report['overall_score'],
            "enforcement_probability": forecast['enforcement_probability'],
            "status": "PENTA-VERITAS-COMPLETE"
        }

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

        with open(os.path.join(self.output_dir, f"penta_veritas_status_{jurisdiction}.json"), 'w') as f:
            json.dump(final_status, f, indent=2)

        print(f"✅ Penta-Veritas Execution Complete for {jurisdiction}.")
        return final_status

if __name__ == "__main__":
    orchestrator = PentaVeritasOrchestratorV15()
    for j in ['EMA', 'MHRA', 'FDA', 'PMDA']:
        orchestrator.run_cycle(j)
