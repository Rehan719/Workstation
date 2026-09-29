# HANDOVER B — RETURN BRIEF

**Written** 2026-09-29 (W514). **For** the session resuming on **Friday 2026-10-02**, when credits reset.
**Paired with** `docs/HANDOVER_CLOUD.md`, which is what the cloud session was told to do in the meantime.

The purpose of this document is narrow: **do not trust the interval, verify it.** A cloud session working
unattended against this repository will have had no Owner in the loop, no green-suite reading handed to anyone,
and no ability to answer the six questions that await a ruling. Everything below assumes its work is a
**proposal**, not a delivery.

---

## 1. Resume in this order. Do not skip step 2

```bash
cd /c/Users/rehan/Workstation
git fetch --all --prune
git log --oneline main..origin/main          # did anything land on main? It should NOT have
git branch -r --sort=-committerdate | head   # the cloud branches, newest first
git status --short                           # is W513 still uncommitted?
curl -s localhost:8000/api/v1/method/handover | python -m json.tool
python scripts/followups.py priority | head -20
```

**Step 2 is `git log --oneline main..origin/main`.** The cloud session was instructed to work on
`cloud/W5xx-<topic>` branches and **leave `main` alone**. If commits landed on `main`, that instruction was not
followed, and the first task is to establish what they are and whether a green suite was ever read on the final
tree — not to build on top of them.

---

## 2. The state you left, so you can tell it apart from what changed

| | at handover (2026-09-29) |
|---|---|
| branch | `main` at `9faea607` |
| plan | **27 of 73 items** — P1 18/18 · P2 9/17 · P3 0/27 · P4 0/6 · P5 0/5 |
| register | 312 rows — 54 open, 247 done, 11 dropped |
| uncommitted | **W513**, five files, suite **not green** |
| capacity | `Weekly · all models` **100 %**, resetting **2026-10-02T10:00:00Z**; the per-model **Fable** weekly window **0 %**; extra usage **disabled** (`get_usage`) |

**Why the interval may be shorter than you expect.** The weekly allowance was **already exhausted** when this
was written, so the desktop session may have stopped mid-sentence rather than at a clean round boundary. Judge
the interval by `git log` and the tree, not by where this document's narrative ends. One consequence worth
checking first: **the Fable weekly window was untouched at 0 %** — if nothing used it, that capacity expired
unspent at the reset, and it is worth deciding in advance whether a future squeeze should draw on a per-model
allowance rather than idle until Friday.

### The unfinished thing that matters most

**W513's suite had ONE failure at ~78% and was never diagnosed.** Five files were modified and not committed:
`docs/FABLE_DELIVERY_PROMPT.md` (P3.26 TURNOVER, P3.27 SELECTION), `docs/FOLLOWUPS.json`,
`docs/WORKSTATION_IDBO_LIVING_PLAN.md`, `docs/WORKSTATION_IDBO_WHOLE_VISION.md` (§8 `Recorded W512`, §16
pointer, §18 the six Owner decisions), `integration_tests/test_mvp_spine.py` (two new guards).

Two of those five files are **CRLF** (`WHOLE_VISION.md`, `LIVING_PLAN.md`); the rest are LF. Check
`git ls-files --eol` before touching any of them, and check `git diff --stat` afterwards for an EOL flip.

**Read `/c/tmp/w513ser.log` first and name the failing test.** The likely candidates are the two guards W513
itself added — a round's own new instrument is the most probable cause of that round's only failure, and W488
measured that 25 of 29 verified findings were the round's defect class re-committed inside its own fix. Refute
the guard before you edit the code it accuses: the W502 lesson is that **a vacuous blind may accuse working
code**, and "fixing" correct code on a bad instrument's word is the expensive failure here.

---

## 3. Verifying the interval's work before merging any of it

For each `cloud/*` branch, in this order. Stop at the first failure and do not merge past it.

1. **Read the diff, not the commit message.** `git diff main...cloud/<branch> --stat`, then the full diff of
   anything touching `agentic_core/api/`, `vbs/quality.py`, `compliance/`, or the watched plan docs.
2. **Was a full suite run on the FINAL tree?** Not on an earlier commit of the branch. If the branch's last
   commit changed code after the suite ran, the suite did not test what is being merged. Re-run it yourself —
   50 minutes, fresh isolated store, one suite at a time.
3. **Did every new guard fail first?** For each guard added, break the thing it checks, watch it go red, restore.
   A guard that cannot fail is worse than no guard, and three such instruments reported success in W498–W500.
   Check specifically for the vacuous shapes: an assert containing the literal it forbids (it matches itself), a
   presence check over a JSX conditional (the field is named in both the gate and the body, so it survives
   `{false && ...}`), and a guard that observes the ambient environment instead of driving it.
4. **Was every found-but-not-done task registered?** `git diff main...cloud/<branch> -- docs/FOLLOWUPS.json`. A
   round that fixed things and registered nothing either found nothing — unlikely — or dropped what it found.
5. **Did an item close, and on what?** An item closes on its **ACCEPT clause**, never on row counts. If a branch
   claims an item, read that item's ACCEPT clause and check each criterion yourself. Zero rows against an item
   means **unexamined**, not nearly closed.
6. **Check the truth discipline held.** Any new figure must carry the name of what it measured; any new verdict
   must have three states with a basis; no over-claim was narrowed in a way that killed a case where the strong
   statement was true.

Then merge, one branch at a time, and run the suite once more on `main` after the last merge.

---

## 4. If the interval produced nothing usable

That is an acceptable outcome and costs you almost nothing. Delete the branches, commit W513 once its failure is
resolved, and pick up **Round 1 of `docs/HANDOVER_CLOUD.md` §4** — FU-160, which is fully measured: one root
cause in `vbs/quality.py:336` threading a floor-served coverage figure into the ethical screen regardless of
`_floor`, a named two-module fix, **both obvious fixes identified as wrong**, and a two-leg guard specified. It
is the cheapest real round available and it does not depend on anything the interval did.

The ordered queue after it, also in that document: FU-276 split into 13 threadable sites plus one decision
covering 39; then the tolerant reader across five rounds, `qms.py` first because its seeded-zero default makes
an unreadable store read as a clean quality record.

---

## 5. What is yours alone, and still waiting

Nothing in the interval can have resolved these, and the cloud session was told not to touch them.

- **The six decisions in §18 of `docs/WORKSTATION_IDBO_WHOLE_VISION.md`**, filed 2026-09-29 with the Vision 8.0
  integration (`cca-66b4dab2e0`). They are integrated into §8 and §16 and carry two new plan items, P3.26
  TURNOVER and P3.27 SELECTION — which is why W513's prompt diff must land before work starts against them.
- **The one OWNER-slotted register row**, plus anything the interval slotted into **`P3.0`** — the slot that
  holds the half of a question which is a ruling rather than a build. Check it on return: a cloud session that
  worked honestly will have *added* to it, and those additions are questions addressed to you.
- **FU-077** — wire the Law ontology or retire the engine. Worth ruling on as one question rather than six: the
  prior `products/` work left six domain rule packs of 139–544 bytes each, which is the same shape as FU-077
  (a named rule pack that governs nothing) repeated per domain. One ruling can cover them all.

---

## 6. One measured caution about the interval

An unattended session optimises for closing rows, and this register **systematically over-states outstanding
work** — seventeen already-satisfied rows were found in a single session. That cuts both ways on return:

- a branch that closed several rows may have closed them **correctly and cheaply**, by measuring that the work
  was already done. Check for a recorded measurement, and if it is there, that is a good round.
- a branch that closed several rows **by building** should be read harder, because some of what it built may
  already have existed. The four-times-in-one-night mistake was concluding absence from a single location, and
  `python scripts/recovery_audit.py` exists because the cleanups **moved** 516 files into `_archive/` rather
  than deleting them.

The distinction to look for is whether each close names **the state it measured** or only the change it made.
