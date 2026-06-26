import os
from fpdf import FPDF
import markdown2
import glob

def markdown_to_pdf(md_dir, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Get all markdown files in the directory sorted by name
    md_files = sorted(glob.glob(os.path.join(md_dir, "*.md")))

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple conversion: strip markdown syntax for a clean text PDF
            # A more complex one would use a proper parser but this ensures readability
            clean_content = content.replace("# ", "").replace("## ", "").replace("**", "")

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt=os.path.basename(md_file), ln=True, align='C')
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=clean_content)
            pdf.add_page()

    pdf.output(output_pdf)
    print(f"PDF generated at {output_pdf}")

if __name__ == "__main__":
    v17_core_dir = "outputs/Science/PatientSafety/v17_sexta_veritas/CORE_ANALYSIS"
    output_path = "outputs/Science/PatientSafety/v17_sexta_veritas/PatientSafety_Dossier_v17.pdf"
    markdown_to_pdf(v17_core_dir, output_path)
