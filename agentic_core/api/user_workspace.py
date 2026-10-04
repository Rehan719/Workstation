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
from agentic_core.config import (StoreUnavailable, atomic_write_json, data_path,
                                 read_json_reported, read_json_strict, store_lock)

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
    # §4.2 (W428) — "profile" joins the document the user already owns. A separate store would
    # mean a second owner-scoping implementation to keep correct; this one is already right.
    return {"owner_id": owner_id, "history": [], "prefs": {}, "profile": {}, "updated_at": None}


def _load(owner_id: str, strict: bool = False) -> tuple[dict[str, Any], str | None]:
    """The caller's document and WHY it could not be read whole, as `(doc, unreadable_reason)`.

    W577 (FU-395) — `strict=True` is for a WRITER and it REFUSES. A tolerant read recovers the
    store's first complete JSON value and discards everything after it, so a writer that bases
    its update on that value hands the prefix to `atomic_write_json` and the remainder is gone.
    Driven on this very file: a store holding two concatenated records (267 bytes, the shape an
    interrupted overwrite of a shorter document by a longer one leaves) went through PUT /profile
    and came back 226 bytes with `history` emptied — the user's own recorded questions destroyed,
    with a success response. The rule capital_fund.py already states for the shared endowment is
    the rule here: a writer asks strictly and refuses, because writing back over a store that
    could not be read whole is how the loss becomes permanent.

    W577 (FU-298) — a READER gets the reason instead of a log line, because the person looking at
    an empty history has no way to tell "nothing saved yet" from "your history could not be read".
    """
    path = _path_for(owner_id)
    if strict:
        doc = read_json_strict(path, _empty(owner_id), expect=dict)
        why = None
    else:
        doc, why = read_json_reported(path, _empty(owner_id))
        if not isinstance(doc, dict):
            doc, why = _empty(owner_id), why or "the store did not hold a document"
    # A record whose owner does not match its file is a corruption/migration artifact — never
    # serve it to the caller under a different identity.
    if doc.get("owner_id") not in (owner_id, None):
        return _empty(owner_id), why
    doc.setdefault("history", [])
    doc.setdefault("prefs", {})
    doc.setdefault("profile", {})
    return doc, why


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
    doc, _why = _load(resolved)
    return {
        "owner_id": resolved,
        "history": doc.get("history", []),
        "prefs": doc.get("prefs", {}),
        "updated_at": doc.get("updated_at"),
        "count": len(doc.get("history", [])),
        # W577 (FU-298) — an empty history and an UNREADABLE history are the same screen without
        # this. `count` is the figure a person reads, so the reason travels beside it and says
        # which way it moves: the records that could not be read are the ones missing from it.
        "store_incomplete": _why,
        "count_is_incomplete": bool(_why),
        "count_basis": ("the records this store could not be read whole are MISSING from this count, "
                        "so your history is at least this long and may be longer"
                        if _why else "every record in this store"),
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
    try:
        # W371 — store_lock now RAISES on timeout rather than writing unserialised. Surface it as a
        # retryable 503 instead of a bare 500: the client's local copy is intact, so retrying is safe.
        with store_lock(path):
            doc, _ = _load(resolved, strict=True)     # W577 (FU-395) — a writer refuses
            history = [_trim_record(r) for r in req.history if isinstance(r, dict)][:MAX_RECORDS]
            doc.update({
                "owner_id": resolved,
                "history": history,
                "prefs": req.prefs,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            atomic_write_json(path, doc)
    except StoreUnavailable as e:
        # W577 (FU-395) — the stored document could not be read WHOLE, so nothing was written. A
        # tolerant read would have handed its recoverable prefix to the write and the rest of the
        # user's own history would be gone for good; driven on this file, 267 bytes -> 226.
        raise HTTPException(
            status_code=503,
            detail=f"{e}; your workspace was NOT overwritten, so nothing stored was lost") from None
    except TimeoutError:
        raise HTTPException(status_code=503, detail="Workspace busy — please retry.") from None
    return {"owner_id": resolved, "count": len(doc["history"]), "updated_at": doc["updated_at"]}


@router.delete("/workspace")
async def clear_workspace(owner_id: str = "default", user: dict | None = Depends(get_current_user)):
    """Clear the caller's own workspace (their 'Clear preferences & history' control)."""
    resolved = request_owner_id(user, owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No workspace found.")
    path = _path_for(resolved)
    try:
        with store_lock(path):                      # W371 — timeout is a retryable 503, not a 500
            doc = _empty(resolved)
            doc["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            atomic_write_json(path, doc)
    except TimeoutError:
        raise HTTPException(status_code=503, detail="Workspace busy — please retry.") from None
    return {"owner_id": resolved, "cleared": True, "updated_at": doc["updated_at"]}


# ── §4.2 (W428) — the explicit user profile ────────────────────────────────────────────────────
#
# "Understand the person" never happened: no profile, goals, constraints or success criteria reached
# any prompt, and there was no field to enter them. This is the field.
#
# It is NOT the recall path. gateway._augment retrieves prior interactions by token overlap and every
# generation call receives it — off by default at the gateway since W489 (W332: "recall was the leak
# vector"). This is the opposite —
# the person's own words, which they can read back and delete. See agentic_core/ai/user_context.py.


class ProfilePut(BaseModel):
    """The five §4.2 fields. Each capped server-side; the client cap is a courtesy, not the rule."""
    about_you: str = ""
    context: str = ""
    goals: str = ""
    constraints: str = ""
    success_criteria: str = ""
    owner_id: str = "default"


@router.get("/profile")
async def get_profile(owner_id: str = "default", user: dict | None = Depends(get_current_user)):
    """The caller's own profile, plus the EXACT preamble it produces.

    The preview is not decoration: a profile that silently shapes generation without the user being
    able to see what it sends is the same opacity this codebase keeps removing elsewhere.
    """
    from agentic_core.ai.user_context import PROFILE_FIELDS, build_preamble

    resolved = request_owner_id(user, owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No profile found.")
    _doc, _why = _load(resolved)
    prof = (_doc or {}).get("profile") or {}
    return {
        "owner_id": resolved,
        "profile": {k: prof.get(k, "") for k in PROFILE_FIELDS},
        "preamble_preview": build_preamble(prof),
        "applied_to": "generation prompts on this platform (never shared with other users)",
        "is_recall": False,
        # W577 (FU-298) — a blank profile form is what a user sees whether they never filled one in
        # or their stored one could not be read. Saving over the second is how the first becomes true.
        "store_incomplete": _why,
        "profile_is_incomplete": bool(_why),
    }


@router.put("/profile")
async def put_profile(req: ProfilePut, user: dict | None = Depends(get_current_user)):
    """Replace the caller's profile. Same lock + atomic write as the workspace it lives in."""
    from agentic_core.ai.user_context import MAX_FIELD_CHARS, PROFILE_FIELDS, build_preamble

    resolved = request_owner_id(user, req.owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No profile found.")
    prof = {k: str(getattr(req, k, "") or "")[:MAX_FIELD_CHARS] for k in PROFILE_FIELDS}
    path = _path_for(resolved)
    try:
        with store_lock(path):
            doc, _ = _load(resolved, strict=True)     # W577 (FU-395) — a writer refuses
            doc["owner_id"] = resolved
            doc["profile"] = prof
            doc["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            atomic_write_json(path, doc)
    except StoreUnavailable as e:
        # W577 (FU-395) — as put_workspace: a writer refuses rather than persisting a prefix.
        raise HTTPException(
            status_code=503,
            detail=f"{e}; your profile was NOT overwritten, so nothing stored was lost") from None
    except TimeoutError:
        raise HTTPException(status_code=503, detail="Profile busy — please retry.") from None
    return {"owner_id": resolved, "profile": prof, "preamble_preview": build_preamble(prof),
            "updated_at": doc["updated_at"]}


@router.delete("/profile")
async def clear_profile(owner_id: str = "default", user: dict | None = Depends(get_current_user)):
    """Delete the caller's profile — the whole thing, not a soft flag.

    Clearing must genuinely stop it reaching prompts, which is why this empties the key rather than
    marking it inactive: an "inactive" profile still sitting in the store is exactly the kind of
    almost-deleted state a user would reasonably call a lie.
    """
    resolved = request_owner_id(user, owner_id)
    if not user_can_access(user, resolved):
        raise HTTPException(status_code=404, detail="No profile found.")
    path = _path_for(resolved)
    try:
        with store_lock(path):
            doc, _ = _load(resolved, strict=True)     # W577 (FU-395) — a writer refuses
            doc["profile"] = {}
            doc["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            atomic_write_json(path, doc)
    except StoreUnavailable as e:
        # W577 (FU-395) — as put_workspace: a writer refuses rather than persisting a prefix.
        raise HTTPException(
            status_code=503,
            detail=f"{e}; your profile was NOT overwritten, so nothing stored was lost") from None
    except TimeoutError:
        raise HTTPException(status_code=503, detail="Profile busy — please retry.") from None
    return {"owner_id": resolved, "cleared": True, "updated_at": doc["updated_at"]}
