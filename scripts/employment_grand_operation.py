import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List
import docx
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- Workstation Core (Persistent Repository Integration) ---
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
            "timestamp": timestamp, "tool": tool, "action": action, "details": details,
            "previous_hash": prev_hash, "attestation": attestation_hash
        }
        self.ledger.append(event)
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(event) + '\n')

class ExperienceEngine:
    def __init__(self, repo_path: str):
        with open(repo_path, 'r') as f:
            self.data = json.load(f)

    def get_publications(self): return self.data.get('publications', [])
    def get_skills(self): return self.data.get('skills', [])

# --- Design Parameters (Golden Ratio v2) ---
PHI = 1.618
BODY_SIZE = 11
SUBHEADER_SIZE = round(BODY_SIZE * PHI) # ~18
HEADER_SIZE = round(SUBHEADER_SIZE * PHI) # ~29
SECTION_SPACING = Pt(round(12 * PHI)) # ~19pt

def apply_monochrome_style(run, size_pt, bold=False):
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    run.font.name = 'Calibri'

# --- Asset Generation (REV4) ---

def generate_cv_rev4(output_path: str, audit: UnifiedEvidenceGraph, engine: ExperienceEngine):
    doc = docx.Document()

    # Golden Ratio Margins (Inner/Outer)
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5 * PHI) # ~4.0cm

    # Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Rehan A. Minhas')
    apply_monochrome_style(run, HEADER_SIZE, True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Edgware, Middlesex | 07443 524 686 | rehan.minhas@hotmail.co.uk')
    apply_monochrome_style(run, BODY_SIZE)

    # Sections helper
    def add_section(title, content_list=None, text=None):
        doc.add_paragraph().paragraph_format.space_before = SECTION_SPACING
        p = doc.add_paragraph()
        run = p.add_run(title)
        apply_monochrome_style(run, SUBHEADER_SIZE, True)

        if text:
            p = doc.add_paragraph()
            run = p.add_run(text)
            apply_monochrome_style(run, BODY_SIZE)

        if content_list:
            for item in content_list:
                p = doc.add_paragraph(style='List Bullet')
                run = p.add_run(item)
                apply_monochrome_style(run, BODY_SIZE)

    # 1. Profile
    profile = "Senior Scientist with 10+ years of high-stakes expertise in infectious disease diagnostics and IVD standardisation at NIBSC/MHRA. Proven lead in established WHO International Standards and delivering zero-non-conformity audits (UKAS/GMP). Recently upskilled in AI-mediated software engineering to architect advanced automation and data analysis solutions for public health science."
    add_section("Professional Profile", text=profile)

    # 2. Competencies (Data-Driven)
    all_skills = engine.get_skills()
    # Categorise skills dynamically
    primary_tech = [s for s in all_skills if s in ['AKTA', 'Roche Cobas 6800', 'Liaison XL', 'ddPCR', 'RT-qPCR', 'ABI 7500', 'Qiagen Rotagene']]
    regulatory = [s for s in all_skills if 'ISO' in s or s in ['GMP', 'GLP', 'ALCOA+', 'UKAS', 'SAPO4']]

    comp_list = [
        f"Molecular Platforms: {', '.join(primary_tech[:5])}",
        f"Quality Governance: {', '.join(regulatory[:5])}",
        "Global Standardisation: Lead on multiple WHO International Study consortia",
        "Clinical Diagnostics: PCR/ELISA for high-containment pathogens (CL3)"
    ]
    add_section("Core Competencies", content_list=comp_list)

    # 3. Experience (Data-Driven from Knowledge Repository)
    add_section("Professional Experience")

    master_data = {}
    master_path = "knowledge/employment/ontology/experience_master.json"
    if os.path.exists(master_path):
        with open(master_path, "r") as f:
            master_data = json.load(f)

    for role in master_data.get("roles", []):
        p = doc.add_paragraph()
        run = p.add_run(f"{role['title']} | {role['organisation']}")
        apply_monochrome_style(run, BODY_SIZE, True)
        p = doc.add_paragraph(role['period'])
        apply_monochrome_style(p.runs[0] if p.runs else p.add_run(role['period']), BODY_SIZE)
        for bullet in role.get("bullets", []):
            p = doc.add_paragraph(style='List Bullet')
            run = p.add_run(bullet)
            apply_monochrome_style(run, BODY_SIZE)

    # Anthony Nolan
    p = doc.add_paragraph()
    run = p.add_run('Senior Laboratory Scientist | Anthony Nolan Institute')
    apply_monochrome_style(run, BODY_SIZE, True)
    p = doc.add_paragraph('Aug 2023 – Feb 2024')
    apply_monochrome_style(p.runs[0] if p.runs else p.add_run('Aug 2023 – Feb 2024'), BODY_SIZE)
    an_bullets = [
        "Optimized ABO blood-group testing on Immunocor Echo, reducing error rates by 66%.",
        "Lead technical preparation for 2024 UKAS audit (Zero major findings).",
        "Evaluated Diasorin Liaison XL chemiluminescent ELISA for viral markers."
    ]
    for b in an_bullets:
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(b)
        apply_monochrome_style(run, BODY_SIZE)

    # 4. Publications (Unique only)
    raw_pubs = engine.get_publications()
    unique_pubs = []
    seen = set()
    for p in raw_pubs:
        # Simple fuzzy match to avoid duplicate entries
        key = p.lower()[:30]
        if key not in seen and len(p) > 50:
            unique_pubs.append(p)
            seen.add(key)

    add_section("Selected Publications", content_list=unique_pubs[:5])

    # 5. CPD
    cpd_text = "Skills Bootcamp in AI-Mediated Software Engineering (2024): Applied Python/AI to diagnostic automation. Digital PCR (ddPCR) Specialist Training. Diploma in Professional Development."
    add_section("Continuing Professional Development", text=cpd_text)

    doc.save(output_path)
    audit.record_event("Generator", "created_cv_rev4", {"path": output_path, "design": "Golden Ratio v2 Monochrome"})

def generate_supporting_info_500_rev4(output_path: str, audit: UnifiedEvidenceGraph):
    content = """# Supporting Information (Executive Summary) - REV4

I am writing to express my strong interest in the Healthcare Scientist position within the UK Health Security Agency (UKHSA). With over 15 years of high-stakes laboratory experience spanning industrial biomanufacturing at Lonza Biologics, regulatory science at NIBSC (MHRA), and public health diagnostics at UKHSA, I offer a unique "Interdisciplinary Bridge" perfectly aligned with the RACU Operations Team. My career is defined by a commitment to the highest professional standards and a systems-thinking approach to diagnostic governance, ensuring scientific outputs are always aligned with public health priorities and the agency mission.

My most recent tenure as a Biotechnologist at Lonza Biologics has further refined my industrial GMP competence and operational agility. I managed the end-to-end operation of AKTA chromatography systems and Sartorius columns, executing complex downstream bioprocessing workflows (IPF, VRF, UF/DF) within high-fidelity clean-room settings. My experience maintaining ALCOA+ compliant batch records and supporting CAPA investigations directly addresses the agency's requirement for absolute procedural rigor and data integrity. This current industrial expertise, combined with my previous tenure at NIBSC orchestrating the production of CE-marked reagents under ISO 13485, provides a powerful foundation for the PHM directorate’s migration to the new GB-specific IVD regulatory framework.

At NIBSC, I spearheaded global NAT harmonization projects for the WHO, coordinating a consortium of 32 institutions across 24 countries to establish primary international standards for high-priority pathogens. This role required delivering high-fidelity data analysis and comprehensive technical reports for senior executive management, aligning with the strategic communication and project leadership requirements of this post. Furthermore, my contribution to the 2024 UKAS audit at Anthony Nolan, which resulted in zero major findings, demonstrates my ability to deliver operational excellence under external scrutiny.

I am eager to return to the UKHSA and bring my rare combination of industrial precision, regulatory depth, and public-service dedication to the RACU. I look forward to contributing to the successful migration of IVDs into regulatory compliance and upholding the agency's mission to protect the public’s health through science-led, innovation-driven solutions and unwavering procedural integrity."""
    with open(output_path, 'w') as f:
        f.write(content)
    audit.record_event("Generator", "created_500_word_rev4", {"path": output_path})

def generate_supporting_info_1500_rev4(output_path: str, audit: UnifiedEvidenceGraph):
    content = """# Application Form Supporting Information - REV4

## Reasons for Applying
My career centers on high-fidelity laboratory science and public health regulation. Serving at MHRA/NIBSC, UKHSA, and Lonza Biologics, I understand the agency's mission and industrial diagnostic production. The IVD regulatory transition aligns with my expertise in ISO 13485, GMP, and IVDR. I am motivated to ensure PHM’s diagnostic capabilities lead in regulatory excellence and patient safety. I view this role as an opportunity to strengthen the bridge between laboratory operations and regulatory assurance. My previous experience during pandemic responses instilled a profound commitment to UKHSA's strategic goals and operational excellence.

## Meeting Essential Criteria (Granular STAR)

### Science Qualification & Experience
I hold an exceptionally strong scientific foundation with over 15 years of experiential learning gained in world-class laboratories and premier public health institutions. My decade-long tenure at NIBSC/MHRA involved managing complex virological diagnostic projects, including the development of WHO International Standards. I have co-authored four definitive WHO Technical Reports (2017–2020), demonstrating my ability to synthesize complex data into authoritative regulatory documents. My technical proficiency spans modern molecular and serological diagnostics, including PCR, RT-qPCR, ddPCR, ELISA, and IFA. Recently, I have focused on leveraging AI/ML to enhance diagnostic automation and data analysis, ensuring my technical toolkit remains at the cutting edge. This blend of traditional excellence and modern computational awareness makes me uniquely qualified for the RACU.

### Knowledge and Experience of IVD Validations/Verifications
At Lonza Biologics, I managed the technical execution of downstream bioprocessing, including set-up and post-run verification for AKTA chromatography systems and Sartorius bind-and-elute columns. This industrial validation experience is a direct extension of my work at NIBSC, where I directed the end-to-end production of CE-marked reagents. I architected validation protocols per MHRA Annex 6, coordinating cross-functional QA and Regulatory Affairs teams to ensure all IVDs met stringent performance specifications. I successfully introduced droplet digital PCR (ddPCR) for vaccine stability testing, which involved designing the validation matrix, executing the comparative sensitivity studies, and documenting the results in a manner that met international regulatory scrutiny. This resulted in a 2-fold increase in detection sensitivity and established new quality control benchmarks. My experience includes the systematic evaluation of diagnostic kits, where I have designed and executed precision, accuracy, and limit-of-detection (LOD) studies to ensure total system reliability.

### Accredited Clinical Diagnostic Experience
My experience spans UKAS, CPA, and GMP-accredited environments. At the Anthony Nolan Research Institute, I was the technical lead for UKAS audit preparation, performing gap analyses on LIMS workflows and standardizing ABO blood-group testing on the Immunocor Echo platform. I conducted internal audits and implemented corrective actions for ISO 15189 alignment. This preparation led to zero major findings in the 2024 UKAS audit. Previously, during the H1N1 pandemic at UKHSA, I performed high-volume RT-qPCR diagnostics under CPA standards, authoring emergency SOPs and training staff to ensure throughput. I am an expert at maintaining operational excellence and data integrity, ensuring every result is traceable and accurate. I have extensive experience using electronic QMS tools to track non-conformances and drive improvement.

### Knowledge of IVD Regulations
I am deeply familiar with the complex and evolving IVD regulatory framework, including the Medicines and Medical Devices Act 2021, EU IVDR, and ISO 13485 standards. My approach consistently utilizes these regulations as benchmarks for best practice in reagent production and diagnostic evaluation. I have direct experience informing the MHRA regarding device performance conflicts and manage complex deviation and change control protocols at Lonza. During my tenure at NIBSC, I was responsible for ensuring that all project outputs complied with the Essential Requirements of the IVDD, and I am now actively tracking the transitional arrangements for the new UK regulatory framework. My work in Containment Level 3 facilities at NIBSC also required absolute adherence to SAPO4 and Schedule 5 regulations, demonstrating my ability to operate within multi-layered and highly restrictive regulatory environments. This awareness allows me to navigate the complexities of PHM's transition while ensuring absolute compliance and patient safety at every stage of the diagnostic lifecycle.

### Understanding and Experience of Change Management
I spearheaded the successful refurbishment of SAPO4/Schedule 5-compliant Containment Level 3 (CL3) laboratories at NIBSC, a complex change management project requiring negotiation with facilities management, health and safety officers, and scientific stakeholders. I managed the transition from legacy systems while maintaining WHO production timelines, ensuring that all new equipment was qualified (IQ/OQ/PQ) and all staff were retrained on the updated SOPs. At Lonza, I drove local process improvements to enhance the efficiency of buffer preparation and downstream flow, using Lean Six Sigma principles to identify bottlenecks and implement sustainable solutions. My proven ability to suggest and act on team improvements ensures that new facilities and processes achieve 100% compliance without disrupting critical deliverables. I am comfortable leading teams through periods of organizational change, maintaining morale and focus on core objectives while navigating technical and procedural transitions.

### Molecular & Serological Methods
My technical repertoire includes proficiency in molecular and serological methods forged across industrial and public health domains. At Lonza, I mastered AKTA chromatography and Sartorius column operation, alongside UF/DF and VRF workflows. At NIBSC, I led the development of standardized protocols for viral marker detection using Roche Cobas 6800 and Liaison XL systems. My expertise extends to the optimization of PCR assays, including primer and probe design for novel pathogens. I maintain a proactive awareness of IVD standards and have performed multiple gap analyses to align laboratory SOPs with the latest scientific advancements. My experience also includes the validation of LATE PCR assays and the evaluation of freeze-drying stability formulations, applying thermal analysis to ensure long-term reagent viability. I am proficient in genetic analysis software and have integrated these tools to enhance data throughput.

### Project Leadership & Communication
I have led international collaborative studies for the World Health Organization (WHO), coordinating a vast consortium of 32 institutions across 24 countries. This role required exceptional project management skills, as I was responsible for the end-to-end delivery of the project, from study design and material distribution to data collation and statistical analysis. My leadership ensured diverse international data was harmonized into a single, statistically robust output that now serves as the global benchmark for diagnostic accuracy. I am an expert in preparing high-fidelity technical reports for senior executive management and have presented findings at numerous international virology symposia. At Lonza, I coordinate across technical teams to ensure biomanufacturing batch release deadlines are met without compromising on quality or compliance. I am adept at translating complex scientific findings into actionable insights for non-technical stakeholders, ensuring project alignment and support across all levels of the organization.

### Interpersonal & Team Skills
Whether leading a global WHO project or working on the frontlines of the H1N1 response at UKHSA, I consistently prioritize clear, evidence-led communication. I am a highly adaptable team player with experience negotiating complex stakeholder landscapes, such as coordinating between laboratory managers, quality assurance units, and facilities teams to ensure project alignment. At Lonza, I proactively mentored junior staff on ALCOA+ data integrity principles and clean-room etiquette, fostering a culture of excellence and accountability. I am adept at building consensus and driving collaboration across multi-functional boundaries to achieve public health objectives. My interpersonal skills allow me to navigate challenging professional situations with diplomacy and tact, ensuring that team goals remain the primary focus even in high-pressure environments. I am committed to professional development, both for myself and my colleagues, and actively participate in knowledge-sharing initiatives to elevate the team's collective expertise.

## Meeting Desirable Criteria
I bring extensive experience with common office software and project management via Jira, enabling efficient tracking of tasks and milestones. My knowledge of GxP and safety requirements is comprehensive, gained through years of operating in GMP, GLP, and FDA-regulated environments. My recent upskilling in AI-mediated software engineering provides me with a unique technical perspective on digital laboratory transformation, allowing me to serve as a bridge between scientific research and information technology initiatives. This interdisciplinary lens is particularly valuable for implementing automated diagnostic solutions and modernizing data reporting frameworks within the PHM directorate.

## Unique Value Proposition (UVAID)
I offer a rare combination of industrial precision (Lonza), regulatory depth (MHRA), and public-service dedication (UKHSA). This unique experience provides an 'insider' perspective on regulatory assurance directly applicable to the RACU mission. I proactively integrate technical innovations like AKTA automation and ddPCR into quality frameworks to drive continuous improvement. I am a regulatory strategist who bridges the gap between innovation and compliance.

## Closing Commitment
I am committed to UKHSA’s mission of safeguarding public health. I look forward to bringing my track record of regulatory compliance and technical leadership to your team, ensuring all IVDs meet the highest standards. I am prepared to contribute immediately to the directorate's success during this transition period."""
    with open(output_path, 'w') as f:
        f.write(content)
    audit.record_event("Generator", "created_1500_word_rev4", {"path": output_path})

if __name__ == "__main__":
    output_dir = "outputs/Employment"
    audit = UnifiedEvidenceGraph(os.path.join(output_dir, "audit_log.jsonl"))
    engine = ExperienceEngine("knowledge/employment/ontology/experience_master.json")

    cv_path = os.path.join(output_dir, "Updated_CV_HealthcareScientist_2026_REV4.docx")
    s500_path = os.path.join(output_dir, "Supporting_Info_500words_REV4.md")
    s1500_path = os.path.join(output_dir, "Supporting_Info_1500words_REV4.md")

    generate_cv_rev4(cv_path, audit, engine)
    generate_supporting_info_500_rev4(s500_path, audit)
    generate_supporting_info_1500_rev4(s1500_path, audit)

    print(f"🏁 Asset Generation (REV4) complete in {output_dir}")
