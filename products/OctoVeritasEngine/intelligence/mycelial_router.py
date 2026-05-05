import logging
from typing import List, Dict, Tuple, Any, Optional

class MycelialRouter:
    def __init__(self, logger: Any):
        self.logger = logger
        self.registry: Dict[str, List[Tuple[str, float]]] = {}
        self._init_defaults()

    def _init_defaults(self):
        # Default fallback graph
        self.registry = {
            "PDF": [("reportlab", 1.0), ("weasyprint", 0.8), ("html_to_pdf", 0.6)],
            "DOCX": [("python-docx", 1.0), ("pandoc", 0.5)],
            "PPTX": [("python-pptx", 1.0), ("office_lib", 0.4)],
            "XLSX": [("openpyxl", 1.0), ("pandas_excel", 0.7)],
            "MP4": [("moviepy", 1.0), ("ffmpeg", 0.9)],
            "MP3": [("pydub", 1.0), ("ffmpeg_audio", 0.9)],
            "PNG": [("pillow", 1.0), ("opencv", 0.6)],
            "SVG": [("native_xml", 1.0), ("cairosvg", 0.8)],
            "HTML": [("jinja2", 1.0), ("mako", 0.4)]
        }

    def register_fallback(self, format: str, fallbacks: List[Tuple[str, float]]):
        self.registry[format.upper()] = sorted(fallbacks, key=lambda x: x[1], reverse=True)

    def get_fallback_path(self, format: str) -> List[str]:
        fallbacks = self.registry.get(format.upper(), [])
        return [f[0] for f in fallbacks]

    def execute_with_resilience(self, format: str, injection_func: Any, *args, **kwargs) -> Any:
        path = self.get_fallback_path(format)
        errors = []

        for method in path:
            try:
                # In a real scenario, we'd swap the underlying implementation based on 'method'
                # For v4.0 simulation, we just call the provided function
                return injection_func(*args, **kwargs)
            except Exception as e:
                errors.append(f"{method}: {str(e)}")
                self.logger.log_event({
                    "operation": "MYCELIAL_REROUTE",
                    "format": format,
                    "failed_method": method,
                    "error": str(e)
                })

        raise RuntimeError(f"InjectionUnrecoverable: All paths for {format} failed. Errors: {errors}")
