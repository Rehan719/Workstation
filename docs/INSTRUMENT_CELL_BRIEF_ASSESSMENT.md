# The "Biomimetic Digital Cell / Growing Tip" briefs — assessed against the tree

Received from the Owner 2026-10-09 (late): two versions of one external-LLM implementation brief, with the
instruction to review, verify and refute it as before, and to observe, record and act on any useful insight.
Measured against the working tree at W639 (parent 375c5ffb). Neither brief's author had read the repository;
the first says so, the second read the README only. This is the fifth external brief assessed
(see docs/OGE_HAIRMS_BRIEF_ASSESSMENT.md for the fourth).

## 1. What the briefs ask for, in one sentence

Given an objective, choose the smallest sufficient set of registered capabilities, run them through the
existing runner, verify the result against stated criteria, and try a declared alternative when one fails —
all inside the existing governance, with nothing reported that was not measured.

## 2. What is already built (so must not be built again)

| The brief asks for | What the tree has | Where |
|---|---|---|
| A registry of capabilities | 41 registered resources, each with id, class, capability tags, parameters, endpoint, usage areas | `agentic_core/api/resource_fabric.py` `_REGISTRY` |
| A composition preview before execution | `POST /compose/simulate` models a configuration, QMS-gates the plan and projects organism capacity | same file, `_simulate_configuration` |
| Execution through real engines | `POST /compositions/{cid}/run`; every real resource passes one choke point | `_run_real_resource` |
| Distinct outcomes, never "ran" for a read | `outcome`: produced, read, assessed, raised, no_calls_ran, specified — decided per run | `_resource_outcome` (W491) |
| "Not assessable" distinct from pass | tri-state `commit_ready` (None when the gate could not assess) | W449 / W475 |
| Run records and provenance | composition runs persisted and listed | `GET /compositions/runs` |
| Admission by resource pressure | `homeostasis.project()` on preview; homeostasis governs at run time | `agentic_core/ai/native/homeostasis.py` |
| Governance, Change Control, owner switches | exist and are never touched by a round | plan, rulings |
| Verification instruments stating their coverage | the fidelity audit refuses to render without coverage (W638) | `scripts/render_fidelity_ledger.py`, `audit_surface_census.py` |

Every named path in the second brief exists. `CLAUDE.md` does not (the brief says to read it).

## 3. What is absent — the real work

Measured, not inferred:

1. **Nothing maps an objective to resources.** `ComposeRequest` takes `resource_ids` from the caller. A person
   picks; the platform never proposes. This is the brief's core and it is true.
2. **A resource declares no contract.** Capabilities are free-text tags; parameters are type-name placeholders
   (`"str"`); there is no input/output shape, no prerequisite, no permission requirement, no cost.
3. **A resource declares no availability.** Whether it can run now (its engine importable, its store readable,
   the local model tier present) is discovered only by running it and reading `raised`.
4. **A composition is a list, not a graph.** No dependency or binding between stages beyond order.
5. **No acceptance criteria.** A run is QMS-gated as text; nothing states what the objective required and
   whether each requirement was met, unmet or not assessed.
6. **No alternative after a failure.** A resource that raises is recorded as raised; no code path in the
   fabric selects another in its place.
7. **No per-run budget** beyond a per-call timeout: no cap on stages, attempts or elapsed time.
8. **The verification scripts are not instruments in any registry.** 68 file names under `scripts/` look like
   audits, gates, scans or checks (a name count, not a classification); none declares what it covers in a
   common form, and W638's coverage rule applies to one of them.

## 4. Refuted, or refused

- **"Growing Tip" as the name.** The plan already uses "growing tip" for the plan's own active edge (the queue
  the round reads — P-item record, W-rounds). A second meaning would make a ruled term ambiguous. The Owner's
  own words for this work are "Instrument Cell"; that is the name.
- **The seven-organ model as architecture** (membrane, nucleus, cytoplasm, ribosomes, mitochondria, autophagy,
  cell division, mutation). The organism already has its own named systems, and the Owner ruled on 2026-10-09
  (evening) against adopting an external brief's vocabulary. The responsibilities are kept; the organ names
  are not. One exception is already in the tree and stays: immune, homeostasis, metabolic.
- **A new eight-state instrument lifecycle and a six-word truth vocabulary** (PASS, FAIL, REVIEW, NOT_ASSESSED,
  SKIPPED, ERROR). The tree has an outcome vocabulary decided from what happened (section 2). A parallel one
  is the "field's meaning belongs to its readers" defect in advance. What is missing is extended in place:
  an outcome for "not attempted — unavailable" and one for "not attempted — refused".
- **Three new architecture documents plus an ADR.** One assessment (this) and the plan item. The repo cut its
  docs from 49 to 14 for a reason.
- **A scalar cost function** (`execution_cost + latency_cost + complexity_cost + …`). No term is measured
  today. Selection is by explainable rule instead: covers the requirement, is available, fewest resources.
- **"Candidate instrument generation", "mutation", "selection", "cell division", self-promotion (briefs' Level
  B and C, phases 4–6).** Not scheduled. It is generated code entering the runtime, which is Change Control's
  subject and the Owner's decision, and nothing in sections 3.1–3.7 needs it.
- **"Reuse memory" as a new store.** Saved compositions already are the reusable record. What is missing is
  the re-check before reuse (availability now), which falls out of 3.3.
- **A new API family and a new page.** The fabric's routes and its page are extended.
- **"Learning" that tunes selection from past runs.** Refused for now: with a deterministic floor serving most
  output, run "success" is not a quality signal, and tuning on it would optimise for not raising.
- **Performance metrics** (selection precision, false-negative rate). There is no ground truth to measure
  them against; publishing them would be a number with no basis.

## 5. What the briefs get right, and is adopted

- The stated order of work: one read-only vertical slice first, expanded only after it is demonstrated.
- "An instrument is not available because it appears in a catalogue."
- "A model's recommendation is not an authorisation"; planning, preview and execution kept distinct.
- "Reuse the structure of a successful assembly, not its old result as proof."
- "Do not retry an unchanged failing plan"; bounded attempts with a recorded reason.
- "The absence of findings is meaningful only when coverage has been demonstrated" — already ruled (W638).
- Smallest sufficient set as the objective, not most resources. The fabric today rewards neither.
- Stop after the first slice for review before any adaptive behaviour is extended.

## 6. Insight acted on beyond the item itself

- **Availability may be a defect class the audits find one surface at a time** — a surface offering a
  capability that cannot run here. I have not counted how many v14 rows are of this kind; counting them is the
  first step of clause 1, and a declared, checked availability per resource would close the class at the
  registry instead of per page.
- **The verification scripts deserve the coverage rule W638 gave the audit.** Recorded as a follow-up, not as
  part of the item: each script that reports "ok" states what it examined.
- **The brief's lifecycle exposes a present gap:** a composition whose resource cannot run is still called
  `commit_ready` if its text passes. Recorded as a follow-up to measure.

## 7. The plan item (chartered next round)

**THE INSTRUMENT CELL — the fabric proposes, checks and adapts; a person still decides.** Built in the
resource fabric, on its registry, runner, store, routes and page. Clauses, in order, each driven red:

1. **Declared and checked availability.** Every registered resource declares what it needs to run and a check
   that reads it now; the registry and the page show available / unavailable with the reason / not checked.
   No resource is "available" by default.
2. **A declared contract.** What each resource needs as input and what it yields, in the registry's own shape;
   a registration that omits it is refused at import.
3. **Requirements from the objective, stated.** The caller's objective plus an explicit list of required
   capabilities and acceptance criteria — supplied by the person or proposed and shown for confirmation.
   Nothing is inferred silently; with no model served, the proposal says it is a tag match.
4. **A proposal, not a run.** `propose` returns the smallest available set covering the stated requirements,
   the rule that chose each resource, every requirement nothing covers, and what was excluded and why. It
   saves nothing and runs nothing.
5. **Verification against the stated criteria.** Each criterion ends met / unmet / not assessed, with the
   evidence it was read from; "not assessed" never counts as met.
6. **One bounded alternative.** When a resource raises or is unavailable at run time and a declared equivalent
   exists, it is tried once, recorded with the reason; otherwise the run says what is missing. A cap on
   attempts and stages is enforced before execution.
7. **The page shows all of it:** proposed versus executed, attempted / not attempted, criteria and evidence.

ACCEPT: an objective whose requirements one resource covers is proposed one resource; an unavailable resource
is never proposed and says why; an uncovered requirement is named, not papered over; a forced failure produces
exactly one recorded alternative attempt and then stops; no Owner switch, governance rule or generated code is
touched.

NOT IN THE ITEM (and why): generated instruments, promotion, tuning from history, a second registry, a second
runner, new documents, the organ vocabulary — section 4.

## 8. For the Owner

Nothing here needs a ruling to start; clauses 1–5 are read-only or preview-only. One decision will arise
before clause 6 ships: whether an automatic alternative attempt is acceptable without a person confirming it
each time (my recommendation: yes, once, for resources that only read or compose; never for one that writes).

## 9. Addendum (W640): three external "current-state reviews" of W639, assessed

Received from the Owner on 2026-10-09 after W639 was pushed: three regenerated reviews by an external model
that read PR #358 and the public README. Checked against the tree and the register, not taken on description.

**True, and already recorded.** The coverage figures (239 of 552 routes, 23 of 55 pages, six regions at the
cap, 46 unlisted); that v14 does not count toward the stopping rule; that the wrapper-as-request class
persists in untouched callers (the reason for W640's floor change); that the Stripe roll is done and the
real-money switch is off; that nothing was deleted in the quarantine; every register row the reviews name
(the parallel stall, the skipped beat, the text-scan guards, the facility lifecycle, the top-level `core/`
lead, the deferred constraints review) exists and is open, each on a plan item.

**True, and NOT stated plainly in the plan until now — acted on:**
1. **Ledger v14 measured the tree before W639's fixes.** The run record names 375c5ffb (W638). W639's four
   fixes, and everything in W640, have been through the suite and their own guards but through NO audit. The
   plan now says so beside the v14 record, and the next audit's record must name the commit it booted.
2. **The counts are in different units and nobody had written the mapping.** 60 finding records = 27 tier-1 +
   16 tier-2 + 9 tier-3 + 8 delivered. 49 register rows = 27 + 16 (one per tier-1 and tier-2 finding) + 6
   (the 9 tier-3 findings grouped one row per region, as ruled). Written into the plan.
3. **"Each stating its coverage" has no threshold.** The stopping rule requires a stated coverage and says
   nothing about how much. A zero run that exercised a tenth of the routes would satisfy its letter. This is
   the Owner's to define; registered as a decision with a recommendation.

**Refuted.**
- "v13: Tier-1 10, Tier-2 7" (first review's table). The retained v13 ledger's own table reads Tier-1 12.
- "Checks could not be confirmed green" — true when written; all five passed and PR #358 merged as 94b425ee.
- The reviews' 20-, 20- and 29-row "genuine gap" registers. Each row I checked restates a plan item or an
  open register row under a new id. Adopting them would create a second register beside docs/FOLLOWUPS.json;
  the three registers also disagree with each other on numbering. Not adopted.
- "Render configuration exists so the backend path is partly there": `render.yaml` exists; nothing in the tree
  records a deployment from it. Unchanged: no deployment is claimed.

**A recommendation I did not follow, and why.** All three reviews advise not starting the Instrument Cell
before the truth work. The Owner's instruction of the same evening is to complete it. The Owner's instruction
governs. The two are less opposed than the reviews assume: the first thing the cell's availability check
measured is a truth defect — registered resources the fabric cannot run (section 10).

## 10. What the first measurements found (W640)

Read from source before anything was built: 41 resources are registered; the fabric's real-resource handler
has a branch for 38; one more (the organisation cascade) is run by the composition runner itself. **Two —
`vsb_spawn` and `genesis_establish` — are registered, selectable and described as spawners, and composing
either adds a prompt stage and runs no engine.** That is the availability gap as a present fact rather than a
hypothesis, and it is what `GET /api/v1/resources/cell/availability` now reports.

## 11. Addendum (W640): the "Third Latent Cell / LGC-03" brief, assessed

Received from the Owner on 2026-10-10. Its author read the public README only and says so.

**The premise is refuted by the tree.** The brief specifies a THIRD Latent Cell, "independent of and
synergistic with" the first two. The words "Latent Cell", "LGC" and "latent growth" appear nowhere in the
repository — code, pages, plan, vision or ledgers; "latent" occurs in no file under `agentic_core` at all.
There is no first or second cell to be third to. The brief itself instructs that this be reported rather than
papered over; it is. The identity "LGC-03" and three-cell framing are not adopted.

**Most of it is the previous brief again.** Its sections on the instrument contract, the execution cycle,
just-right assembly, governed promotion, metabolism, verification, persistence, API and tests restate the
Growing Tip brief of 2026-10-09 almost clause for clause. That work is plan item P3.31 and is not duplicated.

**What is new: section 6, investigating a model's internal representations, in five levels.** Measured:

| Level | What it needs | What the tree has |
|---|---|---|
| 1 behavioural mapping | evaluation sets, a baseline, repeatable runs | a model lifecycle with an evaluate route (`POST /api/v1/native-ai/lifecycle/evaluate`) and recorded evaluations |
| 2 embedding analysis | an embedding backend | none: the archive index states "There is no embedding backend installed"; one older module embeds only when it can |
| 3 hidden activations | a model whose internals are readable | none: the local model tier is reached over Ollama's HTTP generate route, which returns text |
| 4 activation interventions | level 3, plus a way to write activations | none |
| 5 fine-tuning | a training pipeline, data, a compute budget | none; the machine has 7.7 GB of memory and torch is declared but not importable in the test runtime |

So levels 2 to 5 are not buildable on what is installed, and making them buildable is a dependency, a
download and a resource decision — the Owner's. Level 1 is buildable now on the existing evaluate route.

**Adopted.** The brief's own honesty rule — "it must not claim to have inspected its own hidden states … unless
an actual instrument demonstrably performs that operation" — and its evidence ladder (behaviour, embedding,
activation, correlation, causal). And its scientific standard for an evaluation (a stated hypothesis, a
baseline, held-out cases, a control, failed hypotheses kept): that is a bar the existing evaluate route can
be measured against, which nobody has done.

**Refused.** A new cell identity and lifecycle; the organ table (ruled 2026-10-09); a seven-word truth
vocabulary beside the fabric's outcomes; three new documents; the scalar cost function; candidate generation
and self-promotion — each for the reason given in section 4.

**The plan item (chartered W640): P3.32, model behaviour is mapped before anything is said about a model's
insides.** (1) Measure the evaluate route against the standard above and say what it does and does not
establish. (2) A behavioural baseline per served tier: a fixed, versioned case set, held-out cases, a control,
each result stored with the model and case-set version, and a failed case kept as a result. (3) Every surface
that describes a model says which evidence level its statement rests on, and none claims a level above 1.
BOUNDARY, not scheduled: levels 2 to 5, until the Owner rules on an embedding backend or a model with
readable internals.
