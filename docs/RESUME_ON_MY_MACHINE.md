# Resume on my machine — the one prompt to paste

When the weekly allowance resets, open Claude Code (Claude Opus 5.5) **in your local clone** (`C:\Users\rehan\Workstation`)
and paste the block below as your first message. Nothing else is needed.

---

```
Resume the Workstation delivery from where the cloud session stopped, autonomously and efficiently.

1. Sync first, and stash nothing blindly:
   git fetch --all --prune && git status --short
   If PR #355 (main-l1fsqo -> main) is merged, work on main: git checkout main && git pull.
   Otherwise: git checkout main-l1fsqo && git pull origin main-l1fsqo, and keep pushing there.
   Never push to main without me.
2. Read, in this order: docs/HANDOVER_W626.md (the "UPDATED" notes at the top of section 2 are the current state),
   then docs/FABLE_DELIVERY_PROMPT.md. Follow the round discipline in HANDOVER section 3 exactly.
3. Set up once if needed: a Python 3.12 venv with
   pip install -r requirements.txt pytest pytest-xdist==3.8.0, then npm install at the repo root.
4. Check for an unfinished round: if `git status` shows uncommitted changes, they are the last round's
   work in progress. Read `git diff`, finish it (its guard tests and blinds are in
   integration_tests/test_mvp_spine.py), run the full suite once, then commit and push.
5. Then continue the plan: python scripts/followups.py priority | head -30 lists the open rows. Work the open
   P2.x milestone rows round by round. When a milestone item's rows are all closed, re-run M1+M2 as section 4
   of the handover describes: check :8031 is free first, then launch exactly one twelve-agent run.
6. Ask me only for an Owner decision (anything marked OWNER, or anything touching real money, live Stripe,
   managed Postgres, production deploy, external AI keys, deleting an entity, or the AUTH/SIGNUP/AI_EXTERNAL/
   REAL_MONEY switches). Everything else: decide, build, verify, commit, push, and report briefly in chat.
```

---

## What the cloud session left (the short version)

- **All work is in git** on `main-l1fsqo`, carried by **PR #355** into `main`.
- **Rounds W602–W634 are committed.** W635 is the round in progress when credit ran out: if it is not in
  `git log`, it is uncommitted in the cloud container and lost. In that case its fourteen rows are still OPEN in
  the register (P2.30 and P2.31) and are simply worked again.
- **Fidelity series** (twelve-agent M1+M2): v7 20 → v8 18 → v9 11 → v10 4 → v11 4 → v12 6 tier-1. Every row each
  audit filed was closed before the next. The count does not reach 0 because each run samples new surfaces.
- **Owner rulings in force (2026-10-07b):**
  - FU-301, FU-417 and FU-399 ride P5.1.
  - M1 may run locally.
  - FU-283's dependency removal is approved. It was tried and reverted, and the retry plan is in
    `docs/DEPENDENCY_VERDICTS.md`.
  - Vercel is retired; Google Cloud (free tier, dev/beta/release) is the planned target. See `docs/DEPLOYMENT.md`.
- **Still yours:**
  - Merge PR #355 when you are ready.
  - Roll the Stripe key (P4.6).
  - FU-559: whether to build an app-wide constitutional gate.
