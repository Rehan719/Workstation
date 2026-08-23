"""
Unified Event Graph (UEG) Logger — GaaS v5.

A tamper-evident, append-only event log. Each constitutional event is chained to
its predecessor with a SHA3-512 hash, so the entire governance history forms a
verifiable Merkle-DAG: altering any past event invalidates every hash after it.

Used by the v16-Omega interceptor and the self-tuning circuit breaker to record
gates, halts, executions, failures and checkpoints.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("gaas.v5.ueg")

# WORKSTATION_UEG_PATH overrides the audit-ledger location. A tamper-evident chain must never be
# shared between the live platform and ephemeral test/CI runs (concurrent appenders from separate
# processes each hold only an in-process lock, so they corrupt each other's chain) — point tests and
# isolated deployments at their own ledger. Defaults to meta/gaas_v5_ueg.json so existing setups are
# unchanged.
_DEFAULT_PATH = os.environ.get("WORKSTATION_UEG_PATH") or os.path.join("meta", "gaas_v5_ueg.json")


class UEGLogger:
    """Append-only, SHA3-512 hash-chained constitutional event log."""

    def __init__(self, storage_path: str = _DEFAULT_PATH):
        self.storage_path = storage_path
        self._lock = threading.Lock()
        self._initialise()

    # ── storage ───────────────────────────────────────────────────────────
    def _initialise(self) -> None:
        directory = os.path.dirname(self.storage_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.storage_path):
            self._write({"nodes": [], "root_hash": None})

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return {"nodes": [], "root_hash": None}

    def _write(self, graph: Dict[str, Any]) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2)

    @staticmethod
    def _hash(node_base: Dict[str, Any]) -> str:
        content = json.dumps(node_base, sort_keys=True).encode("utf-8")
        return hashlib.sha3_512(content).hexdigest()

    # ── append ────────────────────────────────────────────────────────────
    def log(self, event_data: Dict[str, Any]) -> str:
        """Append an event, chaining it to the current root hash. Returns the new hash."""
        with self._lock:
            graph = self._read()
            base = {
                "id": f"event_{len(graph['nodes'])}",
                "timestamp": time.time(),
                "data": event_data,
                "previous_hash": graph.get("root_hash"),
            }
            node = dict(base)
            node["hash"] = self._hash(base)
            graph["nodes"].append(node)
            graph["root_hash"] = node["hash"]
            self._write(graph)
            # §13 (W327) — tail anchor beside the graph: root_hash lives INSIDE the same file, so
            # a rollback that rewrites both stayed consistent; the sibling anchor catches it.
            try:
                from agentic_core.integrity import write_anchor
                write_anchor(self.storage_path + ".anchor", node["hash"], len(graph["nodes"]))
            except Exception:
                pass
        logger.debug("UEG event %s logged (%s…)", node["id"], node["hash"][:16])
        return node["hash"]

    # ── convenience wrappers (compat with the v3 product suite API) ─────────
    def log_constitutional_event(self, event_data: Dict[str, Any]) -> str:
        return self.log(event_data)

    def log_policy_halt(self, node_id: str, action_type: str, reason: str) -> str:
        return self.log({"type": "policy_gate_halt", "node": node_id,
                         "action": action_type, "reason": reason})

    def log_minimisation_event(self, event_type: str, data: Dict[str, Any]) -> str:
        return self.log({"type": event_type, **data})

    def log_circuit_breaker_trip(self, domain: str, reason: str, state: Dict[str, Any]) -> str:
        return self.log({"type": "circuit_breaker_trip", "domain": domain,
                         "reason": reason, "state_at_trip": state})

    def log_cross_domain_transfer(self, source: str, target: str, pattern_id: str,
                                  attestation: Optional[Dict[str, Any]] = None) -> str:
        return self.log({"type": "cross_domain_transfer", "source": source,
                         "target": target, "pattern_id": pattern_id,
                         "sovereignty_attestation": attestation or {}})

    # ── read / verify ───────────────────────────────────────────────────────
    def recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._read()["nodes"][-limit:]

    def summary(self) -> Dict[str, Any]:
        graph = self._read()
        nodes = graph["nodes"]
        by_type: Dict[str, int] = {}
        for n in nodes:
            t = n.get("data", {}).get("type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1
        return {
            "total_events": len(nodes),
            "root_hash": graph.get("root_hash"),
            "by_type": by_type,
        }

    def verify_chain(self) -> Dict[str, Any]:
        """Recompute every hash and confirm the chain has not been tampered with."""
        graph = self._read()
        prev: Optional[str] = None
        for node in graph["nodes"]:
            base = {
                "id": node["id"],
                "timestamp": node["timestamp"],
                "data": node["data"],
                "previous_hash": prev,
            }
            if self._hash(base) != node.get("hash"):
                return {"valid": False, "broken_at": node["id"]}
            prev = node["hash"]
        # §13 (W327) — the tail anchor catches truncation/rollback (both graph AND its internal
        # root_hash can be rewritten consistently; the sibling anchor cannot be forgotten silently).
        try:
            from agentic_core.integrity import read_anchor
            anchor = read_anchor(self.storage_path + ".anchor")
            if anchor and anchor.get("head") != prev:
                return {"valid": False, "reason": "tail_anchor_mismatch (truncation/rollback suspected)",
                        "events": len(graph["nodes"]), "anchored_head": anchor.get("head")}
        except Exception:
            pass
        return {"valid": True, "events": len(graph["nodes"]), "root_hash": graph.get("root_hash")}
