# Production hardening brief — the outside help a production deployment would need

**DRAFT until the Owner ratifies it.** Written for plan item P5.7 (row FU-812). It scopes the work in separable parts,
so that each can be given to whoever is best placed to do it. Each part says what exists in this tree now, what
evidence would show the part done, and how to choose who does it. No supplier is named: a name enters only after it
has been checked against the criteria in the last section. Nothing here is legal advice, and nothing here deploys
anything. The deploy itself is plan item P4.5, and the switch is the Owner's.

## How to read this brief

- Every statement carries a label: [observed] is read from this tree on 2026-11-13; [inference] is reasoned from what was observed; [deferred] waits on a plan item or a decision; [owner decision] is the Owner's to make. [observed]
- A part is done when its evidence exists and a person other than its author has read it. A part is not done because a supplier says so. [inference]

## 1. Review

- The code is reviewed by its own suite on every push: `.github/workflows/spine.yml` runs the integration suite on Linux and Windows, the production build, a browser smoke and an import check. [observed]
- Two instruments check the perimeter and the tree for private data: `scripts/auth_perimeter.py` lists every route and what guards it, and `scripts/privacy_check.py` searches the tree for private-kind text. `integration_tests/test_no_committed_credentials.py` fails on a committed key. [observed]
- No person outside this project has reviewed the code, its security or its data handling. [observed]
- Done looks like this: a written review of one stated commit, covering authentication, authorisation, input handling, the AI boundary and data at rest, where each finding becomes a register row and is closed or accepted by the Owner in writing. [inference]

## 2. Reproducible deployment

- `requirements.txt` is exported from the lock, and the lock is made from `pyproject.toml`, so CI and a deploy install the same versions (W906). A fresh environment built only from it ran the whole suite (W907). [observed]
- The production image does not yet serve the pages, nor carry the law corpus or the plan: row FU-1156. The Google Cloud path has no pre-flight: row FU-603. [observed]
- Done looks like this: an image built from a clean checkout of one commit serves `GET /health` and the pages, a dry run of the deploy steps in `docs/DEPLOYMENT.md` is recorded with its output, and a second person repeats it from the document alone. [inference]

## 3. Secrets and access

- Keys are read from the environment and never committed, and the suite fails on a committed credential. External AI providers stay off unless the Owner switches them on. [observed]
- Sign-in is built and off: switching it on is plan item P4.1, the Owner's. Until it is on, the deployment has no per-person access control. [observed]
- Done looks like this: every secret held in the host's own secret store and read at start, a rotation carried out once and recorded, administrator access limited to named people, and sign-in on with its suite green. [deferred]

## 4. Dependencies

- Every dependency is declared once, in `pyproject.toml`, and the nineteen the Owner approved for removal are gone (W907, see `docs/DEPENDENCY_VERDICTS.md`). Three more are reached by nothing live and wait on the Owner: row FU-1174. [observed]
- No vulnerability scan has been run on the lock. [observed]
- Done looks like this: a scan of the lock with every finding triaged in writing (fixed, not reachable, or accepted by the Owner), repeated on each dependency change. [inference]

## 5. Backup and restore, demonstrated

- Every store is a file under one data root (`agentic_core/store_paths.py`). No backup script exists, and no restore has ever been carried out. [observed]
- A database is plan item P4.4, and its migration dry-run and rollback have not been started: row FU-284. [observed]
- Done looks like this: a backup taken on a schedule, a restore onto a clean machine timed and recorded, and the suite run against the restored data. A backup that has never been restored is not counted. [inference]

## 6. Monitoring and incident response

- Every route failure is recorded and shown on the Operations page (`GET /api/v1/operations/failures`). Nothing sends a failure to anyone: row FU-1095, whose outside uptime check the Owner sets up at the first deploy. [observed]
- Done looks like this: the uptime check driven once (the service stopped, the alert received, the service started, the alert cleared), and a written incident procedure saying who is told, how and within what time, rehearsed once. [deferred]

## 7. Limits

- The app limits itself in four places: calls through the AI gateway (a governed rate), sign-in attempts per name and per address, external AI calls per hour, and the work budget. [observed]
- Nothing has measured the app's memory or response times on the machine it would run on: row FU-603 asks for the peak-memory measurement. [observed]
- Done looks like this: a load test of stated shape against the target machine, with its peak memory, its slowest routes and the point where it refuses work, recorded with the commit it ran on. [inference]

## 8. Privacy and retention

- A learner's record can be exported (`GET /api/v1/qep/learner/{uid}/export`) and deleted (`DELETE /api/v1/qep/learner/{uid}`). A call to an external AI says what class of data it carries, and a legal matter never leaves (`agentic_core/ai/data_class.py`). [observed]
- No store has a stated retention period, and no deletion request has been carried through every store a person's data reaches. [observed]
- Done looks like this: a retention period for each store with its reason, a deletion request driven end to end and read back, and a record of processing the Owner has approved. [owner decision]

## 9. Rollback and shutdown

- `docs/DEPLOYMENT.md` has no rollback step and no shutdown step. [observed]
- Done looks like this: a return to the previous release carried out once on a running deployment, and a shutdown that keeps the data root carried out once, each recorded with the time it took. [inference]

## 10. Handover

- The working state of the project is written down: `docs/HANDOVER_W626.md` for the round discipline, the register of open rows, and the plan with its items. [observed]
- Done looks like this: a person who has not worked on the project deploys it from the documents alone, and every question they had to ask becomes a sentence in the documents. [inference]

## Choosing who does each part

- Independence: whoever reviews a part did not build it. The review in part 1 and the restore in part 5 are the two where this matters most. [inference]
- Evidence of the same work done before, read from the supplier's own published material and checked, not taken from a sales conversation. [inference]
- A written deliverable per part, against this brief's own "done looks like this", owned by the Owner. [inference]
- Data protection terms in place before any access to the data root, and access removed when the part is done. [owner decision]
- Which parts are bought and which are done in-house, and in what order, is the Owner's call. [owner decision]
