# Agent Collaboration Hub — Claude Code Quickstart

The ACH is a lightweight message bus built into Workstation IDBO. It lets
Claude Chat/Cowork, Claude Code, and domain agents exchange messages and
structured work-orders without any external broker.

## How to mount the router (once)

In `agentic_core/main.py`, add:

```python
from agentic_core.api import agent_hub
app.include_router(agent_hub.router, prefix="/api/v1")
```

---

## Claude Code: picking up a handoff

### Step 1 — register yourself on startup

```bash
curl -s -X POST http://localhost:8000/api/v1/hub/agents/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"claude-code","role":"ENGINEERING","capability_tags":["python","fastapi","git"]}'
```

### Step 2 — subscribe to the engineering SSE stream

```bash
curl -N http://localhost:8000/api/v1/hub/stream?channel=engineering
```

Watch for events where `data.metadata.action == "handoff_created"`.
The event body includes `handoff_file` — the absolute path to the JSON work-order.

### Step 3 — read the work-order

```python
import json, pathlib
handoff = json.loads(pathlib.Path(event["handoff_file"]).read_text())
# handoff["task_title"], handoff["task_description"],
# handoff["acceptance_criteria"], handoff["related_files"]
```

### Step 4 — mark progress and completion

Update `handoff["status"]` to `"in_progress"` when you start, then `"done"` when
you finish. Post a message back so Cowork can see it:

```bash
curl -s -X POST http://localhost:8000/api/v1/hub/message \
  -H "Content-Type: application/json" \
  -d '{"sender_id":"claude-code","sender_role":"ENGINEERING",
       "channel":"engineering","content":"Handoff abc complete — PR #42 opened.",
       "metadata":{"action":"handoff_done","task":"Implement OAuth2 login"}}'
```

---

## Data directories

| Path | Contents |
|---|---|
| `data/agent_messages/` | Every hub message as `{ts}_{sender_id}.json` |
| `data/agent_registry/` | One file per registered agent |
| `data/handoffs/` | Work-orders from Claude Chat — pick these up |

---

## Endpoints at a glance

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/hub/message` | Post a message |
| GET | `/api/v1/hub/messages` | List recent messages (`?channel=&limit=`) |
| GET | `/api/v1/hub/stream` | SSE stream (`?channel=engineering`) |
| POST | `/api/v1/hub/agents/register` | Register agent |
| GET | `/api/v1/hub/agents` | List agents |
| DELETE | `/api/v1/hub/agents/{id}` | Deregister |
| POST | `/api/v1/hub/claude-code-handoff` | Drop a work-order for Claude Code |
