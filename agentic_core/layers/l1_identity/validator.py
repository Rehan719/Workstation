import json
import hashlib
from typing import Dict, Any, List, Optional
import enum
from agentic_core.layers.l11_civilisation.civilisation import mycelial_stack

class ConstitutionalValidatorL1:
    """
    LAYER 1: IDENTITY - Immutable Genome Core.
    Enforces Floor 22 with LIVE service checks.
    """
    def __init__(self, constitution_path: str = "genome/constitution.work"):
        try:
            with open(constitution_path, "r") as f:
                self.genome = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.genome = {"identity": {"merkle_root": "0xgenesis_v3"}}

        self.merkle_root = self.genome.get('identity', {}).get('merkle_root', '0xcivilizational_epoch_v3')
        self.trust_factors: Dict[str, float] = {"default": 0.8}

    def validate_action(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        GaaS Middleware: Natural Language Interpretation & Live Floor 22 Enforcement.
        """
        user_id = context.get("user_id", "default")
        trust_score = self.trust_factors.get(user_id, 0.8)

        # LIVE Check: Article 1104 - Federated Scale (≥50 Nodes)
        if action == "mesh_expansion":
             active_nodes = len(mycelial_stack.peers)
             if active_nodes < 50:
                  return {"valid": False, "reason": f"Article 1104 violation: Cluster has only {active_nodes} nodes (target 50+)."}

        # Article 1107: Mandatory PQC
        if not context.get("pqc_active") and action not in ["pqc_enable", "status_check"]:
             return {"valid": False, "reason": "Article 1107 violation: PQC mandatory."}

        # Article 1101: 10m Veto for high risk
        if context.get("risk") == "high" and context.get("veto_window", 0) < 10:
             return {"valid": False, "reason": "Article 1101 violation: 10-minute veto required."}

        # LIVE Check: Article 1104 - Privacy ε≤0.1
        if action == "federated_sync" and context.get("epsilon", 1.0) > 0.1:
             return {"valid": False, "reason": "Article 1104 violation: Privacy budget ε > 0.1."}

        return {"valid": True, "trust_score": trust_score, "mode": "PRODUCTION_LIVE"}

    def update_trust(self, user_id: str, delta: float):
        self.trust_factors[user_id] = max(0.0, min(1.0, self.trust_factors.get(user_id, 0.8) + delta))

validator_l1 = ConstitutionalValidatorL1()
