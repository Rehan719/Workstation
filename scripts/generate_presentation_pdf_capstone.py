
import datetime
import os
from pathlib import Path
from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_presentation_pdf_capstone():
    print("📽️ Generating Final Capstone Presentation PDF Slides (20 Slides)...")

    output_path = Path("outputs/v3/presentation/slides.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=landscape(LETTER))
    styles = getSampleStyleSheet()

    # Capstone Slide Styles
    title_style = ParagraphStyle(
        'CapstoneTitle',
        parent=styles['Heading1'],
        fontSize=34,
        textColor=colors.HexColor("#64ffda"),
        alignment=1,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        'CapstoneSubtitle',
        parent=styles['Heading2'],
        fontSize=26,
        textColor=colors.HexColor("#94a3b8"),
        alignment=1,
        spaceAfter=30
    )

    body_style = ParagraphStyle(
        'CapstoneBody',
        parent=styles['BodyText'],
        fontSize=18,
        textColor=colors.HexColor("#cbd5e1"),
        alignment=1,
        leading=24
    )

    footer_style = ParagraphStyle(
        'CapstoneFooter',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.grey,
        alignment=2
    )

    slides = [
        ("GRAND OPERATION: CAPSTONE", "Definitive Final Synthesis", "Consolidating all intelligence, evidence, and organizational records into one sovereign masterpiece."),
        ("The Whistleblower Journey", "A Timeline of Truth", "From the first submission in Nov 2025 to the termination in Jan 2026. A journey validated by science."),
        ("Mushahida: Observation", "The Signal in the Noise", "Synthesizing the DeepSeek dossier with real-world patient outcomes and 2025-2026 study data."),
        ("AAV Germline Transduction", "The Wu 2025 Evidence", "High-frequency integration (5%) confirmed. Power-law dynamics identified across tissue types."),
        ("Late-Onset Autoimmunity", "The Chazarin 2026 Timeline", "A 'Second Wave' of cytokine activation at month 24. Mandatory RCM required."),
        ("Gifford 2025: Biosafety", "Capsid Horizontal Transfer", "Documentation of environmental gene leakage. A public health imperative for long-term follow-up."),
        ("The Plausibility Loop", "The Mechanism of Suppression", "How regulatory lag was weaponized to dismiss valid safety concerns as 'anecdotal'."),
        ("Ethics Committee Rejection", "A Failure of Oversight", "Reviewing the 13 Jan 2026 rejection letter. Proceduralism over patient safety."),
        ("The DES Tragedy Parallel", "A Warning from History", "How multi-generational harm occurs when signals are suppressed. We break the cycle."),
        ("Jaiza: Evaluation", "Strategic Options Analysis", "Comparing the Status Quo to Proactive Sovereign Leadership. The ROI of Safety."),
        ("Risk-Benefit Assessment", "Quantitative Meta-Analysis", "High integration probability (5%) vs. moderate therapeutic gain. The balance has shifted."),
        ("The LTSA Suite v3.0", "The Definitive Framework", "PGS | RCM | SLF | CAEH | EAIDE. Integrated sovereign safety."),
        ("1. PGS Module", "Pre-emptive Genomic Screening", "Mandatory baseline sequencing. Identifying risk profiles before enrollment."),
        ("2. RCM Module", "Real-time Cytokine Monitoring", "AI-driven early warning for neurotoxicity and late-onset CRS."),
        ("3. SLF Module", "Standardized Long-term Follow-up", "15-year digital health vault. Secure longitudinal data persistence."),
        ("Strategic Simulation", "Monte Carlo Projections", "1,000 iterations. 92% confidence in NPV stability for Proactive Leadership."),
        ("Regulatory Roadmap", "FDA & EMA PRAC 2026", "Proactive alignment with INTERACT and LTFU guidance. Securing the standard."),
        ("Muaina: The Proposal", "Final Recommendations", "Immediate transition to the Sovereign Standard. Break the Plausibility Loop."),
        ("Final Assessment", "Civilization Secured", "A definitive resolution for patient safety in the genetic era."),
        ("Conclusion: Transcend.", "The Grand Operation is Complete.", "Proceed to the Unified Final Portal. Civilization Secured.")
    ]

    elements = []
    for i, (title, subtitle, content) in enumerate(slides):
        elements.append(Spacer(1, 1.2*inch))
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(subtitle, subtitle_style))
        elements.append(Spacer(1, 0.4*inch))
        elements.append(Paragraph(content, body_style))
        elements.append(Spacer(1, 1.2*inch))
        elements.append(Paragraph(f"CAPSTONE Slide {i+1} | Workstation AI CEO | FINAL RELEASE", footer_style))
        elements.append(PageBreak())

    doc.build(elements)
    print(f"✅ Final Capstone Presentation PDF saved to: {output_path}")

if __name__ == "__main__":
    generate_presentation_pdf_capstone()
