# Resume on my machine — the one prompt to paste

When you want to continue locally, open Claude Code (Claude Opus 5.5) **in your local clone** (`~\Workstation`)
and paste the block below as your first message. Nothing else is needed.

Updated 2026-11-21 (W1131, W1164, W1184, W1187, W1188, W1190). The cloud session works in 8-hour cycles into December, until the plan's
build items are closed and the final audit has run (2026-12-31 at the latest), and pushes to `main-l1fsqo`. While
it runs, the local session works on a branch of its own (step 1), so the two never push to the same branch.

---

```
Resume the Workstation delivery from where the cloud session stopped, autonomously and efficiently.

1. Sync first, and stash nothing blindly:
   git fetch --all --prune && git status --short
   While the cloud session's cycles run (into December, until the plan's build items are closed and the final
   audit has run; 2026-12-31 at the latest) it may still be pushing to main-l1fsqo, so do not push there: work on a
   branch of your own named local-owner (if it exists, check it out and merge origin/main-l1fsqo into it;
   otherwise create it from origin/main-l1fsqo), push that branch, and open its own pull request.
   Once the cycles have stopped: if the open pull request from main-l1fsqo (the one opened after PR #466 was
   merged on 2026-11-21) is merged,
   work on main (git checkout main && git pull); otherwise git checkout main-l1fsqo && git pull origin
   main-l1fsqo, and keep pushing there. Never push to main without me.
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
   or changes what is on this machine, which the cloud session never sees). FU-1046, FU-1038, FU-1040 and
   FU-1005 were done here on 2026-11-20 (W1133l, W1133m), and are closed:
   - FU-1165: as I answered on 2026-11-20, register my two ventures, Atmospheric Harvest Solutions and Aerius
     Energy Harvest, fresh in the new books, then name each in Settings, Protected enterprises, once it exists.
   (FU-1054's step here was done on 2026-11-21 and the row is closed (W1188): the run, cal-8c7430765c, was
   committed from this machine (c657e2a7) and merged in the cloud session at c76809a8. It left five cases
   unanswered, so it calibrates nothing, and it did not meet the bar; the reviewer stays uncalibrated. As I
   ruled that morning, the row closed on it all the same, and what it missed is FU-1831: the cloud session
   makes its three fixes, and the second run is made from this machine before 2027-01-10, with a larger local
   model, as I ruled that afternoon.)
   (FU-1286's step here was done on 2026-11-20 and the row is closed (W1180): venv/ was untracked (7afa4aa9), the
   folder kept on this disk, and merged in the cloud session at 07fb9817. The three one-off command permissions
   in .claude/settings.json that named my home folder were removed in the cloud session the same day, W1176.)
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

- **All work is in git.** PR #462 (rounds W785–W1118) was merged into `main` on 2026-11-19, PR #463 (rounds
  W1119–W1175) on 2026-11-20, and PR #465 (rounds W1176–W1184) and PR #466 (rounds W1185–W1189) on 2026-11-21,
  each on your instruction or decision; the cloud session merged #463, #465 and #466, each with all six checks
  green. Later rounds are on `main-l1fsqo`, carried by the pull request opened after #466 was merged.
- **The plan,** on 2026-11-20: 97 of 119 items done (P1 18/18 · P2 39/41 · P3 30/32 · P4 3/6 · P5 7/22). P2.40 and P2.41
  have every row closed, and close on the final audit. The current figures are the PLAN NOW block of
  `docs/FABLE_DELIVERY_PROMPT.md`.
- **Measured remaining work,** on 2026-11-10: about 214–392 rounds across the 32 items then open, most of it in the
  fifth phase (143–265). Much of that phase is ruled to come after sign-in (P4.1), which is your switch, made in
  the release machine's own settings at its first deploy, together with its domain and HTTPS; the final audit
  runs after the fifth phase and the sign-in readiness round. Details per item in `docs/REMAINING_WORK_MEASURED.md`.
- **Owner rulings in force:** those recorded in the plan, including 2026-11-06 (five decisions taken as
  recommended), 2026-11-10 (decisions go with the recommendation; PR #461 merged), 2026-11-19 (twenty-two
  recommendations accepted; the six switches proceed in the ruled order, each once its pre-flight is built and
  measured; PR #462 merged), 2026-11-20 (that day's recommendations accepted, and that afternoon the ten
  decisions put to you, each taken as recommended; among them, the cycles run into December) and 2026-11-21
  (five decisions taken as recommended: PR #465 merged once green; how the Care reviewer's calibration run
  counts, when FU-1054 closes, and that a case flagged for its own reason and others is caught; P5.18
  clause 4's comparison of named finance products kept closed; and that afternoon, six more taken as
  recommended: the release machine to open a port to the internet only with its domain, HTTPS and sign-in on,
  the domain bought before the first deploy and sign-in your switch; your second calibration run, with a larger
  local model (seven to eight billion parameters if your machine has about 16 GB of memory), once the cloud
  session's three fixes have landed and before 2027-01-10; the Care review item to close when its clauses are
  built and its rows closed, calibrated or not; PR #466 merged by the cloud session once W1189's checks were
  green; the four test-runner faults whose cause was never found to close as not reproduced after twenty
  consecutive green CI runs; and your letters to be sent in the week from 21 November, the Quran platform item
  carrying into January if no written permission for recordings has come by 15 December).
- **Still yours:**
  - Merge the open pull request from `main-l1fsqo` when you are ready, or ask the cloud session to merge it
    once green, as you did for PR #463, PR #465 and PR #466.
  - The row in step 5: FU-1165, a step there.
  - One line in `.env` on your machine for the legal matter's folder (step 3 of the prompt), if the local
    session has not added it.
  - Sending the two permission letters in `docs/letters/` (FU-1188), in the week from 21 November.
  - Sending the request to the Quranic Audio Dataset's authors, also in `docs/letters/` (FU-1283), in the week
    from 21 November.
  - At the first deploy, restoring the data disk once from its snapshot, watching (FU-1288).
  - Buying a domain for the release machine before the first deploy and pointing it at the machine's fixed
    address (FU-1289): without it the machine is to publish no port (P4.1).
  - At the first deploy, an uptime check on `/health` from your own cloud account, beside the billing alert
    (FU-1095).
  - At the first deploy, setting the admin password on the release machine and switching sign-in on in its own
    settings (P4.1; the setting W1191 adds), so that it answers from its first boot with its domain, HTTPS and
    sign-in on; the password and the signing secret stay on the machine, never in the repository. Since W1191 the
    domain and sign-in are set together (docs/DEPLOYMENT.md, step 12).
  - Your second calibration run of the Care reviewer, on your machine with a larger local model (seven to eight
    billion parameters, such as llama3.1:8b, if your machine has about 16 GB of memory), when the cloud session
    says its three fixes have landed, and before 2027-01-10 (FU-1831, P5.15).
  - What no round takes (ruling of 2026-11-19): the deploy on your Google Cloud project, the external-model key,
    and real money, which stays off until a compliance and KYC review by qualified people. On the evening of
    2026-11-20 you recorded outside models and real money as dated boundaries (P4.3, P4.6), so P4 completes
    without either being switched on.
  - One solicitor's engagement before anyone but you is invited (FU-1817): the Law pages before any public
    release, and where other people's data may be kept.
  - Five to eight short interviews with teachers or tutors before the first offer is chosen (FU-1818).
  - Revoking at their providers the credentials W729 redacted from three archived files in the repository, or
    confirming that each no longer works (FU-1837; the plan's list names each by its kind), and with them two earlier
    Stripe values, a live secret key and a webhook signing secret, that the March copies hold and W729 never
    redacted. Redaction does not remove the redacted values from history: the repository has held most of them since
    March 2026, and most of its other branches still carry unredacted copies. And the key in the openQuran archive's
    .env on your machine, which was never in the repository. Read the repository host's secret-scanning alert list
    first, and tell the cloud session the date once it is done. Added to your list at your request on 2026-11-21, to
    be done soon.
- **Settled on 2026-11-20:** the five places that named your Windows home folder (FU-1286, closed W1180), each
  as you accepted that day: `venv/` was untracked on your machine (7afa4aa9, merged into `main-l1fsqo` at
  07fb9817), the folder kept on your disk; the three permissions in `.claude/settings.json` were removed in the
  cloud session (W1176); the pinned fidelity ledgers and `_archive/` stay as they are; and the audit record
  (docs/fidelity_runs/ledger_v14_W639_375c5ffb.json) was edited in the cloud session on 2026-11-20, on your
  go-ahead naming it (W1175).
- **Settled on 2026-11-21:** the Care reviewer's first calibration run (FU-1054, closed W1188), made on your
  machine through the agent's own door with the local model (llama3.2): run cal-8c7430765c left five cases
  unanswered, caught 5 of 10 planted cases and raised 4 false alarms in 6 clean ones, so it calibrates nothing
  and the reviewer is uncalibrated. It was committed (c657e2a7) and merged at c76809a8, and what it missed is
  FU-1831.
