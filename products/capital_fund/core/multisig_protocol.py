import os
import hashlib
import json
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from agentic_core.crypto import pqc

class RealMultiSigProtocol:
    """
    Module 3B Upgrade: Real MultiSig Protocol logic.
    Supports PQC-signed proposal submission and on-chain signature verification logic.
    """
    def __init__(self, ueg: UEGLogger):
        self.ueg = ueg
        self.quorum_threshold = 3
        self.proposals: Dict[str, Dict[str, Any]] = {}

    async def submit_proposal(self, operation: str, amount: Decimal, proposer_did: str, context: Dict[str, Any]) -> str:
        """Submits a withdrawal or high-risk proposal for MultiSig approval."""
        proposal_id = hashlib.sha256(f"{operation}{amount}{proposer_did}{datetime.now(UTC)}".encode()).hexdigest()

        proposal = {
            "proposal_id": proposal_id,
            "operation": operation,
            "amount": float(amount),
            "proposer_did": proposer_did,
            "context": context,
            "status": "PENDING",
            "signatures": {},
            "timestamp": datetime.now(UTC).isoformat()
        }

        self.proposals[proposal_id] = proposal
        await self.ueg.log_event("MULTISIG_PROPOSAL_SUBMITTED", proposal)
        return proposal_id

    async def approve_proposal(self, proposal_id: str, signer_did: str, signature: bytes, public_key: bytes) -> bool:
        """Approves a proposal using PQC verification."""
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        proposal = self.proposals[proposal_id]

        # Verify PQC signature (Dilithium)
        # We use the actual core pqc module
        is_valid = pqc.verify_instruction(proposal_id.encode(), signature, public_key)

        if not is_valid:
            await self.ueg.log_event("MULTISIG_INVALID_SIGNATURE", {"proposal_id": proposal_id, "signer": signer_did})
            return False

        proposal["signatures"][signer_did] = signature.hex() if isinstance(signature, bytes) else str(signature)

        # Check quorum
        if len(proposal["signatures"]) >= self.quorum_threshold:
            proposal["status"] = "APPROVED"
            await self.ueg.log_event("MULTISIG_PROPOSAL_APPROVED", {"proposal_id": proposal_id})
            return True

        return False

    def get_proposal_status(self, proposal_id: str) -> Dict[str, Any]:
        return self.proposals.get(proposal_id, {"status": "NOT_FOUND"})
