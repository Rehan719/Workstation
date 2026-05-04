import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

class LawPDFGenerator:
    def __init__(self, output_dir: str = "outputs/Law/EmploymentTribunal/v19_et1_clarification"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Justified', alignment=1)) # Justified

    def _create_pdf(self, filename: str, content_md: str, title: str):
        path = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(path, pagesize=A4)
        elements = []

        # Header
        elements.append(Paragraph(title, self.styles['Title']))
        elements.append(Spacer(1, 12))

        # Content
        lines = content_md.split('\n')
        for line in lines:
            if line.startswith('# '):
                elements.append(Paragraph(line[2:], self.styles['Heading1']))
            elif line.startswith('## '):
                elements.append(Paragraph(line[3:], self.styles['Heading2']))
            elif line.startswith('### '):
                elements.append(Paragraph(line[4:], self.styles['Heading3']))
            elif line.startswith('**'):
                elements.append(Paragraph(line, self.styles['Normal']))
            elif line.strip() == '---':
                elements.append(Spacer(1, 12))
            elif line.strip():
                elements.append(Paragraph(line, self.styles['Normal']))
            else:
                elements.append(Spacer(1, 6))

        doc.build(elements)
        print(f"VERIFIED: {path} ({os.path.getsize(path)} bytes)")
        return path

    def generate_et1(self, md_path: str):
        with open(md_path, 'r') as f:
            content = f.read()
        return self._create_pdf("ET1_v19_updated.pdf", content, "ET1 Updated Claim Details")

    def generate_letter(self, md_path: str):
        with open(md_path, 'r') as f:
            content = f.read()
        return self._create_pdf("Hillingdon_Legal_Aid_Clarity_Letter_v19.pdf", content, "Hillingdon Law Centre Clarification")

    def generate_timeline(self, md_path: str):
        with open(md_path, 'r') as f:
            content = f.read()
        return self._create_pdf("health_impact_timeline_v19.pdf", content, "Health Impact Timeline Annex")

if __name__ == "__main__":
    gen = LawPDFGenerator()
    # Logic to call these with MD files
