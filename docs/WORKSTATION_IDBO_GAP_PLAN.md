# Workstation IDBO — Vision Gap Plan (fine resolution)

**Reviewed: 2026-06-25** · against `WORKSTATION_IDBO_WHOLE_VISION.md` §1–§17 · HEAD at review = post-W118.

A prioritised, ranked, categorised assessment of the live system vs. the Whole Vision, plus the
execution plan. Honest by construction: "delivered" means reachable + verified end-to-end (route renders,
suite green, in-house provenance, no fabrication); "designed/gated" means intentionally not built yet.

---

## A — DELIVERED to fine resolution (verified end-to-end)

| § | Capability | Evidence |
|---|---|---|
| §3A·1 | Domains — domain-specific AI-mediated tools/resources | 18+ domain tools, native-AI-first |
| §3A·2 | Concept→Commercialisation → living VSB | Genesis journey + `/establish`, QMS-gated (W109) |
| §4 | End-to-end lifecycle | Genesis 3-phase, governed + UEG-sealed |
| §5 | Living Organisation (Chief→Build-to-Order) | cascade: Chief→Board→AI CEO→full C-Suite (each→CoE, user-reconfigurable)→BTO→products; each tier appraises/develops the one below (W104–W107) |
| §6 | Workstation's OWN AI swarm/models/orchestration | native fabric; in-house-first; per-stage `served_by`; selfcheck all_live |
| §7 | Reconfigurable Resource Fabric + Digital Resources (user design control) | select · per-resource param editor (incl. §5 csuite_roles + Reactor Temperature/Mutation/Iteration) · combine · **model & simulate before commit** · QMS-gated+doc-controlled commit · **run on native swarm**. Reactor trilogy: Incubator (W115) · Experimentation (W116) · Studio 2D/3D (W117) |
| §8 | Biomimetic living-organism | 7 layers + immune/circadian attached to every delivery via the living-QMS capability |
| §9 | UX — multimodal, enterprise-aware, reconfigurable | enterprise-aware avatar (multimodal) + reconfigurable Resource-Fabric/Studio surfaces |
| §10 | Solution-Quality Bar | `assure_delivery` (16-criteria bar + real QMS gate) on cascade, Deliverables, Genesis, compositions, experiment, studio |
| §11 | Compliance, Safety & Ethics (continuously live) | **woven into the universal `assure_delivery` gate (W118)** — Halal·Legal·Regulatory·EHS·Ethical screened on EVERY delivery, "not bolted on"; gaas.v5 constitutional gate on the org cascade |
| §13 | Living deliverables | re-runnable, reconfigurable, versioned, QMS-gated |
| — | QMS owns DCMS (ISO 9001 §7.5) | quality records document-controlled → `quality_record_hash` (W110) |
| §17.4 | Human–AI integration **Mode 3** — optional per-stage human review gates (set in the VSB genome) | per-VSB `review_gates` config + human approve/reject decisions, each append-only DCS-audited; `blocks_progress` lets the lifecycle honour the gate (W126) |
| §17.3 | Living Business System — 4 layers (Constitutional · Strategic · Action Plan · **Board Pack**) | the on-demand **Board Pack** (`POST /api/v1/vsb/{id}/board-pack`) is assembled fresh from the VSB's live data + an in-house AI-CEO narrative, **DCS-registered** (document-controlled via the QMS-owned DCMS), with history (W125) |

## B — OWNER-GATED (designed; do NOT build without the Owner's explicit go-ahead)

| Rank | Item | Why gated |
|---|---|---|
| B1 | §12 Economic Organism with **real money rails** (profit share, reinvest, charity distribution) | Virtual-money-first safeguard; spec in `VSB_ECONOMIC_LEGAL_MODEL.md`; awaiting Owner approval |
| B2 | Live Stripe (`sk_live_`) / real payments | Owner's account + real funds |
| B3 | Managed Postgres (durable DB) | Owner's infra + cost |
| B4 | Production deploy / hosting | Owner's infra + cost |
| B5 | Live external AI key (frontier accelerant) | Owner's account + cost; in-house-first remains default |

## D — NEW vision element (added by Owner 2026-06-25) — HIGH priority, substantial, scope before building

| Rank | Item | § | Current state (honest) | Scope |
|---|---|---|---|---|
| ~~**D1**~~ ✅ **COMPLETE (W121–W124)** | **VSB IDBO Entity Repository** — a living, intelligently-autonomous enterprise bespoke to the concept→commercialisation solution, shipped as a version-controlled **repo** with an **integrated Website + Web app + Phone (mobile) app** | §13 | **All 4 increments DONE.** (1) `POST /api/v1/vsb/{id}/repo` — on-disk version-controlled repo from entity data (W121). (2) `…/website` — real multi-page static site into `web/`, served at `…/website/page/{name}` (W122). (3) `…/webapp` — interactive client-side app into `webapp/`, served+runnable at `…/webapp/page/{name}` (W123). (4) `…/mobile` — real installable **PWA** (manifest + service worker + icon + mobile-first app) into `mobile/`, served at `…/mobile/page/{name}` (W124). All QMS-gated + §11-compliance-screened + document-controlled; each has a Generate-* action on the Genesis page; the Website/Web-app/Phone-app are real, served, runnable artifacts. | DONE. (Honest scope: the Web app + Phone app are client-side apps / a PWA — real, runnable, installable+offline-capable when hosted — never fabricated compiled native apps; nothing is deployed/hosted by the platform.) |

## C — CANDIDATE further-depth increments (genuine but lower-priority; confirm scope before building)

| Rank | Item | § | Notes |
|---|---|---|---|
| C1 | Autonomous self-improvement of living deliverables on the heartbeat (deliverables "keep researching/improving") | §13 | heartbeat autonomy partly exists; deeper loop is heavier — confirm before building |
| C2 | Surface the §8 homeostasis loops (immune↔nervous↔metabolic) as a live organism dashboard | §8 | visualization; the data exists |
| ~~C3~~ ✅ | Compliance badge rolled out to all delivery surfaces (cascade · Genesis · composition-run · simulate-preview · studio) | §11 | done W119 — every delivery panel now shows the `compliance: pass/review/fail` badge |
| C4 | Personalisation to user history/preferences across the UI (§9 "personalised to each user") | §9 | needs a user-prefs store; moderate |
| C5 | Broader robustness/test sweeps as new surfaces age | — | opportunistic, only on a real finding |

## Execution order
1. ✅ **§11 compliance woven into the universal gate (W118)** — the #1 ranked gap, done this cycle.
2. Next genuine, non-padding item from **C** only if clearly valuable (C3 is the cheapest honest follow-up:
   surface the compliance badge on the other delivery panels, since the data already flows).
3. **B** items remain the Owner's to authorise — never triggered autonomously.

**Honest position:** §1–§11, §13 and the §3A offerings are delivered to fine resolution with in-house,
verified, end-to-end functionality. The substantive remainder is Owner-gated (B). C-items are real but
lower-value; they are taken only when genuinely worthwhile, never as padding.

---

## E — USER-CAPABILITY GAP FILLING (Owner 2026-06-26: review §1–§17 vs codebase for user capabilities; fill gaps that add user value + ease access)

Reviewed the Whole Vision for **user-facing functionality** gaps (capabilities a user should have but the codebase doesn't yet fully deliver). Prioritised by user value × feasibility (in-house, non-gated):

| Rank | Gap (vision §) | State before | Plan |
|---|---|---|---|
| **E1** ✅ **DONE (W143)** | **"Bring your own data" — attach documents to domain tools** (§9 multimodal · §4.1 "uploaded data: research reports, reviews, data") | All 18 domain tools were **text-only** (DomainTool field types text/textarea/select/keyvalue/list/claims; no upload) | DONE — added a **document-attach** to the shared `DomainTool`: reads a text doc (.txt/.md/.csv/.tsv/.json/.log/.yaml/.xml/.html, ≤200 KB, truncates beyond) **in-browser** and inserts its content into the primary field, so it flows to the in-house endpoint within the existing contract (no backend change). One component change → **all 18 tools** gain it. Verified: attach renders, file content lands in the field, "attached <name>" note shows, /science renders, console clean. |
| E2 | Same "bring your own data" on **Genesis Describe** (offering 2) + the **Refine** box | text-only `problem` textarea | apply the same attach pattern to GenesisJourney's Describe + DomainTool's refine input |
| E3 | **Output history / "My Work"** — revisit past domain-tool + Genesis outputs | domain-tool outputs are ephemeral (lost on navigate) | persist a lightweight per-user outputs history + a retrieval view (Projects store exists to build on) |
| E4 | **Output-format selection** (§4.9 Reports · Presentations · Videos · Websites · Apps…) | repo/website/webapp/mobile/report deliverable buttons are fixed | let the user pick/request which deliverable formats; surface presentation/report variants honestly |
| E5 | **Personalisation to user history/preferences** (§9) | UI is not user-adaptive | needs a prefs store; moderate; non-gated |
| E6 | **Voice / image input** (§9 multimodal) | not present | heavier (mic/vision); only if clearly valuable; honest about scope |
| E7 | **i18n / all languages** (§9 "accessible to all — all languages") | English-only UI | large; scope before building |

Execution: one verified increment per cycle, highest user-value first; in-house only; never fabricate; Owner-gated economic/real-money items remain in §B.
