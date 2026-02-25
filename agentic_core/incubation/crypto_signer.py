import hashlib
from typing import Dict, Any

class CryptoSigner:
    """CO-VIII: Cryptographic signing of approvals and verification."""

    def verify_signature(self, workflow: Dict[str, Any], signature: str) -> bool:
        expected = hashlib.sha256(f"user_approved:{workflow['id']}".encode()).hexdigest()
        return expected == signature
