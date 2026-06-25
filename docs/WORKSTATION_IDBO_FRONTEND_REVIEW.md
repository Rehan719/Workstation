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
