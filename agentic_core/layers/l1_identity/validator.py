import json
import hashlib
from typing import Dict, Any, List, Optional
import enum

class EnforcementMode(enum.Enum):
    COERCIVE = "Immediate Block"
    NORMATIVE = "Warning & Reflection"
    ADAPTIVE = "Context-Based Adjustment"

class ConstitutionalValidatorL1:
    """
    LAYER 1: IDENTITY - Immutable Genome Core.
    Enforces Articles 1-1095 with GaaS Enforcement Modes and Trust Factor (T Fa).
    """
    def __init__(self, constitution_path: str = "genome/constitution.work"):
        try:
            with open(constitution_path, "r") as f:
                self.genome = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.genome = {
                "entity": "Workstation Sovereign v3.0",
                "identity": {"did": "did:vsb:sovereign-v3", "merkle_root": "0xgenesis_v3"},
                "constitution": {"articles": [{"id": 1095, "content": "All actions must pass GaaS validation."}]}
            }

        self.merkle_root = self.genome.get('identity', {}).get('merkle_root', '0xgenesis_v3')
        self.trust_factors: Dict[str, float] = {"default": 0.8} # T Fa score

    def get_enforcement_mode(self, action: str, trust_score: float) -> EnforcementMode:
        """Determines enforcement severity based on risk and trust."""
        high_risk_actions = ["financial_transfer", "genome_amendment", "pqc_disable"]

        if action in high_risk_actions or trust_score < 0.4:
            return EnforcementMode.COERCIVE
        if trust_score < 0.7:
            return EnforcementMode.NORMATIVE
        return EnforcementMode.ADAPTIVE

    def validate_action(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        GaaS Middleware: Natural Language Interpretation & Constitutional Enforcement.
        """
        user_id = context.get("user_id", "default")
        trust_score = self.trust_factors.get(user_id, 0.8)
        mode = self.get_enforcement_mode(action, trust_score)

        print(f"GaaS [L1]: Validating '{action}' (T Fa: {trust_score}) in {mode.value} mode.")

        # Rule: Recombination requires fitness (Article 1095)
        if action == "recombine" and "fitness" not in context:
            if mode == EnforcementMode.COERCIVE:
                return {"valid": False, "reason": "Article 1095 violation.", "mode": mode.name}
            print("GaaS Warning: Article 1095 requires fitness for recombination.")

        # Rule: Autonomous veto window (Article 1091)
        if action == "execute_workflow" and context.get("autonomous") and not context.get("veto_window"):
            return {"valid": False, "reason": "Article 1091 violation: 10m veto required.", "mode": mode.name}

        return {"valid": True, "trust_score": trust_score, "mode": mode.name}

    def update_trust(self, user_id: str, delta: float):
        self.trust_factors[user_id] = max(0.0, min(1.0, self.trust_factors.get(user_id, 0.8) + delta))

validator_l1 = ConstitutionalValidatorL1()
