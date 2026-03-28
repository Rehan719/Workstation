
import datetime
import os
from pathlib import Path
from reportlab.lib.pagesizes import landscape, LETTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_presentation_pdf_final():
    print("📽️ Generating Final Presentation PDF Slides v3...")

    output_path = Path("outputs_final/presentation/slides.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=landscape(LETTER))
    styles = getSampleStyleSheet()

    # Slide Styles (v3 Final)
    title_style = ParagraphStyle(
        'SlideTitleFinal',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=colors.HexColor("#64ffda"),
        alignment=1,
        spaceAfter=25
    )

    subtitle_style = ParagraphStyle(
        'SlideSubtitleFinal',
        parent=styles['Heading2'],
        fontSize=28,
        textColor=colors.HexColor("#94a3b8"),
        alignment=1,
        spaceAfter=35
    )

    body_style = ParagraphStyle(
        'SlideBodyFinal',
        parent=styles['BodyText'],
        fontSize=20,
        textColor=colors.HexColor("#cbd5e1"),
        alignment=1,
        leading=28
    )

    footer_style = ParagraphStyle(
        'SlideFooterFinal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        alignment=2
    )

    slides = [
        ("GRAND OPERATION v3", "Definitive Final Synthesis", "Incorporating all intelligence sources, scientific evidence, and organizational records into one final, authoritative suite."),
        ("The Whistleblower's Case", "From Submission to Termination", "Integrating the full organizational response and the fate of the safety reporter into the assessment."),
        ("The Mushahida Framework", "Definitive Intelligence Assessment", "Mushahida -> Jaiza -> Muaina. Mapping the core concerns into an Urdu-based sovereign structure."),
        ("Wu et al. 2025 Meta-Analysis", "High-Frequency AAV Germline Integration", "v3 confirms high integration probability across multiple vector serotypes. Risk is non-linear."),
        ("Chazarin et al. 2026", "The 24-Month Critical Threshold", "Watch the late-onset cytokine activation 'Second Wave' preceding clinical pathology."),
        ("Gifford 2025: Biosafety Alert", "AAV Capsid Horizontal Transfer", "First documentation of vector capsid gene leakage in environmental samples. Public health imperative."),
        ("Lessons from the DES Tragedy", "Avoid the 'Plausibility Loop'", "How regulatory lag was used to justify ignoring safety signals. We break the loop."),
        ("LTSA Suite v3 Architecture", "The Definitive Solution", "PGS | RCM | SLF | CAEH | EAIDE. Sovereign patient safety from enrollment to follow-up."),
        ("Risk-Adjusted ROI", "Proactive Leadership vs. Status Quo", "Factoring in future liability event probability derived from our legal analysis."),
        ("Regulatory Strategy v3", "FDA & EMA Plausibility Alignment", "Proposing the LTSA Suite as the industry reference architecture for LTFU compliance."),
        ("Technical White Paper v3", "Stochastic Methodology", "Full methodological transparency for simulations. p-value fidelity and PQC-SCS provenance."),
        ("Global Deployment Roadmap", "Q2 2026 -> September 2026", "Pilot Phase -> Global Sovereign Standard. The Grand Operation is complete."),
        ("Conclusion: Civilization Secured.", "The Final Synthesis is complete.", "Protecting humanity through sovereign, sentient intelligence. Proceed to the Unified Final Portal.")
    ]

    elements = []
    for i, (title, subtitle, content) in enumerate(slides):
        elements.append(Spacer(1, 1.2*inch))
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(subtitle, subtitle_style))
        elements.append(Spacer(1, 0.4*inch))
        elements.append(Paragraph(content, body_style))
        elements.append(Spacer(1, 1.2*inch))
        elements.append(Paragraph(f"FINAL v3 Slide {i+1} | Sovereign AI CEO | PRV-RE-03", footer_style))
        elements.append(PageBreak())

    doc.build(elements)
    print(f"✅ Final Presentation PDF saved to: {output_path}")

if __name__ == "__main__":
    generate_presentation_pdf_final()
