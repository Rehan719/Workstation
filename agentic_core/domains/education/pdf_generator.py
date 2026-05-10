import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from PyPDF2 import PdfWriter, PdfReader

class SATsPDFGenerator:
    """
    Generates verified individual and bundled PDFs for the SATs Preparation Pack.
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
        self.generated_pdfs = []

    def _create_pdf(self, path: str, elements: list):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc = SimpleDocTemplate(path, pagesize=A4)
        doc.build(elements)

        # Physical Verification
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF generation failed: {path} not found.")
        size = os.path.getsize(path)
        if size == 0:
            raise ValueError(f"PDF generation failed: {path} is zero-byte.")

        print(f"VERIFIED: {path} ({size} bytes)")
        self.generated_pdfs.append(path)
        return path

    def generate_schedule_pdf(self):
        """Generates the personalized 14-day schedule PDF for Ayaan."""
        elements = [
            Paragraph("📅 14-Day Revision Schedule", self.styles['Heading1']),
            Paragraph("Personalized for Ayaan (Norbury School, Harrow)", self.styles['Heading2']),
            Spacer(1, 12)
        ]
        path = os.path.join(self.base_dir, "revision_schedule/schedule.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                schedule_data = json.load(f)
            for day in schedule_data["revision_plan"]:
                elements.append(Paragraph(f"Day {day['day']} - {day['date']} ({day['status']})", self.styles['Heading3']))
                elements.append(Paragraph(f"<i>{day['motivation']}</i>", self.styles['Italic']))
                for session in day["sessions"]:
                    elements.append(Paragraph(f"• <b>{session['time']}</b>: {session['activity']} (Goal: {session['goal']})", self.styles['Normal']))
                elements.append(Spacer(1, 10))

        output_path = os.path.join(self.base_dir, "revision_schedule/schedule.pdf")
        return self._create_pdf(output_path, elements)

    def generate_exam_pdfs(self):
        """Generates exam question and model answer PDFs."""
        for title, filename in self.papers:
            # Questions PDF
            q_elements = [
                Paragraph(f"📝 PREDICTED QUESTIONS: {title}", self.styles['Heading1']),
                Paragraph("Ayaan - Norbury School", self.styles['Heading3']),
                Spacer(1, 10)
            ]
            q_path = os.path.join(self.base_dir, "predicted_questions", filename)
            if os.path.exists(q_path):
                with open(q_path, "r") as f:
                    questions = json.load(f)
                for q in questions:
                    q_elements.append(Paragraph(f"<b>{q['id']}:</b> {q['question']}", self.styles['Normal']))
                    q_elements.append(Spacer(1, 8))

            out_q = os.path.join(self.base_dir, "predicted_questions", filename.replace(".json", ".pdf"))
            self._create_pdf(out_q, q_elements)

            # Answers PDF
            a_elements = [
                Paragraph(f"✅ MODEL ANSWERS: {title}", self.styles['Heading1']),
                Paragraph("Step-by-Step Solutions for Ayaan", self.styles['Heading3']),
                Spacer(1, 10)
            ]
            a_path = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.json"))
            if os.path.exists(a_path):
                with open(a_path, "r") as f:
                    answers = json.load(f)
                for a in answers:
                    ans_text = a['answer']
                    if isinstance(ans_text, dict):
                        # Handle LINK structure
                        a_elements.append(Paragraph("A:", self.styles['Normal']))
                        for key, value in ans_text.items():
                            a_elements.append(Paragraph(f"<b>{key}:</b> {value}", self.styles['Normal']))
                    else:
                        a_elements.append(Paragraph(f"A: {ans_text}", self.styles['Normal']))

                    sol_key = 'worked_solution' if 'worked_solution' in a else ('rule_or_justification' if 'rule_or_justification' in a else 'method_or_worked_solution')
                    a_elements.append(Paragraph(f"Method: {a.get(sol_key, 'Standard')}", self.styles['Italic']))
                    a_elements.append(Spacer(1, 5))

            out_a = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.pdf"))
            self._create_pdf(out_a, a_elements)

    def concatenate_bundle(self):
        """Uses PyPDF2 to concatenate all individual PDFs into a master bundle."""
        bundle_path = os.path.join(self.base_dir, "deliverable/Norbury_School_SATs_Prep_Pack_2026.pdf")
        os.makedirs(os.path.dirname(bundle_path), exist_ok=True)

        merger = PdfWriter()

        # Cover Page (Dynamic Creation)
        cover_path = os.path.join(self.base_dir, "deliverable/cover.pdf")
        cover_elements = [
            Spacer(1, 150),
            Paragraph("<font size=24 color='#1E3A8A'>بِسْمِ اللَّهِ الرَّحْمٰنِ الرَّحِيْمِ</font>", self.styles['Title']),
            Spacer(1, 40),
            Paragraph("<font size=28 color='#1E3A8A'>KS2 SATs 2026</font>", self.styles['Title']),
            Paragraph("<font size=22 color='#1E3A8A'>COMPLETE PREPARATION PACK</font>", self.styles['Title']),
            Spacer(1, 40),
            Paragraph("Prepared for: <b>Ayaan</b>", self.styles['Heading2']),
            Paragraph("Norbury School, Harrow", self.styles['Heading2']),
            Spacer(1, 100),
            Paragraph("<i>You’ve got this, Ayaan! Let’s work together, step by step.</i>", self.styles['Italic']),
            Spacer(1, 150),
            Paragraph("<font color='#4B5563'>Generated by Workstation Education Grand Operation</font>", self.styles['Normal']),
            Paragraph("<font color='#4B5563'>Constitutional Guard & UEG Logged</font>", self.styles['Normal'])
        ]
        self._create_pdf(cover_path, cover_elements)

        # Add cover
        merger.append(cover_path)

        # Add schedule
        sched_pdf = os.path.join(self.base_dir, "revision_schedule/schedule.pdf")
        if os.path.exists(sched_pdf):
            merger.append(sched_pdf)

        # Add all questions and answers
        for _, filename in self.papers:
            q_pdf = os.path.join(self.base_dir, "predicted_questions", filename.replace(".json", ".pdf"))
            if os.path.exists(q_pdf):
                merger.append(q_pdf)
            a_pdf = os.path.join(self.base_dir, "model_answers", filename.replace(".json", "_answers.pdf"))
            if os.path.exists(a_pdf):
                merger.append(a_pdf)

        with open(bundle_path, "wb") as f:
            merger.write(f)

        # Cleanup temp cover
        if os.path.exists(cover_path):
            os.remove(cover_path)

        size = os.path.getsize(bundle_path)
        print(f"VERIFIED BUNDLE: {bundle_path} ({size} bytes)")
        return bundle_path

if __name__ == "__main__":
    gen = SATsPDFGenerator()
    try:
        gen.generate_schedule_pdf()
        gen.generate_exam_pdfs()
        gen.concatenate_bundle()
        print("EDUCATION GRAND OPERATION: All PDFs Generated and Verified.")
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        exit(1)
