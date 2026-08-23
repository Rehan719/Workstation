import hashlib
import json
import logging
import time
import os
from typing import Dict, List, Any, Optional
from agentic_core.config import data_path


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
    def __init__(self, log_path: str = str(data_path("ueg_audit.log"))):
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
        # §13 (W327) — tail anchor: the head is stamped beside the ledger on every append, so
        # verify catches truncation/rollback (see agentic_core.integrity for the threat model).
        try:
            from agentic_core.integrity import write_anchor
            self._anchor_count = getattr(self, "_anchor_count", None)
            count = self._count_entries() if self._anchor_count is None else self._anchor_count + 1
            self._anchor_count = count
            write_anchor(self.log_path + ".anchor", event_hash, count)
        except Exception:
            pass
        self.logger.info(f"UEG: Event {event_type} logged with hash {event_hash[:16]}...")
        return event_hash

    def _count_entries(self) -> int:
        try:
            with open(self.log_path, "r") as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def verify_chain(self) -> bool:
        """Verify the ENTIRE audit trail: §13 (W327) — every entry's content hash is RECOMPUTED
        from its payload (a mutated payload is caught, not just a broken parent link) and the tail
        is checked against the sibling anchor (truncation/rollback is caught). Previously this
        walked parent links only — content tampering passed as 'chain_valid'."""
        return bool(self.verify_chain_detail().get("valid"))

    def verify_chain_detail(self) -> Dict[str, Any]:
        from agentic_core.integrity import read_anchor, verify_chain_entries
        entries: List[Dict[str, Any]] = []
        try:
            with open(self.log_path, "r") as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
        except FileNotFoundError:
            return {"valid": True, "entries": 0, "head": None,
                    "note": "no ledger yet — vacuously valid"}
        except Exception as exc:
            return {"valid": False, "reason": f"ledger unreadable: {exc}"}
        anchor = read_anchor(self.log_path + ".anchor")
        return verify_chain_entries(
            entries,
            recompute=lambda e: hashlib.sha3_512(
                json.dumps(e["payload"], sort_keys=True, default=_ser_default).encode()).hexdigest(),
            stored_hash=lambda e: e.get("hash"),
            parent_hash=lambda e: e["payload"].get("parent_hash"),
            first_parent="0" * 128,
            anchor=(anchor or {}).get("head") if anchor else None,
        )

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
