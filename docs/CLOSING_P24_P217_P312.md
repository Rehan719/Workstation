# Preparation for closing P2.4, P2.17 and P3.12–P3.19

Measured W518 while the §18.1 suite ran. Read-only. The finding is that **these items hold fewer distinct
defects than they hold rows**, and consolidating them is most of the work.

---

## 1. FU-306 is ALREADY SATISFIED IN SUBSTANCE — and it is the item-rate lever

The row asks for a command listing open rows whose named files a LATER round changed than the round that found
them, as **candidates for re-reading, never automatic closes**, because whether a row is satisfied is a reading
of the code and not a diff.

**That exists and runs.** `api/method.py:1299 _rows_the_tree_moved_under()` — the Appraisal Cell's EXTROSPECTION
faculty, built W510/W512 — is that function, with the same refusal written into its docstring. Driven against the
live register it returns **19 candidates** with `candidate_count`, `basis`, `limits` and `state`.

So the only thing missing is the **CLI entry point** the row names. That is a small addition, and arguably the
API faculty is the better surface. **Close FU-306 on measurement or reduce it to "add the CLI alias".**

**The 19 candidates are the highest-value work available**, because ~18 rows were found already satisfied by hand
in one session and the register's open count is an **upper bound on work, not a measure of it** (M-FCAST-02).
Six of the 19 sit in the target items: **FU-252, FU-259, FU-262, FU-314** (P2.17/P2.4) and **FU-226, FU-238**
(P3.15/P3.18).

**First action of the next round: re-read those 19, not build anything.**

---

## 2. P2.4 — 9 rows, about 6 pieces of work

| rows | one piece of work |
|---|---|
| **FU-075 + FU-298** | the tolerant reader. ONE job over 13 sites, and its own row forbids a single unattended pass: five rounds, `vbs/qms.py` first because its seeded-zero default makes an unreadable store read as a **clean quality record** |
| **FU-313 + FU-314** | the same class — *the register cannot record what was promised, or why anything closed*. Both block retrospection from telling a measured close from a built one. Do them together |
| FU-276 | gateway attribution: **13 threadable + 39 that need a stated `owner_id=None` with a reason**, already sized on the AST |
| FU-316 | two capped stores do not disclose that their oldest rows are gone |
| FU-318 | a dimension-level `not_assessed` never reaches a surface |
| FU-262 | extend the pre-flight to the claims group (30 of 98 labelled defects uncovered) |
| FU-164 | products.py sweep shortfalls |

**P2.4 is not closable until the tolerant reader lands**, which is five rounds by its own terms. Everything else
in it is one round each.

---

## 3. P2.17 — all six rows are ONE subject: the round's own verification budget

This is the cleanest item in the register and nobody has noticed:

- **FU-252** the suite runs twice when once would do
- **FU-301** the parallel suite stalls about one run in three
- **FU-253** the blind sweep is serial only because blinds mutate one tree
- **FU-259** a refutation round can exhaust the disk and lose most of its agents silently
- **FU-255** batches are scoped to the gate item, throwing away two thirds of each round's reach
- **FU-306** nothing detects an already-satisfied row *(satisfied — see §1)*

Every one of them is *the round wastes verification it has already paid for*. And W518 added a seventh instance of
the same subject from the other direction: **M-SESS-11**, a 48-agent fleet beside a suite cost an hour.

**Consequence:** P2.17 should be taken as ONE round that fixes the verification budget, not six. The suite is
0.90h and 36% of a round — this item is about the single largest cost in the whole method.

---

## 4. P3.12 — 8 rows, about 4 distinct defects, and two pairs are near-duplicates

| rows | the actual defect |
|---|---|
| **FU-224 + FU-310** | the consultation contract forces a numeric confidence and excludes the three meta engines. **Near-duplicates.** A patch is already drafted (`c1_consultation_contract.py`) and it goes FIRST, because building six engines against the present contract forces each to invent a confidence — the defect P3.12 exists to remove, recreated by its own interface |
| **FU-229 + FU-257** | the six engines return constants / fixed markers for any input. **Near-duplicates** |
| FU-221 | the registry is never populated, and its call contract does not match |
| FU-223 | `/api/v1/cognitive/*` returns a constant payload and reports `engines_run 9, status complete` |
| FU-275 | the engines have **no path to a model at all** — not a stub call, no import. This is the root: without it, "make them compute" is impossible |
| FU-274 | a CONSTRAINT, not a defect: the archived nine-engine bootstrap must NOT be recovered as-is |

**Order that follows from the dependencies:** contract (FU-224/310) → a model path (FU-275) → engines compute or
refuse (FU-229/257) → registry populated (FU-221) → the surface reports what actually ran (FU-223). Consolidate
the two pairs before starting, or two rounds will fix the same thing twice.

---

## 5. P3.13–P3.19 — the cheap and the blocked

- **FU-237 + FU-243** are the same class: **orphan `.pyc` files beside sources that were archived or deleted**
  (524 of them). Mechanical, cheap, and they can be done in any round as a rider.
- **FU-242** *the geospheric regulators are unwired, so no cycle setpoint is enforced anywhere* — now informed by
  two W515/W516 findings: the regulator is a **threshold comparison, not a PID controller** (FU-307, fixed in all
  three writers), and §18.1's work budget **can now run down**. So there is a coherent chain:
  **budget (built) → setpoint enforcement (FU-242) → capacity derived from the budget (§18.6)**. FU-242 is the
  next real step in Thrust A.
- **FU-235** the constitutional enforcement engine has no validators, so `validate()` always passes — the
  *"a gate that cannot refuse"* class, and it pairs with the ruling that no gate may clear.
- **FU-236** the optimal-transport router cannot solve because POT is not installed — a dependency decision of
  the same shape as FU-269's `pypdf`, so rule on both together.
- **FU-246** requires a Halo2 attestation and an OAM-QKD figure this repository cannot produce — likely a
  **refusal**, in the same family as the biomimetic refusals.
- **FU-230** the five-gate clearance chain cannot refuse and writes literal strings as signatures — same class as
  FU-235.

---

## 6. The ordering this produces

1. **Re-read the 19 extrospection candidates.** Closing on measurement is the cheapest item-rate movement there
   is, and six of them sit in the target items.
2. **P2.17 as one round** — the verification budget is the largest single cost in the method.
3. **FU-242** — the next step in Thrust A, now that the budget exists.
4. **P3.12 consolidated**, in dependency order, starting with the contract patch already drafted.
5. **The tolerant reader** over five rounds, `qms.py` first.

**And a standing rule for all of it:** a gate may never clear (the ruling), so FU-230 and FU-235 are fixed by
giving them a refusal, not by giving them validators that pass.

---

## 7. THE FINDING THAT MATTERS MOST: rule B3 of the delivery method caused tonight's red suite

`docs/FABLE_DELIVERY_PROMPT.md:638` — **B3 OVERLAP WHAT DOES NOT SHARE STATE**:

> *"The refutation workflow runs in isolated worktrees, so it runs CONCURRENTLY with the full suite (approximately
> 45 min saved). Never two pytest runs at once, and never a refuter while a break harness is mutating the tree."*

**That rule authorises precisely what cost W515 an hour.** I ran a 48-agent verification workflow beside a full
suite, on B3's licence. The suite took **1h48m34s against a measured 53m20s** and returned red on two
timing-sensitive tests, both of which passed in 81s alone.

**B3's reasoning is half right and half wrong.** Worktrees do not share STATE, so there is no data corruption -
which is what its "never two pytest runs at once" clause protects. But they do share **CPU**, and the damage from
contention is to **TIMING**, which B3 never considered. Timing damage is worse than data damage because it looks
like a real defect instead of an obvious collision.

**So B3 must be amended, and M-SESS-11 is the evidence.** The register's lesson and the plan's rule currently
contradict each other, and the rule is the one that is wrong. Until it is amended, a future round will read B3
and repeat the hour.

### The coherent next round, which is P2.17's actual subject

| what | evidence |
|---|---|
| **amend B3** — nothing heavy runs beside the suite; isolation of state is not isolation of timing | W515 measured 2.04x slowdown and two false reds |
| **amend B2** and CLOSE FU-252 — the slice during iteration, the full suite ONCE on the final tree | the row names amending B2 as its own completion step, and the practice was adopted through W515-W518 |
| correct **FU-253 and FU-259**'s premise | measured: **`scripts/blind_sweep.py` DOES NOT EXIST**. The blind sweep is an ad-hoc procedure written per round, not committed machinery, so both rows are BUILD rows and not fix rows. My prepared `s2_harness_guard.py` draft is invalid as written, because it guards a script that is not there |

That is one round, one subject, and it removes the largest single cost in the method while fixing the rule that
created it.

---

## 8. THE ITEMS CLOSE IN PARTS — and P2.17 is two thirds met already

Read the bars rather than the rows, which should have been the first move.

### P2.17 — three parts, and the ruling says "each part may be met in its own round"

| part | requirement | verdict |
|---|---|---|
| **(a) THE BUNDLE** | a proposal names a file-connected COMPONENT cut by item, COMPUTED from the row-cites-file edges rather than stated; disjointness asserted when several are combined; a bundled round's guard covers every item | **SATISFIED in substance.** `plan_followups.bundles()` computes **34 components** from each row's DECLARED files, cut by item, with a stated basis, and it FLAGS an under-declared row. What remains is the round-conduct half: a guard asserting disjointness when a round combines bundles |
| **(b) THE FIXED COST** | the parallel suite proven to produce the SAME pass/fail set as serial on the same tree before adoption; the per-worker store proven isolated by a test that would fail if two workers shared it; the blind harness runtime measured before and after | **NOT met, and it is the blocker.** FU-301 records the parallel suite stalling about one run in three |
| **(c) THE FIGURES** | the round-cost figures are computed from git and the register, never typed | **SATISFIED.** `followups.py forecast` computes PACE from the register and prints "WALL CLOCK (git, a separate measurement): 26 commit-to-commit gaps, median 4.1h"; `scripts/session_forecast.py` and `night_sim.py` compute from git, and W516 added a guard forbidding measured figures in the method documents |

**So P2.17 is (a) and (c) met with (b) outstanding.** That is a far smaller item than six open rows suggests, and
the honest next step is to close (a) and (c) on measurement rather than treat the item as unstarted.

### P2.4 — a per-CLUSTER bar, so it closes in parts too

Its ACCEPT is **derived from its rows** rather than transcribed, and says so plainly — a weaker derivation than
P2.3/P2.5, which the bar itself admits. The rules that matter for any attempt:

- the bar is **per cluster**, of four, so **the item can close in parts**;
- a cluster closes when its rows are closed **AND a named guard drives the case each row reproduced**;
- per artefact removed, the round records the check that established **reachability**;
- **no cluster closes on an import search, and none on a count alone**;
- the four legacy `gateway.query` sites (v191, v260, v290, v310) all sit on **MOUNTED routers** — v260's at `/api`
  itself — so retiring one is an **API-surface change**, not a deletion.

### The machine's own bundling confirms the manual grouping

`bundles()` cut these components without being told, and they match the clusters read by hand in §2–§4:

| component | rows | what it is |
|---|---|---|
| P3.12 | **FU-310, FU-274, FU-224, FU-221** | the CONTRACT cluster — and the patch for it is already drafted |
| P3.12 | **FU-229, FU-257, FU-275** | the ENGINES cluster, with FU-275 (no path to a model at all) as its root |
| P2.17 | **FU-253, FU-306, FU-255** | the CLI / plan_followups cluster |
| P2.17 | **FU-252, FU-259** | both cite ONLY `docs/FABLE_DELIVERY_PROMPT.md` — i.e. **the rules themselves**, which is precisely §7's B2/B3 amendment, and it is flagged `also_touching: P2.4` |

**So the rounds are pre-cut:** P3.12 is two rounds, P2.17 is two rounds, and one of P2.17's is the B2/B3
amendment that §7 shows is causing real failures.

## 9. A trap found by walking into it

`python scripts/followups.py bundles` **WRITES** — it re-renders both watched plan documents as a side effect of
a command that reads like a query. It was run here while the full suite was running, which is the one thing the
method forbids. The render happened to be idempotent (`WORKSTATION_IDBO_LIVING_PLAN.md` showed no diff), so
nothing was harmed — **but that was luck, not discipline.**

Two consequences worth carrying: during a suite, call `plan_followups.bundles(reg, prompt)` directly rather than
the CLI; and a query subcommand should not render. The second is a real defect in the CLI and belongs with
P2.17's cluster, which already owns `scripts/followups.py`.

---

## 10. P3.12 measured end to end — a dependency chain, not eight defects

Every claim below was checked against the tree, not inferred from the rows.

| # | row(s) | measured state |
|---|---|---|
| **root** | **FU-275** | **CONFIRMED.** NO file in `agentic_core/cognitive/` imports a gateway, an orchestrator, or any generate/complete call — zero matches. The engines have no path to a model at all, so "make them compute" is impossible until this exists |
| 2 | **FU-224 + FU-310** | **CONFIRMED.** `soch_engine.consult()` returns `ConsultationResponse(..., confidence=0.88)`. The contract makes confidence a REQUIRED float, so an engine that cannot judge itself must invent one - and all eight constructors do. Fix FIRST: building six engines against this contract forces each to fabricate, which is the defect P3.12 exists to remove, recreated by its own interface |
| 3 | **FU-229 + FU-257** | **CONFIRMED, and worse than the rows say.** `soch_engine.reflect()` returns `{"status": "SUCCESS", "hypotheses": ["A", "B"]}` - placeholder LETTERS, not even plausible constants |
| 4 | **FU-221** | **CONFIRMED for the cognitive registry.** `cognitive/registry.py` holds `_engines = {}` with a `register()` classmethod, and the only `.register(` call anywhere is `reactor/__init__.py:34` registering a FACTORY REACTOR. Nothing registers a cognitive engine |
| 5 | **FU-223** | **HALF ALREADY FIXED, and downstream.** `api/cognitive.py:133` now reports `engines_run: 6` with an `engines_run_basis`, and the file's own header records that it USED to report 9 over an unpopulated registry. The count is honest. The payload stays constant only because the ENGINES are, so this closes as a consequence of #3 rather than on its own |
| - | **FU-274** | a CONSTRAINT, not a defect: the archived nine-engine bootstrap must NOT be recovered as-is |

### The two rounds this produces — matching the machine's own bundling

**ROUND 1 — the contract cluster** (`FU-310, FU-274, FU-224, FU-221`, exactly as `bundles()` cut it):
make `ConsultationResponse` three-state with provenance so an engine can say "not assessed" instead of inventing
0.88; reconcile the request `Literal` of seven against the registry's nine `EngineType` values; populate the
cognitive registry; and record FU-274's constraint in place so a later round cannot recover the archived
bootstrap. **The patch is already drafted** (`c1_consultation_contract.py`), and it turns eight fabrications into
eight honest refusals without making any engine compute - which is the right first step, not a half measure.

**ROUND 2 — the engines cluster** (`FU-229, FU-257, FU-275`): give the engines a path to a model, then make each
one compute a real value **or return assessable false with a reason**. FU-223 closes as a consequence.

**Order is forced by the dependency:** contract before engines, or the engines are built against an interface that
requires them to lie.

---

## 11. The 19 extrospection candidates, worked through

| row | slot | verdict from measurement |
|---|---|---|
| **FU-237** | P3.17 | **DROP AS REFUTED.** Three measured facts kill it: the count is **150, not 524**; `git ls-files '*.pyc'` returns **0**, so not one is tracked; and **all 150 sit inside `__pycache__` with none outside it**, so in Python 3 none is importable at all - a cache entry is only used when its source exists. The row's real worry, a stale module being importable, cannot happen. This is untracked local litter, not a repository defect |
| **FU-252** | P2.17 | **CLOSEABLE.** Its fix - slice during iteration, full suite ONCE on the final tree - is the practice run all through W515-W518. The row names "amend B2 in the delivery prompt" as its own completion step, so that is the whole remaining work |
| **FU-253 · FU-259** | P2.17 | **PREMISE FALSE.** `scripts/blind_sweep.py` DOES NOT EXIST. The blind sweep is an ad-hoc procedure written per round, so these are BUILD rows, not fix rows - and the prepared `s2_harness_guard.py` draft is invalid because it guards a script that is not there |
| **FU-275 · FU-257 · FU-223** | P3.12 | measured in §10 - a dependency chain, contract first |
| **FU-242** | P3.19 | **UNBLOCKED TONIGHT.** The regulator is a threshold comparison, not a controller (FU-307, fixed in all three writers), and §18.1's budget can now run down. The chain is budget → setpoint enforcement → capacity derived (§18.6) |
| **FU-077** | OWNER | **RULED tonight**: retire the engine, keep the 494-concept Law vocabulary, never load the 293-node file manifest |
| **FU-314** | P2.4 | raised in W515; nothing can have satisfied it yet |
| FU-226 | P3.15 | post-quantum is NAMED in six modules including `security/pqc_hardening.py`; whether any signature is PERFORMED is unmeasured |
| FU-236 | P3.17 | POT not installed - a dependency decision of the same shape as FU-269's pypdf; rule on both together |
| FU-262 · FU-164 · FU-255 · FU-278 · FU-238 | mixed | unmeasured; the next preparation targets |

**Three rows resolved without writing code: one drop, one close, and two whose premise is false.** That is the
item-rate lever working exactly as M-FCAST-02 says it should - the open-row count is an upper bound on work, not
a measure of it.

## 12. The ordering, final

1. **Land §18.1** (in suite now).
2. **P2.17's rules round** - amend **B3** (it authorises running a fleet beside the suite and caused tonight's
   only red), amend **B2** and close **FU-252**, correct **FU-253/FU-259**'s premise, and stop
   `followups.py bundles` rendering as a side effect of a query. One subject, one round, and it removes the
   largest recurring cost in the method.
3. **Close on measurement**: drop FU-237, close P2.17 parts (a) and (c), close FU-306.
4. **FU-077** as ruled, and **FU-242** next in Thrust A.
5. **P3.12 round 1** - the contract, from the drafted patch.
6. **P3.12 round 2** - the engines' model path.
7. **The tolerant reader**, five rounds, `qms.py` first.

---

## 13. FU-226 measured: 3 of 5 already fixed, 2 live over-claims precisely located

| module | state |
|---|---|
| `security/pqc_hardening.py` | **FIXED.** Its own docstring now opens *"Content integrity digests. NOT post-quantum cryptography, and no longer shaped to look like it"*, and records the prior defect in full: a SHA3-512 digest padded with **4000 zeros** purely so the output would resemble a Dilithium-5 signature to anything inspecting it |
| `api/csuite.py:119` | **FIXED (W410).** `"pqc_status": "Enforced"` retired; reported as unmeasured, with *"nothing checks or enforces PQC"* stated |
| `governance/gaas/gaas.py:28` | **FIXED (W506/FU-076).** Now a content digest, named as one |
| `reactor/religion/qep_flagship.py:318` | **FIXED (W506/FU-076).** The learner's certificate no longer carries a field named for cryptography the platform does not perform |
| **`api/integration_surface.py:135`** | **LIVE OVER-CLAIM** - asserts `"pqc": "Dilithium-5 / Kyber-1024 (configured)"`. Nothing performs it |
| **`avatars/core/avatar_engine.py:33,62,69`** | **LIVE OVER-CLAIM** - *"Uses NIST-standard PQC primitives (Dilithium-5 / Kyber-1024)"*, and `avatar_id` commented `# PQC DID` |

**So FU-226 is a two-site fix with exact locations** - the same class as tonight's FU-307, and cheap.

## 14. A STRUCTURAL finding: the register mixes DEFECTS with CONSTRAINTS

**FU-238** is not a live defect. Both files it describes are in `_archive/`, **nothing live imports either**, and
the row says so itself: *"Recorded so that P3.18 recovers the SHAPE and not the code."* It cannot be fixed - only
honoured when P3.18 is built.

**FU-278** is not a defect either. It is an **ACCEPTANCE BAR** for P3.23's legal specialist - *a generated
artefact must cite a page and a line* - derived from W496 finding a ready-to-send disclosure letter built over
342 rows of "Simulated content for <filename>", asserting an exhibit reference, a punctuality figure, a
monitoring period, an Occupational Health date and a case citation, **none of which existed in anything it read**.

**FU-274** is the same shape: a constraint on P3.12, not a defect in it.

### Why this matters for every projection

M-FCAST-02 already says the open-row count is an **upper bound** on work because some rows are already satisfied.
This is a SECOND reason, and it is structural rather than incidental: **some open rows are not work at all.** They
are constraints and acceptance criteria attached to unbuilt items, and they close when their item is built to
honour them - never by a round "fixing" them.

**The fix is cheap and it makes every figure truthful:** a `kind` field on a row - `defect` | `constraint` |
`acceptance_bar` - so `forecast()` can project over defects and report constraints separately. Without it the
item rate is computed over a population that includes rows no round can close, which understates the real rate
and overstates the remaining work at the same time.

**This belongs with FU-313 and FU-314** - all three are *the register cannot record what kind of thing a row is,
what was promised, or why anything closed* - and `bundles()` already groups FU-314 with the `followups.py`
cluster.

---

## 15. The last three candidates measured — all three are smaller than their rows

**FU-164 — mostly fixed, one narrow check left.**
- **C10 (`'active'` counted every project whatever its status): FIXED by W506.** `api/products.py:816` records it
  by name, and :804 adds *"every project 'active'. Counted from the records, never assumed."*
- **C7, server side: FIXED.** The SSE done event now carries `served_by` and `is_external` (:121, :134), and :184
  documents it. `:901` records FU-164 by name and the forecast result returns both fields.
- **C7, export side: THE ONLY THING LEFT.** Whether the products export prepends the provenance header to the
  `.md` file. The helper exists in the frontend (`provenanceHeader`, used for clipboard in `MyWork.tsx`), so this
  is a one-line check and possibly a one-line fix - not a sweep row.

**FU-255 — the principle stands, the measured gain has EXPIRED.** `batches(register, prompt_text, slot=None)`
already supports an unscoped sweep, so nothing needs building; the defect is that the round *rhythm* calls it with
`--item`. But the gain the row measured is gone: it cited C3 closing **4 rows inside P1.18 against 12 rows across
four items (47 files)**, and today unscoped and scoped return the **same** result - 2 batches, class C7, confined
to P2.4 - because those rows have since been closed. So this is a cheap rhythm amendment, not the large win the
row implies. **A figure recorded without its method drifts** (M-HAND-02), and this is the third instance tonight.

**FU-262 — genuinely unbuilt.** The pre-flight covers four deterministic defect shapes plus two guard shapes; the
claims group is **30 of 98** in the labelled set and is uncovered. That one is real work, and it is the largest
uncovered group in the set.

### What the whole sweep of 19 comes to

| outcome | rows |
|---|---|
| **drop as refuted** | FU-237 |
| **close on measurement / rhythm amendment** | FU-252, FU-255, FU-306, and P2.17 parts (a) and (c) |
| **premise false - build rows, not fix rows** | FU-253, FU-259 |
| **reclassify as a constraint or bar, not a defect** | FU-238, FU-274, FU-278 |
| **narrowed to a one-line check** | FU-164 |
| **precisely located, two sites** | FU-226 |
| **genuinely unbuilt work** | FU-262, FU-275, FU-242, FU-276, FU-075/298, FU-236 |

**Eleven of nineteen are not the work their titles suggest.** That is the register's over-statement measured
directly rather than asserted - and it is why the next round should close on measurement before it builds
anything.

---

## 16. P2.4's FOUR CLUSTERS MEASURED — it needs five rows, not nine, and one cluster is a single check away

The bar is **per cluster**, so the item closes in parts. A cluster closes when its rows are closed **AND a named
guard drives the case each row reproduced**, with the reachability check recorded per removed artefact. No cluster
closes on an import search, and none on a count alone.

| cluster | rows named in the bar | state | what remains |
|---|---|---|---|
| **(a)** dead and legacy code retired or owned | FU-071, 072, 075, 076, 077, 078, 228 | **5 of 7 closed** | **FU-075** (the tolerant reader, five rounds) and **FU-077** — *ruled tonight* |
| **(b)** provenance complete on what leaves the platform | FU-247, 248, 276, 256 | **3 of 4 closed** | **FU-276** only, already sized on the AST as 13 threadable plus one decision covering 39 |
| **(c)** the W477 truth-sweep files cleared | FU-160, 161, 164, 167, 170, 187 | **5 of 6 closed** | **FU-164 ONLY** — and §15 narrowed it to whether the frontend export prepends a provenance header that already exists |
| **(d)** remaining infrastructure rows | FU-220, 260, 261, 262 | **3 of 4 closed** | **FU-262** (the claims group, genuinely unbuilt) |

**Cluster (c) is the nearest closable item-part in the whole plan** — one narrow frontend check plus a driven
guard.

**And FU-077 is nearer than it looks.** Cluster (a)'s own wording rules that *"an audit that finds nothing to wire
is a PASS for that cluster, recorded with what it read — 'audit before wire' means the audit IS the deliverable,
not a preliminary to one."* That audit was performed tonight: **neither candidate ontology file is a graph** —
the real one holds 494 concepts and rules with **zero relations**, and the other holds 293 file paths over the
Owner's own documents with **zero edges**. The Owner has ruled: retire the engine, keep the vocabulary, never load
the manifest. So FU-077's deliverable exists; what remains is executing the retirement with a recorded
reachability check, which cluster (a) explicitly requires and which cannot be an import search.

### A REAL GOVERNANCE DEFECT: rows added after a bar was written sit in NO cluster

P2.4's bar was written W505 and names its rows **explicitly, per cluster**. Five rows slotted to P2.4 since then —
**FU-298, FU-313, FU-314, FU-316, FU-318** — appear in none of the four clusters.

So the item's ACCEPT clause, read literally, can be met while five slotted rows remain open. Either the bar no
longer covers the item's work, or those rows do not belong to the item. Both readings are a problem, and the
current state is that nobody has chosen.

**This is the mirror of the M-MEAS lesson that an item closes on its bar:** a bar that enumerates rows must be
amended when a row is added, or it silently stops being the bar. The cheap fix is that `followups.py add` warns
when a row is slotted to an item whose ACCEPT clause enumerates rows, and `check` reports the discrepancy — which
is the same CLI cluster as FU-314 and belongs with it.

### What this makes the shortest honest route to closing P2.4

1. **FU-164** → closes cluster **(c)**.
2. **FU-077** as ruled → with FU-075 still open, cluster (a) stays open, but the audit half is done.
3. **FU-276** (thread the 13, record the 39) → closes cluster **(b)**.
4. **FU-262** → closes cluster **(d)**.
5. **FU-075/FU-298** the tolerant reader, five rounds → the last of cluster (a).
6. **Decide** whether the five post-W505 rows join a cluster or are declared outside the bar.

**Three of four clusters are within one or two rows of closing.** That is a very different picture from nine open
rows, and it came from reading the bar instead of counting the rows.

---

## 17. THE BIGGEST FINDING: P3.12 is closable in ONE round, and it would be the first P3 item ever closed

Its ACCEPT clause, in full:

> *"an engine's output changes with its input, **or it says assessable:false with the reason**; every result carries
> what served it; no page shows a number an engine did not compute; guard + blinds + a fresh-backend probe."*

**Criterion 1 is a DISJUNCTION.** An engine satisfies it by **honestly refusing**. So the bar does NOT require the
engines to compute — and **FU-275 (no path to a model at all) therefore does not block this item.** Giving the
engines a model is P3.13's kind of work, not P3.12's bar.

| criterion | state |
|---|---|
| **1. output varies with input, OR assessable:false with a reason** | **delivered by the contract round.** The drafted patch (`c1_consultation_contract.py`) makes `confidence` optional with a `confidence_basis` and `ValidationResult.passed` three-state, turning all eight fabrications - `confidence=0.88` in the six engines, 0.96 in MJM - into eight honest refusals |
| **2. every result carries what served it** | **delivered by the same patch**, which adds `served_by` and `is_external` to `ConsultationResponse`. Without them the cognitive layer would be the one place this repository's provenance discipline stops |
| **3. no page shows a number an engine did not compute** | **ALREADY SATISFIED — verified across all twelve frontend files that mention this area.** `KnowledgeHub.tsx:180` renders a confidence ONLY when present, and :56-57 record the prior defect (*"a confidence of 1 that came only from a floor"*) as removed. `ResourceFabric.tsx:191` is a user INPUT label. `CognitionIntegration.tsx` shows only API-coverage figures, explicitly labelled *"routers mounted and stores non-empty — not delivery"*, corrected in W496 |
| **4. guard + blinds + a fresh-backend probe** | the round's own work |

**So P3.12 needs one round: apply the contract patch, change eight constructors from a fabricated number to a
stated refusal, and write the guard with a fresh-backend probe.** Its eight rows resolve as: FU-224 and FU-310 are
the round; FU-229 and FU-257 are satisfied BY the refusal (an engine that says assessable:false no longer returns
a fixed marker as a claim); FU-223 follows; FU-221's registry is populated in the same patch; FU-274 is a
constraint recorded, not built; and **FU-275 moves out of this item's bar**.

**Why this matters beyond one item.** P3 stands at **0 of 27** and the plan's own forecaster warns that its item
rate was measured on P1/P2 work and is being applied to phases whose work differs. Closing P3.12 would be the
first P3 datum — which is worth more than the item itself, because every projection over P3 is currently an
extrapolation from a population that contains no P3 evidence at all.

### Revised ordering, with P3.12 promoted

1. **Land §18.1** (in suite).
2. **The rules round** — B3 (it caused tonight's red), B2 + FU-252, batches scoping + FU-255, the
   `bundles`-writes trap, the enumerated-bar defect, drop FU-237, close FU-306 and P2.17 (a) and (c).
3. **P3.12 in one round** — the contract patch. **First P3 item, and the cheapest item on the board.**
4. **FU-164** → closes P2.4 cluster (c).
5. **FU-077** as ruled; **FU-276** → closes cluster (b); **FU-262** → closes cluster (d).
6. **FU-242**, then the tolerant reader over five rounds.
