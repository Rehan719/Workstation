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

## 12. Addendum (W652): an external "strategic audit prompt" and its five preliminary findings, assessed

Received from the Owner 2026-10-10. Its author says plainly that it read the PUBLIC repository and its
documents and neither cloned the tree nor ran anything. Each claim was checked against the tree at W651/W652.

| # | Claim | Checked against | Verdict |
|---|---|---|---|
| 1 | Ledger v14: 27 tier-1, 16 tier-2, 9 tier-3, 8 delivered of 60, measured at 375c5ffb, not the current tree | the ledger's header and tier table | TRUE, and correctly caveated |
| 2 | Rounds after that commit need a fresh audit; the stopping rule is two consecutive zero runs with stated coverage | the plan's rulings | TRUE and ALREADY RULED: the audit runs when the last tier-1 row closes. It closed in W651; W652 is that audit |
| 3 | PLAN NOW names P2.34 and FU-675 (callers that do not say which text the person wrote) | the register | TRUE WHEN READ, STALE NOW: FU-675 closed in W651 (98 calls say, 8 are named with reasons); P2.34 has no open row |
| 4a | The README's test baseline is of the W498 tree | README line 134 | TRUE. The line said so itself and gave its reason (a count is only true of a tree), but 405 at W498 beside a plan at W650 reads as neglect. RE-DATED in W652 to the W650 run |
| 4b | The plan contradicts itself on the Stripe key rotation | the plan and the vision | TRUE, AND WORSE THAN STATED: the vision carried the same "still owed" sentence. BOTH CORRECTED in W652. That the dead key remains in git history is still true and still stated |
| 5 | "80 of 96 entries done" is not a measure of the vision delivered | the plan's own PLAN NOW block | TRUE. The plan counts entries and rows and projects in rounds; it claims no percentage of the vision. Nothing to change, but the distinction is worth keeping in front of any reader |
| - | "39 of 41 registered resources executable" | the plan's P3.31 text | TRUE. CORRECTED W658: this row said the figure was "not found in that form" and was the reviewer's arithmetic. That was wrong. The plan's P3.31 record says "of 41 registered resources the fabric can run 39; two spawners add a prompt stage and run no engine" (see section 13, row 8) |

**What the review gets right that is worth holding onto.** A registered resource, a passing test and a 200 are
not a capability a person can use. That is the audit's own premise (reach, then truth), and the review
arrived at it from the documents alone.

**What it could not see.** It read documents, so it inherits their lag: it recommends as a next step work
that was already done or already ruled (the FU-675 census, the fresh audit, the screen-failed ship refusal).
It recommends an "audit before touching any code" pass with a ten-part report. The repository already has
that instrument: a twelve-agent, refuted, coverage-stating audit whose output is a ledger and register rows.
Running a second, differently-shaped audit beside it would produce a second source of truth, which the
review itself warns against.

**Its five strategic options (trust-first, finish the ledger, one end-to-end proof, depth and parity, launch
readiness).** The Owner's standing sequence is A then B: close reached-surface truth defects until the
stopping rule is met, then the invisible shortfalls. That stands. OPTION C IS THE USEFUL ADDITION: prove ONE
person's path end to end - challenge, accepted output, established entity, shipped and downloadable body,
honest operation - on a fresh store, as a single driven journey with every claim on the way checked. The
audit samples regions; nothing today drives one journey start to finish and reads every surface it passes.
RECORDED as a register row for the Owner's sequencing, not started.

**Acted on in W652:** the two "rotation still owed" sentences; the README's dated count; one register row
(the single end-to-end journey proof). **Not acted on:** a second audit format; any reordering of the plan.

## 13. Addendum (W658): three external "master prompts" (business strategy, founder action plan, living strategy, LGC-03), assessed

Received from the Owner 2026-10-10 with the instruction to verify them and add work to the plan. All three were
written from the PUBLIC repository's documents; none cloned the tree or ran anything, and each says its figures
are leads to re-verify. Each claim was checked against the tree at W657 (branch head a687f2ce plus the W657
working tree; `main` at bb91d3a3).

### 13.1 Status claims

| # | Claim | Checked against | Verdict |
|---|---|---|---|
| 1 | PLAN NOW names P2.35 next; its leading rows are FU-679, FU-635, FU-625, FU-680, FU-653 | the register | TRUE WHEN READ, STALE NOW: all five closed in W657 |
| 2 | 81 of 98 plan entries done; 75 open rows, 74 scheduled and one awaiting the Owner | the register | AS THE PLAN STOOD AT W654 (not re-derived here). At W657 the register holds 66 open rows (P2.37 23, P3.30 23, P5.1 9, the rest 11), one awaiting the Owner (FU-473, deferred) |
| 3 | Ledger v15: measured at ab829862 on the floor, 118 findings, tier-1 16, tier-2 27, tier-3 48, delivered 27; five of six regions at the cap; does not count toward the two zero runs | the ledger | TRUE, and correctly caveated. All 16 tier-1 rows have since closed (W655, W656) |
| 4 | One prompt says the plan records work through W652, another through W656 | each other | THEY DISAGREE; the tree is at W657. Neither is a defect of the tree: each read a different day |
| 5 | The README's test count is of the W650 tree | README | TRUE. The line dates itself. RE-DATED in W658 to the W657 run |
| 6 | The Living Plan's header says "last reconciled 2026-09-05 (W446)" over a body with far newer records | the file | TRUE. The header also gave a suite figure from W481. CORRECTED in W658: the header now says what it is a record of and where the current figures are |
| 7 | Older text says the Stripe rotation is still owed | the vision | TRUE, AND TWO SENTENCES SURVIVED W652: the vision's list of Owner-held switches still named the rotation, and its "deployment honesty" line still said rotation was required. BOTH CORRECTED in W658. W652 fixed two writers of this sentence and not the other two |
| 8 | "39 of 41 registered resources executable; two spawners add a prompt stage" | the plan's P3.31 record | TRUE, and MY W652 VERDICT IN SECTION 12 WAS WRONG. The plan says exactly this ("of 41 registered resources the fabric can run 39"). I had searched for the reviewer's wording and not for the figure. Section 12 is corrected |
| 9 | The vision names neither a "Latent Cell" nor a "growing tip" | the vision | TRUE (no occurrence of either, nor of "Instrument Cell"). They are plan items P3.31 and P3.32, chartered on the Owner's request, not canon |
| 10 | FU-710 (the action-plan sentence can say zero open objectives beside open ones, and carries no date), FU-716 (the twin routes are prompts with no provenance and no page), FU-473 (16 unchecked constraints, Owner-deferred) | the register | TRUE, all three open and slotted: FU-710 and FU-716 in P2.37, FU-473 with the Owner |
| 11 | Vercel retired 2026-10-07; Google Cloud planned and not built; `render.yaml` present; no native mobile app; no analytics or error monitoring | README, the tree | TRUE |
| 12 | `scripts/recovery_audit.py`, `docs/DEPLOYMENT.md` and the ledgers named exist | the tree | TRUE, every file named exists |
| 13 | A `CONSTITUTIONAL_OVERRIDE` mechanism may exist; explain it or say it does not | the tree | IT EXISTS AS UNREACHED CODE AND IS NOT A CONTROL. One class (`avatars/frontend/avatar_interface.py`) halts an avatar session when a message equals that word, and returns a "signature" that is the digest of a fixed string under a comment reading "mock signed receipt". Nothing constructs the class: no route, no page, no test. There is no Owner override an operator could use, and none should be documented as one. NOT ARCHIVED, AND MY RECOMMENDATION TO ARCHIVE IT WAS WRONG: I made it before reading the plan, which records this module as the HELD avatar path whose wiring the Owner deferred (held until a constitutional check produces a real verdict). Archiving it would have removed deferred work. What W658 changes is the false part only: the answer no longer calls a digest of a constant a signature. Found with it: the plan says the package "exports the orchestrator and not the interface"; it exports both |
| 14 | `inputs/` holds Business Model Canvas material | the folder | PARTLY. It holds a blank third-party canvas TEMPLATE (a PDF and two images of the same empty nine-box form). No Workstation canvas has ever been written; no `docs/business/` or `outputs/` exists |
| 15 | Candidate living-strategy routes: `GET /api/v1/business-plan/roadmap`, `GET /api/v1/plan`, `GET /api/v1/plan/followups` | the routers | TRUE, all three are served; the Board Pack is `POST` and `GET /api/v1/vsb/{id}/board-pack` |

### 13.2 What the prompts ask for, against what exists

**A fresh ten-part audit with a vision-to-reality matrix before any code.** Refused for the reason in section
12: the repository's audit is a twelve-agent, refuted, coverage-stating instrument whose output is the ledger
and register rows, and the Owner has ruled when it next runs (after the tier-2 work, pointed at what v15 did
not exercise). A second audit in a different shape would be a second source of truth.

**"Do not commit, push or merge", and "at most one code slice".** These are the prompts' own boundaries for
whoever runs them. They are not the Owner's: the Owner's standing ruling is that each round reaches `main`
by its own pull request once every check is green. The Owner-held switches the prompts list (external AI,
authentication, signup, real money, deploy, Postgres) are the same ones the plan already holds, and stay held.

**A seven-word truth vocabulary and a second outcome vocabulary for the cell.** Refused for the product (the
fabric's outcomes and the ledger's tiers already exist, section 4). ADOPTED FOR THE BUSINESS DOCUMENTS ONLY,
where nothing like it exists: every statement in them carries one of observed, owner-defined, inference,
hypothesis, deferred, owner decision.

**LGC-03, a third cell.** Assessed twice already (sections 1 to 8 and 11). Nothing new in these prompts beyond
those briefs; the identity is still not adopted; the work is P3.31 and P3.32. One sentence is worth keeping
in front of both items: a catalogue row is not an executable, and declared, available, executed and verified
are four different states.

**A living strategy system.** The prompts say to map what exists before building, and what exists is most of
it: the Chief-owned plan with its opening and layers, the Owner-edit route, the roadmap derived on read, the
Board Pack, the cadence, Change Control and the audit log. The defects they suspect are already rows from
ledger v15 (FU-705 the pack omits the Strategy the Owner wrote, FU-706 a directive re-filed as a duplicate
objective, FU-707, FU-708 a Chief prompted with every scope's instructions, FU-710, FU-711) and are the
prepared rounds after the two Owner rulings. No second planner, scheduler or ledger is built. What does NOT
exist and the prompts are right to name: real product telemetry. Nothing measures a person completing a task,
returning, or accepting an output; a "living" strategy that reads customer evidence has none to read. That
is stated in the KPI dictionary below as NOT MEASURED, not filled with a number.

**A business case for Workstation itself.** THIS IS THE NEW WORK. Nothing in the tree is a business model
canvas, a business plan for Workstation as a business, a founder's operating guide or a list of what is and
is not measured. Phase 5 rehearses commercialisation on virtual WST (one tenant end to end, a derived price,
support, handover, what is not for sale) and never says who the first customer is, what it costs to run, or
what would show the thesis wrong.

### 13.3 The plan item (chartered W658): P5.6

WORKSTATION'S OWN BUSINESS CASE, WRITTEN DOWN, EVERY STATEMENT LABELLED. Five documents under `docs/business/`:
the canvas (nine blocks), the business plan in the canon's order (executive summary, concept, vision, mission,
strategy, aims, objectives, roadmap), the founder's guide for a Windows machine, the evidence and KPI
dictionary, and the living-strategy map. The clauses and the bar are in the plan. Two rules carried from the
prompts because they are right: no figure without a source (an unmeasured metric says NOT MEASURED), and no
promise of a zero bill.

**Refused from the prompts' business content:** every inherited number (monthly prices, a return on
investment, assets under management, user and subscriber counts, a support-resolution rate), every named
partner with no agreement behind it, and every claim of certification or proof. They appear in the documents
only as rejected historical statements, if at all.

### 13.4 For the Owner

RULED by the Owner 2026-10-10, on the recommendations put with this assessment: (1) the first segment to test
is individuals and small organisations using the Domain Working tools (Law, Employment and Career, Education),
stated in the documents as a hypothesis with the test that would show it wrong; the Quran Education Platform
stays free and is not a paid segment. (2) The drafted plan is NOT entered into the product's own Chief-owned
plan as the Owner's words: it ships as a draft document, and the Owner enters what they agree with through the
plan's own edit page. (3) The Owner accepted my recommendation to archive the unreachable override handler;
that recommendation was withdrawn the same day (row 13): the module is the held avatar path and stays. (4) A retired entity stays on the
roster and still counts as registered under the simulation ruling; left as it is and stated, to be decided
when retirement is next worked on. STILL THE OWNER'S: the legal form of the business, which needs qualified
advice and is not decided by a document.

## 14. Addendum (W659): an external "initial strategic assessment" and three revisions of its audit prompt, assessed

Received from the Owner 2026-10-10 (evening). Its author read the public repository's documents through W657
and says plainly that nothing was cloned or run. It is the best-informed of the external reviews so far: it
read the dated rulings and it separates what a document says from what a tree does. Checked against the tree
at W658.

### 14.1 Claims

| # | Claim | Checked against | Verdict |
|---|---|---|---|
| 1 | The README's suite count is of the W650 tree while the plan records work through W657 | README | TRUE WHEN READ. Re-dated in W658 to the W657 run, and it will lag again by one round by construction: a count is of a tree |
| 2 | 81 of 98 plan entries done, 66 open rows, 655 done, 18 dropped | the register at W657 | TRUE, exactly |
| 3 | Ledger v15: 118 findings, 16 / 27 / 48 / 27, five of six regions at the cap, 253 of 559 routes and 24 of 55 pages exercised; a capped count is not a count of all defects | the ledger | TRUE, and the ledger says the same of itself |
| 4 | The README counts 556 API operations and the ledger's census 559 routes; reconcile, do not assume one is wrong | the two instruments | RECONCILED: they count different populations. The README counts method-and-path under `/api/` only; the census counts every route the app registers, less the framework's own. Both are computed, neither is typed. (557 at W657: one route was added.) |
| 5 | PLAN NOW names the tier-2 item P2.35 as next while the tier-1 item P2.36 is open; is that order or staleness? | the plan and the register | NEITHER ITEM HAS AN OPEN ROW. P2.36's sixteen rows closed in W655 and W656; P2.35's last two closed in W658. Both stay open because an item closes on its ACCEPT clause, and theirs is the re-run of the audit, which the Owner ruled runs after the tier-2 work and must be pointed at what v15 did not exercise. PLAN NOW lists items in id order and says of each "every row closed, which is not the same as the item being done" |
| 6 | Ledger rows to re-test: the Board Pack hash that did not cover the pack (R3.1), "2 of 2 owned models produced output" on the floor (R4.1), pillar percentages from mounted routes (R6.0), "every change is gated" beside direct levers (R3.0), entity status disagreeing between readers (R2.4, R2.5), quality attestations (R1.2), immune health with nothing observed (R6.2), a keyword screen reported as compliant (R6.4) | the register | ALL ARE TIER-1 ROWS OF LEDGER v15 AND ALL ARE CLOSED (W655, W656; the immune row in W658), each with a guard driven red. "Closed" here means the row's guard, not a re-audit: whether they stay closed is what the next audit run measures, and the review is right to say so |
| 7 | Rows to re-check: FU-708, FU-706, FU-715, FU-716, FU-718, FU-728, FU-730 | the register | FU-728 closed W658. The other six are open and are the prepared rounds (faith content, silent drops, Board and Chief) |
| 8 | The delivery prompt's header still says "v11, revision 2" and names an earlier model | the file | TRUE. The header records how the prompt was derived at W446 and points to a handover file that exists. It is a dated record, like the Living Plan header corrected in W658; left, and noted here |
| 9 | THE CANON HAS A STALE LIST: a "still with the Owner" paragraph names the lifecycle, the Products axis, the KPI gate, Mode 2, the Stripe key roll and the 162 entities as open | the vision, section 18 | TRUE, AND IT IS THE FIFTH SENTENCE ABOUT THE KEY ROLL. W652 corrected two, W658 two more and added a guard, and the guard could not see this one because it says "roll" and not "rotation". CORRECTED in W659: the list is kept as the W446 record it is and is followed by what became of each entry; the guard now reads both words. The plan's own "ordering" paragraph called the same three items "genuinely unbuilt"; it gains its status too |
| 10 | Every file the prompts name exists (`scripts/entity_coverage_scan.py`, `scripts/reach_audit.py`, the handover file) | the tree | TRUE |
| 11 | The rulings it lists as binding (apex simulation, immune five-minute rule, heartbeat levers audited, Developing means both, faith content on general routes, Pickthall, no direct push to main) | the plan's rulings blocks | TRUE, each as ruled |

### 14.2 Its recommendations, against what is already ruled

**"Establish one reproducible baseline before authorising more development."** The exact-commit discipline it
asks for exists: every ledger names the commit it booted, the suite count is dated with its tree, and CI runs
the whole suite on each round's own pull request before it merges. What it adds that is worth keeping: say of
each number WHICH tree it measured, in the sentence that states it. W658 did that for the Living Plan header;
row 8 above is the one place still not done.

**"Close tier-1 through the existing plan; two consecutive qualifying audits."** This is the Owner's stopping
rule of 2026-10-09, restated accurately. Nothing to change.

**"A report-only first phase; change nothing during the audit."** Its own boundary for whoever runs it. The
repository's audit already changes nothing while it measures; the rounds between audits are the Owner's
standing instruction.

**A second, differently-shaped audit.** Refused, as in sections 12 and 13: one instrument, one ledger.

### 14.3 Worth adopting, and where each goes

- **A common evidence contract for a deliverable or status:** what was requested, what ran, what served it,
  what was measured, what was not assessed, which gate decided, what was hashed, who owns the record. Most of
  these exist as separate fields added round by round (the silent-drops round adds "requested / ran / not
  run"). Nobody has checked ONE deliverable against all eight. REGISTERED as a tier-3 row: take the eight as a
  checklist against the three kinds of stored output (a deliverable, a composition run, a Board Pack) and
  record which each lacks.
- **"Forever" as bounded operational promises:** backup and restore, a protected shutdown, retirement that
  keeps obligations. Belongs in the founder's guide (P5.6) and the deployment pre-flight (P4.5), stated as what
  is and is not built. Carried into both; no new item.
- **A causal chain per biomimetic claim** (stimulus, measurement, decision, action, recorded outcome,
  feedback), with a missing link making the loop partial. The immune work in W658 is exactly this for one
  layer. Carried as a way of reading the next audit's region 6, not a new item.
- **Customer satisfaction with consent and provenance.** No telemetry exists; stated as NOT MEASURED in the
  P5.6 dictionary, which is where what would measure it is written down.

### 14.4 For the Owner

Nothing new to rule. One thing to know: rows 5 and 6 mean the plan now has NO open tier-1 row and the older
tier-2 item has none either; what stands between the plan and the next audit is the 21 open tier-2 rows of ledger
v15, of which the prepared rounds cover the first batches.

## 15. Addendum (W660): a regenerated "Biomimetic Minimisation Engine" specification and integration prompt, assessed

Received from the Owner 2026-10-10 (late). It replaces an earlier greenfield proposal (eight new modules, six
frameworks, fixed thresholds) with a brief that starts from what this repository already records. Its author
read the public documents and ran nothing. Checked against the tree at W659, and this time one thing was RUN:
the status route itself.

| # | Claim | Checked against | Verdict |
|---|---|---|---|
| 1 | P3.17 is recorded DONE at W553 and must not be reopened | the plan | TRUE |
| 2 | The status route, the objective with five weighted terms, the transport router, one thermodynamic ledger and the archived bridge and diffusion sources are where it says | the tree | TRUE, every path |
| 3 | The follow-ups to re-read (FU-233, FU-235, FU-236, FU-329) may no longer be open | the register | ALL FOUR ARE CLOSED (W547, W548), as is FU-234 (invented bit counts, W546) |
| 4 | The objective withholds J when any weighted term is unassessable, and no missing term defaults to zero | the route, driven | TRUE. Driven on the floor: 0 of 5 terms assessable, J not reported, each term naming its missing producer |
| 5 | In the earlier measurement only the entropy-export term had a producer | the route, driven | AS MEASURED NOW: none is assessable with no metrics supplied; entropy export is the one a caller could supply, and its basis says so |
| 6 | The transport solver (POT) was recorded unavailable, and honest unavailability is the right answer | the route, driven | THE BRIEF COULD NOT SEE THIS, AND MEASURING IT FOUND A DEFECT. On this machine the solver IS installed (it is in pyproject and not in requirements.txt - an open row). The response then said two things: the router answered "importable", and the transport TERM beside it said the solver "is not installed". One sentence was computed and one was typed in W548. FIXED in W660: the term asks the router; with the solver present it is still not assessed, and says what is missing (two marginals and a cost matrix). Guarded in both states |
| 7 | The ledger reports a theoretical floor, not energy drawn; the hardware factor is declared, not measured; a payload size is not a count of bits erased | the ledger and its callers | TRUE in the tree since W546: the output is named a floor, the factor says it is declared, and each caller's basis says its count is a payload size. ONE SENTENCE TIGHTENED in W660: the ledger's own basis read "the minimum to erase N bits", which read alone says N bits were erased; it now says what erasing that many would cost and that the count is the caller's |
| 8 | A top-level `core/` package sits beside the "no parallel source tree" rule and nothing should move until that is resolved | the register | TRUE; it is an open lead (a row on the commercial-rehearsal item), and nothing was moved |
| 9 | `torchsde` was recorded as not installed | this machine and requirements.txt | TRUE HERE, and requirements.txt DOES list it: the mirror image of the transport solver. What the status route reports depends on the deployment, which is the reason its sentences must be computed |

**Refused, as the brief itself refuses:** a new minimisation tree, a second meter, a second registry or page;
six frameworks built to fill a table; thresholds, fidelity percentages and confidence figures with no
instrument; wiring the engine into capital allocation, consultation, the avatar or the heartbeat with no
measured use case; installing a solver to make a term turn green.

**Its scientific corrections to the earlier proposal** (the Gaussian divergence written the wrong way round,
a bridge "likelihood" that is not one, a consensus simulation that never passes its own callbacks, Murray's
law applied to software) are about code that was never in this tree. They are right, and they are the
reason none of that code should arrive.

**Outcome.** The brief's own second exit condition holds: no open row asks for minimisation work, P3.17 stays
closed, and nothing is built. What changed is two sentences, both found because the route was driven rather
than read.

## 16. Addendum (W660): revision 3 of the external strategic assessment and its prompt, assessed

Received from the Owner 2026-10-10 (late). It was regenerated from sections 13 and 14 of this document, and
says so. It now restates this repository's own position rather than proposing a second one.

| # | Claim | Verdict |
|---|---|---|
| 1 | One audit instrument; no second audit, ledger, planner or register | AGREED; it is the position of sections 12 to 14 |
| 2 | The Instrument Cell is P3.31, inside the existing fabric; 39 of 41 resources run, and the two spawners (`vsb_spawn`, `genesis_establish`) add a prompt stage and run no engine | TRUE, both ids as named. Still open on P3.31, as its record says |
| 3 | One automatic alternative for a resource that reads or composes, never for one that writes | TRUE, as ruled 2026-10-10 |
| 4 | P3.32: behaviour first; the evaluate route gained a named, versioned probe set and a control; held-out probes are unbuilt; levels 2 to 5 are not scheduled | TRUE, as the plan records it |
| 5 | The single end-to-end journey is recorded for sequencing and not started | TRUE. It is also what the commercial phase's first item already asks (one tenant, concept to commercial output, measured) |
| 6 | P5.6 is five documents; the six labels are for business documents only; the first segment is a hypothesis; the Quran Education Platform stays free; the draft is not entered as the Owner's words | TRUE, each as ruled |
| 7 | The public README and `main` may be behind the working tree | OUT OF DATE WHEN READ HERE: `main` holds W658 and the README is dated to the W658 run |
| 8 | The key rotation is done; history still holds the old key; do not rewrite public history | TRUE, and nothing is rewritten |

**What it adds.** A list of what a release depends on that is not yet a row anywhere: backup and restore of
the file stores, error and usage telemetry, the handling of data about children in the Quran Education
Platform, accessibility, and who answers when something is wrong. The last is the commercial phase's support
item. The others belong in the founder's guide's launch gates (P5.6, clause 3), each stated as built,
measured or absent; carried there, not registered separately, because that clause already owns "the launch
gates in order".

**Nothing here changes the order of work.**

## 17. Addendum (W666): four revisions of an external "whole commercialisation master prompt", assessed

**What was received (Owner, 2026-10-11).** Four files, each a prompt addressed to this model: revision 4
("repository tailored"), revision 5 ("deep research optimised"), revision 6 ("whole vision integrated"), all
dated 2026-10-10, and a shorter regeneration dated 2026-10-11. The covering note describes the last as
building on "the previous Claude prompt" and a "Founder Playbook". They ask for one thing in two directions:
commercialise Workstation as a business, and use Workstation to deliver a customer's solution from challenge
to handover.

**How they were read.** The 2026-10-11 file was read whole. Revisions 4 to 6 were searched for every
statement that can be checked against this tree or an official source (paths, plan and row ids, round ids,
counts, money figures) and each was checked. These prompts make few such statements, and say so of
themselves: they tell their reader to re-derive everything. That is to their credit, and it means most of
their content is instruction, not claim.

### 17.1 What was checked

| # | Statement | Where | Finding |
|---|---|---|---|
| 1 | P5.6 charters five documents under `docs/business/`, with the first segment, the free Quran Education Platform, the labels and the "not the Owner's words" rule | all four | **TRUE** of the plan. The five documents are drafted and not yet landed: `docs/business/` does not exist at this commit |
| 2 | P5.6's register rows "have historically included FU-740 to FU-744" | r4 | **TRUE**, and all five are still open |
| 3 | "`PLAN NOW` pointing to P2.35 ... five P5.6 follow-ups still open" | r6, as a dated observation | **STALE, as it warns.** P2.35 closed in W665; the open truth items are P2.38 and P2.39 |
| 4 | The paraphrases of P5.1 to P5.5 | r6 | **ACCURATE** against the plan's own text, item by item |
| 5 | The quality bar: four criteria measured by a gate, seven attested by a journey, five established by nothing | r6, as a W654 lead | **TRUE** of the vision's section 10 as it stands |
| 6 | A repository-level `CLAUDE.md` | r4, r5, r6, each "if present" | **ABSENT.** There is none; the working rules are in the delivery plan |
| 7 | A companion `WORKSTATION_IDBO_FOUNDER_COMMERCIALISATION_PLAYBOOK_2026-10-10.md` | 2026-10-11, "if present" | **NOT RECEIVED.** No file of that name was supplied; nothing here relies on it |
| 8 | Companies House online incorporation 100 pounds; online confirmation statement 50; online incorporation of a community interest company 115 | r4 | **CONFIRMED** on the Companies House fees page, read 2026-10-11 (page last updated 25 September 2026) |
| 9 | A standard online trade mark application 205 pounds for one class, 60 for each further class | r4 | **PARTLY CONFIRMED.** The government's page read 2026-10-11 says registration "costs at least" 205 pounds; the per-class figure was not on the page read and is NOT CHECKED |
| 10 | The VAT registration threshold is 90,000 pounds of taxable turnover | r4 | **CONFIRMED**, read 2026-10-11 |
| 11 | Corporation Tax: 19% on profits of 50,000 pounds or less, 25% above 250,000, marginal relief between | r4 | **CONFIRMED**, read 2026-10-11 |
| 12 | IN4 Group exists and runs founder and skills programmes | 2026-10-11 | **EXISTS, programmes NOT CHECKED.** Press coverage places it at MediaCity, Salford, with skills and start-up programmes; its own site and what it currently offers were not read. No relationship beyond the Owner's attendance is to be implied |
| 13 | Five candidate names (IDBO Works, IDBO Foundry, VSB Foundry, PurposeWeave, IDBO Systems) | 2026-10-11, as unverified | **NOT CHECKED**, as the prompt labels them. No register, trade mark or domain search has been run |

### 17.2 What is sound, and already the rule here

Authority order (the Owner's vision and rulings, then the plan, then code and evidence, then documents, then
external suggestions); one plan and one register, no second roadmap or ledger; four states kept apart
(declared, available, executed, verified); no invented traction; the Quran Education Platform free; legal
form, spend, filings, publication, sign-up, external models, real money and deployment all the Owner's.
Each of these is already a ruling or a clause of the plan. Nothing in the four files contradicts a ruling.

### 17.3 What is declined, and why

| Asked | Decision |
|---|---|
| "Do not edit files until ... shown the Owner a concise baseline and proposed scope" | **Not adopted as a gate.** It is the prompt's own procedure, not the Owner's; the Owner's standing instruction is to decide and build, and the baseline is what every round already records |
| An "evidence contract" of eight fields on every stored output | **Not added as a second vocabulary.** The product already carries what served an output, what was measured and what was not assessed; the audit checks that they travel with it |
| A pipeline tracker for prospects | **Not built.** There are no prospects. A format is proposed in the workpack and nothing is stored about a person until the Owner decides how |
| Sending outreach, checking names with paid tools, contacting IN4 Group | **Drafts only.** Each is an external act and the Owner's to take |

### 17.4 What it adds that the plan did not have

P5.6 covers the business's description. These prompts ask for the working papers of a first sale, which P5.6
does not: a comparison of candidate first offers, the interview pack, a cost model that separates quotes from
assumptions, a name screen, draft marketing, a route to partners and support, a formation workpack, and a
scope for outside help. They are chartered as **P5.7**, every document a draft, nothing sent or filed.

One finding from doing the check: P5.1 (one tenant from concept to commercial output, measured) is the item
these prompts most depend on. A first offer cannot be chosen on evidence until one journey has been driven
and read back, and ledger v16 found the establish route seals whatever evidence its caller posts. The order
is therefore P2.38, then P5.1, then the offer comparison of P5.7.

## 18. Addendum (W670): an external "final converged master prompt" (Appraisal, Instrument, LGC-03, engines, Horizon, VSB, strategy), assessed

**What was received (Owner, 2026-10-11).** One file, a prompt addressed to this model, 801 lines, described by
its covering note as the final regeneration of the earlier prompts. It asks for one architecture joining an
appraisal nucleus, the Instrument Cell, a third cell ("LGC-03"), the cognitive, MJM and BME engines, Horizon,
the entity layer and the business strategy, delivered in eight phases.

**How it was read.** Its sections 2 and 3 (the repository account and the architecture) were read whole; the
rest was searched for statements that can be checked against this tree. Like its predecessors it tells its
reader to re-derive everything, and most of it is instruction rather than claim.

### 18.1 What was checked

| # | Statement | Finding |
|---|---|---|
| 1 | The README states 695 integration tests passing and 15 skipped on the W668 tree | **TRUE** of the README at the W669 commit |
| 2 | The plan's generated block shows P2.37 next, 83 of 102 items done and 86 open follow-ups | **TRUE** of the plan on main at the W669 commit; all three move with every round |
| 3 | The W640 assessment refuted that a "third Latent Cell" had two predecessors, did not adopt the name "LGC-03" or the organ vocabulary, and found the proposal duplicated plan item P3.31 | **TRUE.** Section 11 of this document says exactly that |
| 4 | The fabric registry holds 41 resources of which 39 can be run; two spawners run no engine | **TRUE** as re-read on 2026-10-11: 41 registrations, 38 with a handler branch and one owned by the runner, two with none |
| 5 | An Owner-ratified inventory of 23 engines in five tiers (six foundational, three meta, three auxiliary, three MJM, eight BME) | **TRUE** (Owner ruling 2026-09-30; `docs/COGNITIVE_ENGINE_ARCHITECTURE.md`) |
| 6 | The BME's functional composes five terms | **TRUE as a declaration.** `agentic_core/biomimicry/minimisation/core/omega_functional.py` names the terms and, for each, what produces it; more than one has no producer, and the module says so |
| 7 | `docs/WORKSTATION_IDBO_UNDERSTANDING.md` and an `inputs/` folder with a canvas template exist | **TRUE** |
| 8 | "The Owner's present instruction deliberately reopens the concept of a distinct third Cell" | **NOT ESTABLISHED BY THIS DOCUMENT.** This is the prompt's statement about the Owner. The Owner's recorded ruling of 2026-10-10 is: Latent Cell level 1 only, the Instrument Cell is P3.31, the model-evaluation work is P3.32. A document cannot reopen a ruling; the question was put to the Owner, who ruled the same day (18.3) |
| 9 | Ten "current public findings" to reproduce or refute | **ALL ARE ROWS ALREADY.** Each is a finding of ledger v15 or v16 and rides P2.39 or P3.30; W670 closes the tier-2 ones among them (the genome stage's stripped qualifiers, the engine-backed label, the edition and riwayah fields) |

### 18.2 What is sound, and already the rule here

One plan and one register; no second registry, runner, result vocabulary or audit; the Instrument Cell's seven
clauses kept as they are; P3.32 kept separate and at the level of behaviour; a check that never ran cannot
pass; an engine that returns a constant is not doing its named work; no parity claim across the 96 realm,
domain and product combinations without measured tasks. Each is a ruling or a clause already in force.

### 18.3 The one thing it adds, and the Owner's ruling on it

Stripped of the cell vocabulary, the prompt's "unique responsibility" for LGC-03 is this: an approved objective
and an Instrument Cell proposal are held together as a **versioned, inspectable assembly specification** that
can be replayed, and whose run is linked back to the proposal it came from. Reading P3.31 against the tree
found the same gap from the other side: a proposal is not saved, so "proposed versus executed" cannot be
linked. That is a bounded addition to P3.31 and needs no third cell, no new name and no new runner.

Whether to go further - a separately named cell with its own lifecycle - was put to the Owner, who RULED on
2026-10-11: no third cell; the saved, versioned proposal is built inside P3.31. The prompt itself allows that
outcome: if the Instrument Cell can meet the requirement "the ADR must say so and propose ... no additional
runtime module".

### 18.4 What is declined

| Asked | Decision |
|---|---|
| An architecture decision record before any source change | **Not adopted as a gate.** This section is the record; the plan and the register carry the decision |
| A reconnaissance report and a "required first response" before editing | **Not adopted.** It is the prompt's procedure; every round already records its baseline |
| Levels 2 and 3 of the cell (candidate generation, governed promotion) | **Not scheduled.** Deferred in section 11 and by the Owner's ruling; nothing here changes that |
| A second set of business deliverables | **Not duplicated.** They are plan items P5.6 and P5.7 |

### 18.5 The path it is right to ask for

The prompt's first milestone is one real path: an appraisal resting on evidence, an authorised execution, a
verification, and the result returned to the next appraisal. Nothing in the suite drives that path end to end,
and the ledger's finding that the organisational cascade's appraisals "develop nothing" is the same absence
seen from a page. It is registered as a row: drive the path with a guard and name the step where it stops.

## 19. Addendum (W672): two revisions of an external "canonical biomimetic OGE/HAIRMS master prompt", assessed

**What was received (Owner, 2026-10-11).** Two files, each a prompt addressed to this model: "v6" (1,413 lines)
and "v7 converged final" (1,524 lines), both dated 2026-10-11. They ask for the functions of the "OGE / HAIRMS"
blueprint assessed in `docs/OGE_HAIRMS_BRIEF_ASSESSMENT.md` on 2026-10-09 to be delivered through the existing
architecture, led by authentication and entity isolation, an "execution contract" and one end-to-end slice.

**How they were read.** v7 was read whole. v6 was compared with it line by line: it differs in eight lines and
is otherwise v7 without Appendices L to O (a "Clownfish" separation of duties, per-engine contracts for the six
foundational engines, "Needs-Wants-Desires", and a crosswalk) and without one sentence of plan figures. Every
statement that can be checked against this tree, the plan on main (`d4ecfdb2`, the W670 merge) or an official
page was checked: 79 in all, listed in the round's notes. The blueprint itself was not supplied with these
files, so what they say the blueprint contains is not checked here. Both prompts label most figures as dated
leads to re-measure, and most of their text is instruction, not claim.

### 19.1 What was checked

| # | Statement | Finding |
|---|---|---|
| 1 | The README reports W670 with 700 integration tests passing and 15 skipped | **TRUE** of the README on main (line 134) |
| 2 | The plan's queue begins P2.37, then P2.38, P2.39, P3.30, P3.31 with 4 of 6 rows, P3.32 with 0 of 1 | **TRUE** of the generated block on main; it moves with every round |
| 3 | FU-814 is the gap joining appraisal, Change Control, applied action, verification and the next appraisal | **TRUE**, open on P3.30, and already scripted as a guarded path |
| 4 | The latest recorded ruling declined a third cell and kept the saved, versioned proposal inside P3.31 | **TRUE** (Owner ruling 2026-10-11; section 18.3; row FU-813) |
| 5 | The 2026-10-09 assessment found the blueprint's paths absent, six named technologies a name list, a constant-success executor, no Nemoclaw runtime, a naive grep gate of 1,173 lines | **TRUE** of that document, each as the prompts report it |
| 6 | The blueprint's ten package paths, the `sovereignctl` command and its two branch names are "not presumed" | **ABSENT, still.** Nine paths are not directories and one holds no tracked file; the command appears in no code; neither branch exists |
| 7 | "The current P3.30 records should establish whether [the constant-success executor] is fixed" | **STALE.** It was archived (`_archive/agentic_core/products/signature_suite/`) and its branch removed from `governance/uci_interceptor.py` |
| 8 | "If MultiSigCouncil ... exists but is unreachable"; the crosswalk lists it as an owner to inspect | **STALE.** Archived on the Owner's ruling of 2026-10-09 (evening); the Board's ratification is the control |
| 9 | Heartbeat, genome, organism status, Sovereign Evolution, Board and Change Control routes are "retest targets" for missing protection | **STALE for those named.** That is plan item P2.6's own list, closed in W505: each router is mounted behind an admin or authenticated dependency (`app_mvp.py:357-483`) and a guard reads the mounted dependency. Not closed for the business plan: see 19.4 |
| 10 | "Read the current data-classification and barred-data rules" | **ABSENT.** No live file carries a data class; it is row FU-610 on P4.3, as the same prompts say elsewhere |
| 11 | A change-class vocabulary C0 to C5; a model tier arrangement 0 to 5 | **ABSENT.** Change Control has LOW, MEDIUM, HIGH, CRITICAL; the tier router declares five tiers and external models are a switch, not a tier |
| 12 | The crosswalk's "current policy middleware" as the owner of constitutional checks | **FALSE.** There is no app-wide gate; `app_mvp.py` says so on every response and gates are applied route by route |
| 13 | Federation interfaces "if operational" | **ABSENT.** No federation package; the validators record that no federation runs |
| 14 | AlphaFold, Ginkgo, Cosmos or Omniverse, holographic systems | **ABSENT** from live code (one comment in `products/`); archived files only |
| 15 | An "OAM-QKD software surrogate"; Mammouth | **NAMES ONLY.** A declared constraint names an enforcer, "OAM_QKDSurrogate validation", that does not exist, and the validator says it measures nothing; Mammouth is a word in one docstring |
| 16 | "A narrative scenario is not a world simulator" | **A FINDING IN THE TREE.** `agentic_core/simverse/causal_simulator.py` is live and called: it returns `fidelity = 0.924` and `backdoor_criterion_verified: True` as constants and writes an event; the avatar effector's "causal" gate is built on it and can refuse only on an exception (19.4) |
| 17 | "Preserve the authentication and roles already implemented" | **EXISTS, narrower than asked.** One user store, three role strings of which only `admin` is ever read, owner scoping by username, switches off by default. No delegation, no service principal, no per-entity grant. An API key is issued and nothing accepts it |
| 18 | 23 engines in five tiers, three MJM engines, `MJMOrchestratorV4`; the six foundational names | **TRUE** (Owner ruling 2026-09-30; `cognitive/registry.py`) |
| 19 | A contract per engine (function, evidence, prohibited inference) | **NOT IN THE TREE in that form.** `docs/COGNITIVE_ENGINE_ARCHITECTURE.md` section 4 states eight invariants that bind every engine alike; the six engines share one response shape |
| 20 | "Clownfish Protocol"; "Needs-Wants-Desires" | **ABSENT** from live code and from the vision; both were in the brief assessed on 2026-10-09 |
| 21 | NIST AI RMF 1.0 has four functions (Govern, Map, Measure, Manage), is voluntary, and is being revised | **CONFIRMED** on the NIST page read 2026-10-11 |
| 22 | "The supplied blueprint is now part of the intended functional destination"; "this prompt adopts those requirements as the target design vocabulary"; "the latest target specification supplied to you" | **NOT ESTABLISHED BY THE DOCUMENT, and contrary to a ruling.** The Owner ruled on 2026-10-09 (evening) that the OGE and HAIRMS vocabulary is not adopted |
| 23 | Real-person records kept as "a future capability vision" in tiers H0 to H3 | **NOT ESTABLISHED BY THE DOCUMENT; the Owner was asked.** The ruling of 2026-10-09 (evening) was no registry of real people. Asked on 2026-10-11, the Owner AMENDED it: the capabilities are wanted inside Workstation, for its entities (19.5) |

### 19.2 What is sound, and already the rule here

One vision, one plan, one register, one runner, one result vocabulary; no package skeletons, no branch named by
a document, no second scheduler; a class, route or count is not a capability; a check that did not run cannot
pass; a threshold with no instrument is not a gate; no number on a person's faith, sincerity or worth; sacred
text never generated; external models, sign-up, real money and deployment the Owner's switches; the facility
lifecycle (FU-609), the data class on an external call (FU-610) and the read-only resource inventory (FU-618,
built W639) routed where the earlier assessment put them. Each is a ruling or a clause already in force, and the
prompts mostly say so themselves.

### 19.3 What is declined, and why

| Asked | Decision |
|---|---|
| OGE and HAIRMS as "target design vocabulary", with an appendix mapping every blueprint name | **Declined.** Owner ruling 2026-10-09 (evening): the vocabulary is not adopted. The crosswalk is used once, here, as a check list |
| Real-person engagement, HR and payroll tiers kept in the target model | **Not taken from the document; chartered on the Owner's own ruling.** The Owner ruled on 2026-10-11 that staff records, payroll and wellbeing are wanted within Workstation. It is chartered as its own plan item, in this platform's words and under its rulings, not as the brief's tiers |
| "Needs-Wants-Desires": contentment, rest, play and focus features | **Not scheduled.** Assessed on 2026-10-09 (section 6) in its monitoring form and refused; the opt-in form names no user who has asked for it |
| "Clownfish" executor, editor and watcher roles | **No new roles.** The existing separation is proposer and admin decider with the Board's ratification (ruling 2026-09-14). The one question it raised is ruled in 19.5 |
| An "execution contract" of twelve concerns and eleven tests on every action | **Not added as a schema.** The saved specification (FU-813), the driven path (FU-814) and the P5.1 journey are scripted and cover the proposal, run, verification and readback links; delegation and expiry have nothing to bind to while there is one principal |
| With authentication enabled, tests of delegates, reviewers, service jobs and agents | **Not buildable as asked.** None of those principals exists. What can be read today is in 19.4, and authentication is the Owner's switch (P4.1) |
| A baseline report, a route matrix and a trace record before any edit | **Not adopted as a gate.** It is the prompt's procedure; every round records its baseline |
| Core-technology adapters, facility provisioning, a CLI | **Declined**, as on 2026-10-09; nothing here can run them and the prompts do not insist |

### 19.4 What it adds

The prompts are right that authentication is the part least proven, and reading for them found things the
audits do not reach, because every audit runs with authentication off. All but the last are **findings from
reading, to be driven before they are relied on**; all sit behind the Owner's switch, so they are pre-flight
work for P4.1, which today carries no rows.

1. Four business-plan routes that write (`/objective`, its `/review` and `/orchestrate`, `/generate`) and three
   that read declare no user at all and the router is mounted with none, although P2.6 lists "owner scoping on
   business-plan". The sibling `/set` stamps the caller; these do not ask who is calling.
2. No instrument counts this. A read of the 84 mounted routers found 547 routes, of which 153 that write and
   146 that read name no user in their signature or their mount. Many are public by design; nothing says which.
3. An API key is generated and stored hashed (`auth/core.py:417`) and no code path verifies one; the module
   says keys "are also accepted as Bearer tokens". The role `viewer` can be assigned and nothing reads it.
4. The heartbeat calls the entity's evolve and re-ship handlers with `user=None`, which the ownership check
   treats as allowed whether or not authentication is on. The only record of who acted is a trigger string.
5. The causal simulator of row 16: a constant presented as a verification, on the held avatar path (P3.30).

### 19.5 What the Owner ruled (2026-10-11)

The questions this reading raised were put to the Owner, who ruled the same day:

1. The vocabulary of the brief is not adopted (the 2026-10-09 ruling stands).
2. The authentication findings of 19.4 are fixed in ONE authentication-readiness round, after P5 and before the
   final audit, chartered under P4.1. No round turns the switch on.
3. The heartbeat acts on an entity only where that entity has opted in, and under a named service identity
   once authentication is on.
4. For a high or critical change the person deciding must differ from the person submitting, once more than
   one administrator exists. Whether they were the same is recorded on every decision from this round.
5. API keys and a read-only role are wanted: both are made to work in the readiness round. Until then the
   product says that a key is not yet accepted.
6. No written contract per engine: the eight shared invariants bind each.
7. **The 2026-10-09 ruling against a registry of real people is amended.** Staff records, payroll and
   wellbeing are wanted "within and for" Workstation and its entities. Chartered as its own plan item. What it
   may hold before authentication is on, and the form wellbeing may take under ruling A.9.5, are stated in the
   item and are still the Owner's to confirm.

**Built in the round that landed this section (W672):** every decision on a change records whether its decider
was also its submitter, stated only when both names were checked; an issued API key and the module that issues
it say a key is not yet accepted; the causal simulator returns no typed fidelity and no typed verdict, and the
string the effector records is headed as not assessed. The rest of 19.4 is filed as rows on the fourth
phase's first item.

## 20. Addendum (W673): five external documents on a finance, tax, invoice, funding and capital-stewardship capability, assessed

**What was received (Owner, 2026-10-12).** Five files and two covering notes. A "Phase 0 reconnaissance" of
12 October (195 lines) and a "Phase 0 audit and Phase 1 handoff" of 11 October (164 lines), both written from
the public repository at the W671 merge (`a96e2011`) with no checkout and no test run, as each says; a README
for an "apply-ready patch" to the capital fund's amount check (43 lines; the patch itself was not supplied);
and a "master prompt" of 11 October (712 lines) supplied twice. The notes ask for a first slice - an entity's
financial profile, a test invoice, an accounting entry, an obligation, a proposed payment, an approval, a mock
payment, a reconciliation - and give an eight-point definition of done.

**How they were read.** All were read whole. The two master prompt files are byte-identical. Every statement
that can be checked against main, against the working tree of this round, or against the three official pages
the documents cite and this round was allowed to open (read 2026-10-12) was checked: 78 in all, listed in the round's notes -
61 true, 6 partly, 3 false, 1 stale, 4 not established by the document, 3 not checked.
**Unlike the earlier documents in this file, these mostly instruct rather than claim, and where they describe
this repository they are mostly right.** Their caveats are accurate wherever they were tested: that nothing
was run, that the plan must be re-read at the checkout, that the payout core was not seen, that a README test
count is not a run. The three false statements are line numbers in one document. None says the code does
something it does not.

### 20.1 What was checked

| # | Statement | Finding |
|---|---|---|
| 1 | The fund's allocate route declared no caller, checked only sign and balance, and continued for an id nothing knows | **TRUE of main** (`api/capital_fund.py` 243-303 there). **No longer true:** W672 holds every allocation for an explicit decision, refuses an unknown id, and refuses a non-finite amount |
| 2 | The allocation recorded "gate: not applied", credited no entity, and wrote its audit event after the save | **TRUE of main.** Still true that no constitutional gate runs and no entity is credited; the record now names the change that approved it |
| 3 | The amount was a plain float, so a NaN would pass both comparisons | **TRUE of main, as reasoning** (nobody drove it). Fixed in the core by W672; the model field is unchanged |
| 4 | The supplied patch "applies cleanly" and "8 passed" | **NOT ESTABLISHED.** No patch was supplied, and its own README says the run was against a stand-in, not this tree. Superseded by row 1 |
| 5 | The payout function takes an `owner` and never reads it | **TRUE**, main and tree (`economy/owner_payments.py:260-288`). See 20.4 |
| 6 | The payout writes no audit event | **TRUE**, main and tree |
| 7 | "Do not repeat the wrong-owner acceptance as proven; the core could not be retrieved" | **An accurate caveat, now settled by reading:** nothing compares the name with the account's owner |
| 8 | `REAL_MONEY_ENABLED = False`; the on-chain withdrawal refuses while it is | **TRUE** (`owner_payments.py:35`; `products/capital_fund/adapters/crypto_gateway.py:94-99`) |
| 9 | The 10,000,000 WST is recorded as an Owner-set virtual endowment, with its basis and with warnings for an incomplete store | **TRUE** (`api/capital_fund.py:84-97`, 57-70) |
| 10 | The fund store "fails closed" and never re-seeds | **PARTLY.** An unreadable or partial store refuses every writer. A MISSING file is read as first creation: a fresh 10,000,000 (20.4) |
| 11 | The ledger is a per-entity virtual double-entry ledger and not statutory books | **TRUE** (`economy/ledger.py:1-6`) |
| 12 | No live path is named for tax, invoices, bookkeeping, VAT or HMRC; one tax module sits under `_archive/` | **TRUE** |
| 13 | `products/capital_fund/` exists and "file existence does not prove a route is live" | **TRUE, and understated:** nothing in the application imports the package (20.4) |
| 14 | The transfer route scopes the sender and documents a gate, a hold for a material amount and an audit event | **TRUE.** Below 250,000 WST nothing is held; that is the designed threshold |
| 15 | PLAN NOW names P2.37 next; 83 of 102 items done; 92 open rows | **TRUE of main.** The tree reads 83 of 103 and 88 |
| 16 | A "discrepancy" between PLAN NOW (P2.37) and the scheduled block (P2.39) | **NOT A DISCREPANCY.** P2.37 has no open row and P2.38 none, so the first item with a row is P2.39; the block says so on its first line |
| 17 | The Living Plan's header was last reconciled at W446 | **TRUE**, and the header says the body is newer |
| 18 | FU-794 was measured against `ca081db0`, with 3,000,000 WST allocated to an id that does not exist, and records a payout issue | **TRUE** of the row. Its allocation half is closed by W672; its payout half is not (20.4) |
| 19 | The earlier review found `archive/products/swf/` never existed, the historical core was a thirty-line stub, and three of 28 "confirmed" paths existed | **TRUE** of `docs/BIOGEOCHEMICAL_AND_COMMS_REVIEW.md` (lines 20, 52-66) |
| 20 | "Verify whether PID controllers are called by live modules" | **Settled:** only by the cycle classes' own methods. The one live reader (`api/cycles.py`) reports gains and readings and calls no controller. No controller output reaches a ledger, a transfer or the fund |
| 21 | "Capital Fund Mesh" as the name of the live capability | **PARTLY.** `mesh/` is a subfolder of the unreached package; the live route calls itself the "Sovereign Capital Fund" |
| 22 | FU-813 is the bounded core of the third-cell request and needs no new cell; a people capability is separately chartered | **TRUE** (rulings of 2026-10-11) |
| 23 | Line references in the 11 October handoff (mount 340-343, payout 538-557, transfer 657-676) | **FALSE**, each by 30 to 40 lines. The 12 October document's references are right |
| 24 | Making Tax Digital for Income Tax: over 50,000 from 6 April 2026, over 30,000 from 6 April 2027, over 20,000 from 6 April 2028 | **CONFIRMED** on the HMRC page read 2026-10-12 (it shows "Updated: 7 September 2026") |
| 25 | GOV.UK's business finance finder and "Find a grant" do what the prompt says | **CONFIRMED** on both pages read 2026-10-12. Neither is called by anything here |
| 26 | VAT Notice 700 and the FCA pages | **NOT CHECKED** |

### 20.2 What is sound, and already the rule here

Extend what exists and build no second ledger, planner, scheduler or approval chain; virtual WST is never cash,
revenue, raised capital or a return; a proposal, a reservation, an approval and a payment are four different
states; a prepared instruction is not a payment and an offer is not money received; a model's confidence is not
a gate and a validator returning true is not compliance; no "compliant" badge without a stated scope and date;
a store that cannot be read is refused and never answered as zeros; nothing is committed, deployed, sent,
filed or paid by a document's say-so; real money, authentication, sign-up, external models and deployment are
the Owner's switches. Each is a ruling or a clause in force, and the documents largely say so themselves.

### 20.3 What is declined, and why

| Asked | Decision |
|---|---|
| Real-currency books for a "genuinely established entity" | **Not built.** The Owner is unincorporated and the legal form is undecided; there is no entity whose books these would be. A real-currency figure may at most be a declared memo field (20.5) |
| A tax rules layer, jurisdiction packs, draft computations, filing | **Not built.** A tax figure computed here would be a model's or a table's guess presented as an obligation. An obligations calendar holds only what the Owner declares, with its source and the date it was read, and says nothing is filed |
| Bank feeds, statement import, payment providers, "approved payment execution" | **Declined** while `REAL_MONEY_ENABLED` is off. A payment in the slice is a virtual posting, labelled as one |
| Funding search run by the platform; applications sent | **Declined.** External search is behind `AI_ALLOW_EXTERNAL`; nothing is submitted by the platform. A pipeline of records the Owner enters is buildable |
| "Capital Fund Mesh", "VSB Treasury & Capital Stewardship", autonomy levels 0 to 4, an eleven-step governing loop, a seven-class truth vocabulary | **Vocabulary not adopted** (ruling of 2026-10-09, evening, applied to a new brief). The product's own words stand; the one naming question is the tree's own (20.5) |
| Decimal amounts in place of floats | **Not as a migration.** The ledger rounds to two places at every write and refuses a non-finite figure at save; the reading found it consistent. New record types (an invoice line) may hold integer hundredths; the ledger's stored shape is not changed |
| Maker-checker, dual approval, role matrices on every action | **Not buildable as asked** with one principal. The existing hold, an explicit decision, and the recorded "decider was also submitter" (W672) are the control; the rest is the readiness round of P4.1 |
| The eight-point definition of done as a gate on this plan | **Mapped, not adopted:** isolation and separation of duties wait on authentication; duplicates, balanced journals, traceable corrections, reconciliation and the intact queue are clauses of the item proposed below; "tax calculations keep source rules" has no subject, since nothing is calculated |
| Applying the supplied patch | **Not applied.** It was not supplied, and W672 already does more |

### 20.4 What it adds

Reading for these documents found things the audits had not, all in what exists today:

1. **The payout half of FU-794 is still true and the row is closed.** A payout is recorded for any owner name,
   writes no audit event, names no requester, is never held at any amount, and its only history is a list cut
   to 200 entries. No test sends the name. W672 fixed the fund and did not touch this file.
2. **Nothing carries a request key.** A transfer request sent twice is two transfers: the ledger is safe to
   replay on an id, and the route mints a new id each time. A posting has no identifier at all, so no
   correction or settlement can name one, and the posting function accepts a zero or negative amount.
3. **A deleted fund store reads as a new fund of 10,000,000 WST**, to readers and writers alike.
4. **The capital fund product package is reached by nothing.** Inside it: a Stripe adapter with live charge and
   payout calls that reads no real-money switch (unreached, and `stripe` is not installed - the shape W535
   fixed in the crypto adapter); a banking adapter that returns "VERIFIED, JP Morgan Chase" for any token and a
   settlement adapter that returns a fixed "SUCCESS", both under docstrings saying "live"; and four modules
   that open a Firestore client at import, which FU-346 fixed in one file only.
5. **What a slice can reuse is more than the documents knew:** service contracts between entities already run
   offer, accept, deliver and settle with a transfer that is safe to retry; a period close exists; the hold and
   release mechanism now has a class with no threshold. An invoice here is a record over those, not a new
   system.

Each is a finding from reading, to be driven first. They are filed as rows; the capability is proposed as one
plan item, scoped to what is honest with money virtual, authentication off and no legal form.

### 20.5 What the Owner ruled (2026-10-12)

The questions this reading raised were put to the Owner with a recommendation each, and ruled the same day:

1. The capability is chartered as one plan item after the people capability, six clauses, virtual only, built
   in about four rounds; the rows of 20.4 on the payout and the ledger are fixed first.
2. The payout request's owner field is removed: the payee is the account's recorded owner.
3. Every owner payout is held for a person's approval, with no threshold, as every fund allocation is.
4. The product package under `products/capital_fund/` is archived as a reversible move, after a reachability
   check; the live fund is untouched.
5. Invoices are on a cash basis first: a transfer's receiving side is already counted as revenue, so
   recognising an invoice at approval would count one sale twice.
6. An invoice names only the Owner's own registered entities until authentication is on.
7. Every invoice settlement is held for a person's decision.
8. A real-currency figure may be entered only as a declared note on the financial profile or on an
   obligation: never summed with WST, never posted.
9. The obligations calendar suggests nothing; the Owner enters each obligation with its source and the date
   that source was read.
10. Only the Owner records a funding state, by hand; the platform prepares drafts and sends nothing.
11. The name a person reads is "Capital Fund"; "Sovereign" is dropped from it.

Unchanged by any of this: no real currency is posted, no tax is computed, nothing is filed, no bank is
connected, no payment is made, and nothing is called compliant.

## 21. Addendum (W674): the count section 6 said had not been made

Section 6 suspected that availability — a surface offering a capability that cannot run here — is a defect class
the audits find one surface at a time, and said it had not been counted. It has now been counted, against ledger
v16 (2026-10-11), over every finding standing at tier 1 or tier 2: 21 and 30, 51 in all.

| class | tier 1 | tier 2 | all |
|---|---|---|---|
| A — a capability whose required resource is not available here | 4 | 5 | 9 |
| mixed — one half A, one half another false statement | 1 | 0 | 1 |
| B — a statement false for another reason | 16 | 14 | 30 |
| C — a missing control | 0 | 7 | 7 |
| D — other (a true surface that leaves out a fact not about availability) | 0 | 4 | 4 |

The ten with an availability half, and whether the Instrument Cell's check reaches them:

| finding | the unavailable resource | reached by the check |
|---|---|---|
| R3.2 (tier 1) | the local model tier, named as the provider while the floor served | no — not a registered resource |
| R5.1 (tier 1) | a catalogue feature whose endpoint answers "not implemented" | registered; needs a kind of need the check lacks |
| R5.17 (tier 1) | the heartbeat's levers ("self-running", said unconditionally; true when audited) | no — not a registered resource |
| R6.2 (tier 1) | a lever's consumer, which can never fire | no — not a registered resource |
| R4.2 (tier 1, mixed) | the POT package, stated installed and not installed | no — not a registered resource |
| R3.7 | running agents, behind sixteen role definitions labelled "live" | no — not a registered resource |
| R4.3 | a model above the floor (the genome's defaults shown as a run) | registered; the completion need counts the floor as met |
| R4.4 | a consumer for a switch nothing reads | no — not a registered resource |
| R5.2 | two pages a blueprint launches that do not exist | registered; the backend cannot read the page table |
| R5.3 | a model above the floor (the realm, said to shape every result) | no — not a registered resource |

What it shows:

- Availability is a real class and a minority one: 9 of 51 (10 with the mixed finding), 4 of the 21 at tier 1.
- The check built for clause 1 would have prevented none of the ten. Seven are on surfaces the registry does not
  hold. Three are on registered resources and need a kind of need the check does not have — above all "a model,
  not the floor", which the completion need cannot say: it counts the floor as meeting it.
- So section 6's sentence, that a declared and checked availability per resource "would close the class at the
  registry instead of per page", does not hold as written. The rule carries (read it now, where the statement is
  made); the registry does not reach most of the places the statement is made. Clause 1 is new capability for
  the fabric. Finishing its remaining declarations will not move the tier-1 count.
- The larger class is the other false statement: 30 of 51. Its repeating shapes are a literal status word, a
  caller's claim printed as the platform's, a stored copy read as the present, and a figure whose name says more
  than its arithmetic.

What it does not show:

- It is a classification by reading, by one reader, of each finding's own text in the ledger. Nothing was
  reproduced and the refuters' paragraphs were not read. Eleven of the 51 classes are uncertain; read strictly
  the availability count is 5, read widely 14.
- Five further findings arise only because the floor served, and are not counted: the surface knows the floor
  served and derives a figure or a mark as if it had not.
- Every region of v16 reached its cap, so 51 is the share among the most consequential findings listed. Tier 3,
  where a disclosed unavailable capability sits, was not classified.
- The count is of v16 and is not carried to another edition. Class by finding — B: R1.0, R1.1, R2.0, R2.1, R2.2,
  R2.3, R2.4, R3.1, R4.0, R4.1, R4.10, R5.0, R6.0, R6.1, R6.3, R6.4, R1.2, R1.3, R1.6, R2.6, R2.7, R3.0, R3.5,
  R4.6, R4.8, R4.9, R5.4, R6.6, R6.7, R6.8. C: R1.4, R2.5, R3.4, R3.6, R4.7, R6.5, R6.9. D: R1.5, R2.8, R3.3,
  R4.5. A and mixed: the table above.

**Built in the round that landed this section (W674):** a need kind that says "a served model, not the
floor" and one that says "nothing is needed, and this was read to conclude it"; all 41 registered resources
now declare, and one that does not is refused when the registry is built. Of the three findings on registered
resources that reaches ONE, and only in part: the genome can now be declared to need a served model, and whether
it is REQUIRED (so that it reads unavailable here) is the Owner's to rule. The other two need a check that calls
the feature or reads the page table; they are filed. None of this reaches the seven that are not resources, and
this section is the reason nobody should say it does.
