"""
Agent Collaboration Hub (ACH) — agentic_core/api/agent_hub.py
==============================================================

A message bus that lets multiple AI agents (Claude Chat/Cowork, Claude Code,
domain agents, the user) post, retrieve, and stream messages in real-time.

Design principles
-----------------
- File-based persistence, matching the projects/api.py pattern exactly:
    data/agent_messages/{timestamp}_{sender_id}.json  — individual messages
    data/agent_registry/{agent_id}.json               — registered agent records
    data/handoffs/{timestamp}_{from_agent}.json       — Claude Code handoff files
- SSE streaming via StreamingResponse (same pattern as products.py reactor/run).
- No external broker needed: asyncio.Queue per connected SSE client, fanned-out
  whenever a new message is written.
- Router mounted at prefix="/api/v1" in main.py → final paths /api/v1/hub/...

Registration in main.py (add these two lines):
    from agentic_core.api import agent_hub
    app.include_router(agent_hub.router, prefix="/api/v1")
"""

from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, AsyncIterator, Literal, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from agentic_core.organism.biobus import biobus

# ── Directory layout ──────────────────────────────────────────────────────────
# All paths are relative to the process working directory (repo root), which
# matches how projects/api.py and products.py handle `data/…` paths.

_MSG_DIR = Path((os.getenv("ACH_MESSAGES_DIR") or str(data_path("agent_messages"))))
_REG_DIR = Path((os.getenv("ACH_REGISTRY_DIR") or str(data_path("agent_registry"))))
_HANDOFF_DIR = Path((os.getenv("ACH_HANDOFFS_DIR") or str(data_path("handoffs"))))

for _d in (_MSG_DIR, _REG_DIR, _HANDOFF_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ── In-process fan-out bus ────────────────────────────────────────────────────
# Each SSE client that connects to GET /hub/stream gets its own asyncio.Queue.
# When a message is posted (via POST /hub/message), _broadcast() pushes the
# serialised message to every live queue.  No threads, no locks needed because
# FastAPI runs everything on a single event-loop thread with async I/O.

_SSE_CLIENTS: list[asyncio.Queue] = []


async def _broadcast(payload: dict) -> None:
    """Push a dict to every connected SSE queue.  Dead/disconnected queues are
    cleaned up lazily: we just skip ones that are full (backpressure guard)."""
    serialised = json.dumps(payload, default=str)
    for q in list(_SSE_CLIENTS):
        try:
            q.put_nowait(serialised)
        except asyncio.QueueFull:
            # Client is too slow; skip rather than block the writer.
            pass


# ── Pydantic models ───────────────────────────────────────────────────────────

# Allowed sender roles — kept as a plain string Literal so callers see the
# complete enum in the OpenAPI schema without importing a separate Enum class.
SenderRole = Literal["STRATEGY", "ENGINEERING", "CEO", "USER", "DOMAIN_EXPERT"]

Channel = Literal["general", "engineering", "qep", "enterprise", "governance"]


class MessageMetadata(BaseModel):
    """Optional contextual tags attached to a message."""
    project_id: Optional[str] = None   # links message to a Workstation project
    task: Optional[str] = None         # short task label e.g. "implement auth"
    action: Optional[str] = None       # machine-readable verb e.g. "request_review"

    model_config = {"extra": "allow"}  # forward-compat: extra keys are kept


class HubMessage(BaseModel):
    """Full message record — stored to disk and streamed to clients."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: _iso_now())
    sender_id: str                          # e.g. "claude-cowork", "claude-code", "user"
    sender_role: SenderRole
    channel: Channel = "general"
    content: str
    reply_to: Optional[str] = None          # id of the message being replied to
    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    read_by: list[str] = Field(default_factory=list)  # list of agent_ids


class PostMessageRequest(BaseModel):
    """Body for POST /hub/message."""
    sender_id: str
    sender_role: SenderRole
    content: str
    channel: Channel = "general"
    reply_to: Optional[str] = None
    metadata: Optional[MessageMetadata] = None


class AgentRecord(BaseModel):
    """Registered agent — stored to disk."""
    agent_id: str
    role: SenderRole
    capability_tags: list[str] = Field(default_factory=list)
    registered_at: str = Field(default_factory=lambda: _iso_now())
    last_active: str = Field(default_factory=lambda: _iso_now())


class RegisterAgentRequest(BaseModel):
    """Body for POST /hub/agents/register."""
    agent_id: str
    role: SenderRole
    capability_tags: list[str] = Field(default_factory=list)


class HandoffRequest(BaseModel):
    """Body for POST /hub/claude-code-handoff.

    Claude Chat/Cowork calls this endpoint at the end of a planning session to
    leave a structured work-order that Claude Code should execute.
    """
    from_agent: str                          # e.g. "claude-cowork-session-abc"
    to_agent: str = "claude-code"
    project_id: Optional[str] = None
    task_title: str
    task_description: str
    acceptance_criteria: list[str] = Field(default_factory=list)
    priority: Literal["low", "normal", "high", "critical"] = "normal"
    related_files: list[str] = Field(default_factory=list)
    metadata: Optional[dict] = None


# ── Helpers ───────────────────────────────────────────────────────────────────

def _iso_now() -> str:
    """Return current UTC time as an ISO-8601 string (no external deps)."""
    import datetime
    return datetime.datetime.utcnow().isoformat() + "Z"


def _msg_path(timestamp_str: str, sender_id: str) -> Path:
    """Deterministic filename for a message, matching the spec:
    {timestamp}_{sender_id}.json  — colons stripped for Windows compat."""
    safe_ts = timestamp_str.replace(":", "-").replace(".", "-")
    safe_sid = sender_id.replace("/", "_").replace(" ", "_")
    return _MSG_DIR / f"{safe_ts}_{safe_sid}.json"


def _write_json(path: Path, data: dict) -> None:
    """Atomic-ish write: write to .tmp then rename to avoid partial reads."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    tmp.rename(path)


def _load_all_messages(channel: Optional[str] = None, limit: int = 100) -> list[dict]:
    """Load messages from disk, newest-first, with optional channel filter.

    Files are sorted by mtime (cheapest proxy for creation order without
    scanning every filename).  For production scale, swap in a SQLite index.
    """
    files = sorted(_MSG_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    results: list[dict] = []
    for f in files:
        if len(results) >= limit:
            break
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue  # corrupt or partially written file — skip gracefully
        if channel and data.get("channel") != channel:
            continue
        results.append(data)
    return results


def _load_all_agents() -> list[dict]:
    """Return all registered agent records."""
    records: list[dict] = []
    for f in _REG_DIR.glob("*.json"):
        try:
            records.append(json.loads(f.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return records


# ── Router ────────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/hub", tags=["Agent Collaboration Hub"])


# ── Messages ──────────────────────────────────────────────────────────────────

@router.post("/message", response_model=HubMessage, status_code=201)
async def post_message(req: PostMessageRequest) -> HubMessage:
    """Post a message from an agent or the user.

    Steps:
    1. Build a HubMessage with a fresh UUID and timestamp.
    2. Persist it to data/agent_messages/{ts}_{sender_id}.json.
    3. Fan-out to all live SSE clients so GET /hub/stream subscribers see it
       without polling.
    4. Touch the sender's registry record (last_active) if they're registered.
    """
    msg = HubMessage(
        sender_id=req.sender_id,
        sender_role=req.sender_role,
        content=req.content,
        channel=req.channel,
        reply_to=req.reply_to,
        metadata=req.metadata or MessageMetadata(),
    )

    # Persist to disk
    path = _msg_path(msg.timestamp, msg.sender_id)
    _write_json(path, msg.model_dump())

    # Update sender's last_active if they exist in the registry
    reg_path = _REG_DIR / f"{msg.sender_id}.json"
    if reg_path.exists():
        try:
            rec = json.loads(reg_path.read_text(encoding="utf-8"))
            rec["last_active"] = msg.timestamp
            _write_json(reg_path, rec)
        except (json.JSONDecodeError, OSError):
            pass  # non-fatal; don't let a registry glitch block message posting

    # Broadcast to SSE subscribers — fire-and-forget coroutine
    await _broadcast({"event": "message", "data": msg.model_dump()})

    # Every inter-agent message is a motor signal — agents communicating = organism thinking
    biobus.fire_signal(
        "motor", f"hub.{msg.sender_role or msg.sender_id}",
        f"[{msg.channel}] {msg.content[:80]}",
        0.4,
    )

    return msg


@router.get("/messages", response_model=list[HubMessage])
async def list_messages(
    channel: Optional[str] = Query(default=None, description="Filter by channel name"),
    limit: int = Query(default=50, ge=1, le=500, description="Max messages to return"),
) -> list[HubMessage]:
    """Return recent messages, newest-first.

    Query params:
    - channel: one of general|engineering|qep|enterprise|governance
    - limit:   1–500, default 50
    """
    raw = _load_all_messages(channel=channel, limit=limit)
    return [HubMessage(**r) for r in raw]


@router.get("/stream")
async def stream_messages(
    channel: Optional[str] = Query(default=None, description="Subscribe to a specific channel only"),
) -> StreamingResponse:
    """Server-Sent Events stream of new hub messages.

    Clients connect once and receive a push event for every new message posted
    after they connect.  The event format is:

        data: {"event": "message", "data": {...HubMessage...}}\n\n

    A heartbeat ping is sent every 15 seconds so proxies / load-balancers don't
    close the idle connection.

    Usage (JavaScript):
        const es = new EventSource('/api/v1/hub/stream?channel=engineering');
        es.onmessage = e => console.log(JSON.parse(e.data));
    """
    # Each client gets its own bounded queue (max 256 pending events).
    client_queue: asyncio.Queue = asyncio.Queue(maxsize=256)
    _SSE_CLIENTS.append(client_queue)

    async def event_generator() -> AsyncIterator[str]:
        try:
            while True:
                try:
                    # Wait up to 15 s for a new message, then send a heartbeat.
                    raw = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    payload = json.loads(raw)

                    # Channel filter: if caller specified a channel, drop events
                    # for other channels server-side (saves bandwidth).
                    if channel:
                        msg_channel = payload.get("data", {}).get("channel")
                        if msg_channel and msg_channel != channel:
                            continue

                    yield f"data: {raw}\n\n"

                except asyncio.TimeoutError:
                    # SSE heartbeat comment — keeps the HTTP connection alive
                    yield ": heartbeat\n\n"

        except asyncio.CancelledError:
            # Client disconnected cleanly
            pass
        finally:
            # Always remove this client's queue to avoid memory leak
            try:
                _SSE_CLIENTS.remove(client_queue)
            except ValueError:
                pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",   # disables nginx response buffering
            "Connection": "keep-alive",
        },
    )


# ── Agent registry ────────────────────────────────────────────────────────────

@router.post("/agents/register", response_model=AgentRecord, status_code=201)
async def register_agent(req: RegisterAgentRequest) -> AgentRecord:
    """Register an agent session with the hub.

    If the agent_id already exists, its record is refreshed (re-registration is
    idempotent — useful when an agent reconnects after a restart).

    Broadcasts a system message to the 'general' channel so other agents are
    aware of the new participant.
    """
    record = AgentRecord(
        agent_id=req.agent_id,
        role=req.role,
        capability_tags=req.capability_tags,
    )

    # Persist registry record
    reg_path = _REG_DIR / f"{req.agent_id}.json"
    _write_json(reg_path, record.model_dump())

    # Announce arrival on the general channel so subscribers know
    system_msg = HubMessage(
        sender_id="hub-system",
        sender_role="STRATEGY",  # system messages use STRATEGY role as neutral default
        content=f"Agent '{req.agent_id}' ({req.role}) joined the hub. Tags: {req.capability_tags}",
        channel="general",
        metadata=MessageMetadata(action="agent_registered"),
    )
    path = _msg_path(system_msg.timestamp, system_msg.sender_id)
    _write_json(path, system_msg.model_dump())
    await _broadcast({"event": "agent_registered", "data": record.model_dump()})

    return record


@router.get("/agents", response_model=list[AgentRecord])
async def list_agents() -> list[AgentRecord]:
    """Return all currently registered agents."""
    return [AgentRecord(**r) for r in _load_all_agents()]


@router.delete("/agents/{agent_id}", status_code=200)
async def deregister_agent(agent_id: str) -> dict:
    """Remove an agent from the registry.

    Broadcasts a 'agent_left' system event so other agents can update their
    awareness of the participant pool.
    """
    reg_path = _REG_DIR / f"{agent_id}.json"
    if not reg_path.exists():
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' is not registered.")

    # Read before deleting so we can broadcast the full record
    try:
        rec = json.loads(reg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        rec = {"agent_id": agent_id}

    reg_path.unlink(missing_ok=True)

    # Announce departure
    await _broadcast({"event": "agent_left", "data": rec})

    return {"status": "deregistered", "agent_id": agent_id}


# ── Claude Code handoff ───────────────────────────────────────────────────────

@router.post("/claude-code-handoff", status_code=201)
async def create_handoff(req: HandoffRequest) -> dict:
    """Write a structured handoff file for Claude Code to pick up.

    Claude Chat/Cowork calls this endpoint at the end of a planning or design
    session.  It writes a JSON file to data/handoffs/ and posts a message to
    the 'engineering' channel so Claude Code's SSE listener is notified.

    File format
    -----------
    data/handoffs/{timestamp}_{from_agent}.json

    {
      "handoff_id": "uuid",
      "created_at": "ISO8601",
      "from_agent": "claude-cowork-session-abc",
      "to_agent": "claude-code",
      "project_id": "optional",
      "task_title": "Implement OAuth2 login",
      "task_description": "...",
      "acceptance_criteria": ["tests pass", "..."],
      "priority": "high",
      "related_files": ["src/auth.py", ...],
      "metadata": {},
      "status": "pending"   ← Claude Code sets this to "in_progress" / "done"
    }

    Claude Code workflow
    --------------------
    1. Poll GET /api/v1/hub/messages?channel=engineering  OR subscribe to
       GET /api/v1/hub/stream?channel=engineering.
    2. Filter events where metadata.action == "handoff_created".
    3. Read metadata.handoff_file to get the path, then open the JSON.
    4. Execute the task, then PATCH the file's "status" field to "done".
       (Or call DELETE /api/v1/hub/agents/{agent_id} when finished to deregister.)
    """
    import datetime

    handoff_id = str(uuid.uuid4())
    now_str = datetime.datetime.utcnow().isoformat() + "Z"
    safe_ts = now_str.replace(":", "-").replace(".", "-")
    safe_from = req.from_agent.replace("/", "_").replace(" ", "_")

    handoff_filename = f"{safe_ts}_{safe_from}.json"
    handoff_path = _HANDOFF_DIR / handoff_filename

    handoff_record = {
        "handoff_id": handoff_id,
        "created_at": now_str,
        "from_agent": req.from_agent,
        "to_agent": req.to_agent,
        "project_id": req.project_id,
        "task_title": req.task_title,
        "task_description": req.task_description,
        "acceptance_criteria": req.acceptance_criteria,
        "priority": req.priority,
        "related_files": req.related_files,
        "metadata": req.metadata or {},
        "status": "pending",  # Claude Code updates this field when it starts/finishes
    }

    _write_json(handoff_path, handoff_record)

    # Notify the engineering channel so any SSE subscriber (Claude Code) is alerted
    notification_msg = HubMessage(
        sender_id=req.from_agent,
        sender_role="STRATEGY",
        content=(
            f"HANDOFF [{req.priority.upper()}]: {req.task_title}\n"
            f"{req.task_description[:300]}"
            + ("..." if len(req.task_description) > 300 else "")
        ),
        channel="engineering",
        metadata=MessageMetadata(
            project_id=req.project_id,
            task=req.task_title,
            action="handoff_created",
            # Extra field (allowed via model_config extra="allow"):
            # Tells Claude Code exactly where to find the full handoff file.
            **{"handoff_file": str(handoff_path), "handoff_id": handoff_id},
        ),
    )
    msg_path = _msg_path(notification_msg.timestamp, notification_msg.sender_id)
    _write_json(msg_path, notification_msg.model_dump())
    await _broadcast({"event": "handoff_created", "data": {
        **notification_msg.model_dump(),
        "handoff_file": str(handoff_path),
        "handoff_id": handoff_id,
    }})

    return {
        "status": "handoff_created",
        "handoff_id": handoff_id,
        "handoff_file": str(handoff_path),
        "message_id": notification_msg.id,
        "channel": "engineering",
    }
