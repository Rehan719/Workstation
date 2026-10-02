import os
import hashlib
import json
from decimal import Decimal
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
# W535 (FU-332) — was `from agentic_core.crypto import pqc`, a module that DOES NOT EXIST: that
# package holds only entropy_pool.py, so this file could not be imported at all. The attestation
# module is the real primitive this repository has, and it states in its own docstring that what it
# computes is a keyed MAC and not a post-quantum signature.
from agentic_core import attestation

class RealMultiSigProtocol:
    """
    Module 3B Upgrade: Real MultiSig Protocol logic.
    Proposals are attested with the platform's keyed MAC (agentic_core.attestation) and verified
    three-state: a signature that CANNOT be checked is neither valid nor invalid, and never counts
    toward quorum. W535 — this line claimed signed submission and on-chain verification; neither
    existed, and the function it called was absent from the package it was imported from.
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
        """Record a signer's approval, only if the signature actually verifies.

        W535 (FU-332) — this called a verification function that did not exist, and returned a bare bool, so
        "the signature is invalid" and "the signature could not be checked" were indistinguishable to every
        caller. They are different facts and only one of them is the signer's fault. verify() is three-state,
        and the middle state is the one that matters here: an unverifiable signature MUST NOT count toward
        quorum, because a quorum assembled from signatures nobody could check is not a quorum.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal not found.")

        proposal = self.proposals[proposal_id]

        _record = {"algorithm": attestation.ALGORITHM, "signed": True,
                   "signature": signature.hex() if isinstance(signature, bytes) else str(signature)}
        _v = attestation.verify({"proposal_id": proposal_id, "signer_did": signer_did}, _record)

        if _v.get("verified") is None:
            # NOT a rejection and NOT an approval. Nothing is recorded against the signer.
            await self.ueg.log_event("MULTISIG_SIGNATURE_UNVERIFIABLE", {
                "proposal_id": proposal_id, "signer": signer_did,
                "basis": _v.get("basis"),
                "counted_toward_quorum": False,
                "why": ("the signature could not be checked, which is not the same as invalid; it is not "
                        "counted, because a quorum of unchecked signatures is not a quorum")})
            return False

        if _v.get("verified") is False:
            await self.ueg.log_event("MULTISIG_INVALID_SIGNATURE", {
                "proposal_id": proposal_id, "signer": signer_did, "basis": _v.get("basis")})
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
