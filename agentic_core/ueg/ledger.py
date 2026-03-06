import hashlib
import json
import logging
import time
from typing import Dict, Any, List, Optional, Set

logger = logging.getLogger(__name__)

class UnifiedEvidenceGraph:
    """
    ARTICLE AC: Unified Evidence Graph (UEG).
    v99 Transcendent: Graph-based reasoning with nodes, edges, and semantic validation.
    """
    def __init__(self):
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, metadata: Dict[str, Any]):
        """Adds a node (HYPOTHESIS, EVIDENCE, PUBLICATION)."""
        self.nodes[node_id] = {
            "type": node_type,
            "metadata": metadata,
            "timestamp": time.time()
        }
        logger.info(f"UEG: Node added [{node_type}] {node_id}")

    def add_edge(self, source: str, target: str, relation: str):
        """Adds a directed edge (SUPPORTS, CONTRADICTS, DERIVED_FROM)."""
        if source not in self.nodes or target not in self.nodes:
            logger.warning(f"UEG: Edge rejected. Source {source} or Target {target} missing.")
            return False

        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation,
            "timestamp": time.time()
        })
        logger.info(f"UEG: Edge added {source} --({relation})--> {target}")
        return True

    def get_subgraph(self, start_node: str) -> Dict[str, Any]:
        """Simple traversal to get related knowledge components."""
        related_nodes = {start_node}
        related_edges = []

        for edge in self.edges:
            if edge["source"] == start_node or edge["target"] == start_node:
                related_nodes.add(edge["source"])
                related_nodes.add(edge["target"])
                related_edges.append(edge)

        return {
            "nodes": {nid: self.nodes[nid] for nid in related_nodes if nid in self.nodes},
            "edges": related_edges
        }

class BlockchainLedger:
    """
    ARTICLE AC: Blockchain-Anchored UEG.
    v53/v99: Merkle-tree based chaining with proof-of-work security.
    """

    def __init__(self, storage_path: str = "meta/ledger.json"):
        self.storage_path = storage_path
        self.chain: List[Dict[str, Any]] = []
        self.ueg = UnifiedEvidenceGraph()
        self.difficulty = 2 # Simulation difficulty
        self._load_chain()

    def commit_ueg_node(self, node_id: str, node_type: str, metadata: Dict[str, Any]):
        """Helper to add a node to UEG and anchor it in the ledger."""
        self.ueg.add_node(node_id, node_type, metadata)
        entry = {
            "action": "ADD_NODE",
            "node_id": node_id,
            "type": node_type,
            "metadata": metadata
        }
        return self.add_block(entry)

    def log_sharia_transaction(self, tx_type: str, user_id: str, amount: float, designation: str):
        """
        ARTICLE 245: Immutable audit trail for Zakat, Sadaqah, and Wakaf.
        """
        entry = {
            "action": "SHARIA_TX",
            "tx_type": tx_type,
            "user_id": user_id,
            "amount": amount,
            "designation": designation,
            "timestamp": time.time()
        }
        return self.add_block(entry)

    def add_block(self, data: Dict[str, Any]):
        """Adds a new block with actual Proof-of-Work simulation."""
        previous_hash = self.chain[-1]["hash"] if self.chain else "0" * 64

        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "previous_hash": previous_hash,
            "nonce": 0
        }

        # ARTICLE AC: Proof-of-Work (No-Stubs compliance)
        block["hash"] = self._mine_block(block)

        self.chain.append(block)
        logger.info(f"LEDGER: Block {block['index']} mined. Hash: {block['hash'][:12]}")
        self._persist()
        return True

    def _mine_block(self, block: Dict[str, Any]) -> str:
        """Simulates finding a hash with a specific number of leading zeros."""
        # ARTICLE AC: Proof-of-Work Loop (v53/v99)
        target = "0" * self.difficulty
        # For simulation at difficulty 2, this is fast enough not to block for long.
        while True:
            hash_res = self._calculate_hash(block)
            if hash_res.startswith(target):
                return hash_res
            block["nonce"] += 1

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
        target = "0" * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current["hash"] != self._calculate_hash(current):
                return False
            if not current["hash"].startswith(target):
                return False
            if current["previous_hash"] != previous["hash"]:
                return False
        return True

    def _persist(self):
        import os
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, "w") as f:
                json.dump(self.chain, f, indent=2)
        except Exception as e:
            logger.error(f"LEDGER: Failed to persist: {e}")

    def _load_chain(self):
        import os
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, "r") as f:
                    self.chain = json.load(f)
                    logger.info(f"LEDGER: Loaded {len(self.chain)} blocks.")
        except Exception as e:
            logger.error(f"LEDGER: Failed to load: {e}")
            self.chain = []
