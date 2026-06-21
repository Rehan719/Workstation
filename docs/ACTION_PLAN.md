<!--
  DETAILED ACTION PLAN — Workstation IDBO
  Objective → Strategy → Gap → timed task breakdown. Living artifact; updated as work proceeds.
  Companion to WORKSTATION_IDBO_LIVING_PLAN.md (vision↔state↔action) and DEVELOPMENT_TIMELINE.md (history).
  Status: LIVING · started 2026-06-21 (autonomous overnight session)
-->

# Workstation IDBO — Detailed Action Plan

## Objective
Deliver the **commercially-ready, launch-ready realisation** of the Workstation IDBO vision: an AI-mediated, intelligently-autonomous, living biomimetic organism that takes any user's challenge end-to-end (Concept → Design → Delivery) and **generates a bespoke living VSB IDBO entity** (with its digital twin) to commercialise the solution — self-running, self-improving, governed, and beneficent.

## Strategy
1. **Close the vision↔reality gap** — the Transformation engine computes realisation from live evidence; build to close each remaining gap.
2. **Dogfood the IDBO** — wherever building is hard, use Workstation's own Concept→Commercialisation workflow (Genesis → Forge → establish → economy/board/twin) to design + pilot it.
3. **Launch-ready standards** — every increment real + verified (boot/tests/tsc/endpoint); honest (no fabrication); governed (gaas/UEG); virtual-money only until the Owner enables Stripe.
4. **Owner sovereignty** — the Chief (Owner's digital twin) + Board own the living business plan; the Owner monitors via the Living Plan + Transformation + Business-Plan dashboards.

## Gap (current state — 2026-06-21, updated)
Computed vision realisation: **100%** (live evidence) for the 11 core pillars. Structural transformation is **complete and operationally verified** (64 pages swept clean; 71 integration tests pass; backend boots live; all AI endpoints bounded). Status of the build-out items:
- ✅ **Living Business-Plan management** (Chief + per-VSB) — built, verified (`/api/v1/business-plan`).
- ✅ **Forge + Compliance frontend pages** — built, sidebar-wired, swept clean.
- ✅ **End-to-end pilot** — "NourishLondon" VSB established with board+twin+economy, gaas-governed.
- ✅ **Frontend↔backend integration** — 18 previously-broken endpoints wired; venv/jose boot crash fixed; AI-gateway hangs bounded; 3 latent SM-2 overflow bugs fixed; smoke coverage added.
- ⛔ **Real-money rails (Stripe)** — **GATED on Owner** (virtual-only until directed).
- ⛔ **Production deployment hardening** + **live AI key** in the running env — **Owner-gated** (next phase).
- ◯ Forward (non-gated, ongoing): deeper engine integration into synthesis workflows; per-VSB business plans; more role automation; broader POST-path test coverage.

> **Conclusion:** the planned **structural transformation is done**. What remains is either Owner-gated (launch/commercial) or ongoing incremental depth — there is no remaining non-gated *structural* gap. See `docs/AUTONOMOUS_PROGRESS.md` for the continuous-cycle log.

---

## Validated current state (2026-06-21 — landed on `main`)
- **Phase 1 integration arc is COMPLETE and merged to `main`** (PR #354, fast-forward, pushed). 14 commits.
- **Frontend↔backend wiring: 61/61 prefixes wired, 0 broken** — every frontend API call resolves to a real `agentic_core` route.
- Backend boots clean (**313 routes**); **78 integration tests pass / 0 fail**; production build `tsc && vite build` clean; **64 pages swept** (0 errors).
- Transformation engine: `overall_realisation = 1.0` (11/11 pillars). All financial flows **virtual/simulated only**.

## Phases & Task Breakdown

### Phase 1 — Integration & Hardening — ✅ COMPLETE (landed on `main`)
T1 action plan · T2 Living Business-Plan API · T3–T5 Business-Plan/Forge/Compliance UIs · T6 end-to-end pilot ("NourishLondon" VSB + twin + economy) · T7 heartbeat autonomy · T8 doc reconcile — **all done**. Plus: 18 broken endpoints wired (integration surface), venv/`jose` boot-crash fixed, AI-gateway hangs bounded, 3 latent SM-2 overflow bugs fixed, +24 tests, bundle code-split, README reconciled.

### Phase 2 — Depth & Coverage (non-gated; ready to start) ◻
- Per-VSB living business plans wired into each generated entity's lifecycle.
- Deeper embedding of compliance + process-intelligence engines into every synthesis/generative workflow.
- Broader automated test coverage (AI-path contract tests behind a key; more POST flows).
- Persistence hardening (SQLite → Postgres) for concurrent writes.
- More automation of functional roles + scheduled evolution cycles.

### Phase 3 — Launch / Commercial — ⛔ OWNER-GATED
- **Real-money rails (Stripe)** behind compliance/KYC — virtual/simulated until the Owner enables.
- **Production deployment hardening** + CI/CD (Render/Vercel), observability, multi-tenant scale.
- **Live AI key** in the running environment → real end-to-end dogfood (replaces labelled fallbacks).
- Public launch: marketing site, onboarding, billing, support; cross-VSB federation & marketplace.

---

## EXPANDED TRANSFORMATION PLAN — Whole-Vision Workstreams (scope · scale · complexity)
> Authored 2026-06-21 from the Owner's "deliver the **whole platform**" directive. Grounded in
> `WORKSTATION_IDBO_WHOLE_VISION.md` (the fine-resolution vision). These workstreams *expand* the plan
> beyond integration/depth to realise the complete IDBO. **W1 is the headline new direction.**

### W1 — ★ Native AI Resource Fabric (own Swarm · Models · Orchestration) — NEW, highest scope
**Why:** the AI Agent Swarm must NOT be "just lots of API calls" to external providers — that creates
dependency, expense, latency, staleness, and loss of control. Workstation must **own** its core AI
capability as dynamic, adaptable, responsive, reconfigurable resources (Whole-Vision §6).
- **W1.1 Native model serving** — make models that Workstation owns/runs first-class (local/self-hosted
  runtime, e.g. an Ollama-class or embedded inference layer the platform controls), with external
  providers demoted to *optional accelerants behind a flag*, never dependencies.
- **W1.2 In-platform Orchestrator** — an owned orchestration engine that composes agent/model/resource
  cascades (not a thin gateway): routing, scheduling, retries, caching, cost/latency governance, and
  graceful degradation — biomimetically mediated (nervous/immune/metabolic), gaas-governed.
- **W1.3 Swarm Engine** — compose **bespoke-per-solution** agent-cascade trees (synthesised, modelled,
  simulated to each solution's needs AND to each founder's digital twin), reconfigurable + reusable.
- **W1.4 Reconfiguration + design control** — users compose/reconfigure swarm cascades, models, and the
  org structure in Synthesis Lab / Build-to-Order / Forge; the platform models+simulates a configuration
  before commit (digital-twin pre-validation).
- **W1.5 Optimisation** — cascades/models/resources are optimised (efficiency, cost, latency, quality),
  verified · tested · validated; knowledge/expertise accrues from experience (learning organism).
- **Acceptance:** Workstation can run a full Concept→Commercialisation cascade producing real
  (non-fallback) AI output **without any external API key set**, using its own resources; external
  providers, when present, only accelerate.

### W2 — Bespoke VSB organisation + resource synthesis (user design control)
Deepen Genesis/BTO/Forge so each generated VSB's **organisation structure AND digital resources/swarm
cascades** are specifically designed · modelled · simulated · optimised for the solution and editable by
the user — reconfigurable org charts, resource compositions, and swarm trees, with twin pre-validation.

### W3 — Full multimodal, enterprise-aware avatar + AI-CEO/Chief interaction
Complete the avatar as the platform-wide, enterprise-aware interaction surface: multimodal (text/voice/
image) dialogue with the **Chief** and **AI CEO**, plus guided navigation/reconfiguration of any area;
continually reconfigurable, function-specific, intuitive, optimised, all-language, personalised UI.

### W4 — Living deliverables (every output a living enterprise)
Make each output type (Report · Presentation · Video · Website · Platform · App · Product · Service) a
**living, reconfigurable, continually-developing** enterprise instance — selectable, combinable,
integrable — rather than a static artefact.

### W5 — Continuous operational excellence + learning organism
Wire the BMS/QMS/DCS/EMS + Sovereign Evolution + heartbeat into a measurable **operational-excellence**
loop: live monitoring/evaluation of effectiveness, efficiency, performance, profitability, satisfaction,
founder-alignment and compliance → autonomous improvement (process/scientific/technical/operational),
with knowledge/expertise built from experience, evidence and live research.

### W6 — Depth, persistence, scale, launch-readiness (absorbs Phase 2/3)
Domain AI depth across all Realm × Domain; persistence hardening (SQLite/Postgres); broader test
coverage (incl. AI-path contract tests once W1 provides native AI); observability; and the gated launch
items (Stripe, production deploy) when the Owner directs.

**Sequencing:** W1 is foundational (it changes what every other AI-mediated workflow runs on) and is the
priority. W2–W5 build the bespoke/living/multimodal/operational depth on top of W1. W6 runs continuously.
Each workstream decomposes into timed, resourced tasks owned by the VSB delivery org (Board → AI CEO →
C-Suite → CoE → BTO), and — true to the vision — is itself delivered **through** the Transformation
Orchestration cascade where practical (dogfooding).

---

## Progress Log (this session)
- **2026-06-21 (overnight)** — Plan generated (T1). Executing T2→T8 autonomously; see `WORKSTATION_IDBO_LIVING_PLAN.md` §8 + the overnight session log for verified outcomes.
