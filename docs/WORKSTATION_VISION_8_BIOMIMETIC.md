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
## 8. The third external brief, interrogated (W515)

The Owner supplied an LLM-authored architecture, *"Attempt 4: Executable Governed Developmental Control Plane"*,
with the instruction to review, interrogate, rationalise, verify, discern, refute and collaborate before updating
this plan. **This is the third such brief**, and the precedent is set: `docs/NATIVE_AI_FABRIC_ROADMAP.md`
interrogated an almost identical external brief on 2026-09-27 (W495) and became plan items **P3.20–P3.24**, under
the rule that every "what exists" claim is measured against the working tree by a named command. The same rule is
applied here.

**Method.** Six verification lenses over the live tree — the proposed primitives, the brief's claimed gaps,
collisions with existing rulings, duplication of existing machinery, the cognitive engines and model tiers, and
the brief's own soundness — each finding then given to an independent agent instructed to refute it and to default
to *not confirmed* unless it reproduced the finding itself. **48 agents, 0 errors. 72 findings raised, 42 carried
to refutation, 28 survived.**

**The distribution is the verdict:**

| what the assessment found | count |
|---|---|
| **DUPLICATES_EXISTING** — the brief's new name for machinery already here | **21** |
| EXISTS_DORMANT — present, nothing calls it | 12 |
| **COLLIDES_WITH_RULING** | **11** |
| ABSENT — genuinely not here | 9 |
| FALSE_ABOUT_REPO — a claim about this repository that does not hold | 8 |
| EXISTS_AND_RUNS | 7 |
| **SOUND_AND_NEW** | **4** |

**THE LIMIT OF THIS ASSESSMENT, stated because it bounds every attribution above.** The verifying agents were
given the brief's *subject matter* but not its full text, so their verdicts are reliable about **this repository**
and about **the named subsystems** — and are *not* quotations of the brief, nor evidence about what its own
wording does or does not avoid. One agent said so unprompted: *"Do not read any finding above as a quotation of
the proposal."* That is a defect in how the verification was commissioned, not in the verification. Where this
section credits or refuses an idea, it refuses **the named subsystem against the existing path**, which is the
question that decides what gets built.

### 8.1 What it confirmed, at higher resolution than §2

- **The metabolic term exists, runs, and cannot fail.** `atp_simulator.py` is a process-wide singleton driven from
  `biobus.py:185` and imported by roughly forty live modules. `biobus.py:47-78` *computes* `can_deplete` and gets
  **False**; `biobus.py:287-303` names every threshold written against the term — the economy's reserve raise, the
  heartbeat's `self_recovery` and `metabolic_throttle` — as unreachable *"for the whole life of the process"*; and
  `ResourceFabric.tsx:535` already tells the viewer it *"does not fall, so it never limits a run"*. The platform is
  honest about it end to end. **Thrust A is therefore not a new build but a correction to a running instrument.**
- **Eight of the eleven `agentic_core/biomimicry/` subpackages contain no files at all.** A fabric cannot be
  layered onto empty directories, and no brief that claims this layer "already defines" a morphogen stack has read
  the tree.
- **The circadian schedule exists twice, byte-identically** — `biobus.py:92` and `heartbeat.py:111`. The work is to
  collapse them into one and make the boundaries data; adding a third abstraction on top would make it worse, and
  the *fix every writer* class applies — both copies move together or the phases disagree.
- **A constitution already runs as CODE**, not as a document: the gaas.v5 policy gate and interceptor at eight live
  sites. Its scope is written into the repository itself — *"intent + domain only … the delivery's content was NOT
  screened"*. The authored constitution document is archived, and `genome_engine.py` is **deliberately** unwired
  with a guard asserting its engine stays `None`.

### 8.2 What folds into the five thrusts — no new phase, no new tree

- **Thrust A — REGULATION** gains **EntityState as a first-class object**: a control loop cannot be closed without
  state estimation, and that is precisely the open end this plan names. It also gains **pressure-as-signal** —
  load that *changes behaviour* rather than a CPU number wearing an anatomical name, which is what the
  Cardiovascular row is today. **Not under the brief's name:** see §8.4.
- **Thrust B — COGNITION** gains the one thing verification marked genuinely new and adoptable: **content
  screening inside the existing gate**, passed as arguments into `intercept()` with rules in the policy gate,
  *not* as a parallel checkpoint subsystem. The gate already discloses that it does not screen content; closing
  that is new capability rather than a rename.
- **Thrust C — CHECKPOINTS** gains **quorum thresholds** as the shape of "bind progression to conditions, not to
  elapsed time" — a stated threshold over evidence or agreement, rather than a timer.
- **Thrust D — TURNOVER** gains the precise **apoptosis / autophagy distinction** (terminate the component versus
  recycle what it accumulated), **TTL and dissolution on an assembled swarm**, and the clean ladder
  **capability → agent → swarm → entity instance**, which gives turnover something with a definite end.
- **Thrust E — SELECTION** gains what is, in this reviewer's judgement and not from the verification, the sharpest
  thing in the brief: **shadow → canary → golden-suite gate → promote-or-roll-back is a fitness function**. This
  plan's §1 records that `genome.py` has variation and inheritance and no selection. A release gate that admits or
  rejects a variant on measured evidence is the missing third leg, and it is nearly all already built in Change
  Control.

### 8.3 What is refused, and on what ground

- **A parallel `src/idbo/` tree beside `agentic_core/`.** One organism, one home. A second tree is the
  two-records-disagreeing defect at directory scale.
- **Any field that grades a PERSON.** A cognitive-load signal, a confidence score about a user, or an
  intention/value-alignment figure computed about someone runs into **ruling A.9.5**. The test is one question —
  *is the subject a person?* Grade the request; never the human.
- **The routing score as specified.** Its terms are not commensurable: an affinity × concentration product, a
  historical frequency, a density bonus and four subtractive penalties summed with no units, no normalisation and
  no calibration path. Ranking possibilities by probability also collides with the prospection invariant
  (*"ranked by nothing, ever"*) and with the one-forecaster rule; `docs/CAPACITY_FACULTY_MODEL.md` §2 already drew
  that line and it is not re-litigated here.
- **A content-bearing shared blackboard.** Marks that carry request or user content re-introduce exactly the
  cross-request defect that `augment=False` closed. A stigmergic mark that is **not content** — a counter, a path
  weight, an item id — may be admissible, and that is the line to build to.
- **Any gate that clears.** Three states with a basis and a coverage field, where only measured coverage may
  clear. A lexical or keyword screen may flag and escalate; it may never certify.
- **The biomimetic citations as authority.** The brief's own opening states its sources *"returned loading errors
  rather than article bodies"* and are treated as bibliographic anchors. Keep the vocabulary; take the
  engineering; refuse the grounding as load-bearing.
- **The engine response contract as a foundation.** A required numeric confidence forces an engine that cannot
  judge itself to invent a figure — which is the measured cause of the fixed literals already in the tree, and is
  registered as a row rather than adopted.

### 8.4 Two naming hazards, both measured

- **"Constitution" is taken.** It names a running gate whose scope is deliberately narrow. A new object under that
  name would be read as governing content, which the existing one explicitly does not.
- **"Mechanical" is taken, and more dangerously.** Throughout this repository it means *mechanically checkable* —
  it is the vocabulary of the change-control gate's one tooth (`change_control.py:782`) and of the method
  register's `mechanically_enforced`. A primitive named for mechanical *state* would be misread by every existing
  reader. Adopt the concept; give it a name that does not collide.

### 8.5 What this adds to the plan

No new thrust and no new phase. Five thrusts gain named content; six refusals are recorded with their grounds so a
later round cannot quietly adopt them; two naming hazards are recorded; and the collapse of the duplicated
circadian schedule joins the truth-maintenance work. **The brief's value was not its architecture — 21 of 72
assessments found it renaming machinery that already exists — but its pressure on five specific open ends, four of
which this plan had already named and one of which (content screening in the gate) it had not.**
