"""
Agent Collaboration Hub (ACH) — agentic_core/api/agent_hub.py
==============================================================

A file-backed message bus with a real SSE stream (in-process fan-out), an agent
registry, and a work-order letterbox ("handoffs").

W443 truth pass — what this IS and IS NOT:
  • The transport is real: messages persist to disk and fan out to connected SSE
    clients (at-most-once, single-process scope — a slow client's queue drops
    events, and a second uvicorn worker would not see this worker's posts).
  • The bus is honest about occupancy: no platform module consumes hub messages
    today. Posting returns how many live subscribers actually received the
    message; a handoff is recorded as a WORK-ORDER RECORD, not an execution —
    no executor is subscribed, and nothing runs handoffs automatically.
  • Security (W443): every op requires an authenticated user when AUTH is
    enabled; every value used in a filename is validated against a strict id
    rule (no separators of either kind); the acting principal is stamped
    server-side into every stored record — a caller-supplied sender name is a
    LABEL, never an identity.

Stores (all under data_path, the platform store conventions):
    agent_messages/{timestamp}_{sender_id}.json
    agent_registry/{agent_id}.json
    handoffs/{timestamp}_{from_agent}.json
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, AsyncIterator, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from agentic_core.auth.core import auth_enabled, get_current_user, user_can_access
from agentic_core.config import atomic_write_json, data_path, load_json_tolerant, store_lock
from agentic_core.organism.biobus import biobus

_MSG_DIR = Path((os.getenv("ACH_MESSAGES_DIR") or str(data_path("agent_messages"))))
_REG_DIR = Path((os.getenv("ACH_REGISTRY_DIR") or str(data_path("agent_registry"))))
_HANDOFF_DIR = Path((os.getenv("ACH_HANDOFFS_DIR") or str(data_path("handoffs"))))

for _d in (_MSG_DIR, _REG_DIR, _HANDOFF_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Retention: message files accumulate one per post; the sweep keeps the newest N so an
# unattended deployment cannot grow without bound (checked every _SWEEP_EVERY posts).
_MAX_MESSAGE_FILES = 5000
_MAX_HANDOFF_FILES = 2000
_SWEEP_EVERY = 100
_post_counter = 0

# ── In-process fan-out bus ────────────────────────────────────────────────────
_SSE_CLIENTS: list[asyncio.Queue] = []


async def _broadcast(payload: dict) -> int:
    """Push a dict to every connected SSE queue; returns how many clients actually
    received it. A full (slow) client's queue is marked dropped — the client gets a
    one-time 'gap' event on its next drain instead of silently missing history."""
    serialised = json.dumps(payload, default=str)
    delivered = 0
    for q in list(_SSE_CLIENTS):
        try:
            q.put_nowait(serialised)
            delivered += 1
        except asyncio.QueueFull:
            setattr(q, "dropped_events", True)
    return delivered


# ── Identity / filename safety (W443) ─────────────────────────────────────────
# Every value that becomes part of a filename MUST pass this rule: 1-64 chars of
# [A-Za-z0-9_.-], no leading dot. This excludes both separator kinds ('/' and '\\')
# and relative-path tokens, so an id can never address a path outside its store.
_ID_RE = re.compile(r"(?!\.)[A-Za-z0-9_.\-]{1,64}$")


def _safe_id(value: str, field: str) -> str:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise HTTPException(status_code=422, detail=(
            f"{field} must be 1-64 characters of letters, digits, '_', '-' or '.' "
            "(no leading dot, no path separators)."))
    return value


def _owner_for_access(record: dict) -> str | None:
    """W443 refuter catch: records stamped 'local' (created while auth was OFF) must map to the
    platform's legacy-record convention — admin-only under auth — not to a claimable username
    literally called 'local'."""
    owner = record.get("registered_by")
    return None if owner in (None, "local") else str(owner)


def _require_hub_user(user: dict | None, action: str) -> str:
    """W443 — the hub is the channel where instructions for the platform's agents
    travel; under auth every op requires an authenticated principal. Single-user
    mode (auth off) has no tenant boundary and acts as 'local'."""
    if not auth_enabled():
        return "local"
    if not isinstance(user, dict) or not user.get("username"):
        raise HTTPException(status_code=401, detail=f"Authentication required to {action} on the agent hub.")
    return str(user["username"])


# ── Pydantic models ───────────────────────────────────────────────────────────

SenderRole = Literal["STRATEGY", "ENGINEERING", "CEO", "USER", "DOMAIN_EXPERT"]
Channel = Literal["general", "engineering", "qep", "enterprise", "governance"]


class MessageMetadata(BaseModel):
    """Optional contextual tags attached to a message."""
    project_id: Optional[str] = None
    task: Optional[str] = Field(default=None, max_length=200)
    action: Optional[str] = Field(default=None, max_length=100)

    model_config = {"extra": "allow"}  # forward-compat: extra keys are kept


class HubMessage(BaseModel):
    """Full message record — stored to disk and streamed to clients.

    W443: the old `read_by` field advertised per-agent read tracking that no code
    ever wrote (always []) — deleted until an acknowledgement op exists.
    `posted_by` is the server-stamped principal; `sender_id` is a caller label."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: _iso_now())
    sender_id: str
    sender_role: SenderRole
    posted_by: str = "local"
    channel: Channel = "general"
    content: str
    reply_to: Optional[str] = None
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)


class PostMessageRequest(BaseModel):
    sender_id: str = Field(max_length=64)
    sender_role: SenderRole
    content: str = Field(min_length=1, max_length=16000)
    channel: Channel = "general"
    reply_to: Optional[str] = Field(default=None, max_length=64)
    metadata: Optional[MessageMetadata] = None


class AgentRecord(BaseModel):
    agent_id: str
    role: SenderRole
    capability_tags: list[str] = Field(default_factory=list)
    registered_by: str = "local"
    registered_at: str = Field(default_factory=lambda: _iso_now())
    last_active: str = Field(default_factory=lambda: _iso_now())


class RegisterAgentRequest(BaseModel):
    agent_id: str = Field(max_length=64)
    role: SenderRole
    capability_tags: list[str] = Field(default_factory=list, max_length=50)


class HandoffRequest(BaseModel):
    """Body for POST /hub/claude-code-handoff — a structured work-order RECORD.

    W443: the old docstring claimed 'Claude Code should execute' these and that an
    'SSE listener is notified' — no such executor or listener exists anywhere in
    the platform. A handoff is a record a human or agent may later pick up via
    GET /hub/handoffs; its status moves only when someone calls the status op."""
    from_agent: str = Field(max_length=64)
    to_agent: str = Field(default="claude-code", max_length=64)
    project_id: Optional[str] = Field(default=None, max_length=100)
    task_title: str = Field(min_length=1, max_length=200)
    task_description: str = Field(min_length=1, max_length=20000)
    acceptance_criteria: list[str] = Field(default_factory=list, max_length=50)
    priority: Literal["low", "normal", "high", "critical"] = "normal"
    related_files: list[str] = Field(default_factory=list, max_length=50)
    metadata: Optional[dict] = None


class HandoffStatusRequest(BaseModel):
    status: Literal["in_progress", "done"]
    note: str = Field(default="", max_length=2000)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _iso_now() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _msg_path(timestamp_str: str, sender_id: str) -> Path:
    safe_ts = timestamp_str.replace(":", "-").replace(".", "-")
    return _MSG_DIR / f"{safe_ts}_{sender_id}.json"


def _load_all_messages(channel: Optional[str] = None, limit: int = 100) -> list[dict]:
    """Load messages from disk, newest-first, with optional channel filter."""
    files = sorted(_MSG_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    results: list[dict] = []
    for f in files:
        if len(results) >= limit:
            break
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue  # corrupt or partially written file — skip
        if channel and data.get("channel") != channel:
            continue
        results.append(data)
    return results


def _load_all_agents() -> list[dict]:
    records: list[dict] = []
    for f in _REG_DIR.glob("*.json"):
        try:
            records.append(json.loads(f.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return records


def _sweep_dir(directory: Path, keep: int) -> None:
    """Keep the newest `keep` files in a hub store (unbounded growth guard). W443 refuter
    catch: the sweep originally covered messages only and its counter advanced only on plain
    posts — registrations and handoffs also write files and now advance it too, and the
    handoff letterbox has its own cap."""
    try:
        files = sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old in files[keep:]:
            old.unlink(missing_ok=True)
    except OSError:
        pass


def _count_write_and_maybe_sweep() -> None:
    global _post_counter
    _post_counter += 1
    if _post_counter % _SWEEP_EVERY == 0:
        _sweep_dir(_MSG_DIR, _MAX_MESSAGE_FILES)
        _sweep_dir(_HANDOFF_DIR, _MAX_HANDOFF_FILES)


# ── Router ────────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/hub", tags=["Agent Collaboration Hub"])


# ── Messages ──────────────────────────────────────────────────────────────────

@router.post("/message", status_code=201)
async def post_message(req: PostMessageRequest,
                       user: dict | None = Depends(get_current_user)) -> dict:
    """Post a message onto the hub: persisted, then fanned out to live SSE clients.

    The response reports `delivered_to_live_subscribers` — the number of connected
    stream clients that actually received it. Zero means the message is stored but
    nobody was listening; nothing on the platform consumes hub messages by itself."""
    principal = _require_hub_user(user, "post a message")
    _safe_id(req.sender_id, "sender_id")

    msg = HubMessage(
        sender_id=req.sender_id,
        sender_role=req.sender_role,
        posted_by=principal,
        content=req.content,
        channel=req.channel,
        reply_to=req.reply_to,
        metadata=req.metadata or MessageMetadata(),
    )
    atomic_write_json(_msg_path(msg.timestamp, msg.sender_id), msg.model_dump())

    # touch the sender's registry record (last_active) if registered — under the store
    # lock, with the platform's atomic writer (the old bespoke rename silently failed
    # on Windows every time, freezing last_active at registration forever)
    reg_path = _REG_DIR / f"{msg.sender_id}.json"
    if reg_path.exists():
        try:
            with store_lock(reg_path):
                rec = load_json_tolerant(reg_path, None)
                if isinstance(rec, dict):
                    rec["last_active"] = msg.timestamp
                    atomic_write_json(reg_path, rec)
        except (OSError, TimeoutError):
            pass  # non-fatal; the message itself is already persisted

    delivered = await _broadcast({"event": "message", "data": msg.model_dump()})

    # W443 — organism telemetry stays honest: a motor signal means communication, and
    # communication requires a receiver. A message nobody received fires nothing (the
    # old code counted letters in a dead letterbox as "organism thinking"). The source
    # carries hub provenance so it can never masquerade as an organic signal.
    if delivered > 0:
        biobus.fire_signal("motor", f"hub:{msg.sender_id}",
                           f"[{msg.channel}] {msg.content[:80]}", 0.4)

    _count_write_and_maybe_sweep()
    return {**msg.model_dump(), "delivered_to_live_subscribers": delivered}


@router.get("/messages", response_model=list[HubMessage])
async def list_messages(
    channel: Optional[str] = Query(default=None, description="Filter by channel name"),
    limit: int = Query(default=50, ge=1, le=500),
    user: dict | None = Depends(get_current_user),
) -> list[HubMessage]:
    """Return recent messages, newest-first. A stored row that no longer validates
    against the schema is skipped like a corrupt file, never a 500 for the listing."""
    _require_hub_user(user, "read messages")
    out: list[HubMessage] = []
    for r in _load_all_messages(channel=channel, limit=limit):
        try:
            out.append(HubMessage(**r))
        except Exception:
            continue
    return out


@router.get("/stream")
async def stream_messages(
    channel: Optional[str] = Query(default=None),
    user: dict | None = Depends(get_current_user),
) -> StreamingResponse:
    """Server-Sent Events stream of new hub messages (single-process scope).

    Semantics are AT-MOST-ONCE: a client whose queue backs up (256 pending) has
    events dropped and receives one `{"event": "gap"}` marker on its next drain
    so it knows history was missed. A 15s heartbeat keeps proxies alive."""
    _require_hub_user(user, "subscribe to the stream")
    client_queue: asyncio.Queue = asyncio.Queue(maxsize=256)
    _SSE_CLIENTS.append(client_queue)

    async def event_generator() -> AsyncIterator[str]:
        try:
            while True:
                try:
                    raw = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    if getattr(client_queue, "dropped_events", False):
                        setattr(client_queue, "dropped_events", False)
                        yield 'data: {"event": "gap", "note": "events were dropped while this client was slow"}\n\n'
                    payload = json.loads(raw)
                    if channel:
                        msg_channel = payload.get("data", {}).get("channel")
                        if msg_channel and msg_channel != channel:
                            continue
                    yield f"data: {raw}\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            try:
                _SSE_CLIENTS.remove(client_queue)
            except ValueError:
                pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


# ── Agent registry ────────────────────────────────────────────────────────────

@router.post("/agents/register", response_model=AgentRecord, status_code=201)
async def register_agent(req: RegisterAgentRequest,
                         user: dict | None = Depends(get_current_user)) -> AgentRecord:
    """Register an agent session. Re-registration refreshes the record (genuinely
    idempotent now — the old bespoke writer raised on overwrite on Windows, so the
    docstring's 'idempotent' claim 500'd exactly where the platform runs)."""
    principal = _require_hub_user(user, "register an agent")
    _safe_id(req.agent_id, "agent_id")

    record = AgentRecord(
        agent_id=req.agent_id,
        role=req.role,
        capability_tags=[t[:80] for t in req.capability_tags],
        registered_by=principal,
    )
    reg_path = _REG_DIR / f"{req.agent_id}.json"
    with store_lock(reg_path):
        prev = load_json_tolerant(reg_path, None) if reg_path.exists() else None
        if isinstance(prev, dict):
            # W443 refuter catch: without this, an authenticated tenant could OVERWRITE another
            # user's registration (re-stamping registered_by) and then pass the deregister gate —
            # the "registrant or admin only" claim was circumventable via overwrite-then-delete.
            if auth_enabled() and not user_can_access(user, _owner_for_access(prev)):
                raise HTTPException(status_code=409, detail=(
                    f"Agent id '{req.agent_id}' is registered by another user."))
            if prev.get("registered_at"):
                record.registered_at = prev["registered_at"]   # a refresh, not a rebirth
        atomic_write_json(reg_path, record.model_dump())

    system_msg = HubMessage(
        sender_id="hub-system",
        sender_role="STRATEGY",
        posted_by=principal,
        content=f"Agent '{req.agent_id}' ({req.role}) joined the hub. Tags: {record.capability_tags}",
        channel="general",
        metadata=MessageMetadata(action="agent_registered"),
    )
    atomic_write_json(_msg_path(system_msg.timestamp, system_msg.sender_id), system_msg.model_dump())
    await _broadcast({"event": "agent_registered", "data": record.model_dump()})
    _count_write_and_maybe_sweep()
    return record


@router.get("/agents")
async def list_agents(user: dict | None = Depends(get_current_user)) -> dict:
    """The hub's participants, honestly split: `registered` are external agent
    sessions that registered themselves (empty until one does); `platform_roster`
    is the swarm's live cast — real platform constructs, listed here so the hub
    reflects who actually exists rather than an empty room narrating a community."""
    _require_hub_user(user, "list agents")
    roster: list[dict] = []
    try:
        from agentic_core.api.swarm import _AGENTS as _SWARM_AGENTS
        roster = [{"id": k, **v, "source": "swarm roster (live platform agents)"}
                  for k, v in _SWARM_AGENTS.items()]
    except Exception:
        roster = []
    registered = []
    for r in _load_all_agents():
        try:
            registered.append(AgentRecord(**r).model_dump())
        except Exception:
            continue
    return {
        "registered": registered,
        "platform_roster": roster,
        "note": ("`registered` lists external agent sessions that called /hub/agents/register; "
                 "`platform_roster` is the swarm's live agent cast. Registration gates nothing "
                 "by itself — it is a presence record."),
    }


@router.delete("/agents/{agent_id}", status_code=200)
async def deregister_agent(agent_id: str,
                           user: dict | None = Depends(get_current_user)) -> dict:
    """Remove an agent from the registry (registrant or admin only under auth)."""
    principal = _require_hub_user(user, "deregister an agent")
    _safe_id(agent_id, "agent_id")
    reg_path = _REG_DIR / f"{agent_id}.json"
    if not reg_path.exists():
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' is not registered.")
    rec = load_json_tolerant(reg_path, None) or {"agent_id": agent_id}
    if auth_enabled() and not user_can_access(user, _owner_for_access(rec)):
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' is not registered.")
    reg_path.unlink(missing_ok=True)
    await _broadcast({"event": "agent_left", "data": rec})
    return {"status": "deregistered", "agent_id": agent_id, "by": principal}


# ── Work-order letterbox ("handoffs") ─────────────────────────────────────────

@router.post("/claude-code-handoff", status_code=201)
async def create_handoff(req: HandoffRequest,
                         user: dict | None = Depends(get_current_user)) -> dict:
    """Record a structured work-order. W443 — honest semantics: this WRITES A
    RECORD. No executor is subscribed; nothing on the platform reads, polls or
    runs handoffs automatically. The record is visible at GET /hub/handoffs and
    its status moves only when someone calls POST /hub/handoffs/{id}/status.
    Any future consumer must treat task_description as untrusted data behind an
    Owner approval gate — never auto-fed to a model or an executing session."""
    principal = _require_hub_user(user, "file a handoff")
    _safe_id(req.from_agent, "from_agent")
    _safe_id(req.to_agent, "to_agent")

    handoff_id = str(uuid.uuid4())
    now_str = _iso_now()
    safe_ts = now_str.replace(":", "-").replace(".", "-")
    handoff_path = _HANDOFF_DIR / f"{safe_ts}_{req.from_agent}.json"

    handoff_record = {
        "handoff_id": handoff_id,
        "created_at": now_str,
        "filed_by": principal,
        "from_agent": req.from_agent,
        "to_agent": req.to_agent,
        "project_id": req.project_id,
        "task_title": req.task_title,
        "task_description": req.task_description,
        "acceptance_criteria": req.acceptance_criteria,
        "priority": req.priority,
        "related_files": req.related_files,
        "metadata": req.metadata or {},
        "status": "recorded",
        "status_note": "no executor is subscribed — this is a work-order record; nothing runs it automatically",
        "status_history": [{"status": "recorded", "at": now_str, "by": principal}],
    }
    atomic_write_json(handoff_path, handoff_record)

    notification_msg = HubMessage(
        sender_id=req.from_agent,
        sender_role="STRATEGY",
        posted_by=principal,
        content=(f"HANDOFF [{req.priority.upper()}]: {req.task_title}\n"
                 f"{req.task_description[:300]}"
                 + ("..." if len(req.task_description) > 300 else "")),
        channel="engineering",
        metadata=MessageMetadata(
            project_id=req.project_id,
            task=req.task_title,
            action="handoff_created",
            **{"handoff_id": handoff_id},
        ),
    )
    atomic_write_json(_msg_path(notification_msg.timestamp, notification_msg.sender_id),
                      notification_msg.model_dump())
    delivered = await _broadcast({"event": "handoff_created", "data": {
        **notification_msg.model_dump(), "handoff_id": handoff_id,
    }})
    _count_write_and_maybe_sweep()

    return {
        "status": "recorded",
        "handoff_id": handoff_id,
        "message_id": notification_msg.id,
        "channel": "engineering",
        "delivered_to_live_subscribers": delivered,
        "note": ("Work-order recorded and visible at GET /hub/handoffs. No executor is "
                 "subscribed to the hub — nothing will run this automatically."),
    }


@router.get("/handoffs")
async def list_handoffs(limit: int = Query(default=50, ge=1, le=200),
                        user: dict | None = Depends(get_current_user)) -> dict:
    """The work-order letterbox, newest-first — the listing the original design
    promised and never built (handoffs were write-only files nobody could see)."""
    _require_hub_user(user, "list handoffs")
    files = sorted(_HANDOFF_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    rows: list[dict] = []
    for f in files[:limit]:
        try:
            rows.append(json.loads(f.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return {"handoffs": rows, "total_on_disk": len(files),
            "note": "records only — no executor is subscribed; statuses move via POST /hub/handoffs/{id}/status"}


@router.post("/handoffs/{handoff_id}/status")
async def update_handoff_status(handoff_id: str, req: HandoffStatusRequest,
                                user: dict | None = Depends(get_current_user)) -> dict:
    """Move a work-order's status (in_progress | done) — the op the original file
    format referenced ('Claude Code updates this field') without providing any way
    to do it. Stamped and history-tracked."""
    principal = _require_hub_user(user, "update a handoff")
    _safe_id(handoff_id, "handoff_id")
    for f in _HANDOFF_DIR.glob("*.json"):
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if rec.get("handoff_id") == handoff_id:
            now = _iso_now()
            # re-read INSIDE the lock — the scan's read is only a locator, never the write base
            # (a concurrent status update would otherwise be lost to read-modify-write)
            with store_lock(f):
                rec = load_json_tolerant(f, None)
                if not isinstance(rec, dict) or rec.get("handoff_id") != handoff_id:
                    continue
                rec["status"] = req.status
                rec["status_note"] = req.note or ("claimed by an executor" if req.status == "in_progress"
                                                  else "completed")
                rec.setdefault("status_history", []).append(
                    {"status": req.status, "at": now, "by": principal, "note": req.note})
                atomic_write_json(f, rec)
            await _broadcast({"event": "handoff_status", "data": {
                "handoff_id": handoff_id, "status": req.status, "by": principal}})
            return {"handoff_id": handoff_id, "status": req.status, "by": principal}
    raise HTTPException(status_code=404, detail=f"No handoff with id '{handoff_id}'.")
