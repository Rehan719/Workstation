from typing import Dict, Any
import os
from products.OctoVeritasEngine import OctoVeritasEngineV3

class EmploymentProductV3:
    def __init__(self, output_dir: str = "outputs/employment-v3"):
        self.domain = "Employment"
        self.engine = OctoVeritasEngineV3(self.domain, output_dir=output_dir)

    def produce_package(self, input_data: Dict[str, Any], mode: str = "jaiza"):
        self.engine.set_mode(mode)

        raw_assets = [
            {
                "name": "CV Heatmap",
                "asset_type": "png",
                "content": b"CV_HEATMAP",
                "pipeline": "Ingestion",
                "accessibility": {"alt_text": "Heatmap of CV focus areas."}
            },
            {
                "name": "Skill Matrix",
                "asset_type": "xlsx",
                "content": b"SKILL_XLSX",
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "Matrix of employee skills vs requirements."}
            }
        ]

        files = self.engine.produce_intelligent_package(raw_assets, audience="hr_manager")
        return {"status": "SUCCESS", "files": files}
