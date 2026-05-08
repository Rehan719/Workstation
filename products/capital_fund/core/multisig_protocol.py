import hashlib
import json
from datetime import datetime, UTC
from typing import List, Dict, Any, Optional
from decimal import Decimal

class MultiSigProtocol:
    """
    Phase 1: Cryptographically verifiable simulated quorum (>=3/5 PQC-signed local keys).
    Simulates MultiSigCouncil for high-risk fund operations.
    """
    def __init__(self, council_members: List[str] = None):
        # Default 5 simulated council members
        self.council_members = council_members or [
            "council_member_1", "council_member_2", "council_member_3",
            "council_member_4", "council_member_5"
        ]
        self.threshold = 3

    async def initiate_proposal(self, operation: str, amount: Decimal, requester_did: str) -> str:
        """Create a proposal hash for the council to sign."""
        proposal_data = {
            "operation": operation,
            "amount": str(amount),
            "requester": requester_did,
            "timestamp": datetime.now(UTC).isoformat(),
            "nonce": hashlib.sha256(str(datetime.now(UTC).timestamp()).encode()).hexdigest()[:8]
        }
        return hashlib.sha3_512(json.dumps(proposal_data, sort_keys=True).encode()).hexdigest()

    async def verify_quorum(self, proposal_hash: str, signatures: List[Dict[str, str]]) -> bool:
        """
        Verify that at least threshold signatures are valid and from council members.
        Phase 1: Simulated verification.
        """
        if len(signatures) < self.threshold:
            return False

        valid_signatures = 0
        signers = set()

        for sig in signatures:
            signer = sig.get("signer")
            signature_val = sig.get("signature")

            if signer in self.council_members and signer not in signers:
                # In Phase 1, we simulate verification of PQC signatures
                # In production, we'd use Dilithium5.verify(proposal_hash, signature_val, public_key)
                if self._simulate_pqc_verify(proposal_hash, signature_val, signer):
                    valid_signatures += 1
                    signers.add(signer)

        return valid_signatures >= self.threshold

    def _simulate_pqc_verify(self, message: str, signature: str, signer: str) -> bool:
        """Simulated Dilithium5 signature verification."""
        # Check if signature follows expected simulated format: "pqc_sig_<signer>_<message_hash[:8]>"
        expected_prefix = f"pqc_sig_{signer}_"
        return signature.startswith(expected_prefix) and signature.endswith(message[:8])

    def generate_simulated_signature(self, proposal_hash: str, signer: str) -> str:
        """Helper to generate a simulated signature for testing."""
        return f"pqc_sig_{signer}_{proposal_hash[:8]}"
