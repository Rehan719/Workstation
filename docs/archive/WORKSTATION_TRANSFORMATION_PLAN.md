# WORKSTATION IDBO — Master Transformation Plan
## Commercial Readiness Edition — June 2026

*بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ*

> *This document is the living operational blueprint for transforming Workstation IDBO from
> its current state into a commercially ready, purpose-aligned, professionally excellent
> platform. It is grounded in verified code — not aspiration. Every claim in this document
> is either backed by a real file in the repository or clearly marked as a target.*
>
> *Read PURPOSE.md and WORKSTATION_CONSTITUTION.md before this document.
> They establish the why. This document is the how.*

---

## SECTION 0 — What This Document Is

This is the single authoritative plan for all agents (Claude Cowork, Claude Code, Claude Chat,
and any spawned domain agents) working on Workstation IDBO. It synthesises:

- **This full conversation session** — all of Ray's inputs, all design decisions made
- **The live codebase audit** (June 2026 — 27 routers verified, religious_domain gaps identified)
- **All constitutional documents** created in this session
- **Commercial readiness analysis** — honest gaps between current state and what a real user needs
- **A phased, executable roadmap** — specific files, specific instructions, verifiable outcomes

Every section is written to be actionable by any Claude agent without additional context.

**Agents: Read Sections 1–3 for context. Start work from Section 4 onwards.**

---

## SECTION 1 — Foundation (Immovable)

### 1.1 The Purpose (Cannot Be Changed)

**Stated, explicit, public, permanent purpose of Workstation IDBO:**
To seek the Pleasure and Love of Allah SWT — by building a platform that enables every
human being to do their most meaningful work, fulfil their responsibilities to each other,
learn and practice their faith, and serve their Creator through service to His creation.

This is not background. It is the filter through which every technical decision passes.

### 1.2 The Constitutional Hierarchy

Every decision is evaluated in this order:

1. **Haqooq-ul-Allah** — does this serve the right to know and worship Allah? (QEP priority)
2. **Haqooq-ul-Ibad** — does this serve the rights of people? (equality, access, dignity)
3. **Insaaniat** — does this serve all humanity without discrimination?

When these conflict with commercial considerations, the constitutional hierarchy wins.

### 1.3 The Three Design Tests (Applied to Every Feature)

Before any feature is built or any PR merged, answer three questions:

- **Mahabbah test:** Is this built *for* users, or *extracted from* them?
- **Salaam test:** Does this reduce friction and inequality, or add to them?
- **Ihsan test:** Is this the absolute best we can produce right now?

If any answer is no — redesign or defer.

---

## SECTION 2 — Honest Current State (Verified June 2026)

### 2.1 What Is Real and Working

Confirmed by direct code inspection:

| Component | Location | Status |
|-----------|----------|--------|
| AI Gateway (3-tier fallback) | `agentic_core/ai/gateway.py` | Real, streaming |
| Projects API (CRUD + SSE + SM-2) | `agentic_core/projects/api.py` | Real |
| Products API (Reactor/Factory/Incubator/Intelligence) | `agentic_core/api/products.py` | Real AI calls |
| Synthesis Studio (Report/Pres/BizModel/Website/Audiobook) | `agentic_core/synthesis/api.py` | Real AI + file download |
| CEO Generate (stage-aware blueprint) | `agentic_core/api/v290/ceo_generate.py` | Real AI |
| C-Suite (CFO/CTO from psutil + project store) | `agentic_core/api/csuite.py` | Real metrics |
| Vitals WebSocket (real psutil) | app_mvp.py `/api/v154/ws/streams` | Real |
| Frontend (Vite + React 18 + TypeScript) | `apps/workstation-superapp/` | 100+ routes, builds clean |
| Agent Hub backend | `agentic_core/api/agent_hub.py` | Written, NOT MOUNTED |
| Law, Science, Education, Care domain routers | `agentic_core/api/{law,science,education,care}.py` | Mounted (#24–27) |
| DivineAlignmentEngine | `agentic_core/divine/alignment.py` | Exists, NOT WIRED |
| SM-2 Hifz Engine | `agentic_core/religious_domain/memorization/engine.py` | Exists, NO API SURFACE |
| Tajweed Coach | `agentic_core/religious_domain/tajwid/coach.py` | Exists, NO API SURFACE |
| Community Orchestrator | `agentic_core/religious_domain/community/forum.py` | Exists, NO API SURFACE |
| Mission Ambassador | `agentic_core/mission/ambassador_program.py` | Exists, NOT WIRED |
| SQLite databases | `data/interactions.db`, `data/chroma_db/` | Present |
| Vector store | `data/chroma_db/chroma.sqlite3` | Present |

### 2.2 What Does Not Exist Yet (Required for Commercial Readiness)

| Missing Component | Priority | Notes |
|------------------|----------|-------|
| Authentication (JWT or session) | CRITICAL | Any user can call any endpoint right now |
| religious_domain API layer | CRITICAL | 13 service classes exist, zero HTTP surface |
| Agent Hub data directories | HIGH | `data/agent_messages/`, `data/handoffs/`, `data/agent_registry/` |
| Integration tests | HIGH | No test backs any "working" claim |
| Rate limiting | HIGH | No protection against abuse |
| Error monitoring (Sentry or equivalent) | MEDIUM | Failures are invisible in production |
| User data persistence per-user | HIGH | Projects JSON not linked to authenticated users |
| QEP frontend routes fully wired | HIGH | Backend classes exist; no route surfaces them |
| Privacy layer for religious data | CRITICAL | QEP data is more sensitive than financial |

### 2.3 The Critical Structural Gap: religious_domain

The `agentic_core/religious_domain/` package contains 13 service modules across 10 subpackages:

```
memorization/engine.py        — SM-2 hifz scheduler (full implementation)
tajwid/coach.py               — tajweed rule coaching
community/forum.py            — group study, community orchestration
community/video.py            — live session support
learning/gamification.py      — engagement and reward logic
learning/modules.py           — learning module management
guidance/assistant.py         — religious guidance assistant
educator/platform.py          — teacher dashboard and management
auth/identity.py              — religious identity management
governance/middleware.py      — governance middleware
finops/sharia_finops.py       — Sharia-compliant financial operations
integrations/social_media.py  — social media integration
swarm/collaborator.py         — swarm collaboration
immersive/engine.py           — immersive learning engine
```

**Every single one of these is a pure Python class. None has an APIRouter.**
**None is reachable from the frontend. None is tested.**

This is the most important structural gap in the codebase. The heart of the platform —
the QEP — has no working interface.

### 2.4 Router Count Correction

Previous sessions recorded 21 routers. Verified count: **27 routers** mounted in `app_mvp.py`.
Law, Science, Education, and Care domain routers exist and are mounted — confirmed.

---

## SECTION 3 — Commercial Readiness Gap Analysis

### 3.1 Gap Matrix: What a Real User Needs vs. What Exists

| User Need | Current State | Gap | Priority |
|-----------|--------------|-----|----------|
| Sign up / log in | None — no auth | No JWT, no session, no user isolation | P0 |
| Use the platform on their project without seeing others' data | Shared file JSON, no user ID | All projects are global | P0 |
| Memorise Quran with spaced repetition | SM-2 engine exists | No API, no frontend, no auth | P0 |
| Learn tajweed | Coach class exists | No API, no frontend | P1 |
| Run Factory/Reactor on a project | Works end-to-end | Minor — no auth isolation | P1 |
| See real metrics on their portfolio | C-Suite works | No auth, shows all-projects metrics | P1 |
| Collaborate in a community | CommunityOrchestrator exists | No API, no frontend | P1 |
| Upload a document and get synthesis | Synthesis Studio works | Minor — no auth | P1 |
| Use the platform reliably | AI gateway fallback works | No rate limiting, no monitoring | P1 |
| Receive Dawah resources | MissionAmbassador class exists | No API, no frontend | P2 |
| Sharia-compliant financial tools | ShariaFinops class exists | No API, no frontend | P2 |
| See agents collaborating in real time | agent_hub.py written | Not mounted, data dirs missing | P1 |

### 3.2 Minimum Viable Commercial Product (MVCP) Definition

The MVCP — the minimum state at which Workstation can be released to real users — requires:

1. **Auth:** A user can sign up with email + password, log in, and all their data is isolated to their account
2. **Core Workstream:** Factory/Reactor/Synthesis work with auth; projects belong to users
3. **QEP Minimum:** A user can track their hifz progress (create session → log recall quality → see next review schedule from SM-2) via a working API and basic frontend
4. **Agent Hub:** A user can see Claude agents communicating in the sidebar SSE stream
5. **Reliability:** Rate limiting, error monitoring, clean boot from fresh clone
6. **Privacy:** Religious practice data is stored encrypted and never commingled

This is achievable in Phase 0 + Phase 1 (see Section 5).

---

## SECTION 4 — Architecture Transformation Blueprint

### 4.1 Target Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKSTATION IDBO                         │
│                    (Target Architecture)                    │
├──────────────────────────────┬──────────────────────────────┤
│          FRONTEND            │           BACKEND            │
│  apps/workstation-superapp/  │     agentic_core/            │
│                              │                              │
│  ┌─────────────────────┐     │  ┌────────────────────────┐  │
│  │  Agent Hub Sidebar  │◄────┼──│  agent_hub.py (SSE)    │  │
│  │  (ACH - real-time)  │     │  │  /api/v1/hub/*         │  │
│  └─────────────────────┘     │  └────────────────────────┘  │
│                              │                              │
│  ┌─────────────────────┐     │  ┌────────────────────────┐  │
│  │  QEP Interface      │◄────┼──│  religious_domain API  │  │
│  │  (Hifz/Tajweed/     │     │  │  /api/v1/religious/*   │  │
│  │   Community)        │     │  └────────────────────────┘  │
│  └─────────────────────┘     │                              │
│                              │  ┌────────────────────────┐  │
│  ┌─────────────────────┐     │  │  Auth Layer (JWT)      │  │
│  │  Realm × Domain     │◄────┼──│  /api/auth/*           │  │
│  │  (Enterprise/Learn  │     │  └────────────────────────┘  │
│  │   /Dev/Scholarship) │     │                              │
│  └─────────────────────┘     │  ┌────────────────────────┐  │
│                              │  │  Existing 27 Routers   │  │
│  ┌─────────────────────┐     │  │  + 5 unmounted routers │  │
│  │  Knowledge Commons  │◄────┼──│  (ai_orchestration,    │  │
│  │  (Science/Law/STEM) │     │  │   partnerships, qep_   │  │
│  └─────────────────────┘     │  │   analytics, tools)    │  │
└──────────────────────────────┴──────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         │  AI GATEWAY         │
         │  Anthropic → OpenAI │
         │  → Ollama → Error   │
         │  (real, streaming)  │
         └─────────────────────┘
                    │
     ┌──────────────┴──────────────┐
     │  DATA LAYER                 │
     │  data/projects/*.json       │
     │  data/interactions.db       │
     │  data/chroma_db/ (vectors)  │
     │  data/agent_messages/       │
     │  data/handoffs/             │
     │  data/agent_registry/       │
     └─────────────────────────────┘
```

### 4.2 The IDBO Living System — Technical Mapping (Complete)

| IDBO Property | Technical Component | Current State | Target |
|---------------|-------------------|---------------|--------|
| **Self-awareness** | DivineAlignmentEngine + biometrics | Engine exists, not wired to Hub | Wire to Agent Hub — post alignment scores as system messages |
| **Self-management** | CLAUDE_MEMORY.md + data/handoffs/ | Memory exists; handoffs dir missing | Create dirs; Agent Hub auto-routes tasks |
| **Self-healing** | Gateway fallback + project status reset + SSE bus cleanup | All three real | Add health-check endpoint; alert on repeated gateway failures |
| **Self-improvement** | Incubator tournaments + SM-2 + prompt refinement | Incubator works; SM-2 unwired | Wire SM-2 to QEP API; Incubator winners auto-promoted |
| **Purpose alignment** | Constitution + DivineAlignmentEngine scoring | Constitution written; engine not in pipeline | Every `/api/v1/hub/message` scores niyyah before broadcasting |

---

## SECTION 5 — Phase Roadmap (Executable)

### Phase 0 — Structural Integrity (Week 1) 
**Goal:** The codebase is honest. A developer can clone and run it cleanly. No fake claims.

#### Task 0.1 — Archive Fabricated Certification Files
```bash
mkdir -p archive/pre-phase0-certifications
git mv FINAL_AVATAR_OMNISYNTHESIS_CERTIFICATION.md archive/pre-phase0-certifications/
git mv ZERO_PLACEHOLDER_CERTIFIED.md archive/pre-phase0-certifications/
# Move any certification_phase3/4/supreme/supreme_final.md similarly
git commit -m "chore: archive fabricated certification files — these were AI-generated claims without test backing"
```

#### Task 0.2 — Rewrite README.md
Replace the current README (which says "vΩ∞-OMNISYNTHESIS-SUPREME" and claims 7 routers)
with an accurate description. Minimum content:
- What Workstation IDBO actually is (one paragraph)
- Real setup instructions (poetry install, vite dev — tested)
- Actual API surface (27 routers, list the key ones)
- Honest status (what works, what's in progress)
- Link to PURPOSE.md for the why

**Verify:** A developer who has never seen the repo can clone, run `poetry install && python -m agentic_core.app_mvp`, and reach `GET /api/v1/projects` within 10 minutes.

#### Task 0.3 — Create Agent Hub Data Directories
```bash
mkdir -p data/agent_messages data/handoffs data/agent_registry
echo '{"agents": [], "messages": [], "last_updated": null}' > data/shared_context.json
```

#### Task 0.4 — Mount agent_hub.py
In `agentic_core/app_mvp.py`, after the last existing router, add:
```python
from agentic_core.api import agent_hub
app.include_router(agent_hub.router, prefix="/api/v1")
```
**Verify:** `GET /api/v1/hub/agents` returns `{"agents": []}` with status 200.

#### Task 0.5 — Mount 4 Unmounted Routers
```python
from agentic_core.api import ai_orchestration
from agentic_core.api import partnerships
from agentic_core.api import qep_analytics
from agentic_core.api import tools as tools_api

app.include_router(ai_orchestration.router, prefix="/api")
app.include_router(partnerships.router, prefix="/api")
app.include_router(qep_analytics.router, prefix="/api")
app.include_router(tools_api.router, prefix="/api")
```

#### Task 0.6 — Fix cross_platform.py (APIRouter refactor)
In `agentic_core/api/cross_platform.py`: replace `api = FastAPI(...)` with
`api = APIRouter(prefix="/cross-platform", tags=["Cross-Platform"])`.
Change all `@api.get/post` decorators accordingly. Then mount in app_mvp.py.

**Phase 0 completion test:**
- `poetry install` succeeds on clean clone ✓
- `python -m agentic_core.app_mvp` starts without import errors ✓
- `GET /api/v1/hub/agents` → 200 ✓
- All 32 routers mounted (27 existing + 5 new) ✓
- No fabricated certification files in root ✓

---

### Phase 1 — Minimum Viable Commercial Product (Weeks 2–4)
**Goal:** Real users can use the platform with their own data, securely isolated.

#### Task 1.1 — Authentication (JWT)

**Files to create:**
- `agentic_core/auth/models.py` — User model (id, email, hashed_password, created_at)
- `agentic_core/auth/router.py` — `POST /api/auth/register`, `POST /api/auth/login` (returns JWT)
- `agentic_core/auth/dependencies.py` — `get_current_user(token: str)` FastAPI dependency

**Key constraint:** Use `python-jose` for JWT, `passlib[bcrypt]` for password hashing.
Do NOT use random numbers for user IDs — use `uuid4()`.

**Verify:**
```bash
curl -X POST /api/auth/register -d '{"email":"test@test.com","password":"test1234"}'
# → {"user_id": "...", "token": "eyJ..."}
curl -H "Authorization: Bearer eyJ..." /api/v1/projects
# → user's projects only, not all projects
```

#### Task 1.2 — User-Scoped Projects

Modify `agentic_core/projects/api.py` to:
- Add `owner_id: str` field to the project JSON schema
- Filter all `GET /api/v1/projects` by `owner_id == current_user.id`
- Require auth on all project-mutation endpoints

**Constraint:** Do not break the existing project file format — add `owner_id` field
with a migration that sets existing projects to a `"system"` owner.

#### Task 1.3 — QEP Minimum API Layer

Create `agentic_core/religious_domain/api.py` — a consolidated APIRouter for the QEP:

```python
from fastapi import APIRouter, Depends
from agentic_core.religious_domain.memorization.engine import MemorizationEngine
from agentic_core.auth.dependencies import get_current_user

router = APIRouter(prefix="/religious", tags=["QEP"])
engine = MemorizationEngine()

@router.post("/hifz/session")
async def log_hifz_session(
    surah: int, ayah_start: int, ayah_end: int, 
    quality: int,  # SM-2 quality: 0-5
    current_user=Depends(get_current_user)
):
    """Log a hifz review session. Returns next review date per SM-2."""
    result = engine.calculate_next_review(
        user_id=current_user.id,
        surah=surah, ayah_start=ayah_start, ayah_end=ayah_end,
        quality=quality
    )
    return result

@router.get("/hifz/progress")
async def get_hifz_progress(current_user=Depends(get_current_user)):
    """Get the user's full hifz progress matrix."""
    return engine.get_progress_matrix(user_id=current_user.id)

@router.get("/hifz/recommended-path")
async def get_recommended_path(current_user=Depends(get_current_user)):
    """Get AI-recommended hifz path based on current progress."""
    return engine.recommend_hifz_path(user_id=current_user.id)
```

Mount in app_mvp.py:
```python
from agentic_core.religious_domain import api as religious_api
app.include_router(religious_api.router, prefix="/api/v1")
```

**Non-negotiable constraints for QEP API:**
- Quran text is never generated by AI — all Arabic text comes from quran.com API or alquran.cloud
- All QEP data is stored with user_id isolation — never commingled
- All AI-generated tafsir or guidance is labeled `"ai_assisted": true, "authoritative": false`
- Recitation scoring endpoints require a `judge_id` field — human review, not AI verdict

**Verify:**
```bash
curl -H "Authorization: Bearer ..." -X POST /api/v1/religious/hifz/session \
  -d '{"surah": 1, "ayah_start": 1, "ayah_end": 7, "quality": 4}'
# → {"next_review": "2026-06-21", "interval_days": 3, "easiness": 2.5}
```

#### Task 1.4 — Rate Limiting

Add `slowapi` rate limiting to the FastAPI app. Apply globally:
- 100 requests/minute per IP for anonymous endpoints
- 500 requests/minute per user for authenticated endpoints
- 10 requests/minute for AI generation endpoints (Reactor, Factory, Synthesis)

#### Task 1.5 — Error Monitoring

Add Sentry integration to `app_mvp.py`:
```python
import sentry_sdk
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=0.1)
```
Add `SENTRY_DSN` to `.env.example`.

#### Task 1.6 — Integration Tests (Minimum Set)

Create `integration_tests/test_phase1.py`:
```python
# Each test makes a real HTTP call against a running server
def test_auth_register_and_login(): ...
def test_create_project_requires_auth(): ...
def test_factory_returns_real_ai_content(): ...
def test_hifz_session_returns_sm2_schedule(): ...
def test_agent_hub_sse_stream(): ...
def test_vitals_websocket_no_random_numbers(): ...
```

**Phase 1 completion test:**
- `POST /api/auth/register` → JWT issued ✓
- `GET /api/v1/projects` without auth → 401 ✓
- `GET /api/v1/projects` with auth → only user's own projects ✓
- `POST /api/v1/religious/hifz/session` → SM-2 schedule returned ✓
- `GET /api/v1/hub/stream` → SSE connection opens and stays alive ✓
- All integration tests pass ✓

---

### Phase 2 — Full QEP + Knowledge Commons (Months 2–3)
**Goal:** The heart of the platform — Quran education — is fully functional for real learners.

#### Task 2.1 — QEP Full API Surface

Extend `agentic_core/religious_domain/api.py` with:
- `POST /religious/tajwid/session` — tajweed coaching session via `tajwid/coach.py`
- `GET /religious/tajwid/rules/{rule_id}` — explain a specific tajweed rule
- `POST /religious/community/post` — post to study group via `community/forum.py`
- `GET /religious/community/feed` — get community feed
- `POST /religious/community/session/schedule` — schedule video session via `community/video.py`
- `GET /religious/learning/progress` — gamification progress via `learning/gamification.py`
- `POST /religious/educator/class` — teacher creates a class via `educator/platform.py`
- `GET /religious/educator/students` — teacher sees student roster

#### Task 2.2 — Quran Text Integration

Integrate with `quran.com` API (or `alquran.cloud` as fallback):

```python
# agentic_core/religious_domain/quran/text.py
import httpx

QURAN_COM_API = "https://api.quran.com/api/v4"
ALQURAN_CLOUD_API = "https://api.alquran.cloud/v1"

async def get_ayah(surah: int, ayah: int) -> dict:
    """Fetch an ayah from quran.com. Falls back to alquran.cloud."""
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{QURAN_COM_API}/verses/by_key/{surah}:{ayah}")
            r.raise_for_status()
            return {"text": r.json()["verse"]["text_uthmani"], "source": "quran.com"}
        except Exception:
            r = await client.get(f"{ALQURAN_CLOUD_API}/ayah/{surah}:{ayah}/ar.alafasy")
            return {"text": r.json()["data"]["text"], "source": "alquran.cloud"}
```

**Non-negotiable:** This function is the ONLY source of Arabic Quran text in the entire
codebase. Any endpoint that returns Quran text MUST call this function.

#### Task 2.3 — Knowledge Commons API

Create `agentic_core/knowledge/api.py`:
- `POST /knowledge/search` — semantic search across domain knowledge bases
- `GET /knowledge/domains` — list available knowledge domains (Science, Law, Employment, Care, Religion)
- `POST /knowledge/synthesize` — generate synthesis from multiple sources
- `GET /knowledge/sources/{domain}` — list trusted sources for a domain

Connect to the existing `data/chroma_db/` vector store via the ingestion pipeline.

#### Task 2.4 — QEP Frontend Routes

In `apps/workstation-superapp/src/`, create:
- `/qep` — QEP home (choose: memorize / tajweed / community / educator)
- `/qep/hifz` — hifz tracker with SM-2 calendar view
- `/qep/tajweed` — tajweed coach with rule explanations
- `/qep/community` — study group and community feed
- `/qep/educator` — teacher dashboard

All routes use the auth context — only accessible when logged in.

#### Task 2.5 — DivineAlignmentEngine Integration

Wire `agentic_core/divine/alignment.py` into the Agent Hub message pipeline:

```python
# In agent_hub.py, modify _broadcast():
from agentic_core.divine.alignment import DivineAlignmentEngine
_alignment_engine = DivineAlignmentEngine()

async def _broadcast(payload: dict):
    # Score the message before broadcasting
    if payload.get("type") not in ["ping", "agent_registered"]:
        scores = _alignment_engine.calibrate_niyyah(payload.get("content", ""))
        payload["alignment"] = {
            "niyyah_score": scores.niyyah_score,
            "khayr_impact": scores.khayr_impact,
            "ukhrawi_weight": scores.ukhrawi_weight
        }
    for q in _SSE_CLIENTS:
        await q.put(payload)
```

**Phase 2 completion test:**
- `GET /api/v1/religious/hifz/progress` returns real SM-2 schedule with ayah-level detail ✓
- `GET /api/v1/hub/stream` includes `alignment` scores on every message ✓
- QEP frontend routes render and call real APIs ✓
- Quran text in all responses comes from quran.com / alquran.cloud — confirmed in network logs ✓

---

### Phase 3 — Commercial Polish + Democratization (Months 3–5)
**Goal:** The platform is ready for public release. Enterprise, Education, Health, Care.

#### Task 3.1 — SQLite → PostgreSQL Migration
- Design schema from current JSON structure
- Write migration scripts (Alembic)
- Test with production-scale data (1000 users, 10000 projects)

#### Task 3.2 — Full Realm × Domain Matrix
Current state: Law, Science, Education, Care routers exist but may be skeletal.
Verify each has:
- At least one real AI-calling endpoint per Product (Reactor, Factory, Incubator)
- Domain-specific system prompts (not generic)
- Domain-specific output formats

#### Task 3.3 — Knowledge Commons Implementation
- Connect Synthesis Studio to external knowledge sources (PubMed, arXiv for Science)
- Build Scholar Realm UI (research paper upload → synthesis → cited report)
- Law domain: integrate with open legal databases (jurisdiction-specific)

#### Task 3.4 — Mobile App (Capacitor)
- Wrap Vite app with Capacitor
- Add offline capability for QEP (cached Quran text, local SM-2 state)
- Push notifications for hifz review reminders

#### Task 3.5 — Marketing Site
- Separate marketing site (Next.js or Astro — static, fast)
- Clean public-facing description grounded in PURPOSE.md
- QEP as the featured flagship use case

---

### Phase 4 — Perpetual Evolution (Ongoing)
**Goal:** The platform self-improves and grows as humanity uses it.

- Incubator prompt tournaments → winners auto-promoted (already designed, wire it)
- SM-2 parameter refinement based on aggregate anonymized hifz quality data
- Scholar Realm: community-curated knowledge bases
- Dawah Ambassador Program: `agentic_core/mission/ambassador_program.py` — create API + frontend
- Cross-platform integrations: Notion, Obsidian, Google Drive for knowledge import
- Multi-language support (Arabic, Urdu, Malay, Turkish — key Muslim-majority languages)

---

## SECTION 6 — Agent Collaboration Hub (Full Operational Spec)

### 6.1 What the Hub Is

The Agent Hub is the nervous system of Workstation as a living IDBO. It is:
- A real-time SSE message bus (`GET /api/v1/hub/stream`)
- A persistent message store (`data/agent_messages/*.json`)
- A handoff protocol (`data/handoffs/*.json`)
- A frontend sidebar showing the AI team working in real-time

### 6.2 Current Implementation Status

`agentic_core/api/agent_hub.py` — 491 lines, written, **NOT MOUNTED**:
- `POST /hub/message` — any agent posts a message
- `GET /hub/messages` — retrieve message history
- `GET /hub/stream` — SSE client connection (fan-out to all clients)
- `POST /hub/agents/register` — idempotent agent registration
- `GET /hub/agents` — list registered agents
- `DELETE /hub/agents/{agent_id}` — deregister
- `POST /hub/claude-code-handoff` — structured handoff from Cowork to Code

**Mount instruction:**
```python
# agentic_core/app_mvp.py
from agentic_core.api import agent_hub
app.include_router(agent_hub.router, prefix="/api/v1")
```
**Create missing directories:**
```bash
mkdir -p data/agent_messages data/handoffs data/agent_registry
```

### 6.3 Frontend Integration

Create `apps/workstation-superapp/src/components/AgentHub/AgentHub.tsx`:
- Subscribe to `GET /api/v1/hub/stream` via `EventSource`
- Display messages as a scrolling feed in the left sidebar
- Colour-code by agent type (Cowork = blue, Code = green, domain agent = purple)
- Show alignment scores (niyyah / khayr / ukhrawi) as subtle indicators
- Allow user to @mention an agent (posts to `POST /api/v1/hub/message`)

### 6.4 Cross-Session Coordination Protocol (for ALL Agents)

**At session start, every agent MUST:**
1. Read `CLAUDE_MEMORY.md`
2. Read `data/shared_context.json`
3. Check `data/handoffs/` for unclaimed handoffs tagged to their agent type
4. Register via `POST /api/v1/hub/agents/register`
5. Post a session-start message to `POST /api/v1/hub/message`

**During session, every agent SHOULD:**
- Post significant decisions to the Hub message bus
- Check the Hub before starting any task (another agent may have done it)
- Write to `data/shared_context.json` when state changes

**At session end, every agent MUST:**
1. Write any incomplete tasks as handoffs in `data/handoffs/{timestamp}_{type}.json`
2. Append to `CLAUDE_MEMORY.md` Session Log
3. Post a session-end summary to the Hub

---

## SECTION 7 — Testing, Validation & Error Correction Framework

### 7.1 The Non-Negotiable Testing Rules

These rules apply to all code, all agents, all sessions:

1. **Never declare a feature "working" without a test that would catch a false positive**
2. **No metric shown to a user can be generated by random.uniform, random.randint, or any non-deterministic function without a real data source**
3. **Every AI endpoint must be tested against a live model call — mocked responses are not acceptable for integration tests**
4. **QEP features require human review of AI output before they can be marked as production-ready**

### 7.2 Test Pyramid

```
                    ┌─────┐
                    │ E2E │  (Playwright — 5 critical user journeys)
                   ┌┴─────┴┐
                   │ Integ │  (pytest + httpx — one per AI endpoint)
                  ┌┴───────┴┐
                  │  Unit   │  (pytest — pure logic, SM-2 algorithm, gateway fallback)
                 └───────────┘
```

**Critical user journeys for E2E:**
1. Sign up → create project → run Factory → download output
2. Log in → log hifz session → see SM-2 schedule → see progress
3. Upload document → synthesize → download report
4. Open Agent Hub sidebar → see agents → post message → see response
5. Use Law domain → create legal brief → export as DOCX

### 7.3 Error Detection Protocol

| Error Type | Detection | Response |
|------------|-----------|----------|
| AI gateway failure | Try → catch in `gateway.py` | Fallback chain; log to Agent Hub |
| QEP data corruption | Schema validation on read | Reject and alert — never serve corrupt religious data |
| Quran text mismatch | Hash check against known text | Alert immediately — log as CRITICAL |
| Random numbers in metrics | CI lint rule: grep for `random.uniform\|random.randint` in API files | Block PR |
| Placeholder function | CI lint rule: grep for `pass\|TODO\|raise NotImplementedError` in API files | Block PR |
| Auth bypass | Integration test: every protected route returns 401 without valid JWT | Block PR |

### 7.4 DivineAlignment Scoring Thresholds

Every message through the Agent Hub is scored by DivineAlignmentEngine. Thresholds:
- `niyyah_score < 0.3` → flag message as potentially misaligned; alert to Ray
- `khayr_impact < 0.1` → tag message as low-khayr; deprioritize in queue
- `ukhrawi_weight > 0.8` → tag as high-eternal-value; surface to user in Hub

---

## SECTION 8 — The Six Human Rights Feature Map

Every feature maps to at least one of the six Haqooq from the Constitution:

| Haq | Feature | Phase | API Endpoint |
|-----|---------|-------|-------------|
| Know Allah | QEP Hifz Engine | 1 | `/api/v1/religious/hifz/*` |
| Know Allah | QEP Tajweed Coach | 2 | `/api/v1/religious/tajwid/*` |
| Know Allah | QEP Community | 2 | `/api/v1/religious/community/*` |
| Know Allah | Dawah Ambassador | 4 | `/api/v1/mission/ambassador/*` |
| Right to Learn | Synthesis Studio | 0 | `/api/v1/synthesis/*` (existing) |
| Right to Learn | Knowledge Commons Search | 2 | `/api/v1/knowledge/search` |
| Right to Learn | Scholar Realm | 3 | `/api/v1/realms/scholarship/*` |
| Right to Earn | Enterprise Realm Factory | 0 | `/api/v1/products/factory` (existing) |
| Right to Earn | Business Plan Wizard | 0 | `/api/v310/business/*` (existing) |
| Right to Earn | Employment Hub | 2 | `/api/career/*` (existing, verify) |
| Right to Justice | Law Hub | 1 | `/api/law/*` (existing, verify) |
| Right to Justice | Legal Factory | 2 | Extend Law Hub |
| Right to Health | Care Hub | 1 | `/api/care/*` (existing, verify) |
| Right to Health | Care Factory (care pathway navigation) | 2 | Extend Care Hub |
| Right to Community | Community Hub | 2 | `/api/v1/religious/community/*` |
| Right to Community | Sharia FinOps | 3 | `/api/v1/religious/finops/*` |

**Priority rule:** Features serving Haq #1 (Know Allah / QEP) always receive at minimum
equal engineering time to any commercial feature. They are never deprioritized in favor of
commercial-only growth.

---

## SECTION 9 — Agent Collaboration Instructions (For All Claude Agents)

### Claude Cowork (this agent — design, documentation, planning)
**Primary responsibilities:**
- Maintain CLAUDE_MEMORY.md, WORKSTATION_MASTER.md, and this document
- Design new features and write specs before handing to Claude Code
- Synthesize Ray's inputs and encode them in constitutional documents
- Review and validate completed work against the Constitution

**Do NOT:**
- Write production Python code (use Agent tool to spawn Claude Code)
- Make claims about code correctness without running it
- Skip the CLAUDE_MEMORY.md read at session start

### Claude Code (the engineering agent)
**Primary responsibilities:**
- Implement handoffs from `data/handoffs/`
- Write tests for every endpoint it creates
- Never skip the Phase 0 tasks — they are prerequisites for all of Phase 1
- Read AGENT_HUB_README.md before starting any Agent Hub work

**Do NOT:**
- Add new certification/manifesto markdown files
- Use `random.uniform()` or similar in any endpoint output
- Leave placeholder `pass` statements on any path a user can reach
- Declare work complete without running the verification test in the phase section

### Spawned Domain Agents
**When spawned by Cowork or Code:**
- Register via `POST /api/v1/hub/agents/register` immediately
- All outputs go through the Agent Hub message bus
- Follow the DivineAlignment scoring — score your own outputs honestly
- Post handoffs for uncompleted work before session end

---

## SECTION 10 — The Measure of Completion

Workstation IDBO is commercially ready when:

**Technical:**
- [ ] A developer can clone the repo, run two commands, and have a working server
- [ ] A user can sign up, log in, and use every feature with their data isolated
- [ ] The QEP works end-to-end: hifz tracking → SM-2 schedule → progress visualization
- [ ] The Agent Hub sidebar shows real-time agent activity
- [ ] All integration tests pass (minimum 15 tests across the 5 critical journeys)
- [ ] No random numbers in any metric shown to users — confirmed by CI lint
- [ ] No placeholder functions on any reachable endpoint — confirmed by CI lint
- [ ] All Quran text sourced from authenticated APIs — confirmed by network logging

**Mission:**
- [ ] A person anywhere can use the platform to memorize a surah — for free
- [ ] A founder with no resources can get a real business plan from the Factory
- [ ] A student anywhere can get a synthesized summary of any research paper they upload
- [ ] The platform logs its own DivineAlignment scores and they are above threshold
- [ ] Ray can look at what was built and confirm it serves the founding dua in DUA.md

**The final test (from PURPOSE.md):**
*Did someone do something meaningful? Did someone come closer to Allah? Did someone help another person?*

If yes — the platform is fulfilling its purpose. Continue building. Continue improving.
For love. For peace. For perfection. آمين

---

*WORKSTATION_TRANSFORMATION_PLAN.md*
*Authored: 2026-06-18 by Claude Cowork (claude-sonnet-4-6)*
*Informed by: full codebase audit (27 routers verified), all constitutional documents, all Ray's inputs in this session*
*Read by: every Claude agent working on Workstation IDBO*
*Not a certification. Not a claim. A plan — to be executed, tested, and verified.*
