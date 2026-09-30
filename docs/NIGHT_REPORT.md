# Night report — 2026-09-29 into 2026-09-30

Written at 05:52 UTC, **before** capacity ran out rather than after, which is the point of writing it at all.
`git log --oneline` is the authoritative record; this says what it means and what was left.

**Committed to 1 round. Expected 2. Delivered 3, plus the method regeneration and the Vision 8.0 update** — the top of the measured range, not a beaten estimate.

---

## What landed

| commit | what |
|---|---|
| `aa0b5d0e` | the night plan runs THROUGH Workstation, and its first round makes Workstation able to hold it |
| `c69439b9` | the session method regenerated from an adversarial audit of itself — and the commitment halves |
| `adcf22aa` | **Round A** — a floor-served coverage figure stops becoming an ethical verdict; Horizon stops claiming it is blocked |
| `2f55a20d` | the third external biomimetic brief, interrogated — 21 of 72 assessments were a rename |
| `eb14f3b9` | **Round B** — a constitution that names how each article is checked and records its own breaches |
| `8cde45bc` | this night report, written before capacity ran out |
| `cb075956` | **Round C** — the select screen stops spending half its report on shapes its own definition excludes |

**Suites:** Round A 491 passed / 15 skipped (52m33s); Round B 493 passed / 15 skipped (51m24s). Exit codes
captured explicitly both times. Pre-flight at Round B: **0 leads over 11 files**. `tsc --noEmit` clean.

**Register:** 10 rows closed (FU-071, 072, 160, 187, 228, 295, 302, 304, 305, 307), 7 registered (FU-313
to FU-318, plus the method's M-SESS-11). The method register stands at 101 lessons in 13 groups.

---

## The three things worth your attention

**1. The plan's own headline number was wrong, and testing my instruments found it.** I had been reporting
"commit 2 rounds, expect 3" at 90% confidence. An adversarial audit of the planning artefacts raised 43
confirmed findings against them, and two mattered because both were claims about the method's own
trustworthiness:

- the round-duration filter discarded every gap over five hours as idle and reported only a count. **Six of
  nineteen were daytime gaps** — real long rounds. It also had no lower bound, so gaps of 0, 5, 11, 12 and 28
  minutes counted as rounds, along with one **negative** gap.
- I had written that "two independent windows agreeing" justified trusting the figure. **The windows were
  nested** — a third of the larger sample *is* the smaller one. The figure does survive, but on a disjoint test
  I ran afterwards, not on the evidence I had cited.

Corrected, the honest commitment was **1 round, expect 2**. Delivering 2 is therefore at the top of the range,
not below a promise.

**2. I cost the night an hour through my own concurrency.** Round A's first full suite came back **red** — two
failures, in 1h48m34s against a measured 53m20s — because I had launched a 48-agent verification workflow on
the same machine. Re-run alone the two passed in 81s; the clean full re-run gave 491 passed. **The subset
passing did not authorise the commit**: a passing subset is a hypothesis and the full suite is the verdict, so I
paid the hour again. Recorded as **M-SESS-11** — the existing rule covered only a second *suite*, whose damage
is to data; a fleet's damage is to *timing*, which looks like a real defect instead of an obvious collision.

**3. The biomimetic brief was mostly a rename.** 72 assessments across six verification lenses: **21
DUPLICATES_EXISTING, 12 EXISTS_DORMANT, 11 COLLIDES_WITH_RULING, 9 ABSENT, 8 FALSE_ABOUT_REPO, 7
EXISTS_AND_RUNS — and 4 SOUND_AND_NEW.** It reasons from the vision documents rather than the tree, so it never
learned that the metabolic term cannot deplete, that eight of eleven biomimicry subpackages contain no files, or
that the circadian schedule exists twice byte-identically. Its genuine contributions were folded into the five
thrusts that already existed. **No new thrust, no new phase, no parallel `src/idbo/` tree.**

---

## Decisions still yours — nothing here was decided for you

- **The three biomimetic refusals** are recorded with grounds rather than acted on: the parallel `src/idbo/`
  tree, any field that would grade a **person** (ruling A.9.5 — grade the request, never the human), and the
  routing score as specified.
- **The six §18 decisions** in `WORKSTATION_IDBO_WHOLE_VISION.md` remain open.
- **FU-313** is the one that unblocks the method itself: nothing in the change record can hold a *commitment*,
  so a promise has no variance and the forecast cannot improve from its own history.
- **Two naming hazards** to rule on if the biomimetic work proceeds: "Constitution" already names a running gate
  with deliberately narrow scope, and "mechanical" throughout this repository means *mechanically checkable* —
  the change-control gate's one tooth.

## What was left undone, and why

- **Round C went ahead and landed** (`cb075956`, 494 passed). A ROUND D was not started: about 3.5 hours of the eight remained against a p75 round of 4.29 hours, so the rule held.
- **Round C's lesson is worth more than its fix.** Three of its four problems were in my own CHECKING, not the code: a plausible FU-303 fix that a driven comparison showed changed nothing (reverted, and the row dropped as refuted); a guard fixture rejected by a path filter in the screen it was testing; and a guard that searched a LINE rather than the matched OCCURRENCE and so flagged eleven correct reports.
- *(superseded)* At the time of first writing, Round C had not been started. About 4.5 hours of the eight remained against a p75 round
  of 4.29 hours, which is inside the rule but only just. If a Round C commit appears above this file's own
  commit, it went ahead; if not, the rule held and it did not.
- **FU-305's literal ask is impossible and is recorded as such.** The eleven defended proposals were never
  written down, so they cannot be recorded as rows. The count is now computed from the ledger instead, and the
  ledger says plainly that the instances are unrecoverable.
- **The tolerant reader (FU-075 / FU-298) remains five rounds of work**, not one. Its own row forbids a single
  unattended pass, and `vbs/qms.py` goes first because its seeded-zero default makes an unreadable store read as
  a clean quality record.

## One honest limit on the biomimetic verification

Its agents were given the brief's *subject* but not its full text — my commissioning error. So their verdicts
are reliable about **this repository** and about **the named subsystems**, and are **not** quotations of the
brief. One agent said so unprompted. Anything in Vision 8.0 §8 that credits or refuses an idea refuses the named
subsystem against the existing path, which is the question that decides what gets built.
