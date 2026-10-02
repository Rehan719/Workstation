"""
Avatar Mushāwara Bridge (vΩ∞-AVATAR-OMNISYNTHESIS).
Deliberative consensus management for cognitive emissions.
"""
from typing import Dict, Any, List, Optional
import time
import logging
import hashlib
import json
from agentic_core.consultation.mushawara.mushawara_bridge_2 import MushawaraBridge2
from agentic_core.avatars.cognition.nine_engine_registry import EngineRegistry9

logger = logging.getLogger(__name__)

class AvatarCognitiveOrchestrator:
    """
    IDBO Layer 9: Orchestration / Cognitive Swarm.
    Manages 9 engines and enforces Mushāwara consensus for high-impact emissions.
    """
    def __init__(self, ueg_logger: Any, enforcement: Any):
        self.ueg = ueg_logger
        self.enforcement = enforcement
        self.registry = EngineRegistry9(ueg_logger, enforcement)
        self.bridge = MushawaraBridge2(ueg_logger, self.registry.registry)

    async def process_engine(self, engine_id: str, input_data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Forward processing to the 9-engine registry."""
        return await self.registry.get_engine_response(engine_id, input_data, context)

    async def consult(self, task: Dict[str, Any], engine_ids: List[str]) -> Dict[str, Any]:
        """
        Synthesize collective intelligence from the cognitive swarm.
        Ensures ≥3 engine perspectives for metabolic consistency.
        """
        etypes = self.registry.get_types(engine_ids)

        # Article Mandate: Minimum 3 engines for high-impact strategy
        if len(etypes) < 3:
             from agentic_core.cognitive.registry import EngineType
             etypes = list(set(etypes + [EngineType.INKASHAF, EngineType.AQAL, EngineType.SAMAJH]))[:3]

        query = type('ConsultationQuery', (), {
            "id": f"q_{int(time.time())}",
            "query": task.get("task", "Analyze instruction"),
            "domain": task.get("domain", "general"),
            "context": task.get("context", {})
        })()

        result = await self.bridge.deliberate(query, etypes)

        # W533 — `agreement_score` is three-state now, and it no longer means what this code assumed. It
        # used to be the mean of the engines' confidences wearing the name "agreement" (every perspective
        # supplied the same constant vector, so the bundle reduced to that mean); it is now the concordance
        # of the constitutional verdicts, and None where nothing supplied one. Defaulting it to 0.0 would
        # read "nothing assessed this" as "total disagreement", so the absence is carried through.
        _out = result.get("outcome", {}) or {}
        agreement = _out.get("agreement_score")
        result["outcome"]["synthesized_response"] = self._synthesize_text(task, agreement, result)
        result["outcome"]["expression"] = ("encouraging" if isinstance(agreement, float) and agreement > 0.8
                                           else "thinking")

        return result

    def _synthesize_text(self, task: Dict, agreement, result: Dict = None) -> str:
        """Render the deliberation's outcome WITHOUT overstating it.

        W533 — this claimed "I have refined a definitive strategy" whenever the number exceeded 0.9. That
        number was the mean confidence of the engines, which refuse for want of a model path, so the strongest
        claim on this surface was reachable without any strategy having been refined. A user-facing claim is
        made only when the deliberation actually cleared, and an unassessed deliberation says so.
        """
        user_input = task.get("context", {}).get("input", "")
        status = (result or {}).get("status")
        if agreement is None:
            return (f"I have not been able to assess '{user_input}': the cognitive perspectives returned no "
                    "constitutional verdict to agree or disagree on.")
        if status == "BLOCKED":
            return f"I cannot proceed on '{user_input}': the deliberation returned a failing verdict."
        if status == "APPROVED" and agreement >= 1.0:
            return f"The perspectives agree on a strategy for '{user_input}'."
        return f"I am evaluating the optimal path for '{user_input}'."

    async def verify_output(self, emission: Dict[str, Any]) -> Dict[str, Any]:
        """Tahqeeq: Final verification gate with Zero-Placeholder enforcement."""
        content = emission.get("text", "")
        if not content:
            return {"verified": False, "reason": "Null emission block"}

        # W533 — two of the five needles here could NEVER match. The test was `p in content.upper()` with
        # lowercase needles, so against an uppercased haystack they are unmatchable whatever the emission
        # says, and a gate that cannot fire is not a gate. The three that could fire substring-matched
        # PROSE, so an ordinary English word inside a sentence to a user would be refused as a placeholder.
        # Both halves are fixed by comparing in one case and matching whole tokens; the ordinary English
        # word that was one of the unmatchable needles is deliberately NOT restored, because in prose
        # written for a user it carries no placeholder signal and would only produce false refusals.
        import re as _re
        for p in ("TODO", "FIXME", "STUB", "NotImplementedError", "FIX ME"):
            if _re.search(r"\b" + _re.escape(p) + r"\b", content, _re.IGNORECASE):
                return {"verified": False, "reason": f"CRITICAL: Zero-placeholder '{p}' detected"}

        return {
            "verified": True,
            # W533 — the refusing branches carry a `reason` and this one did not, so a caller reading
            # res["reason"] raised exactly when the emission had CLEARED.
            "reason": "no placeholder token was found in the emission text",
            "merkle_proof": hashlib.sha3_512(json.dumps(emission, sort_keys=True).encode()).hexdigest()
        }
