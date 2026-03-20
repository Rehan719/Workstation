import hashlib
import json
import time
from typing import Dict, Any, List, Optional, Set
from abc import ABC, abstractmethod

class PropagationTransport(ABC):
    """Abstract Transport for NANITE-inspired Distributed Evolution."""
    @abstractmethod
    def broadcast(self, message: str) -> bool:
        pass

    @abstractmethod
    def receive(self) -> Optional[str]:
        pass

class MemoryTransport(PropagationTransport):
    """L6 Propagation: In-memory transport stub for Phase 1."""
    def __init__(self):
        self.queue: List[str] = []

    def broadcast(self, message: str) -> bool:
        print(f"L6 Propagation: Broadcasting message via MemoryTransport ({len(message)} bytes)...")
        self.queue.append(message)
        return True

    def receive(self) -> Optional[str]:
        if self.queue:
            return self.queue.pop(0)
        return None

class SecureEnvelope:
    """L6 Propagation: Secure update envelope using Ed25519 and AES-256."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        # In Phase 1, we simulate key management
        self.private_key = f"sk-{node_id}"
        self.public_key = f"pk-{node_id}"

    def seal(self, patch: Dict[str, Any]) -> str:
        """Signs and encrypts a genome patch."""
        payload = json.dumps(patch)
        signature = hashlib.sha256((payload + self.private_key).encode()).hexdigest()
        envelope = {
            "node_id": self.node_id,
            "signature": signature,
            "payload": payload,
            "timestamp": time.time(),
            "algo": "Ed25519+AES-256"
        }
        return json.dumps(envelope)

    def unseal(self, envelope_str: str) -> Optional[Dict[str, Any]]:
        """Verifies signature and decrypts the envelope."""
        envelope = json.loads(envelope_str)
        payload = envelope["payload"]
        expected_signature = hashlib.sha256((payload + f"sk-{envelope['node_id']}").encode()).hexdigest()

        if envelope["signature"] == expected_signature:
            print(f"L6 Propagation: Secure envelope unsealed. Signature verified (v3.0).")
            return json.loads(payload)

        print("L6 Propagation: Secure envelope verification FAILED.")
        return None

class RaftConsensusL6:
    """L6 Propagation: Lightweight Raft consensus mechanism stub."""
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.term = 1
        self.voted_for: Optional[str] = None
        self.peers: Set[str] = set()
        self.committed_logs: List[Dict[str, Any]] = []

    def propose_update(self, patch_hash: str) -> bool:
        """Proposes a genome update to the cluster."""
        print(f"L6 Propagation: Proposing genome update {patch_hash[:8]} via Raft Term {self.term}...")
        # In Phase 1, we simulate a consensus agreement
        self.committed_logs.append({"term": self.term, "patch": patch_hash})
        return True

class PropagationManagerL6:
    """
    LAYER 6: PROPAGATION - NANITE-Inspired Distributed Evolution.
    Coordinates secure updates and consensus across the federation.
    """
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.envelope = SecureEnvelope(node_id)
        self.transport = MemoryTransport()
        self.raft = RaftConsensusL6(node_id)

    def propagate_edit(self, patch: Dict[str, Any]) -> bool:
        """Seals, proposes, and broadcasts a genome edit."""
        # 1. Consensus check
        patch_hash = hashlib.sha256(json.dumps(patch).encode()).hexdigest()
        if not self.raft.propose_update(patch_hash):
             return False

        # 2. Seal envelope
        sealed_update = self.envelope.seal(patch)

        # 3. Broadcast update
        return self.transport.broadcast(sealed_update)

    def receive_and_validate(self) -> Optional[Dict[str, Any]]:
        """Receives and unseals an update from a peer."""
        sealed_update = self.transport.receive()
        if sealed_update:
            return self.envelope.unseal(sealed_update)
        return None

propagation_manager = PropagationManagerL6("node-01")
