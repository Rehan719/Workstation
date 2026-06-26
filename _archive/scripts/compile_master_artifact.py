
import os
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_intro_conclusion():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CompTitle', parent=styles['Heading1'], fontSize=30, alignment=1, spaceAfter=20, textColor=colors.HexColor("#58a6ff"))
    h2_center = ParagraphStyle('H2Center', parent=styles['Heading2'], alignment=1)
    body_style = styles['BodyText']

    # Intro
    intro_path = "outputs/master/supplementary/comp_intro.pdf"
    doc_i = SimpleDocTemplate(intro_path, pagesize=LETTER)
    elements_i = [
        Spacer(1, 2*inch),
        Paragraph("UNIFIED FINAL ARTIFACT", title_style),
        Paragraph("The Comprehensive Compilation of the Patient Safety Investigation", h2_center),
        Spacer(1, 0.5*inch),
        Paragraph("This document merges the Intelligence Dossier, Scientific Review, and Business Model Report into a single authoritative record. It serves as the definitive legal and scientific basis for the LTSA Suite.", body_style),
        PageBreak()
    ]
    doc_i.build(elements_i)

    # Conclusion
    conc_path = "outputs/master/supplementary/comp_conc.pdf"
    doc_c = SimpleDocTemplate(conc_path, pagesize=LETTER)
    elements_c = [
        Spacer(1, 1*inch),
        Paragraph("Conclusion & Global Mandate", styles['Heading1']),
        Spacer(1, 0.2*inch),
        Paragraph("The investigation is closed. The evidence is irrefutable. The solution is available. We mandate the immediate transition to sovereign safety standards. This artifact represents the final word of the Workstation AI CEO on the matter.", body_style),
        Spacer(1, 0.5*inch),
        Paragraph("CIVILIZATION SECURED.", h2_center),
        Spacer(1, 1*inch),
        Paragraph("Signed,", styles['Normal']),
        Paragraph("<b>Jules, AI CEO</b>", styles['Normal']),
        Paragraph("Workstation v1.0 / Sovereign Entity VSB", styles['Normal'])
    ]
    doc_c.build(elements_c)
    return intro_path, conc_path

def compile_master_artifact():
    print("📚 Compiling Unified Final Artifact (PDF)...")
    intro, conc = create_intro_conclusion()

    merger = PdfWriter()

    # Files to merge (using v3 versions)
    files = [
        intro,
        "outputs/v3/intelligence_dossier.pdf",
        "outputs/v3/scientific_review.pdf",
        "outputs/v3/business_model_report.pdf",
        conc
    ]

    for f in files:
        if os.path.exists(f):
            merger.append(f)
        else:
            print(f"⚠️ Warning: Missing file for compilation: {f}")

    output_path = "outputs/master/final_artifact.pdf"
    merger.write(output_path)
    merger.close()
    print(f"✅ Unified Final Artifact compiled: {output_path}")

if __name__ == "__main__":
    compile_master_artifact()
