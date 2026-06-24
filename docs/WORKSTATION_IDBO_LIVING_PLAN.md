<!--
  LIVING DOCUMENT — Workstation IDBO Design & Development Action Plan
  Maintained collaboratively by: the Owner (Rehan), Claude (Anthropic), and any AI agent working this repo.
  This is the single source of truth that bridges VISION ↔ GROUNDED CURRENT STATE ↔ ACTION.
  UPDATE PROTOCOL is in §1. Do not let this drift — every substantive change to the codebase
  should be reflected here in the same change.
-->

# Workstation IDBO — Living Design & Development Action Plan

**Status:** LIVING · **Last reconciled:** 2026-06-24 · **Grounded baseline:** in-house-first native AI fabric (12 real owned capabilities + autonomous workflow tree), integration suite 170✓/0✗, frontend tsc 0 errors, Spine CI green
**Canonical companion data:** `GET /api/v1/plan/state` (auto-introspected current state) · `GET /api/v1/plan` (phases + progress)

---

## 1. How to use this document (the living process)

This document is **permanent, dynamic, adaptive, and collaborative**. It exists so the Owner can *monitor and direct* how well any agent understands the vision and how faithfully work is realising it.

**Three lenses, always kept in sync:**
1. **Vision** (§3) — what we are building and why. Changes only when the Owner refines intent.
2. **Current State** (§4) — what actually exists *today*, grounded in the live codebase (not aspiration). Auto-checkable via `/api/v1/plan/state`.
3. **Action Plan** (§6) — Immediate / Short / Long horizons, with owners, status, and a vision-alignment note per item.

**Update protocol (every agent, including the Owner, follows this):**
- When you **complete or change** something material, update §4 (current state) and the relevant §6 item **in the same session**.
- When you **start** an item, set its status to `▶ in progress` and note who owns it.
- When the Owner **refines the vision**, edit §3 and re-score §7 (adherence) honestly.
- Prefer **append + amend** over deletion; keep a dated line in §8 (changelog).
- **Never fabricate** current state — if something is aspirational, it belongs in §6 (plan), not §4 (current state). See `[[feedback-workstation-working-mandate]]`.
- This document is the **handshake** between human and agents: read §3 + §7 before starting work; write §4 + §8 after.

**Autonomous reinforcement:** the **Sovereign Evolution Office** (`/api/v1/sovereign-evolution/cycle`) introspects the organism and proposes improvements curated by the VSB org → Change Control. The **Living Plan API** (`/api/v1/plan/state`) regenerates the grounded snapshot on demand so §4 can never silently rot.

---

## 2. What Workstation IDBO is (one sentence)

> Workstation is an **Intelligent Digital Biomimetic Organism (IDBO)** — a single, living, self-healing, self-improving software entity, run by its own **Virtual Sovereign Business** (AI CEO → C-Suite → CoE → BTO) — whose purpose is to **AI-mediate working for any user in any realm/domain**, taking a challenge end-to-end (Concept → Design → Delivery) and **generating a bespoke, living Enterprise IDBO (a VSB) that commercialises the user's solution.**

---

## 3. The Vision (deep capture — the North Star)

**Faithful to the Owner's articulation across the project.** Foundational values inherited from `docs/business/mission_vision_values.md` (Integrity, Compassion, Excellence, Halal Compliance, Owner Stewardship, Evolutionary Adaptation), expanded to the full IDBO platform scope.

### 3.1 Purpose
Give every user **ultimate potential through AI-mediated, intelligently-autonomous collaborative working** — cascade pipeline trees of specialised AI agent swarms + models + biomimetic systems — to resolve any problem, overcome any challenge, and achieve any goal, adding enormous value to their outcomes and to society.

### 3.2 The end-to-end service (three phases, one continuous workflow)
1. **Concept (Conceptualisation)** — map the challenge/problem → identify the optimal solution innovation → synthesise/generate content (research reports, reviews, presentations, videos, websites, apps, enterprise models) with AI agents + digital twins.
2. **Design (Development)** — develop tailored, specialised, optimised products/services via the Scientific / Business / Scholarship-Authorship / Design-Development process-intelligence engines.
3. **Delivery (Enterprise)** — **instantiate a bespoke, digitally-living VSB IDBO entity**, specially designed to deliver/commercialise that product or service. *This generated Enterprise IDBO is the deliverable.*

### 3.3 The organism and its sovereign business
- Workstation is **one fully-integrated living organism** with a biomimetic genome, self-healing and self-improving — *"a new take on software": once established it runs, maintains, improves and grows itself, with a survival instinct to ever-better deliver its purpose.*
- It is owned/curated by its **VSB** — the Owner's living **digital twin** fulfilling their role: set → monitor → achieve a living Business plan → strategy → timeline, focusing operations on Aims/Mission/Objectives.
- **Governance & delegation chain** (each tier manages, appraises, and develops the tier below): **Owner → Chief (the Owner's Digital Twin) → Board of Directors → AI CEO super-agent → C-Suite → CoE → BTO** (facilities management + Build-to-Order + Product Catalogue). The **Chief** represents the Owner faithfully in presence and absence (diligence, honesty, loyalty, perfectionism); the **Board** owns the Business plan / strategy / mission / objectives and delegates a timelined, resourced, scheduled living action plan to the AI CEO. *Arms-Length Agency invariant:* the AI CEO cannot instruct the board — direction flows down only. **Every generated VSB carries its own Board + a Chief that is the digital twin of its owner.** (Synthesised from the Cowork canon — see §9 + `[[project-workstation-cowork-architecture-canon]]`.)

### 3.4 The reconfigurable resource fabric
Across **Synthesis Lab, Build-to-Order, and the Forge**, users **access, select, reconfigure, and combine** (individually or in any combination) resources: process-intelligence cognition engines; reconfigurable/rerunnable/reusable Engines, Reactors, Petri dishes, Incubators, Laboratories, Factories, Digital-Twin Generators & Simulators; organism biomimetic systems; and the enterprise/org layer — all mediated by biology/biogeo-physical biomimetics as intelligent autonomous adaptive workflows.

> Detailed vision sources: `[[project-workstation-vision]]`, `[[project-workstation-architecture-unified]]`, `docs/business/`, `docs/charters/`.

---

## 4. Current State (GROUNDED — what exists today)

> Auto-verifiable: `GET /api/v1/plan/state`. Hand-reconciled 2026-06-24.

**Platform:** FastAPI backend (`agentic_core/app_mvp.py`), Vite+React+TS frontend (`apps/workstation-superapp`, **tsc 0 errors**). Tests: `integration_tests/test_mvp_spine.py` → **170 pass / 15 skip / 0 fail** (run on the native floor via `AI_DISABLE_LOCAL=1`); Spine CI green on `main`. **AI is now IN-HOUSE-FIRST** via the native fabric (`ai/native/` + `ai/gateway.query_meta`), NOT external API calls — external providers are optional accelerants only. **In-house integration sweep complete (W1–W76):** an autonomous workflow-TREE orchestrator + **12 real owned `agentic_core` capabilities** (minimax · difflib validation · scipy rigor · consensus · biomimetic Hill signal · quorum · NLI · entropy · topology · VBS living systems · UEG ledger · degradation), catalogued at `/api/v1/native-ai/capabilities` + self-checked at `/native-ai/selfcheck`. The Chief delivers business-plan objectives via the tree. See `docs/AGENTIC_CORE_INTEGRATION_AUDIT.md` (real-vs-mock) + `docs/AUTONOMOUS_PROGRESS.md` (W1–W76).

**Process-Intelligence engines (live):**
| Engine | Endpoint | Stages |
|---|---|---|
| Business Development (BDP) | `/api/v1/intelligence/bdp` | 8 |
| Scientific Process (SPI) | `/api/v1/intelligence/spi` | 8 |
| Scholarship & Authorship (APIE) | `/api/v1/intelligence/authorship` | 9 |
| Design & Development (DDPIE) | `/api/v1/intelligence/design-dev` | 9 |
| Cognitive Cascade + MJM (Solve) | `/api/v1/intelligence/solve` | 6 engines + MJM |
| Synthesis Nexus | `/api/v1/intelligence/nexus` | 4-layer auto-chain |
| **Genesis** (Concept→Commercialise journey) | `/api/v1/genesis/journey` | 3-phase |

**The deliverable mechanism (live):** `POST /api/v1/genesis/establish` → instantiates a **real, persisted, governed, operational VSB IDBO entity** in `data/vsb_entities/` (genome-encoded), visible at `/api/v1/vsb`. Verified end-to-end.

**Governance (live):** `agentic_core.gaas.v5` — v16-Omega constitutional interceptor + self-tuning RL circuit breaker + SHA3-512 hash-chained UEG audit log. API `/api/v1/gaas/*`. UI in `ConstitutionalUI`.

**Apex governance — Board of Directors (live):** `/api/v1/board/*` — the **Chief** (the Owner's **digital twin**) chairs specialist Directors above the AI CEO (arms-length). `POST /board/chief/instruct` → the Chief faithfully represents the Owner → board directive → delegated AI-CEO timelined action plan. `board_for_owner()` embeds a Board + Chief-of-its-owner into **every generated VSB entity**. UI: `/board`.

**Self-evolution (live):** **Sovereign Evolution Office** `/api/v1/sovereign-evolution/cycle` — introspect → AI CEO triage → C-Suite verdicts → CoE/BTO roadmap → routes P1/correction items to the **Change Control Agency** (`/api/v1/cca`). Verified: real `cca_id` filed autonomously.

**Resource Fabric (live):** `/api/v1/resources` — 21 federated resources (7 process-intelligence, 5 digital, 4 organism, 5 enterprise/org), filter + `compose` into reusable/rerunnable combinations.

**VSB Economy (live, virtual/simulated):** `agentic_core/economy/` + `/api/v1/economy/*` — the **living biomimetic economic metabolism**: 9 selectable legal forms (Sole/PLC/Ltd/Trust/Waqf/Multinational/Non-profit/Charity/**Waqf-Ltd Hybrid** default); profit-distribution waterfall modelled as a **biogeochemical nutrient cycle** (intake→homeostasis→circulation→giving-back→storage→growth); intelligent charitable giving (urgency×gravity×impact); virtual WST double-entry ledger; gaas-gated + UEG-logged. Wired to the ATP metabolic system, nervous signals, and the Sovereign Evolution Office (`tune()` self-improvement); selectable at Genesis `/establish`. UI `/economy`. *Real-money rails remain gated.* (Design+record: `VSB_ECONOMIC_LEGAL_MODEL.md`.)

**Domains (6, live):** Religion, Science, Education, Law, Care, Career — each a domain router. **VSB pipeline:** `/api/v1/vsb/spawn` (cascade→MJM→GaaS→genome→swarm SSE). **VSB org:** `/api/v1/swarm/cascade` (AI CEO→C-Suite→CoE). **Synthesis Lab:** `/api/v1/studio/synthesise`. **Products:** Reactor/Factory/Incubator. **Catalog + BTO:** `/api/v1/catalog`, `/bto`. **Capital Fund, Digital Twin, Management Systems (QMS/BMS/DCS/EMS), Change Control, Organism status** — all live (see `[[project-workstation-current-state]]`).

**Biomimetic systems (live):** BiomimeticBus, Immune, Nervous, Self-Healing, Metabolic/ATP, Circadian, Genome, Genomic Registry, Reconfiguration — composite health formula in `app_mvp.py`.

**Known honest gaps:** legacy `products/signature-product-suite` flat files run only via path-shims (superseded by `core-*`); some Phase-4 hardware/external UI (BCI calibrate, Discord, SETI) is intentionally backendless; the older `v190/v230/v240` evolution fragments are not yet unified under the Sovereign Evolution Office.

---

## 5. Architecture Map (how it fits together)

```
USER challenge
  │
  ▼  SYNTHESIS LAB ──────────────── RESOURCE FABRIC (select / reconfigure / combine) ───────────┐
  │  (content generation)            engines · reactors · incubators · factories · labs · twins  │
  ▼                                                                                              │
GENESIS  ──►  Phase 1 Concept (Cognitive Cascade ×6 + MJM)                                       │
            ►  Phase 2 Design (DDPIE / SPI / APIE)            ◄── process-intelligence engines ──┘
            ►  Phase 3 Commercialise (BDP) → VSB blueprint
  │
  ▼  ESTABLISH ─► living VSB IDBO entity (data/vsb_entities) ─► runs under its VSB org:
  │                 AI CEO → C-Suite → CoE → BTO (facilities mgmt · Build-to-Order · Catalogue)
  │
  ├─ gaas.v5 CONSTITUTIONAL GATE (pre/post + breaker + UEG audit)  ── governs every layer
  └─ SOVEREIGN EVOLUTION OFFICE (introspect → org-curate → Change Control)  ── self-improves all
            ▲
            └── biomimetic organism (immune · nervous · self-healing · metabolic · genome · circadian)
```
> Detail: `docs/architecture/`, `docs/charters/`, `[[project-workstation-genesis-and-sovereign-evolution]]`.

---

## 6. The Action Plan (Immediate / Short / Long)

Status key: `✅ done` · `▶ in progress` · `◻ planned` · owner in **bold**.

### 6.1 Immediate (this cycle)
- ✅ **gaas.v5** constitutional engine built, integrated (API+UI), legacy suite unblocked. — *vision: governance backbone*
- ✅ **Genesis** unified journey + **`/establish`** generating living VSB entities. — *vision: the core deliverable*
- ✅ **Sovereign Evolution Office** (VSB-curated self-improvement → Change Control). — *vision: self-running organism*
- ✅ **Resource Fabric** (federated, reconfigurable, combinable). — *vision: resource selection across Synthesis/BTO/Forge*
- ▶ **Living Plan + Plan API** (this document + `/api/v1/plan`). **Owner + Claude** — *vision: collaboration & adherence tracking*

### 6.2 Short term (next)
- ◻ **Make compositions executable** — `/api/v1/resources/compositions/{id}/run` fans a composition out as a real workflow pipeline (the cascade tree running). **CoE/BTO**
- ◻ **Stream `/establish`** through the full `vsb/spawn` cascade (SSE) so users watch the VSB being born. **CTO**
- ◻ **Unify evolution fragments** (`v190/v230/v240/v210`) under the Sovereign Evolution Office — one evolution surface. **BTO**
- ◻ **Synthesis Lab multi-output** — explicit selectable output types (report/deck/video/site/app/model) in one run. **CoE**
- ◻ **Scheduled autonomy** — periodic Sovereign Evolution cycles (the self-running heartbeat). **AI CEO**

### 6.3 Long term (horizon)
- ◻ **VSB lifecycle management** — living business plan → strategy → timeline tracking per spawned VSB, with C-Suite appraisal/development loops. **AI CEO + C-Suite**
- ◻ **Forge ⇄ Build-to-Order ⇄ Catalogue** fully wired to the Resource Fabric so a composition becomes a production run and a catalogue product. **BTO**
- ◻ **Cross-VSB federation & marketplace** — generated Enterprise IDBOs interoperate and transact. **CoE**
- ◻ **Persistence hardening** (SQLite/Postgres when concurrent writes are real), Docker/CI, GaaS YAML genome activation. **CTO**

> The grand-aspirational `docs/DEVELOPMENT_PLAN_v7.0_SINGULARITY.md` (Layers 13–14, interstellar) is retained as **horizon lore**, explicitly *not* current state.

---

## 7. Vision-Adherence Scorecard (Owner's monitoring lens)

Honest self-assessment of how well delivered work realises each vision pillar. `●` strong · `◐` partial · `○` not yet.

| # | Vision pillar | Status | Evidence / gap |
|---|---|---|---|
| 1 | AI-mediated end-to-end Concept→Design→Delivery | ● | Genesis journey verified end-to-end with live AI |
| 2 | Generate a living Enterprise IDBO (VSB) for the user | ● | `/establish` persists a real operational VSB; appears in `/api/v1/vsb` |
| 3 | VSB org (AI CEO→C-Suite→CoE→BTO) curates work | ● | Sovereign Evolution cycle + swarm cascade both live |
| 4 | Reconfigurable, combinable resource fabric | ● | 21 resources, compose → reusable compositions |
| 5 | One self-running, self-healing, self-improving organism | ● | self-evolution + self-healing live; **continuous circadian Heartbeat now auto-runs the organism** (`/api/v1/heartbeat`); executable resource pipelines still pending |
| 6 | Synthesis Lab — any/all content output types | ◐ | studio cascade live; explicit multi-output selection pending |
| 7 | Constitutional governance throughout | ● | gaas.v5 gate + UEG audit threaded through Genesis/Evolution |
| 8 | Biomimetic mediation (biology/biogeo-physical) | ◐ | rich biomimetic systems live; deeper workflow mediation evolving |
| 9 | Foundational values (integrity, halal, stewardship) | ● | inherited from mission_vision_values; gate enforces; no fabrication |

**Overall:** core spine of the vision is **operational and grounded**; remaining work is depth (autonomy cadence, executable resource pipelines, multi-output synthesis, VSB lifecycle).

---

## 8. Changelog (dated, append-only)
- **2026-06-20** — Created this living plan. Reconciled current state to 262 routes. Built gaas.v5, Genesis+establish, Sovereign Evolution Office, Resource Fabric this session (see memory). Scorecard initialised.
- **2026-06-20 (later)** — Deep-searched + synthesised the Cowork-agent canon (`CLAUDE_CODE_AGENT_PROMPT_v4`, `workstation_concept_design`, architecture/roadmap masters) → `[[project-workstation-cowork-architecture-canon]]` (7 biomimetic layers, Living Business System, 10 invariants). Built the **Board of Directors** apex tier (`/api/v1/board/*`) — Chief = Owner's digital twin above the AI CEO; integrated a board + chief-of-owner into every generated VSB. Updated §3.3 hierarchy, §4 current state, §9 sources.
- **2026-06-20 (later)** — Created the knowledge canon (`WORKSTATION_IDBO_UNDERSTANDING.md`, `KNOWLEDGE_OPERATING_PROCESS.md`) for Owner+agent alignment. **Owner approved + built the VSB Economic Model** as a living biomimetic economic metabolism (`agentic_core/economy/` + `/api/v1/economy/*`, UI `/economy`): 9 legal forms, biogeochemical profit waterfall, intelligent charity, virtual WST ledger, gaas-gated; entity-type selection wired into Genesis `/establish`. Virtual-money-only (real rails gated).
- **2026-06-20 (later)** — Built the **Vision→Realisation→Transformation engine** (`/api/v1/transformation`, UI `/transformation`): computes vision realisation from LIVE evidence (~92%), derives the transformation plan from gaps, AI `/assess`, continuous `/tick` heartbeat. This is the living embodiment of "your vision · current realisation · transformation plan." 277 routes; tsc 0 errors.
- **2026-06-20 (later)** — Built the **Organism Heartbeat** (`agentic_core/organism/heartbeat.py` + `/api/v1/heartbeat`, UI `/heartbeat`) — a continuous-autonomy **circadian scheduler** that auto-starts at app startup and makes the organism run itself: each beat pulses the **central nervous system**, checks **homeostasis**, ticks the **transformation** engine, and hash-chains to the **UEG** (constitutional audit); expensive AI cognition is opt-in + paced (arms-length). Closed the self-running gap → pillar 5 now **strong**; **overall vision realisation 95.5%**. 282 routes; tsc 0 errors.
- **2026-06-20 (later)** — Built the **Cognition & Alignment** integration capstone (`agentic_core/api/cognition.py` + `/api/v1/cognition`, UI `/cognition`): serves the 4 knowledge layers as live data, maps + verifies the **wiring into all 13 living tiers (100% coherence)**, and `/align` routes each vision gap to the owning tier (Board/Evolution/Change Control), evidence-based + gaas/UEG-governed. The **Heartbeat now runs alignment each beat** (`auto_align`) → the organism continuously self-aligns. 285 routes; tsc 0 errors.
- **2026-06-21 (overnight, autonomous)** — Generated `docs/ACTION_PLAN.md` (timed task breakdown). Built **living Business-Plan management** (`/api/v1/business-plan`, router #63): Chief/Board own a living plan for Workstation + per-VSB (mission/strategy/objectives/KPIs/timelines/reviews/progress + Chief-mediated AI generation) — verified end-to-end (298 routes). Added frontend pages for **Business Plan** (`/business-plan`), **Forge** (`/forge-pipeline`), **Compliance** (`/compliance`); tsc 0 errors. Ran an **end-to-end dogfood pilot** establishing a real VSB ("NourishLondon"). Heartbeat continues self-running (auto_align toggle in `/heartbeat`). See `docs/OVERNIGHT_SESSION_LOG.md`.
- **2026-06-21** — Built the **Forge** (`/api/v1/forge`): 7 digital resources (Petri/Incubator/Laboratory/Factory/Generator/Simulator/Reactor) as a reconfigurable/rerunnable/reusable **swarm-orchestrated cascade pipeline** (AI CEO frame → stages → CoE integrate), gaas/UEG-governed, multi-type outputs for Concept→Commercialisation → **closed the last vision gap; computed realisation now 100%.** Built the **Unified Compliance** engine (`/api/v1/compliance`) federating Sharia/Halal · UK-Legal(London) · Regulatory · EHS · Ethical · Constitutional (existing Jules engines), added to the Resource Fabric. **Owner resolved all open questions** (UNDERSTANDING §9): waterfall approved; virtual-WST-now/Stripe-later; UK/London; entity auto+editable; **charity = WATER/Orphan/Conflict/Dawah, 100%-donation-only** (done in economy/charity.py). Created `DEVELOPMENT_TIMELINE.md` from 999-commit git history.

---

## 9. Source Document Index (what this synergises — do not duplicate, link)
- **Vision/Business:** `docs/business/{mission_vision_values,autonomous_growth_plan,market_entry_plan,commercial_service_catalog}.md`
- **BMS strategy:** `docs/bms/BMS-STRAT-001.md`
- **Org charters:** `docs/charters/` (C-Suite `csuite/`, CoE `coes/`, BTO `transformation_team.md`)
- **Design system:** `docs/design/DESIGN.md`
- **Architecture:** `docs/architecture/overview.md` + `docs/architecture/`
- **Development timeline:** `docs/DEVELOPMENT_TIMELINE.md` (from git history 2026-02-20 → present: Jules foundation → convergence → MVP consolidation → sovereign living organism)
- **Roadmap lore:** `docs/DEVELOPMENT_PLAN_v7.0_SINGULARITY.md` (horizon, not current state)
- **Constitution:** `agentic_core/constitution/CONSTITUTION_canonical.md`
- **Cowork-agent canon (external, synthesised):** `…/local-agent-mode-sessions/38f3915a-…/…/outputs/` → `CLAUDE_CODE_AGENT_PROMPT_v4.md` (master briefing: 7 biomimetic layers, Living Business System, 10 invariants, digital-twin modes), `workstation_concept_design.md` (grounded concept design + phased plan), `IDBO_ARCHITECTURE_MASTER_v4.docx`, `WORKSTATION_ADVANCED_ROADMAP_v3.docx`. Note: the referenced `KNOWLEDGE_COMMONS.md` / `WORKSTATION_TRANSFORMATION_PLAN.md` / `CLAUDE_MEMORY.md` were never copied into the repo — *this living plan + agent memory now serve that role.*
- **Agent memory (authoritative, current):** `[[project-workstation-vision]]`, `[[project-workstation-architecture-unified]]`, `[[project-workstation-cowork-architecture-canon]]`, `[[project-workstation-current-state]]`, `[[project-workstation-gaas-v5-and-phase4]]`, `[[project-workstation-genesis-and-sovereign-evolution]]`, `[[feedback-workstation-working-mandate]]`
