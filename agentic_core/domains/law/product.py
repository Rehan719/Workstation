from typing import Dict, Any, List
from agentic_core.omnimedia.factory import OctoOmnimediaGenerator, MultimediaAsset, OutputFormat
from agentic_core.omnimedia.injector import OmnimediaInjector
from agentic_core.constitutional.gaas_validator_v2 import ConstitutionalValidatorV2
from agentic_core.constitutional.ueg_logger import UEGLogger
import os

class LawProductGenerator(OctoOmnimediaGenerator):
    def __init__(self):
        self.domain = "Law"
        self.validator = ConstitutionalValidatorV2(self.domain)
        self.logger = UEGLogger()
        self.injector = OmnimediaInjector()

    def generate_infographic(self, data: Dict[str, Any]) -> MultimediaAsset:
        # Precedent timeline or similar
        return MultimediaAsset(
            name=data.get("name", "Law Infographic"),
            asset_type="infographic",
            content=None, # Allow injector to generate mock image
            metadata={"accessibility": {"alt_text": "A timeline of legal precedents."}}
        )

    def generate_video(self, data: Dict[str, Any]) -> MultimediaAsset:
        return MultimediaAsset(
            name=data.get("name", "Law Video"),
            asset_type="video",
            content=None,
            metadata={"accessibility": {"alt_text": "Explainer video about ET1 process."}}
        )

    def generate_audio(self, data: Dict[str, Any]) -> MultimediaAsset:
        return MultimediaAsset(
            name=data.get("name", "Law Audio"),
            asset_type="audio",
            content=None,
            metadata={"accessibility": {"transcript": "This is a recording of the hearing details."}}
        )

    def generate_digital_twin(self, data: Dict[str, Any]) -> MultimediaAsset:
        return MultimediaAsset(
            name=data.get("name", "Courtroom Digital Twin"),
            asset_type="digital_twin",
            content=None,
            metadata={"accessibility": {"alt_text": "3D layout of the Employment Tribunal room."}}
        )

    def generate_document(self, data: Dict[str, Any], format: OutputFormat) -> MultimediaAsset:
        # ET1 or Schedule of Loss
        return MultimediaAsset(
            name=data.get("name", "Legal Document"),
            asset_type="document",
            content=data.get("text", "Default legal text"),
            metadata={"accessibility": {"tags": ["legal", "official"]}}
        )

    def generate_dashboard(self, data: Dict[str, Any]) -> MultimediaAsset:
        return MultimediaAsset(
            name="Law Dashboard",
            asset_type="dashboard",
            content="<html><body>Dashboard Content</body></html>"
        )

    def create_et1_package(self, claimant_data: Dict[str, Any], target_formats: List[OutputFormat], mode: str = "warning"):
        """
        Pilot: Generates ET1 and Schedule of Loss, validates, and injects into formats.
        """
        # Update validator mode
        self.validator.mode = mode

        # 1. Validation
        validation_result = self.validator.validate_compliance(claimant_data)
        self.logger.log_event(self.domain, "ET1_VALIDATION", {
            "is_valid": validation_result["is_valid"],
            "actual_valid": validation_result.get("actual_valid"),
            "violations": validation_result["violations"]
        })

        if not validation_result["is_valid"]:
            return {"status": "FAILED", "violations": validation_result["violations"]}

        # 2. Asset Generation
        assets = [
            self.generate_infographic({"name": "Precedent Timeline"}),
            self.generate_digital_twin({"name": "Tribunal Layout"}),
            self.generate_document({"name": "ET1 Form", "text": "Formal ET1 details..."}, OutputFormat.DOCX)
        ]

        # 3. Injection
        results = {}
        for fmt in target_formats:
            target_path = f"ET1_Package_{claimant_data['et1_form']['claimant_name']}.{fmt.value}"
            if fmt == OutputFormat.PDF:
                path = self.injector.inject_into_pdf(target_path, assets)
            elif fmt == OutputFormat.PPTX:
                path = self.injector.inject_into_pptx(target_path, assets)
            elif fmt == OutputFormat.DOCX:
                path = self.injector.inject_into_docx(target_path, assets)
            elif fmt == OutputFormat.XLSX:
                path = self.injector.inject_into_xlsx(target_path, assets)
            elif fmt == OutputFormat.HTML:
                path = self.injector.inject_into_html(target_path, assets)
            else:
                continue

            results[fmt.value] = path
            self.logger.log_event(self.domain, "INJECTION_SUCCESS", {"format": fmt.value, "path": path})

        return {"status": "SUCCESS", "files": results}
