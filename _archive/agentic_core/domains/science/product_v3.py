from typing import Dict, Any, List, Optional
import os
import pandas as pd
import matplotlib.pyplot as plt
from products.OctoVeritasEngine import OctoVeritasEngineV3
from agentic_core.omnimedia.factory import MultimediaAsset

class ScienceProductV3:
    def __init__(self, output_dir: str = "outputs/science-v3"):
        self.domain = "Science"
        self.engine = OctoVeritasEngineV3(self.domain, output_dir=output_dir)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def produce_package(self, input_data: Dict[str, Any], mode: str = "jaiza"):
        self.engine.set_mode(mode)

        # 1. Define assets with pipeline provenance
        # GRADE matrix -> Knowledge pipeline
        grade_data = input_data.get("grade_matrix_data", [
            {"Outcome": "Safety", "Certainty": "High", "Importance": "Critical", "Summary": "No serious AEs."},
            {"Outcome": "Efficacy", "Certainty": "Moderate", "Importance": "Critical", "Summary": "85% response rate."}
        ])
        df = pd.DataFrame(grade_data)

        # Risk Heatmap -> Ingestion/Analysis
        # Digital Twin -> Synthesis/Knowledge

        raw_assets = [
            {
                "name": "GRADE Matrix",
                "asset_type": "infographic",
                "content": df.to_html(),
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "GRADE matrix showing high certainty for safety outcomes."}
            },
            {
                "name": "Risk Heatmap",
                "asset_type": "png",
                "content": self._generate_heatmap_bytes(),
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "Heatmap of safety risks."}
            },
            {
                "name": "AAV Digital Twin",
                "asset_type": "digital_twin",
                "content": b"TWIN_DATA", # Placeholder for actual drawing
                "pipeline": "Learning",
                "accessibility": {"alt_text": "Digital twin of AAV vector persistence."}
            }
        ]

        # 2. Execute Intelligent Injection
        files = self.engine.produce_intelligent_package(raw_assets, audience="regulator")

        return {
            "status": "SUCCESS",
            "domain": self.domain,
            "mode": mode,
            "files": files
        }

    def _generate_heatmap_bytes(self) -> bytes:
        import numpy as np
        import matplotlib.pyplot as plt
        import io
        risk_data = np.random.rand(5, 5)
        plt.figure(figsize=(6, 5))
        plt.imshow(risk_data, cmap='RdYlGn_r', interpolation='nearest')
        plt.colorbar(label='Risk Level')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()
