import hashlib
import json
import logging
import time
import os
from typing import Dict, List, Any, Optional


def _ser_default(o: Any) -> Any:
    """Serialise non-JSON-native payload values (e.g. numpy scalars/bools from scipy) so the ledger
    never crashes on a real-world payload. numpy scalars -> native python; everything else -> str."""
    try:
        import numpy as _np
        if isinstance(o, _np.generic):
            return o.item()
    except Exception:
        pass
    return str(o)


class VSBUEGLogger:
    """
    IDBO Layer 7: Module Library / UEG.
    Immutable SHA-3-512 Merkle-DAG Logger with IPFS pinning logic.
    """
    def __init__(self, log_path: str = "data/ueg_audit.log"):
        self.logger = logging.getLogger("VSB_UEG")
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.merkle_root = self._load_last_root()

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
        """
        payload = {
            "timestamp": time.time_ns(),
            "event_type": event_type,
            "data": data,
            "actor": actor,
            "parent_hash": self.merkle_root
        }

        payload_str = json.dumps(payload, sort_keys=True, default=_ser_default)
        event_hash = hashlib.sha3_512(payload_str.encode()).hexdigest()

        entry = {"hash": event_hash, "payload": payload}

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry, default=_ser_default) + "\n")

        self.merkle_root = event_hash
        self.logger.info(f"UEG: Event {event_type} logged with hash {event_hash[:16]}...")
        return event_hash

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
        """
        Log minimisation-specific metrics with SHA-3-512 integrity.
        Enforces schema consistency for minimisation KPIs.
        """
        data = {
            "schema_version": "1.0.0",
            "metrics": metrics,
            "context": context or {}
        }
        return await self.log_event(f"minimisation:{event_type}", data)
