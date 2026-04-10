from typing import Dict, Any
import os
from agentic_core.domains.generic_product import GenericDomainProductGenerator
from agentic_core.omnimedia.factory import MultimediaAsset, OutputFormat

class CareProductGenerator(GenericDomainProductGenerator):
    def __init__(self):
        super().__init__("Care")

    def generate_news2_trend(self, patient_data: Dict[str, Any]) -> MultimediaAsset:
        import matplotlib.pyplot as plt
        import numpy as np

        times = ["08:00", "12:00", "16:00", "20:00"]
        news2_scores = [2, 1, 3, 2]

        plt.figure(figsize=(6, 4))
        plt.plot(times, news2_scores, marker='o', color='red')
        plt.title("NEWS2 Vital Sign Trend")
        plt.ylabel("Score")
        plt.grid(True)

        img_path = os.path.join(self.output_dir, "news2_trend.png")
        try:
            plt.savefig(img_path)
            plt.close()
        except Exception as e:
            self.logger.log_event(self.domain, "GEN_WARNING", {"message": f"Matplotlib failed: {str(e)}"})

        content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx\xda\x63\x60\x00\x02\x00\x00\x05\x00\x01\x26\x06\x10\x40\x00\x00\x00\x00IEND\xaeB`\x82' if not os.path.exists(img_path) else open(img_path, "rb").read()
        return MultimediaAsset("NEWS2 Trend", "infographic", content)

    def generate_care_schedule(self, data: Dict[str, Any]) -> MultimediaAsset:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["Time", "Activity", "Assigned To"])
        ws.append(["09:00", "Medication", "Nurse Anna"])

        path = os.path.join(self.output_dir, "care_schedule.xlsx")
        wb.save(path)
        with open(path, "rb") as f:
            return MultimediaAsset("Care Schedule", "xlsx", f.read())

    def generate_infographic(self, data: Dict[str, Any]) -> MultimediaAsset:
        return self.generate_news2_trend(data)

    def generate_document(self, data: Dict[str, Any], format: OutputFormat) -> MultimediaAsset:
        return MultimediaAsset("Care Plan", "document", "Individual Care Plan")
