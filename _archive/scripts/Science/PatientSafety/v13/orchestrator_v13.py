import os
from temporal_synthesis_engine import TemporalSynthesisEngineV13

def run_orchestrator():
    print("🚀 Initializing Science Grand Operation v13.0 Orchestrator...")
    output_dir = "outputs/Science/PatientSafety/v13_quadra_veritas/"
    os.makedirs(output_dir, exist_ok=True)

    engine = TemporalSynthesisEngineV13(output_dir)

    # Truth I: Objective Record
    engine.ingest_evidence("Truth_I", "Wu et al. 2025: Germ cell transduction metrics; >5% in gonadal tissue.")
    engine.ingest_evidence("Truth_I", "Chazarin et al. 2026: mRNA-induced proteomic alterations; complement pathway activation.")
    engine.ingest_evidence("Truth_I", "FDA Guidance 2024: Long-term follow-up requirements for gene therapy.")

    # Truth II: Subjective Narrative
    engine.ingest_evidence("Truth_II", "Clinical whistleblower: Inadequate reporting of adverse events in early AAV trials.")
    engine.ingest_evidence("Truth_II", "Patient Advocacy Group: Demand for intergenerational safety transparency.")

    # Truth III: Procedural Compliance
    engine.ingest_evidence("Truth_III", "ICH S5(R3) compliance gap: Germline risk assessment protocols.")
    engine.ingest_evidence("Truth_III", "Trial design failure: Omission of longitudinal immune monitoring.")

    # Truth IV: Temporal-Dynamic Intelligence
    engine.ingest_evidence("Truth_IV", "Regulatory Trajectory: Forecasted MHRA/EMA harmonization on mRNA safety standards.")
    engine.ingest_evidence("Truth_IV", "Liability Risk: 70% increase in predicted settlement costs for long-term immunogenicity.")

    report_path = engine.save_report()
    print(f"✅ Orchestration complete. Report saved to {report_path}")

if __name__ == "__main__":
    run_orchestrator()
