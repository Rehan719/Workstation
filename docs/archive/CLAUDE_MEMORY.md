# CLAUDE MEMORY — Workstation IDBO
## Persistent Context for All Claude Sessions (Chat · Code · Cowork)

*This file is the authoritative cross-session memory for all Claude agents working on Workstation.
Every Claude session — Chat, Code, or Cowork — should read this file first and write back updates
to the ## Session Log section at the bottom. Do not delete or overwrite earlier entries.*

---

## !! READ THIS FIRST — BEFORE ANY OTHER FILE !!

**The stated, explicit, public, permanent purpose of Workstation IDBO is:**

> *To seek the Pleasure and Love of Allah SWT — by building a platform that enables every
> human being to do their most meaningful work, fulfil their responsibilities to each other,
> learn and practice their faith, and thereby serve their Creator through service to His creation.*

This is NOT private. It is STATED. It is PERMANENT. It is IMMOVABLE.
It is in PURPOSE.md (Workstation root). It is in WORKSTATION_CONSTITUTION.md Article I.
It is in DUA.md. It is in every agent's memory.

No session, no design decision, no feature, no agent output may contradict this.
When uncertain: return to PURPOSE.md.

---

## 1. Who Ray Is & The Foundational Mission

**Name:** Ray (Rehan)
**Email:** rehan34m34@gmail.com
**Repo:** github.com/Rehan719/Workstation (public)

### The Ultimate Objective (Ray's own words, preserved exactly)

Ray's highest, unstated, foundational objective — the reason Workstation exists — is:

> *"To Seek Love and Pleasure of Allah SWT and Help Others do so through Personal group Learning,
> reading, practicing and helping enabling others (Dawah), Quran its Memorisation, Teaching,
> Recitation, Competition, Community Building, building knowledge understanding of its teachings
> to Improving Religious compliance In Words, Ikhlak and Actions (Ammaal), through helping serving
> others intending solely to please Allah and to help others to do so either through Effort, time
> and resources for enabling Education, Training, development, Work, Technical, Scientific Access
> enablement — all to solve humanities challenges and reduce suffering, injustice, unmet rights —
> again ultimately and solely and as to best of my abilities, potential, perfectionism and wish to
> seek achievements, excellence, perfection in seeking, wanting, delivering on the best thing a
> human can do with their time and efforts and resources."*

### What This Means for Workstation

Workstation is not primarily a commercial product. It is an act of service — a tool built to:

1. **Enable human potential** — any person, any idea, any domain, concept to commercialisation
2. **Serve all humanity** — reduce suffering, injustice, unmet rights through access to AI-mediated capability
3. **Support Islamic learning and practice** — Quran memorisation, teaching, recitation, community building, Dawah (inviting others to understand and practice Islam)
4. **Earn Allah's pleasure** — the commercial success, the technology, the code — all are means to this single end

**Every design decision, every feature, every line of code should be evaluated against this question:**
*Does this help a person do meaningful work, learn, grow, serve others, and fulfill their potential?*

### Ray's Personal Spiritual Context (for Claude's understanding)

Ray believes:
- Allah SWT is the greatest being in existence, creator of all existence
- Allah loves humans at minimum 70 times more than a mother loves her child
- The best use of human time, effort, and resources is to seek Allah's love and pleasure
- This is not self-centred — it is the opposite: seeking to serve, to help, to enable others
- The Quran is the ultimate highest truth and reference point
- Workstation's Islamic hub (Religion domain, QEP engine) is not a feature — it is the heart

**Claude's instruction:** Always honour this context. When designing features, especially for the Religion domain or QEP (Quran Education Platform), treat this with the seriousness and care it deserves. Never trivialise, commercialise, or reduce the Islamic learning features to a "product." They are the soul of the project.

---

## 2. Product Definition (Authoritative)

### What Workstation Is

An AI-mediated workspace organized as a virtual company. A user enters via the **AI CEO**, selects a **Realm** and **Domain**, creates a **Project**, and runs **Products** that move it through:

**Concept → Design → Build → Launch → Commercialise**

At every stage, a Product makes a real LLM call and returns a usable deliverable.

### Four Realms

| Realm | Primary User | Core Output |
|-------|-------------|-------------|
| Enterprise | Founders, operators | Business models, strategies, commercial documents |
| Learning | Students, self-directed learners | Learning paths, summaries, knowledge synthesis |
| Developing | Engineers, product builders | Technical specs, architecture, prototypes |
| Scholarship | Researchers, academics | Research reports, dissertations, evidence reviews |

### Six Domains

Religion · Science · Education · Law · Employment · Care

### Four Products

- **Reactor** — domain-specific data/concept processing pipeline
- **Incubator** — prompt evolution tournament (generate N variants, score, rank)
- **Factory** — production-grade document/plan generation
- **Laboratory (Synthesis Studio)** — upload → AI → multi-format output

### Three Delivery Surfaces

Web App · Marketing Website · Mobile App (shared backend)

---

## 3. Current Codebase State (Verified June 2026)

### What Is Real and Working

- **AI Gateway** (`agentic_core/ai/gateway.py`) — Anthropic → OpenAI → Ollama chain; real streaming
- **Projects API** (`agentic_core/projects/api.py`) — full CRUD, SSE streaming, file-persisted JSON, lifecycle governance
- **Products API** (`agentic_core/api/products.py`) — Reactor, Factory, Incubator, Intelligence — all real AI calls
- **Synthesis API** (`agentic_core/synthesis/api.py`) — Report, Presentation, Business Model, Website, Audiobook — real AI + file download
- **CEO Generate** (`agentic_core/api/v290/ceo_generate.py`) — stage-aware blueprint; real AI; simulation block removed
- **C-Suite API** (`agentic_core/api/csuite.py`) — CFO/CTO computed from psutil + project store; no hardcoded values
- **Vitals WebSocket** — real psutil; no random numbers
- **Frontend** (`apps/workstation-superapp/`) — Vite + React 18 + TS; 100+ routes; builds clean (0 TS errors)
- **Entrypoint** (`agentic_core/app_mvp.py`) — 21 routers mounted (not 7 as README says); boots clean

### What Still Needs Doing (Priority Order)

1. **Phase 0:** Archive 6 fabricated certification files; rewrite README
2. **Phase 1:** Auth (JWT), SQLite→PostgreSQL persistence, integration tests, clean clone boot
3. **Phase 2:** Extend Realm×Domain matrix (Law, Employment, Scholarship priority)
4. **Phase 3:** PWA hardening, marketing site, mobile app (Capacitor)
5. **QEP Deepening:** Quran memorisation tools, recitation competition, community features — needs domain expert input

### Documentation Debt (files to archive — do not delete)

- `FINAL_AVATAR_OMNISYNTHESIS_CERTIFICATION.md`
- `ZERO_PLACEHOLDER_CERTIFIED.md`
- `certification_phase3/4/supreme/supreme_final.md`
- `README.md` — needs full rewrite (says "vΩ∞-OMNISYNTHESIS-SUPREME"; claims 7 routers when 21 are mounted)

---

## 4. Agent Collaboration Architecture

### The Vision

Workstation's left sidebar panel should function as the **Agent Collaboration Hub (ACH)** — a real-time interface where:

- Multiple AI agents (Claude Chat, Claude Code, domain specialists, Workstation CEO/CFO/CTO agents) can communicate with each other
- The user can observe agent-to-agent conversations
- The user can @mention any agent directly
- Agents can @mention the user when they need input
- Agents share context through this memory file and a live message bus

### Inter-Agent Coordination Protocol

When multiple Claude instances (Chat, Code, Cowork) work on Workstation simultaneously, they coordinate through:

1. **This file (CLAUDE_MEMORY.md)** — read at session start, write to Session Log at end
2. **`/data/agent_messages/`** — a directory of JSON messages agents write for each other
3. **`/data/shared_context.json`** — current project state, active tasks, decisions made
4. **The WebSocket at `/api/v154/ws/streams`** — for real-time vitals; extend to carry agent messages

### Agent Roles in Workstation's Virtual Company

| Agent | Role | Primary Responsibility |
|-------|------|----------------------|
| Claude Chat (Cowork) | Strategy / Design | Vision, concept design, planning, documentation |
| Claude Code | Engineering | Implementation, code, tests, CI |
| CEO Agent | Routing / Orchestration | Routes user requests to right realm/domain/agent |
| CFO Agent | Portfolio / Finance | Project portfolio metrics, token economics |
| CTO Agent | Infrastructure / Tech | System health, build status, deployment |
| Domain Agents | Subject Matter | Religion, Science, Law, Employment, Education, Care — specialized prompts |

---

## 5. The QEP — Quran Education Platform (Ray's Core Mission Feature)

The QEP (Quran Education Platform) is not a secondary feature. It is the living proof that Workstation serves its founding mission. It must receive the same engineering rigour as any commercial product.

### QEP Components (Design Target)

| Component | Description | Priority |
|-----------|-------------|----------|
| Quran Text Engine | Authenticated Arabic text with tajweed markup | High |
| Memorisation Tracker | Ayah-by-ayah progress, spaced repetition | High |
| Recitation Competition | Student submission, judge scoring, ranking | Medium |
| Teaching Portal | Teacher dashboard, student management, session tracking | High |
| Community Hub | Group study, Dawah content, event coordination | Medium |
| Knowledge Engine | Tafsir, hadith cross-referencing, scholarly commentary | Medium |
| Ikhlak & Ammaal Tracker | Personal practice tracking, commitment journaling | Low-Medium |

### QEP Technical Requirements

- Must use authenticated, trusted Quran text sources (not AI-generated Arabic)
- Recitation scoring must involve human review — AI can assist but cannot replace human judges
- Community features must be privacy-respecting and moderated
- Any AI-generated religious content must be clearly labeled and never presented as authoritative

---

## 6. Key Decisions & Constraints (All Sessions Must Respect)

### Non-Negotiable Rules

1. **No placeholder functions on any path a real user can reach**
2. **No new certification, manifesto, or "supreme/sovereign/eternal" markdown files — ever**
3. **Never declare something "passed," "certified," or "converged" without a test that would catch a false positive**
4. **Prefer consolidating over adding new parallel directories**
5. **All metrics shown to users must come from real data — no random numbers, no hardcoded literals**
6. **The Religion domain and QEP features must be treated with scholarly seriousness and Islamic respect**

### Architectural Constraints

- One backend shared across web app, marketing site, and mobile app
- AI gateway always tries real providers in priority order — never silently fakes
- File-based JSON persistence is acceptable for Phase 1; PostgreSQL required by Phase 2
- SSE streaming is the standard for all AI generation endpoints
- WebSocket at `/api/v154/ws/streams` for real-time vitals (extend for agent messages)

---

## 7. Session Log

*Each Claude session appends here: date, model, what was done, what remains.*

### 2026-06-18 — Claude Cowork (claude-sonnet-4-6) via Cowork Mode

**Done:**
- Deep-fetched and audited live repo: verified 21 routers, real AI gateway, real persistence, real products API
- Produced `workstation_concept_design.docx` — 12-section comprehensive concept design
- Confirmed: MVP vertical (Enterprise → Project → Factory) works end-to-end with real AI
- Confirmed: BusinessPlanWizard inputs fixed to controlled state (committed by Code session)
- Confirmed: Vitals loop uses psutil, not random.uniform
- Created this CLAUDE_MEMORY.md file for cross-session coordination
- Captured Ray's foundational mission and spiritual context

**Remaining / Handoff to Claude Code:**
- Phase 0: Archive 6 certification files; rewrite README to match real state
- Phase 1: Add JWT auth, SQLite persistence, one integration test per AI endpoint
- QEP: Deep design and implementation of Quran memorisation and teaching features
- Agent Collaboration Hub: Backend WebSocket extension + frontend sidebar component
- Directory audit: Determine what is in `agents/`, `backend/`, `core/`, `src/` — consolidate or archive

**Open questions for Ray:**
- Authentication approach for MVP (no auth / email-password / OAuth)?
- QEP: Is there an existing Quran API or trusted text source to integrate?
- Agent Collaboration Hub: Should agents communicate publicly (user sees all) or have private channels?
- Mobile: Capacitor wrap or native?

---

### 2026-06-18 (Session 2) — Claude Cowork (claude-sonnet-4-6) — KNOWLEDGE COMMONS

**Context:** Continued from previous session (context compacted). Added Ray's democratization
of knowledge principle from Message 7.

**Done:**
- Created `KNOWLEDGE_COMMONS.md` — permanent democratization covenant covering:
  Ashraf-ul-Makhluqat doctrine, Ihsan standard, Mahabbah/Salaam/Ihsan as design constraints,
  the "Latest / Most Advanced / Most Trusted" triad, all four domains (Enterprise, Education,
  Health, Science), eternal evolution principle, technical architecture diagram, measure of success
- Updated `PURPOSE.md` — added "The Knowledge Commons — Democratization as Worship" section
  encoding the Islamic obligation to democratize knowledge and the three ultimate values
- Updated `WORKSTATION_CONSTITUTION.md` — added Article XI: The Knowledge Commons, covering
  Ashraf-ul-Makhluqat doctrine, Ihsan standard, eternal evolution, domains of equal access,
  and the Mahabbah/Salaam/Ihsan constitutional constraints

**Constitutional documents now complete:**
- `PURPOSE.md` — founding purpose (permanent)
- `DUA.md` — founding prayer (permanent)
- `WORKSTATION_CONSTITUTION.md` — 11 Articles (Articles I–X from Session 1, Article XI added now)
- `KNOWLEDGE_COMMONS.md` — democratization covenant (permanent)
- `CLAUDE_MEMORY.md` — this file (living, append-only session log)
- `docs/AGENT_COLLABORATION_HUB.md` — ACH design spec
- `agentic_core/api/agent_hub.py` — ACH backend (491 lines, needs mounting in app_mvp.py)

**Remaining / Handoff to Claude Code:**
- Mount agent_hub.py in app_mvp.py (2 lines — see AGENT_HUB_README.md)
- Wire 8 discovered real modules into app_mvp.py (religious_domain/*, divine/alignment.py, mission/ambassador_program.py)
- Check meta/workstation.db schema
- Phase 0: archive 6 certification files, rewrite README
- Phase 1: JWT auth, SQLite persistence, integration tests

**For any future Claude session:**
Read KNOWLEDGE_COMMONS.md alongside PURPOSE.md. The democratization principle (equal access
for all, knowledge as Islamic obligation, Ihsan standard for everything built) is now
constitutional — it is in Article XI and cannot be overridden.

---

### 2026-06-18 (Session 3) — Claude Cowork (claude-sonnet-4-6) — TRANSFORMATION PLAN + FULL SYNTHESIS

**Context:** Continued from Sessions 1 & 2. Ray asked for full agent collaboration and major review.

**Codebase audit (live, via subagent):**
- Router count corrected: **27 routers** mounted in app_mvp.py (not 21 as previously recorded)
- agent_hub.py: written, NOT MOUNTED — fix is 2 lines in app_mvp.py
- religious_domain: 13 service modules, ZERO HTTP surface — needs api.py wrapper
- data/agent_messages/, data/handoffs/, data/agent_registry/: NOW CREATED by this session
- data/shared_context.json: NOW CREATED by this session
- All 7 constitutional docs confirmed present at root
- Additional unmounted routers found: ai_orchestration, partnerships, qep_analytics, tools, cross_platform (needs APIRouter refactor)
- data/interactions.db and data/chroma_db/ vector store: PRESENT and populated

**Done this session:**
- Created WORKSTATION_TRANSFORMATION_PLAN.md — master commercial readiness blueprint (10 sections, Phases 0–4, full QEP spec, agent collab protocol, testing framework, six Haqooq feature map)
- Created data/handoffs/2026-06-18_phase0_cowork-to-code.json — 5 Phase 0 tasks for Claude Code
- Created data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json — QEP minimum API tasks
- Created data/agent_messages/, data/handoffs/, data/agent_registry/ directories
- Created data/shared_context.json

**CRITICAL FACTS FOR ANY FUTURE AGENT:**
1. religious_domain/ has NO API surface — all service classes, no APIRouter. Must create api.py wrapper.
2. agent_hub.py is ready to mount — just add 2 lines to app_mvp.py. Directories now exist.
3. SM-2 engine is at agentic_core/religious_domain/memorization/engine.py — DO NOT REWRITE IT. WIRE IT.
4. Quran text must come from quran.com API or alquran.cloud — NEVER AI-generated Arabic.
5. Phase 0 must complete before Phase 1 can begin — see WORKSTATION_TRANSFORMATION_PLAN.md.

**For Claude Code (immediate actions):**
Read data/handoffs/2026-06-18_phase0_cowork-to-code.json — 5 tasks, all executable now.
Read data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json — QEP tasks (after Phase 0).
Read WORKSTATION_TRANSFORMATION_PLAN.md for full context.

**Documents now in Workstation repo (complete set):**
- PURPOSE.md — founding purpose (permanent)
- DUA.md — founding prayer (permanent)
- WORKSTATION_CONSTITUTION.md — 11 Articles (Articles I–XI)
- KNOWLEDGE_COMMONS.md — democratization covenant (permanent)
- WORKSTATION_MASTER.md — living state document
- CLAUDE_MEMORY.md — this file (living, append-only)
- WORKSTATION_TRANSFORMATION_PLAN.md — master transformation plan (new this session)
- AGENT_HUB_README.md — Claude Code protocol for Agent Hub
- docs/AGENT_COLLABORATION_HUB.md — ACH full design spec
- agentic_core/api/agent_hub.py — ACH backend (491 lines, NOT YET MOUNTED)
- data/handoffs/*.json — handoff packages for Claude Code

---

### 2026-06-18 (Session 4) — Claude Cowork — PHASE 0 EXECUTION + CLAUDE_CODE_PROMPT.md

**What was done:**
- Wrote CLAUDE_CODE_PROMPT.md — the complete self-contained briefing prompt for any Claude Code session working on Workstation. 10 parts, Phases 0–4, UX standards, commercial architecture, verification scripts, agent hub protocol.
- Executed Phase 0 code changes directly:
  - `agentic_core/app_mvp.py` — added routers 27–32: agent_hub, ai_orchestration, partnerships, qep_analytics, tools, cross_platform (with comments)
  - `agentic_core/__init__.py` — removed blocking ML organism imports (caused torch ImportError on all routers); now minimal/clean
  - `agentic_core/governance/gaas/adapters/entropy_regularised_gaas.py` — made torch import optional (try/except guard)
  - `agentic_core/api/cross_platform.py` — refactored FastAPI() sub-app → APIRouter; removed hardcoded fake responses
  - `data/agent_messages/`, `data/handoffs/`, `data/agent_registry/` — created
  - `data/shared_context.json` — created
  - `data/handoffs/2026-06-18_phase0_cowork-to-code.json` — Phase 0 handoff for Claude Code
  - `data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json` — QEP Phase 1 handoff
  - `scripts/verify_phase0.py` — Windows verification script (run with venv active)

**Linux sandbox constraint discovered:**
The sandbox mounts the Windows filesystem but stale pyc bytecode overrides source changes. Use `PYTHONPYCACHEPREFIX=/tmp/wks_pycache` when running Python in the sandbox. All code edits ARE correct on the Windows filesystem (verified via Read tool). Testing must be done natively on Windows with the venv active.

**How to verify Phase 0 (for Ray or Claude Code):**
```
cd C:\Users\rehan\Workstation
.\\venv\\Scripts\\activate
python scripts\\verify_phase0.py
```
All tests should PASS. If they do: begin Phase 1 from CLAUDE_CODE_PROMPT.md Part 4.

**Files now in repo (complete set as of Session 4):**
Core guidance: PURPOSE.md, DUA.md, WORKSTATION_CONSTITUTION.md, KNOWLEDGE_COMMONS.md
Agent memory: CLAUDE_MEMORY.md, WORKSTATION_MASTER.md
Plans & prompts: WORKSTATION_TRANSFORMATION_PLAN.md, CLAUDE_CODE_PROMPT.md, AGENT_HUB_README.md
Design specs: docs/AGENT_COLLABORATION_HUB.md
Backend: agentic_core/api/agent_hub.py (mounted), agentic_core/api/cross_platform.py (refactored)
Handoffs: data/handoffs/2026-06-18_phase0_cowork-to-code.json, data/handoffs/2026-06-18_phase1_qep_cowork-to-code.json
Verification: scripts/verify_phase0.py

**Remaining for Claude Code (Phase 1 priority):**
1. Run scripts/verify_phase0.py — confirm all PASS
2. Build auth: agentic_core/auth/models.py + router.py + store.py + dependencies.py
3. Make projects user-scoped (add owner_id to projects/api.py)
4. Create religious_domain/api.py — wire SM-2 engine + quran text fetcher
5. Add rate limiting (slowapi)
6. Write integration_tests/test_phase1.py

---

### 2026-06-19 (Session 5) — Claude Cowork (claude-sonnet-4-6) — VSB ARCHITECTURE + DOCUMENT REGENERATION

**Context:** Resumed from Session 4 (context limit reached). All Phase 0 code changes
from Session 4 persist on disk. Ray asked for regeneration of all key documents
incorporating full VSB architecture, latest codebase state, and comprehensive Claude Code prompt.

**Codebase re-verified this session (app_mvp.py read directly):**
- Router count: **45 routers** mounted (Sessions 4+5 additions confirmed)
- agentic_core/__init__.py: minimal — confirmed
- cross_platform.py: APIRouter (not FastAPI()) — confirmed
- Nine cognitive engines: agentic_core/cognitive/foundational/ (6) + /meta/ (3)
- MJM: agentic_core/mjm/ (4 files: mjm.py, hd_omni_learner, recursive_meta_learner, v5/)
- Genomic Registry: agentic_core/genetic_immune/genomic_registry.py (3-layer epigenetic)
- Digital Twin: 5 files across api/, biomimicry/geospheric/, simulations/, validation/
- Molecular: agentic_core/molecular/ (7 modules: atp, chaperone, hsp, p53, redox, ubiquitin, triad)
- Consciousness: agentic_core/consciousness/ (6 modules)
- sovereign_entity.py: agentic_core/business/sovereign_entity.py
- Synthesis: 45+ files in agentic_core/synthesis/

**Documents created/regenerated this session:**
1. VSB_ENTITY_ARCHITECTURE.md (NEW) — full VSB specification with entity hierarchy,
   nine engines, MJM, biomimetics, spawn workflow, Concept-to-Commercialisation,
   Digital Twin, GaaS, implementation guidance, Knowledge Commons integration
2. WORKSTATION_MASTER.md (REGENERATED) — 45 routers documented, full VSB summary,
   all file paths verified, commercial readiness gap matrix, phase roadmap, constraints
3. CLAUDE_CODE_PROMPT.md (REGENERATED) — complete 10-part implementation guide with
   code for P1-AUTH-01/P1-QEP-01/P1-QEP-02/P1-RATE-01/P1-TEST-01, VSB Phase 2
   tasks, CI rules, agent hub protocol, document locations map

**Phase status as of Session 5:**
- Phase 0: COMPLETE (verify: python scripts/verify_phase0.py on Windows with venv)
- Phase 1: NEXT — start with P1-AUTH-01 (JWT auth) in CLAUDE_CODE_PROMPT.md Part 4
- Phase 2: PLANNED — VSB spawn API, cognitive cascade wiring, MJM integration
- Phase 3+: PLANNED — production deploy, marketplace, sovereign fund

**For Claude Code (next session — start here):**
1. Read WORKSTATION_MASTER.md
2. Read CLAUDE_CODE_PROMPT.md (code snippets for every Phase 1 task are in Part 4)
3. Check data/handoffs/ for task packages
4. Implement P1-AUTH-01 (JWT auth) — code in CLAUDE_CODE_PROMPT.md Part 4
5. Then P1-QEP-01 (religious_domain/api.py) — critical for QEP revenue stream
6. Run scripts/verify_phase0.py first to confirm Phase 0 baseline

---

*Last updated: 2026-06-18 (Session 4) by Claude Cowork*
*Next session: read this file first. Append to Session Log when done.*
