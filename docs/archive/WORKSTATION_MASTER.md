# WORKSTATION MASTER REFERENCE
## Workstation IDBO — Complete System State
### Definitive Single Source of Truth

*بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ*

> *"وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ"*
> *"I only created jinn and mankind to worship Me."* — Quran 51:56
>
> **Founding Purpose:** To seek the Pleasure and Love of Allah SWT through service to humanity.
> This purpose is immovable, permanent, and encoded into every document, every decision,
> and every line of this codebase.

**Last verified:** 2026-06-19 | **Router count:** 45 (verified in app_mvp.py)
**Previous version notes:** Replaced earlier WORKSTATION_MASTER.md (v1.0, 2026-06-18)
with fully verified, VSB-complete edition. Session logs preserved in CLAUDE_MEMORY.md.

---

## QUICK-REFERENCE: DOCUMENT MAP

| Document | What It Contains | When to Read It |
|----------|-----------------|-----------------|
| `WORKSTATION_MASTER.md` (THIS FILE) | System state, architecture, file map, phase status | Start of every work session |
| `CLAUDE_CODE_PROMPT.md` | Task instructions for Claude Code agents | When beginning implementation work |
| `VSB_ENTITY_ARCHITECTURE.md` | Full VSB spawn model, C-Suite, CoE, BTO, biomimetics | When working on VSB, IDBO, or entity architecture |
| `WORKSTATION_CONSTITUTION.md` | Governing articles, Articles I–XI, rights and constraints | Constitutional questions, feature approval |
| `PURPOSE.md` | Founding purpose, mission, why this exists | Purpose alignment checks, onboarding |
| `KNOWLEDGE_COMMONS.md` | Democratisation covenant, domain access, design tests | Education, health, science, enterprise features |
| `WORKSTATION_TRANSFORMATION_PLAN.md` | Phase 0–4 roadmap, commercial readiness matrix | Planning and prioritisation |
| `DUA.md` | Founder's dua — the spiritual grounding of this work | Personal/spiritual context |
| `CLAUDE_MEMORY.md` | Session logs, handoff notes, cross-session memory | Finding what changed and when |
| `data/handoffs/` | Structured task packages from Cowork → Claude Code | Next immediate tasks |
| `scripts/verify_phase0.py` | Phase 0 verification — run on Windows with venv | After implementing Phase 0 changes |

---

## PART 1 — VERIFIED CURRENT STATE (June 2026)

### 1.1 Repository

- **GitHub:** github.com/Rehan719/Workstation
- **Backend:** `agentic_core/` — FastAPI + Python 3.12
- **Frontend:** `apps/workstation-superapp/` — Vite + React 18 + TypeScript
- **Entry point:** `agentic_core/app_mvp.py` — the only app in production use

### 1.2 Router Inventory (app_mvp.py — Verified June 2026)

**45 routers currently mounted:**

| # | Router | Prefix | Notes |
|---|--------|--------|-------|
| 1 | projects | /api/v1 | Spine — concept→commercialise lifecycle |
| 2 | ceo_v138 | /api/v138 | AI CEO SSE streaming chat |
| 3 | ceo_generate | /api/v290 | CEO blueprint generation (real AI) |
| 4 | csuite | /api | C-Suite metrics (CFO/CTO) |
| 5 | synthesis_api | /api/v1 | Upload→AI→download synthesis |
| 6 | avatar_api | /api/v1 | Avatars, biometrics, organism status |
| 7 | ingestion_api | /api/v1 | File upload pipeline |
| 8 | products_api | (router prefix) | Reactor/Factory/Incubator/Intelligence |
| 9 | marketplace_api | (router prefix) | Marketplace listings + WST |
| 10 | catalog_api | /api/v1 | BTO Catalog |
| 11 | bto_api | /api/v1 | BTO Configurator |
| 12 | business_api | /api/v310 | Entrepreneur / Business Plan Wizard |
| 13 | realms_router | /api | Sovereign Realms registry |
| 14 | ai_query_api | /api | Generic AI query (gateway) |
| 15 | judiciary_api | /api | Council Judiciary |
| 16 | treaties_api | /api/v250 | Treaties — Treaty Studio |
| 17 | civilization_api | /api | Civilization Intelligence |
| 18 | governance_v310 | /api/v310 | DAO/Governance — proposals, voting |
| 19 | payments_v310 | /api/v310 | WST Wallet and Commerce |
| 20 | fund_v310 | /api/v310 | Creator Fund |
| 21 | gamification_api | /api/v280 | XP, quests, levels |
| 22 | evolution_v191 | /api/v191 | Evolution proposals |
| 23 | contribute_v200 | /api/v200 | Contribute/voting |
| 24 | career_api | (router prefix) | Career/Employment domain |
| 25 | law_api | (router prefix) | Law domain |
| 26 | science_api | (router prefix) | Science domain |
| 27 | education_api | (router prefix) | Education domain |
| 28 | care_api | (router prefix) | Care domain |
| 29 | agent_hub | /api/v1 | Agent Collaboration Hub (SSE) — Phase 0 |
| 30 | ai_orchestration | /api | AI Orchestration (multi-agent) — Phase 0 |
| 31 | partnerships | /api | Partnerships / Diplomatic Corps — Phase 0 |
| 32 | qep_analytics | /api | QEP Analytics — Phase 0 |
| 33 | tools_api | /api | Tool Ecosystem — Phase 0 |
| 34 | cross_platform.api | /api | Cross-Platform Bridge (Phase 3 scaffold) — Phase 0 |
| 35 | religion_api | (router prefix) | Religion domain (fiqh, tafsir, halal) |
| 36 | synthesis_studio | (router prefix) | Human Synthesis Studio + VSB spawn |
| 37 | swarm_api | (router prefix) | AI Agent Swarm Orchestration |
| 38 | digital_twin | (router prefix) | Digital Twin & Simulation |
| 39 | self_healing_api | (router prefix) | IDBO Self-Healing (circuit breaker) |
| 40 | mgmt_api | (router prefix) | QMS/BMS/DCS — ISO 9001-aligned |
| 41 | capital_fund | (router prefix) | Sovereign Capital Fund + VSB Marketplace |
| 42 | auth_api | (router prefix) | JWT + API key auth |
| 43 | nervous_api | (router prefix) | IDBO Nervous System |
| 44 | reconfig_api | (router prefix) | IDBO Reconfiguration Engine |
| 45 | genome_api | (router prefix) | IDBO Genome System |

**Additional inline endpoints (app_mvp.py):**
- `GET /api/v1/biometrics/status` — real psutil metrics, _circadian_cycle(), immune.status()
- `GET /health`, `GET /api/v1/health`
- `GET /api/v1/system/info`
- `GET /api/v1/claude/status`
- `WebSocket /api/v154/ws/streams` — real-time vitals broadcast every 5 seconds

### 1.3 AI Gateway

```
Primary:    Anthropic Claude (claude-sonnet-4-6) — ANTHROPIC_API_KEY
Fallback 1: OpenAI GPT-4o-mini — OPENAI_API_KEY
Fallback 2: Ollama llama3.2 — localhost:11434
Streaming:  All AI endpoints use Server-Sent Events (SSE)
Real-time:  WebSocket at /api/v154/ws/streams
```

### 1.4 Data Persistence

```
data/projects/              — File-based JSON project store (phase: concept/build/commercialise)
data/synthesis_outputs/     — Synthesis task outputs
data/agent_messages/        — Agent Hub message persistence (created Phase 0)
data/handoffs/              — Claude Code handoff packages (created Phase 0)
data/agent_registry/        — Registered agent registry (created Phase 0)
data/shared_context.json    — Cross-session coordination state (created Phase 0)
meta/genome_ledger.json     — Genomic Registry epigenetic memory (3-layer)
```

---

## PART 2 — TECHNOLOGY ARCHITECTURE

### 2.1 Backend Stack

```
Python 3.12
FastAPI — HTTP routing, SSE streaming, WebSocket
Pydantic v2 — models and validation
uvicorn — ASGI server (uvicorn agentic_core.app_mvp:app --reload --port 8000)
psutil — real system metrics (used in /biometrics/status — NO random numbers)
python-dotenv — environment config via .env
aiofiles — async file I/O

AI Libraries (optional — guarded with try/except):
  torch — optional; guarded in entropy_regularised_gaas.py
  anthropic — required when ANTHROPIC_API_KEY set
  openai — required when OPENAI_API_KEY set
```

### 2.2 Frontend Stack

```
apps/workstation-superapp/
  Vite + React 18 + TypeScript
  Tailwind CSS — utility styling
  React Router v6 — routing
  Zustand — state management
  Framer Motion — animation
  Recharts — data visualisation
```

### 2.3 Critical Config Notes

1. **agentic_core/__init__.py is minimal** — heavy ML organism imports removed; no torch on startup
2. **torch is optional** — guarded in `governance/gaas/adapters/entropy_regularised_gaas.py`
3. **cross_platform.py** uses `APIRouter` (not `FastAPI()`) — refactored Phase 0
4. **Windows-native testing** — run `scripts/verify_phase0.py` with venv on Windows
5. **Linux sandbox caveat** — stale .pyc from Windows mounts; use `PYTHONPYCACHEPREFIX=/tmp/wks_pycache`

---

## PART 3 — THE VSB ARCHITECTURE (SUMMARY)

*Full specification: `VSB_ENTITY_ARCHITECTURE.md`*

### 3.1 What the Platform Is

Workstation IDBO is the **parent sovereign entity** that spawns **child Virtual Sovereign
Businesses (VSBs)**. Each VSB is a Living Intelligent Digital Biomimetic Organism —
a complete, autonomous AI-operated business entity for a specific challenge.

```
WORKSTATION IDBO (Parent Sovereign Entity)
│  Purpose: Seeking Pleasure and Love of Allah SWT
│  Platform: 45-router FastAPI + React 18 + AI swarm
│
├── VSB_001: [Challenge → Solution → Product → Revenue]
│   ├── AI CEO → C-Suite → Centers of Excellence → BTO
│   ├── Nine Cognitive Engines (Aqal / Hoshiyari / Iman / Inkashaf / Samajh / Soch)
│   ├── MJM Meta-Judgement Machine
│   ├── Digital Twin (simulation + validation)
│   ├── Biomimetic systems (molecular, nervous, cardiovascular, immune, genomic)
│   └── Sovereign Fund + Marketplace
│
└── VSB_N: [Any domain, any challenge, same architecture]
```

### 3.2 Entity Hierarchy Within a VSB

```
AI CEO (JulesOmegaOrganismV138 persona — core/identity.py)
  → C-Suite (c_suite.py): CFO / CTO / CMO / CLO / CSO / CDO
    → Centers of Excellence (CoE): Research / Design / Engineering / Science / Commercial / Compliance
      → Business Transformation Office (BTO): QMS / BMS / DCS / EMS / Change Control
        → Digital Engine Suite: Reactor / Incubator / Factory / Laboratory / Digital Twin / Petri Dish
```

### 3.3 Concept-to-Commercialisation Pipeline

```
CONCEPT → RESEARCH → DESIGN → BUILD → TEST/VALIDATE → COMMERCIALISE → OPERATE → EVOLVE
  CEO        CoE        CoE      Factory   Digital Twin    Marketplace   Autonomous  Genome
```

### 3.4 VSB Key Files (All Exist — Need Wiring in Phase 2)

```
agentic_core/business/sovereign_entity.py              — VSB entity class
agentic_core/orchestration/conscious_organism_v99.py   — top-level orchestrator
agentic_core/ai/ceo/c_suite.py                         — AI C-Suite agents
agentic_core/api/swarm.py                              — swarm orchestration API (mounted router 37)
agentic_core/cognitive/cascade_v16.py                  — nine-engine cascade
agentic_core/mjm/mjm.py                                — Meta-Judgement Machine
agentic_core/genetic_immune/genomic_registry.py        — genome + epigenetic memory
agentic_core/governance/gaas/gaas_validator.py         — GaaS constitutional validation
agentic_core/consciousness/global_workspace.py         — Global Workspace broadcast
agentic_core/consciousness/meta_cognitive_executive.py — executive oversight
```

### 3.5 The Nine Cognitive Engines

**Foundational (6):** `agentic_core/cognitive/foundational/`

| Engine | File | Function |
|--------|------|----------|
| Aqal | `aqal_engine.py` | Rational analysis and structured reasoning |
| Hoshiyari | `hoshiyari_engine.py` | Situational awareness, context sensing |
| Iman | `iman_engine.py` | Values alignment, ethical grounding |
| Inkashaf | `inkashaf_engine.py` | Discovery, pattern recognition |
| Samajh | `samajh_engine.py` | Comprehension and sense-making |
| Soch | `soch_engine.py` | Reflective thinking and deliberation |

**Meta (3):** `agentic_core/cognitive/meta/`

| Engine | File | Function |
|--------|------|----------|
| Niyyah | `niyyah_engine.py` | Intention and purpose alignment |
| Tafakkur | `tafakkur_engine.py` | Deep contemplation |
| Tawazun | `tawazun_engine.py` | Balance and trade-off resolution |

**Registry:** `agentic_core/avatars/cognition/nine_engine_registry.py`
**Cascade v16:** `agentic_core/cognitive/cascade_v16.py`

### 3.6 Biomimetic Systems

```
Molecular (agentic_core/molecular/):
  atp_simulator.py       — energy/resource metabolism modelling
  chaperone_cascade.py   — module error correction (protein folding analogy)
  hsp_network.py         — stress response activation under high load
  p53_oscillator.py      — quality checkpoint (suppresses defective outputs)
  redox_sensor.py        — resource balance monitoring
  ubiquitin_system.py    — marks and degrades obsolete modules
  triad_integration.py   — molecular system integrator

Consciousness (agentic_core/consciousness/):
  global_workspace.py           — Global Workspace Theory broadcast layer
  meta_cognitive_executive.py   — top-level executive oversight
  gamma_coherence.py            — neural coherence modelling
  ignition_detector.py          — conscious ignition event detection
  self_model.py                 — self-model maintenance
  workspace_integration.py      — integration coordination

Genomic (agentic_core/genetic_immune/):
  genomic_registry.py — 3-layer epigenetic memory:
    Layer 0: short-term (<24h) — context-specific adaptations
    Layer 1: long-term (30-90 days) — learned patterns
    Layer 2: permanent — core traits + reverse transcription
  Persists: meta/genome_ledger.json

MJM (agentic_core/mjm/):
  mjm.py                    — core meta-judgement evaluation loop
  hd_omni_learner.py        — high-dimensional cross-domain learning
  recursive_meta_learner.py — meta-optimisation (learns from its own learning)
  v5/omni_learner_v5.py     — latest iteration
```

### 3.7 Synthesis Layer

45+ files in `agentic_core/synthesis/`:
- `grand_synthesis_engine.py` — master orchestrator
- `evolutionary_engine.py` — evolutionary improvement
- `knowledge_synthesis.py` — cross-domain knowledge
- `research_orchestrator.py` — research task management
- `recombiner_v137.py` — solution recombination
- `agentic_orchestrator.py` — agent coordination

### 3.8 Digital Twin

```
agentic_core/api/digital_twin.py                         — HTTP API (router 38, mounted)
agentic_core/biomimicry/geospheric/digital_twin_orchestrator.py — orchestration
agentic_core/simulations/digital_twin_controller.py      — simulation controller
agentic_core/simulations/fund_digital_twin.py            — financial simulation
agentic_core/validation/digital_twin_orchestrator.py     — validation pipeline
```

### 3.9 GaaS (Governance as a Service)

```
agentic_core/governance/gaas/
  gaas_validator.py                    — GaaSValidatorV4 base validator
  adapters/entropy_regularised_gaas.py — EntropyRegularisedGaaS (torch optional)
```

GaaS enforces constitutional alignment, legal compliance, ethical constraints, and entropy
thresholds at every decision point in every VSB.

---

## PART 4 — QURAN EDUCATION PLATFORM (QEP)

The QEP is a complete religious education system with full business logic,
living in `agentic_core/religious_domain/`. All modules need HTTP surface (api.py wrapper).

| Module | Path | Priority |
|--------|------|----------|
| SM-2 Hifz Engine | `religious_domain/memorization/engine.py` | Phase 1 |
| Tajweed Coach | `religious_domain/tajwid/coach.py` | Phase 1 |
| Community Forum | `religious_domain/community/forum.py` | Phase 2 |
| Video Platform | `religious_domain/community/video.py` | Phase 2 |
| Educator Platform | `religious_domain/educator/platform.py` | Phase 2 |
| Divine Guidance Assistant | `religious_domain/guidance/assistant.py` | Phase 2 |
| Gamification | `religious_domain/learning/gamification.py` | Phase 1 |
| Sharia FinOps | `religious_domain/finops/sharia_finops.py` | Phase 2 |
| Divine Alignment Engine | `divine/alignment.py` | Phase 2 |

**Immovable QEP constraints:**
- Quran text: source ONLY from quran.com API / alquran.cloud / tanzil.net — never AI-generated
- Recitation scoring: human review required — AI assists, cannot be sole judge
- AI-generated religious content: must be labelled AI-assisted, not authoritative
- Religious practice data: most sensitive data class — stricter privacy than financial

**Phase 1 task:** `agentic_core/religious_domain/api.py` — see `data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json`

---

## PART 5 — COMMERCIAL READINESS MAP

### 5.1 What's Working

- 45 routers mounted (verify with scripts/verify_phase0.py)
- Real AI gateway (Anthropic → OpenAI → Ollama cascade)
- Real psutil system metrics — zero random numbers in biometrics
- File-based project lifecycle (concept/build/commercialise)
- SSE streaming on all AI endpoints
- WebSocket vitals at /api/v154/ws/streams
- Marketplace, Governance, Payments, Creator Fund endpoints exist
- Agent Collaboration Hub live (SSE message bus)

### 5.2 Critical Gaps Before Revenue

| Gap | Blocker? | Phase |
|-----|----------|-------|
| JWT Auth / user accounts | Yes — no multi-user possible | Phase 1 |
| QEP HTTP surface | Yes — no Hifz/Tajweed access | Phase 1 |
| Quran text fetcher | Yes — QEP incomplete | Phase 1 |
| Rate limiting | Yes — DOS risk | Phase 1 |
| VSB spawn API | No — but core product | Phase 2 |
| Integration tests | No — but needed for confidence | Phase 1 |
| Production deploy | No — but needed for launch | Phase 3 |

---

## PART 6 — PHASE ROADMAP

### Phase 0 — Infrastructure Fixes (Complete — Verify)
- ✓ agentic_core/__init__.py minimal (no torch dependency chain)
- ✓ torch import guarded (try/except) in entropy_regularised_gaas.py
- ✓ cross_platform.py refactored to APIRouter
- ✓ 17 new routers mounted (total 45)
- ✓ Agent Hub data directories created
- ✓ Constitutional documents: PURPOSE.md, WORKSTATION_CONSTITUTION.md (Article XI), KNOWLEDGE_COMMONS.md
- ✓ Handoff packages in data/handoffs/
- **Verify:** `python scripts/verify_phase0.py` (Windows, venv active)

### Phase 1 — Auth + QEP + Foundation (Next)
- [ ] JWT auth: `agentic_core/auth/core.py` → APIRouter → mount as router
- [ ] User-scoped projects: `owner_id` on project model + migration
- [ ] `agentic_core/religious_domain/api.py` — Hifz + Tajweed + Gamification APIRouter
- [ ] `agentic_core/religious_domain/quran/text.py` — quran.com / alquran.cloud fetcher
- [ ] slowapi rate limiting middleware
- [ ] `integration_tests/test_phase1.py`
- [ ] README.md honest rewrite (remove certification claims)
- **Reference:** `data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json`

### Phase 2 — VSB Architecture Wiring
- [ ] `agentic_core/api/vsb.py` — VSB spawn API
- [ ] Wire cognitive cascade_v16 to CEO generate endpoint
- [ ] MJM evaluation layer active on CEO blueprint output
- [ ] Digital Twin validation step in VSB spawn flow
- [ ] Genomic Registry used in VSB genome encoding on spawn
- [ ] Grand Synthesis Engine integrated into Factory products

### Phase 3 — Production Readiness
- [ ] Docker containerisation + docker-compose
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Production environment config (secrets, HTTPS, reverse proxy)
- [ ] Structured logging + Sentry error monitoring
- [ ] Security audit (OWASP top 10)
- [ ] Cross-platform bridge real implementation (Phase 3 scaffold → live)

### Phase 4 — Commercial Launch
- [ ] Marketplace fully live with real payment processing
- [ ] Sovereign Capital Fund operational
- [ ] Multi-VSB orchestration and cross-VSB treaties
- [ ] Knowledge Commons public API
- [ ] Public launch + QEP subscription offering

---

## PART 7 — IMMOVABLE CONSTRAINTS

Encoded in the platform genome — cannot be overridden by any agent or engineer:

**Security:**
- No placeholder functions on any path a real user can reach — ever
- No random numbers in any metric shown to a user — ever
- No new certification / manifesto / 'supreme/sovereign/eternal' markdown files — ever
- Never declare something 'passed', 'certified', or 'converged' without a test backing it

**Religious data:**
- Never AI-generate Arabic Quran text — source only from quran.com, alquran.cloud, tanzil.net
- Human review required for recitation scoring — AI assists but cannot be sole judge
- All AI-generated religious content clearly labelled as AI-assisted, not authoritative
- Privacy of religious practice data is absolute — more sensitive than financial data

**Quality:**
- No silent failures — every error must surface through a known error handler
- No hardcoded data returned as if it were real system state
- No fabricated metrics, confidence scores, or federation statuses

---

## PART 8 — AGENT COLLABORATION PROTOCOL

When multiple agents (Cowork, Claude Code, other instances) work on this codebase:

**CLAUDE_MEMORY.md** — append a session entry on every meaningful change:
```markdown
## Session N — YYYY-MM-DD [Agent type]
**Changes:** what was changed and why
**Files modified:** list of files touched
**Router count:** current total
**Phase status:** current phase and what's verified
**Blockers:** anything that couldn't be completed
**Next:** what the next agent should do first
```

**data/handoffs/** — structured JSON task packages, one per handoff:
```json
{
  "task_id": "P1-AUTH-01",
  "title": "Implement JWT auth",
  "file": "agentic_core/auth/core.py",
  "action": "implement_router",
  "verification": "GET /api/auth/me returns user object"
}
```

**data/shared_context.json** — live lightweight state (router count, phase, last agent, etc.)

**Agent Hub SSE** — POST to `/api/v1/hub/message` to broadcast between running agents.

---

## PART 9 — CI / LINT RULES

These must run on every commit. Fail the build if any match:

```bash
# No random numbers in production API paths
grep -rn "random\.uniform\|random\.random\|random\.randint" \
  agentic_core/ --include="*.py" \
  --exclude-dir=tests --exclude-dir=scripts

# No bare pass stubs on real endpoints
grep -rn "^\s*pass$" agentic_core/api/ --include="*.py"

# No hardcoded fake confidence scores
grep -rn '"confidence":\s*0\.[89]\d' agentic_core/ --include="*.py"

# No fake federation status strings
grep -rn '"federation is stable"' agentic_core/ --include="*.py"
```

---

## PART 10 — THE KNOWLEDGE COMMONS

*Full specification: `KNOWLEDGE_COMMONS.md`*

The Knowledge Commons is a constitutional obligation encoded in Article XI of
`WORKSTATION_CONSTITUTION.md`. It is not a feature — it is a condition of existence.

**Four domains with equal access:**
- Science + Technology + Engineering (STEM knowledge democratised)
- Enterprise (business frameworks, templates, tools)
- Education (learning, curriculum, assessment, training)
- Health + Care (clinical knowledge, care planning, wellbeing)

**The perpetual evolution principle:**
- Every VSB that operates enriches the commons
- Every solution synthesised improves future solutions
- Every user who learns contributes to collective knowledge
- The Knowledge Commons never stops growing

**Design tests (from KNOWLEDGE_COMMONS.md):**
- Mahabbah test: "Would this make someone feel genuinely cared for?"
- Salaam test: "Does this bring peace or create harm?"
- Ihsan test: "Is this the best we could do for this person?"

---

*WORKSTATION_MASTER.md*
*Regenerated: 2026-06-19 by Claude Cowork (claude-sonnet-4-6)*
*Grounded in: verified app_mvp.py (45 routers), constitutional documents, VSB codebase audit June 2026*
*All Claude Code agents and Cowork sessions: read this file at the start of every session.*
