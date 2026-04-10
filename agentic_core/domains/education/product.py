from typing import Dict, Any
import os
from agentic_core.domains.generic_product import GenericDomainProductGenerator
from agentic_core.omnimedia.factory import MultimediaAsset, OutputFormat

class EducationProductGenerator(GenericDomainProductGenerator):
    def __init__(self):
        super().__init__("Education")

    def generate_mastery_timeline(self, student_data: Dict[str, Any]) -> MultimediaAsset:
        import matplotlib.pyplot as plt

        subjects = ["Math", "Science", "Law", "Art"]
        mastery = [85, 92, 78, 65]

        plt.figure(figsize=(8, 4))
        plt.bar(subjects, mastery, color='skyblue')
        plt.title("Student Mastery Timeline")
        plt.ylim(0, 100)

        img_path = os.path.join(self.output_dir, "mastery_timeline.png")
        try:
            plt.savefig(img_path)
            plt.close()
        except Exception as e:
            self.logger.log_event(self.domain, "GEN_WARNING", {"message": f"Matplotlib failed: {str(e)}"})

        content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx\xda\x63\x60\x00\x02\x00\x00\x05\x00\x01\x26\x06\x10\x40\x00\x00\x00\x00IEND\xaeB`\x82' if not os.path.exists(img_path) else open(img_path, "rb").read()
        return MultimediaAsset("Mastery Timeline", "infographic", content)

    def generate_gradebook(self, data: Dict[str, Any]) -> MultimediaAsset:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["Student", "Grade", "Status"])
        ws.append(["Jules", "A*", "Distinction"])

        path = os.path.join(self.output_dir, "gradebook.xlsx")
        wb.save(path)
        with open(path, "rb") as f:
            return MultimediaAsset("Gradebook", "xlsx", f.read())

    def generate_infographic(self, data: Dict[str, Any]) -> MultimediaAsset:
        return self.generate_mastery_timeline(data)

    def generate_document(self, data: Dict[str, Any], format: OutputFormat) -> MultimediaAsset:
        return MultimediaAsset("Syllabus", "document", "Course Syllabus")
