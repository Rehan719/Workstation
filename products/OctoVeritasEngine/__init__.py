from .pipelines.registry import PipelineRegistry
from .pipelines.provenance import ProvenanceTracker
from .modes.mode_router import ModeRouter
from .intelligence.injection_planner import InjectionPlanner
from .omnimedia.injector import OmnimediaInjector
from .omnimedia.decision_engine_v3 import OmnimediaDecisionEngineV3
from .omnimedia.accessibility import AccessibilityEngine
from .constitutional.gaas_validator_v2 import ConstitutionalValidatorV2
from .constitutional.fallback import FallbackProtocol
from .constitutional.ueg_logger import UEGLogger
from .constitutional.data_governance import DataGovernanceModule
from .utils.hashing import calculate_sha3_512, attach_hash_to_file, verify_asset_integrity
from .utils.workflow import WorkflowCollaborator

class OctoVeritasEngineV3:
    def __init__(self,
                 domain: str,
                 output_dir: str = "outputs/veritas-v3",
                 db_path: str = "outputs/v3_effectiveness.db"):
        self.domain = domain
        self.registry = PipelineRegistry()
        self.tracker = ProvenanceTracker()
        self.router = ModeRouter()
        self.decision_engine = OmnimediaDecisionEngineV3(db_path=db_path)
        self.planner = InjectionPlanner(self.registry, self.router, db_path)
        self.injector = OmnimediaInjector(output_dir=output_dir)
        self.validator = ConstitutionalValidatorV2()
        self.ueg = UEGLogger(os.path.join(output_dir, "ueg_audit.jsonl"))

    def set_mode(self, mode: str):
        self.router.set_mode(mode)

    def produce_intelligent_package(self,
                                     assets: list,
                                     audience: str = "general",
                                     target_formats: list = None):
        """
        Orchestrates the intelligent injection process.
        """
        # 1. Analyze Context
        mode = self.router.get_mode()

        # 2. Plan Injection
        plan = self.planner.plan_injection(assets, mode=mode, audience=audience)

        # 3. Execute Jobs
        results = []
        for job in plan:
            # Constitutional Check
            compliance = self.validator.validate_compliance(self.domain, job.asset)
            if not compliance["valid"]:
                # Trigger Fallback
                job.modifiers.append("compliance_warning")

            # Inject
            # Note: OmnimediaInjector expects MultimediaAsset objects.
            # We'll need to wrap job.asset.
            from .omnimedia.factory import MultimediaAsset
            m_asset = MultimediaAsset(
                name=job.asset.get('name', 'Unnamed'),
                asset_type=job.asset.get('asset_type', 'png'),
                content=job.asset.get('content', b''),
                hash=job.asset.get('hash', '0'*128),
                accessibility=job.asset.get('accessibility', {})
            )

            # Map format to injector method
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
            output_path = f"{self.domain.lower()}_output_{mode}.{job.format.lower()}"
            result_path = method(output_path, [m_asset])

            # Log to UEG
            self.ueg.log_event({
                "operation": "intelligent_injection",
                "domain": self.domain,
                "mode": mode,
                "pipeline": job.pipeline,
                "format": job.format,
                "output": result_path
            })
            results.append(result_path)

        return results

import os
