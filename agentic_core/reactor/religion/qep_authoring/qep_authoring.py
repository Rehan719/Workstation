import logging
import datetime
import uuid
from typing import Dict, Any, List
from agentic_core.reactor.ecosystem.base import SpecializedReactor

logger = logging.getLogger(__name__)

class QEPAuthoringReactor(SpecializedReactor):
    """
    ARTICLE D3: QEP Authoring Tools Reactor — an adapter over the scholar-review gate.

    Scholars contribute tafsir, translations and educational content here; approval is performed by
    agentic_core.api.scholar_review, which persists the queue and checks the reviewer against a roster.

    W594 (R7, Owner ruling 2026-10-05b on A.12.3) — before this, the queue was a list on the instance and
    approval tested a trust score the CALLER supplied about itself. It had the shape of §11's required
    audit and verified nothing, which is worse than having no mechanism: a reader of this file would
    conclude the audit existed.
    """
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("religion", "qep_authoring", config or {})
        #  W594 (R7) — NO IN-MEMORY QUEUE. `self.annotations` and `self.approval_queue` were plain lists
        #  here, so every approval died with the process and nothing a scholar did survived a restart.
        #  The state lives in agentic_core.api.scholar_review, which persists it under a lock and is the
        #  same record the learner-facing surface reads.

    async def incubate(self, input_data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        task = params.get("task", "submit_annotation")

        if task == "submit_annotation":
            return await self._submit_annotation(input_data, params)
        elif task == "approve_annotation":
            return await self._approve_annotation(input_data, params)
        elif task == "get_pending":
            from agentic_core.api import scholar_review as _sr
            _all = _sr._load(_sr._review_path())
            return {"status": "SUCCESS", "message": None,
                    "pending": [r for r in _all.values() if r.get("state") == _sr.IN_REVIEW],
                    "gate": _sr.gate_status(),
                    "detail": ("the queue is persisted and shared with the learner-facing gate, so this "
                               "is what a scholar would actually see")}

        #  shape-complete beside its siblings: a caller reading `detail` on an unknown task gets a
        #  sentence rather than a KeyError, and `pending`/`gate` are present and empty rather than absent
        return {"status": "ERROR", "message": "Unknown task", "detail": f"no task named {task!r}",
                "pending": [], "gate": None}

    async def _submit_annotation(self, content: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Queue a contribution for review. Submitting has never approved anything and still does not."""
        from agentic_core.api import scholar_review as _sr
        _ref = str(params.get("reference") or "")
        _type = str(params.get("type", "tafsir"))
        _key = f"authoring:{_type}:{_ref or uuid.uuid4().hex[:8]}"
        rec = _sr.submit_if_new(_key, f"qep_authoring/{_type}", content, reference=_ref)
        logger.info("QEPAuthoring: contribution queued for scholarly review (%s)", _key)
        return {"status": "SUCCESS", "annotation_id": _key, "state": rec.get("state"),
                "detail": ("queued for review. It is not published to any learner until a scholar on the "
                           "roster approves it - and with an empty roster nothing can be.")}

    async def _approve_annotation(self, annotation_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Approval is by RECORDED IDENTITY, never by a score the caller asserts about itself.

        W594 (R7) — this read `trust_score` out of the caller's own params and approved anything at or
        above 0.9, recording `scholar_id` as whatever the caller typed. Any caller could approve any
        contribution and sign it with any name. The reviewer is now checked against the scholar roster,
        which is empty until the Owner puts a real person in it.
        """
        from agentic_core.api import scholar_review as _sr
        reviewer = str(params.get("scholar_id") or "")
        if not reviewer:
            return {"status": "DENIED", "annotation": None, "reason": "no reviewer named",
                    "detail": "An approval must record WHO approved it; no scholar_id was supplied."}
        result = _sr.decide(annotation_id, reviewer, approve=True, note=str(params.get("note") or ""))
        if not result.get("ok"):
            return {"status": "DENIED", "annotation": None,
                    "reason": result.get("reason"), "detail": result.get("detail")}
        logger.info("QEPAuthoring: %s approved by %s", annotation_id, reviewer)
        return {"status": "SUCCESS", "annotation": result["record"],
                "reason": result.get("reason"), "detail": result.get("detail")}

    async def analyze(self, data: Any) -> Dict[str, Any]:
        from agentic_core.api import scholar_review as _sr
        _st = _sr.gate_status()
        return {"total_approved": _st["by_state"].get(_sr.APPROVED, 0),
                "total_pending": _st["by_state"].get(_sr.IN_REVIEW, 0),
                "scholars_on_roster": _st["scholars_on_roster"],
                "basis": _st["basis"]}

    async def validate_truth(self, content: Any) -> Dict[str, Any]:
        return {"is_truth": True, "confidence": 1.0}

    async def generate_artifact(self, data: Any, format: str = "pdf") -> Dict[str, Any]:
        return {"type": "ANNOTATION_EXPORT", "url": "https://workstation.ai/qep/export"}

    async def interact(self, state: Any, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "SUCCESS"}

    async def visualize(self, data: Any, mode: str) -> Dict[str, Any]:
        return {"view": "AUTHORING_INTERFACE"}
