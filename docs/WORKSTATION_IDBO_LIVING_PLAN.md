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
  Next: P2.2 Provenance to every surface — 2 follow-ups ride it.
  Then, in order (the follow-ups riding each): P2.4 19 · P2.8 6 · P2.10 1 · P2.11 0 · P2.12 0 · P2.13 1 ·
    P2.14 0 · P2.15 0 · P2.16 0 · P2.17 5 · P3.0 0 · P3.1 0 · P3.2 0 · P3.3 0 · P3.4 0 · P3.5 0 · P3.6 0 ·
    P3.7 0 · P3.8 0 · P3.9 0 · P3.10 0 · P3.11 0 · P3.12 7 · P3.13 0 · P3.14 1 · P3.15 2 · P3.16 1 · P3.17 5 ·
    P3.18 1 · P3.19 2 · P3.20 1 · P3.21 0 · P3.22 0 · P3.23 2 · P3.24 1 · P3.25 1 · P4.1 0 · P4.2 0 · P4.3 0 ·
    P4.4 1 · P4.5 0 · P4.6 0 · P5.1 0 · P5.2 0 · P5.3 0 · P5.4 0 · P5.5 0
  Highest priority in P2.2 (score · area): FU-294 30.0 unmapped · FU-290 17.5 domains_ux
  Done: 24 of 72 items — P1 18/18 · P2 6/17 · P3 0/26 · P4 0/6 · P5 0/5.
  Follow-up completion weighted by priority — P2: 82.1% of its rows' priority closed (111 of 145 rows); every phase's rows: 91.2% (the retired pre-plan queue left out).
  Follow-ups: 59 open — 59 ride a plan item (3 high), 0 unscheduled, 0 awaiting the Owner; 233 done, 10 dropped.
<!-- plannow:end -->
<!-- pace:begin (generated by scripts/followups.py render - never edit by hand) -->
WHERE THIS IS GOING (generated — 24 of 72 plan entries done, 59 open rows)
  PACE, over the last 6 round(s) that closed anything (W502, W503, W504, W505, W506, W507): 10.0 rows closed per round, 3.0 found, net 7.0.
  RATE USED: 10.0 rows/round — steady (one-time intakes excluded).
  NEXT — P2.2: 2 open rows — not projected: only 0 of the last 6 build round(s) closed a row on P2.2 (a rate needs 3); the overall rate is measured over every item's rows and is not this item's.
  ALL OPEN ROWS: 59 — of which 59 ride a plan item ≈ 6 round(s) at the overall rate, and none awaits an Owner decision.
  PLAN COMPLETION (a different population from the rows): 48 open item(s) - 42 build ≈ 102 round(s) at 0.414 item(s)/round, 6 owner-switch (not projected). 24 of 72 plan item(s) carry a DONE marker, across a span of 58 round(s) (W449 to W506) - a rate of 0.414 item(s) per round, which is the rate an ITEM is completed at and not the row rate. Over the last 6 build round(s) 6 item(s) closed (W505, W506); a six-round window cannot measure something that takes many rounds, which is why the span is used. 48 item(s) remain open, of which 30 carry NO registered row - their work is their own ACCEPT criteria and no row count covers it. THE RATE'S POPULATION: every completed item is in P1, P2, so this is the rate THAT work closed at, applied to phases whose work differs. NOT PROJECTED: 6 open item(s) (P4.1, P4.2, P4.3, P4.4, P4.5, P4.6) are declared owner-switch - a switch the Owner flips is not closed by a round, so counting it as rounds would invent them. PROJECTION COVERAGE: 17 of 42 build item(s) carry a registered row; the other 25 have never been sized, so the figure is an average over a population most of which no round has measured - it is the weakest number on this page.
  BY ITEM (each at its OWN measured rate; — = too few rounds have closed one of its rows to measure): P2.2 2r— · P2.4 19r≈19 · P2.8 6r— · P2.10 1r— · P2.13 1r— · P2.17 5r— · P3.12 7r— · P3.14 1r—
  BIGGEST BATCH: C9 (a decision that breaks its own rule) — one mechanism closes 2 row(s) across 3 file(s). Items: P2.4, P2.8.
  BIGGEST BUNDLE: P2.8 — one subsystem, 3 row(s) across 1 file(s). It advances those items; only their own ACCEPT criteria close them.
  This is arithmetic over an observed mean, in rounds. It is not a date and not a promise;
  it moves every time a round closes or registers a row.
<!-- pace:end -->
<!-- followups:begin (generated by scripts/followups.py render - never edit by hand) -->
SCHEDULED FOLLOW-UPS — every task a round finds and does not do is a row in docs/FOLLOWUPS.json, added in
the same commit (python scripts/followups.py add routes it to the plan item that owns its area; a high one
rides the next open item) or slotted OWNER (waits on an Owner decision; never scheduled). A round that
finishes an item marks it with python scripts/followups.py done P1.13 --by W### — its rows move along the
routes or are closed first; the suite fails on a row left on a finished item.
Open 59 (59 scheduled, 3 high · 0 unscheduled · 0 awaiting the Owner) · done 233 · dropped 10.
  P2.2 — Provenance to every surface
    FU-294 [high] [p 30.0] STAGE 1: 17 of 48 open build items state no ACCEPT bar, so they cannot be closed as written - 12 are also unsized — The measurement behind W505, and the reason no P2 item had closed while 32 rows closed in six rounds: an item closes on its ACCEPT criteria, and 17 open build items state none. Nothing was forgotten - there was nothing to check them against. MEASURED (scripts/../stage1_audit.py, bodies parsed from each slot heading to the next heading/MILESTONE/SEQUENCING - an earlier count was WRONG because its pattern required a bracket after the slot and so reported ten Horizon and ruling items as having no body at all): of 48 open build items, 31 state a bar and 17 do not. The 17: P2.2, P2.4, P2.7, P2.8, P3.0, P3.1, P3.2, P3.3, P3.4, P3.5, P3.6, P3.7, P3.8, P3.10, P3.11 (P2.3 and P2.5 were in this list and W505 wrote bars for them from their own bodies and closed them). Of the 17, TWELVE also carry no registered row - unbarred AND unsized, so neither population measures them: P3.0, P3.1, P3.2, P3.3, P3.4, P3.5, P3.6, P3.7, P3.8, P3.10, P3.11 plus P2.3 (now closed). THE WORK, and W505 demonstrated it twice: an item whose body already lists its deliverables does not need a bar invented - the deliverables ARE the bar, and writing them as ACCEPT is transcription plus a guard. P2.3 and P2.5 were closed exactly that way. THE RULE this establishes: a round that finishes an item's work must also write its bar if it has none, or the work cannot be recognised. WHY IT MATTERS BEYOND TIDINESS: the plan's own item projection (128 rounds) is an average over a population most of which nobody has measured, and it says so; 26 of 48 build items being unbarred or unsized is that weakness stated in figures. CORRECTED W505 (second pass): the figure 17 is STALE and this row used it in its own reasoning before checking it. Six of the seventeen have since been given a bar or closed - P2.3 and P2.5 were barred and closed, and P2.4, P2.7 and P2.8 were barred in the same round; P2.2 was never unbarred at all, its GUARD sits inline mid-line and the audit's line-start pattern missed it. The remaining unbarred set is P3.0-P3.8, P3.10, P3.11 and P2.16 (FU-297 covers P2.16). A measurement row that OVERSTATES a problem is the same defect as one that understates it. (found W505 Stage 1 audit)
    FU-290 [medium] [p 17.5] P2.2's own guard is unmet by 19: gateway.query( still has 19 call sites in agentic_core/api — P2.2 states its own bar as a GUARD: 'gateway.query( count in agentic_core/api == 0'. Measured at W504: the count is 19, across at least ai_query.py, business_plan.py and change_control.py (five sites in change_control alone). The item's work is to route those 47 original sites through query_meta carrying {served_by, is_external} and to badge the named surfaces. This row exists because the item carried ZERO registered rows while being 19 sites short of its own stated bar - which is the reason no P2 item has closed: the register tracked found defects and the plan tracked unbuilt work, and nothing connected them. Sizing is the work: each remaining site needs auditing for whether it can carry query_meta, and the badge surfaces the item names need checking one by one. (found W504 item-ACCEPT audit)
  P2.4 — The scatter: 67 ops in 38 clusters, 3–4 per round, audit-before-wire, retire freely
    FU-160 [medium] [p 49.0] sweep quality.py: 3 Tier-2 shortfalls (C1,C5) — Tooltip '7 biomimetic layers · self-managing · improving · healing'. Chip 'organism:… — S3.8 C5: Tooltip '7 biomimetic layers · self-managing · improving · healing'. Chip 'organism: immune 100% ·… → The record itself says 1 of 7 layers contributed (layers=['Immune']; layers_note: '1 of 7 declared biomimetic layers contributed…; S3.18 C1: 'ethical: pass — human: pass; environment: pass; quality: pass; value: pass (engine-backed)', directly under… → assure_delivery threads the floor's delivery_coverage into the ethical engine even when not_assessable is true, so the ethical…; S10.7 C1: Hovering the 'QMS —' chip on a floor-served clinical care plan, safeguarding triage, handover, legal… → The gate itself records that floor output cannot be assessed ('coverage cannot fail by construction'). Even so, that same floor… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-161 [medium] [p 44.6] sweep DomainTool.tsx: 3 Tier-2 shortfalls (C5,C7) — The downloaded or copied file is titled with the tool name (e.g. '<h1>Comparative Fiqh… — S9.2 C7: The downloaded or copied file is titled with the tool name (e.g. '<h1>Comparative Fiqh Research</h1>' or… → The export drops every disclosure the response carries. The fatwa research loses 'It is NOT a fatwa and does not constitute a…; S9.8 C5: The My Work record of a faith or employment tool output after one refine carries a 'refined ×1' chip. → run() saves text + [floor_note] + disclaimer (W456: disclosures travel with the saved text). The refine writer replaces output…; S10.10 C7: The downloaded care plan, legal document or marking feedback file. → exportText is score_summary + displayText. The disclaimer the screen shows ('must be reviewed and validated by a qualified… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-247 [medium] [p 35.0] The server-side export prints the opposite provenance label: floor-served content ships as produced on the AI fabric — W485 gave every BROWSER export a provenance line (lib/api.ts provenanceLine, used by My Work and DomainTool). agentic_core/api/deliverables.py still stamps its own page one with wording that credits Workstation's AI fabric for content the deterministic floor composed, so the server-produced artefact says the opposite of what the browser-produced one now says about the same text. FIX: one statement for both — the export names what served it, and a floor-served export says the floor composed the headings and supplied no analysis. (found W485 refuters (verified real) — found while applying the rule, not delivered)
    FU-170 [medium] [p 24.6] sweep ReactorStudio.tsx: 2 Tier-2 shortfalls (C2,C5) — 'Max Q1 (240)' names one leader. — S5.9 C5: 'Max Q1 (240)' names one leader. → The backend was fixed (W433) to report ties: analytics.max.tied_with = ['Q3']. The page's StudioResult type and the row renderer…; S5.12 C2: The tooltip reads '§11 live compliance — sharia_halal:pass · uk_legal:review · regulatory:pass · ehs:pass ·… → The backend reasons say 'halal vocabulary present and no prohibited (haram) term — a keyword screen, not a certification',… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-302 [low] [p 24.5] Sample and count the persisted outputs written while cross-request recall was the default (FU-256's part (a)) — FU-256's parts (b) and (c) were delivered in W507 under the Owner's ruling: a row written from an augmented prompt is now MARKED at all four gateway writers, and the recall block states its provenance limit where a reader meets it. Part (a) remains and is a MEASUREMENT, not a build: nobody has established what the W489 defect actually did while it was live. THE FACTS: W489 found query/stream/stream_meta inheriting augment=True, so 29 generation-class callers - including the nine-stage synthesis cascade, the CEO blueprint and the digital-twin modeller - had another request's content prepended and presented as analysis of their own subject. THE WORK: sample the persisted outputs of those 29 surfaces for text that plainly came from another request (the native floor's tell is a Domain: or Problem: label whose value belongs to a different subject) and COUNT how many are affected, so the disclosure the Owner chose can eventually name a population instead of the whole pool. WHY IT MATTERS: W507's disclosure is currently over-broad by necessity - a stored row carries no timestamp, so recall must warn about EVERY pre-W507 line rather than the affected ones. A count would let the warning narrow to what is true, and a warning that covers everything is one a reader learns to ignore. (found W507 (FU-256, the part the ruling did not cover))
    FU-164 [medium] [p 22.4] sweep products.py: 2 Tier-2 shortfalls (C7,C10) — 'AI Production Lines · Real Artefact Generation'; green 'done'; an exported… — S8.11 C7: 'AI Production Lines · Real Artefact Generation'; green 'done'; an exported '<name>-<run>.md' titled with… → The done event's served_by:'native' is dropped, so there is no provenance chip, and the export's header carries no provenance.…; S13.9 C10: '2 active projects across 2 realm(s)', '1 concept-stage project(s) ready to run', '1 prototype(s) eligible… → 'active' counts every project regardless of status (live: statuses 'idle' and 'done'). 'ready to run' counts concept-stage… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-187 [medium] [p 19.1] sweep sovereign_evolution.py: 1 Tier-2 shortfall (C9) — Ticking the box and running a cycle suggests the items go to governance. Nothing is… — S13.5 C9: Ticking the box and running a cycle suggests the items go to governance. Nothing is shown when nothing was… → On the floor the only directive is the defaulted P2 'maintenance' item, so the submission filter (P1 or correction) selects… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-248 [low] [p 10.5] Four more export surfaces send text out with no provenance line — W485 fixed the two surfaces the sweep named (My Work, DomainTool) and left the class open elsewhere: Generator.tsx exports result.output raw, CreatorStudio.tsx, ApplicationStudio.tsx and DigitalReactor.tsx each build a Blob from their own text. Several already hold the provenance they would need. FIX: prepend provenanceLine() at each, the same call the two fixed surfaces use, so no export leaves unlabelled. (found W485 refuters (verified real) — found while applying the rule, not delivered)
    FU-276 [medium] [p 9.6] 52 of 61 gateway call sites still thread no account id, so their output is unattributed and recallable by nobody - including its own author — W496 closed the LEAK at the mechanism: a completion written with no account id lands in an UNATTRIBUTED namespace that recall never reads, for any account (driven: tenant-a, tenant-b and an anonymous caller all recall nothing from it, while a deliberate platform note stays recallable and each tenant still recalls its own). That removes the cross-tenant exposure whatever a call site does, which is why it was the right fix rather than editing 52 sites. What remains is the ENHANCEMENT: measured on 2026-09-27, 52 of 61 gateway call sites across 28 files pass no owner_id, so the work those users ask for is stored unattributed and cannot be recalled even BY THEM - the AI CEO chat and the avatar therefore recall far less than the user typed. Nine of the 28 files already have a user in scope (vsb.py 4 calls, synthesis_studio.py 3, change_control.py 3, qep_intelligence.py 2, genesis.py 2, capital_fund.py 2, integration_surface.py 1, projects/api.py 1, organism/reconfiguration.py 1), so threading is plumbing there; the rest (products.py 8, digital_twin.py 3, swarm.py 2, genome.py 1, ...) are platform-internal calls with no user, where unattributed is the correct namespace and nothing needs changing. FIX: thread owner_id through the nine user-facing files and assert per file that a user's own call is recallable BY THAT USER and by nobody else. (found W496 (FU-258, the mechanism fix))
    FU-261 [low] [p 8.4] packages/ui tsconfig cannot be typechecked on its own — npx tsc --noEmit in packages/ui exits with TS5103 Invalid value for --ignoreDeprecations (tsconfig.json line 9), so that package is only ever typechecked transitively through the superapp build. A shared package that cannot be checked alone will drift. Pre-existing, noticed while verifying the W491 CommandCenter edits. (found W491)
    FU-262 [medium] [p 8.2] Extend the pre-flight self-check to the claims group, and wire it into the round rhythm — scripts/selfcheck_diff.py (added W493) mechanically checks the four defect shapes that are deterministic: a key no consumer reads, a key removed while readers survive, a route decorator bound to a private helper, and sibling returns with different key sets, plus two guard shapes (an assertion matching its own text, a comment quoting a forbidden literal). Validated against ground truth: four known W492 defects re-introduced in an isolated worktree, 4 of 4 caught. NOT yet covered: the largest group in the labelled set, 30 of 98 'a new claim the code cannot back' (a basis string that asserts rather than reports). Also wire the script into the per-round sequence in docs/FABLE_DELIVERY_PROMPT.md so it runs before the refuter fleet, not beside it. (found W493)
    FU-298 [medium] [p 7.5] Thirteen tolerant readers still LOG rather than surface their store's incompleteness — W506 delivered FU-075's substance: load_json_tolerant now delegates to the new read_json_reported and LOGS the store, the calling site and exactly what is missing, so a corrupt store is attributable everywhere instead of silent. FOUR readers were fully converted and carry the reason in their own answers - revenue's pending_summary (store_incomplete + counts_are_incomplete), charity's approved signals, the heartbeat's screening rotation, and the avatar's compliance line, which now says a screen is UNKNOWN rather than omitting it. THIRTEEN callers remain on the logging path: ai/native/model_resource.py, api/agent_hub.py, api/board.py (x2), api/capital_fund.py, api/integration_surface.py, api/operational_excellence.py, api/resource_fabric.py, api/swarm.py (x2), api/user_workspace.py, vbs/dcms.py, vbs/qms.py. THE WORK: give each caller the reason in its own response, as the four converted ones do - a log line is a weaker remedy than a field on the answer, because the person reading the number never sees the log. THEN delete load_json_tolerant, which is what the original row asked for and which cannot honestly be done while thirteen callers use it. WHY IT WAS NOT DONE IN ONE PASS: each of the thirteen is a different caller shape, and a careless conversion turns a working list endpoint into a 500 or drops a field a page reads; rewriting thirteen heterogeneous sites in one unattended batch is how a round ships a regression it cannot attribute. (found W506 (FU-075, the part not done))
    FU-077 [medium] [p 6.8] The ontology engine serves empty graphs and the one real ontology (Law, under knowledge/) is unwired — agentic_core/reactor/domains/ontology_engine.py reads agentic_core/data/ontologies/ which holds nothing, reached from the domain weaver (a v138 CEO tool) — every domain query answers an empty graph; knowledge/Law/EmploymentTribunal/ontology/*.json is never loaded. Wire the Law graph or retire the engine (audit-before-wire). (found W473 refuter)
    FU-076 [medium] [p 6.2] pqc_hardening.py stamps a SHA3 digest with a fixed built-in key as a 'Dilithium5 signature' — relabel or retire — agentic_core/security/pqc_hardening.py is not a post-quantum scheme; gaas.py and qep_flagship.py record its output as pqc_signature, which reads as cryptographic assurance the code does not give. Retire the field or name it a content hash. (found W473 refuter)
    FU-071 [low] [p 5.2] Nine source-pointer product directories are still listed as products of a kind — The catalogue now marks them status source ('a pointer, nothing served yet') and no consumer builds from them, but products/ still holds nine metadata.json directories (business_incubator, cognitive_scraper, gse, molecular_sdk, nanophotonic_navigation, scraping_suite, uviap, mjm-intelligence-engine, signature-product-suite) whose only substance is a pointer at SDK source. Fix: for each, either serve it (a route and a real page) or retire the directory; the scatter item decides which, per the reach audit. (found W470)
    FU-072 [low] [p 5.2] The six legacy signature-product directories still sit in products/ with self-declaring manifests — products/Care … products/Science each carry a manifest.json self-declaring PRODUCTION_READY, WCAG 2.2 AAA and nine injection formats that nothing serves; W470 lists them as legacy archives and routes nothing to them, but the directories remain where a reader takes them for products. Fix: move them to _archive/products/ (LEGACY_ARCHIVES then empties) and keep one line in the catalogue saying they were archived. (found W470)
    FU-220 [medium] [p 4.5] relocate_data_store calls a directory populated because a file exists — FU-079's two 'populated' chroma_db copies held 0 and 1 entries — FU-079 was registered as 'two populated copies' of chroma_db because plan() marks a directory CONFLICT when it is non-empty (any file). Read W477: the legacy copy's conversation_memory collection holds 0 embeddings; the repo copy holds 1 (a 30 March test exchange). The Owner ruled 2026-09-19: the repo copy is live, the legacy copy is retired and left on disk untouched. Fix: a directory is populated only when it holds data (for a Chroma store, count the embeddings; for a SQLite file, rows in its tables), and the report states the counts; guard with an empty-store fixture. (found W477 (FU-079 ruling))
    FU-075 [low] [p 3.8] Read-only readers still use load_json_tolerant; retire the tolerant loader once every writer is strict — W472 made every WRITER read strictly (config.read_json_strict). The read-only readers that summarise or list — revenue._load (pending_summary), ueg._read (recent), agent_hub listing reads, integration_surface listings, resource_fabric composition/swarm listings, swarm proposed_catalogue/org_cascade_runs listings, business_plan._load — still use load_json_tolerant or a bare json.loads with a fallback: honest as readers (they never write back) but a listing over an unreadable store shows fewer rows without saying so. Fix: give each listing an 'unavailable' answer via read_json_strict and delete load_json_tolerant when no caller remains. (found W472)
    FU-228 [low] [p 1.8] intelligence.py keeps the unused cascade and MJM singletons W479 stopped calling — W479 removed the stub cascade call from the BDP/SPI stream; agentic_core/api/intelligence.py still imports UltimateCognitiveCascade and MJMOrchestratorV4 and instantiates _cascade and _mjm at import, which now nothing uses. FIX: remove them with the P3.12 engine work (they are the same objects that item rebuilds). (found W480 review of the 12-engine cognitive architecture proposal)
  P2.8 — Bespoke swarms
    FU-186 [medium] [p 21.0] sweep resource_fabric.py: 1 Tier-2 shortfall (C9) — Each real facility run a composition executed is recorded as a successful outcome… — S4.19 C9: Each real facility run a composition executed is recorded as a successful outcome ('measured facility… → record_outcome(..., success=True) runs for every entry in real_runs, including entries that are {'resource', 'error'}. A failed… [docs/TRUTH_SWEEP_W477.md; every writer is named there] (found W477 truth sweep)
    FU-232 [medium] [p 16.0] The transformation cascade has no DELIVERY check, so a run can never be validated and the plan write-back is unreachable — W481 made the verdict honest: 'validated' requires a stage whose check measures a delivered outcome, and no stage has one (stages 1-4 presence, 5-6 nothing, 7 a governance decision, 8 an artifact write, 9 provenance). Every run returns validated=null and the §5 loop closure that moves a living-plan objective planned->in_progress never fires in production (both ways are covered by tests through the summarise_validation seam). FIX: give the cascade one real delivery check — a Build-to-Order order created, or a plan objective's measured progress moving — declared checks='delivery'. Until then the honest state is 'not assessable'. (found W481 refuters (verified real))
    FU-010 [low] [p 13.5] Saved cascades cannot be deleted from the designer page — DELETE /api/v1/resources/swarm/{sid} exists but the /native-ai designer offers no way to call it (found W460 audit (P1.12))
    FU-265 [medium] [p 11.5] Four pre-existing second readers of the metabolic (ATP) term still present it as live capacity or decide on it — W494's refutation found these while sweeping the ATP term; they are OUTSIDE the fourteen rows that round closed and form one coherent follow-on batch. (a) agentic_core/app_mvp.py:438 serves /api/v1/biometrics/status with the raw simulator ratio and NO /15 normalisation, so the figure is a constant 1.0 and the Introspection surface prints 'Metabolic (ATP 100%)' as a live vital that cannot come out otherwise; it also floors the Metabolic efficiency bar at 50%. (b) agentic_core/api/integration_surface.py:469 builds a FRESH ATPSimulator per request, so metabolic_atp_ratio is the constant 0.333, published under a label saying it is real and contrasted in the same payload with values marked simulated; metabolism.py documents that callers must read the SHARED singleton via biobus._get_atp(). (c) agentic_core/economy/metabolism.py:158 DECIDES the reserve rate on the term (atp < 0.3) and records an energy_state that can only read healthy, in the economy that writes the virtual ledger - every VSB cycle therefore records a reserve decided on a simulator. (d) apps/workstation-superapp/src/pages/developers/NativeAI.tsx:618 and the ResourceFabric tooltip print ATP as live capacity with no disclosure, and NativeAI's body copy asserts it governs parallelism. W494 added metabolic.measured=False, can_fall=False and a basis to the organism context and clamped the load to its declared 0-1 domain, so the qualifier now exists for these readers to carry. FIX: normalise (a) and carry measured/basis onto the Introspection label; have (b) read the shared singleton or drop the term; give (c) a three-state energy_state that says the reserve was NOT adjusted because the term is unmeasured; forward metabolic.basis to (d). Note for whoever takes it: driving ATP from a real load signal that can fall is a CAPABILITY change, not a truth fix - the truthful move until then is to say the levers are inert. (found W494 refutation (atp-thresholds lens), deferred as outside the round's fourteen rows)
    FU-008 [medium] [p 10.5] swarm_cascades.json writers are not under store_lock — define, update and delete load-modify-save the store with no lock — a threaded probe during the P1.12 audit lost 38 of 40 concurrent writes (found W460 audit (P1.12))
    FU-009 [low] [p 5.2] The swarm HTTP contract drops per-stage model; runs have no run_id or UEG record — SwarmStageSpec carries role and instruction only, so a stage's model choice is silently discarded; run_swarm records the outcome under stage 1's served_by alone and writes no run id or ledger entry (found W460 audit (P1.12))
  P2.10 — THE DELIVERY METHOD, HELD BY THE ARMS-LENGTH AGENCY
    FU-295 [medium] [p 21.0] Author the new short constitution the Owner ruled for: 20-40 checkable articles from what actually governs — The decision half of FU-266 is RULED (Owner, 2026-09-28) and this is the build half. Nothing archived is restored: measured across the repo, 41 CONSTITUTION documents exist (v52-v139), the one LIVE file (meta/CONSTITUTION_v99.0_LEGACY.md) declares 297 articles and contains 33, and across the 32 parseable documents 9,547 articles are declared while 778 are present - 92% asserted by a section header and never written. The 'canonical' v130 states 'Articles 1-695 retained from v126.0 as immutable genomic anchors' and contains none of them. What IS written mandates capabilities that do not exist and mostly should not (signed MoUs, global marketplace listings, ORCID onboarding with Oxytocin/Serotonin reputation scores, >=50,000 WST monthly revenue, cryptographic Verifiable Credentials), and two articles are self-certifying completion claims (Art. 60 NO-STUBS MANDATE, Art. 736 '100% completion ... No stubs or placeholders are permitted') - a document cannot make code complete by forbidding incompleteness. THE WORK: author a NEW short constitution, order of magnitude 20-40 articles, each CHECKABLE against this platform, drawn from what genuinely governs it - the ratified Owner rulings, A.9.5, the virtual-WST-only boundary with real-money rails owner-gated, the ten architecture invariants, the never-fabricate principle. Each article names how it is verified, and a guard drives the mechanically checkable ones. The /api/v154/constitution/articles endpoint then parses THAT document and keeps its canon_present honesty for the absent case. Do NOT import article numbering from any archived version. Also unresolved: products/OctoVeritasEngine/constitution refused read with a permission error. (found W505 (the Owner's constitution ruling))
  P2.13 — HORIZON - THE ASSET GENOME OVER THE LOCAL ARCHIVES
    FU-296 [medium] [p 7.5] Install pypdf and python-docx, the dependency the Owner ruled for (FU-269) — OWNER RULING 2026-09-28 on FU-269: option (a) - pypdf and python-docx are added to requirements. `_pdf_docx_extractor()` already probes for both, so extraction begins working with no further code; this row exists because the RULING is recorded and the INSTALL is not done, and a closed decision row carries no work. MEASURED (W495, FU-124): all 14 files of the book folder and 4 of the 9 p3 files are .docx/.pdf, so the platform currently reads none of them and answers NOT_EXTRACTED with its reason. THE WORK: add both to requirements, confirm the probe finds them, and prove extraction on one .docx and one .pdf - then P2.13 can make a coverage claim over the Owner's explicit inbox (FU-268's ruling) instead of listing those documents as unread. Until the install lands, NOT_EXTRACTED stays the honest answer and must not be replaced by an optimistic one. (found W505 (the Owner's ruling of 2026-09-28 creates work the closed decision row cannot carry))
  P2.17 — THE ROUND'S OWN COST
    FU-252 [medium] [p 9.0] A round runs the full suite twice when once would do — the pre-refutation run is wasted whenever the refutation finds anything — W488 measured a round's wall clock: the full suite is 41 min on an idle machine (258 tests in 26.0 min = 9.9/min), 91.5 min when overlapped with the refutation's 34 agents; the blind sweep is 22.5 min (37.5s per blind, mostly app boot); the refutation workflow is 84.7 min. B2 permits the suite 'twice at most per round' and W488 used both: once before the refutation and once on its fixes. The first run is dead weight whenever the refutation finds real work — W488's found 25 verified findings, so every line of that 41 min was spent on a tree that was about to change. FIX: run the AFFECTED SLICE (-k) during iteration and the full suite ONCE, on the tree that follows the refutation fixes. Keep the second run only when the refutation returns nothing. Worth 41 min per round at no cost and no new machinery; amend B2 in the delivery prompt when done. (found W488 measurement of where a round's wall clock goes)
    FU-253 [medium] [p 9.0] The blind sweep is serial only because blinds mutate one tree — one worktree per blind would cut it from 22.5 min to about 7 — W488 measured 36 blinds in 22.5 min (37.5s each), and most of each blind is app boot, not the assertion. Blinds cannot run in parallel IN ONE TREE because each mutates the repo and byte-restores it; they can run one-per-git-worktree, which is the pattern the refutation workflow already uses safely here (isolation: 'worktree', its own DATA_DIR per worker). FIX: extend the mk_break harness so the blind list is sharded across N worktrees (N = cpu_count - 2, measured 8 CPUs so 6), each with DATA_DIR/WORKSTATION_DATA_DIR/WORKSTATION_UEG_PATH/PROJECTS_DIR of its own, results merged, and the SAME preflight (every anchor matches exactly once) run in each shard before any mutation. Keep the contamination check: the harness must still verify the WATCHed docs are byte-identical after every blind. Expect 3-4x not 6x (8 CPUs, pytest is CPU-bound) — about 15 min per round. Verify by running the same blind set serially and sharded and comparing the caught/vacuous sets exactly, the same discipline FU-249 requires of xdist. (found W488 measurement of where a round's wall clock goes)
    FU-259 [medium] [p 9.0] A refutation round can exhaust the disk and lose most of its agents silently — 27 of 45 died creating worktrees, and the run still reported a result — W490's refutation raised 40 findings and verified only 13: the other 27 agents failed with 'No space left on device' while creating their git worktrees, and the workflow still returned a normal-looking {confirmed: [...]} result. Free space had fallen to about 9 MB. The cause is accumulated worktrees: 56 existed, one per refuter agent across every round since W479, each a full checkout of this repo, and nothing removed them when a round finished. Removing all 55 secondary worktrees recovered 9.6 GB. Two things to fix, neither of them large: (a) the round rhythm must CHECK free space before launching a refutation and REMOVE the round's worktrees after it (git worktree list --porcelain | git worktree remove --force), so the cost does not accumulate; (b) a refutation whose agents died must not read as a completed refutation — the count of agents that errored is in the tool result and should be checked against the count launched before any finding list is trusted. Until (b) exists, read the agent error count by hand every time. Worth considering: the verify agents are read-only (they read code and run pytest against an isolated DATA_DIR) and may not need a worktree at all, which would cut the disk cost by roughly the number of findings. (found W490 refutation (the run itself failed part-way))
    FU-301 [medium] [p 9.0] The parallel suite stalls about one run in three, with every worker in flight at once - cause not established — W507 delivered the per-worker store isolation FU-249 asked for and MEASURED the win: 50m42s serial to 10m35s on six workers (4.8x), with the pass sets matching exactly (466 passed, 15 skipped, 0 failed both ways). It is NOT the round default because of this row. MEASURED FAILURE MODE: of six parallel runs, three completed and three STALLED - at 74%, 89% and 57% - and in the stalled runs EVERY worker was in flight simultaneously (a -v run showed six tests started with no verdict, one per worker) with the controller and one worker process still alive and no CPU. So it is a simultaneous stall of all workers, not one slow test. WHAT WAS RULED OUT: (a) store_lock itself - it is a per-path threading.RLock plus an O_CREAT|O_EXCL lockfile with a bounded 10s timeout that RAISES TimeoutError and breaks a stale file after 30s, so it cannot deadlock indefinitely; (b) the shared repo register - a stray docs/FOLLOWUPS.json.lock was found and removed, and deselecting all 19 tests that spawn a subprocess or write a repo file did NOT change the stall rate (1 of 3 still stalled), so that lock is a real contention point but not this cause; (c) my own new guards - the stalls predate them (the first two parallel runs stalled before any W507 guard existed); (d) order dependence - --dist load scatter was green on the runs that completed, so no order-dependent test beyond the one W498 fixed. STILL UNEXPLAINED: what all workers block on at once. WHERE TO LOOK NEXT: get a stack from a stalled worker (faulthandler in the controller does not reach xdist subprocesses - try PYTHONFAULTHANDLER with a per-worker dump, or py-spy against a live worker pid); check for Windows handle or process exhaustion, since six workers each build the full app (about 18s and 54MB each) and several tests spawn further subprocesses; and check whether the module-scoped client fixture's app construction can block when six copies start together. UNTIL THEN: the serial run is what a commit is trusted to, and -n 6 is for a fast read only. A tool that fails silently a third of the time is the instrument-that-cannot-fail defect inverted. (found W507 measurement of FU-249's delivery)
    FU-255 [medium] [p 8.2] Batches are scoped to the gate item, which throws away two thirds of each round's reach — the same mechanism closes three times as many rows swept repo-wide — The batch mechanism (W487) is being called as 'batches --item P1.18', and that scoping costs rows for nothing. The generated figures for the SAME class, the SAME mechanism and the SAME files: C3 (invented or constant readings) closes 4 rows inside P1.18, and 12 rows across all items (47 files, advancing 5 more, spanning P1.18, P2.4, P2.8 and P2.9). A class is one rule swept across every file that consumes it; stopping the sweep at the gate item's file list leaves the other consumers emitting the defect the round just proved wrong, and guarantees a later round re-reads the same mechanism. FIX: take the class repo-wide by default and report the closure per item, so the gate's rows still close on schedule while the rest close for free; keep the item filter for the case where a class genuinely spans two unrelated mechanisms. Measured effect on the whole backlog: 173 open rows at 4.0/round is about 44 rounds; at C3's cross-item spread roughly half that. State the optimistic end honestly — C3 is the LARGEST batch; C7 and C1 are smaller. (Re-registered from FU-254, which was marked high for emphasis and routed onto the P1.18 truth gate where a planning-efficiency row does not belong.) (found W488 forecast/batches reading while reporting the timeline)
  P3.12 — The engine contract, then the six
    FU-223 [medium] [p 13.5] /api/v1/cognitive/* returns a constant payload and reports engines_run 9, status complete — ledger v4 R4.3 (tier 2, API_ONLY, refutation SURVIVED): POST /api/v1/cognitive/cascade with two different problems returns identical output bar the echoed problem and elapsed_seconds; engines_run is the literal 6 or 9 and status the literal 'complete'. No frontend calls it, so it is API-only, but it is a public route of this platform. FIX: report what ran, or return 501 until the engines measure. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-229 [medium] [p 8.4] The six cognitive engines return constants for any input — inkashaf_engine.py returns {'status':'SUCCESS','insight':'revealed'}, aqal {'status':'SUCCESS','plan':'computed'}, samajh 'grasped', soch ['A','B'], hoshiyari threat_score 0.01, iman alignment 0.99 — none reads its input (only cycle metrics can deflect them). cascade_v16 chains all six and reports status 'fully_integrated'. FU-146 covers the VSB spawn surface that SHOWS these; this row is the engines themselves. FIX: each engine measures its input or returns assessable:false with the reason. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-257 [medium] [p 6.2] The six cognitive engines still return fixed markers — W489 made the surfaces honest about it, the engines themselves are P3.12's work — W489 corrected every surface that claimed nine engines or presented their literals as analysis: the cascade now reports six, says they do not compute, and marks the three meta engines as PLANNED under P3.13. That closes the TRUTH row (FU-146). It does not make the engines work: inkashaf still returns {'status':'SUCCESS','insight':'revealed'}, aqal 'computed', iman alignment 0.99, and MJM re-runs the same six and returns 'optimised' with compliance 1.0 — all persisted into the VSB entity and its genome on every spawn. FU-229 (P3.12) already carries the engines themselves; this row records what W489 learned that the P3.12 work must also handle: the spawn path PERSISTS cascade_analysis and mjm_result into the entity and the genome, so making the engines real means deciding what happens to the entities already carrying the markers, and the spawn feed's new engines_run/ran/basis fields are the contract P3.12 must keep populating truthfully. (found W489 (the C3 batch — found while making the surfaces honest))
    FU-274 [medium] [p 3.4] The archived nine-engine bootstrap must NOT be recovered as-is: two of its three meta engines return fabricated ratifications and its base class hard-codes confidence 0.95 — The roadmap's Phase 1 says to un-archive cognitive/bootstrap.py and register the nine engines. Measured on 2026-09-27: bootstrap.py exists only at _archive/jules-unwired/agentic_core/cognitive/bootstrap.py and imports the nine from foundational/ and meta/, which in the live tree are EMPTY package shells (__init__.py only) - six engines live at the top level of cognitive/ and the three meta engines do not exist in the live tree at all, though the registry's EngineType enum declares them. The archived meta engines are 7-line stubs returning literals: niyyah_engine returns {'ratified': True, 'signatures': ['council_node_1','council_node_2','council_node_owner'], 'intent_status': 'COMMITTED'} - a fabricated governance record with three invented signatories - and the archived base_engine.py hard-codes confidence=0.95 on every successful output, which is the shape FU-224 and FU-233 already record. FIX (the three engines themselves ride the meta-engine item; this row rides the engine-contract item because that is where cognitive/ routes): write the three engines so each reads its input or returns assessable:false with a reason; recover the CALL CONTRACT from the archive (one signature the engines implement, per FU-221) and nothing else; and never register an engine that cannot compute. Recovering the file without reading it would import a fabricated ratification into the clearance chain P3.14 is meant to make refusable. (found W495 (the Owner's native-AI-fabric roadmap, interrogated))
    FU-275 [medium] [p 3.4] The cognitive engines have no path to a model at all - not a stub call, no import: measured 0 of 6 — Recorded as the measurement behind P3.12, because it is stronger than 'they return constants': a grep for gateway|orchestrator|complete( across all six engine modules returns ZERO for every one of them. There is no disabled call, no try/except around a model, no injection point - the engines were never wired to anything, so making them compute is new wiring rather than repair. The roadmap is right that this is the first job, and its own deliverable is the right shape: one engine reasoning about a real input through a local model, with the result traceable to the call that produced it. Two constraints this repo already knows: on THIS hardware the runnable local tier is llama3.2:1b / 3B (see FU-271), so the not-assessable path will be the common path and must be first-class, not a fallback literal; and the engine must carry what served it, because a reasoning step with no provenance cannot be told from the floor composing headings. (found W495 (the Owner's native-AI-fabric roadmap, interrogated))
    FU-224 [medium] [p 2.7] The consultation contract excludes the three meta engines and forces a numeric confidence — ConsultationRequest.engine is a Literal of seven names (six lenses + mjm), so niyyah, tawazun and tafakkur cannot be requested through the contract the registry declares; ConsultationResponse.confidence is a required float 0..1, which is why every implementer returns a literal (0.96, 0.88). FIX: an explicit assessable state and a provenance block, and the nine names the registry declares. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-221 [medium] [p 2.5] The cognitive engine registry is never populated, and its call contract does not match the engines — CognitiveEngineRegistry._engines starts empty and nothing calls register(), so registry.get(...) raises ValueError on the first call; EngineRegistry9.get_engine_response then calls engine.process(input, context, enforcement) and reads result.payload, while the engines expose unveil_patterns / comprehend / reason / detect_anomalies / reflect / validate_values returning plain dicts. This is why agentic_core/avatars/api.py deliberately bypasses the recirculation orchestrator (its own docstring says the registry 'was never actually populated with working engines'). FIX: one binding, one call signature the engines implement. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.14 — The clearance chain that can refuse
    FU-230 [medium] [p 3.0] The five-gate clearance chain cannot refuse, and writes literal strings as signatures — clearance_chain.py: tawazun_res.get('balanced', True), tahqeeq_res.get('verified', True), a missing risk_score reading as 0 — an engine returning {} clears all five gates; the attestations recorded to the UEG are the literals 'SIG_MUSHAWARA_v1', 'SIG_NIYYAH_v1', 'SIG_TAWAZUN_v1', 'SIG_TAFAKKUR_v1'. Dormant today (only the bypassed recirculation orchestrator calls it), so this must be fixed BEFORE anything is wired to it. FIX: every default blocks; each verdict records its basis. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.15 — Attestations that are attestations
    FU-226 [medium] [p 6.2] Post-quantum signatures are named in five modules and never performed — Dilithium/Kyber appear as strings and descriptions in autonomy_pipelines.py, integration_surface.py, avatar_engine.py, interstellar.py and qep_flagship.py; no attestation path performs a post-quantum signature. FIX: sign a canonical payload with a named algorithm and a stated key source, verify it from a route, and use the words 'post-quantum' only when it is. (found W480 review of the 12-engine cognitive architecture proposal)
    FU-246 [low] [p 2.7] Three outside proposals now require a Halo2 attestation and an OAM-QKD figure this repo cannot produce — The biogeochemical, SWF and communication specifications each require require_halo2_proof=True on every ledger write, and the communication one adds a 'Classical OAM-QKD surrogate' with QBER <5 percent and a key rate >5.5 bits/photon. W482 established that a Halo2 proof here is a SHA string named after one, and FU-226 records the same for Dilithium/Kyber. Registered so P3.15 carries the WORDS as well as the mechanism: a surrogate is never named as the thing it stands in for, and no ledger write claims a proof it did not compute. (found W484 interrogation of the biogeochemical / SWF / comms proposals (archive-first audit))
  P3.16 — The auxiliary engines and the recirculation loop
    FU-227 [low] [p 2.1] The recirculation orchestrator states stage latency targets it never measures — recirculation_orchestrator.py documents 'Target p95 latency: <500ms (SENSE -> ACT)' and per-stage budgets (<100ms sense, <500ms analyse) and measures none of them. It is not on a live path (the avatar API bypasses it and says why), so this is a dormant claim. FIX: measure each stage, record the latencies with the run, and make a breach a recorded fact before the loop is wired to the heartbeat. (found W480 review of the 12-engine cognitive architecture proposal)
  P3.17 — The Biomimetic Minimisation Engine,
    FU-233 [medium] [p 2.7] The VRPR pipeline invents its confidence and renames strings 'Certified' — agentic_core/quality/vrpr_pipeline.py: process() starts at a hard-coded conf = 0.90 and adds 0.05 per iteration, never reading the content; it exits successfully when enforcement.validate() passes (it always does — see the enforcement row) and conf >= 0.95; _polish replaces 'Action result' with 'Certified Sovereign Action Outcome'; a pass returns constitutional_articles=[18,19,20] as a literal. Used by the dormant recirculation orchestrator and mode_controller. Anything gated on 'VRPR confidence >= 0.95' is gated on a manufactured number. FIX: compute the confidence from the content or return assessable:false; the articles come from what was checked. (found W482 interrogation of the BME and support proposals (recovery audit))
    FU-235 [medium] [p 2.5] The constitutional enforcement engine has no validators, so validate() always passes — OmniEnforcementPatternSupreme names twenty-one validators across five phases, but UniversalEnforcementPattern.validators starts empty and register_validator is never called anywhere in the repository. All three constructors (clearance_chain, recirculation_orchestrator, mushawara_bridge_2) pass fail_on_missing_validator: False, so every phase is skipped and validate() returns passed. This is the engine two outside proposals wanted to use as the compliance backbone. FIX: register the validators, or report which phases could not run and refuse rather than pass. (found W482 interrogation of the BME and support proposals (recovery audit))
    FU-236 [low] [p 1.9] The optimal-transport router cannot solve: POT is not installed, and its adapter is on no route — agentic_core/biomimicry/minimisation/core/optimal_transport.py imports POT ('import ot') behind a try/except; POT is not installed and is not in requirements.txt, so OptimalTransportRouter silently has no solver. Its only consumer, EntropyRegularisedGaaS, is imported by governance/gaas/__init__ and mounted on no route (its own comment says so). FIX with P3.17: add POT or implement Sinkhorn over numpy, and have the router report itself unavailable instead of degrading silently. (found W482 interrogation of the BME and support proposals (recovery audit))
    FU-234 [medium] [p 1.8] The thermodynamic ledger is fed invented bit counts, so its joules are invented — core/transcendent_subsystems/tfel.py computes E = k_B x T x ln2 x bits correctly, but every caller passes a constant: tool_registry meters bits=2e5 per effector call ('standard bit cost'), recirculation_orchestrator meters bits=1e4 for its sense stage, causal_simulator uses len(task_batch)*1.5e6. export_cycle_ledger also returns 'compliance': True as a literal. All callers are dormant today. FIX: the bit count comes from an instrumented operation, or the figure is named a proxy (estimated_bits_from_payload_size) and is not reported as energy. (found W482 interrogation of the BME and support proposals (recovery audit))
    FU-237 [low] [p 0.9] 524 orphan .pyc files sit beside sources that were archived or deleted — scripts/recovery_audit.py (W482) finds 524 compiled files under agentic_core/ and core/ whose source is gone: 516 of those sources were MOVED into _archive/ by the W78/W159/W382 sweeps and 3 were deleted outright. The stale artefacts make a package look populated (minimisation/core still shows omega_functional, schrodinger_bridge and diffusion_engine) and can be imported by a stale interpreter. FIX: remove the orphans once P3.17 has recovered what it needs, and keep the audit green. (found W482 interrogation of the BME and support proposals (recovery audit))
  P3.18 — Autonomous technical support, told truthfully
    FU-238 [medium] [p 2.1] The archived support agent is a simulation under a test whose assertions cannot fail — _archive/agentic_core/support/autonomous_support_agent.py sleeps a tier-shaped latency, returns 'Simulated resolution for query: {query}' with confidence 0.96 and success=True unconditionally; _archive/tests-jules/integration/support/test_autonomous_support_sla.py then asserts resolution_rate >= 0.95 and zero_human_intervention is True. Nothing live imports either. Recorded so that P3.18 recovers the SHAPE and not the simulation, and so no future round inherits those assertions or the '96.7% autonomous resolution' figure they appear to support. (found W482 interrogation of the BME and support proposals (recovery audit))
  P3.19 — The six cycles as a control surface
    FU-242 [medium] [p 2.1] The geospheric regulators are unwired, so no cycle setpoint is enforced anywhere — agentic_core/biomimicry/geospheric/ holds five real modules (regulator.py, homeostatic_regulator.py, balance_regulator.py, drad.py, resilience.py) including a genuine PID regulator, and no live route or heartbeat beat calls any of them (resilience.py is already registered dead as FU-078). Three outside proposals now assume these are the running control layer for six biogeochemical cycles with +/-5 percent tolerance. They are not running at all. FIX with P3.19: bind the regulators to figures the platform already measures (reserve fund, self-investment returns, heartbeat work, the section 4 waterfall, immune records) and have an unbound cycle report assessable:false rather than a setpoint nobody enforces. (found W484 interrogation of the biogeochemical / SWF / comms proposals (archive-first audit))
    FU-243 [low] [p 2.1] Six biomimetic layer modules sit in the archive while the live tree keeps their .pyc — _archive/jules-unwired/agentic_core/biomimicry/ holds ant_colony.py (96 lines: a real stigmergic scheduler with a pheromone table, a decay rate and NATS behind a declared mock), communication.py, homeostasis.py, economy.py, immune.py, federation.py and emergence.py. The live agentic_core/biomimicry/ keeps an orphan .pyc for each (part of the 524 in FU-237), which makes the package look populated. The inter-agent communication proposal asks for exactly this layer as new work. FIX with P3.19: read each, recover what computes, delete the orphan .pyc for what does not, and record which was which. (found W484 interrogation of the biogeochemical / SWF / comms proposals (archive-first audit))
  P3.20 — THE TIER REGISTRY AND THE ROUTER (native AI fabric roadmap)
    FU-271 [high] [p 3.6] OWNER DECISION: the hardware ceiling - the roadmap's model stack cannot run on this machine — Measured on 2026-09-27: this machine has 7.7 GB of RAM total, an Intel i3-1315U (6 cores) and integrated Intel UHD graphics with no CUDA device (nvidia-smi is not installed and no discrete GPU is present). The roadmap's tiers assume otherwise: DeepSeek-R1-Distill-Qwen-14B and StarCoder2-15B need roughly 9-12 GB at 4-bit, which is more than the machine's ENTIRE memory, so they cannot load; Llama-3-8B at Q4 is ~4.7 GB, nominally loadable but sharing 7.7 GB with Windows, the browser, the dev server, the backend and the suite, and minutes-per-reply on a CPU-only i3; Qwen-VL vision is out; and 'hot-swap the adapter to save VRAM' has no VRAM to save - Ollama runs on the CPU here. What IS runnable today is llama3.2:1b and llama3.2 (3B), both already pulled, plus the deterministic floor. THE DECISION: (a) design the fabric for a 1-3B local tier plus the floor, and have every higher tier report 'not runnable here' with the measured reason (this is what P3.20 builds by default); (b) provision hardware (a discrete GPU with 12-24 GB, or a rented instance) and state which tiers it unlocks; or (c) route specific high-value tasks to an Owner-gated external accelerant, which the platform supports and keeps off by default. Blocks the inventory half of P3.20. Default if undecided: (a). (found W495 (the Owner's native-AI-fabric roadmap, interrogated))
  P3.23 — FABRIC - THE DOMAIN SPECIALISTS AS EXECUTORS, WITH THEIR GATES
    FU-272 [high] [p 3.6] OWNER DECISION: may the platform index the live legal matter's documents, and on what terms — The roadmap's Litigation Strategist reads the Owner's disclosure bundles, extracts a timeline, maps events to ACAS Code breaches and drafts witness statements for a LIVE employment matter. The document work is buildable and genuinely useful - assembling, citing and cross-checking with provenance per line. The terms are the Owner's to set, because this is sensitive personal data about real people in a live dispute. THE DECISION: (a) read-only, LOCAL-ONLY indexing of a named folder, never sent to any external service (the egress alarm in P3.21/P3.23 covers this), with provenance per document, a human-approval gate on every filing-shaped artefact, and the index kept in data/ and never committed; (b) a narrower scope (e.g. only documents the Owner copies into an explicit inbox); or (c) none, and the platform stays out of the case entirely. Also to confirm: nothing the platform produces is legal advice and it must say so on the surface - the platform may be a meticulous clerk, not counsel. Blocks the law specialist in P3.23. Related: FU-268 (the four desktop archives). (found W495 (the Owner's native-AI-fabric roadmap, interrogated))
    FU-278 [medium] [p 2.0] ACCEPTANCE BAR for the legal specialist: a generated artefact must cite a page and a line that exist in a document the platform read, or it must not be generatable — The rider FU-277 leaves behind. W496's archive audit found the previous Law pipeline generating a ready-to-send disclosure letter over 342 rows of 'Simulated content for <filename>': it asserted an exhibit reference, a punctuality figure, a monitoring period, an Occupational Health date and a case citation, none of which existed in anything it read, and the Owner confirmed none could be verified (the particulars were redacted out in W496 and the originals preserved). The lesson is an ACCEPTANCE BAR for P3.23's legal specialist, not a one-off cleanup: (a) every factual particular in a generated artefact carries the document id and the location it came from, and a particular with no location cannot be rendered; (b) a citation of an authority is either resolved against a real source the platform holds or is refused - never emitted as prose; (c) the artefact states, on its face, which of its particulars came from a document and which are blanks the user must fill; (d) a guard drives the empty-corpus case and proves the generator produces a TEMPLATE with blanks rather than a letter with invented specifics. Without this bar the same class returns the first time the specialist runs on a thin bundle. (found W496 (FU-277, the archive audit))
  P3.24 — FABRIC - STAGED SIMULATION, PROCEDURAL FIRST
    FU-273 [medium] [p 2.2] OWNER DECISION: the tribunal outcome predictor is refused by default - confirm, or name a data source — The roadmap proposes a Tribunal Outcome Prediction that takes evidence strength, the opponent's likely arguments and 'judge tendencies (from public rulings)' and outputs a probability distribution of winning and a settlement range, labelled a 'Predictive Heuristic'. I have REFUSED it as specified and built the procedural half instead (P3.24 stage 1: deadlines and hearing windows computed from published rules and the case's own dates - checkable arithmetic, labelled a schedule). The reasons: there is no outcome dataset in this repo, no judge data, 'judge tendencies' is neither available nor a proper basis for advice to a party, and a settlement range shown to someone in a live matter is a number they may act on however it is labelled. THE DECISION: (a) confirm the refusal - the platform computes schedules and assembles evidence, and never forecasts an outcome (the default); or (b) name a real data source (e.g. a published outcomes dataset) and accept that any figure would be labelled a heuristic over that source, never a legal opinion, and never shown without its base rate and sample size. Governs the scope of P3.24. (found W495 (the Owner's native-AI-fabric roadmap, interrogated))
  P3.25 — WHAT THE PLATFORM RECORDS
    FU-283 [medium] [p 1.4] 25 of 43 DECLARED direct dependencies are imported by no .py in the repo — measured with each distribution's own top-level module names, not its package name — FU-282 was dropped because its transitive-pin premise was false. This is the claim that survives re-measurement, and the instrument matters: a first pass matched the DISTRIBUTION name and reported 28, which was wrong - pyyaml imports as yaml, PyJWT as jwt, scikit-learn as sklearn, psycopg2-binary as psycopg2, pyro-ppl as pyro, z3-solver as z3, POT as ot. Re-run against each installed distribution's own top_level.txt: of 43 direct dependencies in pyproject.toml [tool.poetry.dependencies], 16 are imported and 25 are imported by NO .py under agentic_core, integration_tests or scripts - langchain, langchain-community, streamlit, redis, sqlmodel, sqlalchemy, prefect, transformers, shap, PyJWT, pandas, seaborn, plotly, scikit-learn, pyro-ppl, ray, celery, web3, z3-solver, sympy, qiskit, pennylane, oqs, psycopg2-binary, firebase-admin. TWO ARE UNDECIDABLE and are not counted: POT is not installed here, and autogen's top_level.txt is empty so the instrument could not read its modules - an empty module list makes any() false, which would have reported it as unimported for the wrong reason. WHY THIS IS NOT YET A DELETION LIST: a dependency can be needed without a source import. psycopg2-binary and sqlalchemy/sqlmodel are exactly P4.4's pre-flight material and a driver is loaded by URL, not imported; redis may be reached the same way. So each of the 25 needs one of three verdicts - reached without an import (name the mechanism), held deliberately for a named plan item, or removable - and the ones that are removable matter, because CI and the Dockerfile both install from requirements.txt and the heavy ones here are ray, celery, qiskit, pennylane, transformers, web3 and firebase-admin. NOTHING IS REMOVED UNTIL EACH HAS A VERDICT. (found W500 (re-measuring FU-282's premise with real module names after it was falsified))
  P4.4 — Managed Postgres — migration dry-run script and rollback proven on a copy first
    FU-284 [medium] [p 1.5] P4.4's pre-flight has not been started: six database dependencies are declared and imported by nothing, so no migration dry-run or rollback exists to prove — P4.4 reads 'Managed Postgres - migration dry-run script and rollback proven on a copy first'. That pre-flight is OURS to build; the switch is the Owner's. Measured while correcting FU-282: sqlalchemy, sqlmodel and psycopg2-binary are DIRECT dependencies in pyproject.toml and no .py under agentic_core, integration_tests or scripts imports any of them; asyncpg and alembic are pinned in requirements.txt as transitive dependencies of prefect. So the toolchain for a Postgres migration is installed and NOTHING has been written with it - there is no schema, no migration, no dry-run script and no rollback, which is exactly what P4.4 says must exist before the Owner is asked to flip anything. A driver is legitimately loaded by URL rather than imported, so their presence is not the defect; the ABSENCE of the pre-flight they were installed for is. THE WORK, when P4.4's round comes: a schema derived from the stores that actually accumulate (VSB entities, the token ledger, the UEG chain, marketplace listings), a migration that runs against a COPY, a rollback proven on that copy, and a measured statement of what the JSON stores hold today so the migration has a known input. NOTHING is switched by this row. (found W500 (the corrected FU-282 analysis: the database dependencies exist for P4.4 and nothing imports them))
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
