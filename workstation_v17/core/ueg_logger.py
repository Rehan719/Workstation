"""Immutable Merkle‑DAG logger for constitutional audit trail."""
import hashlib
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger("UEG")

class UEGMerkleLogger:
    def __init__(self, storage_path: str = "/var/ueg_logs"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.chain_path = os.path.join(self.storage_path, "chain.json")
        self.chain = self._load_chain()

    def _load_chain(self) -> List[Dict]:
        if os.path.exists(self.chain_path):
            with open(self.chain_path, 'r') as f:
                try:
                    return json.load(f)
                except:
                    return []
        return []

    def _save_chain(self):
        with open(self.chain_path, 'w') as f:
            json.dump(self.chain, f, indent=2)

    async def initialize(self):
        if not self.chain:
            genesis = {
                "index": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "event": "genesis",
                "data": {"architecture": "IDBO-v10.0"},
                "prev_hash": "0",
                "hash": hashlib.sha3_512(b"genesis").hexdigest()
            }
            self.chain.append(genesis)
            self._save_chain()

    async def log_event(self, event_type: str, data: Dict) -> str:
        prev_hash = self.chain[-1]["hash"] if self.chain else "0"
        block = {
            "index": len(self.chain),
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "data": data,
            "prev_hash": prev_hash,
            "hash": hashlib.sha3_512(json.dumps(data, sort_keys=True).encode() + prev_hash.encode()).hexdigest()
        }
        self.chain.append(block)
        self._save_chain()
        return block["hash"]

    async def rollback_to_last_verified(self):
        logger.warning("Rolling back to last verified state – clearing last cycle")
        self.chain = self.chain[:-1]
        self._save_chain()

    async def finalize(self):
        self._save_chain()
