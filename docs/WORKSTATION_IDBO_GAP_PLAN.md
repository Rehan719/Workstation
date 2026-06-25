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
| **D1** | **VSB IDBO Entity Repository** — a living, intelligently-autonomous enterprise bespoke to the concept→commercialisation solution, shipped as a version-controlled **repo** with an **integrated Website + Web app + Phone (mobile) app** | §13 | **Increment 1 DONE (W121); surfaces are scaffolds.** `POST /api/v1/vsb/{id}/repo` scaffolds a real, on-disk, version-controlled repo (README · IDENTITY · genome.json · BUSINESS_PLAN · ORGANISATION · resources/cascades · compliance/QUALITY · web/webapp/mobile scaffolds · manifest.json) from the entity's REAL data, in-house, QMS-gated + compliance-screened + document-controlled; `GET …/repo` retrieves it; a **Generate VSB Repository** action on the Genesis page renders the tree + badges. **Still scaffolds:** the integrated Website is a single HTML page, the Web app + Phone app are README/manifest placeholders — not yet built. | Increment 2 DONE (W122): integrated **Website** — `POST /api/v1/vsb/{id}/website` generates a real multi-page static HTML/CSS site (index·about·solution + styles) from the entity + in-house copy, into the repo's `web/`, QMS-gated + compliance-screened + document-controlled; served viewable at `…/website/page/{name}` (known pages only). Remaining: (3) **Web app** scaffold→build; (4) **Phone app** (PWA/manifest→RN). Each QMS-gated + compliance-screened + document-controlled, honest (never fabricated built/compiled apps). Confirm sequencing with the Owner. |

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
