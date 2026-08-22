import logging
import time
import uuid
from typing import Dict, Any, List, Optional

from agentic_core.vbs.dcms import DocumentControlManagementSystem


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class QualityManagementSystem:
    """
    VBS: QMS Gatekeeper.
    Enforces ISO 9001-aligned quality thresholds and OAM validation.

    The QMS OWNS the Document Control Management System: in a real quality system (ISO 9001 §7.5),
    control of documented information is a core *function of* the QMS, not a sibling system. So the QMS
    holds the DCMS as its document-control subsystem and exposes `control_document(...)` to place any
    quality record / controlled document under versioned, SHA3-512-sealed control.

    §10 (W307) — genuinely stateful and honest:
    - defects PERSIST (atomic JSON store) and are TRACEABLE (unique id · label · metrics · timestamps);
    - the non-conformance rate is a REAL rate (gate failures / gates run), not a normalised constant;
    - the ISO 8.7/10.2 loop exists: a defect is corrected, then RE-VERIFIED by re-running the same
      gate on the corrected delivery's real metrics — it closes only on a genuine pass, and reopens
      when a correction does not hold.
    """
    def __init__(self, config_path: str):
        self.logger = logging.getLogger("QMS")
        self.min_coverage = 0.95
        # ── The QMS owns document control (ISO 9001 §7.5). One DCMS instance, owned here.
        self.dcms = DocumentControlManagementSystem(config_path)
        self.controlled_documents = 0
        self._store_name = f"qms_state_{config_path}.json"
        self._state: Optional[Dict[str, Any]] = None

    # ── persistent state (lazy: data_path resolves the live DATA_DIR at first use) ──
    def _load_state(self) -> Dict[str, Any]:
        if self._state is None:
            from agentic_core.config import load_json_tolerant, data_path
            self._state = load_json_tolerant(
                data_path(self._store_name), {"gates_run": 0, "defects_total": 0, "defects": []})
        return self._state

    def _save_state(self) -> None:
        if self._state is not None:
            from agentic_core.config import atomic_write_json, data_path
            atomic_write_json(data_path(self._store_name), self._state)

    @property
    def defects(self) -> List[Dict[str, Any]]:
        return self._load_state()["defects"]

    async def run_quality_gates(self, metadata: Dict[str, Any], label: str = "delivery") -> bool:
        """
        Enforces >95% test coverage and zero-stub policy. A failure opens a persistent,
        traceable defect (unique id, the label of the delivery surface, the real metrics).
        """
        coverage = float(metadata.get("coverage", 0.0))
        stubs_found = bool(metadata.get("stubs_found", False))
        passed = (coverage >= self.min_coverage) and not stubs_found

        st = self._load_state()
        st["gates_run"] = int(st.get("gates_run", 0)) + 1
        if not passed:
            st["defects_total"] = int(st.get("defects_total", 0)) + 1
            st["defects"].append({
                "id": f"DEF-{uuid.uuid4().hex[:8]}",
                "label": label,
                "meta": {"coverage": coverage, "stubs_found": stubs_found},
                "status": "open",
                "opened_at": _now(),
                "correction": None,
                "reverified": False,
            })
            st["defects"] = st["defects"][-500:]   # bounded list; defects_total keeps the true count
            self.logger.warning(f"QMS: Quality Gate FAILED ({label}). Coverage: {coverage}")
        self._save_state()

        return passed

    def get_non_conformance_rate(self) -> float:
        """REAL rate: gate failures over gates run (0.0 with no history — never a fabricated figure)."""
        st = self._load_state()
        gates = int(st.get("gates_run", 0))
        return round(int(st.get("defects_total", 0)) / gates, 4) if gates > 0 else 0.0

    # ── §10 (W307) — the defect → correction → re-verify loop (ISO 9001 §8.7 / §10.2) ──
    def correct_defect(self, defect_id: str, correction: str, actor: str = "owner") -> Optional[Dict[str, Any]]:
        """Record the correction taken for an OPEN defect. The defect is not closed here —
        closure requires re-verification against real metrics."""
        st = self._load_state()
        for d in st["defects"]:
            if d["id"] == defect_id and d["status"] == "open":
                d["status"] = "corrected"
                d["correction"] = str(correction)[:2000]
                d["corrected_at"] = _now()
                d["corrected_by"] = actor
                self._save_state()
                return d
        return None

    def reverify_defect(self, defect_id: str, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Re-run the SAME gate on the corrected delivery's REAL metrics. Closes only on a genuine
        pass; a failed re-verification REOPENS the defect (the correction did not hold)."""
        st = self._load_state()
        for d in st["defects"]:
            if d["id"] == defect_id and d["status"] == "corrected":
                coverage = float(metadata.get("coverage", 0.0))
                stubs_found = bool(metadata.get("stubs_found", False))
                passed = (coverage >= self.min_coverage) and not stubs_found
                st["gates_run"] = int(st.get("gates_run", 0)) + 1
                d["reverified"] = passed
                d["reverify_meta"] = {"coverage": coverage, "stubs_found": stubs_found}
                d["reverified_at"] = _now()
                d["status"] = "closed" if passed else "open"
                self._save_state()
                return {"defect": d, "passed": passed}
        return None

    def defect_summary(self) -> Dict[str, Any]:
        st = self._load_state()
        by = {"open": 0, "corrected": 0, "closed": 0}
        for d in st["defects"]:
            by[d.get("status", "open")] = by.get(d.get("status", "open"), 0) + 1
        return {"gates_run": int(st.get("gates_run", 0)),
                "defects_total": int(st.get("defects_total", 0)), **by,
                "non_conformance_rate": self.get_non_conformance_rate()}

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
