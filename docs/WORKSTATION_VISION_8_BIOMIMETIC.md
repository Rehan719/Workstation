<!--
  WORKSTATION VISION 8.0 — THE BIOMIMETIC LIVING-ORGANISM NATURE
  A STRATEGIC PLAN UPDATE, derived from the W512 scoping exercise and the Appraisal Cell's own readings.

  STATUS: PROPOSAL, routed Transformation Office → Change Control Agency.
  NOT a plan item, and not a vision amendment. Only the Owner refines the Vision (M-CONCEPT-03); this
  document states what the organism measurably IS, what Vision 8.0 would change, and in what order — so the
  Owner can ratify, reorder or refuse it. Every figure was measured on 2026-09-29 and says where from.
-->

# Workstation Vision 8.0 — The Biomimetic Living-Organism Nature

> **The vision, in the Owner's words.** Inspired by nature's solved solutions in biology and geobio-physical
> systems, Workstation is a digitally-living entity whose organisation structure, resources, workflows and
> cascades mirror living systems. Once established, it is ever self-managing, improving, growing, evolving,
> healing. The 7 biomimetic layers (Genome · Nervous · Immune · Cardiovascular · Respiratory · Musculoskeletal
> · Endocrine), homeostasis loops (immune↔nervous↔metabolic), circadian operation, and a survival instinct make
> it dynamic, adaptive, responsive — and defend itself, learn, and improve: profitability, customer/user
> satisfaction, founder-alignment, and live compliance are all continuously monitored, evaluated, and improved.

---

## 1. The strategic finding

The organism **senses and acts**. It does not yet **regulate, turn over, or select**.

That is the whole of Vision 8.0 in one line, and it is a measurement rather than an opinion. Sensing is strong
(the heartbeat, the immune status, the provenance on every call, the UEG). Acting is strong (the resource
fabric runs real engines; the economy moves virtual WST; the immune system raises a defence and reverts it).
The three deficits are the three things that make a living system *living* rather than merely responsive:

| deficit | what it means | the measured evidence |
|---|---|---|
| **REGULATION** | the loops are open at the control end | both unreached layers are **regulators**. ATP **cannot deplete** by arithmetic (max consumption 0.1 against min production 0.4). The circadian map never reaches metabolism. No cycle setpoint is enforced anywhere |
| **TURNOVER** | nothing removes or replaces its own parts | no apoptosis, no autophagy, no mitosis, no senescence, no death. The life cycle **ends at launch** — it is embryogenesis, not a life cycle |
| **SELECTION** | evolution is impossible by construction | `genome.py` has **crossover and mutation and no fitness evaluation** — its own docstring says so. Variation ✓, inheritance ✓, selection ✗. Darwin needs three |

A system that cannot regulate cannot be *self-managing*. One that cannot turn over cannot be *healing*. One
that cannot select cannot be *evolving*. Those are three of the five verbs in the vision statement, and each
has a precise, measured, buildable cause.

## 2. Where the organism stands, measured

**The seven layers, from the platform's own state table** (`agentic_core/vbs/quality.py`):

| layer | state | reality |
|---|---|---|
| Immune | engaged, contributes value | read into records |
| Nervous | engaged, contributes nothing | signals route in and are dropped |
| Genome | implemented, off the quality path | on the heartbeat as a vital sign |
| Musculoskeletal | implemented, off the quality path | the fabric runs real engines |
| Cardiovascular | **a measurement under an anatomical name** | `100 − cpu_percent`. There is no circulatory subsystem |
| Endocrine | **code exists, unreached — and it is not a controller** | `integral_error` is declared and never accumulated; `dt` is discarded; actions are strings |
| Respiratory | code exists, unreached | `TriadIntegrator`, imported by nothing |

**1 of 7 contributes value.** And the honesty table itself over-claims on the Endocrine row — it calls that file
*"a real PID regulator"*. Correcting that is the first item of the truth-maintenance thrust below, because a
false statement on the surface built to be true is the most expensive kind.

**What is genuinely strong and should not be disturbed:** the substrate (`store_lock` + `atomic_write_json`,
hard-won through three data-loss incidents), the machinery (gateway, orchestrator, the nine native-AI
primitives, the QMS gate), the organs (CCA, Transformation Office, Resource Fabric, Synthesis Lab, Sovereign
Evolution Office, the economy), the clock (a real oscillator with a real zeitgeber and phase-gated work), and
the **germline** — `docs/DELIVERY_METHOD.json`, which is heritable code with variation, selection, inheritance
and mutation pressure, and whose breach counter is functioning adaptive immune memory.

## 3. The five thrusts

Ordered by what unblocks the most, with dependencies stated. **Each names what it is NOT.**

### Thrust A — REGULATION: make energy real and close the loops
The metabolic loop already exists **fully wired**: work → load → ATP → posture → admitted concurrency, with a
survival instinct at `atp < 0.3`. Two coefficients and one unwired input make it inert.

1. Feed the real circadian efficiency (the 1.0 / 0.7 / 0.5 / 0.3 intensity map) into `_update_atp`, which
   passes only 1.0 or 0.8 today. This alone takes minimum production from 0.4 to 0.15.
2. Rebalance the consumption coefficient so sustained load can exceed minimum production.
3. Build **integral control** — the silicate-weathering thermostat's shape: slow, error-accumulating, stable
   over long horizons. Neither the archived nor the live candidate accumulates error, so this is
   *construction*, not connection.
4. Bind one measured flow per biogeochemical cycle to a setpoint, starting with one.

**Not this thrust:** a new budget mechanism. The loop exists. **Risk to manage:** `atp < 0.3` has never once
fired; making it reachable switches on a throttle to serial cognition across every path. It wants a measured
ramp, not one edit.

### Thrust B — COGNITION: make the organelles compute (the gate)
Six cognitive engines of 24 lines each, every one returning a constant, none with a path to a model.
`registry.register` is never called, so `get()` always raises. `cognitive/meta/` holds only `__init__.py`.

**The contract goes first.** `consultation/interface.py` forces an engine to lie three ways: `confidence` is a
required float with no three-state option, `ValidationResult.passed` is a bare bool, and there is **no
provenance field at all**. Build six honest engines against that contract and you get six fabricated
confidences. Then one engine end to end, driven with two different inputs producing two different outputs;
then the other five; then populate the registry. The three meta engines stay **planned** and say so.

**Not this thrust:** wiring the archived nine-engine bootstrap. Two of its three meta engines are simulations.

### Thrust C — CHECKPOINTS: bind progression to conditions, not to elapsed time
The clock paces and does not gate on conditions met. The machinery exists — the five-gate clearance chain —
and is **not bound to the clock**, and **three of its five gates default to pass** (`.get("balanced", True)`,
`.get("risk_score", 0) > 0.15`, `.get("verified", True)`), so an engine returning `{}` clears them. Flip the
three, handle gate 1's missing key as a refusal rather than a 500, record each gate's verdict with its basis,
measure each stage's **own** latency (today `_assert_latency` measures cumulatively from cycle start and only
logs), and bind the chain to the beat as a G1/S-style checkpoint.

**Depends on Thrust B**: three of the five gates consult exactly the three meta engines.

### Thrust D — TURNOVER: give the organism a life cycle with an end
Apoptosis and mitosis are **one coupled mechanism**, not two features — crustal recycling, not two separate
volcanoes. Destruction without creation is decay; creation without destruction is sprawl.

1. A **lineage field** on an entity (it has none today; genomes have one, entities do not) — the precondition.
2. An **entity state machine**: juvenile → mature → senescent → dormant → retired. **Self-service dormancy,
   governed death.**
3. **Apoptosis with conservation**: what an entity held returns to the reservoirs; the record is retained.
   Never auto-retire anything holding unsettled obligations, under a governance hold, named in a ruling, the
   QEP entity, or the last entity in its realm×domain.
4. **Mitosis**: a mature entity may create a subsidiary inheriting its constitution verbatim, funded from the
   parent's own waterfall share, through Change Control.
5. **Meiosis as a candidate, not a birth**: crossover already exists; a recombined constitution is a *new*
   constitution and needs ratification — exactly as a method lesson does.
6. **Autophagy**: the retire-or-relabel discipline made mechanical, proposing removal through Change Control.
7. **Carrying capacity derived** from the metabolic budget, not set.

**Metamorphosis is the test for the Transformation Office**: a transformation that does not *dissolve* what the
previous stage needed is not a metamorphosis, it is accretion. Today the cascade only adds.

### Thrust E — SELECTION: make evolution possible, honestly
1. **Build a user-satisfaction mechanism.** It is one of the four continuous measures in the vision statement
   and it has **no mechanism anywhere** — the only two occurrences in the codebase are a heading in a generated
   document and a hardcoded `1.0` in an unreached module. This gates the rest of the thrust.
2. Build selection so that it **REFUSES** while any of the four measures is unmeasured, exactly as the §11
   compliance screen refuses rather than clears.
3. Permit **negative selection on a hard floor** meanwhile — an entity that cannot meet its §8 obligations or
   fails compliance outright is flagged for review. A floor creates no optimisation pressure toward a proxy.
4. Delete the dead fitness stub that returns `1.0` for every individual.

**Not this thrust:** reusing the venture funding score. Funding selects on **potential**
(outcome-success × value × benefit × feasibility × strategic-fit, already built). Survival must select on
**record**. Conflating them lets a well-pitched entity outlive a well-performing one.

**Not this thrust either:** a rescue channel between entities. Investment between entities is already built
(§4 Stage 4 + FU-300's adjustable arrival share). Rescue is not investment — routing it through a stage whose
stated basis is *competitive selection on potential* would corrupt that basis, and charity has defined
recipients under the faith constitution. **Rescue before selection means nothing ever fails.**

### Cross-cutting — TRUTH MAINTENANCE
Eleven measured rows, led by: the Endocrine basis over-claiming its own code (**Tier 1**); the circadian map
never reaching metabolism; live mocks in the recirculation constructor (an always-approving mutation regulator
at confidence 0.95, an always-True fixpoint verifier); three dead genome stubs; the consultation contract's
missing provenance; a nine-versus-seven disagreement between registry and contract; and a QEP-labelled
`get_fabric_health()` returning `random.uniform(0.9, 1.0)` — **latent**, since no route selects it.

## 4. Sequence and dependencies

```
A (regulation: 2 coefficients, then integral control)
│        └── enables capacity derived from the budget  [Thrust D.7]
B (cognition: contract first, then one engine, then five)
│        └── required by ──►  C (checkpoints: 3 gates, the clock binding)
D (turnover: lineage ► state machine ► apoptosis+mitosis ► autophagy)
E (selection: user satisfaction FIRST, then refuse-until-measured)
```

**A first** — it is the cheapest (two coefficients and one input), it unblocks capacity, and it makes the clock
load-bearing rather than decorative. **B is the gate** for C and, through the existing rulings, for the Horizon
membrane. **D and E are independent of A–C** and may run in parallel with them. **E's first step is the one
thing in the vision statement with no mechanism at all.**

## 5. What Vision 8.0 will be measured by

The vision names four continuous measures. Honestly, today:

| measure | state |
|---|---|
| **profitability** | real, virtual WST — the §4 waterfall, the ledger, the survival instinct at §8→§12, monitored on the beat |
| **live compliance** | real and honest — the screen clears nothing by itself, and since W507 a certifying body can clear a subject while the platform never does |
| **founder-alignment** | weakest. The Chief is a **role**, not a modelled twin, and no action traces to the clause it serves |
| **customer/user satisfaction** | **no mechanism.** Thrust E.1 |

Vision 8.0 is complete when all four are measured, the seven layers each contribute value or say plainly why
they do not, and the organism can be shown — by a guard made to fail first — to regulate, turn over and select.

## 6. Governance

This document is a **proposal**, not a vision amendment. Under the method's first rule the Owner alone refines
the Vision; where the live system differs from it, the difference is the work to do and never a redefinition of
the vision down to capability.

It is filed through the **Transformation Office → Change Control Agency**, which is the same path a method
lesson takes: a candidate is derived, the agency records it, and ratification is the Owner's. On ratification
the five thrusts become plan items and the eleven truth-maintenance findings become register rows.

**Decisions reserved to the Owner** (six, with recommendations already given): what the metabolic budget is
measured in · what an entity may be selected on · whether an entity may create an entity · what a VSB may
retire itself over · whether a rescue channel should exist at all · whether an entity has a carrying capacity
and an end.

## 7. What this plan does not do

It does not claim the organism is alive in any sense beyond the mechanical. It does not propose any faculty
that assesses a person's inner state — **ruling A.9.5** holds that the Fitrah Spectrum is never a measurement
and no AI verdict is passed on a person's spiritual state, and "soul" in this document names only the
invariant the organism answers to: the vision, the constitution and the rulings. It touches no real-money rail;
all economic mechanisms remain virtual WST. It recovers no archived code: of 52 archived biomimicry modules
named almost exactly for the mechanisms this plan builds, those examined are simulations — `apoptosis.py`
sleeps 0.5s and reports a mock 128 MB reclaimed. **Recover the shape, never the code.**

And it does not promise a date. The plan projects in rounds, from one forecaster, and names its weakest input.
