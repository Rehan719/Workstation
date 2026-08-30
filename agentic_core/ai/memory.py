from typing import List, Dict, Any
import json
import os
import tempfile
from config.paths import MEMORY_FILE
import logging

logger = logging.getLogger(__name__)

class VectorMemory:
    """v1.1 Production: Unified Absolute Path Memory.

    Hardened against two real failure modes the original lock-free read-modify-write store hit
    under load:
      • Corruption tolerance — a partially/interleaved-written store (e.g. concurrent writers, or a
        crash mid-write) yields a JSONDecodeError on load. We recover the valid JSON prefix rather
        than letting EVERY downstream AI call raise (the gateway writes here after each completion).
      • Atomic writes — write to a temp file in the same directory and os.replace() it in, so a
        reader never observes a half-written file and a crash can't truncate the live store.
    """
    def __init__(self):
        self.storage_path = str(MEMORY_FILE)
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(self.storage_path):
            self._write([])

    def _load(self) -> List[Dict[str, Any]]:
        """Load the store, tolerating a corrupt file. On corruption, recover the first complete JSON
        value (the valid prefix written before the bytes got interleaved/truncated) and discard the
        trailing garbage; if nothing is recoverable, start clean. Never raises to the caller."""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
            # recover the valid prefix, then heal the file so the next read is fast + clean
            try:
                with open(self.storage_path, "r", encoding="utf-8", errors="replace") as f:
                    raw = f.read()
                val, _ = json.JSONDecoder().raw_decode(raw.lstrip())
                recovered = [m for m in val if isinstance(m, dict) and "text" in m] if isinstance(val, list) else []
            except Exception:
                recovered = []
            self._write(recovered)   # self-heal: drop only the corrupt trailing bytes, keep real data
            return recovered

    def _write(self, memories: List[Dict[str, Any]]):
        """Atomic write via the shared hardened writer.

        W368 — this used to be a bespoke temp-file + os.replace. On Windows, os.replace fails with
        PermissionError when another writer holds the destination, so concurrent memory writes
        RAISED (93 of 120 in a measured stress) instead of retrying. config.atomic_write_json
        carries the bounded replace-retry added in W348; using it removes a second implementation
        of the same idea that never got the fix. Deliberately does NOT take store_lock: callers
        hold it around the whole load-modify-write, and store_lock is not reentrant."""
        from agentic_core.config import atomic_write_json
        atomic_write_json(self.storage_path, memories)

    MAX_MEMORIES = 500          # W277 — the store is CAPPED (most recent kept), not unbounded

    _STOP = {"the", "and", "for", "with", "that", "this", "from", "your", "have", "will",
             "what", "when", "where", "which", "their", "there", "then", "than", "them",
             "into", "about", "over", "under", "only", "also", "been", "being", "does",
             "each", "must", "should", "would", "could", "user", "output", "provide"}

    @classmethod
    def _tokens(cls, text: str) -> set:
        import re
        return {w for w in re.findall(r"[a-z]{4,}", (text or "").lower()) if w not in cls._STOP}

    # §17.5 invariant 1 (W333) — the namespace for owner-less / organism-internal memory. Recall is
    # scoped to the CALLER's own namespace PLUS this shared platform namespace, never across tenants.
    PLATFORM_NS = "platform"

    def add_memory(self, text: str, metadata: Dict[str, Any] | None = None,
                   owner_id: str | None = None):
        """Store one memory. §17.5 invariant 1 (W333): the owning tenant is stamped into metadata
        so recall can be scoped — previously every write landed in one global pool with an empty
        metadata dict, so any user's prompts/responses were retrievable into any other user's AI
        calls (reproduced live: one user's confidential prompt shipped into another's public
        website). `owner_id=None` means genuinely shared platform memory (organism beats)."""
        meta = dict(metadata or {})
        meta.setdefault("owner_id", owner_id or self.PLATFORM_NS)
        # W368 — the read→append→write cycle was UNSERIALISED: concurrent writers each loaded the
        # same list and wrote back their own copy, so all but one append was destroyed (measured:
        # 107 of 120 memories lost under 8 concurrent writers). The gateway writes here after every
        # completion, so this ran on the live request path. store_lock serialises it across threads
        # AND processes, exactly as the money paths and the constitutional ledger already do.
        from agentic_core.config import store_lock
        try:
            with store_lock(self.storage_path):
                memories = self._load()
                memories.append({"text": text, "metadata": meta})
                self._write(memories[-self.MAX_MEMORIES:])
        except TimeoutError:
            # A memory is a convenience, never worth failing the caller's AI call over. Losing one
            # under extreme contention is acceptable; corrupting the store is not — so we simply
            # do not write, and say so in the log rather than silently pretending success.
            logger.warning("memory write skipped: store busy (lock timeout) — memory not stored")

    def query_memory(self, query: str, k: int = 3, owner_id: str | None = None) -> List[str]:
        """W277 — SCORED retrieval that genuinely fires: rank memories by meaningful-token overlap
        with the query (≥2 shared tokens to count), best-then-most-recent first, top k.
        §17.5 invariant 1 (W333): recall is TENANT-SCOPED — only the caller's own namespace and the
        shared platform namespace are eligible; another tenant's memory can never be recalled.
        `owner_id=None` sees only platform memory (the safe default for anonymous/unattributed
        callers), never the whole pool."""
        q = self._tokens(query)
        if not q:
            return []
        allowed = {owner_id or self.PLATFORM_NS, self.PLATFORM_NS}
        need = min(2, len(q))    # a 1-token query can genuinely match with 1 — 2 would be unreachable
        scored = []
        for i, m in enumerate(self._load()):
            if (m.get("metadata") or {}).get("owner_id", self.PLATFORM_NS) not in allowed:
                continue
            overlap = len(q & self._tokens(m.get("text", "")))
            if overlap >= need:
                scored.append((overlap, i, m["text"]))
        scored.sort(key=lambda x: (-x[0], -x[1]))
        return [t for _, _, t in scored[:max(1, int(k))]]

memory = VectorMemory()
