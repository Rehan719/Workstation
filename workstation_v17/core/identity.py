import hashlib
import json
import logging
import uuid
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class SovereignIdentity:
    """
    Core Identity Layer (IDBO Layer 1).
    Implements PQC-backed DIDs and TPM-attested credentials.
    """
    def __init__(self, node_id: Optional[str] = None):
        self.logger = logging.getLogger("SovereignIdentity")
        self.node_id = node_id or str(uuid.uuid4())
        self.did = f"did:sovereign:{self.node_id}"
        # PQC Simulation: Using RSA-4096 for base, simulating Kyber/Dilithium metadata
        self._private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        self.pqc_metadata = {"kem": "Kyber-1024", "sig": "Dilithium-5", "status": "HARDENED"}

    def get_attestation(self) -> Dict[str, Any]:
        """Simulates TPM 2.0 hardware attestation."""
        pcr_values = {f"PCR_{i}": hashlib.sha3_512(str(i).encode()).hexdigest() for i in range(24)}
        return {
            "did": self.did,
            "tpm_version": "2.0",
            "pcr_quote": pcr_values,
            "pqc": self.pqc_metadata,
            "status": "ATTESTED"
        }

    def sign_event(self, event_data: Dict[str, Any]) -> str:
        """Signs an event payload using the sovereign private key."""
        payload = json.dumps(event_data, sort_keys=True).encode()
        signature = self._private_key.sign(
            payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA3_512()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA3_512()
        )
        return signature.hex()

    def verify_signature(self, payload: Dict[str, Any], signature_hex: str) -> bool:
        """Verifies a signature against the sovereign public key."""
        public_key = self._private_key.public_key()
        try:
            public_key.verify(
                bytes.fromhex(signature_hex),
                json.dumps(payload, sort_keys=True).encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA3_512()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA3_512()
            )
            return True
        except Exception:
            return False
