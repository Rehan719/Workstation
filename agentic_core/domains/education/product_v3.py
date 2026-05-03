from typing import Dict, Any, List
import os
from products.OctoVeritasEngine import OctoVeritasEngineV4

class EducationProductV3:
    """
    Education Domain engine, upgraded to OctoVeritasEngineV4 for the
    Education Grand Operation (SATs 2026).
    """
    def __init__(self, output_dir: str = "outputs/education/sats_2026"):
        self.domain = "Education"
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.engine = OctoVeritasEngineV4(self.domain, output_dir=output_dir)

    def produce_sats_package(self, assets: List[Dict[str, Any]], bto_config: Dict[str, Any] = None):
        """
        Orchestrates the generation of the SATs preparation pack using the V4 engine.
        """
        # Ensure the output directory structure exists
        subdirs = ["predicted_questions", "model_answers", "revision_schedule", "deliverable"]
        for subdir in subdirs:
            os.makedirs(os.path.join(self.output_dir, subdir), exist_ok=True)

        # Use V4 sovereign packaging logic
        results = self.engine.produce_sovereign_package(assets, bto_config=bto_config)
        return {"status": "SUCCESS", "results": results}

    def produce_package(self, input_data: Dict[str, Any], mode: str = "synthesis"):
        """
        Legacy compatibility method.
        """
        self.engine.router.set_mode(mode)
        raw_assets = input_data.get("assets", [])
        files = self.engine.produce_sovereign_package(raw_assets)
        return {"status": "SUCCESS", "files": files}
