from typing import Any, List, Dict
from ..omnimedia.factory import MultimediaAsset
from ..omnimedia.injector import OmnimediaInjector

class OctopusArm:
    def __init__(self, domain: str, injector: OmnimediaInjector, templates: Dict[str, Any] = None):
        self.domain = domain
        self.injector = injector
        self.templates = templates or {}

    def inject_asset(self, job: Any) -> str:
        """
        Domain-specific injection arm.
        """
        # Wrap job asset into MultimediaAsset if needed
        m_asset = MultimediaAsset(
            name=job.asset.get('name', 'Unnamed'),
            asset_type=job.asset.get('asset_type', 'png'),
            content=job.asset.get('content', b''),
            hash=job.asset.get('hash', '0'*128),
            accessibility=job.asset.get('accessibility', {})
        )

        # Mapping format to injector method (Octopus logic)
        method_map = {
            "PDF": self.injector.inject_into_pdf,
            "DOCX": self.injector.inject_into_docx,
            "PPTX": self.injector.inject_into_pptx,
            "XLSX": self.injector.inject_into_xlsx,
            "HTML": self.injector.inject_into_html,
            "MP4": self.injector.inject_into_mp4,
            "MP3": self.injector.inject_into_mp3,
            "PNG": self.injector.inject_into_png,
            "SVG": self.injector.inject_into_svg
        }

        method = method_map.get(job.format.upper(), self.injector.inject_into_html)
        output_path = f"{self.domain.lower()}_v4_output.{job.format.lower()}"
        return method(output_path, [m_asset])
