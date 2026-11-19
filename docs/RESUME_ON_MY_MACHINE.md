# Resume on my machine — the one prompt to paste

When you want to continue locally, open Claude Code (Claude Opus 5.5) **in your local clone** (`C:\Users\rehan\Workstation`)
and paste the block below as your first message. Nothing else is needed.

Updated 2026-11-10 (W787). The cloud session is working through November in 8-hour cycles; if it is still running,
check the open pull request first so the two sessions do not edit the same branch at once.

---

```
Resume the Workstation delivery from where the cloud session stopped, autonomously and efficiently.

1. Sync first, and stash nothing blindly:
   git fetch --all --prune && git status --short
   If PR #462 (main-l1fsqo -> main) is merged, work on main: git checkout main && git pull.
   Otherwise: git checkout main-l1fsqo && git pull origin main-l1fsqo, and keep pushing there.
   Never push to main without me.
2. Read, in this order: docs/REMAINING_WORK_MEASURED.md (every open item, measured 2026-11-10),
   docs/HANDOVER_W626.md section 3 (the round discipline - follow it exactly), then docs/FABLE_DELIVERY_PROMPT.md.
3. Set up once if needed: a Python 3.12 venv with
   pip install -r requirements.txt pytest pytest-xdist==3.8.0, then npm install at the repo root.
4. Check for an unfinished round: if `git status` shows uncommitted changes, they are the last round's
   work in progress. Read `git diff`, finish it (its guard tests and blinds are in
   integration_tests/test_mvp_spine.py), run the full suite once, then commit and push.
5. First, the two rows only this machine can do (both slotted OWNER and listed in the plan's open decisions):
   - FU-1046: drive the section-11 screen on the text kept in data/_moved_books_20261012-155706 and find why
     five change records of 2026-09-01 failed; record the reason.
   - FU-1151: the two committed audit records under docs/fidelity_runs/ that carry text of a private kind.
     Recommended: edit each note to say only what kind of place or matter it was; leave git history as ruled
     on 2026-10-14.
6. Then continue the plan: python scripts/followups.py priority | head -30 lists the open rows. No capped
   fidelity re-run is held before the final audit (P5.22): the Owner allowed one mid-way audit (W675) and ruled
   that the next is the final, uncapped one, after the fifth phase and the sign-in readiness round.
7. Ask me only for an Owner decision (anything marked OWNER, or anything touching real money, live Stripe,
   managed Postgres, production deploy, external AI keys, deleting an entity, or the AUTH/SIGNUP/AI_EXTERNAL/
   REAL_MONEY switches). Everything else: decide, build, verify, commit, push, and report briefly in chat.
```

---

## What the cloud session left (the short version)

- **All work is in git.** PR #461 (rounds W754–W784) was merged into `main` on 2026-11-10 on your instruction.
  Later rounds are on `main-l1fsqo`, carried by **PR #462**.
- **The plan:** 87 of 119 items done (P1 18/18 · P2 39/41 · P3 30/32 · P4 0/6 · P5 0/22). P2.40 and P2.41 have
  every row closed or with you, and close on the final audit.
- **Measured remaining work:** about 214–392 rounds across the 32 open items, most of it in the fifth phase
  (143–265). Much of that phase is ruled to come after sign-in, which is your switch (P4.1), and the final audit
  runs after it. Details per item in `docs/REMAINING_WORK_MEASURED.md`.
- **Owner rulings in force:** those recorded in the plan, including 2026-11-06 (five decisions taken as
  recommended) and 2026-11-10 (decisions go with the recommendation; PR #461 merged).
- **Still yours:**
  - Merge PR #462 when you are ready.
  - FU-1046 and FU-1151 (above).
  - The P4 switches, in the order you ruled on 2026-10-12: sign-in on your own machine first, real money last.
