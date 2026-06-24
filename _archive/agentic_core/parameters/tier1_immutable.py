from typing import Dict, Any

class Tier1Immutable:
    """CP-I: Foundationally Fixed Parameters."""

    def __init__(self):
        self.immutable_params = {
            "reflex_arc_latency_limit_ms": 50,
            "min_cryptographic_key_size": 384,
            "formal_proof_axioms": "L7_Verified",
            "core_model": "DeepSeek-R1-Mastery"
        }

    def get(self, name: str):
        return self.immutable_params.get(name)

    def is_tier1(self, name: str) -> bool:
        return name in self.immutable_params
