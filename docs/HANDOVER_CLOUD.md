# HANDOVER A — CLOUD CONTINUATION

**Written** 2026-09-29 (W514), on the desktop session, because credits are running out.
**For** a cloud Claude Code session that picks the work up in the meantime.
**Paired with** `docs/HANDOVER_RETURN.md`, which is for the Owner's return on **Friday 2026-10-02**. Read both:
this one says what to do, that one says what you will be held to.

---

## 0. The one thing to do first

```bash
curl -s localhost:8000/api/v1/method/handover | python -m json.tool
```

This handover is **prose and goes stale**. `/method/handover` is **computed** from `docs/FOLLOWUPS.json`, the
plan and `docs/DELIVERY_METHOD.json` — the three artefacts that outlive a working context. Where this document
and that surface disagree, **the surface is right and this document is out of date.** Also run
`python scripts/followups.py priority` — it orders the open rows by vision value, and it is where a round starts.

---

## 1. State at handover, and how each figure was obtained

| | figure | method |
|---|---|---|
| branch | `main` at `9faea607` | `git log` |
| plan | **27 of 73 items** — P1 18/18 · P2 9/17 · P3 0/27 · P4 0/6 · P5 0/5 | distinct `P<n>.<n>` ids in the prompt. **`P3.0` is excluded deliberately**: it is not a build item but the slot for an OWNER RULING inside Phase 3 (the §10 bar-wording half sits there). Counting it as an item would inflate Phase 3 to 28 and put a number on the plan that no one can build down |
| register | 312 rows — **54 open**, 247 done, 11 dropped | `docs/FOLLOWUPS.json` |
| where the open rows sit | P2.4 **15** · P3.12 8 · P2.17 7 · P3.17 5 · P3.15/P3.16/P3.19/P3.23/P3.27 2 each · P2.13/P3.2/P3.14/P3.18/P3.20/P3.24/P3.25/P4.4 1 each · **OWNER 1** | grouped by `slot` |

**A dropped row is one measured and REFUTED**, not one abandoned — two were dropped in W507 because the code
they accused did not do what they claimed. Dropping a row is a legitimate outcome; abandoning one is not.

### In flight, uncommitted — W513
Five modified files: `docs/FABLE_DELIVERY_PROMPT.md` (adds P3.26 TURNOVER, P3.27 SELECTION),
`docs/FOLLOWUPS.json`, `docs/WORKSTATION_IDBO_LIVING_PLAN.md`, `docs/WORKSTATION_IDBO_WHOLE_VISION.md`
(§8 `Recorded W512`, §16 pointer, §18 six Owner decisions), `integration_tests/test_mvp_spine.py` (two guards).

**The W513 suite was still running at handover and had ONE failure at ~78%.** It is not diagnosed. Do not
commit W513 until you have read `/c/tmp/w513ser.log`, named the failing test, and either fixed it or recorded
why it is unrelated. **A red suite is not a state you may build on top of.**

---

## 2. Hard constraints. These are not style preferences — each one is a scar

**Run pytest ONLY with an isolated, FRESH store, and never two suites at once:**

```bash
rm -rf /c/tmp/run1 && mkdir -p /c/tmp/run1 && DATA_DIR=/c/tmp/run1 WORKSTATION_DATA_DIR=/c/tmp/run1 WORKSTATION_UEG_PATH=/c/tmp/run1/ueg.json PROJECTS_DIR=/c/tmp/run1/projects AI_DISABLE_LOCAL=1 python -m pytest integration_tests/test_mvp_spine.py -q --no-header -p no:warnings
```

Two concurrent suites corrupt the shared `memory.json` and UEG ledgers and produce ~40 false failures. The full
run takes **about 50 minutes**. **Do not touch the tree or a running suite's store while it runs** — two full
runs were lost that way in W507. Tests must resolve store paths via `config.data_path` / `obj.storage_path`,
**never `os.environ`** — CI sets no `DATA_DIR` and this has broken CI three times.

**Never flip** `AUTH_ENABLED`, `SELF_SERVE_SIGNUP`, `AI_ALLOW_EXTERNAL`, `REAL_MONEY_ENABLED` in a config file.
(Setting one in a probe subprocess or via monkeypatch inside a test is fine.)

**Owner-gated — do not touch without an explicit instruction:** real-money rails, live Stripe, managed
Postgres, production deploy, a live external AI key. All money in this platform is **virtual WST**.

**Never "fix" missing user context by enabling gateway recall.** `augment=False` at all 57 sites is deliberate
and now explicit. `owner_id` is for attribution of what was produced, never for retrieving another request's
content — conflating the two caused W489's twenty-nine-caller defect.

**Faith content:** never AI-generate Quran Arabic; sources are quran.com, alquran.cloud, tanzil.net only; AI
content is labelled; recitation is never scored; never type scripture into a test. **Ruling A.9.5: the Fitrah
Spectrum is never a measurement, and no AI verdict is passed on a person's spiritual state.** An Owner-typed
reflection is the Owner's own words and is not an inference.

**Mechanics:** preserve per-file EOL (`git ls-files --eol`; `WHOLE_VISION.md` and `LIVING_PLAN.md` are **CRLF**,
the rest LF) — never `sed -i` a CRLF file. Commit with an **explicit file list**, never `git add -A`. Never bare
`git stash` / `stash pop` (`stash@{0}` must survive) — snapshot with `git stash create`. Never push escape
sequences, en dashes or backticks through a heredoc; use Write/Edit or a file-based patch script that
**asserts every replacement**. `data/` is gitignored and must never be committed. `gh` needs a `GITHUB_TOKEN=`
prefix (an invalid env token shadows the keyring login).

**Do not edit `docs/FOLLOWUPS.json`, `docs/FABLE_DELIVERY_PROMPT.md` or `docs/WORKSTATION_IDBO_LIVING_PLAN.md`
while a suite or blind sweep runs** — `test_mvp_spine.py` reads the prompt doc.

### Push policy for you specifically

**Work on a branch (`cloud/W5xx-<topic>`) and do not push to `main`.** Every round of this project lands on main
after a green suite read by the session that ran it; you cannot hand that reading to the Owner after the fact.
Commit freely on your branch, push the branch, and leave `main` alone. Doc B tells the Owner to verify your work
before merging, so a branch is what that instruction expects to find.

---

## 3. The method is machine-readable — use it, don't re-derive it

`docs/DELIVERY_METHOD.json` holds 90 lessons in 12 groups, 43 of them enforced by a named guard. It is served
and checkable:

| call | what it gives you |
|---|---|
| `GET /api/v1/method` | the whole register with live breach counts |
| `POST /api/v1/method/check` | **check your intended change against the method before making it** |
| `GET /api/v1/method/forecast` | how long work of this shape has taken, in rounds |
| `POST /api/v1/method/screen` | the six defect classes, as pattern recognition over a diff |
| `GET /api/v1/method/appraise` | the Appraisal Cell — 11 faculties over 4 axes and a temporal spine |
| `POST /api/v1/method/breach` | record a breach. **The third breach of one lesson escalates to Change Control** |

**Record your breaches.** The loop escalated three times on the desktop session's own repeated mistakes, which
is the mechanism working. A hidden breach is worth less than a recorded one.

### The lessons that cost the most, stated plainly

- **An item closes on its ACCEPT clause, not on row counts.** No P2 item closed in 48 rounds because 17 of 48
  open build items stated no ACCEPT clause — nothing to check them against. An item's listed deliverables ARE
  its bar: transcribe them and guard them. **Zero rows against an item means UNEXAMINED, not nearly closed.**
- **Prose is never the measurement.** Check the field, the binding, the AST — never source text. A comment
  naming a forbidden field satisfies a grep.
- **A guard must DRIVE its precondition, never observe the ambient environment.** A guard that reads a dirty
  tree, a one-outcome exit code, or a beat that happens to be stopped cannot fail.
- **Make a new instrument fail first.** Green is evidence only if red was reachable. Three instruments that
  could not fail reported success (one slept four hours).
- **Refute the round's own diff.** 25 of 29 verified findings in W488 were the round's defect class
  re-committed inside its own fix.
- **A found-but-not-done task goes in the register** via `scripts/followups.py` **in the same commit**
  (`drop` takes `--note`; `reslot` takes `--gate` / `--slot`).
- **Search the archive before concluding absence.** Run `python scripts/recovery_audit.py` — the cleanups MOVED
  516 files into `_archive/` and deleted 3, so a delete-only search misses almost everything. The desktop
  session concluded "absence" from a single location **four times in one night** and was wrong each time.

---

## 4. What to actually work on — in this order

### Round 1 (do this one first): FU-160, measured and ready

Scope narrowed at handover to **one root cause with a named two-module fix**.

`vbs/quality.py:326` computes `_floor = floor_served(served_by)`, and `NOT_ASSESSABLE_BASIS` declares that for
floor-served content *"coverage cannot fail by construction and the stub regex never matches its vocabulary"*.
Line 336 then threads **those very two figures** into `screen_compliance` **regardless of `_floor`**. Downstream
`compliance/ethical_engine.py:119` reports **`quality: pass — QMS delivery coverage 1.00, no stub`** over a
figure its own gate says cannot fail, labelled `coverage="metrics"`.

**Both easy fixes are wrong, and this is the whole value of the measurement:**

1. Passing `delivery_coverage: None` makes it **worse** — the `in` test still passes, `float(None or 0.0)` is
   `0.0`, and the dimension flips to a **fabricated failure**: `quality: review — Low delivery coverage (0.00)`.
2. Omitting the key falls through to *"No QMS metrics supplied for this subject"* — which is **false**. Metrics
   were supplied and are unassessable; that is a different fact. The status becomes right and the basis becomes
   a lie.

So: `quality.py` withholds **both** figures when `_floor`, passing
`{"coverage_not_assessable": NOT_ASSESSABLE_BASIS}`; `ethical_engine.py` gains a branch **before** the coverage
branch, emitting `_dim("quality", "not_assessed", <the floor basis>, coverage="not_assessable")`. Import the
constant, never restate it — `SAFETY_FRAMEWORKS` and `_assessed()` already set that pattern in this file.

**The guard must drive BOTH legs:** same content and sections, once with `served_by="native"` and once with a
model name. Floor leg — no dimension is `pass`, quality is `not_assessed`, and its reason contains neither a
coverage number nor "no stub". Model leg — quality IS `pass` with `coverage="metrics"`. Without the model leg
the fix could have disabled the dimension outright and stayed green. Assert on the dimension's **fields**, never
on the reason's wording, and not on `overall` (W483 already made it insensitive to this).

Already **done**, do not re-fix: the tooltip half of FU-160 is satisfied — `api.ts:277` `layerTitle()` renders
"N of 7 declared layers contributed a value" and "code exists but nothing calls it".

### Round 2: FU-276, split into two rows — 57 gateway provenance sites, 52 without an owner

Measured on the AST: **13 have an owner reachable up the enclosing chain** (a mechanical thread — the row's real
ask) and **39 have no owner anywhere** because there is no user: background paths, internal helpers,
heartbeat-driven work. Threading an owner into those 39 would **invent** an attribution, which is the
fabrication class rather than a fix for it. The honest answer for the 39 is `owner_id=None` **with a recorded
reason** ("produced on the beat, not for a user"), as a *field* — because today the absence is silent and a
reader cannot tell "nobody" from "not recorded". Split the row before building.

### Round 3: the tolerant reader, FU-075 / FU-298 — 13 sites, and it needs FIVE rounds not one

The row itself forbids a single unattended pass. The conversion is
`read_json_reported(path, default) -> (value, unreadable_reason)`: the value keeps tolerant behaviour so nothing
goes down, and the reason travels with it (`None` when the store read whole **or is simply absent** — a missing
store is not an error). **The test of a conversion is not that it compiles; it is that a reader of the number is
told the number is incomplete.** Threading `why` and dropping it moves the untruth down a layer.

Order: (1) the five list-store sites, converting `api/board.py:568` and `api/swarm.py:341` **together** because
they read the same store and converting one leaves two surfaces disagreeing; (2) `integration_surface.py:434`,
whose call is inline inside a `for` and needs restructuring, plus the dict-store sites; (3) `vbs/qms.py` then
`vbs/dcms.py` — a **design change**, not a conversion, because they load into `self._state` with no response to
attach a reason to, and **`qms.py`'s default is a seeded zero, so an unreadable store reports zero gates run and
zero defects, which reads as a clean quality record** — the most consequential of the thirteen; (4) the two
`default=None` sites, each of which changes what `None` means to existing callers; (5) delete
`load_json_tolerant` and assert nothing imports it, on the import binding.

### Then, if there is room

`FU-303` self-match precision, and the **blind-harness guard** (drafted; needs the harness refactored so
`run_blinds(guards, tree, target)` is tree-agnostic and testable without paying 162 MB and a 5,040-file checkout
per worktree). `FU-310` — the consultation contract, which should go **before** P3.12 builds six engines against
an interface that forces each one to invent a confidence: all eight current constructors fabricate (0.88 in the
engines, 0.96 in MJM).

**Do not start P2.4 sweep rows wholesale.** Fifteen open rows sit there, and this session has found **seventeen
already-satisfied rows** across the register — it systematically over-states outstanding work. **Measure each
row's LIVE state before building anything.** Several of the fifteen are probably already done.

### Do not touch

The **1 OWNER-slotted row**, the **six decisions in §18** of `WORKSTATION_IDBO_WHOLE_VISION.md`, and anything
slotted **`P3.0`** — that slot exists precisely to hold the half of a question that is an Owner ruling rather
than a build (the §10 bar wording is the live example: the instrument half was built, the wording half stays
`P3.0`). They await a ruling and are not yours or mine to make. If you find work whose honest answer is a
ruling, **put it in `P3.0` and move on** rather than deciding it.

---

## 5. The round rhythm, unchanged

Measure each row's LIVE state → patch → `python scripts/selfcheck_diff.py` → guard test → blind harness with an
**asserted byte-restore** → refute the round's own diff → register + render → **full suite once** on the final
tree → commit with an explicit file list → push **your branch** → update the register.

Blind-harness rules: the anchor must match **exactly once**, restore from bytes in a `finally` with an asserted
SHA, report **BLIND(red) / VACUOUS / BAD BLIND** separately, and abort hard on exit 5. Refuters get real
worktrees, never the real repo, and never run concurrently with a break harness — a refuter once ran
`done P1.15` against the real repo mid-run. Clean up worktrees every round: they are 162 MB each, and 27 of 45
agents once died filling the disk.

---

## 6. Keeping this handover current — the refresh mechanism

A handover written *just before* a limit is written exactly when there is least capacity to write it. So the
rule is the opposite: **this document is committed early and refreshed cheaply**, and the refresh is bounded to
one section.

### The trigger is measured, not guessed

Check the account's own usage rather than estimating from how long the session feels:

```
mcp__ccd_session_mgmt__get_usage   (session_id: "self")
```

It returns each window with `percentUsed` and `resetsAt` — the 5-hour window, `Weekly · all models`, and a
**separate weekly allowance per model**. Read it **at every round boundary** (after a suite lands, before
starting the next round). Thresholds:

| reading | action |
|---|---|
| weekly **< 70 %** | nothing; carry on |
| weekly **70–85 %** | refresh §1 of this document only — the state table and the in-flight paragraph. Two minutes |
| weekly **> 85 %** | refresh §1 **and commit it**, then start no round you cannot finish |
| weekly **= 100 %** | stop starting work. Commit what is green, record what is not, and leave the tree clean |
| a separate per-model weekly window still near 0 % | that allowance is **unspent capacity**. Say so rather than stopping — the choice of model belongs to the Owner, but the fact is yours to surface |

### What a refresh actually changes

**Only §1** (the state table and *In flight, uncommitted*) plus the **head of §4** if the round order moved.
§2, §3, §5 and §7 are the constraints, the method and the Owner's priorities — they change when the project
changes, not when a round ends. A refresh that rewrites them is wasting the capacity it was called to protect.

Recorded so a refresh can tell drift from change: at the last refresh, **2026-09-29**, `Weekly · all models`
read **100 %**, resetting **2026-10-02T10:00:00Z**; the per-model Fable weekly window read **0 %**; extra usage
was **disabled**.

### The honest limit of this mechanism

**Nothing here fires by itself.** There is no scheduler behind this, and a session with no capacity left cannot
write its own handover — which is why the trigger sits at a *round boundary* rather than at a threshold that
would have to interrupt work in progress. If this document is stale when you read it, that is the mechanism
failing in its known direction: **prefer `/method/handover` and `git log`, which are computed and cannot go
stale.**

---

## 7. What the Owner cares about, so you weigh things the way they would

The core purpose, in the Owner's words: **"Success in Striving to Seeking the love and pleasure of Allah SWT
enabling supporting facilitating self and others."** The operative discipline underneath it is narrow and
absolute: **a platform may only report what it did.** Three-state verdicts everywhere — MET / UNMET /
NOT_ASSESSABLE, each with a basis. A figure may only carry the name of what it measured. **Removing a true
statement is also a defect**, so narrow an over-claim without killing the case where the strong claim was true.

The Owner's standing preference is **decide and build** — pick the recommended default and proceed; ask only
when blocked on a fact only they hold. **Honesty over polish.** If you cannot finish something, say exactly what
you left and why; do not round a red suite up to a green one, and do not describe prepared work as delivered.
