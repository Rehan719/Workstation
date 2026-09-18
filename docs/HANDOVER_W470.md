# Handover — W469 → W470 (to Claude Fable 5.1)

> **W470 shipped** (2026-09-18, Claude Fable 5.1): P1.13 ✅ DONE — see `docs/AUTONOMOUS_PROGRESS.md` (`### W470`).
> **W471 shipped** (2026-09-18): P1.14 ✅ DONE (`### W471` in the log). PLAN NOW now says
> **Next: P1.15 Stores that refuse, never replace — 11 follow-ups ride it** (the W442→W468 store class; each row
> names its store and its fix). §1 below is the state as handed over at W469; §3–§6 (the rhythm, the constraints,
> the lessons, the environment) still apply to every round. Two lessons since: never `sed -i` a CRLF file
> (`reference-sed-strips-crlf-trap` in memory), and `done --hand-to` lifts the taker's broad prefixes to the handed
> route's position (FU-073) — remove the finished item's route first and add the area to its next owner by hand.
> **W472 shipped** (2026-09-19): P1.15 ✅ DONE — one strict read (`config.read_json_strict` → `StoreUnavailable`) for
> every writer; eleven register rows closed. PLAN NOW now says **Next: P1.16 Canon and suite hygiene — 14 follow-ups
> ride it**. Lesson: a blind that re-creates a hang needs a guard leg that bounds itself (a worker thread + timeout)
> and a harness with a per-blind timeout — B07 spun for an hour before the still output file gave it away.
> The next free probe port is :8082.

Written 2026-09-18 by the session that shipped W469 (Claude Opus 5), on the Owner's instruction: "leave a
handover for Fable to start W470". The Owner (Rehan) is switching models for W470. Nothing in W470 has been
started. Read this whole page first. Then read `docs/FABLE_DELIVERY_PROMPT.md` whole: that prompt is the
brief, and this page only covers what a fresh session would otherwise have to rediscover.

## 1. Where things stand

- **HEAD:** `2e42da04` (W469) on `main`, pushed. CI: Spine CI and Documentation Quality & Sync both GREEN on 2e42da04 (runs 35346684729 / 35346684756).
- **Suite:** 381 passed · 15 skipped · 0 failed (396 items from 357 test functions; 70 session guards W419–W469), full run on the W469 final tree in the isolated env, 37 min. The log is `docs/AUTONOMOUS_PROGRESS.md`; its last entry is `### W469`.
- **The plan:** `<delivery_plan>` in the prompt. P1.1 to P1.12 are ✅ DONE (W449–W460). The PLAN NOW block
  inside WHERE THE PLAN STANDS is generated, so never edit between its markers. It says:
  **Next: P1.13 Catalogue honesty — no follow-ups ride it.** After that come P1.14, P1.15 (11 rows),
  P1.16 (12 rows), then P2.
- **The register:** `docs/FOLLOWUPS.json` has 54 open rows, 0 awaiting the Owner and 0 unscheduled. Each
  row rides the plan item that owns its area.
- **What W469 did:** the Owner asked why P1.13 never came. The answer: the old NEXT slot grew faster
  than it drained. W469 made these changes:
  - NEXT is retired.
  - Routes send each new row to the item that owns it.
  - PLAN NOW is generated and shown live on `/transformation`.
  - `followups.py done` finishes an item.

## 2. W470 = P1.13 Catalogue honesty

The item text (in the prompt): the Marketplace counts only routed entries as live; the six Domain
Signature literals are badged legacy or retired; the "QEP Flagship" tab is removed from the five
non-Religion hubs; the DomainsHub and AIToolsCatalogue counts come from ONE tool registry that the hubs
mount from. GUARD: a test that counts mounted DomainTool forms against the registry.

The P1.13 route already exists. It covers `pages/domains/`, `pages/AIToolsCatalogue.tsx`,
`pages/marketplace/` and `agentic_core/api/tools.py`, plus the title words "marketplace count(s)",
"domain signature", "qep flagship", "tool registry" and "catalogue count(s)". Anything W470 finds
there and does not do lands on P1.13 automatically.

Closing it, in the same commit as the work:
```
python scripts/followups.py add --title "…" --why "…" --source W470 --files a,b   # each thing found and not done
python scripts/followups.py done P1.13 --by W470 --reroute --hand-to P1.16
```
`done` refuses while rows still ride the item. `--reroute` moves them along the routes. `--hand-to`
merges P1.13's route into P1.16's at the earlier position, so the catalogue area keeps its precedence.
If a write half-lands, run the same `done` again: it finishes what is left. Then add the item's
"DELIVERED / NOT DONE" text under P1.13 by hand, as P1.1 to P1.12 have.

## 3. The rhythm (every round)

audit-before-wire → patch → guard → **break-test** → **refute your own diff** → fresh-backend browser
probe → full suite on the FINAL tree → docs → register → commit → push → CI → memory.

- **Break-test.** Apply each "blind" alone and watch the guard fail. Byte-restore it; never use
  `git checkout`. Read the failure lines: identical failure lines across blinds mean the run was
  contaminated, not that the blinds were caught.
- **Refute.** Use multi-agent refuters, with every finding verified adversarially. Refute a refuter's
  fix again if it changes real logic. Run the probe BEFORE the last refutation.
- **Docs.** The prompt's WHERE THE PLAN STANDS (header "updated W###" plus a line), the living plan
  §4 paragraph plus §8 changelog, the counters (W1→W###, the tests count, and the session-guard count in
  the prompt's `<guards>`), the progress entry, and UNDERSTANDING/WHOLE_VISION counters.
- **Commit.** Use an explicit file list (never `git add -A`). The message has a "What was WRONG" body
  and ends `Co-Authored-By: <your model> <noreply@anthropic.com>`. Push to `main`, then check CI with
  `GITHUB_TOKEN= gh run list --branch main` (the empty GITHUB_TOKEN is required; an invalid env token
  shadows the keyring login).

## 4. Binding constraints (verbatim from the Owner's standing directive)

- Run pytest only with an isolated env: `DATA_DIR=/c/tmp/x WORKSTATION_DATA_DIR=/c/tmp/x
  WORKSTATION_UEG_PATH=/c/tmp/x/ueg.json PROJECTS_DIR=/c/tmp/x/projects AI_DISABLE_LOCAL=1`. Never run
  two suites at once, and never rebuild the bundle while the suite runs.
- Preserve per-file CRLF/LF (`git ls-files --eol`). The living plan and WHOLE_VISION are CRLF; the
  prompt, the register and the progress log are LF.
- Do not flip AUTH_ENABLED / SELF_SERVE_SIGNUP / AI_ALLOW_EXTERNAL / REAL_MONEY_ENABLED.
- OWNER-GATED, never without his explicit instruction: real-money rails, live Stripe (the Owner must
  roll the exposed key), managed Postgres, production deploy, a live external AI key. Money is
  VIRTUAL WST.
- Never fabricate. Never "fix" missing user context by enabling gateway recall (augment=False is
  deliberate).
- Faith content: NEVER AI-generate Quran Arabic. The only sources are quran.com, alquran.cloud and
  tanzil.net. AI content is labelled, and recitation is never scored.
- Never use bare `git stash` or `stash pop` (stash@{0} "Local changes before update" must stay).
  To snapshot, use `git stash create` (it prints a sha and touches nothing).

## 5. Lessons that cost a round (read before you refute)

1. **Refuters escape.** In W462 and again in W469, a refuter told to work in a copy ran a command
   against the REAL repo. In W469 it was `followups.py done P1.15 --by W470`, which marked P1.15 done
   and moved 11 rows while a break run was going. So:
   - Refuters that may run anything get `isolation: "worktree"`.
   - Refuters never run at the same time as a break harness.
   - After every refutation, run `git status` and grep the docs for markers that should not exist
     (`DONE W470` before W470 is done).
   - Snapshot with `git stash create` before every refutation and every break run.
2. **Edits go through scripts with asserted replacements.** Write the patch script with the Write
   tool, never through a heredoc: escapes get mangled. The pattern (EOL-preserving, every replacement
   asserted to match exactly once):
   ```python
   def apply(path, pairs):
       raw = open(path, "rb").read(); crlf = b"\r\n" in raw
       text = raw.decode("utf-8").replace("\r\n", "\n") if crlf else raw.decode("utf-8")
       for old, new in pairs:
           assert text.count(old) == 1, (path, text.count(old), old[:80]); text = text.replace(old, new)
       open(path, "wb").write((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))
   ```
3. **Guards can be vacuous.** An assertion that another check already refuses, or a page needle that
   also matches a neighbouring line, stays green under its blind. Every W469 vacuous blind was one of
   those two. Fix the assertion, then re-run that blind.
4. **The register and the plan docs move together.** Change them only through `scripts/followups.py`
   (add · close · drop · reslot · route · routes · done · render · check · schedule). The suite fails
   in these cases:
   - an open row sits where its routes would not send it (FU-045/FU-063 were the W469 example);
   - a finished item still carries a row;
   - PLAN NOW is edited by hand.

## 6. Environment notes

- **Browser probe:** `scripts/_w4NN_probe.mjs` against a fresh backend. Build first (`npm run build` in
  `apps/workstation-superapp`; the backend serves `dist/`). Start it with `python -m uvicorn
  agentic_core.app_mvp:app --host 127.0.0.1 --port 8079` under an isolated DATA_DIR. The next free port
  is **:8079**; W469 used :8078. Stop the backend afterwards. `innerText` carries CSS uppercase, so
  match titles with `/i`.
- **Port :8000:** a stale orphan may hold it; use another port.
- **CI flake:** the Spine CI can fail on the onnxruntime-node download ("socket hang up"). That is
  infra, not code; re-run it.
- **Open with the Owner:** no register row. The plan rulings still with him are listed in the prompt's
  answers.

## 7. Then pause?

The Owner decides the cadence. Ask him before running several rounds unattended, unless he says to.
