# HANDOVER W626 — CLOUD SESSION → LOCAL CLAUDE OPUS 5.5

**Written** 2026-10-07 by the cloud session (claude.ai/code) that ran W602–W626. **For** a Claude Opus 5.5 session
on the Owner's own machine (`C:\Users\rehan\Workstation`). Read this first, then `docs/FABLE_DELIVERY_PROMPT.md`.

Everything is in git. Nothing of the work lives only in the cloud session — the two things that did (the edit
and blind helpers, and the raw audit results) are committed with this document.

---

## 1. Get onto the work — in this order

```bash
cd /c/Users/rehan/Workstation
git fetch --all --prune
git status --short                 # must be clean before you switch; stash NOTHING blindly
git branch -a --sort=-committerdate | head
```

**Where the work is.** All commits since W601 are on **`main-l1fsqo`**, carried by **pull request #355** into
`main`. If #355 is MERGED, work on `main` (`git checkout main && git pull`). If it is still OPEN:

```bash
git checkout main-l1fsqo && git pull origin main-l1fsqo
```

…and keep committing to `main-l1fsqo` so #355 picks each push up (Spine CI runs only on `main` and on PRs into
`main` — a branch push alone runs only the docs workflow). Never push to `main` without the Owner.

**Environment.** Python 3.12 venv with `pip install -r requirements.txt pytest pytest-xdist==3.8.0`; frontend
`npm install` at the repo root (workspaces). The suite, exactly as every round ran it:

```bash
R=$(mktemp -d); DATA_DIR=$R WORKSTATION_DATA_DIR=$R WORKSTATION_UEG_PATH=$R/ueg.json PROJECTS_DIR=$R/projects \
  AI_DISABLE_LOCAL=1 python -m pytest integration_tests/test_mvp_spine.py -q --no-header -p no:warnings -n 4
```

Last full run: see the W625 commit's message. ~13–15 min at `-n 4`. Frontend: `cd apps/workstation-superapp &&
npx tsc --noEmit` (and `npm run build`, which passes).

---

## 2. State at handover

> **UPDATED after W634 (2026-10-07). START HERE: `docs/RESUME_ON_MY_MACHINE.md` holds the one prompt to paste.**
> State: **W634 issued ledger v12**, with Tier-1 **6** and Tier-2 **8**. **P2.30** (six tier-1) and **P2.31** (eight
> tier-2) are open, FU-574..587. W635, which fixes all fourteen, was in progress in the cloud: if `git log` has no W635,
> work those rows again from the register. Each row's `why` ends with the auditor's SMALLEST HONEST FIX.
> Vercel is RETIRED (Owner): `vercel.json` is archived, and Google Cloud free tier with dev/beta/release channels is the
> plan (`docs/DEPLOYMENT.md`). Disconnecting the Vercel project in the Owner's Vercel account silences the red check.
>
> **Earlier update, after W632 (2026-10-07).** Done: P2.26 and P2.27, closed by the W632 re-run, which issued **ledger v11**:
> Tier-1 **4**, Tier-2 **10**, all NEW surfaces (every v10 row was fixed in W630/W631). **P2.28** carries the four, **P2.29**
> the ten: `python scripts/followups.py list --slot P2.28` and `--slot P2.29`. Each row's `why` ends with the auditor's
> SMALLEST HONEST FIX.
>
> **Before booting the audit backend, check that :8031 is FREE:** `pgrep -af "uvicorn agentic_core"`. An audit agent started
> its own backend on :8031 during W629, and a second boot then exits silently, so the audit can measure the wrong process.
> Confirm the booted commit by a response header or a route that only HEAD has.
>
> **UPDATED after W630 (2026-10-07).** The rest of this section is still accurate, except where the note above updates it.
>
> - **Done:** P2.24 and P2.25 (W629). The M1+M2 re-run W629 issued **ledger v10**: Tier-1 **4**, Tier-2 **12**. The
>   series at twelve agents: v7 20 → v8 18 → v9 11 → v10 4. Raw record: `docs/fidelity_runs/ledger_v10_W629_aeb9fa8.json`.
> - **P2.26** (the 4 tier-1): all four rows closed in W630 (FU-544, 545, 549, 550).
> - **P2.27** (the 12 tier-2): OPEN — FU-546, 547, 548, 551, 552, 553, 554, 555, 556, 557, 558, 559. Each row's
>   `why` ends with the auditor's SMALLEST HONEST FIX. FU-559 (a gate on every response) is architecture: stamp
>   ungated responses rather than build a global gate, unless the Owner rules otherwise.
> - **Next milestone:** M1+M2 re-run when P2.27 closes. Same instrument, twelve agents. Boot a fresh backend from
>   HEAD on a scratch DATA_DIR with AI_DISABLE_LOCAL=1, run `fidelity_audit_v7.js` with `{base, head, date}`, then
>   `refutation_gate.py after --result <the workflow output file>`. Render from the `result` list:
>   `render_fidelity_ledger.py <list.json> docs/VISION_FIDELITY_LEDGER.md <head> <date> 8031 11 W6xx`. Then
>   archive v10, add the milestone record to the prompt, update the anchor in `scripts/blinds_w572.json`, and add
>   rows with `followups.py add`. W629 is the worked example.
> - **Owner rulings, 2026-10-07b:**
>   - P2.24 closes without FU-301, FU-417 and FU-399; they ride P5.1.
>   - M1 may run locally.
>   - The FU-283 dependency removal is approved.
> - **Dependency removal (FU-283): TRIED AND REVERTED.** W628b removed 19 packages and CI's fresh install failed two
>   tests. The retry plan is in `docs/DEPENDENCY_VERDICTS.md`: remove in halves, test on a fresh venv, and hold back
>   firebase-admin.

| | |
|---|---|
| plan | **70 of 83 items** before P2.24 closes — P1 18/18 · P2 23/25 · P3 **29/29** · P4 0/6 · P5 0/5 |
| milestones | ledger **v9** (W621, 12 agents, HEAD 18f3fcc): **Tier-1 11, Tier-2 21** — series v7 20 → v8 18 → v9 11 |
| P2.24 | all **11** v9 tier-1 rows CLOSED (W622–W624). Open: six old riders (FU-283, 301, 398, 399, 417, 474) |
| P2.25 | **7 of 21** v9 tier-2 rows closed (W625). Open: FU-519, 520, 521, 522, 525, 526, 529, 530, 531, 532, 536, 537, 541, 542 |
| next milestone | M1 + M2 re-run when P2.24 and P2.25 close — same instrument, **twelve agents** |
| Owner, still open | the Stripe key roll (P4.6); FU-473 (deferred by the Owner, confirmed 2026-10-07) |
| Owner, ruled 2026-10-07 | all built in W622 — Dawah share, entity scan (no deletion), CI parallel, circadian switch OFF |

`python scripts/followups.py priority | head -30` lists the open rows in order; `render` regenerates the plan's
status block; `check` validates the register.

---

## 3. The round, as it has been run (do not thin it — the Owner reversed a thinner-verification choice)

1. **Measure** the live state; read the row's evidence and reproduce it.
2. **Patch** with `scripts/round_tools/patch.py` (exact-once anchors, line endings preserved). **CRLF files**
   include `agentic_core/api/vsb.py`, `board.py`, `transformation.py`, `gateway.py`, `deliverables.py`,
   `living_vsbs.py`, `GenesisJourney.tsx`, `BoardOfDirectors.tsx`, `VSBEconomy.tsx`, `ProjectsHub.tsx`,
   `.github/workflows/spine.yml` — check `git ls-files --eol` and `git diff --stat` for an EOL flip.
3. **Pre-flight**: `python scripts/selfcheck_diff.py` — read every lead; run the `-k` list it prints when the
   register or plan changed.
4. **Guard** in `integration_tests/test_mvp_spine.py`, driven on the surface a person reads where reachable.
5. **Blinds**: `python scripts/round_tools/blinds.py <file> -k <guard>` — every blind must be `BLIND(red)`. A
   `VACUOUS` blind means the guard does not test the fix; it happened in most rounds tonight (a string present
   twice, a precondition never driven, a CRLF anchor) — fix the guard, re-drive.
6. **Register**: `python scripts/followups.py close FU-xxx --by W6xx --because built --note "..."` (prose through
   an argument, never a backticked shell string).
7. **Full suite once**, then commit with an **explicit file list** (never `git add -A`; `data/` is never
   committed), then push.

Never: flip AUTH_ENABLED / SELF_SERVE_SIGNUP / AI_ALLOW_EXTERNAL / REAL_MONEY_ENABLED; AI-generate Quran Arabic;
score recitation; delete an entity; edit FOLLOWUPS.json or the plan while a suite runs.

---

## 4. Things a fresh session would not know

- **The red check on GitHub is Vercel, and it is not the code.** The `Vercel` preview deployment has failed on
  every `main` commit since at least 2026-08-30 while Spine CI was green, and `npm run build` passes locally. The
  cause is in the Vercel project settings; only its log shows it (`npx vercel inspect <deployment> --logs`, needs
  the Owner's Vercel login). Recorded on PR #355.
- **CI now runs the suite in parallel** (`-n 4`, timeout 60 min — W622, Owner-approved). Its first GitHub run, on PR #355 at 5f9da00,
  was GREEN in ~17 min, with every other check green too. If it later stalls or flakes, that is FU-301's territory: report it to the Owner with the job log.
- **Run records**: `docs/fidelity_runs/ledger_v8_*.json` and `ledger_v9_*.json` are the raw region results the
  ledgers were rendered from (`scripts/render_fidelity_ledger.py <json> docs/VISION_FIDELITY_LEDGER.md <head>
  <date> <port> <version> <round>`). Run M1 with `scripts/workflows/fidelity_audit_v7.js` against a FRESH backend on
  a scratch DATA_DIR with `AI_DISABLE_LOCAL=1`; gate it with `scripts/refutation_gate.py before/after` — `after`
  REFUSED an incomplete result in W621 and the run was resumed to completion. Only one run at a time: W621 started
  a second while the first was still alive, after a worker restart.
- **Entity scan (FU-459)**: run `python scripts/entity_coverage_scan.py` on the Owner's machine — the cloud
  checkout held none of the 162 entities.
- **Rendering escalations**: since W612 a refuter that RAISES a finding's tier stands at the raised tier
  (`render_fidelity_ledger.standing` → "escalated"). v7's Tier-2/3 erratum is in the plan's M1 record.
