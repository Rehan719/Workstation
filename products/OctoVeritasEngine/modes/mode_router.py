import os
from typing import Dict, Any, Optional, List

class ModeRouter:
    VALID_MODES = [
        "mushahida",
        "jaiza",
        "muaina",
        "real_time_support",
        "synthesis",
        "continuous_operation"
    ]

    DEFAULT_FORMATS = {
        "mushahida": ["JSON", "CSV", "HTML"],
        "jaiza": ["PPTX", "HTML", "XLSX"],
        "muaina": ["PDF", "DOCX"],
        "real_time_support": ["HTML", "MP4", "MP3"],
        "synthesis": ["PPTX", "PDF", "HTML"],
        "continuous_operation": ["JSON", "HTML"]
    }

    def __init__(self):
        self._current_mode = os.getenv("OCTO_MODE", "jaiza").lower()
        if self._current_mode not in self.VALID_MODES:
            self._current_mode = "jaiza"

    def set_mode(self, mode: str):
        if mode.lower() in self.VALID_MODES:
            self._current_mode = mode.lower()
        else:
            raise ValueError(f"Invalid mode: {mode}. Valid modes are: {self.VALID_MODES}")

    def get_mode(self) -> str:
        return self._current_mode

    def get_default_formats(self, mode: Optional[str] = None) -> List[str]:
        target_mode = mode.lower() if mode else self._current_mode
        return self.DEFAULT_FORMATS.get(target_mode, ["HTML"])

    def get_injection_strategy(self, mode: str, audience: str) -> Dict[str, Any]:
        # Placeholder for complex strategy logic
        return {
            "mode": mode,
            "audience": audience,
            "apply_watermark": mode == "muaina",
            "interactive": mode in ["real_time_support", "continuous_operation"]
        }
