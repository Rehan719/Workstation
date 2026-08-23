"""
§10×§13 (W327) — ONE recompute-and-verify core for every hash chain on the platform.

The Round-7 audit proved the previous "tamper-evident" claims were not: verify paths walked
parent LINKS without ever recomputing content hashes (mutation passed), and every ledger accepted
tail truncation/rollback undetected. This module is the single honest verifier:

- ``verify_chain_entries`` recomputes EVERY entry's content hash and checks the parent linkage;
  a mutated payload or a re-linked chain is caught and named (index + reason).
- Tail anchoring: each ledger stamps its current head into a sibling anchor file on every append;
  verify compares. HONEST THREAT MODEL: the anchor lives on the same filesystem, so it defeats
  accidental truncation and unsophisticated rollback — an attacker with full file access who
  updates chain AND anchor consistently is out of scope (a remote/WORM anchor is the upgrade path,
  Owner-gated like all external services).
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Callable, Dict, List, Optional


def sha3_512_of(payload: Any, default: Callable[[Any], Any] = str) -> str:
    return hashlib.sha3_512(
        json.dumps(payload, sort_keys=True, default=default).encode()).hexdigest()


def sha256_of(payload: Any, default: Callable[[Any], Any] = str) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=default).encode()).hexdigest()


def verify_chain_entries(entries: List[Any], *,
                         recompute: Callable[[Any], str],
                         stored_hash: Callable[[Any], Optional[str]],
                         parent_hash: Callable[[Any], Optional[str]],
                         first_parent: Optional[str],
                         anchor: Optional[str] = None) -> Dict[str, Any]:
    """The full recompute-and-verify walk. Returns
    {valid, entries, head, [broken_at, reason], [tail_anchored]} — real per-entry verdicts,
    never a constant."""
    prev = first_parent
    for i, e in enumerate(entries):
        if parent_hash(e) != prev:
            return {"valid": False, "entries": len(entries), "broken_at": i,
                    "reason": "parent_link_mismatch"}
        if recompute(e) != stored_hash(e):
            return {"valid": False, "entries": len(entries), "broken_at": i,
                    "reason": "content_hash_mismatch (payload tampered)"}
        prev = stored_hash(e)
    out: Dict[str, Any] = {"valid": True, "entries": len(entries), "head": prev}
    if anchor is not None:
        out["tail_anchored"] = (anchor == prev)
        if anchor != prev:
            out["valid"] = False
            out["reason"] = "tail_anchor_mismatch (truncation/rollback suspected)"
    return out


def write_anchor(anchor_path: str, head: Optional[str], count: int) -> None:
    """Stamp the chain head into the sibling anchor file (best-effort — an anchor write fault
    never loses the ledger append itself)."""
    try:
        tmp = anchor_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"head": head, "count": count}, f)
        os.replace(tmp, anchor_path)
    except Exception:
        pass


def read_anchor(anchor_path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(anchor_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
