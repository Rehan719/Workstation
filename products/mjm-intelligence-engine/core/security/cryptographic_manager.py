import hashlib
from typing import Dict, Any, Optional

class CryptographicManager:
    """
    Sovereign security controls: key management, signing, and verification.
    """
    def __init__(self, key_path: str = "security/keys"):
        self.key_path = key_path

    def sign_artifact(self, content: str) -> str:
        """Simulates signing an artifact with a local key."""
        # v1.0 simplified signing
        return hashlib.sha256(content.encode()).hexdigest()

    def verify_signature(self, content: str, signature: str) -> bool:
        """Verifies the integrity of a signed artifact."""
        return self.sign_artifact(content) == signature

    def generate_causal_chain_hash(self, prev_hash: str, current_content: str) -> str:
        """Creates a tamper-evident link in a provenance chain."""
        return hashlib.sha256((prev_hash + current_content).encode()).hexdigest()
