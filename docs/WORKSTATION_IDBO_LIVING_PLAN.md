<!--
  LIVING DOCUMENT — Workstation IDBO Design & Development Action Plan
  Maintained collaboratively by: the Owner (Rehan), Claude (Anthropic), and any AI agent working this repo.
  This is the single source of truth that bridges VISION ↔ GROUNDED CURRENT STATE ↔ ACTION.
  UPDATE PROTOCOL is in §1. Do not let this drift — every substantive change to the codebase
  should be reflected here in the same change.
-->

# Workstation IDBO — Living Design & Development Action Plan

**Status:** LIVING · **Last reconciled:** 2026-09-05 (W446) · **Grounded baseline:** in-house-first native AI fabric (owned models/orchestration/swarm/ensemble + autonomous workflow tree), integration suite **385✓ / 15 skip / 0 fail — 382 in the full run plus the three register-lockstep legs re-run green once the new script was git-added (the snapshot step had dropped its intent-to-add)** (361 test functions, 400 items) at the last full run (W473), frontend tsc 0 errors, both CI green on `main` at the last pushed commit (re-check the run for the current one)
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
- Work a round **finds and does not do** is never left in a chat or a commit message: it becomes a row in `docs/FOLLOWUPS.json` (`python scripts/followups.py add`, which routes it to the delivery-plan item that owns its area — NEXT was retired W469), or OWNER — §6.4 (PLAN NOW and the schedule, both generated) and `GET /api/v1/plan/followups` show it, and the suite fails when a row rides on an item already marked `✅ DONE W###`, when owner-gated work is slotted anywhere but OWNER, or when an open row names a file that is not in the working tree or not tracked by git (W462).

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

**Platform:** FastAPI backend (`agentic_core/app_mvp.py`, **463 API operations** — method+path pairs; 439 distinct `/api` paths — measured 2026-09-05 with `python scripts/reach_audit.py`; re-measure rather than trust), Vite+React+TS frontend (`apps/workstation-superapp`, **tsc 0 errors**, 73 `<Route>` declarations). Tests: `integration_tests/test_mvp_spine.py` → **385 pass / 15 skip / 0 fail — 382 in the full run plus the three register-lockstep legs re-run green once the new script was git-added (the snapshot step had dropped its intent-to-add)** (361 test functions, 400 items, at the W473 full run; run on the native floor via `AI_DISABLE_LOCAL=1`); Spine + Doc-Sync CI green on `main` at the last pushed commit; browser smoke 17 deep routes + 57 swept. **Rounds 7–10 (W322–W354):** design-surface + swarm tenancy (W324), §11 marketplace teeth + substance-aware birth verdicts (W322), genuinely tamper-evident evidence chains (W327), the streaming owned model that actually serves under its adaptive budget (W323/W353), the enterprise-aware avatar with in-house voice (W325/W326), entity-to-entity service contracts + a real self_investment consumer (W330), the memory layer's cross-tenant bleed closed at the source with per-tenant namespaces + Owner-run purge remediation (W332/W333/W334/W343), store-concurrency correctness across the money paths + the UEG audit chain (W348/W349/W351), owner-scoped avatar sessions (W350), grounded floor-safe shipped copy (W355/W356), and a Docker image that actually boots + an honest prod compose (W354). The §17.5 invariants were live-verified incl. arms-length falsification (W345) and the evolution-apply loop driven end-to-end (W346). **AI is IN-HOUSE-FIRST** via the native fabric (`ai/native/` + `ai/gateway.query_meta`) — owned model discovery/routing/tiers, parallel multi-model **ensemble**, health-reordering orchestrator, hardened memory store (corruption-tolerant + atomic writes); external providers are optional accelerants only. **In-house integration sweep complete (W1–W76)** — autonomous workflow-TREE orchestrator + 16 real owned capabilities (live count 2026-09-11) at `/api/v1/native-ai/capabilities`. **W194–W250:** ALL EIGHT PI cognition engines (BDP·SPI·APIE·DDPIE·Cascade·MJM·Nexus·Genesis), ALL EIGHT digital-resource facilities (Engines·Reactors·Petri·Incubators·Laboratories·Factories·Generators·Simulators — Reactor = the vision-exact Incubator+Experimentation+Studio composite), all 8 biomimetic organism systems, the full enterprise/org layer (cascade·Capital Fund·Change Control·Products Catalogue·Build-to-Order) AND the last registry resources (compliance·truth_consensus·mega_project·omnimedia·federation_mesh) **run their REAL engine when composed in the Resource Fabric** — nothing in the catalogue is a prompt approximation. **W248:** every generated VSB (Genesis /establish, SSE /vsb/spawn, Studio) carries its own Board + Chief (owner's digital twin) + living economy + living-entity registration + seeded plan. **W249:** every economy cycle is gaas-gated + UEG split-logged; material distributions are held for Change Control approval. **W252–W300 (Rounds 3–4):** tenant isolation live on the VSB/Genesis/Studio + per-VSB management surfaces (W252/W295, 404-never-403, server-stamped owners); digital-twin pre-validation gates HIGH/CRITICAL Change Control (W253); SSE establish birth-stream (W255); double-entry ledger + period close + CFO statements (W256); §11 REAL engine-backed verdicts sealed + UEG-logged + CCA-routed, continuously re-screened on the heartbeat (W285–W288); the §13 repo genuinely version-controlled, shipped as one whole, cascades re-runnable (W289–W291); REAL revenue recognition + compounding loops closed (W293–W294); the login/token front door + Owner-gated self-serve signup flag (W296–W297). **W301–W321 (Rounds 5–6):** the §4 journey's WHOLE record survives establishment and reaches every shipped surface (W301–W306: blueprint accessor, birth auto-ship, verbatim-export deliverables, simulated candidate ranking); the §10 bar measured per-criterion with a genuinely-stateful defect→correction→re-verify loop and TRUE failures/gates arithmetic (W307/W316); Offering-1 gated flag-not-block (W308); birth vitals + compliance-held economy + heartbeat auto-evolve/auto-ship of children (W309/W319); the genome mutates only through CCA approval and immune_quarantine genuinely CONTAINS (W310/W318); the economy's materiality hold PRESERVES the held revenue and waterfall bounds bind to the stored entity type (W313); the economy router, Living Deliverables and QMS defects are tenant-scoped (W320); the Shell is mobile-first below 768px (W312); the fabricated front-door/security-theater copy is archived or rewritten truthfully (W314); one establish core serves both paths with scaffold-clean public copy (W315); the 401→/login seam is real and purchases are caller-bound (W317). See `docs/AGENTIC_CORE_INTEGRATION_AUDIT.md` (real-vs-mock) + `docs/AUTONOMOUS_PROGRESS.md` (W1–W250, the authoritative cycle log).

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
**W460 (2026-09-13):** delivery-plan **P1.12 delivered** — the composer canvas retired for the real
cascade designer; every unevaluated compliance badge, score and sentence removed or made conditional on a
real verdict; the Governance Hub flags each UEG event from what it is.
**W461 (2026-09-13):** transformation stage verification honest — three-state stages with a basis, and a
run validates (and moves a living-plan objective) only when every assessable stage verified and the gate
returned 'allowed'; halted, partial and constant-verified runs no longer write back to this plan.
**W462 (2026-09-13):** the follow-up register — `docs/FOLLOWUPS.json` + `scripts/followups.py`: every task a
round finds and does not do is slotted to the delivery-plan item whose round does it (or NEXT / OWNER),
scheduled in plan order, rendered into §6.4 and the delivery plan, served at `GET /api/v1/plan/followups`,
shown on `/transformation`; the suite fails when a finished item still carries one.
**W463 (2026-09-13):** economy approvals (register FU-002 and its class; virtual WST) — a material action's
hold is identified by what filed it, there is one live record per action (kept current while submitted,
withdrawn when it cannot release), an approval releases only the intake it was filed for and is given back
only for the action that spent it, a hold after a rejection needs an explicit decision (the Sanctum lists it),
a decision binds only the amount the reviewer read, and an economy hold cannot be implemented by hand.
**W464 (2026-09-16):** the Owner's rulings of 2026-09-14 on the register's four OWNER rows — a HIGH change a
review approved waits for Board ratification before anything acts on it (FU-012; the Board page's queue); Change
Control writes its decisions to the UEG (FU-013); economy_material is CRITICAL, so only the Owner's explicit
decision releases a material economy action, and code_change is HIGH (FU-014); genome_engine.py fixed and kept,
unwired (FU-020). FU-025…FU-033 registered.
**W465 (2026-09-17):** the register's NEXT rows FU-015, FU-016 and FU-024 (virtual WST) — a service contract is
settled once: the settle claims the contract under a transfer id persisted on the claim (a second settle meanwhile
is refused), a retry after a crash asks the client's ledger first and completes a posted debit instead of paying
again, and every contract change re-reads the store inside its lock, so a long delivery no longer writes an old
copy over a settlement. An unpaid settlement is recorded as what it was (held for the Owner, rejected and by whom,
refused by the gate, a gate error). The owner-payments store is locked and atomic, and it, the contract store and
the pending-transfers queue are refused when unreadable instead of being read as empty and overwritten; a cycle
whose owner accrual fails says so. FU-034…FU-046 registered (FU-038 — a malformed queue record debiting before it
failed — and FU-046 closed in the same round: every record is shape-checked before any debit, and a receiver id that
would hide its own debit from a replay is refused).
**W466 (2026-09-17):** the register's NEXT row FU-023 (virtual WST) — a transfer whose sender was debited and whose
receiver was never credited is found and completed once: every new debit carries its transfer and an open receiver
leg (closed once the receiver's queue holds the id), a completion is a replay that can never debit, and it runs from
the transfer panel's Complete button (the page lists a sender's open legs from the ledger), `POST
/api/v1/economy/transfers/reconcile`, or the heartbeat every fifth beat while autonomous economy is on. Every failed
transfer is answered from the sender's ledger and the receiver's queue, naming the transfer id (it was a bare 500).
Debits made before W466 are never completed — FU-047 registered.
**W467 (2026-09-17):** the register's NEXT rows FU-022, FU-043 and FU-044 (virtual WST) — the heartbeat's governed
cycle consumes its recognised revenue events under a token before it runs (a failed consume after the ledger had
posted used to distribute them twice); a cycle that raises before its first ledger write gives back its events, the
receipts and returns it drained, and the Owner's approval, while one that wrote anything keeps them consumed and the
approval spent (the API cycle counts as run only once it writes too). The revenue-events store is read strictly — an
unreadable store is refused, never overwritten — its cap keeps pending and in-flight events, and a consume whose
process stopped is given back by the stranded-consume pass (every fifth beat with autonomous economy on). FU-048
registered.
**W468 (2026-09-17):** the register's NEXT row FU-041 (virtual WST) — a VSB ledger that cannot be read whole (a
byte-order mark, a truncation, a wrong shape, a lasting sharing violation) is refused by every writer and reader, never
answered with empty books: one heartbeat cycle used to wipe such a ledger by itself, and `/close-period` and `/cycle`
replaced the real books and answered 200. Cycles are refused before any gate, the ledger routes answer 503, a transfer
from an unreadable sender debits nothing, the ledger's writer can never save a shape its reader refuses, and cycle
inputs are bounded. A heartbeat visit that raises advances the rotation (it used to be picked on every beat) and the
living roster says so; the economy pages show the server's reason. FU-049 to FU-066 registered — among them the
compliance history, the living roster, the waterfall overrides and the venture portfolio, each still read tolerantly.
**W469 (2026-09-18):** the Owner asked why P1.13 never came — the register's NEXT slot ("its own round, before the next
plan item") had grown to forty-two rows because rounds registered more than they closed. On his instruction NEXT is
retired: every row rides the plan item that owns its area (P1.15, P1.16 and P2.9 added), ROUTES send each new row to
its item, and PLAN NOW (§6.4 and the delivery prompt) is generated on every register change, served live by
`/api/v1/plan/followups` and shown on `/transformation`, refreshed every minute. `followups.py done` marks an item and
moves its rows and routes on; a done that half-landed is finished by running it again.
**W470 (2026-09-18, Claude Fable 5.1):** P1.13 Catalogue honesty. ONE tool registry
(`src/lib/toolRegistry.ts`) that every domain hub mounts its titles from and that DomainsHub and /ai-tools count,
list, describe and link from (the three hand-kept lists had drifted to 23 / 18 / 24); the 'QEP Flagship' tab and
its two dead components gone from the five non-Religion hubs (QEP lives in Religion); the catalogue API says what
each products/ directory is — live (5, a route serves it), source (9, a pointer), legacy (6, the signature-product
archives, never routed) — and the marketplace counts live only, badges the rest and opens only a served surface.
FU-071, FU-072 and FU-073 registered (the third: `done --hand-to` lifted the taker's broad prefixes to the first route).
**W471 (2026-09-18, Claude Fable 5.1):** P1.14 Board pack + Chief's Opening honesty. The board pack's required
sections are measured on the narrative alone (its own preamble used to give every pack coverage 1.0); an empty
blueprint is refused ('no concept recorded — pack not assembled'); every pack carries a content hash over what it
holds with a version that moves only when that changes and 'unchanged since' — three assemblies of an unchanged VSB
show one version; the Genesis card badges the narrative's provenance. The Chief's Opening writes nothing from the
native floor (the fields stay pending, said on the page), keeps a draft's preamble as provenance, fills only empty
fields from a model, and `/business-plan/set` is now the owner-edit surface on BusinessPlan.tsx (clear works, edits
are marked). FU-074 registered.
**W472 (2026-09-18, Claude Fable 5.1):** P1.15 Stores that refuse, never replace — the class-kill. One strict read
for writers (`config.read_json_strict` → `StoreUnavailable`), applied to every store the register named: the living
roster, the compliance history (unreadable → the entity is held, standing unknown), the Owner's waterfall overrides,
the venture portfolio, the UEG chain (refused, never restarted) and the interceptor's own writes (the decision stands,
`ueg_logged` says whether it reached the ledger), the chain's default path through `data_path`, the federation twins,
the proposed catalogue, agent registrations, composition runs, the tier stores, `mutate_json`; `store_lock`'s stale
timeout; a non-finite revenue amount refused; and `POST /economy/ledger/{id}/repair` for a refused ledger
(quarantine, lossless recovery, what was lost said). Eleven register rows closed; FU-075 registered.
**W473 (2026-09-19, Claude Fable 5.1):** P1.16 Canon and suite hygiene before the milestone — PHASE P1 COMPLETE.
The two mandate pages rewritten as honest inventories (`docs/compliance/MANDATES.md`, `MANDATES_FINAL.md`: every
VERIFIED / PRESENT row names paths that exist; the false rows say NOT PRESENT; the simulated 'PQC' signer, the
ontology engine over an empty directory and the unwired 'LSTM' named as what they are); `config/paths.py` roots the
data store in the repository and names a richer legacy store by what it holds; `scripts/relocate_data_store.py`
copies, verifies, merges disjoint maps and never deletes (the Owner's memory and interactions stores relocated and
verified; chroma_db is his to move — FU-079); the genome validator resolves under the repository and self-healing
refuses to ratify its template; the Command Center prints only what it measures; ten live data files untracked from
git; the register's tooling refuses to rewrite closed rows, reports a marker in any form, validates hand-offs and
keeps every handed route in its place. Thirteen register rows closed; FU-076…FU-079 registered. MILESTONE M1 next.
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

**Apex governance — Board of Directors (live):** `/api/v1/board/*` — the **Chief** (the Owner's **digital twin**) chairs specialist Directors above the AI CEO (arms-length). `POST /board/chief/instruct` → the Chief faithfully represents the Owner → board directive → delegated AI-CEO timelined action plan. `board_for_owner()` embeds a Board + Chief-of-its-owner into **every generated VSB entity**. UI: `/board`. **Board ratification (W464, the Owner's ruling):** `GET /board/ratifications` lists every HIGH change a review approved that the Board has not ratified; `POST /board/ratifications/{cca_id}` (`ratify` | `refuse`, `on_owner_direction: true`; admin-only under auth) records the Owner's decision — nothing implements such a change until then.

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
- ▶ **Persistence hardening** — PARTIAL: `store_lock` + `atomic_write_json` + `load_json_tolerant` across the money paths (the owner-payments store and service-contract settles — found by the W463 class sweep, FU-016/FU-015 — closed W465, with strict reads that refuse an unreadable owner-payments, contract or pending-transfers store instead of overwriting it), UEG chain, living registry (every roster write serialised by W463), the per-action economy gate lock (W463), AI memory, users, fund and venture stores (W348–W351, W365–W371, W442–W444, W463 — each round found one more unlocked writer; the rule is now 'enumerate every writer'); SQLite/Postgres is Owner-gated (managed Postgres). Docker/CI ✅. **CTO**
- ▶ **User isolation** (the §17.5 absolute invariant) — PARTIAL: delivered on the VSB spine, Genesis, Studio, economy, deliverables, QMS defects, marketplace, avatar sessions, native memory and the Agent Hub (W252–W443, 404-never-403, server-stamped owners); NOT yet on the organism's control perimeter — the heartbeat, genome, organism-status, sovereign-evolution, board, business-plan and swarm routers each carry zero auth dependencies (W446 audit R6.2); change-control has read an identity on its write routes since W459 (submit stamps the authenticated principal; under auth an override, a CRITICAL decision and — W463 — retiring an economy record are admin-only), but its read routes (`GET /cca`, `/cca/queue`, `/cca/approved`, `/cca/rejected`, `/cca/implemented`, `/cca/{id}`, `/cca/impact/{id}`) carry no auth dependency — with AUTH_ENABLED on, a caller who is not signed in still reads every change record and can trigger an impact assessment, and `synthesis_studio`'s `GET /studio/vsb` lists every entity with no owner filter. Planned: prompt v11 rev 2 delivery plan. **CTO**
- ✅ **Digital-twin pre-validation** in the Change Control implement path (W253 — HIGH/CRITICAL gated, 409 on a twin failure). Caveat found W446: with no twin model registered the check falls back to an organism-health default (`source: health_gate_default`) and a manual override is attributed to `cca_ai` in the audit trail — both in the delivery plan. **Closed W459:** the fallback now reads "no twin model — health gate only" and every decision records the principal that made it, never `cca_ai`. **BTO**

> The grand-aspirational `_archive/docs/DEVELOPMENT_PLAN_v7.0_SINGULARITY.md` (Layers 13–14, interstellar) is retained as **horizon lore**, explicitly *not* current state.

### 6.4 Plan now and scheduled follow-ups (generated from the delivery plan and `docs/FOLLOWUPS.json` — never edit between the markers)
```text
<!-- plannow:begin (generated by scripts/followups.py render - never edit by hand) -->
PLAN NOW — generated from the delivery plan's items and docs/FOLLOWUPS.json by scripts/followups.py on
every register change (add · close · drop · reslot · route · done · render); never edit between the markers.
  Next: P2.1 Cascade grounding — no follow-ups ride it.
  Then, in order (the follow-ups riding each): P2.2 0 · P2.3 0 · P2.4 6 · P2.5 0 · P2.6 9 · P2.7 1 · P2.8 3 ·
    P2.9 19 · P3.0 0 · P3.1 0 · P3.2 0 · P3.3 0 · P3.4 0 · P3.5 0 · P3.6 0 · P3.7 0 · P3.8 0 · P3.9 0 ·
    P3.10 0 · P3.11 0 · P4.1 0 · P4.2 0 · P4.3 0 · P4.4 0 · P4.5 0 · P4.6 0
  Done: 16 of 43 items — P1 16/16 · P2 0/9 · P3 0/12 · P4 0/6.
  Follow-ups: 39 open — 38 ride a plan item (0 high), 0 unscheduled, 1 awaiting the Owner; 40 done, 0 dropped.
<!-- plannow:end -->
<!-- followups:begin (generated by scripts/followups.py render - never edit by hand) -->
SCHEDULED FOLLOW-UPS — every task a round finds and does not do is a row in docs/FOLLOWUPS.json, added in
the same commit (python scripts/followups.py add routes it to the plan item that owns its area; a high one
rides the next open item) or slotted OWNER (waits on an Owner decision; never scheduled). A round that
finishes an item marks it with python scripts/followups.py done P1.13 --by W### — its rows move along the
routes or are closed first; the suite fails on a row left on a finished item.
Open 39 (38 scheduled, 0 high · 0 unscheduled · 1 awaiting the Owner) · done 40 · dropped 0.
  P2.4 — The scatter: 67 ops in 38 clusters, 3–4 per round, audit-before-wire, retire freely
    FU-076 [medium] pqc_hardening.py stamps a SHA3 digest with a fixed built-in key as a 'Dilithium5 signature' — relabel or retire — agentic_core/security/pqc_hardening.py is not a post-quantum scheme; gaas.py and qep_flagship.py record its output as pqc_signature, which reads as cryptographic assurance the code does not give. Retire the field or name it a content hash. (found W473 refuter)
    FU-077 [medium] The ontology engine serves empty graphs and the one real ontology (Law, under knowledge/) is unwired — agentic_core/reactor/domains/ontology_engine.py reads agentic_core/data/ontologies/ which holds nothing, reached from the domain weaver (a v138 CEO tool) — every domain query answers an empty graph; knowledge/Law/EmploymentTribunal/ontology/*.json is never loaded. Wire the Law graph or retire the engine (audit-before-wire). (found W473 refuter)
    FU-071 [low] Nine source-pointer product directories are still listed as products of a kind — The catalogue now marks them status source ('a pointer, nothing served yet') and no consumer builds from them, but products/ still holds nine metadata.json directories (business_incubator, cognitive_scraper, gse, molecular_sdk, nanophotonic_navigation, scraping_suite, uviap, mjm-intelligence-engine, signature-product-suite) whose only substance is a pointer at SDK source. Fix: for each, either serve it (a route and a real page) or retire the directory; the scatter item decides which, per the reach audit. (found W470)
    FU-072 [low] The six legacy signature-product directories still sit in products/ with self-declaring manifests — products/Care … products/Science each carry a manifest.json self-declaring PRODUCTION_READY, WCAG 2.2 AAA and nine injection formats that nothing serves; W470 lists them as legacy archives and routes nothing to them, but the directories remain where a reader takes them for products. Fix: move them to _archive/products/ (LEGACY_ARCHIVES then empties) and keep one line in the catalogue saying they were archived. (found W470)
    FU-075 [low] Read-only readers still use load_json_tolerant; retire the tolerant loader once every writer is strict — W472 made every WRITER read strictly (config.read_json_strict). The read-only readers that summarise or list — revenue._load (pending_summary), ueg._read (recent), agent_hub listing reads, integration_surface listings, resource_fabric composition/swarm listings, swarm proposed_catalogue/org_cascade_runs listings, business_plan._load — still use load_json_tolerant or a bare json.loads with a fallback: honest as readers (they never write back) but a listing over an unreadable store shows fewer rows without saying so. Fix: give each listing an 'unavailable' answer via read_json_strict and delete load_json_tolerant when no caller remains. (found W472)
    FU-078 [low] geospheric/resilience.py ('LSTM' self-healing) is unwired dead code — agentic_core/biomimicry/geospheric/resilience.py holds a hand-rolled 'LSTM' over a JSON model file; nothing imports it. The organism's real self-healing is agentic_core/organism/self_healing.py. Retire it or wire it honestly (audit-before-wire). (found W473 refuter)
  P2.6 — The perimeter and the gate
    FU-005 [medium] The /api/v1/swarm router carries no auth dependency — agentic_core/api/swarm.py has zero Depends — the org cascade (POST /cascade), CEO delegation (POST /delegate), proposed-catalogue curation and the run histories are callable by anyone when AUTH_ENABLED is on; P2.6 names 'swarm' among its routers, this row pins the routes (found W460 audit (P1.12))
    FU-006 [medium] The org cascade's governance verdict gates a constant string, not the delivery — swarm.py's _attest returns a fixed attestation sentence, so 'gov: allowed' can never reflect the delivered content; W460 relabelled the chip 'intent only' — the real fix is gating the delivery itself (found W460 audit (P1.12))
    FU-007 [medium] One violation trips the shared circuit breaker, and anyone can reset it — record_event trips on a single is_violation (no threshold), halting every later action on the node; POST /api/v1/gaas/breaker/reset has no user dependency (found W460 audit (P1.12))
    FU-029 [medium] Board ratification is apex-only, and the Board's other routes trust a client-supplied owner — GET/POST /api/v1/board/ratifications cover every change (admin under auth; on_owner_direction in both modes) — a VSB-scoped change is not routed to that VSB's own board or tenant owner; board.py's chief/instruct and directive still take 'owner' from the request body and carry no auth dependency (the P2.6 perimeter) (found W464 Board audit (read))
    FU-019 [low] The evolution apply's claim release is a status-only compare-and-set — apply_approved_evolution's _release flips implemented back to approved whenever the status is implemented, without proving the implemented state is this caller's own claim (no claim nonce) — the shape W463 removed from the economy restore; not reachable today (found W463 class-sweep verifier (read))
    FU-030 [low] In single-user mode a HIGH override needs no acknowledgement, so it skips Board ratification — with auth off any client's override_decision is recorded as admin_override (the Owner's explicit decision) and a HIGH change approved that way is not queued for ratification; CRITICAL requires admin_decision_for_critical, HIGH requires nothing (found W464 ratification audit (read))
    FU-031 [low] A decision whose ledger write failed leaves no mark on the record, and nothing reconciles it — Change Control writes a decision's UEG node after the record lands (W464, FU-013); a failed write or a process that dies in between leaves the decision without a node, reported only in that response (ueg_logged false) and the server log — the record carries nothing a later reconciliation could find, so the gap is invisible after the response (found W464 UEG audit (read))
    FU-032 [low] The audit views read an Owner's rejection as a fault — classify_event flags cca.change_rejected and board.change_ratification_refused (a refusal); the Governance Hub shows them red FLAGGED and counts them with failures without rendering flag.why, and ConstitutionalUI's UEG tab ignores flag entirely (tone keyed to two event types) (found W464 UEG audit (read))
    FU-033 [low] A review of a change record missing rationale, affected_systems or rollback_plan answers 500 — review_change builds its prompt with c['rationale'], c['affected_systems'] and c['rollback_plan'] — a record written without them (hand-written or by an older writer) raises KeyError after _start has already moved it to under_review (found W464 (found writing the tier guard))
  P2.7 — The organism defends for real (the honest half first, then the wiring)
    FU-018 [low] The optimizer's resource fabric releases resources a pool never consumed — assemble_pool records the full requirements even when it could not decrement capacity, and disassemble_pool gives all of them back (gpu available 1064 of 64 at unit level); the optimizer engine assembles and releases per call (found W463 class sweep (reproduced at unit level))
  P2.8 — Bespoke swarms
    FU-008 [medium] swarm_cascades.json writers are not under store_lock — define, update and delete load-modify-save the store with no lock — a threaded probe during the P1.12 audit lost 38 of 40 concurrent writes (found W460 audit (P1.12))
    FU-009 [low] The swarm HTTP contract drops per-stage model; runs have no run_id or UEG record — SwarmStageSpec carries role and instruction only, so a stage's model choice is silently discarded; run_swarm records the outcome under stage 1's served_by alone and writes no run id or ledger entry (found W460 audit (P1.12))
    FU-010 [low] Saved cascades cannot be deleted from the designer page — DELETE /api/v1/resources/swarm/{sid} exists but the /native-ai designer offers no way to call it (found W460 audit (P1.12))
  P2.9 — The economy's flows told as they happened (virtual WST)
    FU-034 [medium] A service contract can be offered to an entity that is not living, and nothing declines or cancels one — offer_contract never checks that the client and provider are registered living entities: the W465 probe offered a contract to a provider id that exists nowhere, accepted it, and delivered it (a whole provider-scoped org cascade ran — 15-25 minutes on a local model) before settle refused the transfer with 404. There is no decline for the provider or cancel for the client, so such a contract sits 'delivered' forever. Fix: validate both parties at offer (and again at accept), add decline/cancel with their own UEG events, and let the page offer them. (found W465 audit (read) and probe (reproduced))
    FU-035 [medium] A settlement's materiality approval is bound to the client-provider pair, not to the contract — A contract settlement goes through the transfer gate, which binds an approval to the sender, the counterparty and an amount ceiling (W463). Two material contracts between the same client and provider therefore share one hold identity: the Owner's approval of contract A's settlement releases contract B's settlement of an equal or smaller price if B settles first, and A is then asked again. Virtual WST. Fix: carry the contract id into the gate's action identity (source 'contract:<id>') so a hold, an approval and a rejection name exactly one contract. (found W465 audit (read))
    FU-036 [medium] A failed owner accrual is reported but never re-applied, so the Owner's balance stays short — Since W465 a cycle whose owner accrual fails says so (owner_accrual.accrued false, economy.owner_accrual_failed on the UEG, an error log) — but nothing re-applies the missing credit: the ledger shows the owner stage distributed while owner payments never received it. Fix: record the failed accrual durably (the UEG event carries vsb, amount and cycle), and reconcile on the next successful accrual or heartbeat — re-apply each unreconciled failure once, idempotent on its cycle id. (found W465 audit (read))
    FU-017 [low] A marketplace purchase can charge the buyer without recording the sale — consume_tokens runs before the listing save and the receipt write; if either raises there is no refund, so the buyer is charged for a sale nothing records (consume-without-compensation) (found W463 class sweep (read, not reproduced))
    FU-037 [low] A second delivery of the same contract runs a whole cascade before it is refused — deliver_contract binds its result with a compare-and-set only after the cascade returns (W465), so a second Deliver while the first runs starts a second provider-scoped org cascade (15-25 minutes on a local model) whose work is then discarded with 409 'another delivery bound first'. Fix: claim the delivery before the cascade (as settle claims), release it if the cascade raises. (found W465 audit (read))
    FU-039 [low] A settle that raises leaves the previous attempt's unpaid outcome on the contract — settle_contract records an outcome only when the transfer answers; any exception exit (a crash after the debit, a 503 from the ledger or the pending store) releases the claim and leaves the settlement field of an EARLIER attempt, so the page can still show 'held for the Owner' after the Owner approved and the latest attempt failed for another reason. Nothing is paid twice and settling again completes it. Fix: on an exception exit, record outcome 'unknown' with the error (inside the release mutation), and let the page say settle again. (found W465 third refutation (reproduced, pre-existing))
    FU-040 [low] A cycle swallows a failed venture-returns intake silently, and the Board page cites a server log it may not have — W465 made a failed inter-VSB receipts intake visible (inter_vsb_receipts_error, a warning log) and made the gate measure only receipts the intake can take; consume_pending_returns in the same cycle still swallows every error as 0 recycled with no report or log, and its peek may read differently. Separately BoardOfDirectors.tsx tells the Owner to 'see the server log' when a ratification's ledger entry did not land — check that the server logs that case (the W465 owner-accrual alert did not until the third refutation). (found W465 third refutation (read))
    FU-045 [low] The heartbeat drops a failed entity visit silently, and revenue.consume_pending is ungated dead code — heartbeat.py:239-243 discards operate_vsb's error result, so a failed or partly posted non-material cycle leaves no trace anywhere (reproduced); and revenue.consume_pending (revenue.py:108-134) has no callers yet would consume every pending event without any gate if one were added. Fix: log the failed visit (UEG + log) and delete the dead function. (found W466 pre-audit of FU-023/FU-022 (reproduced))
    FU-047 [low] A transfer stranded before W466 can only be found by hand — W466 completes a stranded transfer (the sender debited, the receiver never credited) only when its debit carries the receiver-leg marker written since W466: a debit made earlier cannot prove whether its receiver was credited once its id left the receiver's 50-row display window (and before W465 no durable credited-id list existed), so completing it could credit the receiver twice. POST /transfers/{id}/complete refuses such a debit (409) and the pass never lists it. Fix, if any exist: a one-off Owner-reviewed audit listing unmarked transfer_out debits with no credited-id and no display-window entry, completed individually on the Owner's decision. (found W466 pre-audit (reproduced: replaying an old id re-credited it))
    FU-048 [low] A heartbeat cycle whose process stopped mid-cycle leaves the Owner's approval spent and asks again — W467 consumes a cycle's recognised events before it runs; if the process is killed between that consume and the cycle's first ledger write, the stranded-consume pass (every fifth beat with autonomous economy on) gives the events back after 15 minutes, but a material cycle's approval stays implemented without a released_action_ran marker (it reads as still in flight — the restrictive side), so the next beat files a fresh CRITICAL hold for the same events and the Owner decides twice. The economy.cycle_intake_consumed record names the approval's cca_id and consume_id. Fix: when the pass gives back a token's events, restore that approval if its trail has no released_action_ran for that consume_id (the W463 give-back rules). (found W467 first refutation (reproduced by killing a process))
    FU-057 [low] A transfer refused on a retry says nothing was debited although an earlier attempt may have — _transfer_core answers any SenderLedgerUnavailable with X-Transfer-Debited: false and 'Nothing was debited' (true of this request only): a settlement retried under its persisted transfer id, whose first attempt debited, is told nothing was debited once the ledger becomes unreadable. And a gated action that raised is retried outside the gate (W463 design), so a refusal inside the action runs again ungated. Fix: say 'this attempt debited nothing; an earlier attempt under this id may have' and keep the retry inside the gate's decision. (found W468 second refutation (reproduced))
    FU-058 [low] A cycle whose ledger write times out answers a bare 500 — /cycle maps only LedgerUnavailable (503) and LedgerWriteRefused (409): a store_lock TimeoutError or a PermissionError from atomic_write_json during a cycle's writes still escapes as a 500 with no statement of what was written; the async governed_cycle writes no economy.cycle_raised record when its cycle raises (the heartbeat path does); and the strict read's retry sleeps block the event loop in async routes. Fix: map them with the ledger_written wording, and move the retries off the loop. (found W468 first refutation (reproduced))
    FU-059 [low] The economy pages keep earlier figures beside a new refusal — VSBEconomy.runCycle and VSBCockpit leave the previous cycle's report and balances on screen under a refused or partly written cycle; the cockpit shows nothing for a 200 hold (cycle null), its other actions (growth, chief, transformation, deliverables, ship state) are not tied to the selected entity, avatars/api.py reads the raw roster hold (stale after a repair, and blind to decision_hold and last_error), and doClosePeriod parses a non-JSON error body as JSON. Fix: clear or label the stale figures, render the hold, and guard every entity-scoped load as W468 guarded the ledger. (found W468 first refutation (reproduced))
    FU-060 [low] A development spend posts as a distribution and two spends can overdraw the fund — spend_self_investment checks the balance on the construction snapshot and records under the lock without re-checking, so two concurrent spends each draw the whole balance (self_investment goes negative); and record('self_investment', kind='debit') posts Dr distribution_self_investment / Cr cash, the same as a distribution, so a spend increases the distribution expense; a spend that fails for any other reason (a busy ledger lock) is recorded nowhere. Fix: check inside the lock and post a development-spend account. (found W468 second refutation (reproduced))
    FU-061 [low] Books near the float limit: a period close saves and then answers 500 — With balances near 1.7e308 WST (only a crafted or imported ledger reaches this; cycle inputs are bounded at 1e15 since W468), close_period's statement sums overflow to inf: the close marker is saved with an Infinity net profit and the route answers a bare 500 (JSON cannot carry inf). The ledger's save check covers balances and posting amounts, not the close marker's figures. Fix: compute the statements before saving and refuse (LedgerWriteRefused, 409) when any figure is not finite. (found W468 third refutation (reproduced))
    FU-063 [low] Visit outcomes are reported inconsistently across heartbeat, genesis and pages — heartbeat counts a held or refused visit (ledger_unavailable, compliance or governance hold) as an operate_vsb action and sets last_vsb_operated; genesis's streaming establish says 'cycle ran' for an operate_vsb result that has only an error, and a result {error, cycle_ran True} (a cycle that posted and whose roster bookkeeping raised) is counted as not operated; list_living shows statuses that are not holds (intake_unavailable, intake_consumed_elsewhere) as 'held by governance'; a gate-error hold (no Change Control record) is kept on a raise as if it were a decision; the compliance branch's roster write sits outside the try (a raise there leaves last_operated unchanged); and two visits of one entity at once can clobber each other's row. Fix: report held, refused, raised and ran as four outcomes everywhere. Related to FU-045. (found W468 first refutation (reproduced))
    FU-064 [low] The roster's ledger-hold text reads every held entity's whole ledger on each call — list_living describes a ledger_unavailable hold from a live strict read of that entity's ledger; the heartbeat and pages call it often, and with large ledgers this is seconds per call (4 s for 60 held rows of 4 MB, measured). Negligible at today's sizes. Fix: cache by the file's size and mtime. (found W468 second refutation (reproduced))
    FU-065 [low] A ledger that keeps reserves only in the legacy balances refuses every transfer — A ledger written before W256 holds entries and balances but no accounts: validate_transfer reads reserve_fund from accounts (0.0) and refuses any transfer as insufficient funds, although the legacy view shows reserves. Fix: say the ledger predates double entry, or migrate it once. (found W468 second refutation (reproduced))
    FU-074 [low] The Cockpit's plan tab has no owner-edit surface and no owner-edited marks — W471 wired the owner-edit form (POST /business-plan/set with clear) and the owner-edited marks into BusinessPlan.tsx only; VSBCockpit's plan tab shows the Chief's Opening with its provenance badge and pending list but the founder cannot set or clear a field there and set fields are not marked. Fix: mount the same edit form and marks on the Cockpit's plan tab (one component shared by both pages). (found W471)
  AWAITING THE OWNER — recorded, never scheduled into a round without the Owner's instruction:
    FU-079 [medium] chroma_db: the legacy vector store above the repository was not relocated (both copies populated) — scripts/relocate_data_store.py refuses to merge two populated directories; the Owner's <repo-parent>/data/chroma_db and the repo's data/chroma_db both hold data. The Owner decides which is live; the script copies nothing until then. (found W473)
<!-- followups:end -->
```

---

## 7. Vision-Adherence Scorecard (Owner's monitoring lens)

Honest self-assessment of how well delivered work realises each vision pillar. `●` strong · `◐` partial · `○` not yet.

| # | Vision pillar | Status | Evidence / gap |
|---|---|---|---|
| 1 | AI-mediated end-to-end Concept→Design→Delivery | ◐ | Journey runs end-to-end; the user's problem survives every stage (W434); the journey UI discloses the floor (W436). ◐ because (W446, ledger R2/R1) the shipped VSB body's SUBSTANCE still awaits the owned model (since W450, P1.2, a floor-served field ships as an honest pending state and the founder names the enterprise — never scaffold, never a fallback name; the §10 gate says 'not assessable' since W449), Mode 3 gates now GATE every mover (W452) but pause the ship, not a stage mid-journey, and §4.6 Develop has no stage — plan P3.1 |
| 2 | Generate a living Enterprise IDBO (VSB) for the user | ● | `/establish` (and the SSE stream) persists a real, governed VSB with Board + Chief + economy + plan + registration (W248/W255); 219 entities live. Caveat: born at `stage: "commercialise"` from a literal (Owner ruling 3.10) and, on the floor, bodied with scaffold (P1.2) |
| 3 | VSB org (AI CEO→C-Suite→CoE→BTO) curates work | ◐ | The full-hierarchy cascade runs on the owned fabric with real facility requisitions, plan binding and UEG seal (W446 re-verified, ledger R3.7) and the Sovereign Evolution cycle runs — but the hub's DEFAULT tab (AI CEO chat) is a detached "Galactic Era" Ollama roleplay outside the fabric (R3.0), review gates are advisory (R3.1), and the Board's grounded deliberation is API-only (R3.4). ◐ until P1.3/P1.4 land |
| 4 | Reconfigurable, combinable resource fabric | ● | 41 federated resources (live count); compose → simulate → commit → **every composed resource runs its REAL engine** on the native swarm (W199–W250); cascades user-definable on `/native-ai` and `/resource-fabric` (W446 re-verified, R4.4). Caveats: the per-VSB swarm is one fixed 4-stage template (P2.8); the Composer tab was a disconnected canvas (P1.12) — retired W460 for the real designer |
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
- **2026-09-19 (W473)** — §4 updated (P1.16 closed: canon and suite hygiene; Phase P1 complete); §6.4 re-rendered
  (P1.16 ✅; FU-003, FU-004, FU-011, FU-025–FU-028, FU-066–FU-070, FU-073 closed; FU-076–FU-079 added; P1.16's
  route handed to P2.4; FU-075 re-slotted to P2.4).
- **2026-09-18 (W472)** — §4 updated (P1.15 closed: the strict-read class); §6.4 re-rendered (P1.15 ✅; FU-021, FU-042,
  FU-049–FU-056, FU-062 closed; FU-075 added).
- **2026-09-18 (W471)** — §4 updated (P1.14 closed: board pack measured on its narrative, refused over an empty
  blueprint, versioned by content; the Chief's Opening writes nothing from the floor, owner-editable); §6.4 re-rendered
  (P1.14 ✅; FU-074 added).
- **2026-09-18 (W470)** — §4 updated (P1.13 closed: one tool registry; dead flagship tabs gone; catalogue live/source/legacy);
  §6.4 re-rendered (P1.13 ✅; FU-071, FU-072, FU-073 added; P1.13's route handed to P2.4, P1.16 kept last).
- **2026-09-18 (W469)** — §4 updated (NEXT retired; routes; PLAN NOW live); §6.4 gains the generated PLAN NOW block;
  42 rows re-slotted to P1.15/P1.16/P2.6/P2.7/P2.8/P2.9; FU-067 to FU-070 added.
- **2026-09-17 (W468)** — §4 updated (an unreadable VSB ledger is refused, never replaced by empty books; a raised
  heartbeat visit advances the rotation); §6.4 re-rendered (FU-041 closed; FU-049 to FU-066 added).
- **2026-09-17 (W467)** — §4 updated (the heartbeat cycle distributes its recognised revenue once; the revenue
  store refused when unreadable); §6.4 re-rendered (FU-022, FU-043, FU-044 closed; FU-048 added).
- **2026-09-17 (W466)** — §4 updated (stranded transfers found and completed once; failed transfers answered from the
  ledger); §6.4 re-rendered (FU-023 closed; FU-047 added).
- **2026-09-17 (W465)** — §4 updated (service contracts settled once with every unpaid outcome recorded; the
  owner-payments, contract and pending-transfers stores refused when unreadable); the persistence-hardening row
  updated; §6.4 re-rendered (FU-015, FU-016, FU-024 closed; FU-034 … FU-046 added, FU-038 and FU-046 closed).
- **2026-09-16 (W464)** — §4 updated (the Owner's Change Control rulings: Board ratification, decisions on the UEG,
  economy holds CRITICAL, genome engine fixed); the apex-governance paragraph gained the ratification routes; §6.4
  re-rendered (FU-012, FU-013, FU-014, FU-020 closed; FU-025 … FU-033 added).
- **2026-09-14 (W463 documentation sweep)** — after the W463 push, every document was audited for current-state claims W463 left stale and each finding verified by a second agent: the status line and §4 suite figures (371/15/0, 347 test functions, 386 items), the §6.3 persistence-hardening row (FU-015/FU-016 still open; the roster serialised) and the change-control isolation row (write routes read an identity since W459; the read routes are still unscoped).
- **2026-09-13 (W463)** — §4 updated (economy approval integrity); §6.4 re-rendered (FU-002 closed; FU-015 …
  FU-024 added).
- **2026-09-13 (W462)** — §6.4 Scheduled follow-ups added (generated from `docs/FOLLOWUPS.json`); §1 update
  protocol gains the follow-up rule; §4 updated.
- **2026-09-13 (W461)** — transformation verification honest: halted/partial/constant-verified runs no
  longer move objectives on this plan; §4 updated.
- **2026-09-13 (W460)** — delivery-plan P1.12 delivered (composer retired; no unevaluated compliance
  claim); §4 updated; the §7 pillar-4 caveat annotated retired; glyphs unchanged.
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
