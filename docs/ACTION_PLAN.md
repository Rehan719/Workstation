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

## Progress Log (this session)
- **2026-06-21 (overnight)** — Plan generated (T1). Executing T2→T8 autonomously; see `WORKSTATION_IDBO_LIVING_PLAN.md` §8 + the overnight session log for verified outcomes.
