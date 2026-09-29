# Modelling the unattended-session method into the growing tip

Written W514 (2026-09-30). **This is a MODEL. Nothing in it is built**, and the part that changes the growing tip
is not mine to ratify — see §7. It is written because the mechanism built tonight
(`scripts/plan_night.py`, `session_forecast.py`, `night_sim.py`, `coupling.py`, `docs/OVERNIGHT_METHOD.md`) turns
out to be a general organ rather than a one-off convenience, and the place it belongs is already occupied by
something that deliberately refuses to do part of its job.

---

## 1 · What the mechanism actually is, abstracted

Strip the overnight framing and four invariants remain:

1. **Measure your own throughput from your own history**, correcting for the fact that an *interval* is not a
   *duration* — and report what was excluded.
2. **Simulate what fits the resource you actually hold**, as a distribution rather than a point, and refuse to
   project below a minimum sample.
3. **Commit to a bounded scope** at a stated confidence, with a separate expected figure, and fixed stop rules
   decided in advance so no judgement is needed under pressure.
4. **Checkpoint durably and report so an absent principal can verify cold** — artefacts, not narration.

That is not a session trick. **It is what any autonomous entity must do when it holds finite resources and its
principal is not watching** — which is the definition of a VSB entity operating between Owner reviews. The
mapping is structural, not metaphorical.

## 2 · THE COLLISION — and it must be resolved before anything is built

The obvious home is the Appraisal Cell's temporal spine (`retrospection → observation → prospection`,
`api/method.py:1591`). It is the wrong home as stated, and the reason is written into the code:

> `_prospect()` — *"PROSPECTION: the branches, each with its assumption. Ranked by nothing, ever. A possibility
> given a probability has been turned into a prediction, and this platform has exactly one forecaster. So this
> enumerates and refuses to order."*

`night_sim.py` does exactly what that forbids: it attaches probabilities to possibilities (P(≥2 rounds) = 90%).
Bolting it into prospection would break a designed invariant and would do it quietly, since the function would
still return branches.

**The resolution is that these are two different classes of claim, and the distinction is load-bearing:**

| | prospection's branches | the capacity figure |
|---|---|---|
| about | what the **Owner** or the plan will decide or deliver | the executing system's **own throughput** |
| involves agency | yes — a person's decision, an item's outcome | no — a measured physical property of the machine |
| a probability here would be | **a prediction about a person**, which this platform refuses | a rate measured from the system's own history |

So: a probability about **self** is a measurement; a probability about **another's choice** is a fabrication. That
line is why `_prospect` is right to refuse and why the capacity figure is nonetheless admissible.

**Therefore: a NEW faculty, not an extension of prospection.** Prospection may *consume* it as a stated
assumption — "at the measured throughput, the branch where the gate clears needs N rounds" — while still
enumerating rather than ranking. The capacity faculty answers only ever about itself.

## 3 · Where each piece lands

### 3.1 The Appraisal Cell — a **CAPACITY** faculty beside the spine
A fourth temporal function, distinct from the three: retrospection reads what happened, observation reads what
is, prospection names what could be, **capacity says what this organism can complete before its principal next
looks.** Serves `{throughput_measured, resource_held, committed_scope, confidence, refused_because}` and refuses
below the minimum sample exactly as `session_forecast.py` does.

It must NOT be called a forecast. `plan_followups.forecast()` is the one forecaster of the plan and projects in
rounds, never dates. This measures wall-clock against a held resource. Two questions, two sources, neither
restating the other — the same separation already enforced between `/method/forecast` and
`/api/v1/plan/followups`.

### 3.2 The Transformation Office — the organ that produces the bounded commitment
The Office is the growing tip's planning organ, and `plan_night.py` is already the shape of what it should do
per cycle: read live state, measure cost, simulate what fits, order candidates by value-over-duration, and
**refuse to choose the work** — emitting candidates plus the rule rather than an asserted plan. Generalised, a
transformation cycle gains a *commitment* with a confidence and a stated scope boundary, instead of an
open-ended intent.

### 3.3 The Change Control Agency — the stop rules ARE arms-length governance
`transformation_orchestration.py:371` already submits to `submit_change`, so the seam exists. What the night
method adds is a **breach of a commitment as a reviewable event**, in the CCA's existing risk classes rather
than a second governance:

| night rule | CCA shape |
|---|---|
| red suite → one diagnosis pass → stop | an andon event; tier 0–1, applied and logged |
| a second red suite → stop (error budget spent) | tier 2, applied AND recorded as a change |
| scope committed at 85% was not delivered | a recorded variance with its measured cause, not a silent carry-over |
| the attribution test failed (a red suite could not be attributed to one batched change) | **a review criterion**: the batch was too big, and that is a method finding, so the existing breach counter applies — third breach auto-escalates |
| anything whose honest answer is a ruling | parked, never decided — already the `P3.0` mechanism |

The attribution test is the genuinely new governance content: it is an objective, checkable bound on how much
change may share one verification, and nothing currently states one.

### 3.4 The VSB entity — and a measured opportunity worth naming
Each entity would carry its own capacity faculty, measured from **its own** history rather than the platform's.
Two consequences:

- **It fixes a real defect rather than adding a feature.** `organism/biobus.py:62` computes
  `can_deplete = max_consumption > min_production`, which with `atp_simulator.py`'s constants is `0.1 > 0.4` —
  **False**. The §8 organism therefore declares an energy model **that cannot run down**, and the honest field
  already says so. Tonight's error budget is a budget that *can* be spent: one full re-run of a 0.90h suite out
  of a stated 8h. Grounding the organism's energy story in a measured, depletable budget replaces a simulator
  that cannot deplete with one that can — and the existing `can_deplete` field is exactly where the change
  would show.
- **The genome becomes the right home for the parameters.** Error budget, confidence threshold for a
  commitment, minimum sample before projecting, and the stop rules are heritable entity settings — the same
  place `review_gates` already lives — so a spawned entity inherits its parent's discipline rather than
  re-deriving it.

### 3.5 Sovereign Evolution / BTO
`sovereign_evolution.py` already returns `change_control_handoff` with `requested` / `directives_considered` /
`met_the_rule` / `submitted` and the rule verbatim. A capacity figure gives self-improvement a **budget** it
currently lacks: how much of its own change it can propose and verify before the next review, rather than an
unbounded directive list.

## 4 · The loop, once assembled

```
capacity(resource held)  ──▶  Transformation Office: bounded commitment (scope, confidence)
        ▲                                   │
        │                                   ▼
   retrospection ◀── variance ───  execute with fixed stop rules
   (what the last                          │
    commitment cost)                       ▼
                              CCA: breach / variance / ruling parked
```
Retrospection closing the loop is the point: **a commitment's variance is the next capacity measurement's input.**
That is how the figure improves rather than drifting, and it is why this is an organ and not a report.

## 5 · The outside view, recorded against myself
My judgement said "3 rounds, possibly 4". Measured and simulated, 4 is the 23–29% tail; 2 is the 90–99% commit.
**Reference-class forecasting against this repository's own record beat the inside view**, and the size of that
gap is the optimism bias any future estimate here should expect. That is the single strongest argument for the
faculty existing at all: the organism's own confident judgement was measurably wrong in a knowable direction.

## 6 · What this must never become
- not a second forecaster — it never restates the plan's rate, and it never emits a date;
- not a probability about a person's decision — §2's line is the whole discipline;
- not a promise: a commitment at 85% means roughly one night in seven misses, and that must be said where the
  commitment is read, not in a footnote;
- not a reason to skip verification — the constraint is worked around, never removed, and a passing subset
  stays a hypothesis while the full suite is the verdict.

## 7 · Status, and what is the Owner's
**Nothing here is built.** The pieces divide cleanly:

- **Buildable without a ruling** (they only add a measurement that refuses when it cannot measure): the capacity
  faculty beside the spine, and the attribution test as a recorded review criterion.
- **Requires the Owner**, because it changes the growing tip and the organism's own model of its energy:
  grounding §8's ATP in a depletable measured budget; putting the budget, confidence threshold and stop rules in
  the **genome** so they are inherited; and treating a missed commitment as a CCA variance event.

The second group is a change to how Workstation governs itself, which is precisely the class the plan reserves
to the Owner. It is recorded here and parked, not proposed as settled.
