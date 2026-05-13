import hashlib
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from agentic_core.ueg.logger import VSBUEGLogger

class CrossInstanceUEGLedger:
    """
    Extends UEG Merkle-DAG to support cross-instance consensus and fork detection.
    Constraint 10: Trillion-Token Provenance.
    """
    def __init__(self, instance_id: str, peers: List[str], ueg_logger: Optional[VSBUEGLogger] = None):
        self.instance_id = instance_id
        self.peers = peers
        self.ueg = ueg_logger or VSBUEGLogger()
        self.local_chain = [] # List of Merkle roots
        self.cross_links = {} # root -> peer_signatures

    async def append_cross_instance(self, event_data: Dict[str, Any], peer_signatures: Dict[str, str]) -> str:
        """
        Append an event that requires cross-instance ratification.
        """
        n_peers = len(self.peers)
        quorum_target = (2 * n_peers // 3) + 1

        if len(peer_signatures) < quorum_target:
             raise PermissionError(f"Insufficient quorum for cross-instance append: {len(peer_signatures)}/{quorum_target}")

        event_hash = hashlib.sha3_512(str(event_data).encode()).hexdigest()

        # Log to local UEG
        await self.ueg.log_minimisation_event("cross_instance_append", {
            "instance": self.instance_id,
            "event_hash": event_hash,
            "quorum_size": len(peer_signatures)
        })

        self.local_chain.append(event_hash)
        self.cross_links[event_hash] = peer_signatures
        return event_hash

    async def detect_forks(self, peer_roots: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Detects inconsistencies between local and peer Merkle roots.
        Fork detection target: <100ms.
        """
        start_time = asyncio.get_event_loop().time()
        forks = []

        local_root = self.local_chain[-1] if self.local_chain else "0"*128

        for peer_id, peer_root in peer_roots.items():
            if peer_root != local_root:
                forks.append({
                    "peer": peer_id,
                    "local_root": local_root,
                    "peer_root": peer_root,
                    "status": "FORK_DETECTED"
                })

        detection_latency_ms = (asyncio.get_event_loop().time() - start_time) * 1000

        if forks:
            await self.ueg.log_minimisation_event("fork_detected", {
                "count": len(forks),
                "latency_ms": detection_latency_ms
            })

        return forks
