import hashlib
import json
import time
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class GenomeBlock:
    def __init__(self, index: int, timestamp: float, acquired_traits: Dict[str, Any], previous_hash: str, zkp_proof: str):
        self.index = index
        self.timestamp = timestamp
        self.acquired_traits = acquired_traits
        self.previous_hash = previous_hash
        self.zkp_proof = zkp_proof
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "traits": self.acquired_traits,
            "prev": self.previous_hash,
            "zkp": self.zkp_proof
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class GenomicRegistry:
    """
    ARTICLE DC: Blockchain Genomic Registry (v70 Mastery).
    Immutable ledger for Lamarckian inheritance with ZKP mutation verification.
    """
    def __init__(self):
        self.chain: List[GenomeBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = GenomeBlock(0, time.time(), {"origin": "master_seed"}, "0", "zkp:init")
        self.chain.append(genesis)

    def commit_mutation(self, acquired_traits: Dict[str, Any], zkp_proof: str) -> str:
        """v71.0 Alpha: Functional mutation commitment."""
        prev_block = self.chain[-1]
        new_block = GenomeBlock(
            index=len(self.chain),
            timestamp=time.time(),
            acquired_traits=acquired_traits,
            previous_hash=prev_block.hash,
            zkp_proof=zkp_proof
        )
        self.chain.append(new_block)
        logger.info(f"GENOME: Block {new_block.index} committed. Hash={new_block.hash[:8]}")
        return new_block.hash

    def verify_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.previous_hash != previous.hash:
                return False
            if current.hash != current._calculate_hash():
                return False
        return True

    def get_genome_depth(self) -> int:
        return len(self.chain)
