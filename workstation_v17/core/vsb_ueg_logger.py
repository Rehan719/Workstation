"""VSB UEG Logger - v17.0 implementation."""
import hashlib
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger("VSB-UEG")

class VSBUEGLogger:
    def __init__(self, storage_path: str = "/tmp/ueg_v17", ipfs_gateway: str = None):
        self.storage_path = storage_path
        self.ipfs_gateway = ipfs_gateway
        os.makedirs(storage_path, exist_ok=True)
        self.chain_file = os.path.join(storage_path, "ueg_merkle_dag.json")
        self.chain = self._load_chain()

    def _load_chain(self):
        if os.path.exists(self.chain_file):
            with open(self.chain_file, 'r') as f:
                return json.load(f)
        return []

    async def initialize(self):
        """Create v17.0 Genesis Block."""
        if not self.chain:
            genesis = {
                "index": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "event": "genesis",
                "data": {"arch": "IDBO-v17"},
                "prev_hash": "0",
                "hash": hashlib.sha3_512(b"genesis_v17").hexdigest()
            }
            self.chain.append(genesis)
            self._save_chain()
            logger.info("VSB initialized with Genesis Block (SHA-3-512).")

    async def log_event(self, event_type: str, data: dict) -> str:
        """v17.0: Append to Merkle-DAG."""
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
        logger.warning("VSB Rollback triggered.")
        self.chain = self.chain[:-1]
        self._save_chain()

    def _save_chain(self):
        with open(self.chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
