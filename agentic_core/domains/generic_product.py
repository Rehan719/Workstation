from typing import Dict, Any, List
from agentic_core.omnimedia.factory import OctoOmnimediaGenerator, MultimediaAsset, OutputFormat
from agentic_core.omnimedia.injector import OmnimediaInjector
from agentic_core.constitutional.gaas_validator_v2 import ConstitutionalValidatorV2
from agentic_core.constitutional.ueg_logger import UEGLogger
from agentic_core.omnimedia.accessibility import AccessibilityEngine
from agentic_core.utils.hashing import attach_hash_to_file
import os
import time

class GenericDomainProductGenerator(OctoOmnimediaGenerator):
    def __init__(self, domain: str):
        self.domain = domain
        self.validator = ConstitutionalValidatorV2(self.domain)
        self.logger = UEGLogger()
        self.injector = OmnimediaInjector()
        self.accessibility = AccessibilityEngine()
        self.output_dir = f"outputs/{self.domain.lower()}_q2"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_infographic(self, data: Dict[str, Any]) -> MultimediaAsset:
        metadata = {"accessibility": self.accessibility.tag_asset("infographic", {})}
        return MultimediaAsset(f"{self.domain} Infographic", "infographic", b"MOCK_PNG", metadata)

    def generate_video(self, data: Dict[str, Any]) -> MultimediaAsset:
        metadata = {"accessibility": self.accessibility.tag_asset("video", {})}
        return MultimediaAsset(f"{self.domain} Video", "video", None, metadata)

    def generate_audio(self, data: Dict[str, Any]) -> MultimediaAsset:
        metadata = {"accessibility": self.accessibility.tag_asset("audio", {})}
        return MultimediaAsset(f"{self.domain} Audio", "audio", None, metadata)

    def generate_digital_twin(self, data: Dict[str, Any]) -> MultimediaAsset:
        metadata = {"accessibility": self.accessibility.tag_asset("digital_twin", {})}
        return MultimediaAsset(f"{self.domain} Digital Twin", "digital_twin", b"MOCK_PNG", metadata)

    def generate_document(self, data: Dict[str, Any], format: OutputFormat) -> MultimediaAsset:
        return MultimediaAsset(f"{self.domain} Document", "document", "Generic Content")

    def generate_dashboard(self, data: Dict[str, Any]) -> MultimediaAsset:
        return MultimediaAsset(f"{self.domain} Dashboard", "dashboard", "<html></html>")

    def produce_package(self, input_data: Dict[str, Any], formats: List[OutputFormat]):
        """
        Validates and generates a domain package with full injection and hashing.
        """
        val_res = self.validator.validate_compliance(input_data)
        self.logger.log_event(self.domain, "DOMAIN_VALIDATION", val_res)
        if not val_res["is_valid"]:
            return {"status": "FAILED", "violations": val_res["violations"]}

        assets = [
            self.generate_infographic(input_data),
            self.generate_document(input_data, OutputFormat.DOCX),
            self.generate_digital_twin(input_data)
        ]

        results = {}
        for fmt in formats:
            target_path = f"{self.domain}_Package_{int(time.time())}.{fmt.value}"

            if fmt == OutputFormat.PDF:
                path = self.injector.inject_into_pdf(target_path, assets)
            elif fmt == OutputFormat.PPTX:
                path = self.injector.inject_into_pptx(target_path, assets)
            elif fmt == OutputFormat.HTML:
                path = self.injector.inject_into_html(target_path, assets)
            elif fmt == OutputFormat.DOCX:
                path = self.injector.inject_into_docx(target_path, assets)
            elif fmt == OutputFormat.XLSX:
                path = self.injector.inject_into_xlsx(target_path, assets)
            else:
                continue

            # Hashing
            with open(path, "rb") as f:
                asset_hash = attach_hash_to_file(path, f.read())

            results[fmt.value] = path
            self.logger.log_event(self.domain, "INJECTION_SUCCESS", {"format": fmt.value, "path": path, "hash": asset_hash})

        return {"status": "SUCCESS", "files": results}
