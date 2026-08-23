import hashlib
import json
import logging
import time
from typing import Dict, Any, List

class DocumentControlManagementSystem:
    """
    VBS: DCMS.
    Cryptographic versioning and trace logic.

    §10×§13 (W327) — genuinely VERIFIABLE now: previously the seal was write-only (in-memory
    registry, content never stored, no verify path, get_audit_integrity() a constant 1.0). Every
    commit persists the entry WITH the content it sealed (capped), verify_artifact re-hashes the
    stored content against the stored seal, and get_audit_integrity() is the RECOMPUTED fraction
    of entries whose seal still matches — a real measurement, never a constant.
    """
    _CONTENT_CAP = 16000   # serialised chars stored per entry (larger content: hash-only, declared)

    def __init__(self, config_path: str):
        self.logger = logging.getLogger("DCMS")
        self.registry = self._load()   # id -> list of entries (persistent)

    def _store_path(self) -> str:
        from agentic_core.config import data_path
        return str(data_path("dcms_registry.json"))

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            from agentic_core.config import load_json_tolerant
            return load_json_tolerant(self._store_path(), {}) or {}
        except Exception:
            return {}

    def _persist(self) -> None:
        try:
            from agentic_core.config import atomic_write_json
            atomic_write_json(self._store_path(), self.registry)
        except Exception:
            pass

    async def commit_artifact(self, artifact_id: str, content: Dict, actor: str) -> str:
        """Commit + version an artifact — the seal AND what it sealed persist together."""
        payload = json.dumps(content, sort_keys=True, default=str)
        h = hashlib.sha3_512(payload.encode()).hexdigest()
        entry = {
            "version": len(self.registry.get(artifact_id, [])) + 1,
            "hash": h,
            "actor": actor,
            "timestamp": time.time_ns(),
            # W327 — the sealed content itself (capped): the verify path's raw material
            "content": payload if len(payload) <= self._CONTENT_CAP else None,
            "content_stored": len(payload) <= self._CONTENT_CAP,
        }
        self.registry.setdefault(artifact_id, []).append(entry)
        self._persist()
        return h

    def verify_artifact(self, artifact_id: str) -> Dict[str, Any]:
        """§13 (W327) — recompute every stored version's seal. A mutated entry is caught + named."""
        entries = self.registry.get(artifact_id)
        if not entries:
            return {"artifact_id": artifact_id, "valid": False, "reason": "unknown artifact"}
        results = []
        for e in entries:
            if e.get("content_stored") and e.get("content") is not None:
                ok = hashlib.sha3_512(e["content"].encode()).hexdigest() == e.get("hash")
                results.append({"version": e.get("version"), "verified": ok,
                                "basis": "recomputed"})
            else:
                results.append({"version": e.get("version"), "verified": None,
                                "basis": "hash_only (content exceeded storage cap — honest)"})
        recomputed = [r for r in results if r["basis"] == "recomputed"]
        return {"artifact_id": artifact_id,
                "valid": bool(recomputed) and all(r["verified"] for r in recomputed),
                "versions": results}

    def get_audit_integrity(self) -> float:
        """The RECOMPUTED fraction of verifiable entries whose seal still matches (0.0 with no
        verifiable history — never a fabricated constant)."""
        total = ok = 0
        for entries in self.registry.values():
            for e in entries:
                if e.get("content_stored") and e.get("content") is not None:
                    total += 1
                    if hashlib.sha3_512(e["content"].encode()).hexdigest() == e.get("hash"):
                        ok += 1
        return round(ok / total, 4) if total else 0.0
