# The unattended-session method — forecast, simulate, engineer, align

Written W514 (2026-09-30) for an ~8-hour unattended run, and kept as the reusable method for any future one.
Every figure here is measured from this repository or marked as an assumption. **Section 0 is the repeatable
procedure — start there.** Four scripts hold the mechanism: `plan_night.py` (the plan itself),
`session_forecast.py` (wall-clock capacity), `night_sim.py` (completion probability) and `coupling.py` (which
readers a change must not forget).

---

## 0 · RUN IT AGAIN — the repeatable procedure

Four steps, and only the first is yours.

1. **Tell Claude how many hours and that you are going to sleep.** Capacity is readable only in the app
   (`get_usage`), so it is an INPUT to the plan; if the hours are wrong, everything downstream is wrong.
2. **Claude runs `python scripts/plan_night.py <hours>`.** That regenerates this whole plan from live state —
   measured round cost, the simulated probability of each round completing, where the open work sits, the
   ordering and batching rules, the pre-round checks and the stop rules. It refuses to project at all below a
   five-round history rather than substituting a rate.
3. **Claude reads the generated plan back to you with the committed round count and what each round holds**,
   and you approve or redirect. This is the alignment step: the numbers are computed, the batching is judgement,
   and the judgement is stated so you can overrule it.
4. **You invoke `/loop` with that plan and go to sleep.** Claude self-paces, refreshes the handover's state
   section at every round boundary, and writes the night report at the start of the last affordable round.

**In the morning:** `git log --oneline` is the report, `docs/NIGHT_STATE.json` is the machine-readable status, and
`docs/NIGHT_REPORT.md` says what was left and why. Nothing needs the conversation you slept through.

**The one thing no mechanism covers:** keep-awake prevents idle sleep, never a closed lid. Leave the machine open.

### The instruments, and what each refuses to do
| script | answers | refuses |
|---|---|---|
| `scripts/plan_night.py <hours>` | the whole plan, from live state | to choose the work — it orders candidates and states the batching rule |
| `scripts/session_forecast.py <hours>` | how many rounds fit the hours | to project below a 5-round sample; to pick between two disagreeing history windows |
| `scripts/night_sim.py` | P(≥k rounds complete) | to state one red-suite rate it cannot measure — it shows a range |
| `scripts/coupling.py <paths>` | which files historically change together | to assert coupling for a file with fewer than 4 commits |

Each refusal is the point. An instrument that always answers is the one that reports a false clean — which
happened twice on the night this was written.

## 1 · Measured: what a round of this project actually costs

| quantity | value | how |
|---|---|---|
| round duration, **W490+** | n=8, median **2.05–2.15h**, p75 2.63h, max 3.72h | gap between consecutive rounds' final commits |
| round duration, **W460+** | n=28, median **2.14–2.21h**, p75 3.72h, max 4.87h | same |
| full serial suite | **0.90h** (two runs: 3274s, 3200s) | measured |
| suite share of a median round | **41%** | derived |
| single-test selector | **49.6s** | measured, same tree |

**The correction that makes this honest.** Raw round-to-round gaps read a median of **5.08h** because most gaps
contain the Owner asleep. *An interval is not a duration.* Gaps above a 5h cap are excluded as idle, and the
**19 exclusions are reported, not dropped** — a filtered population that does not say what it filtered is how a
rate becomes a wish. Two independent windows agreeing on the median within 0.06h is why any of this is usable.

## 2 · Simulated: the probability each planned round completes

Empirical bootstrap, 20,000 trials, fixed seed, resampling observed durations with replacement — because round
durations are right-skewed (median 2.14h, max 4.87h) and a normal assumption would understate exactly the tail
that ruins an unattended night. `p_red` is the chance a round needs a second full suite; it is an **assumption,
not a measurement**, so the result is shown across a range rather than at one indefensible value.

| window | p_red | P(≥1) | P(≥2) | P(≥3) | P(≥4) |
|---|---|---|---|---|---|
| W460+ (conservative) | 0.25 | 100% | **90%** | **55%** | 23% |
| W490+ (recent) | 0.25 | 100% | **99%** | **77%** | 29% |
| W460+ | 0.50 | 100% | 87% | 45% | 16% |

**So: commit to 2 rounds (90–99%), expect 3 (55–77%), treat 4 as unlikely (23–29%).** This supersedes
`session_forecast.py`'s `committed_round_count`, which returns 1 by taking the lower of two slow bands and so
compounds two conservative estimates — the simulation shows 2 is safe on either window.

**Biased pessimistic by construction, deliberately:** it does not model a round that turns out to be a decision
(finishes in minutes), and the sample includes the Owner's reply time, so an unattended night may run faster
than its own history.

**The outside view.** My own judgement said "3 rounds, possibly 4". Measured and simulated, that is the
optimistic tail — P(≥4) is 23–29%. Reference-class forecasting against this repo's own record beat the inside
view, and the gap is the size of the optimism bias to expect next time.

## 3 · The constraint, and how it is worked around rather than removed

The suite is the bottleneck: 0.90h fixed, 41% of a median round, with a **65× ratio** to a targeted selector.

- **Exploit:** diff-scoped selector first, one full suite last. W513's failure was reproduced and fixed in 49.6s
  against a 53-minute run; W503 recorded the same at 16s versus 49 minutes.
- **Subordinate:** never start a round that cannot pay one full suite plus contingency.
- **Do NOT elevate.** Parallelising the suite is forbidden for a measured reason — two concurrent runs corrupt
  the shared `memory.json` and UEG ledgers and produce ~40 false failures. The constraint stays.
- **Never skip the full suite.** A selector cannot see cross-test interaction, where this project's hardest
  defects live (an `importlib.reload` splitting a singleton so a route returned `None` one line after a guard set
  the field). **A passing subset is a hypothesis; the full suite is the verdict.**

### Batch size: DORA and the measurement point opposite ways
Small batches reduce cycle time and change-failure rate; here each round boundary costs a fixed 0.90h, so two
extra boundaries cost a round's work. **Resolution: decouple the batch of CHANGE from the batch of
VERIFICATION** — each change small, single-purpose, independently reviewable; one suite amortised over several
*coherent* changes. The honest bound is the **attribution test: if a red suite could not be attributed to one
batched change within one diagnosis pass, the batch was too big.**

## 4 · Change coupling — predicting the second-reader miss before it happens

Mined from 556 commits: logical dependencies, not static imports. `vbs/quality.py` co-changes with
`test_mvp_spine.py` 100%, **`Deliverables.tsx` 67%**, `genesis.py` 58%.

This found a real gap in this night's plan: the FU-160 fix named `quality.py` and `ethical_engine.py` and **not
the page that reads them** — the "fixed one writer, not its reader" class that recurs here by name. Checked:
`Deliverables.tsx` reads framework-level verdicts and `overall`, not the ethical engine's inner dimensions, and
`qmsChip`'s not-assessable branch already omits coverage. **Cleared; the two-file fix stands.** The value is the
cost asymmetry — two greps before, versus a 53-minute suite after. The instrument **refuses** below 4 commits
(`ethical_engine.py` 2, `method.py` 3, `regulator.py` 0) rather than asserting a coupling it cannot support.

## 5 · Hazards as unsafe control actions (STPA)

The controller's actions overnight are *commit*, *push*, *close-row*, *mark-item-done*. Each unsafe version and
its constraint:

| unsafe control action | constraint |
|---|---|
| close a row that is not satisfied | a close names **the state it measured**, never only the change made |
| commit on red | explicit `PYTEST_EXIT=$?`, one diagnosis pass, then stop |
| act on wrong feedback from a guard | refute the guard before the code — W513 was exactly this |
| mark an item done on activity | the ACCEPT clause is the bar, transcribed and guarded |
| push a change whose reader was not updated | the coupling check above, before the fix |

## 6 · Resilience: checkpoint, reversibility, error budget

- **Checkpoint = one round = one commit.** A crash, a sleep or an exhausted budget loses at most the round in
  flight. Alongside it, `docs/NIGHT_STATE.json` holds machine-readable round status
  (`{round, status: planned|in_progress|landed|abandoned, commit, suite, left_undone}`) so resumption is
  deterministic rather than dependent on reading prose.
- **Two-way doors only.** Everything planned is revertible in one commit. Nothing that is not — schema change,
  data migration, store rewrite, anything owner-gated — is in the plan.
- **Error budget: one red suite (0.90h reserved).** A second means stop and write up, not push on.
- **SPC:** p75 = 2.63h is the control limit. A round exceeding it is special-cause — investigate, do not
  accelerate.
- **Atomicity** (`store_lock` + `atomic_write_json`) and **asserted byte-restore** on every blind, because
  interruption tonight is expected rather than hypothetical.

## 7 · Work-type routing (Cynefin) and ordering (WSJF)

*Clear* — the stale-document fixes: best practice applies, batch them. *Complicated* — FU-160: analysable, one
right answer. *Complex* — the tolerant reader across 13 heterogeneous sites: its own row forbids a single
unattended pass, hence five rounds. Applying clear-domain confidence to complex work is the classic failure and
the row predicted it.

**WSJF orders Round A:** the two stale Horizon statements are near-zero duration and unblock five items on
paper — the highest value-over-duration in the queue, so they go first.

## 8 · ETTO, named and bounded

Tonight explicitly trades thoroughness for throughput; that is what batching one suite across coherent changes
*is*. The bound is the attribution test in §3. Safety-II's four cornerstones already exist here under other
names: **respond** = the red-suite stop rule; **monitor** = the four signals in §9; **learn** = the method
register (90 lessons, 43 guarded, third breach auto-escalates to Change Control); **anticipate** = the pre-mortem
in §10.

## 9 · The four signals, with decision rules

| signal | healthy | else |
|---|---|---|
| suite exit code, captured explicitly | `0` | one diagnosis pass, then stop and write up |
| `git status --short` | empty after each round | never start a round on a dirty tree |
| weekly allowance (`get_usage`) | falling as expected | write the night report while capacity remains |
| round elapsed vs p75 (2.63h) | under | do not start a round that cannot finish |

## 10 · Pre-mortem — three of these happened within 24 hours of writing

| how the night fails | mechanism | status |
|---|---|---|
| the lid closes; nothing runs | keep-awake covers **idle** sleep only, never a closed lid — disclosed, not claimed | **unguardable** |
| two suites at once corrupt shared stores (~40 false failures) | WIP limit of 1; fresh isolated store per run | hard rule |
| the tree is edited while a suite reads it (two 50-min runs lost in W507) | measurement only while a run is live | **happened** |
| a guard goes red against correct code | refute the guard first; ask whether the *edit* produced the condition | **happened tonight** |
| a new guard cannot fail | driven red before trusted, restored with an asserted SHA | standing |
| a wrapper masks the exit code | `PYTEST_EXIT=$?` captured, never the wrapper's status | **happened tonight** |
| capacity ends mid-round with no record | night report written at the *start* of the last affordable round | designed in |
| a measurement instrument is vacuous | driven against a known-positive before its zero is believed | **happened twice tonight** |

## 11 · Alignment: three commitments checkable cold in two minutes

1. **`git log --oneline` is the report.** Every round is one commit stating what was measured, what changed, what
   was left. No round exists that is not a commit; nothing is "nearly done".
2. **`HANDOVER_CLOUD.md` §1 refreshed at every round boundary — and only §1**, so a refresh does not burn the
   capacity it exists to protect.
3. **`NIGHT_REPORT.md` written before capacity runs out**, at the start of the last affordable round: what
   landed · what was already satisfied on measurement · what was left and exactly why · what now awaits a ruling.

**Escalation fixed in advance, so it needs no judgement at 04:00:** red suite → one diagnosis pass → stop and
write up, tree clean. Anything whose honest answer is a ruling → parked in `P3.0`, never decided. The six §18
decisions, the OWNER-slotted row and every owner-gated switch → untouched. A round that cannot finish in the
remaining time → not started.

## 12 · What is deliberately NOT done unattended

No suite parallelisation or sharding, no CI changes, no dependency beyond the ruled `pypdf` line, no refactor
whose blast radius exceeds one commit, and no agent fan-out — refuter worktrees cost 162 MB each and once filled
the disk, killing 27 of 45 agents silently. **An unattended night optimises throughput of the existing method,
never the method itself.**
