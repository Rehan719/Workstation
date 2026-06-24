from typing import Dict, Any, List
from products.OctoVeritasEngine import OctoVeritasEngineV4

class LawProductV4:
    def __init__(self, output_dir: str = "outputs/law-v4"):
        self.domain = "Law"
        self.engine = OctoVeritasEngineV4(self.domain, output_dir=output_dir)

    def produce_package(self, input_data: Dict[str, Any], bto_config: Dict[str, Any] = None):
        # Assets for Law domain v4
        raw_assets = [
            {
                "name": "ET1 Form",
                "asset_type": "document",
                "content": f"ET1 Claim Form for {input_data.get('claimant', 'John Doe')}",
                "pipeline": "Introspection",
                "hash": "sha3_law_001",
                "accessibility": {"alt_text": "Completed ET1 form for tribunal submission."}
            },
            {
                "name": "Precedent Timeline",
                "asset_type": "infographic",
                "content": b"TIMELINE_BYTES",
                "pipeline": "Knowledge",
                "hash": "sha3_law_002",
                "accessibility": {"alt_text": "Sovereign Law precedent timeline."}
            }
        ]

        # BTO default overrides
        if bto_config is None:
            bto_config = {"default_mode": "muaina"}

        return self.engine.produce_sovereign_package(raw_assets, bto_config=bto_config)
