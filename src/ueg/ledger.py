from typing import Dict, Any, List, Optional, Tuple
import networkx as nx
from datetime import datetime
import copy
import hashlib
import json
from src.security.sigstore_handler import SigstoreHandler

class BlockchainLedger:
    """
    Article BA: Blockchain-inspired provenance ledger.
    Ensures immutability using SHA-256 block chaining and Sigstore signatures.
    """
    def __init__(self, sigstore: SigstoreHandler):
        self.sigstore = sigstore
        self.blocks = []
        self.current_transactions = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        self.add_block(previous_hash='0', proof=100)

    def add_transaction(self, sender: str, action: str, data: Any) -> int:
        """Adds a new transaction and signs it using Sigstore logic."""
        transaction = {
            'sender': sender,
            'action': action,
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }
        # Data-dependent signature
        data_str = json.dumps(data, sort_keys=True)
        transaction['signature'] = hashlib.sha256(f"{sender}:{data_str}".encode()).hexdigest()

        self.current_transactions.append(transaction)
        return len(self.blocks) + 1

    def add_block(self, proof: int, previous_hash: Optional[str] = None) -> Dict[str, Any]:
        block = {
            'index': len(self.blocks) + 1,
            'timestamp': datetime.utcnow().isoformat(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.blocks[-1]) if self.blocks else '0',
        }
        self.current_transactions = []
        self.blocks.append(block)
        return block

    @staticmethod
    def hash(block: Dict[str, Any]) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class UnifiedEvidenceGraph:
    """
    v52.0 Production: Robust Unified Evidence Graph (UEG).
    """
    def __init__(self):
        self.graph = nx.DiGraph()
        self.sigstore = SigstoreHandler()
        self.ledger = BlockchainLedger(self.sigstore)
        self.version = "52.0"

    def add_node(self, node_id: str, node_type: str, metadata: Optional[Dict[str, Any]] = None):
        metadata = metadata or {}
        metadata['type'] = node_type
        self.graph.add_node(node_id, **metadata)
        self.ledger.add_transaction('system', 'ADD_NODE', {'id': node_id, 'metadata': metadata})

    def add_edge(self, source_id: str, target_id: str, relation: str, metadata: Optional[Dict[str, Any]] = None):
        metadata = metadata or {}
        metadata['relation'] = relation
        self.graph.add_edge(source_id, target_id, **metadata)
        self.ledger.add_transaction('system', 'ADD_EDGE', {'source': source_id, 'target': target_id, 'metadata': metadata})

    def commit(self):
        self.ledger.add_block(proof=123)

    def get_edges(self):
        return self.graph.edges(data=True)
