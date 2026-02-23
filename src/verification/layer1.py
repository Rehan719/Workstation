from typing import Any, Dict, Optional
import hashlib
import json
from src.ueg.ledger import UnifiedEvidenceGraph

class SourceVerifier:
    """
    Layer 1: Source Integrity & Provenance (v53 Mastery).
    Verifies the authenticity and origin of ingested artifacts using Sigstore and Merkle roots.
    """
    def __init__(self, ueg: Optional[UnifiedEvidenceGraph] = None):
        self.ueg = ueg

    async def verify_integrity(self, artifact_data: Any, signature: str) -> bool:
        """
        Verifies artifact against its cryptographic signature and checks blockchain ledger.
        """
        # 1. Sigstore Verification Simulation
        expected_sig = hashlib.sha256(f"sigstore:{json.dumps(artifact_data, sort_keys=True)}".encode()).hexdigest()
        sig_valid = (expected_sig == signature)

        # 2. Ledger Integrity Verification (v53 Mastery)
        ledger_valid = True
        if self.ueg and self.ueg.ledger:
            ledger_valid = self.ueg.ledger.verify_integrity()

        return sig_valid and ledger_valid

    async def verify_merkle_root(self, block_index: int, root: str) -> bool:
        """
        Explicitly verifies a block's Merkle root for high-stakes auditing.
        """
        if not self.ueg or not self.ueg.ledger:
            return False

        if block_index >= len(self.ueg.ledger.blocks):
            return False

        block = self.ueg.ledger.blocks[block_index]
        return block['merkle_root'] == root
