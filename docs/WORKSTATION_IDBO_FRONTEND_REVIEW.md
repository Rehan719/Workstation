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

### ⏳ Next cycles (planned, one section per cycle — review outputs, then keep/fix/consolidate/archive)
- **Governance & Ops** extras — `ab-testing`, `learning-dashboard`, `audit-dashboard`, `grand-ops`
  (no backend fetch): verify; consolidate dashboards, archive thin ones.
- **Home** cluster — `grand-ops` / `introspection` / `organism` / `heartbeat` / `cognition`: confirm each
  shows real organism data; consolidate overlapping dashboards.
- **Resource Fabric** cluster — confirm `synthesis`/`nexus`/`forge-pipeline`/`reactor`/`incubator`/
  `intelligence`/`authorship`/`design-dev`/`solutions` each produce a coherent output or fold into the
  Resource Fabric.
- **Core KEEP set (verified vision-delivering):** Genesis Journey · Resource Fabric · Reactor Studio ·
  Deliverables · Swarm Intelligence · Native AI · Domains + 6 domain hubs · VSB Spawn/Cockpit ·
  Business Plan · Compliance · Governance Hub · Board/AI-CEO · Transformation · Organism.

## Principle
Every page in the final nav must answer: **which §-vision capability does this deliver, and does its
output prove it?** If it can't, it is consolidated or archived. The unified UI is the §1–§17 vision made
navigable and coherent — nothing more, nothing decorative.
