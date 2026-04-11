from typing import Dict, Any
from products.OctoVeritasEngine import OctoVeritasEngineV4

class ScienceProductV4:
    def __init__(self, output_dir: str = "outputs/science-v4"):
        self.domain = "Science"
        self.engine = OctoVeritasEngineV4(self.domain, output_dir=output_dir)

    def produce_package(self, input_data: Dict[str, Any], bto_config: Dict[str, Any] = None):
        raw_assets = [
            {
                "name": "GRADE Matrix",
                "asset_type": "infographic",
                "content": b"GRADE_BYTES",
                "pipeline": "Knowledge",
                "hash": "sha3_sci_001",
                "accessibility": {"alt_text": "Scientific evidence GRADE matrix."}
            },
            {
                "name": "Risk Heatmap",
                "asset_type": "png",
                "content": b"HEATMAP_BYTES",
                "pipeline": "Knowledge",
                "hash": "sha3_sci_002",
                "accessibility": {"alt_text": "Patient safety risk heatmap infographic."}
            }
        ]
        return self.engine.produce_sovereign_package(raw_assets, bto_config=bto_config)
