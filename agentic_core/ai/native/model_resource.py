"""
Model Resource Registry — the native AI fabric's catalogue of usable model resources.

Honest, in-house-first enumeration:
  - native  (always)         : Workstation's own structured engine (the floor).
  - ollama  (local/self-hosted): used when a local Ollama server is reachable — OWNED capability.
  - anthropic / openai (external): OPTIONAL accelerants, available ONLY when a key is present AND
                                   AI_ALLOW_EXTERNAL=true. Never a dependency.

The registry never makes Workstation depend on an external provider: with no key / flag off and no
local model, the `native` resource still serves. `select()` returns resources in-house-first.
"""
from __future__ import annotations

import os
import time
from typing import Dict, List

_OLLAMA_CACHE = {"at": 0.0, "up": False}
_OLLAMA_TTL = 30.0


def external_allowed() -> bool:
    """External providers are opt-in accelerants only."""
    return os.getenv("AI_ALLOW_EXTERNAL", "false").lower() == "true"


def _ollama_base() -> str:
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    return url.rsplit("/api/", 1)[0] if "/api/" in url else url


def ollama_up() -> bool:
    """Probe the local Ollama server (cached). Owned/self-hosted, no external dependency."""
    now = time.monotonic()
    if now - _OLLAMA_CACHE["at"] < _OLLAMA_TTL:
        return _OLLAMA_CACHE["up"]
    up = False
    try:
        import httpx
        r = httpx.get(f"{_ollama_base()}/api/tags", timeout=1.0)
        # A server that merely responds is not enough — it must have a model pulled, or it
        # cannot serve a completion. Requiring a model avoids burning the per-call read
        # timeout on a server that will only fail, keeping the in-house path snappy.
        up = r.status_code == 200 and bool(r.json().get("models"))
    except Exception:
        up = False
    _OLLAMA_CACHE.update(at=now, up=up)
    return up


class ModelResourceRegistry:
    """Catalogue + in-house-first selection of model resources."""

    def available(self) -> List[Dict]:
        ext = external_allowed()
        rows = [
            {"name": "native", "kind": "native", "available": True, "is_external": False,
             "note": "Workstation's own structured engine — always available, owned."},
            {"name": "ollama", "kind": "local", "available": ollama_up(), "is_external": False,
             "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
             "note": "Self-hosted local model — owned capability when running."},
            {"name": "anthropic", "kind": "external", "available": bool(os.getenv("ANTHROPIC_API_KEY")) and ext,
             "is_external": True, "model": os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6"),
             "note": "Optional accelerant — only with a key AND AI_ALLOW_EXTERNAL=true."},
            {"name": "openai", "kind": "external", "available": bool(os.getenv("OPENAI_API_KEY")) and ext,
             "is_external": True, "model": "gpt-4o-mini",
             "note": "Optional accelerant — only with a key AND AI_ALLOW_EXTERNAL=true."},
        ]
        return rows

    def select(self, prefer_external: bool = False) -> List[str]:
        """Return resource names to try, IN-HOUSE FIRST (local owned model → native floor →
        external accelerants only if allowed). External is never tried unless explicitly allowed."""
        avail = {r["name"]: r for r in self.available()}
        order: List[str] = []
        if avail["ollama"]["available"]:
            order.append("ollama")            # owned, self-hosted, real model — preferred
        # external accelerants only if allowed; placed AFTER owned local unless prefer_external
        externals = [n for n in ("anthropic", "openai") if avail[n]["available"]]
        if prefer_external and externals:
            order = externals + order
        order.append("native")                # the always-available owned floor
        if not prefer_external:
            order += externals                # accelerants last (only if allowed)
        # de-dupe, keep order
        seen, final = set(), []
        for n in order:
            if n not in seen:
                seen.add(n); final.append(n)
        return final


registry = ModelResourceRegistry()
