from typing import Dict, Any
import os
from products.OctoVeritasEngine import OctoVeritasEngineV3

class EducationProductV3:
    def __init__(self, output_dir: str = "outputs/education-v3"):
        self.domain = "Education"
        self.engine = OctoVeritasEngineV3(self.domain, output_dir=output_dir)

    def produce_package(self, input_data: Dict[str, Any], mode: str = "synthesis"):
        self.engine.set_mode(mode)

        raw_assets = [
            {
                "name": "Mastery Timeline",
                "asset_type": "png",
                "content": b"MASTERY_PNG",
                "pipeline": "Learning",
                "accessibility": {"alt_text": "Timeline of student mastery across curriculum."}
            },
            {
                "name": "Lesson Plan",
                "asset_type": "docx",
                "content": "Lesson Plan: Introduction to AI",
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "Differentiated lesson plan."}
            }
        ]

        files = self.engine.produce_intelligent_package(raw_assets, audience="teacher")
        return {"status": "SUCCESS", "files": files}
