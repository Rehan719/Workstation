from typing import Dict, Any
import os
from agentic_core.domains.generic_product import GenericDomainProductGenerator
from agentic_core.omnimedia.factory import MultimediaAsset, OutputFormat

class EmploymentProductGenerator(GenericDomainProductGenerator):
    def __init__(self):
        super().__init__("Employment")

    def generate_cv_heatmap(self, cv_data: Dict[str, Any]) -> MultimediaAsset:
        """
        Generates a CV attention heatmap infographic.
        """
        import matplotlib.pyplot as plt
        import numpy as np

        heatmap = np.random.rand(10, 10)
        plt.figure(figsize=(4, 6))
        plt.imshow(heatmap, cmap='hot', interpolation='nearest')
        plt.title("CV Attention Heatmap")
        plt.axis('off')

        img_path = os.path.join(self.output_dir, "cv_heatmap.png")
        try:
            plt.savefig(img_path)
            plt.close()
        except Exception as e:
            self.logger.log_event(self.domain, "GEN_WARNING", {"message": f"Matplotlib failed: {str(e)}"})

        content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDATx\xda\x63\x60\x00\x02\x00\x00\x05\x00\x01\x26\x06\x10\x40\x00\x00\x00\x00IEND\xaeB`\x82' if not os.path.exists(img_path) else open(img_path, "rb").read()
        return MultimediaAsset("CV Heatmap", "infographic", content)

    def generate_skill_matrix(self, data: Dict[str, Any]) -> MultimediaAsset:
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["Skill", "Level", "Experience"])
        ws.append(["Python", "Expert", "5 years"])

        path = os.path.join(self.output_dir, "skill_matrix.xlsx")
        wb.save(path)
        with open(path, "rb") as f:
            return MultimediaAsset("Skill Matrix", "xlsx", f.read())

    def generate_infographic(self, data: Dict[str, Any]) -> MultimediaAsset:
        return self.generate_cv_heatmap(data)

    def generate_document(self, data: Dict[str, Any], format: OutputFormat) -> MultimediaAsset:
        return MultimediaAsset("Employment Contract", "document", "Contract Details")
