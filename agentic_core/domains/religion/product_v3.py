from typing import Dict, Any
import os
from products.OctoVeritasEngine import OctoVeritasEngineV3

class ReligionProductV3:
    def __init__(self, output_dir: str = "outputs/religion-v3"):
        self.domain = "Religion"
        self.engine = OctoVeritasEngineV3(self.domain, output_dir=output_dir)

    def produce_package(self, input_data: Dict[str, Any], mode: str = "mushahida"):
        self.engine.set_mode(mode)

        raw_assets = [
            {
                "name": "Tajweed Waveform",
                "asset_type": "png",
                "content": self._generate_waveform(),
                "pipeline": "Knowledge",
                "accessibility": {"alt_text": "Visual waveform of Surah Al-Fatihah with tajweed annotations."}
            },
            {
                "name": "Mouth Model",
                "asset_type": "png",
                "content": b"MOUTH_PNG",
                "pipeline": "Extrospection", # External anatomical reference
                "accessibility": {"alt_text": "Diagram showing tongue placement for Makharij."}
            }
        ]

        files = self.engine.produce_intelligent_package(raw_assets, audience="student")
        return {"status": "SUCCESS", "files": files}

    def _generate_waveform(self) -> bytes:
        import matplotlib.pyplot as plt
        import numpy as np
        import io
        t = np.linspace(0, 1, 100)
        y = np.sin(2 * np.pi * 5 * t) * np.exp(-t)
        plt.figure(figsize=(8, 2))
        plt.plot(t, y)
        plt.title("Tajweed Waveform Sample")
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        return buf.getvalue()
