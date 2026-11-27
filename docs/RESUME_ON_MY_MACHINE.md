# Resume on my machine — the one prompt to paste

When you want to continue locally, open Claude Code (Claude Opus 5.5) **in your local clone** (`~\Workstation`)
and paste the block below as your first message. Nothing else is needed.

Updated 2026-11-22 (W1131, W1164, W1184, W1187, W1188, W1190, W1191, W1192, W1193, W1193b, W1193c, W1199, W1193d). The cloud session works in 8-hour cycles into December, until the plan's
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
   The pull request this step means is PR #467 until it is merged: on the morning of 2026-11-22 I told the cloud
   session to merge it once W1193c has landed and CI is green, as I did for #463, #465 and #466, and then to open a
   fresh one for the build rounds, which this step means from then on.
2. Read, in this order: docs/REMAINING_WORK_MEASURED.md (every open item, measured 2026-11-22),
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
   - FU-1840: as I ruled on 2026-11-22, read your notes on this machine and list each lesson derived since W677, the
     round it cites and your recommendation: add it to the batch, or say why not. I ratify the batch in one sitting;
     nothing enters the method until I have ratified the batch.
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
  PR #33 (opened 2026-03-12, before the plan) was closed unmerged on 2026-11-22, on your word; its branch is left.
  On the morning of 2026-11-22 you told the cloud session to merge the pull request opened after #466 was merged, PR
  #467, once W1193c has landed and CI is green, as it merged #463, #465 and #466, and then to open a fresh pull
  request for the build rounds, which carries the later rounds from then on.
- **The plan,** on 2026-11-20: 97 of 119 items done (P1 18/18 · P2 39/41 · P3 30/32 · P4 3/6 · P5 7/22). P2.40 and P2.41
  have every row closed, and close on the final audit. The current figures are the PLAN NOW block of
  `docs/FABLE_DELIVERY_PROMPT.md`.
- **Measured remaining work,** on 2026-11-22: about 147.75–288.5 rounds across the 22 items open, most of it in the
  fifth phase (105.75–213). Much of that phase is ruled to come after sign-in (P4.1), which is your switch, made in
  the release machine's own settings at its first deploy, together with its domain and HTTPS; the final audit runs
  after the fifth phase and the sign-in readiness round. By your rulings of 2026-11-22, P5.8 and P5.9 are to be
  built now, driven with sign-in on in a test process.
  Details per item in `docs/REMAINING_WORK_MEASURED.md`.
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
- **Ruled on 2026-11-22:** twenty recommendations, each taken as recommended: revoking the W729 credentials that
  day, with no branch deleted or changed without your explicit word (FU-1837); an entity's people and its money
  (P5.8, P5.9) to be built now and driven with sign-in on in a test process, a person's own record of their week
  with no health field until a data protection impact assessment that you and the solicitor review, and invoices
  naming outside parties and real payroll held; the avatar and upload memory to be retired; a model to be made the
  serving default only with its licence read, with no override; the work budget's readers on the platform's total
  until a second person runs work; a founder's own Chief, Board and budget figure with sign-in on, for their own
  entities only; a deletion drill to be built now, the retention
  periods yours once the solicitor answers; the canvas amended on your word for the platform's fee and the owner's
  share, its earlier words kept (the vision's section 12 and the economic model's sections 4 and 7 were given
  dated records of your rulings of 2026-10-12, which that day's word did not cover); the solicitor's engagement to
  carry the licence, title and investment questions (FU-1817); the deferred measures and the canvas's first tests
  put on your list (FU-1839); a teacher shown both outputs at the end of an interview, labelled, and the first
  offer's gate evidenced at five recorded interviews and your recorded choice (FU-1818); the generation credit to
  be carried forward against later fees; no valuation material yet; PR #33 closed unmerged; a scholar or trusted
  institute asked for now (FU-1838); the lessons since W677 ratified in one sitting (FU-1840, step 5), the 8-hour
  cycles replacing the three-stretch rule and the six working rules going into the method; and the tajwid
  companion to be built and held, its examples said as not available until a recording source permits them. The
  standing answer for the outside "digital mitochondria" prompts is to be recorded with the assessment's next
  section (a later round). W1193 recorded that standing answer in section 35 of
  docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md.
- **Ruled on the morning of 2026-11-22:** six recommendations put in the early hours and three put that morning,
  each taken as recommended: chromadb to be removed from the dependency list once the retired memory is removed, the
  same way the unused streamlit, plotly and pandas packages were taken out, with a full test run on a fresh install
  (round W1230, no longer held); the two legal-form descriptions to be reworded to say what each template models,
  the nine names kept and the old words kept in a dated note (round W1231, no longer held); the solicitor also to be
  asked in writing about retention and erasure, and you to approve a record of processing once the solicitor has
  answered (FU-1817), the deletion-drill rounds going ahead either way, every retention period marked "not decided:
  the Owner's"; the ratified canvas's credit line given a dated note for your carry-forward ruling, its old words
  kept; the business plan given the dated note the canvas was given for the platform's fee and the owner's share,
  saying the platform's 25% fee comes first and 20 parts in a hundred of what remains go to each entity's own owner,
  its old words kept; "after Phase 5" meaning after its build items close, so the final audit runs in December, the
  rows still waiting on you (the letters and the second Care calibration) listed in its record as open and carrying
  into January without holding it back (FU-1086); the three exchange lessons you already ratified to keep the
  section 27 counts their defects quote, as dated quotations of what was measured at the time, the section 27 totals
  staying in the assessment; PR #467 to be merged by the cloud session once W1193c has landed and CI is green, and a
  fresh pull request then opened for the build rounds; and, once you have revoked the leaked keys, the two earlier
  Stripe values among them, the stale branches that hold them listed for you to check, main, main-l1fsqo,
  local-owner and anything else you name kept, and none deleted without your explicit word (FU-1837). W1193c
  recorded each where the work reads it.
- **Ruled on the evening of 2026-11-22:** the decisions put in chat that evening, each taken as recommended, in your
  words "I want to go with all your recommendations, all items for me I will return to soon keep collating proceed
  with rest": a sale to post its declared cost, naming the receipt, unless that cost is already on the books (P5.2,
  whose sale piece builds to it); the Law page's partnership_deed template added to the solicitor engagement
  (FU-1817) as a written question, and kept held meanwhile; the second Care calibration run also to wait for
  FU-1822, settled first, in 0.5-1 round, before 2027-01-10; NICE's terms on quoting NG249 1.1.1 verbatim put to the
  solicitor (FU-1817), nothing changing now; the scholar letter (W1199): you fill the blanks and send it as drafted,
  your act, later; the full-clone credential history scan (W1208): you run it on a mirror clone and rotate any value
  not yet rotated, your act, later; the teacher-interview record format W1201 defines accepted, and it may be
  written into the notes template; and your own rows, which you will return to. W1193d recorded each where the work
  reads it; your acts stay on the list below, and none is closed.
- **Still yours:**
  - Merge the open pull request from `main-l1fsqo` when you are ready, or ask the cloud session to merge it
    once green, as you did for PR #463, PR #465 and PR #466.
    On the morning of 2026-11-22 you told it to merge PR #467 once W1193c has landed and CI is green; the fresh pull
    request it then opens carries the build rounds.
  - The rows in step 5: FU-1165 and FU-1840, each a step there.
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
    As you ruled on the evening of 2026-11-22, it also waits for FU-1822 (whether the reviewer may be shown the
    NEWS2 table), settled first, in 0.5-1 round, before 2027-01-10; the run's step is not yet in step 5.
  - What no round takes (ruling of 2026-11-19): the deploy on your Google Cloud project, the external-model key,
    and real money, which stays off until a compliance and KYC review by qualified people. On the evening of
    2026-11-20 you recorded outside models and real money as dated boundaries (P4.3, P4.6), so P4 completes
    without either being switched on.
  - One solicitor's engagement before anyone but you is invited (FU-1817): the Law pages before any public
    release, and where other people's data may be kept. As you ruled on 2026-11-22, it also carries written
    questions on the project's licence and title and on the investment-side perimeter, and is to review with you
    the data protection impact assessment to be drafted before any health-related wellbeing entry.
    As you ruled on the morning of 2026-11-22, the solicitor is also to be asked in writing about retention and
    erasure, and you are to approve a record of processing once the solicitor has answered; the deletion-drill
    rounds go ahead either way, with every retention period marked "not decided: the Owner's".
    As you ruled on the evening of 2026-11-22, two more written questions go to it: the Law page's partnership_deed
    template, which stays held meanwhile, and NICE's terms on quoting NG249 1.1.1 verbatim, with nothing changing
    now.
  - Five to eight short interviews with teachers or tutors before the first offer is chosen (FU-1818). Each ends
    by showing both outputs, labelled, as you ruled on 2026-11-22.
    As you accepted on the evening of 2026-11-22, the interview record format W1201 defines is accepted, and it may
    be written into the notes template.
  - Revoking at their providers the credentials W729 redacted from three archived files in the repository, or
    confirming that each no longer works (FU-1837; the plan's list names each by its kind), and with them two earlier
    Stripe values, a live secret key and a webhook signing secret, that the March copies hold and W729 never
    redacted. Redaction does not remove the redacted values from history: the repository has held most of them since
    March 2026, and most of its other branches still carry unredacted copies. And the key in the openQuran archive's
    .env on your machine, which was never in the repository. Read the repository host's secret-scanning alert list
    first, and tell the cloud session the date once it is done. Added to your list at your request on 2026-11-21, to
    be done soon. On 2026-11-22 you accepted doing it that day. The cloud session may list stale branches for deletion; no
    branch is deleted or changed without the Owner's explicit word.
    Ruled on the morning of 2026-11-22: you revoke the leaked keys first; then the cloud session lists the stale
    branches that hold them for you to check, keeping main, main-l1fsqo, local-owner and anything else you name, and
    deletes only on your explicit word.
    As you accepted on the evening of 2026-11-22, you run the full-clone credential history scan (W1208) on a mirror
    clone and rotate any value not yet rotated; that is your act, later.
  - Asking a scholar or a trusted institute to review what the religious tools hold back for one (FU-1838), as you
    ruled on 2026-11-22.
  - Sending the request to a scholar or a trusted institute, drafted in `docs/letters/SCHOLAR_REVIEW_REQUEST.md`
    (FU-1838): it names no one, so fill in whom it goes to and your name and address, read it through, and
    send it from your own address.
    As you accepted on the evening of 2026-11-22, you fill the blanks and send it as drafted; that is your act,
    later.
  - After the first deploy, the channel test and the price test the canvas names first, each your act; the same
    row carries three measures the metrics document defers, not yet scheduled (FU-1839).
  - Ratifying in one sitting the lessons a local session lists from this machine's notes (FU-1840, step 5).
  - Opening a developer account at the Quran Foundation (FU-1882), after reading its developer terms whole; its
    credentials stay on the machine that runs the platform, never in the repository, and production use waits for
    the publisher's approval. Tell the cloud session the date it is open.
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
