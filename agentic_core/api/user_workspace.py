"""§9 — the user's OWN durable workspace: their work history and interface preferences, stored
server-side and scoped to the authenticated user.

Why this exists: "My Work" and the interface preferences were a per-BROWSER localStorage store, so
a user's history did not follow them to another device, and on a shared browser one person's work
was visible to the next (W352 closed the leak by clearing on identity change — the honest minimum,
not the real fix). This is the real fix: the workspace lives with the USER.

Tenancy follows the platform invariant: `Depends(get_current_user)` → `request_owner_id` stamps the
owner server-side (a client cannot claim another owner) → `user_can_access` gates reads/writes →
404-never-403 when scoped out. Auth-off single-user mode keeps working unguarded, under the
"default" namespace, exactly as the rest of the platform does.

Durability follows the platform invariant too: every mutation is a lock-serialised
load → modify → atomic_write_json, so concurrent writes from two devices cannot interleave into a
truncated or half-written file.
"""
from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agentic_core.auth.core import get_current_user, request_owner_id, user_can_access
from agentic_core.config import atomic_write_json, data_path, load_json_tolerant, store_lock

router = APIRouter(prefix="/api/v1/user", tags=["user-workspace"])

_STORE_DIR = data_path("user_workspace")

# Caps — a workspace is a convenience store, not an archive. These mirror the frontend's caps so
# the two agree instead of silently diverging.
MAX_RECORDS = 50
MAX_OUTPUT_CHARS = 24_000
MAX_INPUT_CHARS = 400
MAX_VERSIONS = 5


def _safe_owner(owner_id: str) -> str:
    """A filesystem-safe file stem. Usernames are the owner ids, so never trust them as paths."""
    keep = "".join(ch if (ch.isalnum() or ch in "-_") else "_" for ch in (owner_id or "default"))
    return keep[:80] or "default"


def _path_for(owner_id: str):
    _STORE_DIR.mkdir(parents=True, exist_ok=True)
    return _STORE_DIR / f"{_safe_owner(owner_id)}.json"


def _empty(owner_id: str) -> dict[str, Any]:
    return {"owner_id": owner_id, "history": [], "prefs": {}, "updated_at": None}


def _load(owner_id: str) -> dict[str, Any]:
    doc = load_json_tolerant(_path_for(owner_id), _empty(owner_id))
    # A record whose owner does not match its file is a corruption/migration artifact — never
    # serve it to the caller under a different identity.
    if doc.get("owner_id") not in (owner_id, None):
        return _empty(owner_id)
    doc.setdefault("history", [])
    doc.setdefault("prefs", {})
    return doc


def _trim_record(rec: dict[str, Any]) -> dict[str, Any]:
    out = dict(rec)
    if isinstance(out.get("output"), str):
        out["output"] = out["output"][:MAX_OUTPUT_CHARS]
    if isinstance(out.get("input"), str):
        out["input"] = out["input"][:MAX_INPUT_CHARS]
    versions = out.get("versions")
    if isinstance(versions, list):
        out["versions"] = [
            {**v, "output": str(v.get("output", ""))[:MAX_OUTPUT_CHARS]}
            for v in versions[-MAX_VERSIONS:]
            if isinstance(v, dict)
        ]
    return out


class WorkspacePut(BaseModel):
    """The client's whole workspace. `owner_id` is accepted for auth-off callers only — under auth
    the server always stamps the authenticated username, so it cannot be spoofed."""
    history: list[dict[str, Any]] = Field(default_factory=list)
    prefs: dict[str, Any] = Field(default_factory=dict)
    owner_id: str = "default"


@router.get("/workspace")
async def get_workspace(owner_id: str = "default", user: dict | None = Depends(get_current_user)):
    """The caller's own workspace (history + prefs). Never another user's."""
    resolved = request_owner_id(user, owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No workspace found.")
    doc = _load(resolved)
    return {
        "owner_id": resolved,
        "history": doc.get("history", []),
        "prefs": doc.get("prefs", {}),
        "updated_at": doc.get("updated_at"),
        "count": len(doc.get("history", [])),
        "storage": "server (follows the user across devices)",
    }


@router.put("/workspace")
async def put_workspace(req: WorkspacePut, user: dict | None = Depends(get_current_user)):
    """Replace the caller's workspace. Serialised under a cross-process lock so two devices saving
    at once cannot interleave into a corrupted file."""
    resolved = request_owner_id(user, req.owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No workspace found.")
    path = _path_for(resolved)
    with store_lock(path):
        doc = _load(resolved)
        history = [_trim_record(r) for r in req.history if isinstance(r, dict)][:MAX_RECORDS]
        doc.update({
            "owner_id": resolved,
            "history": history,
            "prefs": req.prefs,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        atomic_write_json(path, doc)
    return {"owner_id": resolved, "count": len(doc["history"]), "updated_at": doc["updated_at"]}


@router.delete("/workspace")
async def clear_workspace(owner_id: str = "default", user: dict | None = Depends(get_current_user)):
    """Clear the caller's own workspace (their 'Clear preferences & history' control)."""
    resolved = request_owner_id(user, owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No workspace found.")
    path = _path_for(resolved)
    with store_lock(path):
        doc = _empty(resolved)
        doc["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        atomic_write_json(path, doc)
    return {"owner_id": resolved, "cleared": True, "updated_at": doc["updated_at"]}
