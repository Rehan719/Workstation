<!--
  LIVING DOCUMENT — Workstation IDBO Design & Development Action Plan
  Maintained collaboratively by: the Owner (Rehan), Claude (Anthropic), and any AI agent working this repo.
  This is the single source of truth that bridges VISION ↔ GROUNDED CURRENT STATE ↔ ACTION.
  UPDATE PROTOCOL is in §1. Do not let this drift — every substantive change to the codebase
  should be reflected here in the same change.
-->

# Workstation IDBO — Living Design & Development Action Plan

**Status:** LIVING · **Last reconciled:** 2026-09-05 (W446) · **Grounded baseline:** in-house-first native AI fabric (owned models/orchestration/swarm/ensemble + autonomous workflow tree), integration suite **389✓ / 15 skip / 0 fail** (365 test functions, 404 items) at the last full run (W481), frontend tsc 0 errors, both CI green on `main` at the last pushed commit (re-check the run for the current one)
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
**W474 (2026-09-19, Claude Fable 5.1):** MILESTONE M1 — the fidelity workflow re-run against HEAD `cdd7619f` on a fresh
backend (:8083, native floor): six assessors, six refuters, 60 findings (53 survived, 7 overturned),
each carrying the tier the refuter stands behind. Standing Tier-1 count **14** (NOT met — the Tier-1 entries are register rows FU-080…FU-093); Tier-2 19,
Tier-3 17; STUB 8 · MISSING 0 · DOC_OVERCLAIM 4 · API_ONLY 0 · PARTIAL 38 · DELIVERED 10. `docs/VISION_FIDELITY_LEDGER.md` is v4 (`scripts/render_fidelity_ledger.py … 4 W474`); v3 kept
as `VISION_FIDELITY_LEDGER_v3.md`. Phase P2 begins at P2.1.
**W475 (2026-09-19, Claude Fable 5.1 → Claude Opus 5):** P1.17 The second truth pass — the fourteen ledger-v4 Tier-1 entries closed by
execution: the halal screen's negation window (REVIEW with the phrase, never 'Prohibited element'); the tafsir's floor
subject (never the Arabic block); the seven management-systems generators without recall and with provenance; the
living text and roster listing tied to the heartbeat's lever; scaffold-composed documents 'template' to the shipped
gates; officers' stances only from a model's last line; recalled personas neutralised; the Chief titled for what serves
it; the last three Command Center channels honest; no 'proceed'/'commit-ready' on a gate that could not assess; live
products only over served routes; the realisation figure labelled API surface coverage; costs an expense, never a
reserve. FU-080…FU-093 closed. MILESTONE M1 re-runs next (W476).
**W476 (2026-09-19, Claude Opus 5):** MILESTONE M1 re-run after P1.17, against HEAD `929508f0` on a fresh backend
(:8086, native floor): ledger v5 (60 findings, 53 survived, 7 overturned; STUB 12 · MISSING 1 · DOC_OVERCLAIM 2 ·
API_ONLY 2 · PARTIAL 36 · DELIVERED 7). Standing Tier-1 count **27 — NOT met**: surfaces neither earlier audit sampled
(each is capped at ten findings per region) — above all the compliance screen certifying what it cannot know (a
one-word ethical FAIL sealed as a safety verdict; 'compliant'/'safe' recorded as measured from keyword screens), the
Basmala prepended to ayah 1 of 112 surahs, a vetoed Genesis candidate still selected, and organism/economy readings
that cannot fail. P1.18 (the third truth pass) carries them as FU-094…FU-120. v4 kept as
`VISION_FIDELITY_LEDGER_v4.md`.
**W477 (2026-09-19, Claude Opus 5):** the one-time TRUTH SWEEP the Owner chose over repeated sampled audits: every
reached frontend surface (83 of 114 files — every page — and the 273 `/api` paths they call, followed into their
handlers and every other writer) checked against the ten defect classes with no cap, each finding reproduced by a
skeptic. `docs/TRUTH_SWEEP_W477.md`: 228 reported, 190 reproduced — **106 Tier-1**, 84 Tier-2 (56 overlap ledger v5,
mostly as writers it did not name). Registered one row per emitting file: 36 Tier-1 rows join P1.18 (now 63 rows,
the whole reached-surface class), 63 Tier-2 rows ride the P2 items that own their areas (FU-121…FU-219).
**W478 (2026-09-19, Claude Opus 5):** on the Owner's instruction, a PRIORITISATION mechanism in the planning system:
each follow-up's priority is a product of named, shown parts — the vision area it serves (the section its title cites,
else its primary file, else a title word) × truth tier × reach (core journey · reached · internal) × criticality (the
current phase gate · later · Owner-gated) × breadth (untruths closed per fix) × effort — from the Owner's weights in
`docs/PRIORITY.json` (`agentic_core/plan_priority.py`). Inside a plan item rows run highest-priority first (the plan's
order and phase gates stand; a suggested order by total priority is shown, never applied); PLAN NOW and the
/transformation card name the highest-priority rows and the follow-up completion weighted by priority;
`followups.py priority` shows every score's parts, `add --tier/--area/--reach` and `reprioritise` set them.
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
  Next: P2.28 THE NINTH TRUTH PASS — no OPEN follow-up rides it, and 4 have — every row closed, which is NOT the same as the item being done: it closes on its ACCEPT clause.
  AREAS WITH NO OWNER (8), each retired when the item that owned it closed and no open item claimed it. A new row in one of these is UNSCHEDULED and names its own slot:
    [agentic_core/api/business_plan.py] retired with P3.4 by W587
    [agentic_core/support/] retired with P2.18 by W588
    [agentic_core/biomimicry/geospheric/regulator.py, agentic_core/biomimicry/geospheric/homeostatic_regulator.py, agentic_core/biomimicry/geospheric/balance_regulator.py] retired with P2.18 by W588
    [agentic_core/api/change_control.py, apps/workstation-superapp/src/pages/governance/, agentic_core/api/board.py] retired with P2.18 by W588
    [agentic_core/api/resource_fabric.py, agentic_core/api/swarm.py, apps/workstation-superapp/src/pages/developers/NativeAI.tsx] retired with P2.18 by W588
    [agentic_core/economy/, agentic_core/api/economy.py, agentic_core/api/marketplace.py] retired with P2.18 by W588
    [agentic_core/catalog/, products/, apps/workstation-superapp/src/pages/domains/] retired with P2.18 by W588
    [integration_tests/, docs/, config/] retired with P2.18 by W588
  Then, in order (the follow-ups riding each): P2.29 0/10 · P4.1 0/0 · P4.2 0/0 · P4.3 0/0 · P4.4 1/2 ·
    P4.5 0/0 · P4.6 0/0 · P5.1 5/5 · P5.2 0/0 · P5.3 0/0 · P5.4 0/0 · P5.5 0/0
  Done: 74 of 87 items — P1 18/18 · P2 27/29 · P3 29/29 · P4 0/6 · P5 0/5.
  Follow-up completion weighted by priority — P2: 100.0% of its rows' priority closed (345 of 345 rows); every phase's rows: 99.3% (the retired pre-plan queue left out).
  Follow-ups: 7 open — 6 ride a plan item (0 high), 0 unscheduled, 1 awaiting the Owner; 548 done, 18 dropped.
<!-- plannow:end -->
<!-- pace:begin (generated by scripts/followups.py render - never edit by hand) -->
WHERE THIS IS GOING (generated — 74 of 87 plan entries done, 7 open rows)
  PACE, over the last 6 round(s) that closed anything (W625, W627, W628, W630, W631, W633): 9.0 rows closed per round, 0.0 found, net 9.0.
  RATE USED: 9.0 rows/round — steady (one-time intakes excluded).
  NEXT — P2.28: no registered row rides it — its work is the item's own ACCEPT criteria in the plan, which no row count measures.
  ALL OPEN ROWS: 7 — of which 6 ride a plan item ≈ 1 round(s) at the overall rate, and 1 await an OWNER decision (FU-473) and are not projected.
  PLAN COMPLETION (a different population from the rows): 13 open item(s) - 7 build ≈ 18 round(s) at 0.402 item(s)/round, 6 owner-switch (not projected). 74 of 87 plan item(s) carry a DONE marker, across a span of 184 round(s) (W449 to W632) - a rate of 0.402 item(s) per round, which is the rate an ITEM is completed at and not the row rate. Over the last 6 build round(s) 0 item(s) closed (none); a six-round window cannot measure something that takes many rounds, which is why the span is used. 13 item(s) remain open, of which 11 carry NO registered row - their work is their own ACCEPT criteria and no row count covers it. THE RATE'S POPULATION: every completed item is in P1, P2, P3, so this is the rate THAT work closed at, applied to phases whose work differs. NOT PROJECTED: 6 open item(s) (P4.1, P4.2, P4.3, P4.4, P4.5, P4.6) are declared owner-switch - a switch the Owner flips is not closed by a round, so counting it as rounds would invent them. PROJECTION COVERAGE: 1 of 7 build item(s) carry a registered row; the other 6 have never been sized, so the figure is an average over a population most of which no round has measured - it is the weakest number on this page.
  BY ITEM (each at its OWN measured rate; — = too few rounds have closed one of its rows to measure): P4.4 1r— · P5.1 5r—
  BIGGEST BATCH: none — no sweep class has an open row left; every row citing one of them is closed
  BIGGEST BUNDLE: P5.1 — one subsystem, 2 row(s) across 3 file(s). It advances those items; only their own ACCEPT criteria close them.
  This is arithmetic over an observed mean, in rounds. It is not a date and not a promise;
  it moves every time a round closes or registers a row.
<!-- pace:end -->
<!-- followups:begin (generated by scripts/followups.py render - never edit by hand) -->
SCHEDULED FOLLOW-UPS — every task a round finds and does not do is a row in docs/FOLLOWUPS.json, added in
the same commit (python scripts/followups.py add routes it to the plan item that owns its area; a high one
rides the next open item) or slotted OWNER (waits on an Owner decision; never scheduled). A round that
finishes an item marks it with python scripts/followups.py done P1.13 --by W### — its rows move along the
routes or are closed first; the suite fails on a row left on a finished item.
Open 7 (6 scheduled, 0 high · 0 unscheduled · 1 awaiting the Owner) · done 548 · dropped 18.
  P4.4 — Managed Postgres — migration dry-run script and rollback proven on a copy first
    FU-284 [medium] [p 1.5] P4.4's pre-flight has not been started: six database dependencies are declared and imported by nothing, so no migration dry-run or rollback exists to prove — P4.4 reads 'Managed Postgres - migration dry-run script and rollback proven on a copy first'. That pre-flight is OURS to build; the switch is the Owner's. Measured while correcting FU-282: sqlalchemy, sqlmodel and psycopg2-binary are DIRECT dependencies in pyproject.toml and no .py under agentic_core, integration_tests or scripts imports any of them; asyncpg and alembic are pinned in requirements.txt as transitive dependencies of prefect. So the toolchain for a Postgres migration is installed and NOTHING has been written with it - there is no schema, no migration, no dry-run script and no rollback, which is exactly what P4.4 says must exist before the Owner is asked to flip anything. A driver is legitimately loaded by URL rather than imported, so their presence is not the defect; the ABSENCE of the pre-flight they were installed for is. THE WORK, when P4.4's round comes: a schema derived from the stores that actually accumulate (VSB entities, the token ledger, the UEG chain, marketplace listings), a migration that runs against a COPY, a rollback proven on that copy, and a measured statement of what the JSON stores hold today so the migration has a known input. NOTHING is switched by this row. (found W500 (the corrected FU-282 analysis: the database dependencies exist for P4.4 and nothing imports them))
  P5.1 — ONE TENANT, CONCEPT TO COMMERCIAL OUTPUT, MEASURED
    FU-454 [medium] [p 20.5] Genesis presents three phases for a seven-stage journey, so three stages reach no reader — The pre-flight asked which surface shows the new develop keys and the answer was none, which led to reading the page properly. GenesisJourney.tsx builds its phase list from exactly three entries - Conceptualisation, Design and Development, Enterprise Commercialisation - while the journey response returns seven stage bodies: phase_1_conceptualisation, stage_3_innovate_research, stage_5_model_simulate_rank, phase_2_design_development, stage_6_develop (added W597), stage_7_operational_intelligence and phase_3_commercialisation. So stage_3_innovate_research, stage_5_model_simulate_rank and stage_7_operational_intelligence are computed, paid for in model calls or floor composition, verified in stage_verifications, and shown to NOBODY on the page a founder actually reads. W597 fixed only the one it created: the develop body and its artefact verdict now render inside the Design and Development card, because that card is NAMED for development and was showing only the design body, and the export gained the stage too. The other three are older and were not that round's to take. NOT A FABRICATION - nothing claims they are displayed, and the export includes two of them - but a journey that computes seven stages and narrates three understates its own work to the only person who sees it, and the verifications of the unshown stages count toward the stages_verified figure the page DOES show. REMEDY: either render the missing stages, or state on the page which stages are summarised rather than shown, so the count and the narrative agree. An informed decision needs reading why the three-phase framing was chosen - it matches the marketing arc in the header - so this is a design question and not a mechanical fix. (found W597 pre-flight)
    FU-449 [medium] [p 15.9] Every entity is born with three template objectives carrying NO KPI, so §17.5's release gate blocks all listing until a founder sets them — _seed_plan_from_journey gives every established entity three objectives - 'Validate the concept', 'Deliver the design', 'Launch to market' - each with an EMPTY kpi field. R5 (Owner ruling 2026-10-05b) made KPIs load-bearing: §17.5's gate blocks marketplace release until the owning VSB's objectives carry them. MEASURED CONSEQUENCE: every newly-born entity is now blocked from listing any product until a founder sets three KPIs by hand, which surfaced as a 409 in test_w586_p37 whose subject is repo reachability and not the gate. THE GATE IS NOT THE DEFECT and is not weakened: §17.5's invariant is a KPI gate before customer delivery, and blocking release on unmeasurable objectives is precisely what was ruled. What this exposes is that THE PLATFORM CREATES OBJECTIVES IT CANNOT MEASURE - an objective with no KPI is an unmeasurable claim at birth, which is the class this phase exists to remove. AND THE PLATFORM MUST NOT INVENT THE KPIs: a measure the platform makes up for a founder's objective is a fabricated figure, which is worse than asking for one, so the gate's message now names these three as platform-seeded so a founder knows whose omission it is. THE WORK: either establishment stops seeding objectives it cannot measure (asking the founder for a KPI as it asks for a name), or the seeded three are marked as drafts that do not gate - a decision about what establishment owes a founder, not a defect fix, which is why it is registered rather than done in W594. (found W594 — surfaced by R5's KPI gate blocking a guard whose subject was repo reachability)
    FU-417 [medium] [p 9.5] A beat skipped the cadence for both layers in the full suite and the cause was never recorded; not reproduced since — OBSERVED ONCE IN W589 AND NOT REPRODUCED, which is why this is open rather than closed. test_w585_p33 failed in the full suite and passed in isolation: it ages both cadence layers' history past their periods, asserts with cadence.due() that each is genuinely DUE, runs one real beat, and the beat's actions came back as ['pulse', 'homeostasis', 'genome_scan', 'compliance_rescreen', 'transformation_tick'] with no 'cadence_refresh'. So the step raised, because the whole step sat in `except Exception: pass` - and the exception was swallowed, so the run that failed left NO record of the cause anywhere. The two defects that reading the step then found were fixed in the same round (the swallowed reason, and a single try around the whole layer loop that discarded a layer's completed refresh when a later layer raised), plus a confirmed ValueError where _compose ran int() on a progress field it does not own. The re-run with all three in place is green and the failure did not recur, so it CANNOT be said which of these was the cause, or whether the cause was any of them: a green run after a change is not evidence when the red run was not reproduced first. What remains to be done is therefore not a fix but a reproduction: the beat now records could_not_run with the exception type, message and a basis stating that a layer which could not run is still due, so the next occurrence names its own cause in the suite output and the guard's assertion message carries it. Candidates worth testing deliberately if it recurs: a store_lock TimeoutError on the plan path (store_lock raises after its timeout rather than writing unserialised, and the plan is written by several tests in a worker), and a strict read failing on a plan an earlier test left in a shape business_plan._load rejects. Do not close this row on another green suite; close it on a reproduction with the recorded reason, or on a measured argument that the fixed defects were necessarily the cause. (found W589 full suite)
    FU-301 [medium] [p 4.5] The parallel suite stalls about one run in three, with every worker in flight at once - cause not established — W507 delivered the per-worker store isolation FU-249 asked for and MEASURED the win: 50m42s serial to 10m35s on six workers (4.8x), with the pass sets matching exactly (466 passed, 15 skipped, 0 failed both ways). It is NOT the round default because of this row. MEASURED FAILURE MODE: of six parallel runs, three completed and three STALLED - at 74%, 89% and 57% - and in the stalled runs EVERY worker was in flight simultaneously (a -v run showed six tests started with no verdict, one per worker) with the controller and one worker process still alive and no CPU. So it is a simultaneous stall of all workers, not one slow test. WHAT WAS RULED OUT: (a) store_lock itself - it is a per-path threading.RLock plus an O_CREAT|O_EXCL lockfile with a bounded 10s timeout that RAISES TimeoutError and breaks a stale file after 30s, so it cannot deadlock indefinitely; (b) the shared repo register - a stray docs/FOLLOWUPS.json.lock was found and removed, and deselecting all 19 tests that spawn a subprocess or write a repo file did NOT change the stall rate (1 of 3 still stalled), so that lock is a real contention point but not this cause; (c) my own new guards - the stalls predate them (the first two parallel runs stalled before any W507 guard existed); (d) order dependence - --dist load scatter was green on the runs that completed, so no order-dependent test beyond the one W498 fixed. STILL UNEXPLAINED: what all workers block on at once. WHERE TO LOOK NEXT: get a stack from a stalled worker (faulthandler in the controller does not reach xdist subprocesses - try PYTHONFAULTHANDLER with a per-worker dump, or py-spy against a live worker pid); check for Windows handle or process exhaustion, since six workers each build the full app (about 18s and 54MB each) and several tests spawn further subprocesses; and check whether the module-scoped client fixture's app construction can block when six copies start together. UNTIL THEN: the serial run is what a commit is trusted to, and -n 6 is for a fast read only. A tool that fails silently a third of the time is the instrument-that-cannot-fail defect inverted. (found W507 measurement of FU-249's delivery)
    FU-399 [medium] [p 4.1] 81 page guards are still text scans and 295 data-testid attributes are still unexercised, now that a renderer exists — W579 installed the frontend runner (vitest 2.x pinned to the vite-5 line, jsdom, @testing-library/react + jest-dom) and wrote the FIRST rendered page guard in this repository. It earned its place immediately: its first draft asserted the insights-error chip, failed, and the failure showed that the insights list rendered an insight's TITLE and never its DETAIL - so the clause W576 deliberately moved INSIDE insights to refuse the 'you have no projects' reading reached no reader at all. A text scan found the string present in the source and would have concluded the opposite. THE SCALE: 81 tests in integration_tests/test_mvp_spine.py read a .tsx file and every one asserts by substring, and 295 data-testid attributes exist across the app for a renderer that until now did not exist. THIS IS NOT A REQUEST TO DELETE THE SCANS. A substring scan is not worthless and must not be characterised as such: one caught the {false && ...} class in W577, where a render was switched OFF while its field name survived in the source, and an AST or DOM check would have missed it. The two instruments answer different questions - a scan asks whether the code says it, a render asks whether a person sees it - and a claim about what a PERSON SEES belongs to the second. THE WORK, as a scheduled migration rather than one round: convert the guards whose claim is about what is RENDERED (an empty state, a disclosure chip, a figure with its basis, a control's direction), leave the ones whose claim is about the SOURCE (a binding present, a gate not disabled, a literal absent), and record which of the 295 testids are exercised so the count stops reading as coverage. ALSO: nothing in the Python suite shells out to node, so a guard that EXECUTES the runner would add an environment assumption CI does not carry - the round runs npm test the way it runs tsc, and the W579 guard asserts only that the configuration is intact and says so in writing. (found W579 (FU-352's remainder, scheduled as that row required))
  AWAITING THE OWNER — recorded, never scheduled into a round without the Owner's instruction:
    FU-473 [medium] REVIEW: which of the 16 unchecked constitutional constraints apply to an avatar reply, and which should be retired from the declared set — Deferred by the Owner on 2026-10-06 as choice 3 of FU-472. Gate 6 now clears by coverage and every delivered reply names the 16 it did not check: 15 with no instrument anywhere (edge_first_sovereignty, causal_sovereignty, biomimetic_fidelity, genetic_immune_topology_integrity, statistical_rigor, legal_precision_hard, adversarial_co_evolution, trillion_token_provenance, human_ai_constitutional_co_sovereignty, oam_qkd_software_only, federated_consensus, commercial_integrity, first_principles_grounding, sincerity_integrity_loyalty, lob_fixpoint) and 1 whose instrument is never given its input (thermodynamic_accountability). For each, the Owner decides: keep and build an instrument, keep as declared-but-unchecked (stated on every reply, as now), or retire from the declared set with the reason recorded. Nothing is retired without that decision. (found W607 (FU-472 ruling, choice 3 deferred by the Owner))
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
- **2026-09-26 (W494)** — a verdict that cannot come out otherwise is not an assessment: the gate's
  own batch, fourteen rows on P1.18. A figure is decided on what was MEASURED; an unmeasured term is
  unknown, never 1.0; where nothing was measured the decision HOLDS. This batch exists because of how it
  was found: the gate had been closing at 2.67 rows a round against the register's 9.83, and the cause was
  that **20 of its 35 open rows cite no sweep class at all** — they came from the fidelity ledger, and the
  batch generator groups by cited class, so it could only ever propose three of them.
  The organism's health composite is 0.4·immune + 0.4·self_healing + 0.2·metabolic. With no circuit
  tracked, self-healing is DEFAULTED to 1.0, and the metabolic term is a simulator whose production always
  exceeds consumption, so it only rises: after ~25 reads the blend is 0.6 + 0.4·immune for the rest of the
  process's life. The mode read NOMINAL with "Standard operations active" while the only measured term was
  immune health 0.0 at threat CRITICAL; the Change Control review rule, the LOW auto-approval and the twin
  pre-validation fallback had no failing branch; four survival levers were unreachable from the first read.
  All of them decide on `composite_health_measured_only` now — which already existed beside the blend and
  which no gate read. Plus ten more verdicts of the same shape, including a viability test computed as
  "'not viable' not in tail" that the floor never writes, a "100% coherence" figure that counts mounted
  routes, a green BUILT chip meaning "produce() did not raise", and an emerald governance verdict from a
  gate handed an intent label and a constant sentence at five call sites.
  **The refutation raised 77 findings, verified all 77 and confirmed 76 — thirty-two of them this round's
  own rule broken inside its own fix.** Six would have shipped broken: the suite was RED on a pre-existing
  BMS enum (four more pinned enums rejected states the round added), a page would have thrown on a
  governance dict rendered as a JSX child, a badge would have printed an object where a provenance belongs,
  and a claim the round wrote into a basis string was FALSE — the fabric's own reconfigurable
  `metabolic_load`, declared "float 0-1" and validated nowhere, took the process-wide ATP singleton from
  0.358 to 0.033 in one call. The largest group was basis strings asserting universals instead of computing
  them: the health gate wrote "carries a defaulted and a simulated term and cannot fall below 0.6" into
  every permanent change record, reproduced false at a blend of 0.472 with self-healing measured.
  65 blinds, all caught, none vacuous; probe 30/30 with two checks honestly unassessable. The gate closed
  from 35 rows to 21 and its own rate rose from 2.67 to 4.0 per round, so its projection fell from fourteen
  rounds to six. FU-265 registers the four pre-existing readers of the metabolic term the round left.
- **2026-09-26 (W493)** — a present-tense claim needs the process running: the C4 batch taken
  repo-wide across P1.18, P2.4 and P2.9 (nine rows). Three shapes. A counter advanced before the thing
  happened — `/vsb/{id}/evolve` incremented `generation` on FILING, while the genome mutates only after
  the Owner approves the change record. A capability in the present tense while its lever is off or its
  scope is narrower than stated — "self-aligns … continuous" with `execute: false` and `auto_align` off;
  "every living VSB each beat" when exactly one is tended per beat; "self-running" with all five autonomy
  levers off and the page reading none of them; an endowment base "protected" by nothing but a waterfall
  share above zero. And a control naming what does not exist — a Run Pipeline that discarded the canvas,
  a static Event Stream rendered even when the read FAILED, badges for preferences nothing acts on, and
  two governance bodies absent from the codebase.
  This round added a mechanical pre-flight over its own diff (`scripts/selfcheck_diff.py`, built from the
  98 defects the W491 and W492 refutations confirmed). It found two defects before any agent ran and,
  re-run over the FINISHED diff, two more — including one my own notes recorded as applied that was not
  in the tree. The refutation's 63 confirmed findings are the round's real result: findings about the nine
  row fixes fell 27%, and 26 of the 63 were about the two things the round ADDED (eleven in the tool,
  fifteen in my own guard legs). A new artefact was held to a lower standard than the code it checks; five
  of the tool's seven checks were defective, one of them missing the exact rename it was written to catch.
  53 blinds, all caught, none vacuous; probe 34/34 with nothing unassessable, including the state the round
  is about driven rather than skipped (a lever set while the heartbeat is stopped). FU-264 registers what is
  not done: an entity's evolution lifecycle is true and reaches no surface.
  The round also turned its own rule on the PLANNER. The pace block projected each plan item's backlog at
  the rate measured over the WHOLE register, so the gate read "35 open rows ≈ 4 rounds" while the six build
  rounds on record closed 16 of its rows — 2.67 per round, fourteen rounds. A class-wide batch closes rows
  on five or six items at once, so no single item moves at the overall rate. Each item is now projected at
  the rate measured on its OWN rows, prints nothing where too few rounds have closed one of them (P2.3, P2.7
  and every P3 item), and the block says which population each figure covers.
- **2026-09-25 (W492)** — the page says what the engine said: the C5 batch taken repo-wide across
  P2.4, P2.6, P2.7, P2.8 and P2.9 (ten rows — none of them on the gate item). Nothing that qualifies a
  claim may be dropped between
  the engine that produced it and the surface that shows it, and no surface may present as current,
  verified or successful what the API reported as stale, unchecked or failed. A second writer stripping the
  qualifier (`_screen_listing` kept the verdicts and dropped the screen's own basis, so a refusal read as a
  pass); a 409 from a pending review gate swallowed on a page whose own comment says actions never fail
  silently; an error frame re-raised inside the page's own malformed-event catch, leaving an optimistic
  "running" uncorrected; and an anatomy card printing a hard-coded "blended (20% simulated)" beside its own
  line saying 40% measured. A live break the round itself caused: a helper inserted between a
  `@router.post` decorator and its handler rebound the route, which 422'd every call while the app still
  booted and three guards stayed green.
- **2026-09-25 (W491)** — a count says what population it covers: the C10 batch taken repo-wide across
  P1.18, P2.4, P2.6, P2.8 and P2.9 (ten rows). A fetch limit is not a total; a catalogue of what the platform
  supports is not a record of having operated it; a resource having matched is not a facility having run.
  The UEG Audit Trail counted the events the page had fetched; the organism signal feed read `type`/`ts`
  while the API sends `signal_type`/`age_seconds`, so up to 25 signals rendered blank; the cockpit headed
  nine management standards in the present tense, identical for every entity, none operated or certified.
  The lesson the refutation produced: a NATURE field cannot report an OUTCOME — `kind` (what a resource
  IS) was used by five counters to say what HAPPENED, so every failed attempt counted as a run or a read
  (31 of 47 findings). 79 blinds, 17 of them vacuous on the first pass because an assert containing the
  literal it forbids matches itself. This round also broke CI once: a guard asserted
  `repository_commits_total > returned`, and CI's shallow checkout makes both 1 — the guard was fixed to
  pin the mechanism, not the code.
- **2026-09-25 (W490)** — floor-served output says so wherever it goes: the C7 batch taken repo-wide
  across P1.18, P2.3, P2.4, P2.6 and P2.9 (twelve rows). The mechanism already existed — one badge
  helper, one map helper, one export line — and this round applied it everywhere and made the APIs
  carry what the surfaces need. A badge in the DOM is not a label on the text: the career documents and
  management frameworks downloaded with only the floor's own marker. `gateway.query` discards
  served_by, so a panel headed AI Assessment and a Concept Blueprint had nothing to render. /solve
  printed eight named analysers over THREE gateway calls. Settings told every user "nothing is inferred
  from your activity" while two surfaces recall prior interactions. And eleven export formats credited
  the platform's AI fabric for content the deterministic floor composed.
  The refutation raised 40 findings — and 27 of its 45 agents died on a full disk while the run still
  returned a normal-looking result (56 accumulated worktrees, ~9 MB free; cleaning them recovered
  9.6 GB). Resumed: 18 verified real, almost all either a NEW claim the round could not back (a badge
  claiming the floor where nothing served at all; the server phrase dropping the browser's count rule;
  a verbatim ingest exported as composed; the corrected privacy line replaced with another falsehood)
  or a SECOND READER left disagreeing (card footers contradicting their own subtitle; the Business Plan
  page rendering the tree the cockpit badges; a second deliverables list; FU-134 changing the API and
  not the page). Two of the round's own guards were broken — W453 and W488. 66 blinds, none vacuous;
  probe 17/17. Registered: the shared-namespace isolation defect (high, on this gate) and the
  worktree/disk failure mode.
- **2026-09-21 (W489)** — a reading is measured, or it is not presented as a reading. The first round
  taken REPO-WIDE: class C3 (invented or constant readings) across P1.18, P2.4, P2.8 and P2.9 at once —
  twelve rows, because the same mechanism closes 4 inside the gate item and 12 across all of them. A
  fixed 0.85 shown as "EMS +85%" beside a process-lifetime CO2 total labelled as this run's; a learner
  at the SM-2 floor told they retain the ayah well; a card's "Confidence 1" floored out of three fields
  the API never sends; a document nobody read filed at 70% confidence from an except branch; an
  unparseable value plotted as a real zero; an IDLE host displaying "Work"; a platform-wide QMS rate fed
  by a typed number and called "a real rate"; and nine cognitive engines claimed over a cascade that
  runs six — the other three are PLANNED work and now say so, naming P3.13. Also corrected W488's own
  claim: its recall audit grepped one method name, so 29 generation callers still inherited
  augment=True; the gateway default is now off and the two conversational callers opt in by name.
  The refutation returned 36 findings, 19 real — four pre-existing tests the round broke, the wrong plan
  item in eleven places, and its own class re-committed twice inside its own fix. 78 blinds, none
  vacuous; probe 19/19.
- **2026-09-20 (W488)** — the page and the API say the same thing: the first round the BATCH mechanism
  chose (class C5, six rows — FU-136, FU-137, FU-142, FU-143, FU-149, FU-150). The Owner's business plan
  is read whole or REFUSED, never replaced: a 503 naming the file on every scoped route, an unreadable
  plan kept as a marked row in the listing instead of vanishing from the rows and the count, and the
  scope reduced to a filename. The apex tier — and every other generation-class caller in the repository,
  eleven of them — reads the Owner's words and nothing else; the avatar conversation is the one
  deliberate exception and says why in place. A legal form the registry overrode is disclosed on six
  economy surfaces WITHOUT inventing a claim the caller never made, and W313's binding (silently
  evaporated for every VSB known to the vsb store but not the living roster, because the leg read a key
  no writer sets) holds again. The management floor offers a frame to complete, the BTO page composes a
  blueprint and says nothing is provisioned. The refutation returned 29 findings, 25 verified real, and
  every one was this round's own class re-committed inside this round's own fix — now recorded as rule
  B4 with its four recurring shapes. 56 blinds, none vacuous; probe 22/22.
- **2026-09-20 (W487)** — the plan proposes the ROUND, not just the row: the third planning leg beside
  PRIORITY (which row) and PACE (how fast). `batches()` groups open rows by the sweep class their own
  evidence cites — rows are one per FILE, defects run ACROSS files, and that mismatch is why rounds that
  take the next row close two or three while the round that built one rule and swept its consumers closed
  seven. A multi-class row is ADVANCED, never counted as closed. `followups.py batches`, served on
  `/api/v1/plan/followups`, named beside the projection. Also records the measured round shape as B1/B2/B3:
  per-row 32 rounds → class batches ≈23, and the machinery run once per tree rather than once per fix
  (~4h → ~1h10 of the same evidence). FU-249 registers xdist as the remaining lever, not taken blind.
- **2026-09-20 (W486)** — the plan says where it is going, or says it cannot. `forecast()` measures the
  pace from the register's own record (which round closed each row, which round found it) and projects in
  ROUNDS. A one-time intake — an audit, a sweep, an interrogation — is NAMED and excluded rather than
  averaged in; too few rounds is not assessable; a backlog that is not shrinking projects nothing. No date
  is produced. Served on `/api/v1/plan/followups` and `/api/v1/plan`, rendered as a generated PACE block
  here and in the delivery plan under the same lockstep as PLAN NOW, and shown on the /transformation
  live card. 24 blinds, all failing first time.
- **2026-09-20 (W485)** — P1.18: a veto stops the journey (FU-097), a board pack says whose text it
  screened (FU-101), and exported text carries its provenance (FU-128). A vetoed candidate had still won
  and been carried into Design and Commercialisation with status 'complete'; the page's two-step Establish
  button bypassed the veto and built a living VSB from it — both establish writers now refuse with 409. A
  pending board pack no longer reports a verdict about its own placeholder, and the entity's own §11
  verdict travels beside it in three states. Refuted once (27 findings, 22 real); 44 blinds; probe 19/19;
  suite 392/15/0. FU-247, FU-248 registered.
- **2026-09-20 (W484)** — three more outside proposals interrogated and planned as **P3.19**: the
  biogeochemical cycle system, the Sovereign Wealth Fund and the inter-agent communication fabric. Of 28
  paths they present as “confirmed existing”, 3 exist; `archive/products/swf/` never has, and the SWF core
  in git history is 30 lines whose only verdict is a literal string. The three documents give DIFFERENT
  “immutable” PID gains for the same six cycles. The MAPPING is adopted — as a control surface over flows
  already measured, driven by the unwired geospheric regulators — and the real stigmergic scheduler in
  `_archive/jules-unwired/agentic_core/biomimicry/` is recovered rather than rebuilt. Register FU-242…FU-244,
  FU-246. `docs/BIOGEOCHEMICAL_AND_COMMS_REVIEW.md`. No behaviour changed.
- **2026-09-20 (W483)** — P1.18: a keyword screen flags and never clears. Seven rows (FU-094, 095, 096,
  099, 105, 115, 140), one defect — a word list recorded as a verdict. A severe-harm term is now escalated
  with the term named instead of convicting; an empty match no longer clears; a subject's own halal or
  benefit vocabulary is its claim, not a certification; §10 'compliant'/'safe' are met only where a row
  could actually assess; one complianceChip rules twelve §11 chips across nine pages. The halal
  pre-assessment stops composing a status from prompt headings and adds a deterministic ingredient screen;
  an ayah is the text of that ayah (the edition's prepended Basmala separated off, prefix sourced as 1:1,
  never written here). The escalation reaches a human exactly as the FAIL it replaced did. Refuted once
  (24 findings, 15 real); 67 blinds; probe 19/19; suite 390/15/0. Three findings registered on the items that own their areas.
- **2026-09-20 (W482)** — two more outside proposals interrogated and planned, not taken on trust: the Biomimetic
  Minimisation Engine (P3.17) and autonomous technical support (P3.18). Both largely EXIST already — archived by
  the W382/W78 sweeps — which `scripts/recovery_audit.py` (new) now finds mechanically: 516 sources moved into
  `_archive/`, 3 deleted outright, including the cognitive `bootstrap.py` that registers all nine engines and the
  `base_engine.py` contract the live registry calls. Register FU-233…FU-238. No behaviour changed.
- **2026-09-20 (W481)** — §5: the transformation cascade no longer certifies itself. Each stage declares what kind
  of check it ran; a presence check is never a verification; a run is validated only when a DELIVERY check
  verified, so today every run reads NOT ASSESSABLE and none writes onto the living plan. The digital-twin
  'simulation' is a projection with its formula stated. Closes FU-122 and FU-231; FU-232 registers the missing
  delivery check on P2.8.
- **2026-09-20 (W479)** — §4: the intelligence engines (BDP · SPI · APIE · DDPIE · Synthesis Nexus · /solve · /mjm)
  now stamp every stage with what served it and count only what ran; a failed call is never output, never feeds
  another prompt and is never green. Genesis records its lens and MJM calls, and a gate certifying text reads the
  servers of THAT text (`body_served_by`). Closes FU-121 and FU-153 on P1.18.
- **2026-09-19 (W478)** — §4 updated (the priority mechanism); §6.4 re-rendered (rows ordered by priority; PLAN NOW
  carries the top rows and the follow-up completion weighted by priority).
- **2026-09-19 (W476)** — §4 updated (the M1 re-run: ledger v5, Tier-1 27, NOT met; P1.18 added); §6.4 re-rendered
  (FU-094–FU-120 added, riding P1.18).
- **2026-09-19 (W477)** — §4 updated (the truth sweep: 190 reproduced, 106 Tier-1); §6.4 re-rendered (FU-121–FU-219
  added: 36 Tier-1 rows on P1.18, 63 Tier-2 rows on P2.3/P2.4/P2.6/P2.7/P2.8/P2.9).
- **2026-09-19 (W475)** — §4 updated (P1.17 closed: the fourteen ledger-v4 truth defects); §6.4 re-rendered (P1.17 ✅;
  FU-080–FU-093 closed; no route pointed at P1.17 — its rows rode it as high-severity rows).
- **2026-09-19 (W474)** — MILESTONE M1: ledger v4 issued (60 findings; Tier-1 14); §4 updated; v3 renamed
  `VISION_FIDELITY_LEDGER_v3.md`; the render script takes a version and renders tiers.
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
