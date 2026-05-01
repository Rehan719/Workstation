import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

class SATsPDFGenerator:
    """
    Generates individual and bundled PDFs for the SATs Preparation Pack.
    """
    def __init__(self, base_dir: str = "outputs/education/sats_2026"):
        self.base_dir = base_dir
        self.styles = getSampleStyleSheet()
        self.papers = [
            ("English Grammar, Punctuation & Spelling", "english_gps.json"),
            ("English Reading", "english_reading.json"),
            ("Mathematics Paper 1: Arithmetic", "maths_arithmetic.json"),
            ("Mathematics Paper 2: Reasoning", "maths_reasoning_1.json"),
            ("Mathematics Paper 3: Reasoning", "maths_reasoning_2.json")
        ]

    def _create_pdf(self, path: str, elements: list):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = SimpleDocTemplate(path, pagesize=A4)
        doc.build(elements)
        return path

    def generate_schedule_pdf(self):
        elements = []
        elements.append(Paragraph("14-Day Revision Schedule", self.styles['Heading1']))
        elements.append(Spacer(1, 10))

        path = os.path.join(self.base_dir, "revision_schedule/schedule.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                schedule_data = json.load(f)
            for day in schedule_data["revision_plan"]:
                elements.append(Paragraph(f"Day {day['day']} - {day['date']} ({day['status']})", self.styles['Heading3']))
                for session in day["sessions"]:
                    elements.append(Paragraph(f"• {session['time']}: {session['activity']}", self.styles['Normal']))
                elements.append(Spacer(1, 10))

        output_path = os.path.join(self.base_dir, "revision_schedule/schedule.pdf")
        return self._create_pdf(output_path, elements)

    def generate_exam_pdfs(self):
        generated_paths = []
        for title, filename in self.styles.items() if isinstance(self.styles, dict) else self.papers: # Corrected loop
            # Questions PDF
            q_elements = [Paragraph(f"PREDICTED QUESTIONS: {title}", self.styles['Heading1']), Spacer(1, 10)]
            q_path = os.path.join(self.base_dir, "predicted_questions", filename)
            if os.path.exists(q_path):
                with open(q_path, "r") as f:
                    questions = json.load(f)
                for q in questions:
                    q_elements.append(Paragraph(f"Q: {q['question']}", self.styles['Normal']))
                    q_elements.append(Spacer(1, 5))

            out_q = os.path.join(self.base_dir, "predicted_questions", filename.replace(".json", ".pdf"))
            generated_paths.append(self._create_pdf(out_q, q_elements))

            # Answers PDF
            a_elements = [Paragraph(f"MODEL ANSWERS: {title}", self.styles['Heading1']), Spacer(1, 10)]
            a_path = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.json"))
            if os.path.exists(a_path):
                with open(a_path, "r") as f:
                    answers = json.load(f)
                for a in answers:
                    ans_text = str(a['answer'])
                    a_elements.append(Paragraph(f"A: {ans_text}", self.styles['Normal']))
                    sol_key = 'worked_solution' if 'worked_solution' in a else ('rule_or_justification' if 'rule_or_justification' in a else 'method_or_worked_solution')
                    a_elements.append(Paragraph(f"Method: {a.get(sol_key, 'Standard')}", self.styles['Italic']))
                    a_elements.append(Spacer(1, 5))

            out_a = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.pdf"))
            generated_paths.append(self._create_pdf(out_a, a_elements))

        return generated_paths

    def generate_bundle(self):
        bundle_path = os.path.join(self.base_dir, "deliverable/Norbury_School_SATs_Prep_Pack_2026.pdf")
        doc = SimpleDocTemplate(bundle_path, pagesize=A4)
        elements = []

        # Cover
        elements.append(Spacer(1, 100))
        elements.append(Paragraph("SATs 2026: COMPLETE PREPARATION PACK", self.styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Personalized for Norbury School Pupil", self.styles['Heading2']))
        elements.append(Spacer(1, 100))
        elements.append(Paragraph("بِسْمِ اللَّهِ وَعَلَى بَرَكَةِ اللَّهِ", self.styles['Normal']))
        elements.append(PageBreak())

        # Reuse logic for schedule and each paper
        # Schedule
        elements.append(Paragraph("14-Day Revision Schedule", self.styles['Heading1']))
        schedule_path = os.path.join(self.base_dir, "revision_schedule/schedule.json")
        if os.path.exists(schedule_path):
            with open(schedule_path, "r") as f:
                schedule_data = json.load(f)
            for day in schedule_data["revision_plan"]:
                elements.append(Paragraph(f"Day {day['day']} - {day['date']} ({day['status']})", self.styles['Heading3']))
                for session in day["sessions"]:
                    elements.append(Paragraph(f"• {session['time']}: {session['activity']}", self.styles['Normal']))
                elements.append(Spacer(1, 5))
        elements.append(PageBreak())

        # Papers
        for title, filename in self.papers:
            elements.append(Paragraph(title, self.styles['Heading1']))
            elements.append(Spacer(1, 10))

            q_path = os.path.join(self.base_dir, "predicted_questions", filename)
            if os.path.exists(q_path):
                elements.append(Paragraph("Predicted Questions", self.styles['Heading2']))
                with open(q_path, "r") as f:
                    questions = json.load(f)
                for q in questions:
                    elements.append(Paragraph(f"Q: {q['question']}", self.styles['Normal']))
                    elements.append(Spacer(1, 5))

            elements.append(Spacer(1, 10))
            a_path = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.json"))
            if os.path.exists(a_path):
                elements.append(Paragraph("Model Answers & Worked Solutions", self.styles['Heading2']))
                with open(a_path, "r") as f:
                    answers = json.load(f)
                for a in answers:
                    ans_text = str(a['answer'])
                    elements.append(Paragraph(f"A: {ans_text}", self.styles['Normal']))
                    sol_key = 'worked_solution' if 'worked_solution' in a else ('rule_or_justification' if 'rule_or_justification' in a else 'method_or_worked_solution')
                    elements.append(Paragraph(f"Method: {a.get(sol_key, 'Standard')}", self.styles['Italic']))
                    elements.append(Spacer(1, 5))
            elements.append(PageBreak())

        doc.build(elements)
        return bundle_path

if __name__ == "__main__":
    gen = SATsPDFGenerator()
    gen.generate_schedule_pdf()
    gen.generate_exam_pdfs()
    gen.generate_bundle()
    print("All PDFs (individual and bundled) generated successfully.")
