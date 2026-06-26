# Agent Collaboration Hub — Design Specification
## Workstation IDBO Feature Design

**Status:** Design Complete — Implementation Ready
**Author:** Claude Cowork, 2026-06-18
**For implementation by:** Claude Code session

---

## 1. What This Is

The Agent Collaboration Hub (ACH) is both:

1. **A Workstation product feature** — the left sidebar becomes a live multi-agent workspace where the user watches AI agents collaborate, can direct any agent, and receives coordinated outputs from the full AI team
2. **A meta-coordination mechanism** — the system by which Claude Chat, Claude Code, Cowork, and specialized domain agents share context, hand off tasks, and avoid duplicating work across sessions

The ACH turns Workstation's "virtual company" metaphor into something real: the user has an actual AI C-Suite working for them, communicating with each other, routing work, and reporting progress — all visible in the sidebar.

---

## 2. The Left Sidebar — From Navigation to Agent Workspace

### Current State
The left sidebar (`Shell.tsx`) is a navigation drawer — links to routes, realm switcher, breadcrumbs.

### Target State

```
┌─────────────────────────┐
│  WORKSTATION            │
│  ━━━━━━━━━━━━━━━━━━━━━ │
│  🟢 CEO Agent (routing) │
│  🟢 Claude Code (build) │
│  🟡 CFO Agent (standby) │
│  ⚪ Domain: QEP (idle)  │
│  ━━━━━━━━━━━━━━━━━━━━━ │
│  AGENT CHANNEL: general │
│                         │
│  CEO → Code: "Phase 0   │
│  archiving complete.    │
│  Starting auth..."      │
│                         │
│  Code → You: "README    │
│  rewritten. Review?"    │
│                         │
│  You: @CEO route my     │
│  new QEP idea           │
│  ━━━━━━━━━━━━━━━━━━━━━ │
│  [Type to any agent...] │
│  [@CEO] [@Code] [@All]  │
└─────────────────────────┘
```

### Key UX Principles

- **The user is always in control.** Agents communicate with each other autonomously, but the user can interject at any point with an @mention
- **Transparent by default.** All agent-to-agent messages are visible in the general channel. Private channels exist but user can always see them
- **Non-intrusive.** The sidebar can be collapsed; agents continue working in background; notifications appear as a badge count
- **Action-oriented.** Every agent message that requires user decision ends with a clear prompt: "Review?" / "Approve?" / "Continue autonomously?"

---

## 3. Agent Roles

| Agent ID | Role | In Workstation's Virtual Company |
|----------|------|----------------------------------|
| `claude-cowork` | STRATEGY | Chief Strategy Officer — vision, design, planning, documentation |
| `claude-code` | ENGINEERING | CTO / Lead Engineer — implementation, code, tests, CI |
| `ceo-agent` | CEO | Routes requests, delegates to agents, synthesizes outputs |
| `cfo-agent` | FINANCE | Portfolio metrics, token economics, commercial framing |
| `cto-agent` | INFRASTRUCTURE | System health, build status, deployment monitoring |
| `qep-agent` | DOMAIN: RELIGION | Quran Education Platform — Islamic scholarly context |
| `law-agent` | DOMAIN: LAW | Legal analysis, contract review, compliance |
| `science-agent` | DOMAIN: SCIENCE | Research synthesis, methodology, evidence review |
| `user` | PRINCIPAL | The human — all agents ultimately serve them |

---

## 4. Backend Architecture

### New Endpoints (implement in `agentic_core/api/agent_hub.py`)

```
POST  /api/v1/hub/message              — post message (agent or user)
GET   /api/v1/hub/messages             — list recent messages (channel filter, limit)
GET   /api/v1/hub/stream               — SSE real-time message stream
POST  /api/v1/hub/agents/register      — register agent session
GET   /api/v1/hub/agents               — list active agents
DELETE /api/v1/hub/agents/{agent_id}   — deregister
POST  /api/v1/hub/claude-code-handoff  — write structured handoff for Code to pick up
GET   /api/v1/hub/handoffs             — list pending handoffs
PATCH /api/v1/hub/handoffs/{id}/claim  — claim a handoff (mark as in-progress by agent)
PATCH /api/v1/hub/handoffs/{id}/complete — mark handoff done
```

### Message Schema

```json
{
  "id": "uuid",
  "timestamp": "2026-06-18T18:00:00Z",
  "sender_id": "claude-cowork",
  "sender_role": "STRATEGY",
  "channel": "general",
  "content": "Phase 0 archiving complete. README rewritten. Handing off auth implementation.",
  "reply_to": null,
  "metadata": {
    "project_id": null,
    "task": "phase-0-documentation",
    "action": "handoff",
    "handoff_id": "abc123"
  },
  "read_by": []
}
```

### Handoff Schema

```json
{
  "id": "uuid",
  "created_at": "ISO8601",
  "from_agent": "claude-cowork",
  "to_agent": "claude-code",
  "priority": "high",
  "title": "Implement JWT auth on all project endpoints",
  "context": "Phase 1 requires auth. Design: email+password, JWT, gate /api/v1/projects/* and /api/v1/factory/*. See CLAUDE_MEMORY.md Phase 1 section.",
  "files_to_read": ["CLAUDE_MEMORY.md", "agentic_core/app_mvp.py", "agentic_core/projects/api.py"],
  "acceptance_criteria": [
    "POST /api/v1/auth/register and /api/v1/auth/login endpoints",
    "JWT middleware on all /api/v1/* routes except /health",
    "One integration test: register → login → create project → run factory"
  ],
  "status": "pending",
  "claimed_by": null,
  "claimed_at": null,
  "completed_at": null
}
```

### Persistence

- Messages: `data/agent_messages/{timestamp}_{sender_id}.json`
- Agent registry: `data/agent_registry.json`
- Handoffs: `data/handoffs/{id}.json`
- Shared context: `data/shared_context.json` (current system state for all agents)

### Shared Context Schema

```json
{
  "updated_at": "ISO8601",
  "active_phase": "phase-0",
  "current_focus": "documentation-cleanup",
  "open_handoffs": ["uuid1", "uuid2"],
  "active_agents": ["claude-cowork", "claude-code"],
  "project_portfolio": {
    "total": 0,
    "by_stage": {"concept": 0, "prototype": 0, "commercialise": 0}
  },
  "decisions": [
    {
      "date": "2026-06-18",
      "topic": "persistence",
      "decision": "File-based JSON for Phase 1, PostgreSQL for Phase 2",
      "made_by": "claude-cowork"
    }
  ],
  "open_questions": [
    {
      "id": "oq-1",
      "question": "Authentication approach: no-auth / email-password / OAuth?",
      "needs_answer_from": "ray",
      "blocking": "phase-1-auth"
    }
  ]
}
```

---

## 5. Frontend — ACH Sidebar Component

### File: `apps/workstation-superapp/src/components/layout/AgentHub.tsx`

**Structure:**

```tsx
<AgentHub>
  <AgentRoster />           // list of registered agents + online status
  <ChannelSelector />       // general | engineering | qep | enterprise | governance
  <MessageThread />         // scrollable message history with sender avatars/roles
  <Composebar />            // @mention autocomplete, send button
  <HandoffBadge />          // count of pending handoffs needing user attention
</AgentHub>
```

**AgentRoster pill design:**
- Green dot = active (last message < 5 min)
- Yellow dot = standby (registered, no recent message)
- Grey dot = offline

**Message bubble design:**
- CEO Agent: gold border, `CEO` badge
- Claude Code: blue border, `CODE` badge
- Claude Chat/Cowork: purple border, `STRATEGY` badge
- User: right-aligned, no badge
- System/status: grey, italic, no avatar

**@mention routing:**
- `@CEO` → routes to `ceo-agent` channel
- `@Code` → routes to `claude-code` channel
- `@All` → broadcasts to general channel
- `@QEP` → routes to `qep-agent` channel

### Data Fetching

Use the SSE endpoint `GET /api/v1/hub/stream` with EventSource for real-time messages — same pattern already used in ProjectsHub and SynthesisStudio.

```typescript
const source = new EventSource('/api/v1/hub/stream?channel=general');
source.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  dispatch(addMessage(msg));
};
```

### State: `agentHubStore.ts`

```typescript
interface AgentHubState {
  agents: AgentRegistration[];
  messages: HubMessage[];
  activeChannel: Channel;
  pendingHandoffs: Handoff[];
  unreadCount: number;
  isOpen: boolean;
}
```

---

## 6. Inter-Agent Coordination — Cross-Session Protocol

The challenge: Claude Chat, Code, and Cowork are separate processes with no shared runtime memory. They coordinate through files.

### Protocol Steps

**When Claude Cowork starts a session:**
1. Read `CLAUDE_MEMORY.md` — understand current state
2. Read `data/shared_context.json` — see active tasks and decisions
3. Read `data/handoffs/*.json` where `to_agent = "claude-cowork"` and `status = "pending"` — claim and action them
4. Post a registration message: `POST /api/v1/hub/agents/register`

**During a session:**
- Post messages to `/api/v1/hub/message` for major decisions, completions, questions
- Write handoffs for Claude Code: `POST /api/v1/hub/claude-code-handoff`
- Update `data/shared_context.json` with decisions made

**When ending a session:**
- Append to `CLAUDE_MEMORY.md` → Session Log
- Update `data/shared_context.json` with what changed
- Post a wrap-up message to general channel

**When Claude Code starts a session:**
1. Read `CLAUDE_MEMORY.md`
2. Read `data/handoffs/*.json` where `to_agent = "claude-code"` and `status = "pending"`
3. Claim each: `PATCH /api/v1/hub/handoffs/{id}/claim`
4. Execute, then complete: `PATCH /api/v1/hub/handoffs/{id}/complete`
5. Post result to general channel

---

## 7. QEP Agent — Special Domain Agent

The QEP (Quran Education Platform) agent deserves its own permanent registration. It holds specialized system context:

```json
{
  "agent_id": "qep-agent",
  "role": "DOMAIN: RELIGION",
  "system_context": "You are a specialist in Quran education, Islamic pedagogy, and Arabic text processing. You assist with: Quran text (using trusted authenticated sources only), memorisation (hifz) tracking, tajweed rules, teaching methodology, and community learning coordination. You never generate Arabic Quran text from an AI model — always source from authenticated text APIs. You treat all Islamic content with scholarly seriousness.",
  "capability_tags": ["quran", "arabic", "hifz", "tajweed", "dawah", "islamic-education"],
  "trusted_sources": ["quran.com API", "tanzil.net", "alquran.cloud"]
}
```

---

## 8. Implementation Order for Claude Code

1. **`agentic_core/api/agent_hub.py`** — backend router (see technical spec from subagent)
2. **Mount in `agentic_core/app_mvp.py`** — add `from agentic_core.api import agent_hub; app.include_router(agent_hub.router, prefix="/api/v1")`
3. **`apps/workstation-superapp/src/components/layout/AgentHub.tsx`** — sidebar component
4. **`apps/workstation-superapp/src/stores/agentHubStore.ts`** — Zustand store
5. **Wire into `Shell.tsx`** — add `<AgentHub />` to left sidebar
6. **`data/shared_context.json`** — initialize with current system state
7. **Register QEP agent** — seed `data/agent_registry.json` with the QEP agent definition

---

## 9. Success Criteria

The ACH is done when:

- User opens Workstation and sees the Agent Hub in the left sidebar
- Claude Code and Claude Chat/Cowork can post messages that appear in real-time in the sidebar
- User can type `@Code: implement auth` and it creates a handoff task
- User can type `@QEP: help me plan a Quran memorisation schedule` and the QEP agent responds
- All agent messages persist across page reloads
- Claude Code session reads `data/handoffs/` on startup and claims pending tasks

---

*Designed by Claude Cowork, 2026-06-18*
*Implementation: Claude Code session*
*Next review: after Phase 1 completion*
