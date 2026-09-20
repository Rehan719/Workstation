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

— driven by the geospheric regulators that already exist in `agentic_core/biomimicry/geospheric/`.
Not a seventh store of invented numbers. That reframing, plus recovering the ant-colony scheduler and
the rest of #6's biomimetic layer from `_archive/`, is what **P3.19** is for.

Proposal #6's protocol tier (MCP · A2A · ACP · FIPA-ACL) is a separate and also real question: this
repository's agents talk through `agentic_core/api/agent_hub.py` (W443), not a protocol stack.
Adopting MCP or A2A is an Owner-level architecture decision, not a recovery, and it is not planned
here.
