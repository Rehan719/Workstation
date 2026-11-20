# Resume on my machine — the one prompt to paste

When you want to continue locally, open Claude Code (Claude Opus 5.5) **in your local clone** (`~\Workstation`)
and paste the block below as your first message. Nothing else is needed.

Updated 2026-11-20 (W1131). The cloud session works in 8-hour cycles until 2026-11-30 and pushes to `main-l1fsqo`.
While it runs, the local session works on a branch of its own (step 1), so the two never push to the same branch.

---

```
Resume the Workstation delivery from where the cloud session stopped, autonomously and efficiently.

1. Sync first, and stash nothing blindly:
   git fetch --all --prune && git status --short
   Before 2026-12-01 the cloud session may still be pushing to main-l1fsqo, so do not push there: work on a
   branch of your own named local-owner (if it exists, check it out and merge origin/main-l1fsqo into it;
   otherwise create it from origin/main-l1fsqo), push that branch, and open its own pull request.
   From 2026-12-01: if the open pull request from main-l1fsqo (PR #463 on 2026-11-20) is merged, work on main
   (git checkout main && git pull); otherwise git checkout main-l1fsqo && git pull origin main-l1fsqo, and keep
   pushing there. Never push to main without me.
2. Read, in this order: docs/REMAINING_WORK_MEASURED.md (every open item, measured 2026-11-10),
   docs/HANDOVER_W626.md section 3 (the round discipline - follow it exactly), then docs/FABLE_DELIVERY_PROMPT.md.
3. Set up once if needed: a Python 3.12 venv with
   pip install -r requirements.txt pytest pytest-xdist==3.8.0, then npm install at the repo root.
   Then, once: add the line LEGAL_MATTER_FOLDER=${USERPROFILE}\data\legal-matter to .env if it is not there
   (W1129: the legal matter's folder is named on this machine only, never in a committed file), and check it with
   python -c "from dotenv import load_dotenv; load_dotenv(); from agentic_core.legal import bundle; print(bundle.resolve_bundle_dir()['state'])"
   which prints configured_present. Until the line is there, no document in the folder is read.
4. Check for an unfinished round: if `git status` shows uncommitted changes, they are the last round's
   work in progress. Read `git diff`, finish it (its guard tests and blinds are in
   integration_tests/test_mvp_spine.py), run the full suite once, then commit and push.
5. First, the rows only this machine can do (slotted OWNER and listed in the plan's open decisions; each reads
   or changes the data on this machine, which the cloud session never sees):
   - FU-1046: drive the section-11 screen on the text kept in data/_moved_books_20261012-155706 and find why
     five change records of 2026-09-01 failed; record the reason.
   - FU-1038: turn the durable defect loop once for real: close the fifteen defects of the retired door with
     that reason, and correct and re-verify the other four or report them as not reproducible.
   - FU-1040: find the writer of the 162 operation rows served by a test double, and move those rows aside
     reversibly, under the rule already ruled for test entities.
   - FU-1165: list the entities in this machine's data and ask me which two are mine; then name them in
     Settings, Protected enterprises.
   - FU-1005: once the fund's recorded reversal exists (its row says so), reverse the three June test
     allocations with it.
   (The two committed audit records under docs/fidelity_runs/ that carried text of a private kind were edited
   in the cloud session on 2026-11-20, as recommended and with your go-ahead; git history keeps the earlier
   text, as ruled on 2026-10-14.)
6. Then continue the plan: python scripts/followups.py priority | head -30 lists the open rows. No capped
   fidelity re-run is held before the final audit (P5.22): the Owner allowed one mid-way audit (W675) and ruled
   that the next is the final, uncapped one, after the fifth phase and the sign-in readiness round.
7. Ask me only for an Owner decision (anything marked OWNER, or anything touching real money, live Stripe,
   managed Postgres, production deploy, external AI keys, deleting an entity, or the AUTH/SIGNUP/AI_EXTERNAL/
   REAL_MONEY switches). Everything else: decide, build, verify, commit, push, and report briefly in chat.
```

---

## What the cloud session left (the short version)

- **All work is in git.** PR #462 (rounds W785–W1118) was merged into `main` on 2026-11-19 on your instruction.
  Later rounds are on `main-l1fsqo`, carried by **PR #463**.
- **The plan,** on 2026-11-20: 89 of 119 items done (P1 18/18 · P2 39/41 · P3 30/32 · P4 0/6 · P5 2/22). P2.40 and P2.41
  have every row closed, and close on the final audit. The current figures are the PLAN NOW block of
  `docs/FABLE_DELIVERY_PROMPT.md`.
- **Measured remaining work,** on 2026-11-10: about 214–392 rounds across the 32 items then open, most of it in the
  fifth phase (143–265). Much of that phase is ruled to come after sign-in (P4.1), which now proceeds without
  waiting on you, and the final audit runs after it. Details per item in `docs/REMAINING_WORK_MEASURED.md`.
- **Owner rulings in force:** those recorded in the plan, including 2026-11-06 (five decisions taken as
  recommended), 2026-11-10 (decisions go with the recommendation; PR #461 merged), 2026-11-19 (twenty-two
  recommendations accepted; the six switches proceed in the ruled order, each once its pre-flight is built and
  measured; PR #462 merged) and 2026-11-20 (that day's recommendations accepted).
- **Still yours:**
  - Merge PR #463 when you are ready.
  - The rows in step 5: FU-1046, FU-1038, FU-1040, FU-1165, and FU-1005 once its reversal exists.
  - One line in `.env` on your machine for the legal matter's folder (step 3 of the prompt), if the local
    session has not added it.
  - Sending the two permission letters in `docs/letters/` (FU-1188).
  - Sending the request to the Quranic Audio Dataset's authors, also in `docs/letters/` (FU-1283).
  - Five places that still name your Windows home folder: one audit record, the pinned fidelity ledgers, `venv/`, `.claude/settings.json` and `_archive/` (FU-1286).
  - At the first deploy, an uptime check on `/health` from your own cloud account, beside the billing alert
    (FU-1095).
  - What no round takes (ruling of 2026-11-19): the deploy on your Google Cloud project, the external-model key,
    and real money, which stays off until a compliance and KYC review by qualified people.
