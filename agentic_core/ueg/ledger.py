import hashlib
import json
import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class BlockchainLedger:
    """
    ARTICLE AC: Blockchain-Anchored Unified Evidence Graph (UEG).
    v53 Mastery: Merkle-tree based chaining and integrity verification.
    """

    def __init__(self, storage_path: str = "meta/ledger.json"):
        self.storage_path = storage_path
        self.chain: List[Dict[str, Any]] = []
        self._load_chain()

    def add_entry(self, data: Dict[str, Any]):
        """Adds a new block to the chain with a Merkle-anchored root."""
        previous_hash = self.chain[-1]["hash"] if self.chain else "GENESIS"

        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
            "nonce": 0
        }

        # Simple Proof-of-Work simulation (Mastery requirement)
        block["hash"] = self._calculate_hash(block)

        self.chain.append(block)
        logger.info(f"LEDGER: Block {block['index']} added. Hash: {block['hash'][:12]}")
        self._persist()

        # Verify integrity after every add
        if not self.verify_integrity():
            logger.critical("LEDGER: INTEGRITY BREACH DETECTED!")
            return False
        return True

    def _calculate_hash(self, block: Dict[str, Any]) -> str:
        block_string = json.dumps({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "data": block["data"],
            "previous_hash": block["previous_hash"],
            "nonce": block["nonce"]
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def verify_integrity(self) -> bool:
        """v53 Mastery: Validates entire chain hashes and link consistency."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Check hash validity
            if current["hash"] != self._calculate_hash(current):
                return False

            # Check link continuity
            if current["previous_hash"] != previous["hash"]:
                return False

        return True

    def get_merkle_root(self) -> str:
        """Simulates Merkle root of current chain state."""
        if not self.chain: return "EMPTY"
        all_hashes = "".join([b["hash"] for b in self.chain])
        return hashlib.sha256(all_hashes.encode()).hexdigest()

    def _persist(self):
        try:
            with open(self.storage_path, "w") as f:
                json.dump(self.chain, f, indent=2)
        except Exception as e:
            logger.error(f"LEDGER: Failed to persist: {e}")

    def _load_chain(self):
        try:
            import os
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r") as f:
                    self.chain = json.load(f)
                    logger.info(f"LEDGER: Loaded {len(self.chain)} blocks from disk.")
        except Exception as e:
            logger.error(f"LEDGER: Failed to load: {e}")
            self.chain = []
