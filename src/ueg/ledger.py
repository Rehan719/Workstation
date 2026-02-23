import os
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
import networkx as nx
from datetime import datetime, timezone

class BlockchainLedger:
    """
    Article BA: Blockchain-inspired provenance ledger (v53 Persistent).
    Full block chaining with SHA-256 and Merkle roots, now with JSON persistence.
    """
    def __init__(self, persistence_path: str = "meta/ledger.json"):
        self.persistence_path = persistence_path
        self.blocks = []
        self.current_transactions = []
        self._load()
        if not self.blocks:
            self._create_genesis_block()

    def _load(self):
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, 'r') as f:
                    self.blocks = json.load(f)
            except Exception:
                self.blocks = []

    def _save(self):
        os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
        with open(self.persistence_path, 'w') as f:
            json.dump(self.blocks, f, indent=2)

    def _create_genesis_block(self):
        self.add_block(previous_hash='0', proof=100)

    def add_transaction(self, sender: str, action: str, data: Any) -> int:
        transaction = {
            'sender': sender,
            'action': action,
            'data': data,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        data_str = json.dumps(data, sort_keys=True)
        transaction['signature'] = hashlib.sha256(f"{sender}:{data_str}".encode()).hexdigest()
        self.current_transactions.append(transaction)
        return len(self.blocks) + 1

    def _calculate_merkle_root(self, transactions: List[Dict[str, Any]]) -> str:
        if not transactions: return hashlib.sha256(b"empty").hexdigest()
        hashes = [hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest() for tx in transactions]
        while len(hashes) > 1:
            if len(hashes) % 2 != 0: hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = hashes[i] + hashes[i+1]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            hashes = new_hashes
        return hashes[0]

    def add_block(self, proof: int, previous_hash: Optional[str] = None) -> Dict[str, Any]:
        block = {
            'index': len(self.blocks) + 1,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'transactions': self.current_transactions,
            'merkle_root': self._calculate_merkle_root(self.current_transactions),
            'proof': proof,
            'previous_hash': previous_hash or (self.hash(self.blocks[-1]) if self.blocks else '0'),
        }
        self.current_transactions = []
        self.blocks.append(block)
        self._save()
        return block

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class UnifiedEvidenceGraph:
    """
    v53 Production: Persistent Unified Evidence Graph (UEG).
    Integrates formal proofs and blockchain provenance with disk storage.
    """
    def __init__(self, persistence_path: str = "meta/ueg_graph.json"):
        self.persistence_path = persistence_path
        self.graph = nx.DiGraph()
        self.ledger = BlockchainLedger()
        self._load()

    def _load(self):
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, 'r') as f:
                    data = json.load(f)
                    for node in data.get('nodes', []):
                        self.graph.add_node(node['id'], **node['metadata'])
                    for edge in data.get('edges', []):
                        self.graph.add_edge(edge['source'], edge['target'], **edge['metadata'])
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
        data = {
            'nodes': [{'id': n, 'metadata': d} for n, d in self.graph.nodes(data=True)],
            'edges': [{'source': u, 'target': v, 'metadata': d} for u, v, d in self.graph.edges(data=True)]
        }
        with open(self.persistence_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_node(self, node_id: str, node_type: str, metadata: Optional[Dict[str, Any]] = None):
        metadata = metadata or {}
        metadata['type'] = node_type
        self.graph.add_node(node_id, **metadata)
        self.ledger.add_transaction('system', 'ADD_NODE', {'id': node_id, 'metadata': metadata})
        self._save()

    def add_edge(self, source_id: str, target_id: str, relation: str, metadata: Optional[Dict[str, Any]] = None):
        metadata = metadata or {}
        metadata['relation'] = relation
        self.graph.add_edge(source_id, target_id, **metadata)
        self.ledger.add_transaction('system', 'ADD_EDGE', {'source': source_id, 'target': target_id, 'metadata': metadata})
        self._save()

    def validated_by(self, claim_id: str, validator_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.add_edge(claim_id, validator_id, 'VALIDATED_BY', metadata)

    def supports(self, evidence_id: str, claim_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.add_edge(evidence_id, claim_id, 'SUPPORTS', metadata)

    def contradicts(self, evidence_id: str, claim_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.add_edge(evidence_id, claim_id, 'CONTRADICTS', metadata)

    def derived_from(self, child_id: str, parent_id: str, metadata: Optional[Dict[str, Any]] = None):
        self.add_edge(child_id, parent_id, 'DERIVED_FROM', metadata)

    def commit(self):
        self.ledger.add_block(proof=123)

    def get_edges(self):
        return self.graph.edges(data=True)

    def get_nodes(self):
        return self.graph.nodes(data=True)
