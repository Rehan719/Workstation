from typing import List, Dict, Any
import json
import os
import tempfile
from config.paths import MEMORY_FILE

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
        """Atomic write: temp file in the same dir → os.replace (atomic on Windows + POSIX)."""
        d = os.path.dirname(self.storage_path) or "."
        os.makedirs(d, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=d, prefix=".memory.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(memories, f)
            os.replace(tmp, self.storage_path)
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def add_memory(self, text: str, metadata: Dict[str, Any] = {}):
        memories = self._load()
        memories.append({"text": text, "metadata": metadata})
        self._write(memories)

    def query_memory(self, query: str) -> List[str]:
        """Simple keyword matching for POC RAG."""
        memories = self._load()
        results = [m["text"] for m in memories if query.lower() in m.get("text", "").lower()]
        return results[:5]

memory = VectorMemory()
