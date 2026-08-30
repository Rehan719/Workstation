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
    """Append-only, SHA3-512 hash-chained constitutional event log.

    §13 (W351) — ONE instance per storage path: production constructed a fresh UEGLogger() per
    call, so each instance held its own threading.Lock and concurrent appenders clobbered the
    whole-file graph (the Round-10 audit measured 196/200 constitutional events silently lost
    while verify_chain reported the survivors 'valid'). __new__ returns the per-path singleton,
    and log() additionally holds the cross-process store_lock."""

    _instances: dict = {}
    _instances_guard = threading.Lock()

    def __new__(cls, storage_path: str = _DEFAULT_PATH):
        # W367 — initialisation happens HERE, under the same guard that hands out the singleton.
        # It used to live in __init__, which runs UNGUARDED: two threads constructing the logger
        # for a not-yet-existing path could both see `_initialised` False, so both ran
        # `_initialise()` — and `_initialise` writes an EMPTY graph. The second write could land
        # after the first thread had already logged an event, destroying it. That is a silent loss
        # from a tamper-evident ledger, and CI caught it as 119 of 120 concurrent events surviving.
        with cls._instances_guard:
            inst = cls._instances.get(storage_path)
            if inst is None:
                inst = super().__new__(cls)
                inst.storage_path = storage_path
                inst._lock = threading.Lock()
                inst._initialise()
                inst._initialised = True          # set LAST: a partially-built instance is never published
                cls._instances[storage_path] = inst
            return inst

    def __init__(self, storage_path: str = _DEFAULT_PATH):
        # Construction is complete before __new__ returns; __init__ is intentionally a no-op so a
        # second construction for the same path can never re-run initialisation.
        return

    # ── storage ───────────────────────────────────────────────────────────
    def _initialise(self) -> None:
        directory = os.path.dirname(self.storage_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(self.storage_path):
            # W367 — the exists→write window must be serialised across PROCESSES too: another
            # worker may create and append to the chain between the check and the write, and an
            # empty-graph write would erase its events. Re-check inside the lock.
            from agentic_core.config import store_lock
            try:
                with store_lock(self.storage_path):
                    if not os.path.exists(self.storage_path):
                        self._write({"nodes": [], "root_hash": None})
            except Exception:
                # never let lock contention stop construction — but only create when still absent
                if not os.path.exists(self.storage_path):
                    self._write({"nodes": [], "root_hash": None})

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return {"nodes": [], "root_hash": None}

    def _write(self, graph: Dict[str, Any]) -> None:
        # W351 — atomic: a torn whole-file write under contention wiped the chain
        from agentic_core.config import atomic_write_json
        atomic_write_json(self.storage_path, graph)

    @staticmethod
    def _hash(node_base: Dict[str, Any]) -> str:
        content = json.dumps(node_base, sort_keys=True).encode("utf-8")
        return hashlib.sha3_512(content).hexdigest()

    # ── append ────────────────────────────────────────────────────────────
    def log(self, event_data: Dict[str, Any]) -> str:
        """Append an event, chaining it to the current root hash. Returns the new hash.
        W351 — the in-process lock serialises threads; the cross-process store_lock serialises
        separate processes (the heartbeat + API workers write the same chain in production)."""
        from agentic_core.config import store_lock
        with self._lock, store_lock(self.storage_path):
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
            # W351 — MONOTONICITY: a clobbered graph with fewer nodes than the anchor ever
            # recorded is a silent wipe, not a valid chain (the audit saw 196 lost events
            # 'verify' as valid because the survivors chained cleanly).
            if anchor and int(anchor.get("count") or 0) > len(graph["nodes"]):
                return {"valid": False,
                        "reason": (f"node_count_below_anchor (anchor recorded "
                                   f"{anchor.get('count')}, graph holds {len(graph['nodes'])} — "
                                   "silent loss detected)"),
                        "events": len(graph["nodes"])}
        except Exception:
            pass
        return {"valid": True, "events": len(graph["nodes"]), "root_hash": graph.get("root_hash")}
