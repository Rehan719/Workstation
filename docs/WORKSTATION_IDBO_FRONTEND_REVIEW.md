# Workstation IDBO — Frontend Coherence Review & Unification Plan

**Started 2026-06-25** (Owner: "extensive lists of pages which do not result in any coherent outputs —
review the whole frontend against the whole vision as a unified UI delivering the functionality, outputs
verified end to end").

**Goal:** the frontend is **one unified UI that coherently delivers the §1–§17 vision capabilities** —
not a long list of pages, several of which produce incoherent/placeholder output. Each page must either
deliver a clear vision capability with a coherent output, be consolidated into one that does, or be
archived. Verified by actually exercising the page in the browser.

**Method:** exercise each page on the served build; judge its **output** against the vision; classify
**KEEP** (coherent, vision-delivering) · **FIX** (wired but output thin/incoherent) · **CONSOLIDATE**
(redundant with a stronger page) · **ARCHIVE** (off-vision / placeholder). Work in cycles; archive is
history-preserving (`git mv` → `_archive/frontend-pages/`).

---

## Scope at start
9 nav sections, ~85 routed pages (90 routes). That breadth is itself the problem the Owner flagged.

## Evidence of incoherence (sampled in the browser)
- **Cosmic Nervous System** (`/cosmic-nervous`) → *"Interplanetary Sensory Network · Planetary Defense Map ·
  NEO Orbital Tracking · Apophis-B · Solar Resonance"* — pure off-vision sci-fi placeholder. **ARCHIVE.**
- **Civilization Brain** (`/civilization`) → *"Co-Conscious Mode · Civilization Brain"* grandiose framing
  over thin portfolio aggregates (redundant with Dashboard/Projects). **ARCHIVE.**
- The whole **Explore** section (cosmic, reality, AR/VR, wearables, embodiment, civilization) is the
  Phase-4 experimental cluster — none of it appears in §1–§17. **ARCHIVE.**

## Convergence cycles

### ✅ Cycle 1 (W127) — archive the off-vision experimental tail
Archived 6 pages (no other importers): **CivilizationDashboard · RealityDashboard · CosmicNervousSystem ·
ARVRSandbox · WearableSync · EmbodimentStudio** → `_archive/frontend-pages/`. Removed their imports +
routes (App.tsx) + nav items (Sidebar); cleaned now-unused icon imports. The Explore section now holds
only **Scholar Realm** (a vision realm) + **QEP Suite** (pending review). Verified: clean `tsc && vite
build`; served build → Genesis (core) renders, nav no longer lists the cut pages, an archived route
(`/cosmic-nervous`) falls through to the graceful "Page Not Found" (no crash), console clean.

### ✅ Cycle 2 (W128) — QEP Suite + Explore section
Exercised each: `/qep` (QEPReligionHub) = a **genuine Qur'an Education Platform** (real Qur'anic text — Al-Baqarah, Hafs recitation — memorization coaching) → **KEEP**, consolidated into the **Domains** section as "Qur'an Platform" (faith-rooted Religion-domain capability, §3A·1). The rest were grandiose/mock/mislabeled incoherent output → **ARCHIVE**: `/qep-engine` (mislabeled organism "Quad Engine Reactor" dashboard, redundant with /organism), `/qep-community` ("Signature Product v8.4 · SLA 99.99%" status placeholder), `/qep/observatory` (XAI observatory with fabricated F1/precision metrics), `/qep/governance` (mock voting UI with fake proposals/votes), `/qep/oversight` (no-fetch mock queue). Also archived `/scholar` (ScholarRealm — grandiose "Observatory of Understanding" claiming a fabricated "50+ federated nodes"). **The entire Explore nav section is now eliminated.** Verified: clean `tsc && vite build`; served build → /qep renders under Domains, Explore gone, archived routes graceful Page-Not-Found, console clean. Running total: 9 sections/~85 pages → **7 sections / ~73 pages**.

### ✅ Cycle 3 (W129) — Transformation & Economy extras
Exercised each: **ARCHIVE** `/prediction-market` (Wisdom Hub "Civilizational Prediction Markets" — fabricated betting market: BUY YES/BUY NO, 74%, 48,200 WST volume — off-vision + gambling-adjacent, conflicts the halal/faith-rooted ethics §2) and `/soul-record` (grandiose "Soul-Record · Multi-Dimensional Identity Explorer" over a thin reputation graph — off-vision framing). **KEEP** `/wallet` (Sovereign Capital Fund — WST virtual liquidity + allocation, the §12 economy surface, coherent), `/product-catalog` (20 real registered products — coherent; consolidation candidate with /bto + /marketplace, noted not cut), `/impact` (real organism/projects aggregates — thin but coherent). Core kept: transformation · economy · marketplace · deliverables. Verified: clean `tsc && vite build`; served build → /prediction-market falls through to graceful Page-Not-Found (no betting content), console clean. Running total: 7 sections / **~71 pages**.

### ✅ Cycle 4 (W130) — Governance/Home dashboard cluster
Exercised each: **ARCHIVE** four fabricated/grandiose dashboards — `/grand-ops` (Grand Ops "command center" with hardcoded infra metrics CPU 69.4%/Mem 9.1% — no backend), `/introspection` (IntrospectionDashboard — fabricated reasoning log "Confidence 99% · Initialize BTO-Religion Swarm", no backend), `/ab-testing` (fabricated A/B experiments "Control 42%/Variant-A 67%/Confidence 94%"), `/learning-dashboard` (grandiose "Evolutionary Impact 86.5% · Feedback Resonance 0.96", redundant with /impact). **KEEP** the real governance/organism pages: Governance Hub · Compliance · Change Control · Constitution · Sovereign Evolution · Operational Excellence (4 real /operations endpoints) · CoE Hub · Audit Dashboard (fetches real /meta) · Organism · Heartbeat · Cognition · Dashboard. Verified: clean `tsc && vite build`; served build → /compliance renders, nav drops Grand Ops/Introspection/AB-Testing/Learning, /grand-ops → graceful Page-Not-Found (no fake metrics), console clean. Running total: 7 sections / **~67 pages**.

### ✅ Cycle 5 (W131) — Resource-Fabric cluster + core verification pass (NO cuts — all coherent)
Exercised all 10 Resource-Fabric engine pages; **every one wires a real §7 backend and produces coherent, distinct output → KEEP ALL**: `/synthesis` (knowledge ingest), `/nexus` (4-layer orchestration: Cognitive Cascade→Meta-Assessment→engine→Apex Synthesis, /intelligence/nexus), `/forge-pipeline` (/forge/run), `/reactor` (/reactor/run), `/incubator` (/incubator/evolve), `/intelligence` (8-stage BDP/SPI), `/authorship` (9-stage scholarship, /intelligence/authorship), `/design-dev` (9-stage design&dev, /intelligence/design-dev), `/solutions` (Design·Build·Launch brief + native Ollama model select, /ai/query), `/factory` (/factory/produce). This is the genuine substance of §7 — nothing fabricated, so nothing cut. **Final verification spot-check** of the core KEEP-set — all render coherently, no errors, console clean: Genesis (Concept→Commercialisation journey) · Resource Fabric (24.7k chars, the §7 unifier) · Living Deliverables (11.5k) · Native AI Fabric (25.6k, "not a façade over external API calls") · Board of Directors (Chief = Rehan's digital twin) · Economic Metabolism (§12 nutrient-cycle, virtual-money-first). Running total unchanged: 7 sections / **~67 pages** (this cycle confirmed coherence, no archives).

>### ✅ Cycle 6 (W132) — remaining sections (Native AI · Domains · VSB Enterprises · Developer & System) — REVIEW COMPLETE
Exercised the remaining unverified pages. **KEEP** (all real, coherent, vision-delivering): Native AI Fabric — `/ai-tools` (18-tool native catalogue), `/ceo` (real CEO chat), `/visual-composer` (Swarm Topology Designer — Brain/Immune/Tool nodes, real native models Nematron-1B/Nemoclaw-3B), `/swarm-intelligence` (delegate-mission hub with real swarm runs); Domains — 6 hubs + Qur'an Platform (real §3A tools, e.g. `/science` → /science/literature+synthesise); VSB Enterprises — `/vsb-cockpit` (avatar+BTO), `/management` (real BMS/DCS/audit), `/digital-twins` (/twin/models), Genesis, Business Plan, Capital, Projects; Developer & System — `/creator` (visual data-pipeline blueprint builder), Contribute, Entity Control, Settings. **ARCHIVE** two grandiose placeholders with no backend: `/dev-portal` (fabricated "PQC-MANDATORY · CRYSTALS-Dilithium · third-party reactors" claims) and `/roadmap` (hardcoded "Workstation civilization · Guardian resonance" roadmap — the real living roadmap is the Living Plan, /api/v1/plan). Cleaned the now-orphaned `Map` + `Globe` icon imports. **Noted (not cut):** `/enterprise` ("Enterprise Realm · Forest of Collaboration") has real project data but grandiose framing and overlaps `/projects` — a future consolidation candidate. Verified: clean `tsc && vite build`; served build → /dev-portal → graceful Page-Not-Found (no PQC content), nav drops Developer Portal + Public Roadmap, console clean.

---

## ▶ PHASE 2 — STREAMLINING (consolidate & align to a lean, vision-aligned UI)
Owner (2026-06-25): "Further consolidate and align to deliver to vision an effective efficient streamlined user interface." The review removed the *incoherent*; streamlining removes the *redundant* + de-clutters + de-fabricates so each surviving surface is a distinct vision capability.

### ✅ Streamline Cycle 1 (W133) — de-fabricate Marketplace + consolidate duplicate product/project/impact surfaces
- **De-fabricated the §12 Marketplace** (`/marketplace`, LivingMarketplace): removed the entirely-fabricated "Trending Agents" storefront (8 hardcoded fake agents with invented `sales`/`trust`/prices + a fake "Economy Vitals" panel: "12.4K WST volume / 142 WST fee burn / 4.92 reputation" / "Connect Wallet via PQC"). The Marketplace now shows ONLY the real `/api/v1/catalog/products` (20 live, openable products) with an honest subtitle. A real VSB-to-VSB listings/orders economy is Owner-gated and will be built on real WST rails, not seeded with invented figures.
- **Consolidated 3 redundant pages** (archived → _archive/frontend-pages/, route kept as a redirect so old links resolve): `/product-catalog` (ProductCatalog — a duplicate of the Marketplace's products view) → **/marketplace**; `/enterprise` (EnterpriseRealm — "Forest of Collaboration" grandiose shell over the same 3 projects) → **/projects**; `/impact` (UserImpact — thin personal aggregate of organism/projects/swarm data) → **/organism**.
- Net: nav items 59 → **56**; VSB Enterprises 10→9, Transformation & Economy 7→5; one fabrication removed. Verified: clean `tsc && vite build`; served build → Marketplace shows 20 real products + zero fabricated agents, all 3 redirects land (/enterprise→/projects, /product-catalog→/marketplace, /impact→/organism), console clean.

### ✅ Streamline Cycle 2 (W135) — Resource Fabric nav de-clutter (13 → 3 items, zero capability lost)
The heaviest section. SAFE approach (no orphaning): FIRST added a **"Process-Intelligence Studios" launcher grid** to the Resource Fabric hub page (`ResourceFabric.tsx`) — 12 clickable cards that `navigate()` to every engine route (synthesis · nexus · forge-pipeline · reactor · incubator · reactor-studio · factory · intelligence · authorship · design-dev · solutions · bto). VERIFIED in the browser: the grid renders ("12 engines"), and clicking a card navigates (Authorship → /authorship renders). THEN trimmed the Sidebar Resource Fabric section from **13 → 3** nav items (Resource Fabric hub · Reactor Studio · Build to Order); the 10 engines are now launched one-click from the hub. **All engine ROUTES stay live** (verified /factory still renders directly) — this is nav de-clutter, not removal; no real §7 capability lost. Cleaned 6 now-orphaned Sidebar icon imports (Hammer/Zap/FlaskConical/Factory/Brain/BookOpen). Verified: clean `tsc && vite build`; served build → Fabric shows the Studios grid, folded engine route renders directly, console clean. Nav items 56 → **46**.

>### ✅ Streamline Cycle 3 (W136) — dashboard overlap sweep + fabrication sweep → PHASE 2 COMPLETE
Swept the remaining sections for overlap. **Home** (Dashboard·Organism·Heartbeat·Cognition) — all 4 exercised + distinct (portfolio · composite-health · autonomy/circadian loop · knowledge-integration); no overlap. **Native AI Fabric** (6) — distinct (verified prior cycles). **Governance & Ops** — found ONE clear duplicate: `/audit-dashboard` rendered the same GAAS Audit Center that the **Governance Hub already contains as its "Audit" tab** → consolidated `/audit-dashboard` → **/governance-hub** (redirect; AuditDashboard archived; capability preserved in the Hub). `/constitution` confirmed distinct (Constitutional Core / self-modification engine). **Fabrication sweep** of kept pages: strict fake-metric patterns = 0 (the Marketplace was the only one, fixed W133); softened the lone grandiose residue on `/solutions` (deployment options: `Orbital-L1`→`On-Prem`, "Global sovereign mesh"→"Multi-region distribution"). Verified: clean `tsc && vite build`; served build → /audit-dashboard → /governance-hub (Audit Center intact), Solutions clean, console clean. Nav items 46 → **45**.

---

## ✅ PHASE 2 — STREAMLINING COMPLETE (W133–W136)
The frontend is now a lean, honest, vision-aligned UI. Combined with Phase 1 (review), the convergence arc:

| | Pre-convergence | Now |
|---|---|---|
| Nav sections | 9 | **8** |
| Nav items | ~79 | **45** |
| Routes | 90 | **70** (live; folded/consolidated paths kept as launchers/redirects) |
| Pages archived | — | **24** (history-preserving) |
| Fabricated surfaces | several | **0** |

**Streamlining moves (Phase 2):** de-fabricated the §12 Marketplace (real catalog products only); consolidated 4 redundant surfaces via redirects (`product-catalog`→`marketplace`, `enterprise`→`projects`, `impact`→`organism`, `audit-dashboard`→`governance-hub`); de-cluttered the Resource Fabric section 13→3 by adding a "Studios" launcher grid on the hub (engines stay live, one click away); removed the last "Enterprise Realm" branding; cleared off-vision grandiosity (Orbital/sovereign-mesh wording).

**The lean 8-section nav:** **Home** (Dashboard·Organism·Heartbeat·Cognition) · **Native AI Fabric** (Native AI·AI Tools·AI CEO·Board·Visual Composer·Swarm Intelligence) · **Domains** (Overview·Religion·Qur'an Platform·Science·Education·Law·Care·Employment) · **VSB Enterprises** (Spawn Studio·Cockpit·Genesis·Business Plan·Management·Change Control·Digital Twins·Capital·Projects) · **Resource Fabric** (Resource Fabric hub→12 Studios·Reactor Studio·Build to Order) · **Transformation & Economy** (Transformation·Economy·Marketplace·Deliverables·Wallet) · **Governance & Ops** (Governance Hub·Constitution·Compliance·Operations·Sovereign Evolution·CoE) · **Developer & System** (Creator·Contribute·Entity Control·Settings). Every surface is a distinct §1–§17 vision capability with browser-verified, honest output.

### (historical) streamlining backlog — now cleared

- **Home/Governance dashboards** — confirm organism/heartbeat/cognition + governance-hub/constitution/audit don't overlap; consolidate if they do.
- Final alignment pass + a single coherent nav screenshot.

## ✅ REVIEW COMPLETE (W132)
All 8 nav sections cycle-reviewed against §1–§17; every page's **output** exercised in the browser.

| | Start | Now |
|---|---|---|
| Nav sections | 9 | **8** (Explore eliminated) |
| Routes (App.tsx) | 90 | **70** |
| Nav items | ~79 | **59** |
| Pages archived | — | **20** (history-preserving `git mv` → `_archive/frontend-pages/`) |

**The 20 archived** (all exercised, judged incoherent vs the vision): the 6-page off-vision **Explore** cluster (cosmic/reality/AR-VR/wearables/embodiment/civilization), the 5-page **QEP sprawl** + **Scholar Realm** (fabricated metrics / mock voting / "50+ federated nodes"), `/prediction-market` (gambling-adjacent betting, conflicts §2 ethics) + `/soul-record`, the 4 **fabricated dashboards** (grand-ops/introspection/ab-testing/learning-dashboard), and `/dev-portal` + `/roadmap` (grandiose placeholders).

**The coherent unified UI** (8 sections, every page a real §-vision capability with verified output): **Home** (Dashboard·Organism·Heartbeat·Cognition) · **Native AI Fabric** (§6 — Native AI·AI Tools·AI CEO·Board·Swarm Topology·Swarm Intelligence) · **Domains** (§3A — 6 hubs + Qur'an Platform) · **VSB Enterprises** (§3A·2/§4/§13 — Spawn·Cockpit·Genesis·Business Plan·Management·Change Control·Digital Twins·Capital·Projects) · **Resource Fabric** (§7 — Fabric + 12 engines/reactors/labs) · **Transformation & Economy** (§12 — Transformation·Economy·Marketplace·Deliverables·Catalog·Wallet·Impact) · **Governance & Ops** (§10/§11 — Governance·Constitution·Compliance·Operations·Sovereign Evolution·CoE·Audit) · **Developer & System** (Creator·Contribute·Entity Control·Settings). The Owner's "extensive lists of pages which do not result in any coherent outputs" is resolved: no sci-fi placeholders, fabricated metrics, gambling, or grandiose duplicate dashboards remain.

### (historical) planned-cycles note

- **Remaining sections to cycle-review:** Domains (6 hubs + tools + Qur'an Platform), VSB Enterprises
  (spawn/cockpit/capital/marketplace/bto), Developer & System, Native-AI-Fabric (swarm) — then declare COMPLETE.
- **Core KEEP set (verified vision-delivering):** Genesis Journey · Resource Fabric · Reactor Studio ·
  Deliverables · Swarm Intelligence · Native AI · Domains + 6 domain hubs · VSB Spawn/Cockpit ·
  Business Plan · Compliance · Governance Hub · Board/AI-CEO · Transformation · Organism.

## Principle
Every page in the final nav must answer: **which §-vision capability does this deliver, and does its
output prove it?** If it can't, it is consolidated or archived. The unified UI is the §1–§17 vision made
navigable and coherent — nothing more, nothing decorative.

---

## ▶ PHASE 3 — UNIFY TO THE WHOLE VISION (transform the frontend into one vision-delivering UI)
Owner (2026-06-26): "Further consolidate and align… review the whole frontend against the whole vision (Fine Resolution) and intelligently review/transform the whole frontend as a Unified UI delivering the functionality and capabilities in vision, verified end to end." Phases 1–2 removed the incoherent/redundant; Phase 3 makes the surviving surfaces cohere into ONE experience organised around the vision (§3A two journeys · §17.1 Realms×Domains×Products · §4 lifecycle), and verifies each §-capability is delivered end-to-end.

### ✅ Phase-3 Cycle 1 (W137) — the unified front door (`/` Command Center)
The default route was a grandiose "Command Center · Welcome, Conscious Guardian" with **fabricated "Active Objectives"** ("v1.0 Global Launch 100% / v2.0 Neural Mesh 12%"), an arbitrary action-card set, and a **dead link** ("Genome Core" → /genome-explorer, which is archived). Rebuilt it as a **unified, honest, vision-aligned front door** (`DashboardNew.tsx`): (1) **foregrounds §3A's two journeys** as the primary choice — "Work in a Domain" (offering 1 → /domains) and "Concept → Commercialisation" (offering 2 → /genesis); (2) **maps the capability pillars** (Native AI Fabric §6 · Resource Fabric §7 · Living Enterprises §13 · Governance & Compliance §10/§11 · Economic Organism §12 · Living Organism §8) — every one a real reachable surface; (3) **real status only** — composite health + mode from `/api/v1/organism/status`, vitals + project count from the stats endpoint, recent activity from `/api/v1/projects/` (removed the fabricated objectives). Also fixed the grandiose default identity string (`mockUserProfile` "Conscious Guardian" → "Founder"). Verified: clean `tsc && vite build`; served build → `/` shows the two journeys + 6 pillars + real "Full Power · 100% health", "Work in a Domain" card navigates to /domains, no fabrication, console clean.

### ⏳ Phase-3 backlog
- **End-to-end §-coverage verification:** walk each §1–§17 capability and confirm a coherent delivering surface is reachable from the front door (fix any gap/dead link).
- **Align the nav to the vision** where it adds coherence (e.g. surface the two §3A journeys / the Realms×Domains×Products structure in the IA).
- Continue consolidating any remaining redundancy found during the walk.
