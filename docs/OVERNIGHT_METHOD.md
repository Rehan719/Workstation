# The unattended-session method

For working a long stretch — a night, a weekend — with no Owner in the loop, and for generating that plan
repeatably rather than improvising it each time.

**This document contains no measured figures, deliberately.** W514's adversarial audit confirmed 43 findings
against an earlier version of these artefacts, and the largest single class was a figure typed into prose in more
than one place: the suite cost carried at two different values by two scripts, its share of a round stated two
ways in two documents, a best-case selector ratio presented as typical, and a confidence restated as the wrong
odds. A constant with two homes has no home. (The specific values are in the commit that removed them, not here —
a document must not quote the literal its own rule forbids.) **So every number lives in code and is printed by running the instrument.**

Where this document and the instruments disagree, the instruments are right and this document is out of date.

---

## 0 · Run it — four steps, only the first is yours

1. **Tell Claude the hours available and that you are going to sleep.** Capacity is readable only in the host
   app, never from a script, so it is an INPUT to the plan; if the hours are wrong everything below is void, and
   the generated plan says so at the top.
2. **Claude runs `python scripts/plan_night.py <hours>`.** That regenerates the plan from live state: measured
   round cost with every exclusion itemised, the simulated probability of each round completing, the committed
   and expected round counts, where the open work sits, the ordering and batching rules, the pre-round checks,
   the stop rules, and how the night routes through Workstation.
3. **Claude reads it back with the committed count and what each round holds**, and you approve or redirect.
   The counts are computed; the batching is judgement; the judgement is stated so you can overrule it.
4. **You invoke `/loop` with that plan and sleep.**

**In the morning:** `git log --oneline` is the report, `docs/NIGHT_STATE.json` the machine-readable status,
`docs/NIGHT_REPORT.md` what was left and why. Nothing needs the conversation you slept through.

**The one risk no mechanism covers:** keep-awake prevents idle sleep, never a closed lid. Leave the machine open.

### The instruments, and what each refuses to do

| script | answers | refuses |
|---|---|---|
| `plan_night.py <hours>` | the whole plan, from live state | to choose the work — it orders candidates and states the rule |
| `night_sim.py` | P(≥k rounds complete), and the committed/expected counts | to state one red-suite rate it cannot measure; to hide what its filters excluded |
| `session_forecast.py <hours>` | wall-clock capacity and the cost of round boundaries | to project below a minimum sample; to let a worst case be read as the commitment |
| `coupling.py <paths>` | which files historically change together | to assert coupling for a file with too few commits |
| `_session_measured.py` | the measured constants, with each one's basis | — it is data, and it is the only home for these numbers |

**Each refusal is the point.** An instrument that always answers is the one that reports a false clean — which
happened twice on the night this was written.

---

## 1 · It runs THROUGH Workstation, not beside it

The canon's own instruction (`WORKSTATION_IDBO_WHOLE_VISION.md`): *"the organism delivers its own transformation
through its own org: dogfood is the design, not an afterthought."* So each round submits its change to
`POST /api/v1/cca/submit` and carries the returned `cca_id` in its commit message, putting the round under the
platform's arms-length agency rather than under a convention in a document.

The verified cascade, what was measured to work, and the one gap that blocks full integration are in
**`docs/CAPACITY_FACULTY_MODEL.md` §8–§9** — pointed at, not repeated, because two copies of a structure drift.

**The bootstrap, and it is the point.** Workstation cannot yet hold this plan: no commitment, confidence,
variance, budget or capacity field exists anywhere in the change record, at any depth (**FU-313**, verified by
recursive search). So the first round builds that field, and from the second the plan lives in Workstation
instead of in a file. The process's first act is to make the platform able to host it.

---

## 2 · The method's rules live in the register, not here

The rules earned by this work are lessons in **`docs/DELIVERY_METHOD.json`**, group `session`. That is not
filing: a lesson there reaches `GET /api/v1/method`, `POST /api/v1/method/check` (so a change is checked *before*
it is made), the breach counter that escalates a third breach to Change Control, and the `method_check` that
`/transformation/orchestrate` already returns. **A rule in the register is enforced by the organisation; a rule
in a markdown file is decoration.**

Read them with `GET /api/v1/method` or from the register directly. In summary, each earned by a defect recorded
beside it: a claim that the method is trustworthy must itself be tested · no figure is restated in prose · an
exclusion must justify itself against what it excluded · one rule owns the committed figure · a probability about
self is a measurement but a probability about another's decision is a fabrication · capacity is an input ·
amortise one verification over coherent changes, bounded by the attribution test · one red-suite error budget ·
never start a round that cannot finish · a commitment carries its confidence and its variance.

---

## 3 · The three loops

1. **Inner — exists.** Defect → lesson → guard → breach counter → Change Control escalation at the third breach.
   It has fired on this project's own repeated mistakes.
2. **Middle — FU-313.** Commitment → delivery → **variance** → the next capacity measurement. Without it a
   forecast can drift forever, because nothing compares promised with delivered.
3. **Outer — the instrument audit.** Adversarial refutation of the instruments themselves, by agents that must
   reproduce a finding before it counts. On its first run it raised findings against every artefact here and
   refuted roughly a quarter of them, which is why the verify stage exists.

The outer loop is what caught the two findings that mattered, and neither would have survived re-reading: a
filter that discarded real rounds while reporting only a count, and a validity claim resting on two windows that
were nested rather than independent. **Both were claims about the method's own trustworthiness, which is the
class a method document is least able to audit in itself.**

---

## 4 · Engineering, in one place

**The constraint.** The full suite is the bottleneck and is fixed per round; a diff-scoped selector is far
cheaper. So: selector first on the diff, one full suite last on the final tree, with the process exit code
captured explicitly rather than read off a wrapper. The constraint is **worked around, never removed** —
parallelising the suite is forbidden for a measured reason, because two concurrent runs corrupt the shared
ledgers. And a selector never replaces the full run: it cannot see cross-test interaction, where this project's
hardest defects live. **A passing subset is a hypothesis; the full suite is the verdict.**

**Batch size.** Small-batch guidance and a fixed per-round verification cost point opposite ways. Decouple the
batch of CHANGE from the batch of VERIFICATION: each change small, single-purpose and reviewable; one suite
amortised over several *coherent* changes. The bound is the **attribution test** — if a red suite could not be
attributed to one batched change within one diagnosis pass, the batch was too big.

**Hazards as unsafe control actions.** The control actions are *commit*, *push*, *close-row*, *mark-item-done*.
A close names the state it measured, never only the change made. No commit on red. Refute a guard before the
code it accuses. An item closes on its ACCEPT clause, not on activity. And check the readers a change must not
forget, with `coupling.py`, before making it.

**Resilience.** One round = one commit, so a crash loses at most the round in flight. Two-way doors only:
nothing whose blast radius exceeds one revert. Atomic writes under lock, because interruption is expected rather
than hypothetical. One red-suite error budget. A round exceeding the p75 duration is special cause — investigate,
do not accelerate.

**The four signals, checked at every round boundary:** the suite's own exit code · `git status --short` empty ·
the allowance falling as expected · elapsed against p75.

**Pre-mortem.** The failure modes, with the mechanism for each, are in `CAPACITY_FACULTY_MODEL.md`. Several of
them have actually happened here, which is what makes the list worth keeping.

---

## 5 · Alignment — three commitments, checkable cold in two minutes

1. **`git log --oneline` is the report.** Every round is one commit stating what was measured, what changed, what
   was left. No round exists that is not a commit; nothing is "nearly done".
2. **The handover's state section is refreshed at every round boundary — and only that section**, so a refresh
   does not burn the capacity it exists to protect.
3. **The night report is written BEFORE capacity runs out**, at the start of the last affordable round. A report
   written after the budget is gone is the one report that cannot be written.

**Escalation, fixed in advance so nothing needs judgement at 04:00:** red suite → one diagnosis pass → stop,
write up, tree clean. A second red suite → stop. Anything whose honest answer is a ruling → parked, never
decided. Owner-gated switches and Owner-reserved decisions → untouched. A round that cannot finish → not started.

---

## 6 · What is deliberately NOT done unattended

No suite parallelisation or sharding, no CI changes, no new dependency beyond one already ruled, no refactor whose
blast radius exceeds a single commit, and no agent fan-out — refuter worktrees are expensive and have filled the
disk before, killing most of a fleet silently. **An unattended night optimises throughput of the existing method,
never the method itself.**
