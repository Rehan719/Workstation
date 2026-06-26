import os
import glob
from fpdf import FPDF

class ScientificDossierPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Septima-Veritas Scientific Intelligence Dossier v17.1', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | VSB Signature Product v17.1', 0, 0, 'C')

def generate_pdf(src_dirs, output_path):
    pdf = ScientificDossierPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, 'SCIENCE GRAND OPERATION', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 15, 'v17.1 "SEPTIMA-VERITAS"', 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Sovereign Patient Safety Intelligence Platform\nScientific Review & Analysis Optimized Production Release', align='C')
    pdf.ln(20)
    pdf.cell(0, 10, 'Date: Thursday, April 09, 2026', 0, 1, 'C')

    # Content
    pdf.set_font('Arial', '', 11)

    all_files = []
    for d in src_dirs:
        files = sorted(glob.glob(os.path.join(d, "*.md")))
        all_files.extend(files)

    for md_file in all_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Basic cleanup of markdown syntax for the PDF
            title = os.path.basename(md_file).replace('.md', '').replace('_', ' ').title()
            clean_content = content.replace('# ', '').replace('## ', '').replace('**', '').replace('---', '')

            pdf.add_page()
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, title, 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 7, clean_content)

    pdf.output(output_path)
    print(f"✅ Definitive Scientific Dossier PDF generated at {output_path}")

if __name__ == "__main__":
    base = "outputs/Science/PatientSafety/v17.1_septima_veritas/"
    dirs = [
        os.path.join(base, "SCIENTIFIC_DOSSIER"),
        os.path.join(base, "ADVANCED_SCIENTIFIC_TOOLKIT"),
        os.path.join(base, "REAL_TIME_SCIENTIFIC_SUPPORT"),
        os.path.join(base, "FINAL_SCIENTIFIC_SUBMISSION")
    ]
    out = os.path.join(base, "PatientSafety_Dossier_v17.1.pdf")
    generate_pdf(dirs, out)
