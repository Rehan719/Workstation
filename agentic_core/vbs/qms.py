import logging
from typing import Dict, Any, List

from agentic_core.vbs.dcms import DocumentControlManagementSystem


class QualityManagementSystem:
    """
    VBS: QMS Gatekeeper.
    Enforces ISO 9001-aligned quality thresholds and OAM validation.

    The QMS OWNS the Document Control Management System: in a real quality system (ISO 9001 §7.5),
    control of documented information is a core *function of* the QMS, not a sibling system. So the QMS
    holds the DCMS as its document-control subsystem and exposes `control_document(...)` to place any
    quality record / controlled document under versioned, SHA3-512-sealed control.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("QMS")
        self.min_coverage = 0.95
        self.defects: List[Dict[str, Any]] = []
        # ── The QMS owns document control (ISO 9001 §7.5). One DCMS instance, owned here.
        self.dcms = DocumentControlManagementSystem(config_path)
        self.controlled_documents = 0

    async def run_quality_gates(self, metadata: Dict[str, Any]) -> bool:
        """
        Enforces >95% test coverage and zero-stub policy.
        """
        coverage = metadata.get("coverage", 0.0)
        stubs_found = metadata.get("stubs_found", False)

        passed = (coverage >= self.min_coverage) and not stubs_found

        if not passed:
            self.defects.append({"id": "QG_FAIL", "meta": metadata})
            self.logger.warning(f"QMS: Quality Gate FAILED. Coverage: {coverage}")

        return passed

    def get_non_conformance_rate(self) -> float:
        return len(self.defects) / 100.0  # Normalized

    async def control_document(self, doc_id: str, content: Dict[str, Any], actor: str) -> str:
        """Place a document under QMS document control — versioned + SHA3-512 sealed via the OWNED DCMS.
        Returns the controlled-document hash (the proof the record is under quality document control)."""
        h = await self.dcms.commit_artifact(doc_id, content, actor)
        self.controlled_documents += 1
        return h

    def document_control_status(self) -> Dict[str, Any]:
        """The QMS's document-control posture — proves the DCMS is owned and operating under the QMS."""
        return {
            "owned_subsystem": "DCMS (Document Control Management System)",
            "controlled_documents": self.controlled_documents,
            "registered_artifacts": len(self.dcms.registry),
            "audit_integrity": self.dcms.get_audit_integrity(),
        }
