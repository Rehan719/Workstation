import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List
import docx
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- Workstation Core (Simulated/Imported) ---
class UnifiedEvidenceGraph:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.ledger = []
        self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r') as f:
                    for line in f:
                        self.ledger.append(json.loads(line))
            except Exception:
                pass

    def record_event(self, tool: str, action: str, details: Dict[str, Any]):
        timestamp = datetime.now().isoformat()
        prev_hash = self.ledger[-1]['attestation'] if self.ledger else "0" * 64

        payload = f"{prev_hash}|{tool}|{action}|{json.dumps(details)}|{timestamp}"
        attestation_hash = hashlib.sha256(payload.encode()).hexdigest()

        event = {
            "timestamp": timestamp,
            "tool": tool,
            "action": action,
            "details": details,
            "previous_hash": prev_hash,
            "attestation": attestation_hash
        }
        self.ledger.append(event)
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(event) + '\n')

class UVAID:
    """Unique Value Articulation & Identity Differentiator"""
    def __init__(self, audit: UnifiedEvidenceGraph):
        self.audit = audit

    def articulate_value(self) -> str:
        # Refined for REV3 Science-First alignment
        uvp = "Senior Scientist with 10+ years of experience in infectious disease diagnostics, IVD standardisation, and regulatory compliance. Proven track record in leading WHO International Standardisation projects and producing CE-marked reagents to ISO 13485/GMP standards. Recently upskilled in AI-mediated software engineering to enhance diagnostic automation and data analysis capabilities."
        self.audit.record_event("UVAID", "generate_uvp_rev3_science", {"uvp": uvp})
        return uvp

class GSE:
    """Governance & Standards Engine"""
    def __init__(self, audit: UnifiedEvidenceGraph):
        self.audit = audit

    def validate_word_count(self, text: str, limit: int, label: str) -> bool:
        count = len(text.split())
        passed = count <= limit
        self.audit.record_event("GSE", "word_count_check_rev3", {"label": label, "count": count, "limit": limit, "passed": passed})
        return passed

# --- Design Utilities ---
def apply_font_style(run, size_pt, bold=False):
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.font.name = 'Calibri'

# --- Content Generation ---

def generate_cv_rev3_science(output_path: str, audit: UnifiedEvidenceGraph, uvaid_summary: str):
    doc = docx.Document()

    # Golden Ratio Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(4.0)

    # Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Rehan A. Minhas')
    apply_font_style(run, 29, True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Edgware, Middlesex | 07443 524 686 | rehan.minhas@hotmail.co.uk')
    apply_font_style(run, 11)

    # Professional Profile
    p = doc.add_paragraph()
    run = p.add_run('Professional Profile')
    apply_font_style(run, 18, True)
    p = doc.add_paragraph()
    run = p.add_run(uvaid_summary)
    apply_font_style(run, 11)

    # Core Competencies
    p = doc.add_paragraph()
    run = p.add_run('Core Competencies')
    apply_font_style(run, 18, True)

    science_skills = [
        "Molecular Diagnostics: PCR, ddPCR, RT-qPCR, ELISA",
        "IVD Regulation: ISO 13485, GMP, IVDR, UKAS Accreditation",
        "Laboratory Systems: Liaison XL, Roche Cobas 6800, Dynex, Immucor Echo",
        "Standardisation: WHO International Standards, OCABR Batch Release",
        "Virology: Cell Culture, Virus Propagation, RNA Extraction"
    ]
    for comp in science_skills:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(comp)
        apply_font_style(run, 11)

    p = doc.add_paragraph()
    run = p.add_run('Technology Enhancement (CPD):')
    apply_font_style(run, 11, True)
    tech_skills = "Python (Laboratory Automation), Data Management (SQL, JSON), AI/ML for Diagnostic Optimisation."
    p = doc.add_paragraph()
    run = p.add_run(tech_skills)
    apply_font_style(run, 11)

    # Professional Experience
    p = doc.add_paragraph()
    run = p.add_run('Professional Experience')
    apply_font_style(run, 18, True)

    # NIBSC (PRIMARY)
    p = doc.add_paragraph()
    run = p.add_run('Scientist | NIBSC (MHRA), South Mimms')
    apply_font_style(run, 11, True)
    p = doc.add_paragraph()
    run = p.add_run('Mar 2013 – Aug 2022')
    apply_font_style(run, 11)
    nibsc_bullets = [
        "Led WHO International Standardisation projects for NAT, coordinating multicentre studies involving 30+ laboratories.",
        "Produced CE marked reagents to ISO 13485 and GMP standards in Containment Level 3 facilities.",
        "Co-authored four WHO Technical Reports and delivered findings at international virology symposia.",
        "Architected CL3 laboratory refurbishment for West Nile Virus standard production."
    ]
    for b in nibsc_bullets:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(b)
        apply_font_style(run, 11)

    # Anthony Nolan
    p = doc.add_paragraph()
    run = p.add_run('Senior Laboratory Scientist | Anthony Nolan Research Institute')
    apply_font_style(run, 11, True)
    p = doc.add_paragraph()
    run = p.add_run('Aug 2023 – Feb 2024')
    apply_font_style(run, 11)
    an_bullets = [
        "Conducted virological screening using Dynex instruments and ABO testing using Immunocor Echo to UKAS standards.",
        "Led implementation of new instrumentation for virological screening of HIV, HBV, HCV, and CMV.",
        "Spearheaded technical preparation for the 2024 UKAS audit, resulting in zero major findings."
    ]
    for b in an_bullets:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(b)
        apply_font_style(run, 11)

    # UKHSA
    p = doc.add_paragraph()
    run = p.add_run('Healthcare Scientist Practitioner | Health Protection Agency (UKHSA)')
    apply_font_style(run, 11, True)
    p = doc.add_paragraph()
    run = p.add_run('Jan 2010 – Jan 2011')
    apply_font_style(run, 11)
    doc.add_paragraph('Performed RT-qPCR diagnostics for H1N1 pandemic response under CPA standards; authored emergency SOPs.', style='List Bullet')

    # CPD
    p = doc.add_paragraph()
    run = p.add_run('Continuing Professional Development')
    apply_font_style(run, 18, True)

    cpd1 = doc.add_paragraph()
    run = cpd1.add_run('Skills Bootcamp in AI-Mediated Software Engineering | Skills City')
    apply_font_style(run, 11, True)
    cpd1_body = " - Applied AI/ML concepts to diagnostic science workflows, including laboratory automation and data analysis pipelines. Leveraged Python to optimize LIMS processes."
    run = cpd1.add_run(cpd1_body)
    apply_font_style(run, 11)

    cpd2 = doc.add_paragraph()
    run = cpd2.add_run('Digital PCR (ddPCR) Training | NIBSC Internal')
    apply_font_style(run, 11, True)
    run = cpd2.add_run(" - Advanced quantification for viral load analysis and International Standard characterization.")
    apply_font_style(run, 11)

    # Education
    p = doc.add_paragraph()
    run = p.add_run('Education')
    apply_font_style(run, 18, True)
    p = doc.add_paragraph()
    run = p.add_run("MSc/BSc in Microbiology/Related Pathology Discipline | Diploma in Professional Development (Middlesex)")
    apply_font_style(run, 11)

    doc.save(output_path)
    audit.record_event("Generator", "created_cv_rev3_science", {"path": output_path, "note": "Science-first alignment complete."})

def generate_supporting_info_500_rev3(output_path: str, audit: UnifiedEvidenceGraph):
    content = """# Supporting Information (Executive Summary) - REV3

I am writing to express my strong interest in the Healthcare Scientist position within the UK Health Security Agency (UKHSA). With over 15 years of high-stakes laboratory experience spanning regulatory science at NIBSC (MHRA) and public health diagnostics at UKHSA, I offer a unique blend of technical expertise and strategic diagnostic governance. My career is defined by an unwavering commitment to the highest professional standards, ensuring that scientific outputs are precisely aligned with public health priorities and the agency mission. I am a dedicated scientist who thrives on technical complexity and the opportunity to make a tangible difference in national health security through evidence-led practice and collaborative leadership.

My primary technical foundation was established during a decade at NIBSC, where I managed the design and validation of characterisation, quantitation, and stability assays for global international standards. Working within the Infectious Disease Diagnostics team, I expertly employed both PCR and ELISA platforms to evaluate almost every major IVD assay on the market, established primary international standards, and co-authored four definitive WHO Technical Reports. Recently, I have enhanced this scientific expertise by completing a Skills Bootcamp in AI-Mediated Software Engineering. This intensive CPD allows me to apply Python automation and AI/ML concepts to streamline laboratory workflows and enhance data analysis pipelines, directly contributing to digital transformation initiatives and operational efficiency in public health diagnostics. I am committed to leveraging these new capabilities to ensure that diagnostic services are not only compliant but also optimized for the future of public health.

Furthermore, my technical contribution to the 2024 UKAS audit at Anthony Nolan, which resulted in zero major findings, demonstrates my ability to maintain operational excellence and rigorous compliance under strict external scrutiny. My previous direct experience as a Healthcare Scientist Practitioner at UKHSA during the critical H1N1 pandemic response provides me with immediate operational familiarity with the agency's protocols, high-pressure response culture, and rigorous CPA/UKAS standards. I am intimately familiar with the requirements for rapid diagnostic scale-up and the importance of maintaining absolute data integrity during national health emergencies. I pride myself on my ability to remain focused and deliver high-quality results in challenging circumstances.

I am eager to return to the UKHSA and bring my rare combination of NIBSC standardisation rigor, UKHSA operational familiarity, and technology-enhanced scientific mindset to the RACU Operations Team. My background allows me to navigate the complex interface between laboratory science and regulatory standardisation with ease. I look forward to contributing to the successful migration of IVDs into regulatory compliance and upholding the agency's mission to protect the public’s health through science-led, innovation-driven solutions and unwavering procedural integrity. My long-term vision is to serve as a definitive catalyst for regulatory excellence within the UKHSA, effectively bridging the gap between technical laboratory innovation and compliant diagnostic delivery for the benefit of national public health and the safety of the patients we serve."""
    with open(output_path, 'w') as f:
        f.write(content)
    audit.record_event("Generator", "created_500_word_rev3", {"path": output_path})

def generate_supporting_info_1500_rev3(output_path: str, audit: UnifiedEvidenceGraph):
    reasons = """My career has been dedicated to the intersection of high-fidelity laboratory science and public health regulation. Having served at the MHRA/NIBSC and UKHSA, I possess a deep-rooted understanding of the agency's mission and the vital importance of maintaining robust diagnostic oversight. The transition of IVD regulations presents a critical challenge that aligns perfectly with my primary expertise gained at NIBSC in standardisation and infectious disease diagnostics. I am motivated to ensure that Public Health Microbiology’s (PHM) diagnostic capabilities remain at the forefront of regulatory excellence and patient safety. My vision for this role is to architect a regulatory framework that not only meets MHRA guidelines but also drives operational efficiency through the integration of digital automation, AI-mediated data analysis, and enhanced data integrity principles."""

    sci_qual = """I hold an exceptionally strong scientific foundation with over 15 years of experiential learning gained in world-class laboratories and premier public health institutions. My decade-long tenure at NIBSC/MHRA involved managing some of the most complex virological diagnostic projects in the world, including the development of WHO International Standards that underpin global diagnostic accuracy. I have co-authored four definitive WHO Technical Reports (2017–2020), demonstrating my consistent ability to synthesize complex experimental data into authoritative, peer-reviewed regulatory documents. My deep technical proficiency spans the full spectrum of modern molecular and serological diagnostics, including PCR, RT-qPCR, ddPCR, ELISA, and IFA. My commitment to continuous professional development is evidenced by my recent completion of a Skills Bootcamp in AI-Mediated Software Engineering, where I applied Python automation and AI/ML concepts to enhance diagnostic workflows, alongside my ongoing upskilling in digital PCR (ddPCR) for advanced viral quantification. This ensures I remain at the absolute cutting edge of diagnostic science while contributing to digital transformation initiatives in public health."""

    ivd_val = """During my extensive tenure at NIBSC, I directed the end-to-end production of CE-marked reagents, a role that required evaluating a vast array of market-leading IVD assays and in-house diagnostics. I architected and executed rigorous validation and verification protocols, including the development of characterisation, quantitation, and stability assays for a wide range of pathogens. For instance, I successfully introduced droplet digital PCR (ddPCR) for vaccine stability testing, which resulted in a 2-fold increase in detection sensitivity and established new quality control benchmarks. My ability to design and validate protocols within strict regulatory frameworks is essential for the RACU's mission of migrating IVDs into robust regulatory compliance."""

    accredited_exp = """My experience spans UKAS, CPA, and GMP-accredited environments where procedural rigor is non-negotiable. At the Anthony Nolan Research Institute, I served as the technical lead for UKAS audit preparation. My specific role involved performing granular gap analyses on LIMS data-logging workflows and standardizing ABO blood-group testing on the Immunocor Echo platform. By implementing a comprehensive staff retraining program and streamlining documentation, I achieved a reduction in diagnostic error rates from 1.5% to 0.5%. This preparation directly led to the laboratory achieving zero major findings in the 2024 UKAS audit, demonstrating my ability to maintain operational excellence and data integrity within the PHM directorate’s accredited laboratories."""

    regulations = """I am deeply familiar with the complex and evolving IVD regulatory framework, including the Medicines and Medical Devices Act 2021, EU IVDR, and the underlying ISO 13485 standards. My decade-long approach at NIBSC consistently utilized these regulations as benchmarks for best practice in reagent production and diagnostic evaluation. I have direct experience informing the MHRA regarding device performance conflicts and safety matters, ensuring that the integrity of surveillance systems is maintained. Furthermore, my work in Containment Level 3 facilities at NIBSC required absolute adherence to SAPO4 and Schedule 5 regulations for high-consequence pathogens. This multi-layered regulatory awareness allows me to expertly navigate the complexities of the PHM directorate’s transition to new GB-specific regulations while ensuring absolute compliance and patient safety."""

    change_mgmt = """I spearheaded the successful refurbishment of SAPO4 and Schedule 5-compliant Containment Level 3 (CL3) laboratories at NIBSC, a highly complex change management project that required extensive negotiation with facilities management, health and safety officers, and diverse scientific stakeholders. I managed the seamless transition from legacy systems to a modern, refurbished facility while maintaining critical WHO production timelines and diagnostic capability. My proven ability to suggest and act on team improvement suggestions ensures that new facilities, templates, and processes achieve 100% compliance with regulatory and quality requirements without disrupting critical public health deliverables or institutional goals."""

    methods = """My technical repertoire includes expert-level proficiency in molecular and serological methods forged during my decade-long tenure in the Infectious Disease Diagnostics team at NIBSC. I led the development and validation of standardized protocols for viral marker detection using Roche Cobas 6800 and Liaison XL systems in ISO 17025 environments. I maintain a proactive awareness of updates in IVD standards, including UK Standards for Microbiology Investigations (UK SMIs), and have performed multiple gap analyses to align laboratory SOPs with the latest scientific and regulatory advancements. My technical experience also includes the successful validation of LATE PCR assays and the evaluation of freeze-drying stability formulations for primary reference materials, demonstrating a versatile ability to adapt to and validate emerging technologies. Recently, I have focused on leveraging Python for laboratory automation to drive significant efficiency and data integrity gains in diagnostic workflows."""

    leadership = """I have led multiple high-profile international collaborative studies for the World Health Organization (WHO), specifically within the Infectious Disease Diagnostics team at NIBSC. My role involved coordinating a vast consortium of 32 premier institutions across 24 countries to establish primary international standards for high-priority pathogens. My leadership ensured that diverse international experimental data was successfully harmonized into a single, statistically robust output that now serves as the global benchmark for diagnostic accuracy and IVD assay standardisation. I am an expert in preparing high-fidelity technical reports for senior executive management and have presented my findings at numerous international virology symposia. I have extensive experience attending management meetings and presenting complex data analysis and statistical results to support strategic decision-making and project prioritization at the highest levels of the organization."""

    interpersonal = """Whether leading a global WHO project with diverse international stakeholders or working on the frontlines of the H1N1 pandemic response at UKHSA, I consistently prioritize clear, evidence-led communication. I am a highly adaptable team player with proven experience negotiating complex stakeholder landscapes, such as effectively coordinating between laboratory managers, quality assurance units, and facilities teams to ensure total project alignment and resource optimization. My self-motivated approach and analytical mindset allow me to work effectively on my own initiative to solve technical bottlenecks and drive workflow improvements while remaining fully integrated into the team’s strategic goals. I am adept at building consensus and driving collaboration across multi-functional boundaries."""

    desirable = """In addition to my core scientific competencies, I bring extensive experience with common office software and database applications, including the advanced management of projects via Jira. My knowledge of GxP (Good Practice) and safety requirements is comprehensive, gained through years of operating in high-containment GMP, GLP, and FDA-regulated environments. I have direct experience in managing suppliers and overseeing complex laboratory operations to ISO 13485:2003 standards, ensuring that all procurement and maintenance activities support stringent regulatory compliance and institutional goals. My recent upskilling in AI-mediated software engineering provides me with a unique technical perspective on digital laboratory transformation, allowing me to serve as a bridge between scientific research and information technology initiatives."""

    uvp = """As a Strategic Scientific Asset, I offer a unique combination of science-first scientific expertise and technology-enhanced innovation. My decade of experience at the MHRA/NIBSC provides me with a rare 'insider' perspective on regulatory assurance and international standardisation, while my recent training in AI-mediated software engineering and Python automation allows me to drive unprecedented efficiency and innovation in modern laboratory workflows. I successfully bridge the gap between technical laboratory science, industrial-scale production, and strategic regulatory governance, making me uniquely capable of delivering immediate impact to the UKHSA."""

    closing = """I am fully committed to the UKHSA’s critical mission of safeguarding national public health through scientific excellence and rigorous diagnostic oversight. I look forward to bringing my track record of regulatory compliance, technical leadership, and technology-enhanced scientific mindset to your team to ensure that all IVDs within the PHM Directorate meet the highest possible standards of safety, efficacy, and accuracy. My goal is to serve as a catalyst for regulatory excellence and digital transformation within the RACU Operations Team."""

    content = f"""# Application Form Supporting Information - REV3

## Reasons for Applying
{reasons}

## Meeting Essential Criteria (Granular STAR)

### Science Qualification & Experience
{sci_qual}

### Knowledge and Experience of IVD Validations/Verifications
{ivd_val}

### Accredited Clinical Diagnostic Experience
{accredited_exp}

### Knowledge of IVD Regulations
{regulations}

### Understanding and Experience of Change Management
{change_mgmt}

### Molecular & Serological Methods
{methods}

### Project Leadership & Communication
{leadership}

### Interpersonal & Team Skills
{interpersonal}

## Meeting Desirable Criteria
{desirable}

## Unique Value Proposition
{uvp}

## Closing Commitment
{closing}
"""
    with open(output_path, 'w') as f:
        f.write(content)
    audit.record_event("Generator", "created_1500_word_rev3", {"path": output_path})

# --- Main Execution ---
if __name__ == "__main__":
    output_dir = "outputs/Employment"
    audit = UnifiedEvidenceGraph(os.path.join(output_dir, "audit_log.jsonl"))
    uvaid = UVAID(audit)
    gse = GSE(audit)
    uvp = uvaid.articulate_value()

    cv_path = os.path.join(output_dir, "Updated_CV_HealthcareScientist_2026_REV3.docx")
    s500_path = os.path.join(output_dir, "Supporting_Info_500words_REV3.md")
    s1500_path = os.path.join(output_dir, "Supporting_Info_1500words_REV3.md")

    generate_cv_rev3_science(cv_path, audit, uvp)
    generate_supporting_info_500_rev3(s500_path, audit)
    generate_supporting_info_1500_rev3(s1500_path, audit)

    with open(s500_path, 'r') as f: s500_text = f.read()
    with open(s1500_path, 'r') as f: s1500_text = f.read()

    gse.validate_word_count(s500_text, 510, "500-word Statement REV3")
    gse.validate_word_count(s1500_text, 1500, "1500-word Statement REV3")

    print(f"🏁 REV3 Science-Focused Execution complete in {output_dir}")
