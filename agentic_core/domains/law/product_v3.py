from typing import Dict, Any, List
import os
from products.OctoVeritasEngine import OctoVeritasEngineV3

class LawProductV3:
    def __init__(self, output_dir: str = "outputs/law-v3"):
        self.domain = "Law"
        self.engine = OctoVeritasEngineV3(self.domain, output_dir=output_dir)
        self.output_dir = output_dir

    def produce_package(self, input_data: Dict[str, Any], mode: str = "muaina"):
        self.engine.set_mode(mode)

        # Assets for Law domain
        raw_assets = [
            {
                "name": "ET1 Form",
                "asset_type": "document",
                "content": f"ET1 Claim Form for {input_data.get('claimant', 'John Doe')}",
                "pipeline": "Introspection", # QA/Action oriented
                "accessibility": {"alt_text": "Completed ET1 Employment Tribunal form."}
            },
            {
                "name": "Precedent Timeline",
                "asset_type": "infographic",
                "content": b"TIMELINE_BYTES",
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "Timeline of relevant case law precedents."}
            },
            {
                "name": "Schedule of Loss",
                "asset_type": "xlsx",
                "content": b"EXCEL_BYTES",
                "pipeline": "Retrospection", # Based on historical loss patterns
                "accessibility": {"alt_text": "Calculated schedule of loss spreadsheet."}
            }
        ]

        files = self.engine.produce_intelligent_package(raw_assets, audience="legal_rep")

        return {
            "status": "SUCCESS",
            "domain": self.domain,
            "mode": mode,
            "files": files
        }
