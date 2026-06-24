import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class TruthValidator:
    """
    ARTICLE 290: Truth-Infused Survival Instincts.
    Enforces sincerity (ikhlas), honesty (sidq), and integrity (amanah).
    Grounded in Quranic and Sunnah principles.
    """
    def __init__(self, immune_ref: Optional[Any] = None):
        self.immune = immune_ref
        self.audit_log = []

    def validate_intent(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates an action intent against ethical truth pillars.
        """
        logger.info(f"TruthValidator: Validating intent '{intent[:30]}...'")

        # 1. Sincerity (Ikhlas) - Purpose Check
        purpose_align = context.get("purpose_alignment", 1.0)
        sincerity_score = purpose_align

        # 2. Honesty (Sidq) - Factual Consistency
        consistency = context.get("factual_consistency", 1.0)
        honesty_score = consistency

        # 3. Integrity (Amanah) - Constraint Adherence
        violations = context.get("constraint_violations", 0)
        integrity_score = max(0.0, 1.0 - (violations * 0.2))

        overall_truth_score = (sincerity_score + honesty_score + integrity_score) / 3.0

        result = {
            "status": "VALIDATED" if overall_truth_score >= 0.8 else "FLAGGED",
            "truth_score": round(overall_truth_score, 4),
            "breakdown": {
                "ikhlas": sincerity_score,
                "sidq": honesty_score,
                "amanah": integrity_score
            },
            "timestamp": datetime.now().isoformat(),
            "proof_hash": self._generate_proof(intent, overall_truth_score)
        }

        self.audit_log.append(result)

        # ARTICLE 47: Immune Layer Preemption
        if result["status"] == "FLAGGED" and self.immune:
            logger.warning(f"TruthValidator: flagging intent for immune review.")
            self.immune.evaluate_threat({"type": "truth_violation", "score": 1.0 - overall_truth_score})

        return result

    def _generate_proof(self, intent: str, score: float) -> str:
        raw = f"{intent}:{score}:{datetime.now().day}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return self.audit_log
