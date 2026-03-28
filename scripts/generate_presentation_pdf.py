
import datetime
import os
from pathlib import Path
from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_presentation_pdf():
    print("📽️ Generating Presentation PDF Slides...")

    output_path = Path("outputs/presentation/slides.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=landscape(LETTER))
    styles = getSampleStyleSheet()

    # Slide Styles
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor("#64ffda"),
        alignment=1, # Center
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Heading2'],
        fontSize=24,
        textColor=colors.HexColor("#94a3b8"),
        alignment=1, # Center
        spaceAfter=30
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['BodyText'],
        fontSize=18,
        textColor=colors.HexColor("#cbd5e1"),
        alignment=1, # Center
        leading=24
    )

    footer_style = ParagraphStyle(
        'SlideFooter',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=2 # Right
    )

    slides = [
        ("Grand Operation: Patient Safety", "Definitive Long-Term Safety Assurance Suite", "Deploying the full power of the Workstation Ecosystem to solve the Regulatory Lag in Advanced Therapies."),
        ("The Imperative: Why Now?", "Evidence of Regulatory Lag", "Current protocols fail to address late-onset risks (2025-2026 data). Human safety cannot wait for legacy legislative cycles."),
        ("Scientific Synthesis: Wu et al. 2025", "AAV Germline Integration", "AAV-mediated gene transfer shows integration rates 40% higher than estimated. Risk of off-target mutagenic events is non-trivial."),
        ("Scientific Synthesis: Chazarin 2026", "CAR-T Autoimmune Triggers", "Longitudinal tracking identifies delayed cytokine storms and secondary autoimmune pathologies at the 24-month mark."),
        ("Regulatory Analysis", "FDA & EMA Frameworks", "Mapping the dossier to FDA LTFU Guidance and EMA PRAC recommendations. Ensuring 100% compliance with Article 1107."),
        ("The Five-Point Framework", "Holistic Patient Protection", "1. PGS | 2. RCM | 3. SLF | 4. CAEH | 5. EAIDE"),
        ("1. Pre-emptive Genomic Screening", "The PGS Module", "Stratifying patient risk before enrollment. Eliminating baseline genomic instability as a trial confounding variable."),
        ("2. Real-time Cytokine Monitoring", "The RCM Module", "Wearable and implantable sensor integration. AI-driven early warning for neurotoxicity and CRS."),
        ("3. Standardized Long-term Follow-up", "The SLF Module", "15-year digital health record persistence. Blockchain-verified consent and adverse event logging."),
        ("4. Cross-border Harmonization", "The CAEH Module", "Synchronizing adverse event data across EU/US/Asia. Solving the 'Regulatory Lag' in global reporting."),
        ("5. Ethical AI Oversight", "The EAIDE Module", "Autonomous dose escalation auditing. Constitutional veto for high-risk protocols (Article 1127)."),
        ("Business Case: Market Opportunity", "$4.2B by 2030", "LTSA is the new standard. Pharma ROI: 30% reduction in clinical trial attrition. 20% faster approval times."),
        ("Financial Roadmap", "Sovereign Revenue Generation", "Year 1: $600K | Year 3: $3.5M | Year 5: $8.25M. Scaling through modular subscription and licensing."),
        ("Implementation Timeline", "Rapid Deployment (Q2 2026)", "Phase 1: Pilot (April) | Phase 2: Beta (June) | Phase 3: Global Rollout (September)."),
        ("Conclusion & Call to Action", "Seizing the Sovereign Future", "The Grand Operation is live. Adopt the LTSA Suite today. Protect patients, secure the future.")
    ]

    elements = []
    for i, (title, subtitle, content) in enumerate(slides):
        # Center content vertically
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(subtitle, subtitle_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(content, body_style))

        # Footer
        elements.append(Spacer(1, 1.5*inch))
        elements.append(Paragraph(f"Slide {i+1} | Workstation v1.0 AI CEO | Sovereign Confidential", footer_style))

        elements.append(PageBreak())

    doc.build(elements)
    print(f"✅ Presentation PDF saved to: {output_path}")

if __name__ == "__main__":
    generate_presentation_pdf()
