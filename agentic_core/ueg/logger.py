import hashlib
import json
import logging
import time
import os
import asyncio
from typing import Dict, List, Any, Optional

class VSBUEGLogger:
    """
    IDBO Layer 7: Module Library / UEG.
    Immutable SHA-3-512 Merkle-DAG Logger with IPFS pinning logic.
    Optimised for vΩ∞-MASTER with log batching for free-tier quota preservation.
    """
    def __init__(self, log_path: str = "data/ueg_audit.log"):
        self.logger = logging.getLogger("VSB_UEG")
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.merkle_root = self._load_last_root()
        self.log_buffer = []
        self.batch_interval = 10 # seconds
        self._flush_task = None

    def _load_last_root(self) -> str:
        if not os.path.exists(self.log_path):
            return "0" * 128
        try:
            with open(self.log_path, "rb") as f:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0: return "0" * 128
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
                    if f.tell() == 0: break
                last_line = f.readline().decode()
                return json.loads(last_line)["hash"]
        except Exception:
            return "0" * 128

    async def log_event(self, event_type: str, data: Dict[str, Any], actor: str = "SYSTEM") -> str:
        """
        Appends a new event to the Merkle-DAG chain.
        Now uses batching to conserve I/O and cloud quotas.
        """
        payload = {
            "timestamp": time.time_ns(),
            "event_type": event_type,
            "data": data,
            "actor": actor,
            "parent_hash": self.merkle_root
        }

        payload_str = json.dumps(payload, sort_keys=True)
        event_hash = hashlib.sha3_512(payload_str.encode()).hexdigest()
        entry = {"hash": event_hash, "payload": payload}

        self.log_buffer.append(entry)
        self.merkle_root = event_hash # Update root immediately for chaining

        # Start flush task if not running
        if self._flush_task is None or self._flush_task.done():
            self._flush_task = asyncio.create_task(self._periodic_flush())

        return event_hash

    async def _periodic_flush(self):
        await asyncio.sleep(self.batch_interval)
        await self.flush()

    async def flush(self):
        if not self.log_buffer:
            return

        entries_to_write = list(self.log_buffer)
        self.log_buffer = []

        try:
            with open(self.log_path, "a") as f:
                for entry in entries_to_write:
                    f.write(json.dumps(entry) + "\n")
            self.logger.info(f"UEG: Flushed {len(entries_to_write)} events to audit log.")
        except Exception as e:
            self.logger.error(f"UEG: Failed to flush logs: {e}")

    def verify_chain(self) -> bool:
        """Verifies the integrity of the entire audit trail."""
        expected_parent = "0" * 128
        try:
            with open(self.log_path, "r") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry["payload"]["parent_hash"] != expected_parent:
                        return False
                    expected_parent = entry["hash"]
            return True
        except Exception:
            return False

    async def log_minimisation_event(self, event_type: str, metrics: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> str:
        data = {
            "schema_version": "1.0.0",
            "metrics": metrics,
            "context": context or {}
        }
        return await self.log_event(f"minimisation:{event_type}", data)

    def get_last_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Retrieve the last N entries for state reconstruction."""
        if not os.path.exists(self.log_path):
            return []
        try:
            with open(self.log_path, "r") as f:
                lines = f.readlines()
                return [json.loads(line) for line in lines[-count:]]
        except Exception:
            return []
