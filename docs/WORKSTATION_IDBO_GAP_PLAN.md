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
| **E2** ✅ **DONE (W144)** | Same "bring your own data" on **Genesis Describe** (offering 2) | text-only `problem` textarea | DONE — extracted a reusable **`AttachDocument`** component (DRY) and used it on Genesis "Describe" (seeds the journey with a research report / brief / dataset) + refactored DomainTool to use it. "Bring your own data" is now consistent across **both §3A offerings**. (The DomainTool *Refine* box is for instructions, not data — intentionally not given attach.) Verified: Genesis + /science both insert attached content; new bundle; console clean. |
| **E3** ✅ **DONE (W145)** | **Output history / "My Work"** — revisit past outputs | domain-tool outputs were ephemeral (lost on navigate) | DONE — `lib/outputHistory.ts` (localStorage, honest/per-browser, ≤50 entries) + DomainTool saves each result + a new **My Work** page (`/my-work`, nav under Home) listing past outputs with view/copy/download/remove/clear. Verified: empty state + a seeded record render; save wired in DomainTool.run; 0 dead nav links (46 items). Local-only is stated clearly to the user (no fabricated server history). |
| **E4** ✅ **DONE (W146)** | **Output-format selection** (§4.9) | result only exported `.md` | DONE — DomainTool result now exports in **4 real formats**: Markdown (.md), plain text (.txt), styled HTML (.html, minimal self-contained doc), and JSON (.json — {title, output, provenance, generated_at}). A compact format chooser replaces the single download. Honest: only formats actually producible in-house; the richer living-output formats (Website/Web app/Phone app) already come via Genesis (repo/website/webapp/mobile/board-pack); Presentations/Videos are NOT in-house-generatable today → not faked. Verified end-to-end: ran the Science tool live → result panel shows md/txt/html/json + HTML export executes; the run also auto-saved to My Work (E3 confirmed live). |
| **E5** ✅ **DONE (W147)** | **Personalisation to user history/preferences** (§9) | UI was not user-adaptive; /settings was a stub | DONE — `lib/userPrefs.ts` (localStorage prefs: displayName, defaultRealm, defaultDomain) + a **real Settings page** (`/settings`, replaces the stub: profile form + canonical realm/domain defaults + "clear preferences & history"). The **front door** now greets by the stored name and shows a **"Continue · Recent work"** strip from My Work history (when present); a stored realm/domain pre-seeds a new Genesis journey via the existing `?realm=&domain=` deep-link. Honest: all local, no fabrication; no history → clean front door (no fake "recent"). Verified: Settings saves displayName "Rehan" → front door greets "Welcome, Rehan" + recent strip renders; two journeys intact; 0 dead nav links. |
| **E6** ✅ **DONE (voice) / honestly-scoped (image) (W148)** | **Voice / image input** (§9 multimodal) | not present | DONE (voice) — reusable **`DictateButton`** (Web Speech API `SpeechRecognition`/`webkitSpeechRecognition`, runs in-browser/in-house) wired into the DomainTool primary field (all 18 tools) + Genesis "Describe"; **feature-detected** — renders nothing if the API is unavailable (honest, no fake mic); transcript appended to the field. **Image: honestly NOT built** — the native AI floor has no vision model, so image *analysis* would be fabrication; deferred until a vision model is provisioned (Owner-gated). Verified: Dictate renders where SR is available (present iff supported), on /science + /genesis, no crash. |
| **E7** ✅ **DONE (language pref + multilingual voice) / honestly-scoped (AI-output + full-UI translation) (W149)** | **i18n / all languages** (§9) | English-only | DONE (real, today) — a **Language preference** (12 languages, BCP-47) in Settings + `userPrefs.language`; it drives the **DictateButton recognition language**, so users can **dictate in their own language now** (Arabic, Urdu, French, …) via the browser Web Speech API. **Honestly scoped (NOT faked):** AI *text responses* in the chosen language + **full *machine* translation of every string** would benefit from the AI accelerant, but the **UI i18n framework is now built** (see W150) and translates surfaces incrementally — the external LLM accelerant — the in-house native floor reasons in English and (verified) does NOT actually translate (the /qep/translation/translate endpoint returns English scaffolding on the native floor). Settings states this transparently. Verified: language select saves "ar-SA"; dictation uses it; honest note shown. |

### ▶ E7 follow-on — FULL-UI i18n rollout (W150+, in-house, no model needed)
A dependency-free i18n layer (`lib/i18n.tsx`: keyed strings, English fallback for anything missing, RTL for ar/ur, language follows `userPrefs.language`) is now built and proven on the **front door** (`/`), the **navigation** (Sidebar), and the **Domains hub** (`/domains`, §3A offering-1 landing), translated into **English · Arabic (RTL) · French · Spanish · Urdu (RTL)** — switches live from the Settings language selector. Coverage rolls out surface-by-surface (high-traffic pages next: My Work · Settings); untranslated strings fall back to English gracefully (honest — never blank/keys). This is genuinely in-house (no LLM needed for the static UI chrome; human/curated translations).

### ✅ PHASE E COMPLETE (E1–E7, W143–W149) — user-capability gap filling
Seven user-value gaps reviewed against §1–§17 and filled in-house, honest, verified end-to-end:
- **E1** bring-your-own-data on all 18 domain tools · **E2** same on Genesis "Describe" (reusable AttachDocument) · **E3** output history ("My Work") · **E4** export .md/.txt/.html/.json · **E5** personalisation (real Settings + front-door greeting + recent-work strip) · **E6** voice input (Web Speech, feature-detected) · **E7** language preference + multilingual voice dictation.
- **Honestly NOT faked (need Owner-gated capability):** image *analysis* / video / presentation generation (no in-house vision/media model), AI *text output* in non-English languages + full interface-string i18n (need the external LLM accelerant). These are recorded as gated, not built — when the Owner enables the AI accelerant (§B5) / a vision model, they light up.

Execution: one verified increment per cycle, highest user-value first; in-house only; never fabricate; Owner-gated economic/real-money items remain in §B.
