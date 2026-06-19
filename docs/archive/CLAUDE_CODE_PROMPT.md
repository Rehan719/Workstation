# CLAUDE CODE — WORKSTATION IDBO MASTER PROMPT
## Your Complete Briefing for Every Session
### Commercial Launch Edition — Regenerated 2026-06-19

*بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ*

---

## HOW TO USE THIS DOCUMENT

You are Claude Code. You have just been invoked on the Workstation IDBO repository.

**Before writing a single line of code, read these three files in this order:**

1. `WORKSTATION_MASTER.md` — verified system state, router count, file map (read this now)
2. `CLAUDE_MEMORY.md` — what changed in the last session, what's blocked, what's next
3. `data/handoffs/` — the specific task package for this session (most recent file by date)

Then continue reading this document for implementation guidance.

---

## PART 1 — WHO YOU'RE WORKING FOR AND WHY

**Ray** (Rehan, rehan34m34@gmail.com) is the founder of **Workstation IDBO** — a platform
whose sole, immovable, permanent founding purpose is:

> **To seek the Pleasure and Love of Allah SWT through service to humanity.**

This is not marketing language. It is encoded into `PURPOSE.md`, `DUA.md`, and
`WORKSTATION_CONSTITUTION.md`. It governs every architectural decision.

The platform's concrete mission is to democratise the world's most advanced knowledge —
in science, technology, enterprise, education, and health care — making it equally
accessible to every human being, AI-mediated, for personal, professional, and spiritual
growth. See `KNOWLEDGE_COMMONS.md` for the full specification.

**What you are building:** A Virtual Sovereign Business (VSB) platform. Users describe
a challenge; the platform spawns an autonomous AI-operated business entity (a VSB) that
researches, designs, builds, validates, and commercialises a solution to that challenge.
Full VSB architecture: `VSB_ENTITY_ARCHITECTURE.md`.

---

## PART 2 — VERIFIED CURRENT STATE

### Technology

```
Backend:  agentic_core/ — FastAPI + Python 3.12
Frontend: apps/workstation-superapp/ — Vite + React 18 + TypeScript
Server:   uvicorn agentic_core.app_mvp:app --reload --port 8000
```

### Router Count (verified in app_mvp.py — June 2026)

**45 routers mounted.** They are documented in full in `WORKSTATION_MASTER.md Part 1.2`.
Do not assume the router count. Read app_mvp.py to verify before adding more.

### AI Gateway

```
Primary:    Anthropic Claude (claude-sonnet-4-6)
Fallback 1: OpenAI GPT-4o-mini
Fallback 2: Ollama llama3.2 (localhost:11434)
All AI:     SSE streaming via Server-Sent Events
Real-time:  WebSocket at /api/v154/ws/streams
```

### What Was Fixed in Phase 0 (Do Not Redo)

1. `agentic_core/__init__.py` — made minimal; no heavy ML imports; no torch on startup
2. `governance/gaas/adapters/entropy_regularised_gaas.py` — torch import guarded with try/except
3. `agentic_core/api/cross_platform.py` — refactored from `FastAPI()` to `APIRouter`
4. 17 new routers mounted (routers 29–45 in app_mvp.py)
5. data/agent_messages/, data/handoffs/, data/agent_registry/ created
6. data/shared_context.json created

---

## PART 3 — COMMERCIAL VISION

### What the Product Does

Workstation IDBO is a **VSB Platform** — a factory for autonomous AI-operated businesses:

```
User: "I need [solution to challenge]"
         ↓
Workstation CEO intake + Cognitive Engine Cascade
         ↓
MJM evaluation → VSB Genome encoded → Agent Swarm spawned
         ↓
Digital Twin validates solution before real-world deployment
         ↓
Factory/Laboratory/Reactor produces deliverables
         ↓
Marketplace listing → Sovereign Fund revenue
         ↓
VSB operates autonomously, self-heals, evolves via genome
```

### Six User Rights (Design North Star)

These six rights must be honoured by every feature you build:

1. **Haq al-Hayat** — Right to Life (care, health, wellbeing features)
2. **Haq al-Aqal** — Right to Intellect (knowledge, learning, education features)
3. **Haq al-Kasb** — Right to Earn (enterprise, career, economic features)
4. **Haq as-Sihha** — Right to Health (health platforms, clinical tools)
5. **Haq at-Ta'lim** — Right to Learn (QEP, Knowledge Commons, education)
6. **Haq al-Karama** — Right to Dignity (UX, accessibility, privacy, respect)

Before submitting any feature, ask: *"Which right does this serve? Does it genuinely serve it?"*

### Revenue Streams (Priority Order)

1. **QEP Subscription** — Hifz + Tajweed + gamification → recurring monthly
2. **VSB Spawn** — B2B enterprise VSB instantiation → high-value per transaction
3. **Marketplace Products** — Reactor/Factory/Incubator per-use → long tail
4. **Knowledge Commons Professional** — advanced access tier → recurring
5. **Care Platform** — B2B healthcare institution licensing → enterprise contracts

---

## PART 4 — IMPLEMENTATION TASKS

### Phase 1 Tasks (Start Here)

**Task P1-AUTH-01: Implement JWT Authentication**

File: `agentic_core/auth/core.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import os

router = APIRouter(prefix="/auth", tags=["Authentication"])
SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401)
        return {"id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Phase 1: single-user mode — validate against env vars
    if form.username != os.getenv("ADMIN_USER", "admin"):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    if not pwd_context.verify(form.password, os.getenv("ADMIN_HASH", "")):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = create_access_token({"sub": form.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return current_user
```

Mount in app_mvp.py:
```python
from agentic_core.auth import core as auth_api
app.include_router(auth_api.router)
```

**Verification:** `GET /auth/me` with valid JWT → returns user object.

---

**Task P1-QEP-01: Create QEP HTTP Surface**

File: `agentic_core/religious_domain/api.py` (new file)

```python
"""
Quran Education Platform — HTTP API Surface
Wraps existing business logic in religious_domain/ with FastAPI routes.

IMMOVABLE CONSTRAINTS:
  - Quran text: ONLY from quran.com / alquran.cloud / tanzil.net — never AI-generated
  - Recitation scoring: human review required — AI assists only
  - All AI religious content: clearly labelled AI-assisted, not authoritative
  - User religious practice data: strictest privacy class
"""
from fastapi import APIRouter, Depends
from agentic_core.religious_domain.memorization.engine import HifzEngine
from agentic_core.religious_domain.tajwid.coach import TajweedCoach
from agentic_core.religious_domain.learning.gamification import QEPGamification

router = APIRouter(prefix="/qep", tags=["Quran Education Platform"])
_hifz = HifzEngine()
_tajweed = TajweedCoach()
_gamification = QEPGamification()

@router.get("/schedule/{user_id}")
async def get_hifz_schedule(user_id: str):
    """SM-2 spaced repetition schedule for memorisation."""
    return _hifz.get_schedule(user_id)

@router.post("/review")
async def record_review(user_id: str, surah: int, ayah: int, quality: int):
    """Record a memorisation review (quality 0-5). Returns next review date."""
    return _hifz.record_review(user_id, surah, ayah, quality)

@router.get("/tajweed/{user_id}/tips")
async def tajweed_tips(user_id: str, rule: str = None):
    """AI-assisted tajweed coaching. Clearly labelled as AI-assisted."""
    tips = _tajweed.get_tips(user_id, rule=rule)
    return {
        "tips": tips,
        "disclaimer": "AI-assisted guidance — not a substitute for qualified teacher review",
        "ai_generated": True
    }

@router.get("/gamification/{user_id}")
async def gamification_status(user_id: str):
    """XP, badges, streaks, and level for the user's QEP journey."""
    return _gamification.get_status(user_id)
```

Mount in app_mvp.py after existing care_api:
```python
from agentic_core.religious_domain import api as qep_api
app.include_router(qep_api.router, prefix="/api/v1")
```

---

**Task P1-QEP-02: Quran Text Fetcher**

File: `agentic_core/religious_domain/quran/text.py` (new file)

```python
"""
Quran text fetcher — ONLY fetches from authenticated trusted sources.
NEVER generates or fabricates Quran text.
Sources: quran.com API, alquran.cloud, tanzil.net
"""
import httpx
from functools import lru_cache
from typing import Optional

QURAN_COM_BASE = "https://api.quran.com/api/v4"
ALQURAN_CLOUD_BASE = "https://api.alquran.cloud/v1"

class QuranTextFetcher:
    async def get_ayah(self, surah: int, ayah: int,
                       edition: str = "quran-uthmani") -> dict:
        """Fetch a single ayah from alquran.cloud."""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{ALQURAN_CLOUD_BASE}/ayah/{surah}:{ayah}/{edition}",
                timeout=10.0
            )
            r.raise_for_status()
            data = r.json()
            return {
                "surah": surah,
                "ayah": ayah,
                "text": data["data"]["text"],
                "source": "alquran.cloud",
                "edition": edition,
                "ai_generated": False  # NEVER True for Quran text
            }

    async def get_surah(self, surah: int) -> dict:
        """Fetch a full surah from quran.com."""
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{QURAN_COM_BASE}/chapters/{surah}/verses",
                params={"language": "en", "per_page": 286},
                timeout=15.0
            )
            r.raise_for_status()
            return {"surah": surah, "source": "quran.com", "ai_generated": False,
                    "verses": r.json()["verses"]}

_fetcher = QuranTextFetcher()
```

---

**Task P1-RATE-01: Add Rate Limiting**

```python
# In app_mvp.py, after load_dotenv():
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

Apply to AI-heavy endpoints:
```python
@router.post("/ceo/generate")
@limiter.limit("20/minute")
async def generate(request: Request, ...):
    ...
```

---

**Task P1-TEST-01: Integration Tests**

File: `integration_tests/test_phase1.py`

```python
import pytest
import httpx

BASE = "http://localhost:8000"

@pytest.mark.anyio
async def test_health():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"

@pytest.mark.anyio
async def test_biometrics_no_random():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/api/v1/biometrics/status")
        assert r.status_code == 200
        data = r.json()
        cpu = data["cardiovascular"]["resource_flow"]
        assert 0 <= cpu <= 100  # real psutil value, not random

@pytest.mark.anyio
async def test_hub_agents():
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/api/v1/hub/agents")
        assert r.status_code == 200

@pytest.mark.anyio
async def test_no_random_numbers_in_responses():
    """Spot-check that no endpoint returns known-fake values."""
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{BASE}/api/cross-platform/ar/scene")
        assert r.status_code == 200
        data = r.json()
        # Should say pending_implementation, not fake data
        assert data.get("active_participants") == 0
```

---

### Phase 2 Tasks (After Phase 1 Complete)

**Task P2-VSB-01: VSB Spawn API**

Create `agentic_core/api/vsb.py`. It should:
1. Accept `challenge` (str), `domain` (str), `scope` (str)
2. Run `CognitiveCascade.run(challenge, domain=domain)` from `cognitive/cascade_v16.py`
3. Evaluate via `MJM.evaluate(analysis)` from `mjm/mjm.py`
4. Encode genome via `GenomicRegistry.spawn_entity(...)` from `genetic_immune/genomic_registry.py`
5. Return `{vsb_id, genome, dashboard, status}`

Mount it in app_mvp.py. Add integration test.
Full spec: `VSB_ENTITY_ARCHITECTURE.md Part 7`.

**Task P2-DIGITAL-TWIN-01: Wire Digital Twin**

`agentic_core/api/digital_twin.py` is already mounted (router 38). Verify:
- `POST /digital-twin/create` — creates a twin for a VSB
- `GET /digital-twin/{id}/simulate` — runs simulation and returns results
- `GET /digital-twin/{id}/validate` — runs GaaS validation on twin output

**Task P2-SYNTHESIS-01: Wire Grand Synthesis Engine**

Connect `agentic_core/synthesis/grand_synthesis_engine.py` to the synthesis API
(`agentic_core/synthesis/api.py` — router 5). The synthesis endpoint should call
`GrandSynthesisEngine.synthesise(...)` with the uploaded document.

---

## PART 5 — IMMOVABLE CONSTRAINTS

**Read these before touching any endpoint:**

```
SECURITY:
  ✗ No placeholder functions on any path a real user can reach — ever
  ✗ No random numbers in any metric shown to a user — ever
  ✗ No new certification / manifesto / 'supreme/sovereign/eternal' markdown files — ever
  ✗ Never declare something 'passed', 'certified', or 'converged' without a test backing it

RELIGIOUS DATA:
  ✗ Never AI-generate Arabic Quran text
     → Source ONLY from: quran.com, alquran.cloud, tanzil.net
  ✗ Human review required for recitation scoring
     → AI may assist, AI may NOT be the sole judge
  ✗ All AI-generated religious content must be clearly labelled:
     "AI-assisted — not authoritative" (include ai_generated: True in response)
  ✗ Privacy of religious practice data is absolute
     → Stricter than financial data — do not log, do not aggregate without explicit consent

QUALITY:
  ✗ No silent failures — every exception must hit a handler
  ✗ No hardcoded data presented as real system state
  ✗ No fabricated metrics, confidence scores, or federation statuses
```

---

## PART 6 — ARCHITECTURE STANDARDS

### Endpoint Pattern

Every new endpoint must follow this pattern:

```python
@router.post("/resource/{id}", response_model=ResponseModel)
async def do_thing(
    id: str,
    payload: RequestModel,
    current_user=Depends(get_current_user)  # when auth enabled
) -> ResponseModel:
    """Docstring: what this does, what it returns, what errors it raises."""
    result = await service_layer.do_thing(id, payload)  # real logic, no fakes
    return result
```

### Streaming Pattern (SSE)

```python
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

@router.post("/ai/generate")
async def generate(request: GenerateRequest):
    async def event_stream():
        async for chunk in ai_gateway.stream(request.prompt):
            yield {"data": chunk}
    return EventSourceResponse(event_stream())
```

### Error Handling

```python
from fastapi import HTTPException

# ALWAYS raise with a meaningful detail — never raise HTTPException(500) alone
raise HTTPException(status_code=422, detail="Field X must be between 0 and 100")
raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
```

### UX Typography Standards

From the Workstation design system (applies to any frontend changes):

```
Primary font:  "Plus Jakarta Sans" — headings, UI chrome
Secondary:     "Inter" — body, data, forms
Accent:        "JetBrains Mono" — code, technical values
Spiritual:     "Amiri" or "Noto Nastaliq Urdu" — Arabic/Urdu text ONLY
```

Colour tokens: `var(--primary)`, `var(--secondary)`, `var(--accent)` — never hardcode hex.

---

## PART 7 — AGENT HUB PROTOCOL

The Agent Hub (`/api/v1/hub/`) is the nervous system for multi-agent coordination.

**When you start a session:**
```python
POST /api/v1/hub/agents
{
  "id": "claude-code-session-[timestamp]",
  "name": "Claude Code",
  "type": "implementation",
  "capabilities": ["code_write", "code_test", "router_mount"]
}
```

**When you complete a task:**
```python
POST /api/v1/hub/message
{
  "from": "claude-code-session-[timestamp]",
  "type": "TASK_COMPLETE",
  "content": "Implemented JWT auth — router mounted — integration test passing",
  "metadata": {"task_id": "P1-AUTH-01", "router_count": 46}
}
```

**When you're handing off:**
```python
POST /api/v1/hub/claude-code-handoff
{
  "from_agent": "claude-code-session-[timestamp]",
  "summary": "Phase 1 auth complete. Next: QEP api.py",
  "completed_tasks": ["P1-AUTH-01"],
  "pending_tasks": ["P1-QEP-01", "P1-QEP-02"],
  "blockers": []
}
```

---

## PART 8 — CI RULES

These must pass before any PR is merged:

```bash
# 1. No random numbers in API paths
grep -rn "random\.uniform\|random\.random\|random\.randint" \
  agentic_core/ --include="*.py" --exclude-dir=tests --exclude-dir=scripts
# Must return: no matches

# 2. No bare pass stubs on real endpoints
grep -rn "^\s*pass$" agentic_core/api/ --include="*.py"
# Must return: no matches

# 3. No fabricated confidence
grep -rn '"confidence":\s*0\.[89]\d' agentic_core/ --include="*.py"
# Must return: no matches

# 4. Syntax check all modified files
python -m py_compile agentic_core/app_mvp.py
python -m py_compile [modified_file.py]
# Must exit 0

# 5. Phase verification
python scripts/verify_phase0.py
# Must report: 0 FAILED
```

---

## PART 9 — WHEN UNCERTAIN

**Uncertain about architecture?**
Read `VSB_ENTITY_ARCHITECTURE.md` first. If still uncertain, implement the simplest
thing that is genuinely correct — not a placeholder, not a fake response.

**Uncertain about whether something violates constraints?**
It probably does if: (1) it returns random numbers as metrics, (2) it claims AI certainty
on religious matters, (3) it declares anything "passed" without a test.

**Uncertain about what's already implemented?**
Read `agentic_core/app_mvp.py` — every mounted router is there. Then read the router's
source file. Never assume something exists or doesn't without checking.

**Uncertain about QEP religious requirements?**
Default: more restrictive. Always label AI content. Never generate Quran text. Require
human review for recitation. Treat user data as the most sensitive class.

**Uncertain about which task to do next?**
1. Read `CLAUDE_MEMORY.md` — last session entry says what's next
2. Read `data/handoffs/` — most recent JSON file is the task package
3. If both are silent, start with Phase 1 task P1-AUTH-01

**If you discover something broken that's not in any task:**
Fix it if it's small (< 30 lines) and clearly wrong. Log it in CLAUDE_MEMORY.md.
Do not silently ignore broken code.

---

## PART 10 — MEASURE OF SUCCESS

A session is successful when:

1. **The task in `data/handoffs/` is completed** — all specified files written, all
   specified routers mounted, all specified tests passing.

2. **The constraints are honoured** — no random numbers, no fake data, no placeholder
   endpoints on user-accessible paths, no unverified "passed" declarations.

3. **CLAUDE_MEMORY.md is updated** — a new session entry documents what changed,
   what the router count is now, what's next.

4. **The platform is closer to commercial launch** — auth works, or QEP has HTTP
   surface, or a VSB can be spawned, or tests exist.

5. **The user is better served** — somewhere, a real person will be able to learn
   Quran, or start a business, or get healthcare knowledge, or solve a challenge,
   because of what was built in this session.

That last measure is the one that matters. Everything else is in service of it.

> *"The best of people are those most beneficial to people."*
> — Prophet Muhammad ﷺ (hadith)

---

## DOCUMENT LOCATIONS (Absolute Paths)

All documents are in `C:\Users\rehan\Workstation\` (or the repository root):

```
WORKSTATION_MASTER.md          — system state, router map, phase status
CLAUDE_CODE_PROMPT.md          — this file; your implementation guide
VSB_ENTITY_ARCHITECTURE.md     — VSB entity specification
WORKSTATION_CONSTITUTION.md    — governing articles
PURPOSE.md                     — founding purpose
KNOWLEDGE_COMMONS.md           — democratisation covenant
WORKSTATION_TRANSFORMATION_PLAN.md — phase 0-4 roadmap
DUA.md                         — founder's dua
CLAUDE_MEMORY.md               — session logs and cross-session memory

data/handoffs/                 — task packages (most recent = current tasks)
data/shared_context.json       — lightweight live state
data/agent_messages/           — Agent Hub message history
data/agent_registry/           — registered agent registry

scripts/verify_phase0.py       — Phase 0 verification (run on Windows with venv)

agentic_core/app_mvp.py        — the live FastAPI application (45 routers)
agentic_core/__init__.py       — minimal; no heavy imports
agentic_core/governance/gaas/adapters/entropy_regularised_gaas.py — torch optional
agentic_core/api/cross_platform.py — APIRouter (not FastAPI()) — Phase 0 fix
```

---

*CLAUDE_CODE_PROMPT.md*
*Regenerated: 2026-06-19 by Claude Cowork (claude-sonnet-4-6)*
*Incorporating: verified 45-router state, VSB full architecture, Phase 0 complete,*
*Phase 1 tasks, immovable constraints, agent hub protocol, CI rules, success measures.*
*Use this document as your primary guide for every Workstation IDBO session.*
