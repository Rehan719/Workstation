# The biogeochemical cycles, the Sovereign Wealth Fund and the inter-agent communication fabric

**Three outside specifications, interrogated against this repository — W484, 2026-09-20.**

They arrived separately and are reviewed together because they are one body of work: the SWF
specification is the same six biogeochemical cycles with a capital mapping, and the communication
fabric restates both those cycles and the cognitive layer already reviewed in
`COGNITIVE_ENGINE_ARCHITECTURE.md` (W480). Reviewing them apart would have produced three documents
that disagreed with each other, which is itself one of the findings.

This review follows the rule the last three interrogations established: **ask the archive first, check
every cited path, and record only what this repository can be shown to contain.**
(`scripts/recovery_audit.py`, and [[feedback-ask-the-archive-before-building]].)

---

## 1. The finding that governs all the others

All three documents open with a table of "✅ Confirmed Existing Components — reuse as-is", presented
as the result of a recovery assessment. **Of the 28 distinct paths they name, three exist at the path
given.** That is the third consecutive proposal whose "what you already have" table was not checked
(W482's support specification cited thirteen paths; twelve did not exist).

This matters more than a list of typos, because every gate, test, deployment step and success
criterion in the three documents is built on those paths. A validation script that greps for
`from core.constitutional.constraint_engine import ConstitutionalGate` will fail forever, and a
"recovery" that cannot find its source silently becomes a rewrite.

### 1.1 What is actually where

Eight of the "missing" components DO exist — under different names, in different packages. The
proposals guessed a layout rather than reading one.

| The proposals say | This repository has |
|---|---|
| `core/transcendent_subsystems/simverse/` | `agentic_core/simverse/causal_simulator.py` |
| `core/transcendent_subsystems/pid/pid_controllers.py` | `agentic_core/biomimicry/geospheric/` — `regulator.py`, `homeostatic_regulator.py`, `balance_regulator.py`, `drad.py`, `resilience.py` |
| `core/transcendent_subsystems/geospheric_homeostasis.py` | the same directory |
| `core/transcendent_subsystems/tfel_accounting.py` | `core/transcendent_subsystems/tfel.py` |
| `agentic_core/cognitive/bridge/mushawara.py` | three live: `agentic_core/avatars/cognition/mushawara_bridge.py`, `agentic_core/consultation/mushawara/mushawara_bridge_2.py`, `products/capital_fund/consultation/mushawara_capital.py` |
| `agentic_core/cognitive/engines/mjm_v5.py` | `agentic_core/mjm/mjm.py` (+ `products/mjm-intelligence-engine/`) |
| `agentic_core/cognitive/personaliser/sil.py` | `agentic_core/personalisation/sil_personaliser.py` |
| `agentic_core/validation/vrpr/pipeline.py` | `agentic_core/quality/vrpr_pipeline.py` |
| `agentic_core/ledger/ueg/ledger.py` **and** `core/ledger/ueg/ledger.py` | neither — the live logger is `agentic_core.gaas.v5.UEGLogger`. An older `agentic_core/ueg/ledger.py` was archived by the W79 sweep. Two of the documents give different paths for the same object, so at least one was wrong even against itself. |
| `agentic_core/compliance/nemoclaw/validator.py` | archived: `_archive/agentic_core/governance/nemoclaw_runtime.py` (the live tree has only orphan `.pyc`) |
| `agentic_core/cognitive/engines/niyyah.py` | archived: `_archive/jules-unwired/agentic_core/cognitive/meta/niyyah_engine.py` (orphan `.pyc` only) |
| `products/capital_fund/digital_twin.py`, `pid_controllers.py` | do not exist — but `products/capital_fund/` is a real seventeen-package product (core/vault + multisig, treasury, portfolio, mesh, immune, regulatory, investors, sub_funds, vehicles, governance, orchestration, reporting, consultation, adapters, audit) and it IS wired: `agentic_core/api/capital_fund.py`, plus economy, resource_fabric, v310/governance and the native orchestrator import it. |

**Genuinely absent:** `agentic_core/finance/`, `backend/stripe/tiered_subscriptions.py`,
`core/constitutional/constraint_engine.py`, `config/fidelity_targets.yaml`,
`scripts/zero_placeholder_check_advanced_v2.sh`, `scripts/deploy_zero_cost.sh`,
`core/transcendent_subsystems/niyyah_reratification.py`, and the `archive/products/swf/` directory
both SWF documents tell the agent to copy from.

### 1.2 The SWF "recovery" — what was really there

The SWF specification lists five files to recover from `archive/products/swf/`, two of them
"🔴 Critical". That directory does not exist. Git history does contain `products/swf/`, added in
`a2c2f0fb` and removed in `07442957`, and it held exactly **two** files: `__init__.py` and
`sovereign_wealth_core.py`. The latter is **thirty lines** in full:

- a `cycles` dict of the six names with one setpoint each (`water: 0.10`, `carbon: 0.08`, …),
- `get_status()`, which returns that dict plus the literal `"compliance": "Articles 1-1342 active"`,
- `rebalance()`, which returns `{"status": "rebalance_initiated", "strategy": "conservative"}` and
  rebalances nothing.

There was never a `biogeochemical_cycles.py`, an `fcc_ratification.py`, a `compliance_bridge.py` or a
`cycles.yaml`. So the honest statement is: **the six-cycle MAPPING is recoverable; the SWF
implementation is not, because there has never been one.** The document's own sample code is the
first implementation, not a reconstruction — and it should be read and reviewed as new code, which
changes what is owed before it is trusted.

### 1.3 What the archive really does hold for these proposals

Worth recovering, and genuinely more than the SWF stub:

- `_archive/jules-unwired/agentic_core/biomimicry/ant_colony.py` (96 lines) — a real stigmergic
  scheduler: a pheromone table keyed subject → agent → level, a decay rate, NATS with a declared mock
  fallback. This is proposal #6's "Ant Colony layer", and it computes.
- `.../biomimicry/communication.py`, `homeostasis.py`, `economy.py`, `immune.py`, `federation.py`,
  `emergence.py` — the rest of #6's biomimetic layer, archived by the W382 sweep.
- `_archive/agentic_core/governance/nemoclaw_runtime.py` and
  `_archive/jules-unwired/agentic_core/cognitive/meta/niyyah_engine.py` — both leave an orphan `.pyc`
  in the live tree (already registered as FU-237), which makes their packages look populated.

---

## 2. The three documents contradict each other on their own constants

Both SWF documents and the communication fabric give PID gains and setpoints for the **same six
cycles**, and present them as exact recovered values that are "immutable" and may not be changed
"without FCC ratification + constitutional amendment":

| Cycle | SWF spec | Communication fabric |
|---|---|---|
| Water | kp 1.2 / ki 0.1 / kd 0.5 — 10% of AUM | kp 2.0 / ki 0.2 / kd 1.0 — thermal latency ≤50 ms |
| Carbon | 0.9 / 0.05 / 0.3 — 8% ROI | 1.5 / 0.15 / 0.5 — storage efficiency ≥90% |
| Nitrogen | 1.5 / 0.2 / 0.6 — drawdown ≤15% | 1.2 / 0.1 / 0.3 — throughput ≥1000/s |
| Oxygen | 0.8 / 0.08 / 0.4 — volatility ≤20% | 1.8 / 0.08 / 0.4 — ≥10× GPU baseline |
| Phosphorus | 1.1 / 0.15 / 0.45 — ≤20% per class | 1.0 / 0.1 / 0.4 — cache hit ≥85% |
| Sulfur | 2.0 / 0.25 / 0.8 — error <1% | 0.5 / 0.02 / 0.2 — latency <100 ms |

Two documents cannot both be the canonical recovered constants. And nothing in this repository ever
tuned either set against a plant: **an untuned PID gain is a decoration.** If the cycles are adopted,
the gains are DEFAULTS awaiting tuning and must be labelled so, with the tuning procedure named and
the first tuning run recorded. The setpoints are worse: "8% annualised ROI", "max drawdown ≤15%",
"volatility ≤20%" are aspirations. A controller driving toward an aspiration reports *deviation from
a wish*, which must never be rendered as performance.

---

## 3. Claims that must not cross into this repository

Each of these is either already registered as a defect here or is a claim the platform cannot back.

1. **`biomimetic_fidelity ≥ 0.924` / "≥90% functional equivalence to biological reference systems".**
   A weighted mean of three self-chosen sub-scores is not a measured fidelity to any natural process.
   It carries the name of a measurement nothing performed — the naming invariant (§11 of
   `COGNITIVE_ENGINE_ARCHITECTURE.md`).
2. **`require_halo2_proof=True`, "O(1) verification <1 ms".** W482 established that a "Halo2 proof"
   here is a SHA string named after one. FU-226 already records the same defect for Dilithium/Kyber.
3. **`vrpr.confidence ≥ 0.95` as a gate.** FU-233: the confidence is `0.90 + 0.05 × iteration`, read
   off nothing. Both SWF documents make it the gate on every transaction.
4. **`constitutional_gate.validate_request` as the backbone.** FU-235: twenty-one named validators,
   none registered, `fail_on_missing_validator: False` at every construction — it cannot refuse.
   W483 has just finished removing exactly this shape from the §11 screen.
5. **"Classical OAM-QKD surrogate … QBER <5%, key rate >5.5 bits/photon".** A software surrogate is
   not quantum key distribution and may not be named as though it were.
6. **"≥95% test coverage, ≥90% mutation score, zero placeholders" asserted as achieved state**, with
   a CI badge line to match. Those are measurements; this repository states them from a run.
7. **Tests that cannot fail.** `assert result["status"] in ["executed", "rejected"]` admits every
   outcome; `test_cycle_orchestrator_enforces_biomimetic_fidelity_target` mocks fidelity to 0.85 and
   then asserts it equals 0.85, its own comment conceding enforcement "would" happen in a real
   implementation. This is the shape already registered as FU-238.
8. **Code that cannot run.** `with_reratified_intent` returns `reratified_intent=ratified` — an
   undefined name. `HomeostasisStatus.deviation_reason` is read but never defined on the class the
   proposal itself supplies. `CycleOutput.rejected()` builds a `HomeostasisStatus` whose `deviations`
   maps to a string where every other use maps to a dict. The samples are sketches.
9. **Money and deployment.** AUM, MiFID II, ISO 20022, Stripe tiers, `$1M AUM cap`, Cloud Run with
   `--allow-unauthenticated`, Firestore indexes, "$0 owner expenditure". Money here is **virtual WST**
   and the real-money rails, live Stripe, managed Postgres and production deploy are OWNER-GATED
   (P4.5/P4.6). None of it is in scope for the item this review plans.

---

## 4. Invariants any adoption is held to

1. **A cycle reports a measured figure or says it cannot.** No cycle returns a constant, and no
   `biomimetic_fidelity` is emitted unless something measured fidelity to a named reference.
2. **A PID gain is a default until it is tuned**, and the record says which it is.
3. **A setpoint is an aspiration until something measures the variable.** Deviation from an
   aspiration is never reported as performance.
4. **A gate's default is refusal** (and see W483: a screen may refuse and may escalate, never clear).
5. **No second store of figures.** The cycles read the ledger, the waterfall, the heartbeat and the
   immune system that already exist. A cycle that needs a number nothing measures reports
   `assessable: false`.
6. **Virtual only.** Every flow the cycles touch is virtual WST inside the existing economy.
7. **One governance path.** Changes route through the existing Change Control Agency — not an "FCC".
8. **Recovery is read-then-decide.** The archive holds both real work (the ant-colony scheduler) and
   stubs (the SWF core). Recovering without reading is how a thirty-line stub becomes a "critical
   component".

---

## 5. What is genuinely valuable, and what P3.19 should do

The **mapping** is a good idea and belongs in §8 of the vision: six named operational functions, each
with a natural analogue, plus a coupling matrix between them. The honest form is **a control surface
over flows this repository already measures** —

| Cycle | The flow that already exists here |
|---|---|
| Water — liquidity | the reserve fund and the virtual ledger's balances |
| Carbon — growth | self-investment spend and its returns (`economy/revenue.py`) |
| Nitrogen — risk | the §8→§12 survival instinct and the immune system |
| Oxygen — metabolism | the heartbeat and its per-beat work |
| Phosphorus — allocation | the §4 six-stage profit waterfall, Owner-adjustable within template bounds |
| Sulfur — resilience | immune records, Change Control holds, the operational-excellence outcomes |

— driven by `agentic_core/biomimicry/cycles/` and `cycles/bindings.py`. CORRECTED W543: this named `agentic_core/biomimicry/geospheric/`, whose five modules contain no PID at all (regulator.py is a proportional comparator that returns an action string); the real PID is in cycles/base_cycle.py and nothing called it.
Not a seventh store of invented numbers. That reframing, plus recovering the ant-colony scheduler and
the rest of #6's biomimetic layer from `_archive/`, is what **P3.19** is for.

Proposal #6's protocol tier (MCP · A2A · ACP · FIPA-ACL) is a separate and also real question: this
repository's agents talk through `agentic_core/api/agent_hub.py` (W443), not a protocol stack.
Adopting MCP or A2A is an Owner-level architecture decision, not a recovery, and it is not planned
here.

## The archived biomimetic layer, read and decided (W544 — FU-243)

FU-243 asked for a read-then-decide record over the archived biomimetic layer: read each module, recover
what computes, delete the orphan `.pyc` for what does not, and record which was which. This is that record.
**Nothing here is recovered into the live tree by this round** — a recovery is a build with a consumer, and
each verdict below says what a recovery would require.

**TWO OF THE ROW'S OWN PREMISES WERE WRONG, measured before anything was decided.**

1. **There are no orphan `.pyc` files.** The row says "the live `agentic_core/biomimicry/` keeps an orphan
   `.pyc` for each", which "makes the package look populated". Measured: `agentic_core/biomimicry/__pycache__/`
   contains exactly one file, `__init__.cpython-312.pyc`. So the delete half of the FIX is already
   satisfied — by the earlier `.pyc` sweep, not by this round — and nothing was deleted here.
2. **The archive holds THIRTY-THREE modules, not six — and this record's first draft said ten.** The row
   names seven files and calls them "six biomimetic layer modules". Measured:
   `_archive/jules-unwired/agentic_core/biomimicry/` holds **33 top-level `.py` files totalling 2,693
   lines**, plus four subdirectories (`adapters/`, `capital/`, `cascade/`, `cycles/`).
   **The first draft of this section claimed ten, because the directory listing it was written from was
   truncated at fourteen entries and nobody re-counted.** The completeness leg in
   `test_w544_the_sixth_cycle_joins_the_other_five_and_the_archive_record_is_complete` caught it by
   comparing this table against the directory, which is the whole reason that leg computes its list
   instead of trusting this prose.

   **SCOPE OF THIS RECORD, stated rather than implied:** the ten modules below are FU-243's seven named
   files plus the three siblings adjacent to them (`apoptosis.py`, `autophagy.py`, `avatar.py`). The other
   twenty-three are NOT assessed here and are named so that the gap is visible:
   `ethical_transparency`, `federated_learning`, `fitness`, `gaas_validator`, `hal`, `marketplace`,
   `metabolism`, `module_generator`, `module_library`, `moo`, `morphogenesis`, `mycelium`, `nas`,
   `octopus`, `optimizer`, `predictive`, `recombination_validator`, `recombiner`, `resilience_manager`,
   `summarizer`, `swarm_formation`, `symbiosis`, `tournament`. A record that quietly covered ten of
   thirty-three while reading as a survey of the layer would be the same defect the table below convicts
   `autophagy.py` of: a precise-looking account of work that was not done.

**AND THE PACKAGE DOES NOT LOOK POPULATED FOR THE REASON THE ROW GIVES.** It looks populated because a
sibling does real work: `agentic_core/biomimicry/cycles/utils.py` exports `constitutional_guard`, which ten
cognitive engines import. A reachability check that greps the package therefore finds a crowd of importers
and concludes the layer runs. That is why W543 measured reach per CLASS rather than per package.

| module | lines | what COMPUTES | what is FABRICATED or DECLARED-MOCK | verdict |
|---|---|---|---|---|
| `ant_colony.py` | 96 | **The algorithm is real.** A pheromone table keyed subject → agent → level; `deposit_pheromone` is genuine positive feedback; `decay_pheromones` multiplies by `(1 - 0.1)` for evaporation; `allocate_task` selects by highest pheromone and broadcasts when the table is empty. | The NATS transport is a **declared** `MockNATS`, and `initialize()` logs a warning when the real connect fails — honest about itself. | **RECOVERABLE ALGORITHM, NO CONSUMER.** The stigmergy computes and is worth keeping. A recovery needs a real task-allocation consumer on this platform and a transport; NATS is not installed. Recovering it without a consumer would add a scheduler nothing schedules — the exact state the six cycles were in before W543. |
| `homeostasis.py` | 54 | **Computes over caller-supplied input.** `monitor_vitals(current_vitals)` takes vitals from its caller rather than inventing them, and computes a real latency delta against its setpoints. | Setpoints (`cpu_target` 70.0, `latency_target_ms` 10.0) are literals with no provenance. It indexes `current_vitals["latency_ms"]` directly, so a missing key raises rather than reporting a third state. | **SUPERSEDED, NOT RECOVERED.** A live homeostasis path already exists and is better wired: `agentic_core/api/organism_status.py` computes an adjustment and **files it through the Change Control Agency**. Recovering this would be a second homeostasis with no governance path. |
| `emergence.py` | 75 | **Counts real markers from real events.** `ingest_event` increments per-agent counters for leadership, altruism and specialisation from the event payloads it is given. | Nothing fabricated. The counters are only as good as the event source, and it has none. | **COMPUTES, NEEDS AN EVENT SOURCE.** Note on scope: it grades AGENTS, not people, so Ruling A.9.5 is not engaged — but any later recovery must keep it that way. |
| `immune.py` | 97 | **Computes a score from supplied events** (`score_inc += 0.3` / `+= 0.1` per marker) and `_trigger_adaptive_response` zeroes a trust factor. | The increment weights are literals with no provenance, and a comment states the handoff is simulated. | **SUPERSEDED, NOT RECOVERED.** `agentic_core/genetic_immune/immune_system.py` is live and holds `evaluate_threat`. W543 declined to bind the nitrogen cycle to it for a related reason: it scores a sample a caller supplies and holds no standing figure. |
| `economy.py` | 57 | `get_balance` reads a real token balance. | `process_yield` applies a **"0.1% daily yield (simulated)"**, and `execute_payout` returns True/False on a balance check alone. | **DO NOT RECOVER.** The live VSB economy (ledger, §4 waterfall, virtual WST) is the real one, and a simulated yield is precisely what it must never contain. |
| `federation.py` | 78 | `find_node` genuinely sorts and returns the nearest five ids. | Its own docstring says **"Simulated Kademlia DHT"**: `put` writes to a local dict and `get` reads it back. There is no distributed hash table, no network, no peers. | **DO NOT RECOVER AS FEDERATION.** It is a dictionary with a DHT's vocabulary. The honest description of what it does is "a local dict", and recovering it under the name federation would make a single process look like a network. |
| `communication.py` | 67 | Nothing. | `self.clients` is annotated **"Simulated connected SSE clients"**, and `push_alert` returns `True` unconditionally — reporting a delivered alert with no transport. | **DO NOT RECOVER.** Already settled by Owner ruling: Channels is retired. A notifier that reports success without delivering is a worse surface than no notifier. |
| `avatar.py` | 68 | **One real thing worth keeping as a RULE, not as code:** `start_stream` refuses when `user_consent` is false. | `synthesize_speech` returns `{"status": "SUCCESS", "latency_ms": 150.0}` — a literal latency for speech it did not synthesise. | **DO NOT RECOVER THE CODE; KEEP THE CONSENT RULE.** A fixed latency reported as measured is the same defect W543 removed from the fabric's health, and W541 from the support answer. |
| `apoptosis.py` | 46 | Nothing. | `reclaimed_ram_mb = 128.0 # Mock`, emitted as a completed reclamation. | **DO NOT RECOVER.** |
| `autophagy.py` | 46 | Nothing. | `purged_items = 150`, `pruned_deps = 3`, `reclaimed_space_mb: 45.2` — all literals, emitted as a completed recycling cycle. It purges no cache and prunes no dependency. | **DO NOT RECOVER.** The most instructive of the ten: it logs "Cycle complete" and emits three precise figures for work that never happened. Nothing about the output reveals that. |

**THE TALLY: three compute and have no consumer (`ant_colony`, `emergence`, and `homeostasis` which is also
superseded), two compute but are superseded by live systems (`homeostasis`, `immune`), and five fabricate
outright (`economy`, `federation`, `communication`, `avatar`, `apoptosis`, `autophagy` — six by file, five
by subject, since `avatar` carries one rule worth keeping).** Not one of the ten is recovered into the live
tree by this round, and the reason is uniform: every module that computes computes over input it is HANDED,
and this platform has no caller to hand it any. That is the same finding W543 recorded about the six cycles,
and it is the finding that matters about this whole layer — the algorithms were never the missing part.

## The other twenty-three, read and decided (W563 — FU-356)

The W544 section above named twenty-three modules it did **not** assess, so the gap would be visible rather
than implied. This is that assessment, on **two axes**, because the first one alone would have answered the
wrong question. Axis one reads the code: what computes, what fabricates, and a verdict. Axis two asks what
the first pass never asks — **is the capability wanted here at all**, is it already live, and does the
vision call for it. **Nothing is recovered into the live tree by this round.**

### The two tallies, and the second one is the answer

**AXIS ONE — THE CODE: fourteen RETIRE, nine RECOVERABLE_WITH_REPAIR** (fifteen and eight after the one
verdict-changing correction below). **104 distinct fabrications across twenty-three files totalling 2,009
lines, a mean of 87.3 each** — so 4.5 fabrications per file. (The mean was first written as 85 and
measured 87.3; a figure rounded in the wrong direction in a record about unmeasured figures is worth
correcting rather than letting stand.) **All twenty-three fabricate at least one thing.**
`morphogenesis.py` was reported as
the exception and the verification pass found line 23 asserts the parent of every spawned node by the
literal `"core_node_1"`.

**AXIS TWO — THE CAPABILITY: fifteen SUPERSEDED, four WANTED_REBUILD, four NOT_WANTED — and ZERO
WANTED_RECOVER.** For **eighteen of the twenty-three the vision does call for the capability**, and in **not
one case is the archived code the route to it.** That is the whole finding. "Recoverable" was the wrong
question: nine files can be repaired and none of the nine should be, because for fifteen a live system
already does the job better and for four the capability is wanted but the code is an *anti*-head-start —
built from precisely what the item that wants it forbids.

**AND ZERO OF THE TWENTY-THREE JUDGE A PERSON.** Ruling A.9.5 is not engaged by any module as it stands:
every verdict in the layer is scoped to an action, an artefact or a software agent. Two rows need naming
anyway. `module_generator.py` mints display names in a `Religion` domain — not a person-verdict, but it
manufactures religious-authority artefacts, which the Owner's ruling of 2026-09-29 places outside anything
this platform may assert on its own. And **`fitness.py` carries the one half of this layer that could not be
written without a ruling first**: see the Owner question below.

**THE VERIFICATION PASS CORRECTED AXIS ONE 46 TIMES** — **7 wrong, 26 a missed fabrication, 11
overstated, 2 unsupported.** The largest class is a *missed* fabrication, so the first read was
systematically too generous rather than too harsh, and this record states the breakdown instead of
reporting the first pass. Three corrections bear on a decision and all three are folded in: the
`morphogenesis` hardcode; `module_library`'s verdict, moved to RETIRE on the ground that the same repairs
leave the same dict wrapper `ethical_transparency` was retired for; and `federated_learning`'s basis, which
asserted a universal ("no HTTP transport exists") where the supportable statement is narrower — no
**peer-to-peer or federation** transport exists, since six live modules do import HTTP.

| module | lines | what COMPUTES | what is FABRICATED | verdict | disposition |
|---|---|---|---|---|---|
| `fitness.py` | 116 | A real weighted sum, a star average, and an honest append-and-emit store with an explicit (stars) and an implicit (dwell) channel. | **The no-feedback fallback: 70% of the reported fitness becomes a uniform random draw.** CORRECTED IN W564 BY REFUTING THIS ROW: the first draft quoted `0.8 + random()*0.2`, which that call site CANNOT REACH — it passes the 17-character literal `"agent_output_mock"` and the branch needs a length above fifty, so the reached expression is `0.4 + random()*0.3` and `user_context` is ignored entirely. The defect is unchanged in kind and smaller in magnitude: `user_base` lands in [0.40, 0.70], so the reported fitness is 0.3·tech + 0.7·that, which even at a perfect technical score cannot exceed 0.79. Quoting a branch without checking that the caller reaches it is the same defect this table convicts others of. Metric defaults meaning "not measured" become scores. The per-user model "simulates federated learning" and is never read. "(Article 1120 compliant)". | RECOVERABLE_WITH_REPAIR | **WANTED_REBUILD.** FU-311 and P3.27(2) want exactly this capability and the code is built from the three things that clause forbids — a synthesised signal in the one place it must read "not measured", defaults that make an unmeasured system look mediocre-but-measured, and undated "Phase 4" weights. Copying it would re-commit the class the item exists to prevent. |
| `metabolism.py` | 55 | ~20 lines of honest ledger arithmetic, **both branches real and reachable**: it debits and emits `METABOLIC_EXCHANGE`, or refuses and emits `METABOLIC_STARVATION` naming required beside available. It invents no measurement — `compute_units` arrives from its caller. | The opening `wst_balance = 1000.0`, the rate `0.05` labelled "Example", and "resource burn rate" for a list nothing reads. | RECOVERABLE_WITH_REPAIR | **SUPERSEDED** by `molecular/work_budget.py` (the Owner-ruled instrument, in seconds and tokens, with `store_lock` and atomic writes) plus `atp_simulator.py` and `organism/reconfiguration.py`. `cost = compute_units * 0.05` is the exact class ruling S18.1 removed: a currency figure from an undefined unit by a coefficient with no provenance. |
| `predictive.py` | 58 | A two-point slope — and **an explicit `INSUFFICIENT_DATA` refusal below five samples**, taken before any arithmetic. | A **strictly positive** random term added to every forecast — and the recommendation is chosen by a threshold over that number, so **the random draw can change the advice**. Timestamps recorded and discarded. `numpy` imported and unused. | RECOVERABLE_WITH_REPAIR | **SUPERSEDED, and the vision does not ask for the rest.** `plan_followups.forecast()` already projects in rounds from a measured closure rate and returns "not projected" with a basis rather than a number. The slope also divides a rise by the sample **count** rather than the time span. |
| `octopus.py` | 92 | `OctopusCRDTManager` (L6–35) is a genuine CRDT wrapper and the only non-trivial capability in the layer: real `Y.encode_state_as_update` binary state and a convergent `Y.apply_update` merge, with no fabricated figure in those ~30 lines. | `OctopusEmbodiedIntelligence`'s branch is decided by `hal.py`'s hardcoded `0.92` against a `0.85` threshold, so **the fallback leg can never execute and the author says so at L85**. `250.0` ms reported for a central call never made. | RECOVERABLE_WITH_REPAIR (split) | **SUPERSEDED.** The half the plan wants — refuse a *tier*, never the request — shipped in `ai/native/tiers.py route()`, which walks down from the wanted tier recording a `why_not` per rejection and terminates on a floor that always runs. **`y_py` is in no requirements file**, so the module raises `ImportError` before any logic. |
| `hal.py` | 113 | `stdp_update` is a correct bounded monotone plasticity rule, and `RealCL1SDK.connect` is **commendably honest** — it returns False and says so rather than faking hardware. | `{"confidence": 0.92}`. A latency that times its own `random.uniform(0.005, 0.015)` sleep, reported as meeting a 5–15 ms criterion. `efficiency_ratio = 250.0/1.25` with `"status": "Target Met"` — a verdict about silicon nothing measured. | RECOVERABLE_WITH_REPAIR | **NOT_WANTED.** Nothing in the vision asks for neuromorphic hardware, and nothing in this repository produces spike pairs to feed the one real function. Deleting `cl1_infer` and `power_profile` — whose outputs *are* the constants they were built from — leaves ~20 of 113 lines with no caller. |
| `marketplace.py` | 94 | Real guarded arithmetic: `transfer` refuses on insufficient funds and mutates nothing; a listing whose SOLD state is **conditional on the transfer succeeding**; tax computed from the price. | A `100000.0` liability fund nothing computed and nothing reads. "Escrow" with no hold. "Reputation" as an empty dict. **"(ERC-20) Smart Contract on Polygon"** with no chain anywhere. No `amount > 0` guard, so a negative transfer credits the sender. | RECOVERABLE_WITH_REPAIR | **SUPERSEDED, and refused on top of that.** The live VSB economy owns settlement and money is **virtual WST** by ruling; the blockchain claim is exactly what §3 above forbids crossing into this repository. |
| `symbiosis.py` | 91 | A real partnership ledger: a sorted-pair key, **a membership gate that genuinely refuses an unregistered pair**, and a volume accumulator. | Trust seeded at `0.5` by literal, rising with repetition and **never able to fall**, so the Article 1105 fairness gate is unreachable. **A failed payment is recorded as a completed exchange** — the Article 1110 claim inverts in exactly the case it governs. | RECOVERABLE_WITH_REPAIR | **SUPERSEDED.** Inter-entity investment is already built (§4 Stage 4), and Vision 8.0 Thrust E explicitly refuses a rescue channel between entities. |
| `module_library.py` | 104 | A correct SHA-256 over canonically-serialised JSON, a dict store, a working substring query. | **A wall-clock timestamp inside the hashed payload, which defeats the content addressing the module claims.** A 128-dimension "embedding" whose 128 components are the same number. "Vector search" that never reads a vector. 15 seeds pointing at artefacts that do not exist. | **RETIRE** (verifier-corrected) | **SUPERSEDED.** The first pass said a repair was possible; the ground for correcting it: after its own repairs the honest remainder is ~25 lines of dict wrapper, which is what `ethical_transparency` was retired for — and a better archived candidate exists for the genuine hole (`layer_registry.py:14` declares layer 7 and the live directory is empty): `_archive/jules-unwired/agentic_core/layers/l7_module_library/registry.py`, which persists to disk. Compare the two; wire neither blind. |
| `moo.py` | 89 | **The algorithm is genuinely present** and is deap's, correctly wired: NSGA-II, properly bounded SBX and polynomial operators, real non-dominated sorting. The only module of the twenty-three whose claimed algorithm is actually there. | **The entire objective function** — three invented formulas over a genome with no referent, emitted per generation as `best_accuracy`. "Provides Pareto-optimal swarm configurations", present tense. | RECOVERABLE_WITH_REPAIR | **SUPERSEDED.** `cognitive/meta/tawazun_engine.py` (P3.13, W524) computes the non-dominated set over named objectives with stated directions and refuses while naming what was missing. The leftover half — generating candidates — nothing asks for, and **`deap` is in no requirements file**. |
| `tournament.py` | 84 | Generic deap wiring; its own contribution is `_evaluate_swarm`. | **70% of every fitness value is `random.random()`** under "placeholder for RLHF reward model"; the other 30% is the mean of a five-float vector mapping to nothing. "Production-grade" four lines above the RNG. | RETIRE | **WANTED_REBUILD.** Selection is ratified and sequenced (S18.3: lineage first, selection second, mitosis third), but the "evolution" here optimises noise and it ships the worst-shaped artefact in the set — a per-generation best-fitness curve that looks like learning and is order statistics on random numbers, printed as proof by its own `__main__`. |
| `recombiner.py` | 216 | Source-hash resolution and one `None` check. **No tensor, array, weight, mask, sign or Fisher quantity is touched anywhere in 216 lines.** | TIES / DARE / Fisher are three real published method **names** implemented as `time.sleep(1.0)`, `0.8` and `1.2` — **three named algorithms are three durations.** A licence determination asserted by a literal. `crossover_points` hardcoded. | RETIRE | **WANTED_REBUILD.** Meiosis over constitutions producing a ratifiable candidate is an Owner-ruled want and is not built. This is no head start: the live Protocol of the same name requires `async merge_weights(List[Dict[str,float]])`, which this class does not implement, so **recovering it would not even fill that port.** |
| `recombination_validator.py` | 82 | Three dict lookups and a constant. One gate tests a real property: a non-empty lineage. | `perf_score = 0.92 # Mock score` behind a `0.3`s sleep, **published as measured performance**. The licence gate refuses only the literal `INVALID`, **which the only producer never writes**. Then it logs "passed all validation gates" and emits `OFFSPRING_VALIDATED`. | RETIRE | **WANTED_REBUILD — and it is the anti-pattern this programme exists to remove.** P3.26(6) ratifies the gate; two of these three gates cannot fail. |
| `gaas_validator.py` | 111 | `_load_articles` is a working regex parser — 42 articles against the **archived** constitution, **0 against the live one**, which uses a different heading form. | **`self.articles` is never read outside `__main__`**, so the parsed constitution never reaches the decision. `reason = "Constitutional alignment verified."` for every non-high-risk payload. Trust defaults to **maximum** for an unseen agent and is regained by **volume of allowed calls**. | RETIRE | **SUPERSEDED** by the live `gaas/v5` stack, which carries which article refused, escalation-versus-breach, and whether the decision reached the ledger. `validate_payload("a", {})` returns ALLOW with "Constitutional alignment verified." — a validator that clears empty input, breaching canon §4. |
| `ethical_transparency.py` | 61 | An f-string template over three dict keys, plus one article lookup. | **An unconditional clearance over empty input**: `explain_decision({})` returns "Everything looks good! This action aligns with our constitutional values." A constitutional-failure claim with no article identified. **It reads the real `reason` field and discards it**, substituting generic prose. | RETIRE | **SUPERSEDED.** Breaches canon §4 and §3 directly. Repairing it leaves ~15 lines that re-print fields the caller already holds. |
| `module_generator.py` | 67 | Nothing beyond `random.choice` and `random.randint`. | **The entire generated inventory** — 485 rows in its own demo, named e.g. `Health-Specialist-LLM-847`, `content` set to `bin://{name}.gguf` for files never created, metadata asserting int4 quantization and LoRA rank 16. A comment asserting a "Constitutional Integrity Check (Simulated)" above a call that performs none. | RETIRE | **NOT_WANTED, and of the twenty-three the one that would most damage the register.** Its volume is the point: recovering it adds hundreds of claims that quantized models exist, and no capability whatsoever. |
| `nas.py` | 73 | A uniform draw from a 27-point grid and two closed-form formulas over the draw. | `est_accuracy = 0.6 + layers/40 + dim/10000` — **an invented formula that is not dimensionally possible and returns values above 1.0**, written into the registry **as a discovered metric**. "Pareto-optimal" with no dominance test. `time.sleep(0.2)` for search cost. | RETIRE | **NOT_WANTED.** Nothing is searched and nothing is selected: the input space is returned under the longer name "discovered architectures". |
| `optimizer.py` | 62 | One real line: a composite reward from the passed KPIs. | **`action = random.choice([...])`** under the author's "# Policy Selection (Simulated PPO)". `reward_history` is written and **never read**. `SYSTEM_OPTIMIZED` emitted unconditionally, including on IDLE. | RETIRE | **SUPERSEDED.** Vision 8.0 Thrust A.3 already names this as the archived candidate that does not accumulate error. Wiring it adds the claim "the system reconfigures itself by reinforcement learning" and the capability of a coin flip on one integer. |
| `morphogenesis.py` | 52 | List push/pop on an in-memory dict. The connection pruning is correct, and **of the modules that emit events at all, it is the only one that suppresses the event on a no-op** — corrected in W564 from "the only module here that does not emit on a no-op", which is false: six of the twenty-three (`gaas_validator`, `hal`, `module_generator`, `module_library`, `octopus`, `resilience_manager`) have no event emitter at all, so they cannot emit on anything. | **Line 23 asserts the parent of every spawned node by the literal `"core_node_1"`** — found by the verification pass, not the first read. Node ids are reissued after a prune/spawn cycle. | RETIRE | **SUPERSEDED.** 52 lines of list operations wearing service-mesh vocabulary: "triggers agent spawning or migration" is `list.append` of a string, with no migration path. |
| `swarm_formation.py` | 97 | A genuine Euclidean distance and **a correct single-rule Boids cohesion step** — about six real lines. | A trust score fixed at maximum, never computed, never read. `SWARM_FORMED` **announcing a formed swarm with a leader for a party of one.** Random velocity re-drawn every tick. Alignment and Separation are asserted in the docstring and absent. | RETIRE | **SUPERSEDED.** Everything it is named for is missing, and the gap needs the clusterer written — building, not repairing. |
| `summarizer.py` | 52 | `len(events)`. **The events list is never iterated, never read.** | **"94% fitness" and "99.8% uptime"** as two invented metrics inside the returned digest. "using local LLMs" with no model anywhere. A latency that times a random sleep, stored as summarization latency. | RETIRE | **SUPERSEDED.** Strip the fabrications and what remains is one f-string over `len()`. Recovering it would import a sentence asserting 94% fitness into a live surface. |
| `federated_learning.py` | 62 | **The Laplace mechanism is written correctly** (scale = sensitivity/epsilon) — the one real formula in the file. | **The averaged node updates are made by `random.uniform`**, over global weights seeded by `random.random()`. **ε=0.1 presented as a privacy guarantee for a round that transmitted nothing.** `FL_ROUND_COMPLETE` on an empty participant list. "Secure Aggregation". | RETIRE | **NOT_WANTED.** Federated averaging needs nodes, data and a model and this has none of the three. Corrected basis, TWICE: the first said no HTTP transport exists anywhere, which is false (six live modules import it); the verifier's replacement said `agentic_core/network/*.py` import only stdlib, which is ALSO false — `planetary.py` imports `fastapi` and `stack.py` imports `agentic_core.governance.gaas`. **The supportable statement, measured in W564: no module in `agentic_core/network/` imports a TRANSPORT** — no `httpx`, `requests`, `aiohttp`, `grpc`, `websocket`, `socket`, `libp2p` or `nats` in any of the five — so there is nothing to reach a peer with. A server framework is not a peer transport, and an internal import is not one either. Two false universals in one basis is the strongest evidence in this record for computing a claim instead of writing one. |
| `mycelium.py` | 84 | It writes to and reads from one local dict. | `"latency": random.uniform(5, 50)` on insertion, then an Article 1102 latency gate over it. `"status": "ALIVE"` stamped unconditionally. A heartbeat that **refreshes its own liveness evidence** with this process's clock. `new_path = [...]` logged as "Automatic reroute successful" and emitted as `NETWORK_REROUTE`. | RETIRE | **SUPERSEDED.** The recorded KademliaDHT shape again: a plain dict carrying a mesh's vocabulary. Three of its four methods produce a fabrication and the fourth manufactures its own evidence. |
| `resilience_manager.py` | 94 | **Nothing of its own.** Every substantive action is a `Callable` the caller supplied; `mmr_repair` passes both states straight through with no diffing. Its sole original logic is one `>` comparison. | `recovery_success_rate = 1.0` that nothing updates, and `"status": "Homeostatic"` derived from it. Counters reported as repairs. "Global state reconciled via Raft/libp2p re-sync". | RETIRE | **SUPERSEDED.** The repository already carries this name three times, and `integration_tests/test_mvp_spine.py` records a `ResilienceManager` guard leg already "RETIRED WITH ITS SUBJECT" under W506/FU-078. It would add a fourth claim of self-healing and no self-healing. |

### Where these twenty-three land on Vision 8.0's five thrusts

Asked by the Owner directly: are they relevant to the biomimetic implementations planned in
`docs/WORKSTATION_VISION_8_BIOMIMETIC.md`? **Nineteen of the twenty-three land on a thrust by subject —
and on the four thrusts where they land hardest, the archived module fabricates at the exact point the
thrust exists to make honest.** The subject overlap is real; it is the reason to read them, not to take them.

| thrust | the honesty requirement it states | the archived module on that subject | what it does there |
|---|---|---|---|
| **E.1 user satisfaction** (gates all of Thrust E) | build the mechanism; §E.2 selection **refuses** while a measure is unmeasured | `fitness.py` | has the mechanism, then **falls back to a random draw** when it has no feedback. An unmeasured user is scored, which is the whole defect; the FIGURE first written here (~0.9) was arithmetically impossible and is corrected — the reachable branch puts the user term in [0.40, 0.70] and the weighted total at most 0.79 |
| **C checkpoints** | three of five live gates default to pass — flip them | `recombination_validator.py` | a gate that **cannot fail**, publishing `0.92` as measured performance |
| **B cognition** | no engine may report a confidence it did not compute | `hal.py` | confidence hardcoded `0.92`, latency timing its own random sleep |
| **A.3 integral control** | "neither the archived nor the live candidate accumulates error" | `optimizer.py` | **this is that archived candidate**: the policy is `random.choice` |
| **A energy** | "not this thrust: a new budget mechanism" | `metabolism.py` | a real ledger with an invented opening balance and an undefined unit |
| **D.5 meiosis** | a recombined constitution needs ratification | `recombiner.py` | three real method names implemented as three `time.sleep` durations |
| **D metamorphosis** | a transformation that does not dissolve what the last stage needed is accretion | `morphogenesis.py` | **only appends and pops**, parent edge asserted by a literal |
| **E selection** | select on **record**, not on a proxy | `tournament.py`, `moo.py` | 70% of fitness is RNG; `moo`'s algorithm is real and its objective is invented |
| **cross-cutting truth maintenance** | a screen may flag and escalate; it may never clear | `gaas_validator.py`, `ethical_transparency.py` | **both clear empty input**, one with "Constitutional alignment verified." and one with "aligns with our constitutional values" |

### What is actually worth carrying: five rules, and not one line of code

Every item below is a **shape or a rule with a line reference**, to be written fresh against a live
consumer. None is a recovery, and nothing here authorises adding a dependency.

1. **A budget that can say no, and says what it was short by** — `metabolism.py:23,32–39`. The refusal
   leg emits `required` beside `available`. This answers a **live open need**: FU-308 records that the live
   budget's `can_deplete` is False by arithmetic with a 4× gap, so the organism currently has no way to
   refuse. Keep the shape; discard the `0.05` coefficient, the WST unit and the minted opening balance.
2. **Refuse before computing, on a stated minimum** — `predictive.py:25–26`, an `INSUFFICIENT_DATA`
   return taken *before* any arithmetic. The only thing in that file which cannot lie.
3. **Refuse an offspring that cannot name its parents, and record how deep the lineage goes** —
   `recombination_validator.py:27–31` plus the `provenance_depth` field. It matches a measured live gap:
   FU-312 records that a VSB record carries no parent and no lineage field at all, which is the
   precondition for any form of entity reproduction. **Nothing else in that file.**
4. **Record each selection round as it runs, not only its winner** — `tournament.py:63–67`. P3.27(3)
   and (4) need exactly that record to show *which* measure was missing when selection refused and *which*
   floor a flagged entity failed.
5. **A collective is governed at the FLOOR of its members, never their average** —
   `gaas_validator.py:64–66`, `effective_t_fa = min(t_fa, swarm_t_fa)`. Worth keeping as a rule if a
   swarm is ever given a governed identity.

Two further shapes are **corroboration rather than salvage**, and are recorded so no later round mistakes
them for new work: `recombiner.py`'s pluggable-backend ABC that raises on an unknown method — which
`genome.py`'s `_CROSSOVER_METHODS` already does — and `moo.py`'s `weights=(1.0, -1.0, -1.0)` declaring each
objective's direction as data, which `tawazun_engine` already enforces because guessing a direction inverts
the frontier.

And **`octopus.py`'s `OctopusCRDTManager` is a shape reference only.** It is the only genuinely non-trivial
code in the layer, and it is still not a recovery: `y_py` is in no requirements file, nothing ratified calls
for CRDT state, and the frontend's own already-unused `yjs ^13.6.14` is where that question would be settled
if the Owner ever asks for multi-user co-edit.

### One Owner question this assessment raises, and nobody may write it meanwhile

`fitness.py` lines 73–84 collect **implicit** feedback — a person's dwell time — and lines 86–95
build a **per-user preference model** (`verbosity_pref`) from that person's own behaviour. Neither is a
verdict on a person and neither breaches A.9.5 as written, so the module passes the ruling. But a *rebuild*
of that half would mean the platform maintaining a behavioural model of an individual, which meets the
Owner's one-question test — **is the subject a person?** — and that is a ruling, not an engineering
choice. **Until the Owner rules, FU-311's channel is built from the explicit rating only**
(`fitness.py:59–71`'s event shape: user, subject, stars, flags, type, timestamp — with the aggregate
reading `None` rather than a default on an empty store). The implicit channel and the per-user model are not
written.

### What this record does not do, and the mechanical fact underneath it

It recovers nothing, installs nothing, and adds no dependency. Every RECOVERABLE_WITH_REPAIR above says a
repair is *possible*, not that it is scheduled — and axis two then says, for each in turn, that the
repair should not happen.

**NEITHER `_archive/jules-unwired/agentic_core/` NOR ITS `biomimicry/` DIRECTORY HAS AN `__init__.py`**, so `import
agentic_core.biomimicry.<name>` resolves to the LIVE package and fails for all twenty-three. (CORRECTED IN W564:
this read "no `__init__.py` at any level", which is FALSE — forty-six exist under that archive root, two of them
inside `biomimicry/` itself, at `adapters/` and `capital/`. The operative fact is the absence at those two
levels, not an absence everywhere, and the stronger sentence was a universal this record did not compute.)
Loaded by file path instead, **sixteen of the twenty-three execute and seven fail outright** — four on the
missing intra-package import of `module_library`, `moo` and `tournament` on `deap`, `octopus` on `y_py`
— **and neither `deap` nor `y_py` is installed or listed.** There is no wire-up available for any of them;
any use is a copy-and-repair into a live consumer, which is what the five rules above are.

### And this record was itself refuted (W564)

Five lenses were run against it in isolated worktrees, thirty findings were adversarially verified, and
**eleven survived — five of them about this document.** They are folded in above, each marked where it
sits rather than listed apart, and the corrections are stated with what the first draft said so a later
round inherits the correction rather than the claim.

**FOUR OF THE FIVE WERE THE SAME CLASS, and it is the class this record convicts the archive of:** a
sentence asserting a universal the document did not compute — "no `__init__.py` at any level", "import
only stdlib", "the only module here that does not emit on a no-op", and a mean taken rather than measured.
A record built to catch fabricated figures carried four of its own, and every one of them would have read
as authoritative.

**THE FIFTH WAS WORSE IN KIND AND SMALLER IN REACH:** the headline fabrication quoted for `fitness.py`
was an expression its own call site cannot reach, and the figure derived from it could not arise from the
arithmetic. The verdict and the disposition were unaffected, which is exactly why it is worth recording:
a row can be right about what a module does and wrong about the evidence it cites, and only the citation
gets copied forward.
