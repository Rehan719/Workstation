import hashlib
import time
import json
import logging
import os
from typing import Dict, List, Any, Optional

class VSBUEGLogger:
    """
    Unified Event Graph (UEG) Logger with SHA-3-512 Merkle-DAG chaining.
    """
    def __init__(self, log_path: str = "ueg_audit.log"):
        self.logger = logging.getLogger("VSBUEGLogger")
        self.log_path = log_path
        self.last_hash = self._get_last_hash()

    def _get_last_hash(self) -> str:
        if not os.path.exists(self.log_path):
            return "0" * 128

        try:
            with open(self.log_path, "rb") as f:
                f.seek(0, os.SEEK_END)
                if f.tell() == 0:
                    return "0" * 128

                # Read last line
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
                    if f.tell() == 0:
                        break
                last_line = f.readline().decode()
                if last_line:
                    entry = json.loads(last_line)
                    return entry["hash"]
        except (IOError, json.JSONDecodeError, UnicodeDecodeError):
            self.logger.warning("Failed to parse last log line for parent hash.")
        return "0" * 128

    async def initialize(self):
        self.logger.info("VSBUEGLogger initialized.")

    def log_event(self, event_type: str, data: Dict[str, Any], actor: str = "SYSTEM") -> str:
        """
        Logs an event and returns its cryptographic hash.
        """
        timestamp = time.time_ns()

        payload = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data,
            "actor": actor,
            "parent_hash": self.last_hash
        }

        event_str = json.dumps(payload, sort_keys=True)
        event_hash = hashlib.sha3_512(event_str.encode()).hexdigest()

        log_entry = {
            "hash": event_hash,
            "payload": payload
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        self.last_hash = event_hash
        return event_hash

    def verify_chain(self) -> bool:
        """
        Verifies the integrity of the Merkle-DAG chain.
        """
        current_expected_parent = "0" * 128
        try:
            if not os.path.exists(self.log_path):
                return True
            with open(self.log_path, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    entry = json.loads(line)
                    actual_hash = entry["hash"]
                    payload = entry["payload"]

                    if payload["parent_hash"] != current_expected_parent:
                        self.logger.error(f"Chain broken. Expected parent {current_expected_parent[:16]}, got {payload['parent_hash'][:16]}")
                        return False

                    recomputed_hash = hashlib.sha3_512(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                    if recomputed_hash != actual_hash:
                        self.logger.error(f"Hash mismatch at {actual_hash[:16]}.")
                        return False

                    current_expected_parent = actual_hash
            return True
        except (IOError, json.JSONDecodeError) as e:
            self.logger.error(f"Verification error: {e}")
            return False
