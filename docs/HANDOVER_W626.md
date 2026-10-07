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
