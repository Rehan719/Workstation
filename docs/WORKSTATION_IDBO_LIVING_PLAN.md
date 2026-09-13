<!--
  LIVING DOCUMENT — Workstation IDBO Design & Development Action Plan
  Maintained collaboratively by: the Owner (Rehan), Claude (Anthropic), and any AI agent working this repo.
  This is the single source of truth that bridges VISION ↔ GROUNDED CURRENT STATE ↔ ACTION.
  UPDATE PROTOCOL is in §1. Do not let this drift — every substantive change to the codebase
  should be reflected here in the same change.
-->

# Workstation IDBO — Living Design & Development Action Plan

**Status:** LIVING · **Last reconciled:** 2026-09-05 (W446) · **Grounded baseline:** in-house-first native AI fabric (owned models/orchestration/swarm/ensemble + autonomous workflow tree), integration suite **350✓ / 15 skip / 0 fail** (326 test functions) at the last full run, frontend tsc 0 errors, both CI green on `main` at the last pushed commit (re-check the run for the current one)
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

> Workstation is an **Intelligent Digital Biomimetic Organism (IDBO)** — a single, living, self-healing, self-improving software entity, governed and run by its own **Virtual Sovereign Business** (Owner → **Chief, the Owner's digital twin** → Board → AI CEO → C-Suite → CoE → BTO) — whose purpose is to **AI-mediate working for any user in any realm/domain**, taking a challenge end-to-end (Concept → Design → Delivery) and **generating a bespoke, living Enterprise IDBO (a VSB) that commercialises the user's solution.**

---

## 3. The Vision (deep capture — the North Star)

**Faithful to the Owner's articulation across the project.** Foundational values inherited from `_archive/docs/business/mission_vision_values.md` (Integrity, Compassion, Excellence, Halal Compliance, Owner Stewardship, Evolutionary Adaptation), expanded to the full IDBO platform scope.

### 3.1 Purpose
Give every user **ultimate potential through AI-mediated, intelligently-autonomous collaborative working** — cascade pipeline trees of specialised AI agent swarms + models + biomimetic systems — to resolve any problem, overcome any challenge, and achieve any goal, adding enormous value to their outcomes and to society.

### 3.2 The end-to-end service (three phases, one continuous workflow)
1. **Concept (Conceptualisation)** — map the challenge/problem → identify the optimal solution innovation → synthesise/generate content (research reports, reviews, presentations, videos, websites, apps, enterprise models) with AI agents + digital twins.
2. **Design (Development)** — develop tailored, specialised, optimised products/services via the Scientific / Business / Scholarship-Authorship / Design-Development process-intelligence engines.
3. **Delivery (Enterprise)** — **instantiate a bespoke, digitally-living VSB IDBO entity**, specially designed to deliver/commercialise that product or service. *This generated Enterprise IDBO is the deliverable.*

### 3.3 The organism and its sovereign business
- Workstation is **one fully-integrated living organism** with a biomimetic genome, self-healing and self-improving — *"a new take on software": once established it runs, maintains, improves and grows itself, with a survival instinct to ever-better deliver its purpose.*
- It is owned/curated by its **VSB**, whose apex is the **Chief of the Board — the Owner's living digital twin** (vision §5; "the VSB is the twin" was the pre-Board-layer wording, corrected W446) — fulfilling the Owner's role: set → monitor → achieve a living Business plan → strategy → timeline, focusing operations on Aims/Mission/Objectives.
- **Governance & delegation chain** (each tier manages, appraises, and develops the tier below): **Owner → Chief (the Owner's Digital Twin) → Board of Directors → AI CEO super-agent → C-Suite → CoE → BTO** (facilities management + Build-to-Order + Product Catalogue). The **Chief** represents the Owner faithfully in presence and absence (diligence, honesty, loyalty, perfectionism); the **Board** owns the Business plan / strategy / mission / objectives and delegates a timelined, resourced, scheduled living action plan to the AI CEO. *Arms-Length Agency invariant:* the AI CEO cannot instruct the board — direction flows down only. **Every generated VSB carries its own Board + a Chief that is the digital twin of its owner.** (Synthesised from the Cowork canon — see §9 + `[[project-workstation-cowork-architecture-canon]]`.)

### 3.4 The reconfigurable resource fabric
Across **Synthesis Lab, Build-to-Order, and the Forge**, users **access, select, reconfigure, and combine** (individually or in any combination) resources: process-intelligence cognition engines; reconfigurable/rerunnable/reusable Engines, Reactors, Petri dishes, Incubators, Laboratories, Factories, Digital-Twin Generators & Simulators; organism biomimetic systems; and the enterprise/org layer — all mediated by biology/biogeo-physical biomimetics as intelligent autonomous adaptive workflows.

> Detailed vision sources: `[[project-workstation-vision]]`, `[[project-workstation-architecture-unified]]`, `docs/business/`, `docs/charters/`.

---

## 4. Current State (GROUNDED — what exists today)

> Auto-verifiable: `GET /api/v1/plan/state`. Hand-reconciled 2026-09-05 (W446); the full delivery record is in `docs/AUTONOMOUS_PROGRESS.md`, and the section-by-section fidelity verdict is `docs/VISION_FIDELITY_LEDGER.md` (v3, 2026-09-05 — every finding individually refuted against a HEAD-booted backend). The distilled, ordered plan to close what remains is `docs/FABLE_DELIVERY_PROMPT.md` (v11 rev 2, `<delivery_plan>`).

**Platform:** FastAPI backend (`agentic_core/app_mvp.py`, **463 API operations** — method+path pairs; 439 distinct `/api` paths — measured 2026-09-05 with `python scripts/reach_audit.py`; re-measure rather than trust), Vite+React+TS frontend (`apps/workstation-superapp`, **tsc 0 errors**, 73 `<Route>` declarations). Tests: `integration_tests/test_mvp_spine.py` → **350 pass / 15 skip / 0 fail** (326 test functions; run on the native floor via `AI_DISABLE_LOCAL=1`); Spine + Doc-Sync CI green on `main` at the last pushed commit; browser smoke 17 deep routes + 57 swept. **Rounds 7–10 (W322–W354):** design-surface + swarm tenancy (W324), §11 marketplace teeth + substance-aware birth verdicts (W322), genuinely tamper-evident evidence chains (W327), the streaming owned model that actually serves under its adaptive budget (W323/W353), the enterprise-aware avatar with in-house voice (W325/W326), entity-to-entity service contracts + a real self_investment consumer (W330), the memory layer's cross-tenant bleed closed at the source with per-tenant namespaces + Owner-run purge remediation (W332/W333/W334/W343), store-concurrency correctness across the money paths + the UEG audit chain (W348/W349/W351), owner-scoped avatar sessions (W350), grounded floor-safe shipped copy (W355/W356), and a Docker image that actually boots + an honest prod compose (W354). The §17.5 invariants were live-verified incl. arms-length falsification (W345) and the evolution-apply loop driven end-to-end (W346). **AI is IN-HOUSE-FIRST** via the native fabric (`ai/native/` + `ai/gateway.query_meta`) — owned model discovery/routing/tiers, parallel multi-model **ensemble**, health-reordering orchestrator, hardened memory store (corruption-tolerant + atomic writes); external providers are optional accelerants only. **In-house integration sweep complete (W1–W76)** — autonomous workflow-TREE orchestrator + 16 real owned capabilities (live count 2026-09-11) at `/api/v1/native-ai/capabilities`. **W194–W250:** ALL EIGHT PI cognition engines (BDP·SPI·APIE·DDPIE·Cascade·MJM·Nexus·Genesis), ALL EIGHT digital-resource facilities (Engines·Reactors·Petri·Incubators·Laboratories·Factories·Generators·Simulators — Reactor = the vision-exact Incubator+Experimentation+Studio composite), all 8 biomimetic organism systems, the full enterprise/org layer (cascade·Capital Fund·Change Control·Products Catalogue·Build-to-Order) AND the last registry resources (compliance·truth_consensus·mega_project·omnimedia·federation_mesh) **run their REAL engine when composed in the Resource Fabric** — nothing in the catalogue is a prompt approximation. **W248:** every generated VSB (Genesis /establish, SSE /vsb/spawn, Studio) carries its own Board + Chief (owner's digital twin) + living economy + living-entity registration + seeded plan. **W249:** every economy cycle is gaas-gated + UEG split-logged; material distributions are held for Change Control approval. **W252–W300 (Rounds 3–4):** tenant isolation live on the VSB/Genesis/Studio + per-VSB management surfaces (W252/W295, 404-never-403, server-stamped owners); digital-twin pre-validation gates HIGH/CRITICAL Change Control (W253); SSE establish birth-stream (W255); double-entry ledger + period close + CFO statements (W256); §11 REAL engine-backed verdicts sealed + UEG-logged + CCA-routed, continuously re-screened on the heartbeat (W285–W288); the §13 repo genuinely version-controlled, shipped as one whole, cascades re-runnable (W289–W291); REAL revenue recognition + compounding loops closed (W293–W294); the login/token front door + Owner-gated self-serve signup flag (W296–W297). **W301–W321 (Rounds 5–6):** the §4 journey's WHOLE record survives establishment and reaches every shipped surface (W301–W306: blueprint accessor, birth auto-ship, verbatim-export deliverables, simulated candidate ranking); the §10 bar measured per-criterion with a genuinely-stateful defect→correction→re-verify loop and TRUE failures/gates arithmetic (W307/W316); Offering-1 gated flag-not-block (W308); birth vitals + compliance-held economy + heartbeat auto-evolve/auto-ship of children (W309/W319); the genome mutates only through CCA approval and immune_quarantine genuinely CONTAINS (W310/W318); the economy's materiality hold PRESERVES the held revenue and waterfall bounds bind to the stored entity type (W313); the economy router, Living Deliverables and QMS defects are tenant-scoped (W320); the Shell is mobile-first below 768px (W312); the fabricated front-door/security-theater copy is archived or rewritten truthfully (W314); one establish core serves both paths with scaffold-clean public copy (W315); the 401→/login seam is real and purchases are caller-bound (W317). See `docs/AGENTIC_CORE_INTEGRATION_AUDIT.md` (real-vs-mock) + `docs/AUTONOMOUS_PROGRESS.md` (W1–W250, the authoritative cycle log).

**W355–W434 (Rounds 11–13 + the v8→v10 prompt cycle, 2026-08-30 → 2026-09-02):** the frontend
defect ledger closed 47/47 (dead governance surface, HTTP-status blindness class-killed, every
fabricated handler deleted — zero fabricated strings in the shipped bundle); the owned model
UNBLOCKED — four independent gates each sufficient to stop it ever serving (W375–W380), now measured
serving all 11 journey stages; §4.5 candidate ranking screens real compliance+safety with a veto and
discloses ties (W419); §10 separates gate-MEASURED from caller-ATTESTED criteria (W419); all five
autonomy flags switchable and restart-durable (W420); §11 verdicts + economic holds visible to the
entity owner (W421); the biomimetic record names only contributing layers and composite health names
its simulated term (W422); regeneration is a measured IMPROVEMENT pass over the prior draft (W425);
realm reaches every generation prompt at the Owner's approved narrow scope (W427/W434); an explicit
owner-scoped profile reaches prompts — never recall (W428); PDFs extracted in-browser, zero external
requests (W429); **a defect CLASS — a value selected or reported when nothing discriminated — closed
in sixteen places across five subsystems** (W419–W433, ledger: `NATIVE_PRIMITIVE_DEFECT_LEDGER.md`);
and the user's problem now provably survives every journey stage into the exported document, with the
public VSB website scaffold-clean (W434). 25 new guards, each broken and watched fail before being
trusted.

**W435–W446 (the v10→v11 prompt cycle and the Tier-2 reach campaign, 2026-09-02 → 2026-09-05):**
the journey UI's floor disclosure closed (W436 — floor-served stages return `verified: null`, never a
certification); the systemic reach backlog (148 genuine-unreached ops in 43 clusters at W437) worked
to completion cluster by cluster — native-AI Primitive Console (W437), organism Anatomy + config
governance fused with the CCA (W438), the **Quran Education Platform delivered into the Religion
domain by Owner directive under the §11 faith-content constitution** (W439 — the tafsir route had
been asking models to GENERATE Quranic Arabic; now fetch-and-inject, recitation never scored,
translation refuses the floor), the VBS operating systems on the VSB Cockpit (W440), the frontier
router RETIRED to `_archive` (W441), the economy money-integrity round (W442 — the ledger had no
lock, NaN killed funds conservation, a blocked verdict ran the cycle anyway), the Agent Hub rewritten
with auth + strict ids + honest delivery counts (W443), and the residual clusters incl. a shadowed
parallel marketplace retired (W444). Reach now: **325/456 `/api` ops reached · 64 legacy (non-v1, unreached by the
fragment matcher — kept under rule 17) · 67 genuine-unreached, small scatter in 38 tiny clusters.** Every round since W437 has
been adversarially refuted before shipping — nine consecutive rounds of real catches. W445/W446
regenerated the canon from provenance (vision, prompt v11, fidelity ledger v3, this plan).
**W449 (2026-09-12):** delivery-plan **P1.1 delivered** — the living-QMS gate learned who served the
content: floor-served → `qms_gate_passed: null` with the basis (never `pass`), no gate run counted, the
record sealed per delivery; coverage measured against the prompt's own sections; a verbatim ingest and
a journey-born entity carry their origin to the gate; Genesis withholds modelled/simulated/ranked on a
tie; one `qmsChip` helper on every surface under a grep guard.
**W450 (2026-09-12):** delivery-plan **P1.2 delivered** — the shipped body never wears floor scaffold nor a
fallback name: floor-served fields → `content pending the owned model` (by provenance); slug name →
pending, nothing ships until the founder names it (`POST /vsb/{id}/name`); `/repo` never regresses a
generated surface; the board-pack narrative and evidence excerpt are pending on the floor.
**W451 (2026-09-12):** delivery-plan **P1.3 delivered** — the AI CEO chat on the owned fabric:
`gateway.stream_meta` surfaces provenance from the stream path; the chat is grounded in the Board's
directives + the living plan + the business plan + the real meeting log; per-message `served_by`
badge and a pill that reads from it; the persona, fake tool registration and canned advisory deleted.
**W452 (2026-09-12):** delivery-plan **P1.4 delivered** — Mode 3 review gates gate: one shared guard on
every lifecycle mover (409 with the gate named while a gated stage is pending or rejected), gates set at
birth hold the birth-ship, the heartbeat holds gated entities with a recorded action, the panel says so.
**W453 (2026-09-12):** delivery-plan **P1.5 delivered** — provenanceBadge class-kill part 2: every badge
site renders the helper's cls/title; `provenanceMapBadge` for count maps; the floor is amber everywhere;
a source-grep guard holds the shape.
**W454 (2026-09-12):** delivery-plan **P1.6 delivered** — Employment default-tab honesty: the hub opens
on the CV tools; the job search returns illustrative listings (no invented url/date, no 'source'), the
page says so and badges the search and every generated document.
**W455 (2026-09-12):** delivery-plan **P1.7 delivered** — compliance that reads: the constitutional row
says what it can check; the audit hash covers the subject; nothing matched is review, not pass; the
Frameworks card names what each check does; a FAIL deliverable carries its verdict on page one of every export.
**W456 (2026-09-12):** delivery-plan **P1.8 delivered** — the tafsir tab completes §11: the floor's
Translation/Transliteration withheld with the reason, a disclaimer, the sourced Arabic and the range cap on
screen.
**W457 (2026-09-12):** delivery-plan **P1.9 delivered** — Care scoring computes: NEWS2 / MUST / Waterlow
from the published tables in-house (falls as a labelled factor count), validated, returned first; the AI
interprets only.
**W458 (2026-09-13):** delivery-plan **P1.10 delivered** — disabled ≠ failed: a resource never attempted
(config-disabled, unknown, or refused by the spend policy) is a labelled SKIP that records nothing, and
`/native-ai/status` follows the last completion that actually served, naming the row it read.
**W459 (2026-09-13):** delivery-plan **P1.11 delivered** — Change Control enforced: identity read and
stamped, the override gated (admin under auth; CRITICAL always an explicit admin decision), the decision
source recorded honestly, the twin fallback labelled, every change record written under a compare-and-set.
Open items live in `FABLE_DELIVERY_PROMPT.md` (v11 rev 2 — the `<ledger>` and the `<delivery_plan>`
for the whole of §1–§15).

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

**Resource Fabric (live):** `/api/v1/resources` — 41 federated resources (live registry count 2026-09-11 — re-measure) across process-intelligence · digital-resource facilities · native-AI · organism · enterprise/org classes; filter + reconfigure params + `compose` (model/simulate before commit) + **`/compositions/{id}/run` executes every composed resource's REAL engine** on the owned native swarm with provenance.

**VSB Economy (live, virtual/simulated):** `agentic_core/economy/` + `/api/v1/economy/*` — the **living biomimetic economic metabolism**: 9 selectable legal forms (Sole/PLC/Ltd/Trust/Waqf/Multinational/Non-profit/Charity/**Waqf-Ltd Hybrid** default); profit-distribution waterfall modelled as a **biogeochemical nutrient cycle** (intake→homeostasis→circulation→giving-back→storage→growth); intelligent charitable giving (urgency×gravity×impact); virtual WST double-entry ledger; gaas-gated + UEG-logged. Wired to the ATP metabolic system, nervous signals, and the Sovereign Evolution Office (`tune()` self-improvement); selectable at Genesis `/establish`. UI `/economy`. *Real-money rails remain gated.* (Design+record: `VSB_ECONOMIC_LEGAL_MODEL.md`.)

**Domains (6, live):** Religion, Science, Education, Law, Care, Employment (canonical taxonomy id `employment` — `agentic_core/taxonomy.py`; the legacy `/api/v1/career/*` router is kept for its live callers) — each a domain router; the Religion domain carries the QEP flagship (`/religion?tab=qep`, `/qep`). **VSB pipeline:** `/api/v1/vsb/spawn` (cascade→MJM→GaaS→genome→swarm SSE). **VSB org:** `/api/v1/swarm/cascade` (AI CEO→C-Suite→CoE). **Synthesis Lab:** `/api/v1/studio/synthesise`. **Products:** Reactor/Factory/Incubator. **Catalog + BTO:** `/api/v1/catalog`, `/bto`. **Capital Fund, Digital Twin, Management Systems (QMS/BMS/DCS/EMS), Change Control, Organism status** — all live (see `[[project-workstation-current-state]]`).

**Biomimetic systems (live):** BiomimeticBus, Immune, Nervous, Self-Healing, Metabolic/ATP, Circadian, Genome, Genomic Registry, Reconfiguration — composite health formula in `app_mvp.py`.

**Known honest gaps (regenerated W446 from `VISION_FIDELITY_LEDGER.md` v3 — 60 findings against a HEAD-booted backend, every one refuted; the ordered plan to close them is `FABLE_DELIVERY_PROMPT.md` v11 rev 2 `<delivery_plan>`):** TIER 1 (reached surfaces that mislead — plan P1): the shared QMS gate certifies floor scaffold (coverage measured against no sections; Genesis got the W436 fix, the shared gate did not); the shipped VSB body presents that scaffold as the enterprise's concept; the Living Organisation hub's DEFAULT tab is a detached Ollama roleplay outside the native fabric; Mode 3 review gates gate nothing; ten badge sites paint the floor green; the Employment default tab promises a "live job board" over AI synthesis; the Constitutional compliance row never reads the subject; the tafsir tab serves a floor "Translation" heading; Care "validated scoring" computes nothing; `/native-ai/status` inverts on a failure row; Change Control's tiers are prose; a disconnected composer canvas; a marketplace counting directories as live products; a board pack certifying an empty narrative. TIER 2 (invisible shortfalls — P2): floor cascades grounded in the engine's own marker text; provenance stopping at the API boundary on seven pages; the avatar answering its persona line; the organism defending on paper (reflex arcs 0, immune defence uncalled, a survival instinct on a simulator that cannot fall, Cardiovascular/Endocrine vouched for by unwired files, torch optionality failing at import); the GaaS gate on 8 of 57 modules; an unauthenticated control perimeter; the 67-op scatter. TIER 3 (unbuilt — P3): §4.6 Develop, §4.1 image intake, §17.3 cadence layers, §17.4 Mode 2, autonomy that starts at establishment, §9 i18n depth, §13 repo access — and four OWNER RULINGS (the lifecycle; the §17.1 Products axis; the §17.5 KPI gate; Mode 2 scope). Standing and honest: mp4/mp3 remain a not-yet catalogue; the §6 path is exercised on the deterministic floor in CI (`AI_DISABLE_LOCAL=1`) — live-model soak runs are a manual Owner activity; the Stripe key remains in git history (Owner action); 162 test-owned entities (Owner's call).

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
> Detail: `_archive/docs/architecture/`, `_archive/docs/charters/` (archived W153+), `[[project-workstation-genesis-and-sovereign-evolution]]`.

---

## 6. The Action Plan (Immediate / Short / Long)

Status key: `✅ done` · `▶ in progress` · `◻ planned` · owner in **bold**.

### 6.1 Immediate (this cycle)
- ✅ **gaas.v5** constitutional engine built, integrated (API+UI), legacy suite unblocked. — *vision: governance backbone*
- ✅ **Genesis** unified journey + **`/establish`** generating living VSB entities. — *vision: the core deliverable*
- ✅ **Sovereign Evolution Office** (VSB-curated self-improvement → Change Control). — *vision: self-running organism*
- ✅ **Resource Fabric** (federated, reconfigurable, combinable). — *vision: resource selection across Synthesis/BTO/Forge*
- ✅ **Living Plan + Plan API** (this document + `/api/v1/plan`). **Owner + Claude** — *vision: collaboration & adherence tracking*

### 6.2 Short term (delivered; reconciled W251)
- ✅ **Compositions executable** — `/compositions/{id}/run` executes every composed resource's REAL engine on the native swarm (W199–W250: PI engines · all 8 facilities · organism systems · enterprise layer · the full catalogue). **CoE/BTO**
- ✅ **Stream `/establish`** — `POST /api/v1/genesis/establish/stream` is the Genesis page's SSE birth stream (W255; one establish core serves both the blocking and the streamed path, W315). **CTO**
- ✅ **Unify evolution fragments** — the `v191` proposals engine was absorbed under arms-length governance in W261 (approve files a REAL Change Control request; outcomes mirrored). The `/api/v191` mount remains as an UNREACHED legacy namespace — no frontend caller exists (the `app_mvp.py:153` comment naming Proposals + EvolutionDashboard is stale) — so retire-or-keep is a P2.4 scatter decision, not open unification work (corrected W448). **BTO**
- ✅ **Synthesis Lab multi-output** — 15 selectable output types in one run (`agentic_core/synthesis/api.py`; Video is honestly a slide+narration deck until real rendering exists). **CoE**
- ✅ **Scheduled autonomy** — the circadian Heartbeat auto-starts at app startup and runs paced Sovereign-Evolution cycles + living-VSB economy ticks (now gaas-gated + UEG-logged, W249). **AI CEO**

### 6.3 Long term (horizon)
- ✅ **VSB lifecycle management** — every generated VSB carries Board+Chief, a living business plan, economy metabolism, and living-entity registration (W248); C-Suite appraisals run in the swarm cascade. **AI CEO + C-Suite**
- ✅ **Forge ⇄ Build-to-Order ⇄ Catalogue** — BTO configures real blueprints from the 20-product catalogue; the fabric composes/runs them (W246). **BTO**
- ▶ **Cross-VSB federation & marketplace** — PARTIAL: entity-to-entity service contracts (W330), WST transfers, and the §12 marketplace's listing/pricing/purchase door (W444) are live; cross-INSTANCE federation stays honestly simulated (`simulated: true`) by Owner decision 2026-08-31 — Option A, recorded as vision §18-E. **CoE**
- ▶ **Persistence hardening** — PARTIAL: `store_lock` + `atomic_write_json` + `load_json_tolerant` across the money paths, UEG chain, living registry, AI memory, users, fund and venture stores (W348–W351, W365–W371, W442–W444 — each round found one more unlocked writer; the rule is now 'enumerate every writer'); SQLite/Postgres is Owner-gated (managed Postgres). Docker/CI ✅. **CTO**
- ▶ **User isolation** (the §17.5 absolute invariant) — PARTIAL: delivered on the VSB spine, Genesis, Studio, economy, deliverables, QMS defects, marketplace, avatar sessions, native memory and the Agent Hub (W252–W443, 404-never-403, server-stamped owners); NOT yet on the organism's control perimeter — the heartbeat, genome, organism-status, sovereign-evolution, board, change-control, business-plan and swarm routers each carry zero auth dependencies (W446 audit R6.2/R3.2: `change_control.py` imports none — a CRITICAL change can be filed as `ai_ceo` and override-approved by anyone), and `synthesis_studio`'s `GET /studio/vsb` lists every entity with no owner filter. Planned: prompt v11 rev 2 delivery plan. **CTO**
- ✅ **Digital-twin pre-validation** in the Change Control implement path (W253 — HIGH/CRITICAL gated, 409 on a twin failure). Caveat found W446: with no twin model registered the check falls back to an organism-health default (`source: health_gate_default`) and a manual override is attributed to `cca_ai` in the audit trail — both in the delivery plan. **Closed W459:** the fallback now reads "no twin model — health gate only" and every decision records the principal that made it, never `cca_ai`. **BTO**

> The grand-aspirational `_archive/docs/DEVELOPMENT_PLAN_v7.0_SINGULARITY.md` (Layers 13–14, interstellar) is retained as **horizon lore**, explicitly *not* current state.

---

## 7. Vision-Adherence Scorecard (Owner's monitoring lens)

Honest self-assessment of how well delivered work realises each vision pillar. `●` strong · `◐` partial · `○` not yet.

| # | Vision pillar | Status | Evidence / gap |
|---|---|---|---|
| 1 | AI-mediated end-to-end Concept→Design→Delivery | ◐ | Journey runs end-to-end; the user's problem survives every stage (W434); the journey UI discloses the floor (W436). ◐ because (W446, ledger R2/R1) the shipped VSB body's SUBSTANCE still awaits the owned model (since W450, P1.2, a floor-served field ships as an honest pending state and the founder names the enterprise — never scaffold, never a fallback name; the §10 gate says 'not assessable' since W449), Mode 3 gates now GATE every mover (W452) but pause the ship, not a stage mid-journey, and §4.6 Develop has no stage — plan P3.1 |
| 2 | Generate a living Enterprise IDBO (VSB) for the user | ● | `/establish` (and the SSE stream) persists a real, governed VSB with Board + Chief + economy + plan + registration (W248/W255); 219 entities live. Caveat: born at `stage: "commercialise"` from a literal (Owner ruling 3.10) and, on the floor, bodied with scaffold (P1.2) |
| 3 | VSB org (AI CEO→C-Suite→CoE→BTO) curates work | ◐ | The full-hierarchy cascade runs on the owned fabric with real facility requisitions, plan binding and UEG seal (W446 re-verified, ledger R3.7) and the Sovereign Evolution cycle runs — but the hub's DEFAULT tab (AI CEO chat) is a detached "Galactic Era" Ollama roleplay outside the fabric (R3.0), review gates are advisory (R3.1), and the Board's grounded deliberation is API-only (R3.4). ◐ until P1.3/P1.4 land |
| 4 | Reconfigurable, combinable resource fabric | ● | 41 federated resources (live count); compose → simulate → commit → **every composed resource runs its REAL engine** on the native swarm (W199–W250); cascades user-definable on `/native-ai` and `/resource-fabric` (W446 re-verified, R4.4). Caveats: the per-VSB swarm is one fixed 4-stage template (P2.8); the Composer tab is a disconnected canvas (P1.12) |
| 5 | One self-running, self-healing, self-improving organism | ◐ | The heartbeat genuinely runs (beats UEG-chained), self-healing breakers are real, autonomy flags are switchable + restart-durable (W420). ◐ (W446, ledger R6/R4): every autonomy flag defaults OFF and stays OFF (genome generation 0, no VSB ever tended unless a flag is flipped); reflex arcs registered = 0; the immune defence route has no caller; the survival instinct keys off an ATP simulator that cannot fall below its threshold. Self-running is a switch nobody is told about — plan P2.7/P3.2 |
| 6 | Synthesis Lab — any/all content output types | ◐ | 15 selectable output types in one run; Video/mp4/mp3 remain an honest not-yet catalogue |
| 7 | Constitutional governance throughout | ◐ | gaas.v5 + UEG are real where wired (economy cycles gated + split-logged + held, W249; twin pre-validation W253; tenant isolation on the business spine). ◐ (W446, ledger R6.0/R3.2/R1.1/R1.3): the GaaS gate covers 8 of 57 API modules — every other output passes a three-regex filter; Change Control's tiers are prose (no auth, override honoured for CRITICAL, a human override logged as `cca_ai`) — closed W459, the glyph moves only when the re-run audit says so; the Constitutional compliance row never reads the subject; a compliance FAIL ships an unmarked export. Plan P1.7/P1.11/P2.6 |
| 8 | Biomimetic mediation (biology/biogeo-physical) | ◐ | Immune sensing, the Nervous bus, self-healing, the Musculoskeletal facilities and the §6↔§8 homeostasis loop are real (W177–W245). ◐ (W446, ledger R4.5/R4.6/R6.1): Cardiovascular is CPU-idle relabelled and Endocrine an unimported PID file while the W434 quality note vouching for them travels in every record; reflex arcs cannot fire; the §8→§12 survival instinct is a dead branch on a non-depleting simulator. Plan P2.7 |
| 9 | Foundational values (integrity, halal, stewardship) | ● | inherited from mission_vision_values; the faith-content constitution delivered (W439 — Quran never AI-generated, recitation never scored); charity 100%-donation screen with Owner directives; virtual-only finance with real rails gated; honesty-over-polish as practice (63/63 fabrication audit; refuters on every round). Caveat: the W446 audit found fourteen reached surfaces that still mislead — listed in §4 and being worked first (P1) |

**Overall (re-scored W446, 2026-09-05 — honestly DOWN, from 7 strong to 3):** the vision's spine is built and
operational — the fabric, the economy, the domain surfaces, the org cascade, the living roadmap and the
faith constitution are DELIVERED by execution — and it is now measured by a re-runnable six-region audit
(`VISION_FIDELITY_LEDGER.md` v3, 60 findings, all refuted) rather than self-reported. The re-score moves
four pillars to ◐ because the audit found what a user meets first: a default hub tab outside the native
fabric, a quality gate that cannot fail on the shipped configuration, review gates that do not gate, an
organism whose autonomy is a switch nobody is told about, and a constitutional gate covering 8 of 57
modules. None of these is a reach gap; all are honesty gaps, and `FABLE_DELIVERY_PROMPT.md` v11 rev 2
carries the ordered plan (P1 truth → P2 reach/disclosure → P3 capability → P4 Owner switches) with
acceptance criteria, a six-step verification per workstream, and milestones that re-run this audit.
The scorecard moves back up only when the audit says so — and `GET /api/v1/plan` mirrors this table
under a lockstep test, so the API dropped with it in the same commit.

---

## 8. Changelog (dated, append-only)
- **2026-09-13 (W459)** — delivery-plan P1.11 delivered (Change Control enforced); §4 updated; the two
  W446 Change Control caveats annotated closed; glyphs unchanged (they move only on the re-run audit).
- **2026-09-13 (W458)** — delivery-plan P1.10 delivered (status honesty; disabled ≠ failed); §4 updated;
  glyphs unchanged.
- **2026-09-12 (W457)** — delivery-plan P1.9 delivered (Care scoring computes); §4 updated; glyphs
  unchanged.
- **2026-09-12 (W456)** — delivery-plan P1.8 delivered (the tafsir surface completes §11); §4 updated;
  glyphs unchanged.
- **2026-09-12 (W455)** — delivery-plan P1.7 delivered (compliance that reads); §4 updated; glyphs
  unchanged.
- **2026-09-12 (W454)** — delivery-plan P1.6 delivered (Employment default-tab honesty); §4 updated;
  glyphs unchanged.
- **2026-09-12 (W453)** — delivery-plan P1.5 delivered (provenanceBadge class-kill part 2); §4 updated;
  glyphs unchanged.
- **2026-09-12 (W452)** — delivery-plan P1.4 delivered (Mode 3 gates gate); §4 and §7 row 1 evidence
  updated; glyphs unchanged (row 1 stays ◐ until P3.1).
- **2026-09-12 (W451)** — delivery-plan P1.3 delivered (the AI CEO chat on the fabric); §4 updated;
  glyphs unchanged.
- **2026-09-12 (W450)** — delivery-plan P1.2 delivered (the shipped body never wears scaffold nor a
  fallback name); §4 and §7 row 1 evidence updated; glyphs unchanged (row 1 stays ◐ until P1.4/P3.1).
- **2026-09-12 (W449)** — delivery-plan P1.1 delivered (the gate that could not fail on the floor); §4
  and §7 row 1 evidence updated; glyphs unchanged (row 1 stays ◐ until P1.2/P1.4/P3.1).
- **2026-09-05 (W446 reconciliation)** — §4 brought current through W435–W446 (suite 350✓/15 skip/0 fail;
  463 ops / 439 paths; reach 325/456 + 64 legacy + 67 scatter); §6.2/§6.3 statuses corrected against code
  (SSE establish ✅, twin pre-validation ✅ with its health-gate caveat, isolation/federation/persistence
  ▶ partial with the exact routers still open); §4's gaps regenerated from `VISION_FIDELITY_LEDGER.md` v3
  (60 findings, every one refuted against a HEAD-booted backend); **§7 re-scored honestly — pillars 3, 5,
  7, 8 to ◐** with the API mirror (`living_plan.py::_PILLARS`) moved in the same commit under the W435
  lockstep test; §2/§3.3 corrected (the Chief, not the VSB, is the Owner's twin; the apex tiers named);
  the vision gained recorded Owner directives at their claim sites and §18-E; delivery prompt at v11 rev 2
  with the first whole-vision `<delivery_plan>` (P1–P4, definition of complete).
- **2026-09-02 (W434 reconciliation)** — §4 + §7 brought current through W355–W434: suite 337✓/15
  skip/0 fail; 466 API operations / 441 paths measured against a HEAD boot; the §4.5 defect CLASS
  closed in sixteen places; the journey chain fixed at three causes with the user's problem now
  surviving into the export; `VISION_FIDELITY_LEDGER.md` regenerated (v2, adversarially refuted);
  the vision's §16 rewritten as a short pointer section (its 203-line accretion was the source of
  DOC_OVERCLAIM verdicts) and §18's four questions recorded as settled; delivery prompt at v10.
- **2026-08-23** — W321 reconciliation: §4 + gaps brought current through Rounds 3–6 (W252–W321); suite 274✓/15 skip at the last CI-green run; taxonomy canonicalised frontend+backend; README counts measured.
- **2026-06-20** — Created this living plan. Reconciled current state to 262 routes. Built gaas.v5, Genesis+establish, Sovereign Evolution Office, Resource Fabric this session (see memory). Scorecard initialised.
- **2026-06-20 (later)** — Deep-searched + synthesised the Cowork-agent canon (`CLAUDE_CODE_AGENT_PROMPT_v4`, `workstation_concept_design`, architecture/roadmap masters) → `[[project-workstation-cowork-architecture-canon]]` (7 biomimetic layers, Living Business System, 10 invariants). Built the **Board of Directors** apex tier (`/api/v1/board/*`) — Chief = Owner's digital twin above the AI CEO; integrated a board + chief-of-owner into every generated VSB. Updated §3.3 hierarchy, §4 current state, §9 sources.
- **2026-06-20 (later)** — Created the knowledge canon (`WORKSTATION_IDBO_UNDERSTANDING.md`, `KNOWLEDGE_OPERATING_PROCESS.md`) for Owner+agent alignment. **Owner approved + built the VSB Economic Model** as a living biomimetic economic metabolism (`agentic_core/economy/` + `/api/v1/economy/*`, UI `/economy`): 9 legal forms, biogeochemical profit waterfall, intelligent charity, virtual WST ledger, gaas-gated; entity-type selection wired into Genesis `/establish`. Virtual-money-only (real rails gated).
- **2026-06-20 (later)** — Built the **Vision→Realisation→Transformation engine** (`/api/v1/transformation`, UI `/transformation`): computes vision realisation from LIVE evidence (~92%), derives the transformation plan from gaps, AI `/assess`, continuous `/tick` heartbeat. This is the living embodiment of "your vision · current realisation · transformation plan." 277 routes; tsc 0 errors.
- **2026-06-20 (later)** — Built the **Organism Heartbeat** (`agentic_core/organism/heartbeat.py` + `/api/v1/heartbeat`, UI `/heartbeat`) — a continuous-autonomy **circadian scheduler** that auto-starts at app startup and makes the organism run itself: each beat pulses the **central nervous system**, checks **homeostasis**, ticks the **transformation** engine, and hash-chains to the **UEG** (constitutional audit); expensive AI cognition is opt-in + paced (arms-length). Closed the self-running gap → pillar 5 now **strong**; **overall vision realisation 95.5%**. 282 routes; tsc 0 errors.
- **2026-06-20 (later)** — Built the **Cognition & Alignment** integration capstone (`agentic_core/api/cognition.py` + `/api/v1/cognition`, UI `/cognition`): serves the 4 knowledge layers as live data, maps + verifies the **wiring into all 13 living tiers (100% coherence)**, and `/align` routes each vision gap to the owning tier (Board/Evolution/Change Control), evidence-based + gaas/UEG-governed. The **Heartbeat now runs alignment each beat** (`auto_align`) → the organism continuously self-aligns. 285 routes; tsc 0 errors.
- **2026-06-21 (overnight, autonomous)** — Generated `docs/ACTION_PLAN.md` (now `_archive/docs/ACTION_PLAN.md`) (timed task breakdown). Built **living Business-Plan management** (`/api/v1/business-plan`, router #63): Chief/Board own a living plan for Workstation + per-VSB (mission/strategy/objectives/KPIs/timelines/reviews/progress + Chief-mediated AI generation) — verified end-to-end (298 routes). Added frontend pages for **Business Plan** (`/business-plan`), **Forge** (`/forge-pipeline`), **Compliance** (`/compliance`); tsc 0 errors. Ran an **end-to-end dogfood pilot** establishing a real VSB ("NourishLondon"). Heartbeat continues self-running (auto_align toggle in `/heartbeat`). See `_archive/docs/OVERNIGHT_SESSION_LOG.md`.
- **2026-06-21** — Built the **Forge** (`/api/v1/forge`): 7 digital resources (Petri/Incubator/Laboratory/Factory/Generator/Simulator/Reactor) as a reconfigurable/rerunnable/reusable **swarm-orchestrated cascade pipeline** (AI CEO frame → stages → CoE integrate), gaas/UEG-governed, multi-type outputs for Concept→Commercialisation → **closed the last vision gap; computed realisation now 100%.** Built the **Unified Compliance** engine (`/api/v1/compliance`) federating Sharia/Halal · UK-Legal(London) · Regulatory · EHS · Ethical · Constitutional (existing Jules engines), added to the Resource Fabric. **Owner resolved all open questions** (UNDERSTANDING §9): waterfall approved; virtual-WST-now/Stripe-later; UK/London; entity auto+editable; **charity = WATER/Orphan/Conflict/Dawah, 100%-donation-only** (done in economy/charity.py). Created `DEVELOPMENT_TIMELINE.md` from 999-commit git history.
- **2026-08-12 (W251 reconciliation)** — Hand-reconciled this plan to reality after W77–W250 (the interim record lives in `docs/AUTONOMOUS_PROGRESS.md`, the authoritative cycle log). Highlights folded into §4/§6/§7: native-AI mandate delivered in depth (owned model discovery/routing/tiers/ensemble; hardened memory store); the Resource Fabric executes every composed resource's REAL engine across the whole catalogue (8 PI engines · 8 facilities incl. the vision-exact composite Reactor + the previously-missing Generator · 8 organism systems · the full enterprise/org layer · compliance/consensus/mega/omnimedia/mesh); the VSB Economic Model BUILT (9 legal forms, adjustable waterfall, owner-payments, ventures, living VSBs on the heartbeat — W249: gaas-gated + UEG split-logged + Change-Control materiality holds); W248 healed the §3.3 invariant (every generated VSB carries Board+Chief+economy on ALL spawn paths); frontend converged to the vision IA with honest surfaces. §6.2/§6.3 statuses flipped to match; honest-gaps list refreshed; scorecard re-scored.

---

## 9. Source Document Index (what this synergises — do not duplicate, link)

> Paths re-pointed W448: everything under `_archive/` was moved there in the W153+ docs consolidation and is a
> HISTORICAL source, not a maintained document — the vision prevails where they disagree.
- **Vision/Business:** `_archive/docs/business/{mission_vision_values,autonomous_growth_plan,market_entry_plan,commercial_service_catalog}.md`
- **BMS strategy:** `_archive/docs/bms/BMS-STRAT-001.md`
- **Org charters:** `_archive/docs/charters/` (C-Suite `csuite/`, CoE `coes/`, BTO `transformation_team.md`)
- **Design system:** `_archive/docs/design/DESIGN.md`
- **Architecture:** `_archive/docs/architecture/overview.md` + `_archive/docs/architecture/`
- **Development timeline:** `_archive/docs/DEVELOPMENT_TIMELINE.md` (archived in the W153+ docs consolidation; from git history 2026-02-20 → 2026-06: Jules foundation → convergence → MVP consolidation → sovereign living organism; the ongoing record is `docs/AUTONOMOUS_PROGRESS.md`)
- **Roadmap lore:** `_archive/docs/DEVELOPMENT_PLAN_v7.0_SINGULARITY.md` (horizon, not current state)
- **Constitution:** `_archive/agentic_core/constitution/CONSTITUTION_canonical.md`
- **Cowork-agent canon (external, synthesised):** `…/local-agent-mode-sessions/38f3915a-…/…/outputs/` → `CLAUDE_CODE_AGENT_PROMPT_v4.md` (master briefing: 7 biomimetic layers, Living Business System, 10 invariants, digital-twin modes), `workstation_concept_design.md` (grounded concept design + phased plan), `IDBO_ARCHITECTURE_MASTER_v4.docx`, `WORKSTATION_ADVANCED_ROADMAP_v3.docx`. Note: the referenced `KNOWLEDGE_COMMONS.md` / `WORKSTATION_TRANSFORMATION_PLAN.md` / `CLAUDE_MEMORY.md` were never copied into the repo — *this living plan + agent memory now serve that role.*
- **Agent memory (authoritative, current):** `[[project-workstation-vision]]`, `[[project-workstation-architecture-unified]]`, `[[project-workstation-cowork-architecture-canon]]`, `[[project-workstation-current-state]]`, `[[project-workstation-gaas-v5-and-phase4]]`, `[[project-workstation-genesis-and-sovereign-evolution]]`, `[[feedback-workstation-working-mandate]]`
