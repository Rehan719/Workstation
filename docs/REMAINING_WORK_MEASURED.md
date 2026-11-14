# Remaining work, measured — 2026-11-10 (HEAD fc9e9c76)

Every open plan item, read against the code at the commit named above: what closes it, what exists, what is left,
a size in rounds and what it rests on, and what only the Owner can do. One round is one fix with its test (median
about 1.3 hours, from git). A size is an estimate with its basis, not a promise; an item marked unsized has none.
The register (docs/FOLLOWUPS.json) and the plan (docs/FABLE_DELIVERY_PROMPT.md) stay the source of truth; this
page is a measurement of them, dated, and is re-measured rather than edited when the work moves.

HOW IT WAS MEASURED: three read-only research agents, one per group of items (P2-P4, P5.1-P5.11, P5.12-P5.22),
each reading the item's text and the files it names and checking the plan's claims against the code. Their
findings are claims; the ones W787 turned into register rows were re-checked by hand first, and the rest are
recorded here as read, not verified. Sizes are theirs, each with its basis.

## By phase

| Phase | Open items | Size (rounds) | Unsized |
|---|---|---|---|
| P2 Reach and disclosure | 2 | 0–2 | 0 |
| P3 Capability | 2 | 50–87 | 0 |
| P4 The Owner's switches | 6 | 21–38 | 0 |
| P5 Commercialisation, rehearsed on virtual WST | 22 | 143–265 | 0 |

**All open items: 214–392 rounds**, before any rows a later audit adds.

## P2.40 — THE FIFTEENTH TRUTH PASS (M1 re-run, ledger v17 tier-1 x20, 12 agents)

- **Closes when:** ACCEPT: P2.22's six clauses, unchanged: (1) a clause closes when its mechanism holds nowhere it applies; (2) every fix is driven on the surface a person reads; (3) each carries a guard whose blind was seen RED; (4) where the honest fix is to stop claiming, the claim is removed and that is recorded as the fix; (5) no allowance for authorship; (6) M1 re-runs when this item closes, its agent count stated beside its Tier-1 count. WHICH RE-RUN: this item's own text records the Owner's 2026-10-12 ruling that THE FINAL AUDIT is uncapped and census-partitioned, built, guarded and calibrated in its own round, and run after the fifth phase and the authentication-readiness round. The committed ledger block calls W675 'the MID-WAY audit the Owner allowed on 2026-10-11', and W675's commit says it was 'the one audit the Owner allowed between the third phase and the fifth'. Read together, no capped re-run is held before the final audit, so ACCEPT (6) is met by P5.22's final audit and not by a fidelity_audit_v7.js twelve-agent run. v7 is capped (CAP default 20) and region-based, so it cannot meet P5.22's 'no region is capped' or 'the union of the slices equals the census'. W786 writes exactly this under P2.40 and guards it (test_w786_p240_and_p241_say_they_close_on_the_final_audit). Beyond the re-run, clauses (1)-(5) must hold for every closed row, and the final ledger must print the instrument's agent count beside the Tier-1 count.
- **Delivered by:** build
- **Size:** 0–1 rounds. Nothing of its own remains: all 25 rows are closed. 0-1 rounds is the bookkeeping when the final audit reports. The audit itself is P5.22's work (an instrument round, calibration, and a run in two configurations) and is 'unsized' here; it waits for the whole fifth phase. If the Owner orders a capped v7 re-run instead, that is one round by precedent (W629, W639, W654, W665 and W675 each re-ran, rendered and chartered in one round).
- **Open rows:** count: 0
- **Built now:**
  - All 25 riding rows are closed. The 20 tier-1 rows closed in W676 (commit e5515798: 'eighteen distinct defects ... 87 blinds driven red'). FU-1110 closed in W742, FU-1084, FU-1094 and FU-1098 in W752, and FU-1113 in W755. (docs/FOLLOWUPS.json (slot P2.40, 25 of 25 rows done))
  - 18 guards for the 18 distinct defects are present at HEAD (integration_tests/test_mvp_spine.py test_t1_r10_the_gate_reports_what_it_measured_and_marks_nothing_met_from_headings (line 59767) through test_t1_r60_a_beat_step_that_caught_its_own_failure_is_in_steps_failed (line 60626). The blinds are not kept in the tree, so '87 red' is the commit message's claim and is not verified.)
  - The audit instrument: six regions, one assessor and one refuter each (12 agents). The cap is an argument (default 20). It states coverage (surfaces_exercised), can be pointed with args.unexercised, follows residue rules, and refuses to run without head and date. (scripts/workflows/fidelity_audit_v7.js lines 49 (CAP), 60-77 (pointing and refusal), 99 (COMMON brief))
  - W785, committed as 34434b98 while this read ran: the repository path is an argument, the audit store defaults to the temp directory, and truth_sweep_inventory's ROOT is derived from __file__; guard test_w785, 3 blinds red, full suite 911 passed. This makes the CAPPED v7 instrument runnable off the Owner's machine; it is not the final audit's instrument. (git show 34434b98: scripts/workflows/fidelity_audit_v7.js:54,99; scripts/boot_audit_backend.py:30; scripts/truth_sweep_inventory.py:8)
  - A boot script for a fresh scratch store with AI_DISABLE_LOCAL=1 on :8031 that refuses a busy port. A Linux venv exists here (it is running the current suite). (scripts/boot_audit_backend.py; the session's venv)
  - Post-run tooling. The renderer refuses a home-directory path in a residue line. (scripts/refutation_gate.py; scripts/render_fidelity_ledger.py lines 146-148 (HOME_PATH) and 267-276; scripts/audit_returns.py (FU-990); scripts/audit_unexercised.py)
  - A pointing list for a capped re-run is prepared, outside the repo: 176 routes and 14 pages of v17's census were not exercised (this session's scratchpad unexercised_v17.json (from_record ledger_v17_W675_d90ca2d4.json))
  - The current ledger is edition 17; the next is 18 (docs/VISION_FIDELITY_LEDGER.md header: v17 (2026-10-12), measured at HEAD d90ca2d4)
- **Remaining:**
  - no row captures: THE FINAL AUDIT (P5.22, whose one row is FU-1086, high). An uncapped, census-partitioned instrument, built, guarded and calibrated in its own round, with each of P5.22's ACCEPT (1)-(7) driven red by a planted fault. It runs in both configurations (the native floor and the local model) after Phase 5 and the readiness round. No such instrument exists: scripts/workflows/ holds only fidelity_audit_v3.js and fidelity_audit_v7.js.; When it reports: record the standing Tier-1 count with the instrument's agent count (ACCEPT 6), render and archive the ledger, file the standing rows, and run followups.py done P2.40 (and P2.41).; Clauses (1)-(5) for the 25 closed rows rest on commit statements (W676 says 87 blinds red; blinds are not kept in the tree). The final audit is the only independent test of clause (1). audit_returns already judged 3 of v17's 4 return candidates to be returns of earlier findings.; Portability for any audit run on this Linux machine, left after W785: .claude/launch.json boots 'Backend M1 Audit' with venv\Scripts\python.exe; scripts/truth_sweep_inventory.py:56 still writes C:/tmp/w477_inventory.json; scripts/boot_signin_check_backend.py:21 still defaults to C:\tmp\signin_check. W785's guard regex catches none of the three.
- **Waits on:**
  - P5.22, the final audit: its instrument (FU-1086), then a run after Phase 5 (P5.1-P5.22) and the authentication-readiness round
  - P2.41 under the joint M1/M2 rule: its rows closed or routed to the Owner (W786)
  - W786 landing (landed as fc9e9c76)
- **Only the Owner can:**
  - Nothing beyond the rulings already made. A capped re-run before the final audit would need a new Owner ruling, because the recorded rulings allow none.
- **First round:** None of its own is due. The next round that advances it is P5.22's first: build the census slicer on scripts/audit_surface_census.py and scripts/audit_unexercised.py, so that every route and page of a fresh HEAD census lands in exactly one slice or the overlap is stated (P5.22 ACCEPT 1), and the union of the slices equals the census (ACCEPT 2). Drive each red with a planted fault: a route dropped from every slice, and a route placed in two. If it is to run here, fix the three Linux portability gaps above first.

## P2.41 — THE INVISIBLE SHORTFALLS, TENTH PASS (M2 re-run, ledger v17 tier-2 x33, 12 agents)

- **Closes when:** ACCEPT: P2.23's, unchanged: 'each surface either delivers what it implies or says, where it is read, what it does not do; a guard per fix with a blind seen RED'; and 'M1 and M2 re-run together when the tier-1 item and this item close.' By the rulings recorded at P2.40, that joint re-run is the final audit (P5.22), and W786 writes this here too. The M2 milestone line under it (Tier-2 count 0, reach scatter resolved) is the milestone's bar, not this item's: P2.23, P2.37 and P2.39 each closed on a non-zero re-run.
- **Delivered by:** build
- **Size:** 0–1 rounds. With W786 landed, no row of ours rides the item. 1 round if FU-1046's keep-the-reason half is split back out as a buildable row. Before W786 the figure was 2-4 rounds (FU-969 1, FU-1046 1-2, FU-1151 0-1). The final audit is P5.22's.
- **Open rows:** count: 3; note: 3 open at HEAD. After W786: 0 ride the item and 2 await the Owner.; need owner or owner machine: FU-1046: the 'why' half needs the moved books on the Owner's machine; FU-1151: an Owner decision, which the Owner asked to be worked in the local session
- **Built now:**
  - 57 of the 60 riding rows are closed (W676-W761) (docs/FOLLOWUPS.json slot P2.41)
  - FU-969 in part (W758): the QEP adaptation picker and the Solutions platform read the six domains from lib/taxonomy.ts (apps/workstation-superapp/src/components/qep/QEPIntelligence.tsx:20,207-208; apps/workstation-superapp/src/pages/SolutionsPlatform.tsx:13,60; integration_tests/test_mvp_spine.py:69756 test_w758_p241_cascade_design_is_signposted_and_pickers_use_the_six_domains)
  - FU-969 in part: an off-taxonomy domain is shown as 'outside the six domains' wherever domain_label or domainLabel is used (agentic_core/taxonomy.py domain_label (above normalise_domain at line 121))
  - FU-1046 in part: the LATEST screen keeps its verdicts (capped at 12), but each history entry keeps only the overall result and the time (agentic_core/organism/heartbeat.py screen_living_vsb lines 145 (history entry) and 151 (latest verdicts))
  - FU-1151 in part, from the register only: v15's paths were replaced in W754, and the renderer refuses home-directory paths in residue lines (docs/FOLLOWUPS.json FU-1151 slot_source; scripts/render_fidelity_ledger.py:148,267-276. The run records under docs/fidelity_runs/ were not opened (out of scope).)
  - W786. The New-project form and the URL default now open on CANON_REALMS[0] instead of 'technology'. FU-1046 and FU-1151 move to the OWNER slot ('both can only be done on the Owner's own machine'). (git diff: apps/workstation-superapp/src/pages/projects/ProjectsHub.tsx:102-104,550; docs/FOLLOWUPS.json; test_w786_fu969_a_new_project_opens_on_a_canonical_subject)
- **Remaining:**
  - captured by open rows: FU-969 (open at HEAD; closed in W786's working tree). Left after it, and outside its smallest fix: POST /api/v1/projects/ still defaults realm 'general' and domain 'product' (agentic_core/projects/api.py:142-144,161-167), and normalise_domain defaults to 'enterprise' (agentic_core/taxonomy.py:121).; FU-1046 (a), buildable here: a section-11 FAIL keeps its reason. The history entry at agentic_core/organism/heartbeat.py:145 keeps only the overall result and the time, and the row also names agentic_core/api/change_control.py. W786 routes the whole row to the Owner, although this half needs none of his data.; FU-1046 (b), on the Owner's machine: find why the 2026-09-01 entity failed. Its text is in data/_moved_books_20261012-155706, which is absent from this container.; FU-1151, on the Owner's machine: the v16 note is to be restated as the kind of matter it was. W786 records the recommendation: edit each note to say only what kind of place or matter it was, and leave git history as ruled. Not verified: the files are out of scope.
  - no row captures: The final audit, shared with P2.40 and sized as P5.22's.; A rule to watch: P3.30's ACCEPT (3) moves a mis-tiered finding to the item that owns its tier. FU-855 is marked 'possibly tier 2', and re-tiering it would put a row back on this item.
- **Waits on:**
  - P5.22, the final audit (the joint M1/M2 re-run)
  - The Owner's machine for FU-1046's read and FU-1151's edit
- **Only the Owner can:**
  - On his machine: read the moved books for FU-1046, and decide FU-1151 (recommended: restate each note as a kind of place or matter, and leave git history).
- **First round:** Split FU-1046's buildable half into its own row and do it here. In agentic_core/organism/heartbeat.py screen_living_vsb, the history entry appended at line 145 keeps only the overall result and the time. Make a FAIL entry keep its failing verdicts (framework and reason, capped), and carry the reason into the change record the row names (agentic_core/api/change_control.py). Guard: screen a living VSB whose plan text trips one framework, and assert that the HISTORY entry, not only the latest record, carries the reason. Blind: drop the field and see the guard go red. Why the 2026-09-01 entity failed stays the Owner's to find, on his machine.

## P3.30 — THE DISCLOSED GAPS GET AN OWNER (M3 queue: tier-3 findings, one row per region)

- **Closes when:** ACCEPT: (1) every STUB, MISSING or DOC_OVERCLAIM among them is built, removed, or re-stated so the document no longer claims it; (2) for every PARTIAL and API_ONLY, the disclosure is DRIVEN at the surface and shown to reach the reader (a disclosure that exists only in an API field or a tooltip is not one); (3) a finding that on reading is mis-tiered is re-tiered with the reason stated and moved to the item that owns that tier, never closed here; (4) every fix is guarded on the property and driven RED; (5) M3 re-runs with M1 and M2 when this item's rows close, on an instrument that states its coverage.
- **Delivered by:** build
- **Size:** 44–77 rounds. The sum of the group estimates above. The plan's generated pace prices the item at about 49 rows at its own rate of about 1 row per round (W786's render says about 60). The high end prices each region row by its findings rather than as one row. ACCEPT (5)'s audit is P5.22's.
- **Open rows:** count: 49; need owner or owner machine: FU-869: the Owner names his two entities on his own store (PUT /api/v1/economy/protected-entities); the restore route is ours to build; FU-1116: whether a birth may be refused over capacity is the Owner's decision; FU-688: the row says 'for the Owner's sequencing'; it overlaps P5.1
- **Built now:**
  - 123 of the 172 riding rows are closed, recently one per round (W762-W784) (docs/FOLLOWUPS.json slot P3.30)
  - Two v17 region findings are already satisfied by later rounds. R2[9]: the direct stage advance is retired (W678/FU-965). R4[1]: the cognitive cascade's fixed threat score is now None with a basis (W730/FU-861). (agentic_core/projects/api.py:545-556; agentic_core/cognitive/hoshiyari_engine.py:28)
  - Disclosures already in code that ACCEPT (2) would drive at the surface: an off-taxonomy domain label, the protected-entities rule with its route for naming entities, quarantine of an unreadable capital-fund store, and the work budget's spend_basis (agentic_core/taxonomy.py domain_label; agentic_core/economy/turnover.py:19-80 and agentic_core/api/economy.py:982-1038; agentic_core/api/capital_fund.py:40-97; agentic_core/molecular/work_budget.py:326)
  - ACCEPT (5)'s instrument states its coverage (scripts/workflows/fidelity_audit_v7.js surfaces_exercised and args.unexercised)
- **Remaining:**
  - captured by open rows: The 49 rows, as grouped above (G1-G9).
  - no row captures: ACCEPT (2): driving each PARTIAL/API_ONLY disclosure at its surface (43 findings) lives only inside the six region rows; no row of its own measures it.; ACCEPT (3): re-tiering mis-tiered findings (FU-855 'possibly tier 2'; the region findings must be read for this).; ACCEPT (5): the M3 re-run with M1 and M2 after the rows close is, by the rulings recorded at P2.40, the final audit (P5.22). It is not counted here.
- **Waits on:**
  - The Owner's decisions on FU-1116 and his naming of entities for FU-869
  - ACCEPT (5) waits for the final audit (P5.22)
  - FU-688 is better done under P5.1
- **Only the Owner can:**
  - Name his two protected entities on his store (FU-869). Decide whether a birth may be refused over capacity (FU-1116). Sequence FU-688. Optional architecture decisions inside the region findings (a global output gate, R6[1]) are not needed for ACCEPT's honesty bar.
- **First round:** FU-984 (ledger v17 R5). (a) Run a reachability check, then archive the v280 gamification router (agentic_core/api/v280/gamification.py, mounted at agentic_core/app_mvp.py:288-290) and the cross_platform router (app_mvp.py:349-350) as reversible moves with one restore constant. Unmount PlayfulEffectsManager from apps/workstation-superapp/src/App.tsx; its store, store/gamificationStore.ts:24,33,41, is the only caller of /api/v280/gamification/*. (b) R5[2]: the Memorization card says flashcards, heatmap and audio are not built, and the 'Launch Full Dashboard' button goes (components/QEPFlagshipFeatures.tsx:158). (c) R5[3]: the avatar's empty-state line 'Responses are tailored to the ... context' (components/avatar/ConversationPanel.tsx:252) says what the floor does instead. Guard each (the routes answer retired, App.tsx no longer mounts the manager, the two sentences), with each blind seen red. The next round drives R5's four remaining disclosures at their pages and closes the row.

## P3.32 — A MODEL'S BEHAVIOUR IS MAPPED BEFORE ANYTHING IS SAID ABOUT ITS INSIDES

- **Closes when:** ACCEPT: 'a baseline run is reproducible from its recorded versions; a changed case set is a new version, never an edit; no page or response says a model's internal state was inspected, compared or altered; every clause guarded on the property and driven RED.' The clauses: (1) the evaluate route says what it establishes and what it does not; (2) a per-tier behavioural baseline with held-out cases and a control, stored with the model and case-set version, failures kept; (3) every model-describing surface states its evidence level, never above the first.
- **Delivered by:** build
- **Size:** 6–10 rounds. FU-1087 1-2; FU-1090 1; FU-1091 1; FU-1092 1-2; FU-1129 1; FU-892 1; FU-926 1; FU-918 0-1 (a browser view). At the low end FU-892 and FU-926 share a round and FU-918 folds into another.
- **Open rows:** count: 8; need owner or owner machine: FU-1087: the Owner's question whether promotion must also require a recorded baseline; FU-1091: recording the settings is buildable here, but showing it on a real model tier needs the Owner's machine
- **Built now:**
  - Clause 1 and a versioned public probe set: version '2', a pinned digest history, a CONTROL probe, and a refusal when a set is edited under its version. The evaluate answer carries marker_hits, the probe-set digest and the evidence level. (agentic_core/api/native_ai.py:366-415, 563, 600-606)
  - The held-out set in its own pinned file (version 1, three cases) with an exposure check (agentic_core/ai/native/heldout_cases.json; native_ai.py:432-486 (_load_heldout, _require_heldout), 488 (heldout_exposure))
  - A baseline per owned serving tier, run on demand, in an append-only store; any other tier is refused (POST /api/v1/native-ai/baseline/run at native_ai.py:796-808; store at 713-789; owned tiers only at 727-734; guard integration_tests/test_mvp_spine.py:56989 test_p3d_r8_a_baseline_is_pinned_held_out_on_demand_and_can_be_re_read)
  - Clause 3: an evidence-level table and route, plus a per-router count of served_by blocks that state a level, with declared not-an-answer blocks. A guard asserts that no undeclared block is silent. (native_ai.py:992-1027 (GET /evidence-levels), 1030-1100 (NOT_AN_ANSWER, _blocks_naming_a_model); test file around line 65922 (silent_not_declared == 0))
  - W745: installed models are described from the runtime, and research leads sit in a candidate register; nothing is downloaded (agentic_core/ai/native/model_resource.py:199 describe_installed; test file 67802 test_w745_the_installed_model_is_described_from_the_runtime_and_candidates_are_registered_not_downloaded)
  - A phrase scan for claims about a model's insides, over three roots (test file 57328 (agentic_core/api, agentic_core/ai, apps/workstation-superapp/src))
  - FU-918's code half: the evidence and baseline blocks sit outside the lifecycle card, and a failed read is shown (apps/workstation-superapp/src/pages/developers/NativeAI.tsx around lines 517 and 1059-1089)
- **Remaining:**
  - captured by open rows: FU-1087 (high): promote_model checks only that the model is installed. There is no runtime digest, licence line, evaluation state or research-lead refusal, and the effective default re-checks only the name (native_ai.py:1154-1170).; FU-1091: a baseline records no runtime settings, so ACCEPT's 'reproducible from its recorded versions' cannot hold on a model tier.; FU-1090: the held-out set has 3 cases (format, arithmetic, join). Add one each for injection, refusal without a source, malformed output and unsupported claim, each scored by a computed check, as a new version.; FU-1092: an answer names its server, never the model, its digest or the device. The row sequences this after token counting (FU-1100, on P4.3).; FU-1129: VISION_FAMILIES is a typed name list (agentic_core/ai/native/tiers.py:180); read the runtime's capabilities first.; FU-892: the claims scan reads three roots; docs/ and the other packages are unread.; FU-926: three typed statements stand where a probe exists. Which three was not verified.; FU-918: view the Native AI page with the lifecycle read failing (a browser check).
  - no row captures: Showing reproducibility on a served model tier needs a machine with a local runtime and a model. None is here (no ollama binary), so it needs the Owner's machine or his decision to download one.
- **Waits on:**
  - FU-1100 (P4.3) before FU-1092, per FU-1092's own row
  - The Owner's answer on FU-1087's baseline question
  - A machine with a local model to show model-tier reproducibility
- **Only the Owner can:**
  - Answer FU-1087's question (does promotion require a recorded baseline?). Any model download, and any baseline run on a real local model, are his.
- **First round:** FU-1087, the item's only high row. Drive POST /api/v1/native-ai/lifecycle/promote with model_resource.local_models patched to list a model, and first show that today's code promotes it with no licence or digest check (confirming the hypothesis). Then make promote store the runtime digest and return the licence line and evaluation state it relied on. Refuse with 409 and a stated reason when no licence text is held or the model is a research-only lead, with an admin force that leaves a UEG trail. The effective default holds only while the digest matches; patch describe_installed to report a different digest and assert the default falls back with its reason. Files: agentic_core/api/native_ai.py:1154 and agentic_core/ai/native/model_resource.py. One blind per refusal.

## P4.1 — AUTH_ENABLED on (the Owner's switch), after the authentication-readiness round

- **Closes when:** 'AUTH_ENABLED on, with the auth-ON suite green and the perimeter (P2.6) closed.' The Owner flips it, on his own machine, first in the switch order. Ours is the readiness round: an instrument reading every route's MOUNTED dependency against a declared public list; the business-plan routes ask who is calling; an issued API key authenticates; the read-only role is refused every write; the heartbeat acts only on an opted-in entity under a named service identity; for a high or critical change the decider differs from the submitter once a second administrator exists. Each is a row, driven with authentication on in a test process only.
- **Delivered by:** owner-switch
- **Size:** 9–16 rounds. FU-1120 1, FU-849 1-2, FU-850 1, FU-1152 1, FU-1089 1-2, FU-1061 4-8 (one guard per record-holding router group: a second person signs in and the first person's record is not found), plus 0-1 for the final strict re-measure.
- **Open rows:** count: 6
- **Built now:**
  - 4 of the 6 named readiness checks, plus the pages and status rows (see preflight_ours (W683, W686, W687, W688, W693, W706))
- **Remaining:**
  - captured by open rows: FU-849; FU-850; FU-1061 (group by group: projects, business plan, economy, uploads first); FU-1089; FU-1120; FU-1152
  - no row captures: As the last readiness act, re-run scripts/auth_perimeter.py --strict and every auth-on test after the rows close. The switch itself is the Owner's.
- **Waits on:**
  - P2.6 (DONE W505; the perimeter was closed at the mount in W683)
  - These rows before the Owner's switch, which comes first in the order: readiness, then auth on, then deploy, then invited, then self-serve, then external models, then money
- **Only the Owner can:**
  - Flip AUTH_ENABLED on his own machine and set JWT_SECRET and ADMIN_PASSWORD there. Decide whether to create a second administrator. Opt entities into the heartbeat once FU-849 is built.
- **First round:** FU-1120. In a test with AUTH_ENABLED=true (monkeypatched), call the VSB operating cycle (agentic_core/api/vsb.py:3601, which calls swarm.cascade_orchestration) and economy.deliver_contract (agentic_core/api/economy.py:1832) directly. Assert there is no AttributeError and the tiers run. Fix swarm.py:428 to 'user if isinstance(user, dict) else None', as line 511 already does, and sweep the other route functions that are called directly and read (user or {}). Blind: revert the line and see it go red.

## P4.2 — SELF_SERVE_SIGNUP (the Owner's switch), after an invited stage

- **Closes when:** 'SELF_SERVE_SIGNUP per the Owner; the 162 test-owned entities pruned only on instruction. BEFORE IT, AN INVITED STAGE: accounts only for people the Owner names. Self-serve opens only after every domain tool states the tier of review it has reached and the four exceptions to release on the platform's own review are enforced (religious content, a clinical score in direct care, regulated advice, real money).'
- **Delivered by:** owner-switch
- **Size:** 1–3 rounds. No row rides it. Our part is one exception-inventory guard and one invited-stage drive with sign-in on. 'unsized' for P5.15's release machinery, which this switch also waits on. FU-1089 and FU-1152 are counted under P4.1.
- **Open rows:** count: 0
- **Built now:**
  - The invited-stage mechanism, the review-tier statement, and three of the four exception holds in place (see preflight_ours)
- **Remaining:**
  - no row captures: A guard that maps each of the four exceptions to the check that holds it, and fails when one has none. The Care early-warning score is the likely gap.; The release machinery itself is P5.15's (a calibrated reviewer agent and the release rule). Not sized here.
- **Waits on:**
  - P4.1 switched on
  - FU-1089 and FU-1152 (P4.1 rows)
  - P5.15's calibrated reviewer agent and release rule
  - The switch order (after a private deploy)
- **Only the Owner can:**
  - Name the invited people. Flip SELF_SERVE_SIGNUP. Instruct the prune of the 162 test-owned entities on his store. Engage the people the four exceptions keep: a named scholar, a clinician, a solicitor, and three signatures for money.
- **First round:** Write one guard with sign-in on and self-serve off. /auth/signup answers 403; /auth/register refuses a non-admin and admits an admin. Then, for each of the four exceptions, name the enforcing check (scholar gate; Care withheld-on-terms; law route; REAL_MONEY_ENABLED) and assert that it refuses. The guard fails if an exception has no enforcing check. Expect the Care early-warning score to be the leg that has none, and register it as a row.

## P4.3 — AI_ALLOW_EXTERNAL + a key (the Owner's switch), as accelerants only

- **Closes when:** 'AI_ALLOW_EXTERNAL + a key, as accelerants only: the in-house-first order proven by test.'
- **Delivered by:** owner-switch
- **Size:** 5–7 rounds. FU-610 2-3 (declare a class at each external call site and refuse a barred class, driven over HTTP); FU-1088 1-2; FU-1100 1; FU-1128 1.
- **Open rows:** count: 4
- **Built now:**
  - The in-house-first order is proven by test on the query and stream paths, and the orchestrator path has a spend cap (see preflight_ours)
- **Remaining:**
  - captured by open rows: FU-610; FU-1088 (privacy fit tied to FU-610's data class); FU-1100; FU-1128
- **Waits on:**
  - FU-610 before FU-1088
  - The switch order: after auth on, the private deploy and the invited and self-serve stages
- **Only the Owner can:**
  - The key and the switch. Which data classes are barred beyond the legal-matter folder. The rung order and the hourly cap value.
- **First round:** FU-610's first cut. Add a data_class to gateway.query_meta and stream_meta and to the orchestrator's anthropic and openai branches (agentic_core/ai/gateway.py, agentic_core/ai/native/orchestrator.py:542-550), carried into the output's provenance. Bar 'legal_matter' (material from LEGAL_BUNDLE_DIR) before transmission. Guard, with the switch on, a placeholder key and a fake client that records calls: a legal-matter call never reaches the fake client and returns the floor with the refusal reason; an ordinary call reaches it and states its class. A blind on each leg. (FU-1128 is a one-round alternative.)

## P4.4 — Managed Postgres (the Owner's switch): DEFERRED and recorded as a boundary

- **Closes when:** 'Managed Postgres: migration dry-run script and rollback proven on a copy first. DEFERRED BY THE OWNER (2026-10-12) AND RECORDED AS A BOUNDARY until a measured need exists ... The database dependencies that nothing imports are removed (in halves, on a fresh install, as the earlier removal's retry plan says).' P4 is COMPLETE only when each switch is 'flipped or recorded as a section-18 boundary'.
- **Delivered by:** owner-switch
- **Size:** 1–2 rounds. One removal commit on a fresh venv built only from the new requirements.txt, with the full suite; a second if the halves split or the torch-absent boot failure recurs. It can share the run with P4.5's FU-604.
- **Open rows:** count: 1
- **Built now:**
  - The Owner's deferral recorded in the plan (docs/FABLE_DELIVERY_PROMPT.md P4.4)
- **Remaining:**
  - captured by open rows: FU-284, which needs re-scoping to the dependency half
  - no row captures: A dated section-18 line for the boundary, if the COMPLETE rule requires one in the vision (not verified).
- **Waits on:**
  - The FU-604 retry plan (P4.5): in halves, on a fresh venv, with the torch-absent scipy failure bisected
- **Only the Owner can:**
  - He has ruled (deferred). He decides if and when a measured need re-opens it.
- **First round:** Re-scope FU-284 to what the deferral leaves. Remove sqlalchemy, sqlmodel and psycopg2-binary from pyproject.toml and requirements.txt, and archive the unimported config/database.py. Run the full suite on a fresh venv built only from the new requirements.txt, in its own commit. Update docs/DEPENDENCY_VERDICTS.md:18-20. Guard: every declared runtime dependency is imported by live code or carries a verdict; blind it by re-adding one undeclared import.

## P4.5 — Production deploy on Google Cloud (the Owner's account), after a measured dry run

- **Closes when:** 'Production deploy on GOOGLE CLOUD ... from the Docker image that boots (W354), behind the Owner's account. The pre-flight is a DRY RUN a round builds and measures first; the project, billing and the deploy itself are the Owner's. THE FIRST DEPLOY is ONE small virtual machine on the free tier, PRIVATE TO THE OWNER, running the floor only, and only after the dry run has measured that the platform fits its memory.' Where another person's data may be kept is a solicitor's question.
- **Delivered by:** owner-switch
- **Size:** 5–9 rounds. FU-603 2-4: build and boot the image with a health probe, measure peak memory under a fixed floor drive against the free-tier VM, a secrets pattern, ephemeral-disk behaviour, a rollback drill, cost labels, and the docs only after a measured boot. FU-604 1-2. FU-607 1. FU-1095 1.
- **Open rows:** count: 4; need owner or owner machine: FU-1095: the uptime check e-mails the Owner from his own cloud account (the naming and the runbook are ours); FU-603: the dry run is ours; the GCP project, billing and the deploy are the Owner's
- **Built now:**
  - A Dockerfile whose COPY set is guarded statically, and a CI boot import check (Dockerfile; integration_tests/test_mvp_spine.py:5349; .github/workflows/spine.yml 'Boot check')
- **Remaining:**
  - captured by open rows: FU-603; FU-604; FU-607; FU-1095
  - no row captures: Decide how pages, docs/ and knowledge/ reach the single VM (in the image, or hosted separately). FU-603's 'container boots with a health probe' would not catch their absence.
- **Waits on:**
  - P4.1 (auth on, on the Owner's machine) precedes the deploy dry run in the switch order
  - FU-604 and FU-607, so the image installs the same code CI tests
  - The Owner's GCP project and billing
  - A solicitor's answer on US data residency before anyone else's data is stored
- **Only the Owner can:**
  - The GCP project, billing and the deploy itself. The billing alert and the uptime check's e-mail from his account. A solicitor's answer on where another person's data may be kept.
- **First round:** FU-603's first measurement. Build the image from the Dockerfile and boot it with AI_DISABLE_LOCAL=1 on an ephemeral DATA_DIR. Poll /health, drive a fixed set of floor requests (a Genesis journey, a deliverable, a beat), and record peak container memory (cgroup memory.peak or docker stats) against the free-tier VM's memory, the figure read at Google's own page. Record what the image lacks (dist, docs/, knowledge/). The report refuses when it measured nothing. Update docs/DEPLOYMENT.md only after the measurement, replacing its Render and Cloud Run text with the ruled single small VM.

## P4.6 — REAL_MONEY_ENABLED (the Owner's switch), last, after compliance/KYC review

- **Closes when:** 'REAL_MONEY_ENABLED only after compliance/KYC review. (Its other half is done: the Owner rotated the Stripe keys and expired the old ones on 2026-10-09. The switch itself is untouched and stays the Owner's.)' P4 is COMPLETE when M3 holds and every P4 switch is flipped or recorded as a section-18 boundary.
- **Delivered by:** owner-switch
- **Size:** 0–1 rounds. No row and no open pre-flight. At most one round to re-drive the payments mode matrix end to end before the Owner's switch.
- **Open rows:** count: 0
- **Built now:**
  - The triple gate and its guards (see preflight_ours)
- **Remaining:**
  - no row captures: Nothing of ours is open. The rest is P5's rehearsal and the Owner's review.
- **Waits on:**
  - P5.1-P5.5 and one whole rehearsal on virtual WST
  - P5.15's 'three people's signatures' before real money
  - Last in the switch order
- **Only the Owner can:**
  - The compliance/KYC review and a solicitor. The reviewed code change setting REAL_MONEY_ENABLED=True, plus STRIPE_LIVE_ENABLED and a live key. The three signatures.
- **First round:** None due now. When P5.1-P5.5 hold, re-drive simulation, test, live_gated and live with REAL_MONEY_ENABLED False, assert live is refused at every money door, and confirm FU-878's guard still finds no adapter that reaches a live call without the constant.

## P5.1 — One tenant, concept to commercial output, measured

- **Closes when:** Take one VSB from a stated problem to a delivered, priced, exportable output, each stage saying what it produced and what served it (engine or deterministic floor, named; an empty stage says so). ACCEPT (quoted): 'the journey is driven by a guard, not narrated in a doc; every stage's output is read back from the store it was written to; every figure on the summary is computed from those stores; and the provenance of each artefact travels with it into the export (W490's rule).'
- **Delivered by:** build
- **Size:** 12–34 rounds. ACCEPT work alone 4-9 rounds: the multi-stage guard with read-backs 2-4, the computed summary 1-2, the price leg once P5.2 exists 1, P5.10 clause 6 on this instrument 1-2. The 11 rows add 8-25: FU-399 is a migration of 81 text-scan guards (3-8); five rows are reproductions of intermittent stalls that may not close on demand. No P5 row has closed yet, so the item's own rate is unmeasured.
- **Open rows:** count: 11; ids: FU-301; FU-399; FU-417; FU-454; FU-605; FU-609; FU-1071; FU-1072; FU-1085; FU-1141; FU-1147; need owner or owner machine: id: FU-301; why: all-worker stall measured on Windows; the row's next look is Windows handle or process exhaustion, so it needs a Windows machine, most likely the Owner's (inference); id: FU-1072; why: seen in a 'local run' with one and two workers; probably the Owner's machine (not verified); note: Eight of the eleven (FU-301, FU-399, FU-417, FU-1071, FU-1072, FU-1085, FU-1141, FU-1147) are suite or CI health rows, three of them re-slotted here by Owner ruling 2026-10-07b; FU-605 and FU-609 are unrelated architecture leads; only FU-454 touches the journey. On 'done' open rows move along their routes, so they do not block the ACCEPT.
- **Built now:**
  - Genesis journey returns seven stage bodies with per-call provenance and stage verifications, and persists each run (agentic_core/api/genesis.py:322 genesis_journey (JourneyRequest :149 has establish and name; stage keys at :900-908); runs written to data_path('genesis_journeys') at :1230-1241)
  - Establishment of the entity from the journey (W735: Genesis records itself on the entities it establishes) (agentic_core/api/genesis.py:1447 POST /api/v1/genesis/establish)
  - Deliverable production and export; the exported Markdown carries the floor/model provenance phrase (agentic_core/api/deliverables.py:258 /produce, :1085 /{id}/export; _to_markdown calls _provenance_phrase (:418, :435))
  - Ship of every surface (repo last) and download of the entity body (agentic_core/api/vsb.py:3442 POST /{id}/repo/ship; :671 GET /{id}/repo/zip)
  - One operating cycle on virtual WST; revenue and costs are caller-typed with default 0 (agentic_core/api/economy.py:234 POST /api/v1/economy/cycle; CycleRequest :170-186)
  - A structure pass no longer earns; the delivery answer says no acceptance route exists (agentic_core/api/swarm.py:33 DELIVERY_EARNS_ON_GATE_PASS = False; :1172-1181)
  - The Genesis page already renders stages 3, 5 and 7 as their own cards beside the three phase cards (read from source, not rendered) (apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:863, :875, :958 (contradicts open row FU-454))
  - NOT BUILT: no guard drives one journey end to end; no price exists anywhere; no summary computed from the stores (no test in integration_tests/test_mvp_spine.py names P5.1 or a one-tenant journey; register row FU-688 (rides P3.30) is that guard and says 'not started')
- **Remaining:**
  - captured by open rows: FU-454: re-check by rendering; source already renders stages 3, 5 and 7, so it is probably closable with a rendered guard rather than a build; FU-399: migrate the page guards whose claim is about what is rendered onto the vitest renderer (a scheduled multi-round migration); FU-605: move core/transcendent_subsystems/tfel.py into agentic_core with its two importers (agentic_core/api/minimisation.py:48, agentic_core/avatars/core/recirculation_orchestrator.py:31); archive core/identity.py; FU-609: measure which fabric resources hold state between calls, then a lifecycle only where one exists; FU-1141: set the suite's GATEWAY_RPM default; the limiter sleeps holding one asyncio lock; FU-1147: route about twenty local block-comment strippers through the _code_only masking helpers; FU-301, FU-417, FU-1071, FU-1072, FU-1085: reproduce or record suite stalls and worker deaths; each closes only on a reproduction or a measured argument; (FU-688, riding P3.30 and not counted here, is the one-journey guard itself)
  - not captured by any row: The guard: problem -> Genesis journey -> establish -> name -> deliverable -> price -> ship -> zip -> one cycle -> export, each step read back from its own store and naming floor or engine, an empty stage saying so; A summary whose every figure is computed from those stores (a route, or the guard's own read), driven red; The priced stage (waits on P5.2; until then the honest answer is null with a reason); P5.10 clause 6 (rendered state of a short list of pages) is to be carried by this instrument; A decision whether 'delivered' includes a person's acceptance (acceptance is a post-sign-in record)
- **Waits on:**
  - items rulings switches: P5.2 for the priced stage (otherwise the price leg is null with a reason); FU-688 re-slotted from P3.30; Plan order puts P5 after P2.40 (Owner ruling 2026-10-12: its tier-1 rows fixed before the fifth phase begins; all 25 are closed, the item still awaits its M1 re-run), P2.41, P3.30, P3.32; P5.7 clause 1 and P5.10 clause 6 wait on this item
  - before sign in: The whole guard, on the floor, single user; it keeps nothing about another person.
  - after sign in: An acceptance leg by a person (FU-1003 / FU-1049), if 'delivered' is read as accepted.
- **Only the Owner can:**
  - None to build the guard.
  - The walk of the Owner's own endeavour (meal service first, registered fresh, on his machine with the model on; ruled 2026-10-12, docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md section 28.6) is his act and separate from the guard.
  - FU-301 and FU-1072 reproductions most likely need his Windows machine.
- **First round:** Re-slot FU-688 from P3.30 to P5.1, then write test_p51_one_tenant_journey_is_driven_and_read_back in integration_tests/test_mvp_spine.py on the isolated test store (client fixture): POST /api/v1/genesis/journey {problem, establish: true, name}; POST /api/v1/deliverables/produce scoped to the new entity; POST /api/v1/vsb/{id}/repo/ship; GET /api/v1/vsb/{id}/repo/zip; POST /api/v1/economy/cycle; GET /api/v1/deliverables/{id}/export?format=md. After each call read the record back from its own store (genesis_journeys, the VSB store, the deliverables store, the vsb_repos manifest, the entity ledger), assert each stage names its server ('native' on the floor) and that the export text carries the provenance phrase, and assert the price leg is null with a reason until P5.2 lands. Drive one blind per leg red (e.g. drop _provenance_phrase from deliverables._to_markdown).

## P5.2 — A price in WST, derived from the waterfall, never typed

- **Closes when:** A stated WST amount for a named deliverable with the arithmetic that produced it, derived from the waterfall and the entity's own costs, never hardcoded; missing cost inputs mean no price. ACCEPT (quoted): 'each price is recomputed from the waterfall on read, with a basis naming its inputs; changing a VSB's waterfall changes its prices; an absent input yields null and a reason, never a figure; and the ledger entry for a sale is a revenue event that the books already know how to consume.'
- **Delivered by:** build
- **Size:** 2–4 rounds. No rows; one new module, one route and four guard legs, on existing waterfall and revenue machinery. +1 if the formula ruling or the typed-price cleanup lands in its own round.
- **Open rows:** count: 0
- **Built now:**
  - Revenue events with consume/unconsume tokens, as the item says (agentic_core/economy/revenue.py:119 record_event, :162 consume_events, :198 unconsume_events)
  - Owner-adjustable, template-bounded per-VSB waterfall (agentic_core/api/economy.py:432 GET /api/v1/economy/waterfall, :540 POST (validate_waterfall, waterfall_bound_violations))
  - UEG logging of a waterfall change is best-effort: the append sits in try/except pass while the reply says 'logged to the UEG' unconditionally (agentic_core/api/economy.py:577-585 (except at :584), note at :590)
  - Declared costs exist only per cycle, typed by the caller, posted to operating_costs; no per-deliverable cost input exists (agentic_core/api/economy.py:184 CycleRequest.costs; agentic_core/economy/ledger.py:310 operating_costs)
  - Precedent for refusing a figure by naming its ruling (agentic_core/economy/qep_pricing.py:41-90 check_individual_price / check_institutional_price)
  - The Owner-set generation price (P5.16) is stated and charged by nothing (agentic_core/economy/generation_price.py:15 PRICE_GBP, statement(); served at agentic_core/api/genesis.py:190 GET /api/v1/genesis/price)
  - Typed prices a derived price would sit beside: a service contract defaults to 100 WST; a listing is priced by its creator; a reached route asks a model for a valuation range in pounds and WST, a pricing strategy and 1/3/5-year revenue projections (refused only on the floor) (agentic_core/api/economy.py:1508; agentic_core/api/marketplace.py:425-431; agentic_core/api/capital_fund.py:742 POST /api/v1/marketplace/value, called from apps/workstation-superapp/src/pages/marketplace/LivingMarketplace.tsx:506)
  - NOT BUILT: no pricing module, route or derived price (grep of agentic_core for a derived price: none)
- **Remaining:**
  - not captured by any row: The arithmetic: the waterfall splits a profit but does not set one, so 'derived from the waterfall and the entity's own costs' needs a margin or target the plan does not state; A pricing module and route that recompute on every read, with a basis naming the waterfall, the cost inputs and the formula; A per-deliverable cost input (declared, not typed into code); absent -> price null with the missing input named; Guard legs: waterfall change -> price changes; absent input -> null; a sale -> a revenue event the next cycle consumes; A decision on the typed contract default (100 WST) and the model-composed valuation route, which contradict 'never typed' for a priced deliverable
- **Waits on:**
  - items rulings switches: No hard dependency.; P5.16 clause 3 (25% of profit taken first, ruled 2026-10-12) changes the profit base the arithmetic works on; P5.5 and P5.1's priced stage wait on this item
  - before sign in: All of it: a price keeps nothing about a person.
  - after sign in: Nothing.
- **Only the Owner can:**
  - A ruling on the price arithmetic (what margin or target the derivation uses, and how the 25% fee taken first enters it) - recommended before building beyond the null-with-reason path.
  - Whether typed contract and listing prices and the model valuation route stay beside a derived price.
- **First round:** Build agentic_core/economy/pricing.py price_of(vsb_id, deliverable_id) that reads the effective waterfall through the same resolver GET /api/v1/economy/waterfall uses and the entity's declared cost for that deliverable, returning price_wst null with the missing input named whenever any input is absent, plus GET /api/v1/economy/price recomputing on read. Guard: absent cost -> null and reason; POST /api/v1/economy/waterfall changes the basis; a blind that returns a constant goes red. Put the arithmetic question to the Owner in the same round.

## P5.3 — Support operations: who answers when an autonomous entity is wrong

- **Closes when:** A tenant raises that an output is wrong; the claim is recorded against the artefact with its provenance, routed to Change Control like every other change, and its resolution UEG-logged. ACCEPT (quoted): 'a raised claim reaches a named owner through an executing path (not a comment); the artefact's provenance is part of the record; the UEG entry is hash-chained like the rest; and a claim nobody has answered is visible as OPEN, never closed by a timer.'
- **Delivered by:** build
- **Size:** 4–8 rounds. Plan calls it the P5 item most likely to take more than a round; tickets, Change Control and the UEG exist to build on. Claim path with guards 3-6, acceptance route 1-2 after sign-in.
- **Open rows:** count: 1; ids: FU-1003; need owner or owner machine: id: FU-1003; why: an acceptance keeps a person's record, so it is post-sign-in (the Owner's P4.1 switch); who may accept is not ruled (what acceptance earns was ruled 2026-10-12)
- **Built now:**
  - Support tickets (P3.18): ask, confirm (the only writer of 'resolved'), file a support-logic change with Change Control, SLA over confirmed records; each event attested and appended to the UEG. The item's 'no existing machinery' is stale for tickets, not for claims (agentic_core/api/support.py:111 /ask, :162 /confirm, :179 /policy-change -> change_control.submit_change, :228 /sla, :47 _attest_and_log)
  - Tickets hold no artefact, provenance or owner field (agentic_core/support/tickets.py:38 create_ticket, :164 listing)
  - Change Control tiers: CRITICAL is held until an explicit admin decision; a MEDIUM change with no model marker is decided by the organism-health rule (agentic_core/api/change_control.py:14-31; submit_change :863)
  - Hash-chain verification of the UEG (agentic_core/ueg/logger.py:97 verify_chain_detail)
  - Acceptance of a delivery switched off by constant, waiting for this item (agentic_core/api/swarm.py:33, :1172-1181)
  - NOT BUILT: a claim against an artefact, its provenance snapshot, a named owner, an OPEN listing (grep of agentic_core for a claim store or route: none)
- **Remaining:**
  - captured by open rows: FU-1003: the acceptance route, who may accept, and the event it records (to be built with the claims item)
  - not captured by any row: A claim store and route keyed to an artefact (deliverable, composition run, board pack) that copies its provenance, gate verdict and hash; Filing through Change Control under a tier that only a person decides (a MEDIUM filing would be closed by the health rule on the floor); A named owner resolved from the entity's owner record; with sign-in off, the Owner; UEG entries for raise and resolution, chain verified in the guard; OPEN visible on an API and a page; a guard that advancing the clock never closes a claim
- **Waits on:**
  - items rulings switches: An Owner ruling on the tier a claim is filed under; Sign-in on (P4.1) for claimants other than the Owner and for FU-1003; Related: FU-982 finding [1] (P3.30) - a MEDIUM review on the floor is decided by organism health
  - before sign in: The claim path with the Owner as the only raiser: artefact, provenance, Change Control, UEG, OPEN state (inference from the phase's sign-in split).
  - after sign in: Claims raised by invited people (the claimant is a record about a person) and the acceptance route (FU-1003).
- **Only the Owner can:**
  - Rule the claim's Change Control tier (CRITICAL keeps it open until a person decides).
  - Rule who may accept a delivery.
  - Turn sign-in on (P4.1) before claims from other people.
- **First round:** Add agentic_core/support/claims.py and POST /api/v1/support/claims {artefact_kind: 'deliverable', artefact_id, what_is_wrong}: load the deliverable from agentic_core/api/deliverables.py, copy its ai_provenance, quality gate and hash into the claim, file it with change_control.submit_change under a claim type held for an explicit decision, append support.claim_raised through _attest_and_log, and list claims at GET /api/v1/support/claims as OPEN until decided. Guard: raise one, read it back from the claim and Change Control stores, verify the UEG chain, advance the clock and assert still OPEN; blinds for a timer close, a dropped provenance and a MEDIUM filing each go red.

## P5.4 — The entity repository, handed over - it must live without this repo

- **Closes when:** The entity repository gets a version, a changelog of what changed between versions, and proof that a clean clone boots on its own. ACCEPT (quoted): 'the repo carries a version and a changelog generated from what actually changed; a clean clone is booted BY A GUARD and serves its own pages; and the manifest states plainly which parts are scaffold and which are the entity's own, so a reader is not handed a template as a business.'
- **Delivered by:** build
- **Size:** 3–6 rounds. No rows; four builds in one file plus one guard: version + changelog 1-2, manifest order + board pack + labelling 1-2, clone-and-serve guard 1-2.
- **Open rows:** count: 0
- **Built now:**
  - git init on first generation and one commit per generation (SHA3 hash-chain fallback without git) (agentic_core/api/vsb.py:382 _version_control_commit)
  - Repository generator with a manifest that labels web, webapp and mobile as generated or scaffold, keeps a manifest history, and carries the quality record (agentic_core/api/vsb.py:444-591 generate_vsb_repo; integrated_surfaces :557-560; :427 _manifest_history)
  - Detection of template-served documents and owner-written plan fields (inputs to a scaffold/own statement) (agentic_core/api/vsb.py:337 _body_served_by, :103 _owner_written)
  - Ship runs every surface then the repo; zip of the declared files, which excludes manifest.json and .git (agentic_core/api/vsb.py:3442-3470; :671-711; README note :165-167)
  - Content-hash versioning already exists for board packs (reusable for a repo VERSION) (agentic_core/api/vsb.py:1787 _pack_version)
  - CONTRADICTS THE ITEM TEXT: the board pack is stored outside the repository, and manifest.json is written after the commit, so a clean clone's HEAD carries the previous manifest or none (read from code, not driven) (board packs at data_path('vsb_board_packs') agentic_core/api/vsb.py:1565, :2115; commit at :542, manifest write at :584)
  - NOT BUILT: VERSION, CHANGELOG, a clone-and-boot guard, a run instruction or server in the repo (grep for changelog / git clone in agentic_core and the suite: none)
- **Remaining:**
  - not captured by any row: A version in the repo, moved only when content changes; CHANGELOG.md generated from the diff between versions; manifest.json written before the commit so the clone carries the manifest describing it; The board pack written into the repository it is said to be part of; A per-part 'scaffold | entity's own' statement in the manifest (today only three surfaces are labelled); A guard that clones into a temporary folder, serves the clone's own pages and reads them back; the repo needs its own run instruction
- **Waits on:**
  - items rulings switches: None. Related open P2.41 rows touch the same surfaces (FU-945: the phone app caches under a fixed name).
  - before sign in: All of it.
  - after sign in: Nothing.
- **Only the Owner can:**
  - none
- **First round:** In agentic_core/api/vsb.py generate_vsb_repo, write manifest.json and a VERSION (moved from the previous manifest only when the file digests change) BEFORE _version_control_commit, and write CHANGELOG.md from the names of files that changed since the last version. Guard: generate, POST /api/v1/vsb/{id}/concept with new text, generate again, git clone the entity repo from data/vsb_repos into tmp_path, and assert the clone's manifest matches the platform's copy, VERSION moved by one and CHANGELOG names the changed files; a blind that writes the manifest after the commit goes red.

## P5.5 — What is not for sale, stated plainly

- **Closes when:** Faith content (section 11), the Fitrah Spectrum (ruling A.9.5) and anything needing a real-money rail while section 18 stands are not for sale and not a paid tier. ACCEPT (quoted): 'the exclusions are served from one place the pricing surface reads, so a priced deliverable cannot name an excluded capability; a guard proves an attempt to price one is refused with a reason; and the refusal names the ruling it rests on.'
- **Delivered by:** build
- **Size:** 1–2 rounds. No rows; a small register and one refusal inside the pricing module P5.2 builds.
- **Open rows:** count: 0
- **Built now:**
  - Nothing for exclusions: no register, route or refusal (grep of agentic_core for not-for-sale / exclusions of capabilities: none (marketplace 'not for sale' means unpriced))
  - Precedents: refusals that name their ruling for QEP prices; A.9.5 cited in code; the real-money switch read without being set (agentic_core/economy/qep_pricing.py:41-90; agentic_core/horizon/consumption.py:183; agentic_core/organism/selection.py:30; agentic_core/economy/generation_price.py:26 _real_money_on)
- **Remaining:**
  - not captured by any row: One register of the three exclusions, each with its ruling, served by a route; The pricing surface (P5.2) reads it and refuses a deliverable naming an excluded capability, with the ruling in the reason; A guard driving one refusal per exclusion, driven red
- **Waits on:**
  - items rulings switches: P5.2 (there is no pricing surface to read the register yet)
  - before sign in: All of it.
  - after sign in: Nothing.
- **Only the Owner can:**
  - none
- **First round:** Once P5.2's pricing module exists: add agentic_core/economy/not_for_sale.py holding the three exclusions with their rulings, serve it at GET /api/v1/economy/not-for-sale, and make price_of refuse a deliverable whose domain, type or capability names one, with the ruling in the reason. Guard drives one refusal per exclusion; a blind that skips the check goes red.

## P5.6 — Workstation's own business case, written down, every statement labelled

- **Closes when:** Five documents under docs/business: canvas, business plan, founder's guide (Windows), evidence and KPI dictionary, living-strategy map. ACCEPT (quoted): 'every repository path, script, route and plan or row id a document names EXISTS (a guard reads the documents and checks each); every command in the guide was run on the tree it is committed with; no metric carries a figure without a named source; no price, user count, return or partner is stated as fact; each document says it is a DRAFT until the Owner ratifies it, and nothing enters the product's own plan as the Owner's words ...; the guard is driven RED.'
- **Delivered by:** build
- **Size:** 4–7 rounds. Three document rows at about one round each (W703 did two documents in one round), the guide 2-3 because its commands must be run and backup/restore written; the guard extension 1.
- **Open rows:** count: 3; ids: FU-742; FU-743; FU-744; need owner or owner machine: id: FU-742; why: the guide's Windows commands (set-up, start, health, tests, backup and restore) must be run on Windows: the Owner's machine, or the backend-windows CI job if that is accepted as 'the tree it is committed with'; this Linux session cannot run .ps1/.bat
- **Built now:**
  - Canvas and business plan written (W703), ratified by the Owner 2026-10-13, name line changed with his word 2026-10-14 (W725) (docs/business/BUSINESS_MODEL_CANVAS.md, docs/business/BUSINESS_PLAN.md)
  - A guard reading every docs/business/*.md: draft-or-ratified opening, files, plan items and row ids exist, every statement labelled, money only beside an Owner ruling, no count of people; driven on planted faults. It does NOT check routes, and only matches .py/.json/.md/.yml/.tsx files (integration_tests/test_mvp_spine.py _w703_faults and test_w703_the_business_documents_are_labelled_drafts_that_name_only_what_exists (:64629))
  - The Owner enters the ratified plan through the plan's own route, refused with sign-in off (/api/v1/business-plan/ratified/preview and /enter (W726 guard near test_mvp_spine.py:65790))
  - Metric sources that exist but hold no customer value (agentic_core/api/support.py:228 /sla and :273 /satisfaction; agentic_core/api/registers.py:58 /coverage; no product telemetry in agentic_core)
  - Inputs for the guide: deployment notes, Windows start scripts, a Windows CI job (docs/DEPLOYMENT.md; setup.ps1; start_backend.bat; .github/workflows/spine.yml:55-85 backend-windows)
- **Remaining:**
  - captured by open rows: FU-742: the founder's guide for a Windows machine, every command run on the committed tree, deployment costs per channel with no zero-bill promise; FU-743: the evidence and KPI dictionary (definition, source, denominator, freshness, or NOT MEASURED and what would measure it); FU-744: the living-strategy map (observe, propose, review, authorise, apply, record: component, file, what verified it, the open rows in the way)
  - not captured by any row: The guard must check every route a document names (and .ps1/.bat/.mjs/.js script names), which the ACCEPT requires and the W703 guard does not do; A mechanism that shows each guide command was run on the tree it is committed with
- **Waits on:**
  - items rulings switches: None hard. The guide's launch gates describe the P4 switches in their ruled order; nothing is switched by this item.
  - before sign in: All of it.
  - after sign in: Nothing.
- **Only the Owner can:**
  - Run, or accept a Windows CI run of, the founder's guide commands.
  - Ratify each new document when he chooses (each stays a DRAFT until then; not needed to close).
- **First round:** Extend _w703_faults in integration_tests/test_mvp_spine.py so every /api/v1/... route a document names must be a mounted route of the app, and .ps1/.bat/.mjs/.js/.sh files are checked, each with a planted fault driven red; then write docs/business/KPI_DICTIONARY.md (FU-743): each metric with definition, source, denominator and freshness, or NOT MEASURED and what would measure it - e.g. support resolution rate (GET /api/v1/support/sla), satisfaction (GET /api/v1/support/satisfaction), journeys a person can complete (GET /api/v1/registers/coverage), open register rows (docs/FOLLOWUPS.json).

## P5.7 — The working papers of a first sale, every one a draft, nothing sent

- **Closes when:** Seven drafts under docs/business: first-offer comparison and interview pack, cost model, name and brand screen, marketing drafts, route to support and partners, formation workpack, scope for outside help. ACCEPT (quoted): 'the guard of the item before this one reads these documents too (every path, route, script and row id named exists); every money figure carries a source and date or the word ASSUMED; no document states a customer, an interview, a partner, an endorsement, a price agreed or a name cleared; no personal detail of the Owner appears; every public-facing draft carries its DRAFT heading; and the guard is driven RED on each.'
- **Delivered by:** build
- **Size:** 7–11 rounds. Six document rows at about one round each, the clause 3 remainder 1, the guard changes 1-2; reading public pages adds time to FU-810 and FU-811.
- **Open rows:** count: 6; ids: FU-806; FU-807; FU-809; FU-810; FU-811; FU-812; note: None needs the Owner to write; every external act (sending a draft, contacting the course organisation, interviews, filing) is his and outside this item.
- **Built now:**
  - Name searched and ruled (FU-808 closed W725): Companies House and UK/EU trade mark registers read, one line in each ratified document, no clearance claimed (docs/business/BUSINESS_MODEL_CANVAS.md (Key resources); docs/business/BUSINESS_PLAN.md (Risks); test_w725_... (test_mvp_spine.py:65614))
  - Fees already read at publishers on 2026-10-11 and the course organisation named (docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md section 17.1 rows 8-12)
  - The W703 guard reads every docs/business/*.md, so new drafts are checked automatically - but its money rule (a figure only beside an Owner ruling) and its label rule would fail a sourced cost model or an interview guide as written (integration_tests/test_mvp_spine.py _w703_faults)
  - NOT BUILT: none of the seven documents exists (docs/business holds only the canvas and the plan) (ls docs/business)
- **Remaining:**
  - captured by open rows: FU-806: first-offer comparison, leading hypothesis, unsuitable customers, interview guide, willingness-to-pay questions, notes template (only after one journey is driven and read back); FU-807: cost model (quoted / sourced and dated / ASSUMED / not measured; lean, base, higher-assurance; founder's time apart; formulas without values; seven investment gates); FU-809: marketing drafts, each headed DRAFT - NOT APPROVED FOR PUBLICATION, each claim traced (built from the first offer); FU-810: public support routes and partner drafts read from their own pages and dated, or NOT CHECKED; FU-811: formation workpack (routes compared, none chosen; placeholder worksheet; official sources dated; questions for an accountant and a solicitor); FU-812: production-hardening brief in separable parts with acceptance evidence and selection criteria
  - not captured by any row: Clause 3's inventory of what the Owner holds and the register of each public claim with its evidence (asked by FU-808, which closed without them); Guard changes: money figure with source and date or ASSUMED; DRAFT heading on public-facing drafts; refusal of customer / interview / partner / endorsement / price agreed / name cleared; no personal detail of the Owner; each driven red
- **Waits on:**
  - items rulings switches: P5.6's guard (extended, not replaced); P5.1: the offer comparison (FU-806) and the marketing drafts built from it (FU-809) are written only after one tenant's journey is driven and read back
  - before sign in: All of it; nothing is stored about a person (no prospect tracker by ruling).
  - after sign in: Nothing.
- **Only the Owner can:**
  - The inventory of what he holds (accounts, domains, marks) beyond what the ratified documents already say.
  - Every external act and any choice of legal form (outside this item).
- **First round:** Change the W703 money rule so a figure in docs/business stands only with a quoted or sourced label naming the page and the date read, or the word ASSUMED, and add the DRAFT-heading and banned-claim rules, each with a planted fault driven red; then write docs/business/COST_MODEL.md (FU-807), re-reading each fee at its publisher's page with the date (assessment section 17.1 rows 8-11 were read 2026-10-11).

## P5.8 — An entity's people: seats, pay runs, a person's own record of their week

- **Closes when:** ACCEPT (quoted): 'an entity's page shows clause 1 with nothing filled that is not; a pay run the balance cannot cover is refused and an approved one posts exactly its lines, each labelled virtual; no route returns one person's wellbeing entry to another caller and no field ranks or scores a person; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 5–9 rounds. No rows; three clauses, each a store, a route, a page sentence and a guard: seats 1-2, pay runs 2-3, wellbeing 2-3, page 0-1.
- **Open rows:** count: 0
- **Built now:**
  - Nothing: no seat, pay run, payroll or wellbeing code (grep of agentic_core for seats / pay_run / payroll / wellbeing: none)
  - Reusable parts: one checked posting function; hold classes with no threshold; organisational roles that can stand as platform resources in a seat (agentic_core/economy/ledger.py post (chart guard ~:423, floor :443-451); agentic_core/economy/governance.py:35-40, :639-648; agentic_core/api/swarm.py:75 role table)
- **Remaining:**
  - not captured by any row: Clause 1 seats: list each seat and what fills it (platform resource, named person, nobody); vacant shown vacant; Clause 2 virtual pay runs: reserve to an expense account (needs a chart account), one line per person-held seat, refused for an unregistered entity or an uncovered balance, held for a person at any size, the 'pays nobody / not a payroll' sentences; Clause 3 wellbeing as a person's own record, readable only by that person unless shared, never scored or read by a model; A guard per clause driven red
- **Waits on:**
  - items rulings switches: Sign-in on (P4.1, the Owner's switch) and the readiness work landed (P4.1 rows FU-1089, FU-1152, FU-1061, FU-850, FU-849, FU-1120 open); Ruled sequence: after the fifth phase's first seven items (P5.1-P5.7); A data protection impact assessment before health-related entries
  - before sign in: Nothing is built; until then no record of a real person other than the Owner is held and the pages say so.
  - after sign in: All three clauses.
- **Only the Owner can:**
  - Turn sign-in on.
  - The data protection impact assessment for health-related entries (research can be drafted; the decision is his).
  - Real payroll stays behind the real-money ruling and a compliance review (boundary, not needed to build).
- **First round:** None until sign-in is on and P4.1's readiness rows are closed. Then: GET /api/v1/vsb/{id}/seats listing each organisational role with filled_by resource / person / none and a vacant seat shown vacant; guard: an entity with no person shows every person seat vacant, and a blind that fills a default name goes red.

## P5.9 — An entity's money on paper: profile, invoices and bills, what it owes, what it asked for

- **Closes when:** Before any clause a reconciliation read across ledger, owner payments, fund and roster; double-entry is the book of record; the payee comes from the entity's owner record; every figure says where its value entered; then six clauses. ACCEPT (quoted, abridged): 'a guard drives one invoice from draft to settled between two registered test entities and reads back the profile, the invoice, the hold, the transfer's posting and the view from their own stores; the same invoice sent twice is one invoice and the same settlement sent twice is one transfer; the trial balance holds after every step; a reversal leaves both postings in the books and the first unchanged; reconciliation names an invoice marked settled with no posting, a posting with no invoice, and an amount that differs ...; received cannot be entered; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 16–30 rounds. Eight rows (the three reconciliation rows fold into one instrument) about 7-11 rounds, the six clauses 10-17, plus 1-2 for FU-877 and FU-887 on P3.30, which the ruled sequence closes first.
- **Open rows:** count: 8; ids: FU-1004; FU-1005; FU-1006; FU-1007; FU-1008; FU-1009; FU-1010; FU-1049; need owner or owner machine: id: FU-1004; why: measured on the Owner's store; those books were moved aside by the Owner on 2026-10-12 (data/_moved_books_20261012-155706 on his machine), so checking them there needs his machine; id: FU-1005; why: the reversal can be built here; applying it to the real fund needs his machine and word (after the move his fund read nothing allocated - assessment 28.5); id: FU-1006; why: the code path can be read here; the data is on his store; id: FU-1007; why: code here; the 44 test-owner accounts are on his store; id: FU-1008; why: the population counts are on his store; id: FU-1009; why: the apex figures are on his store; id: FU-1049; why: an acceptance is a post-sign-in record (the Owner's P4.1 switch); what it earns was ruled 2026-10-12
- **Built now:**
  - Per-entity double-entry chart with no receivable, payable or liability account (agentic_core/economy/ledger.py:297-312 CHART)
  - Every new posting carries an identifier (W760) and a non-zero finite amount (W759); trial balance, statements, period close (agentic_core/economy/ledger.py:461 posting_id, :443-451, :581 trial_balance, :625 statements, :717 close_period)
  - A transfer request can carry an idempotency key, so a resend is one transfer (W759; supersedes the item's 'no request carries a key') (agentic_core/api/economy.py:1096-1098 TransferRequest.idempotency_key)
  - Stranded-transfer completion and a read-only report of where an entity's credits came from (agentic_core/economy/transfers.py:586 reconcile_receiver_legs, :686 intake_sources)
  - Service contracts offer, accept, deliver and settle through the transfer (agentic_core/api/economy.py:1674-2090)
  - Hold classes with no threshold (fund allocation, payout) (agentic_core/economy/governance.py:35-40, :639-648)
  - The payee is still the name stored on the account at first accrual (FU-1007 not built); a typed first-name default remains in accrue and the cycle request (agentic_core/economy/owner_payments.py:154 payee_of, :277 accrue; agentic_core/api/economy.py:186)
  - No reversal of a fund allocation (agentic_core/api/capital_fund.py (no reversal function))
  - NOT BUILT: profile, invoice, bill, obligation calendar, funding record, the read-only view, the cross-store reconciliation. One dead, unimportable stub returns a literal invoice id, revenue 1500.0 and 'audit: PASSED' (grep of agentic_core: none; agentic_core/business/pipelines.py:30 (listed in scripts/import_integrity_baseline.txt))
- **Remaining:**
  - captured by open rows: FU-1008, FU-1004, FU-1009: the reconciliation read (populations that do not match; pots versus postings; apex accrual versus owner pot); FU-1007: payee from the entity's owner record, the account name kept as history; FU-1005: a recorded reversal for the fund's three June test allocations; FU-1006: read the fund contribution path and say whether the gap is old data or a quiet failure; FU-1010: every figure says where its value entered; FU-1049: acceptance as a recorded act (who, when, which version), earning only an accepted contract's amount
  - not captured by any row: Labels: pots as a derived view, books older than double-entry as older; Clause 1 financial profile (declared / not declared fields beside registered or simulated status); Clause 2 invoices and bills: draft until approved, duplicate refusal, never edited once approved, settled only through the transfer carrying its number, held for a person, 'settled' only when the posting is found; Clause 3 reversal postings naming the first, its reason and who asked; Clause 4 what is owed and when (Owner-entered rows plus approved unsettled bills, the fixed no-tax sentence); Clause 5 funding record states, 'received' refused while money is virtual, permissibility NOT ASSESSED; Clause 6 one read-only view labelling virtual / declared / forecast and never adding across labels
- **Waits on:**
  - items rulings switches: Ruled: the rows found while reading for it are closed first - FU-877 and FU-887 are still open on P3.30; Ruled: a reconciliation read before any clause; Ruled sequence 'after the item before this one' (P5.8, which is built after sign-in) - read literally this puts P5.9 behind sign-in although most of it keeps nothing about a person; Sign-in for an invoice naming any party outside the Owner's own entities and for FU-1049
  - before sign in: Reconciliation, labels, payee, figure origins, profile, invoices and bills between the Owner's own registered entities, reversal, calendar, funding record, view.
  - after sign in: Invoices naming outside parties; acceptance (FU-1049).
- **Only the Owner can:**
  - Access to his store for the six rows measured on it.
  - A reading of the sequence (after P5.8, or beside the readiness round).
  - Later, a certificate before a funding record's permissibility reads anything but NOT ASSESSED (not needed to build).
- **First round:** Close FU-887 with FU-1007 in agentic_core/economy/owner_payments.py: payee_of resolves the payee from the entity's owner record and keeps the account's stored name as history, and an account whose entity has no record has no payee and says why. Guard: an account whose stored name differs from the entity's owner, and one with no entity, each read back; blind red. Next round: the read-only reconciliation instrument, driven on a test store made wrong in each way.

## P5.10 — A correction is effective when the next look does not find it again

- **Closes when:** Nine clauses: effectiveness check, fix rule, hotspot round, literal-outcome screen, calibrated audit, rendered state, nothing earns on a structure pass, triage, a model-on checklist. ACCEPT (quoted): 'clause 1 is driven on a record made to hold a returned finding; clause 4 fails on a typed outcome added to a handler; clause 5 reports three measured rates and their sample sizes; clause 6 fails when a page's condition is disabled; clause 7 is driven both ways; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 16–32 rounds. Twelve rows at about one round each, several larger (FU-1059 is eighteen-plus callers, FU-991 a hotspot rewrite, FU-993 a calibration run): 12-24; uncaptured clauses 4, 8, 9 and the clause 2/7 legs: 4-8.
- **Open rows:** count: 12; ids: FU-991; FU-992; FU-993; FU-995; FU-1036; FU-1038; FU-1039; FU-1040; FU-1059; FU-1060; FU-1142; FU-1143; need owner or owner machine: id: FU-1036; why: needs the local model configuration the Owner runs; id: FU-1038; why: the loop is turned on the Owner's own store; id: FU-1040; why: moving rows aside in his real store (earlier moves were made at his terminal); id: FU-1142; why: his decision whether the pre-isolation rows move (recommended no); id: FU-1039; why: code here; the 2,000 rows checked are on his store; id: FU-1059; why: its prepared classification and edit script are on his machine (C:/tmp paths); can be redone from the code
- **Built now:**
  - Clause 1: the effectiveness check lists candidate returns and fails while one is undecided, driven on a made record (FU-990 closed W749). Reopening the row and guarding the class stay a person's follow-through (scripts/audit_returns.py; test_w676_a_returned_finding_cannot_pass_unread (integration_tests/test_mvp_spine.py:60683))
  - Clause 2: the fix rule is in the method, ratified, with enforced_by null (docs/DELIVERY_METHOD.json lesson M-CORR-07)
  - Clause 7, one way: a structure pass no longer earns (FU-994 done W676); the acceptance way is not built (agentic_core/api/swarm.py:33, :1172-1181)
  - Clause 9 groundwork: a person's material is marked as data and its cut recorded, but only law.py and education.py use it (agentic_core/api/_ai_provenance.py:188 MATERIAL_SLOT, :192 wrap_material; callers agentic_core/api/law.py, agentic_core/api/education.py)
  - Clause 6 groundwork: one frontend test file for 124 .tsx files under src; a CI browser smoke renders routes (apps/workstation-superapp/src/pages/coe/KnowledgeHub.test.tsx; .github/workflows/spine.yml:101-145; scripts/browser_smoke.mjs)
  - Clause 8 groundwork: batches and bundles of rows are computed; no rule drops a tier-3 row on no reached surface (agentic_core/plan_followups.py:933-978)
  - Clauses 3, 4, 5: not built (a deny-list of known fabricated strings and a census over the cognitive package exist, not an allow-list over every answer; nothing plants defects in an audit) (integration_tests/test_mvp_spine.py test_frontend_fabrications_do_not_return; W730 commit 54ef5642; grep of scripts/workflows/fidelity_audit_v7.js for plant/calibrat: none)
- **Remaining:**
  - captured by open rows: FU-991 (clause 3): one source per stated fact in agentic_core/api/vsb.py and the establishment route; FU-992 (clause 6): rendered checks for pages; FU-993 (clause 5): planted defects and false findings in one slice; one slice to two assessors; FU-995, FU-1059 (clause 9): ingest paths, and 32 of 34 composing callers still to hand text over as marked material (three cut it silently); FU-1036: the audit in both configurations (floor and the Owner's local model); FU-1038: turn the durable defect loop once for real on the Owner's store; FU-1039: write the quality field from the gate; rankings say they rank what produced output; FU-1040, FU-1142: test-double rows and pre-isolation rows in the Owner's operations record; FU-1060: widen the sources check; domain pages read what their forms do from the registers; FU-1143: make the refutation gate's findings-against-verdicts reconciliation run
  - not captured by any row: Clause 4: a commit-time literal-outcome screen with an allow-list and reasons, failing on a typed outcome added to a handler; Clause 8: the triage rule (batch by file into a round already there, or drop with a reason when on no reached surface); Clause 9: the one model-on checklist document; Clause 2: a guard for the fix rule (or a stated reason why none can exist); Clause 7: the acceptance leg, driven both ways (shares the build of FU-1049 / FU-1003)
- **Waits on:**
  - items rulings switches: Ruled per clause: 1, 2, 7 with the tier-1 rounds; 3, 4, 8 before the fifth phase's selling items; 5 before the final audit (P5.22); 6 with P5.1; 9 before any local model is installed - already passed, since the plan records one is installed; Clause 7's acceptance leg after sign-in
  - before sign in: Clauses 1-6, 8, 9 and the rows; the quality store stays shared and says so.
  - after sign in: Clause 7's acceptance leg (an acceptance is a record about a person).
- **Only the Owner can:**
  - His machine and store for FU-1036, FU-1038, FU-1040 (and to verify FU-1039).
  - His decision on FU-1142.
- **First round:** FU-1059's three silent cuts: in agentic_core/api/career.py (classifier at 2,000 characters, generator at 600 a file) and agentic_core/api/employment.py (job search at 300), pass the person's text through ai_text(material=..., material_label=..., material_limit=...) as law.py analyse does, so the cut is recorded in provenance and said in the answer. Guard: post over-limit text with a capturing ai_text, assert the material markers, read_whole False and the partial-read sentence; one blind per caller red. (Clause 9 is overdue by its own sequence.)

## P5.11 — A person with a problem leaves with a date, a place to go and a list - none generated

- **Closes when:** Nine clauses inside the Law domain, England first. ACCEPT (quoted): 'clause 1's check fails on a row that claims a journey nothing drives; clause 2 is driven on the day before, the day of and the day after each change, at a month end and in a leap year, for each nation, and with no matching rule; clause 3's stale label is driven by date; clause 4 is driven with the screen made to return nothing; clause 5 and 6 are driven both ways; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 8–15 rounds. Two rows plus six clause builds: clause 2 2-4 (rules read at publishers plus the drive matrix), clauses 3, 4, 6, 7, 8 1-2 each, clause 9 and the page order 1-2. Clauses 1 and 5 are built.
- **Open rows:** count: 2; ids: FU-1012; FU-1013
- **Built now:**
  - Clause 1: coverage register (75 rows, 22 Law), its check (a row in journey or arithmetic must name a test in the suite), served by a route and guarded. The check proves the named test exists, not that it drives the subject. Its directory row says 'no directory is held' though a help list exists since W724 (docs/COVERAGE_REGISTER.json; scripts/coverage_register.py; agentic_core/api/registers.py:58 GET /api/v1/registers/coverage; test_registers_a_named_source_has_a_row_and_a_claimed_journey_names_its_test (test_mvp_spine.py:62250))
  - Clause 5: the generator refuses filing-shaped templates with 409 and names the clerk's route; guarded (agentic_core/api/law.py:299-312; agentic_core/legal/specialist.py:23 FILING_SHAPED; test_law_a_filing_shaped_document_has_one_door_and_no_prompt_claims_a_role_or_a_forecast (test_mvp_spine.py:60791))
  - Clause 6, partly: prompts claim no professional role and ask for no probability, forecast or confidence (guarded); named authorities in research/analyse output are NOT resolved against a held source - only the clerk resolves them (agentic_core/api/law.py:191-192, :253-266; agentic_core/legal/specialist.py:75 resolve_authority (used at :150 only))
  - Clause 3, partly: eight places to get help, names and links only, one read date for all, no nation per row and no staleness (agentic_core/api/law.py:391 HELP_FROM_A_PERSON; :411 GET /api/v1/law/help (P5.20, W724))
  - A register of sources with a 90-day staleness check (reusable for dated rules and places) (docs/SOURCES.json; scripts/sources_check.py; agentic_core/api/registers.py /sources)
  - FU-1013 half done: what the deployment can serve is said before each form (W737); the tools needing no model are not yet first (apps/workstation-superapp/src/components/DomainTool.tsx:276 ServingNow; apps/workstation-superapp/src/pages/domains/LawHub.tsx (three AI forms above MatterAssemblyPanel and StatutePanel))
  - Clause 9 not verified as held: the shared tool component saves the first 400 characters of what a person typed and the answer to browser storage on every Law form (server-side only when signed in) (apps/workstation-superapp/src/components/DomainTool.tsx:185 saveOutput; apps/workstation-superapp/src/lib/outputHistory.ts:31, :42)
  - Clauses 2, 4, 7 and 8: not built (no deadline rule, no urgent routes; the regulated subjects are 'excluded' rows with a ruling but no regulator page, date or route) (grep of agentic_core for deadline rules / urgent routes: none; docs/COVERAGE_REGISTER.json law-immigration, law-debt-solutions rows)
- **Remaining:**
  - captured by open rows: FU-1012: a deadline as arithmetic on a dated rule and a route as a directory row (the core of clauses 2 and 3); FU-1013: put the tools that need no model first on the Law page
  - not captured by any row: Clause 2's full matrix (each change of rule, month end, leap year, each nation, no rule) and the earlier-date sentence where a source does not settle a date; Clause 3: per-row nation, page, read date, 90-day not-recently-checked label driven by date; Clause 4: the fixed urgent-routes list shown first; a screen may add and never remove, driven with the screen returning nothing; Clause 6: no named authority shown unless it resolves against a held source (live on the Owner's local model); Clause 7: regulated subjects as rows with the regulator's page and date and a route to an authorised person; Clause 8: checklists as lists with sources; Clause 9: a decision on browser-side saving of typed input before sign-in
- **Waits on:**
  - items rulings switches: Ruled sequence: 5 and 6 with the tier-2 round (done in part); then 2; then 3, 4 and 1; then 7 and 8; Rules and places read at their publishers' pages (network access to legislation and government sites); Sign-in for clause 9
  - before sign in: Clauses 1-8: they store nothing about a person.
  - after sign in: Clause 9: a person's own matter (facts, documents, dates).
- **Only the Owner can:**
  - A qualified person's view before any public release is his to arrange (not needed to build).
- **First round:** Clause 2 (FU-1012): agentic_core/legal/deadlines.py holding the employment tribunal limits either side of 1 October 2026 and the Scottish exception as dated data (claim type, nation, in force from and to, source page, read on, read by), each source added to docs/SOURCES.json after reading it at the publisher; GET /api/v1/law/deadline does arithmetic on the matching rule, shows the rule, shows both rules near the change, and with no match says a limit may still apply and where to ask today. Guard drives the day before, of and after the change, a month end, 29 February, each nation and no rule; move law-tribunal-time-limit in docs/COVERAGE_REGISTER.json to 'arithmetic' naming the test.

## P5.12 — Education: a teacher or an adult learner is told what was read, what was checked and what this machine can do

- **Closes when:** ACCEPT: 'clause 1 is driven through an untouched caller in another domain; clause 2 is driven with a capture in the model's place at one character over the limit, at the limit, and blank; clause 3 is read in the saved and downloaded text and not only in the answer's fields; clause 4 refuses a made-up framework and a made-up type; clause 5 fails when the page's sentence is shown on a machine that does something else; clause 7's check fails on a row that claims a journey nothing drives; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 4–7 rounds. one open row (a doc round) plus five unrowed clause gaps (4, 3+6, 8, 5, the Education half of 1), each about one fix-with-test, clause 8 and 5 nearer 1.5; the cross-domain helper callers (FU-1059) and pages-from-registry (FU-1060) ride P5.10 and are not counted
- **Open rows:** count: 1; ids: FU-1055; basis: FU-1055 is a reading-and-table round
- **Built now:**
  - Clause 1 helper: a person's material is its own argument; the helper cuts it, records read-of-total, marks it as data and defuses imitated marks (agentic_core/api/_ai_provenance.py wrap_material (l.192-206), ai_text material= (l.209-239), provenance['material'] (l.292-293); integration_tests/test_mvp_spine.py test_w680_a_persons_material_travels_as_marked_data_through_two_untouched_looking_doors (l.62203))
  - Clause 2: blank work refused 422; work over 6,000 characters has Criterion-by-Criterion and Indicative Level / Grade withheld with the reason in the text, on a model as on the floor (agentic_core/api/education.py marking_feedback (l.234-315); test_education_work_not_read_whole_is_not_graded_and_every_answer_says_what_was_not_checked (l.60836) drives at the limit, one over, and blank)
  - Clause 3 (most): lesson and assessment texts say nothing was checked by a person, the answer key was checked by nobody, the religion screen did not clear the subject, and who the tool is for; curriculum text carries the for-whom and name-only framework sentences (education.py _LESSON_NOTE/_ASSESSMENT_NOTE (l.155-160), lesson text l.215, assessment text l.367, curriculum text l.132; screen_note reaches saved/copied/downloaded text through withDisclosures in apps/workstation-superapp/src/components/DomainTool.tsx l.97-114)
  - Clause 4 (part): framework list is names only with held='name only'; unknown framework and unknown assessment type refused 422; curriculum clamps said in 'adjusted' and in the text; 'UK National Curriculum' renamed National Curriculum (England) with page and read date (education.py FRAMEWORK_HELD l.34, _FRAMEWORKS l.36-50, refusals l.92-95 and l.333-336, clamps l.96-101 and l.132-133)
  - Clause 5 (generic part): a server-read sentence before every form says whether an owned model is serving or the floor will return a frame (apps/workstation-superapp/src/components/ServingNow.tsx; DomainTool.tsx l.276-277; test_w737_what_serves_is_said_before_a_form_is_filled (l.66649))
  - Clause 6 (answer side): when needs are typed the lesson text says they were sent exactly as typed and not to name a pupil (education.py _NEEDS_NOTE l.157-158, l.215; FU-1031 closed W677)
  - Clause 7: 22 Education coverage rows (4 frame, 14 nothing_built, 4 excluded with their rulings); the check fails a journey or arithmetic row naming no test that exists in the suite; served (docs/COVERAGE_REGISTER.json; scripts/coverage_register.py check(); agentic_core/api/registers.py GET /api/v1/registers/coverage)
  - Sources already read for the routes out and the children's step (docs/SOURCES.json rows gov-regulated-qualifications, gov-lle-when-to-apply, gov-national-curriculum, dfe-genai-product-safety (read 2026-10-12))
  - Religious teaching refused on all four routes; every prompt opens 'Claim no professional role' (agentic_core/religious_domain/subject_screen.py refuse_if_religious_teaching; prompt-as-sent leg 7 of the test at l.60836)
- **Remaining:**
  - work: The education department's thirteen product-safety headings set against the four tools, each met / partly / not met, read from the department's page; no code; row: FU-1055
  - work: Clause 4: 7 of 8 framework rows say region 'International' with no publisher page and no date read (only uk_national has both); several are not publications (STEM Framework, Competency-Based Education) and need a read row or retirement; the lesson-plan duration is clamped 20-180 with nothing said (education.py l.180); row: none (item clause 4)
  - work: Clause 3: the marking answer carries no 'subject not cleared by the religion screen' sentence (the route returns no screen_note); the curriculum's screen note reaches the text only via the page channel; row: none (item clause 3)
  - work: Clause 6 form side: the lesson form (EducationHub.tsx l.124-133) offers no needs field at all, so no form says 'do not name a pupil'; the API and the composition registration (agentic_core/api/resource_fabric.py l.588, l.598) still accept special_needs; row: none (item clause 6)
  - work: Clause 8: funding, qualifications, admissions and providers are 'nothing_built' rows ('no route is held yet'); build them as route_only rows / one list naming the official page with the date read and the 90-day rule, never a figure; row: none (item clause 8)
  - work: Clause 5: the per-form sentences on EducationHub.tsx (l.78, 93, 108, 124) are typed and still promise marking 'with an indicative level', a 'ready-to-use' assessment and a 'classroom-ready plan'; the clause's own check needs each sentence read from the form's registration so it fails on another machine; row: none here; the cross-domain class rides FU-1060 on P5.10
  - work: Clause 1, Education part: task, rubric, special_needs, prior_knowledge and learning_objectives are still joined into the instruction (education.py l.190-191, l.254-255, l.341) and those answers carry no read-of-total figure; ACCEPT's 'untouched caller in another domain' has not been driven (test_w680 drives Law and Education, both edited that round); row: none here; the other 18 callers ride FU-1059 on P5.10
  - work: Clause 9: a guard that nothing a person types is stored before authentication; the learner record itself waits for sign-in; row: none (item clause 9)
- **Waits on:**
  - waits for: P5.10 FU-1059 and FU-1060 for the cross-domain halves of clauses 1 and 5; P4.1 AUTH_ENABLED (the Owner's switch) for clause 9
  - before sign in: clauses 1-8 and FU-1055
  - after sign in: clause 9: a learner's own record (goals, work, progress)
  - rulings already given: children do not use the tools (standing rule 2026-10-13, W712)
- **Only the Owner can:**
  - none for the build; clause 9 waits on the Owner's sign-in switch
- **First round:** Finish clauses 3, 4 and 6 (the part the SEQUENCE put first): in agentic_core/api/education.py give each framework row nation + publisher page + read_on read at its publisher (enter the rows in docs/SOURCES.json) or retire it with the reason where no publisher exists; say the lesson-plan duration clamp in an 'adjusted' list and in the text; put SCREEN_NOT_CLEARED into the marking text; either add the needs field to the lesson form in EducationHub.tsx with 'do not name a pupil' beside it or stop the registration accepting it. Extend test_education_work_not_read_whole_is_not_graded_and_every_answer_says_what_was_not_checked: every framework row has page+read_on+nation or a stated no-publisher basis; duration 500 says 'was asked for' in the text; the marking text holds the screen note; blinds (drop a row's page, remove the clamp sentence, drop the note) each driven red.

## P5.13 — Care: the first line is the route to a person, every source is known to still stand, nothing a clinician alone may say is composed

- **Closes when:** ACCEPT: 'clause 1's check is driven on a row made replaced and on a name with no row; clause 2 is driven with every combination of factors and returns no count; clause 3 is driven on the floor, with a capture in the model's place and with a composer that returns nothing; clause 4 with a child, an adult and a made-up jurisdiction; clause 5 by reading the prompt as sent; clause 6 in the saved and downloaded text; the scorer's boundary cases become a kept test read once against the chart at its publisher; every clause has a guard driven RED.'
- **Delivered by:** build
- **Size:** 5–9 rounds. 2 open rows (about 1 each, the hazard log possibly 2) + the urgent-routes mechanism (1-2, ruled one shared round with the register) + the child route (1) + four small unrowed gaps (row pointers, draft wording, unread keys, page and front-door sentences, about 2-3 together) + the chart re-read (0.5)
- **Open rows:** count: 2; ids: FU-1033; FU-1056; basis: both are a round's reading and writing; FU-1033 may need a person to open the Waterlow owner's site in a browser if it keeps redirecting, and whether to seek a MUST licence is the Owner's question (ruled 2026-10-12: no letter, a route instead)
- **Built now:**
  - Clause 1: one register of sources (72 rows: 63 current, 8 named_not_read, 1 replaced) with page, date read, reader, status, replaced_by; the check fails a name with no row and a reader of a replaced row; rows past 90 days reported (fail only with --strict-stale); served with recently_checked (docs/SOURCES.json; scripts/sources_check.py check(); agentic_core/api/registers.py GET /api/v1/registers/sources; test_registers_a_named_source_has_a_row_and_a_claimed_journey_names_its_test (l.62250))
  - Clause 2: falls count retired - 410 naming NG249 and its page; every key sent named back, nothing counted (agentic_core/care/scoring.py FALLS_RETIRED l.344-350, score_falls l.357-365; agentic_core/api/care.py l.175-180; test_care_the_falls_count_is_retired_and_the_safeguarding_form_is_the_adult_route_for_england (l.61818))
  - Clause 3 (safeguarding only): typed 999 line is the first line of the text, whoever composed the rest (care.py IMMEDIATE_DANGER_FIRST l.64-66, prepended l.299; test_w676_the_emergency_line_is_the_first_line_of_the_safeguarding_text (l.60746))
  - Clause 4 (part): adult route for England stated first; any other jurisdiction refused 422 before composing; prompt asks for no contact details (care.py ADULT_ROUTE_ONLY l.70-71, refusal l.268-272, prompt l.274-275)
  - Clause 5: no clinician-only section asked for; one a composer returns is cut and named; the text says DRAFT ORGANISER ... reviewed by nobody (care.py CLINICIAN_ONLY_* l.75-81, l.105-133; test_care_a_plan_asks_for_nothing_only_a_clinician_may_write_and_the_oxygen_scale_is_said (l.61879))
  - Clause 6 (part): handover disclaimer says DRAFT, not reviewed, not sent; DomainTool appends disclaimer and the 'Review: Unreviewed' line to saved and downloaded text (care.py l.353-356; DomainTool.tsx withDisclosures l.106, l.114)
  - Clause 7: catalogue 'does' field (computes / frame / withheld / retired); unknown id refused 422 naming the tools (care.py _TOOLS l.30-55, l.163-169)
  - Clause 8 (part): the second oxygen scale is said to apply only where a clinician prescribed it; 47 boundary cases are a kept test (scoring.py l.121-124; test_care_the_early_warning_score_matches_its_chart_at_every_boundary (l.61766))
  - Clause 9 (two of three): MUST terms read at BAPEN and withheld 409; NEWS2 terms read at RCP, acknowledgement and unmodified carried; Waterlow withheld as unread (scoring.py WITHHELD_ON_TERMS l.374-385, withheld_sentence l.388-393; care.py l.34-45; test_w679_a_score_is_withheld_on_its_owners_terms_and_the_one_that_computes_is_acknowledged (l.62071))
  - Clause 10: 22 Care coverage rows (1 arithmetic, 6 frame, 8 nothing_built, 7 excluded) (docs/COVERAGE_REGISTER.json)
- **Remaining:**
  - work: Waterlow's reuse terms still unread (its owner's site answered with a redirect); per ruling 29.4 item 9 the MUST and Waterlow places become ROUTES to their owners' published tools once each page is read - MUST's page was read but the refusal gives no link; row: FU-1033
  - work: A hazard log for the Care tools: read the published example the ruling names, then one entry per hazard linked to its guard or marked unguarded, with a check that every named guard exists; row: FU-1056
  - work: Clause 3: one typed list of urgent routes (immediate danger, mental-health crisis, serious deterioration), each read at its source for England, shared with Law (P5.11 clause 4 - Law carries none yet), shown first on every care answer where danger may be present (risk-assess/NEWS2, a mental_health plan, safeguarding, handover); driven on the floor, with a capture and with an empty composer. Only safeguarding has a typed line; coverage row care-urgent-routes is nothing_built; row: none on this item; named inside FU-1060 on P5.10
  - work: Clause 4: nothing on the form or the API says the concern is about a child, so a child's concern is always composed as adult guidance under the adult-only line; needs an adult/child field, the children's route returned with nothing composed, and the child leg the ACCEPT names; coverage row care-children-safeguarding still says 'the adult form still accepts it until the tier-2 round' though W677 has passed; row: none (item clause 4)
  - work: Clause 1: entries point at a row only by name-pattern match (4 patterns, 5 folders); catalogue 'standard' text is not tied to row ids; NICE NG97 and the Care Act 2014 are named_not_read yet the catalogue names NG97 as a standard with no 'not read' (care.py l.48 against its own comment l.31-33); no page shows recently_checked; row: none here; widening the check is in FU-1060 on P5.10
  - work: Clause 6: risk-assess and safeguarding texts do not say 'a draft no professional has reviewed' ('decision aid', 'process guidance'); only the Review line says it in saved text - confirm in a downloaded file; row: none (item clause 6)
  - work: Clause 8: NEWS2 does not name the keys it did not read (only the retired and withheld entries return keys_not_read); row: none (item clause 8)
  - work: ACCEPT: the 47 boundary cases have not been read once against the chart at its publisher (the test docstring at l.61767 still says 'TO BE READ ONCE'); row: none
  - work: Boundary: front-door and page sentences claim what the code does not - toolRegistry.ts l.52 'Score a validated tool ... (NEWS2 · MUST · Waterlow)' and CareHub.tsx l.75 name two withheld scores as computed and use 'validated'; 'Safeguarding Triage' / 'Triage concern' (toolRegistry.ts l.53, CareHub.tsx l.126) against 'triages nobody'; 'person-centred care plan' (toolRegistry.ts l.51, CareHub.tsx l.60) while the API says 'not a care plan'; care.py l.238-239 disclaimer still names MUST and Waterlow; row: none
  - work: Clause 11: a guard that no care record is stored before sign-in; row: none (item clause 11)
- **Waits on:**
  - waits for: P5.10 FU-1060 (the typed urgent-routes list and the widened sources check are filed there); P5.11 clause 4 (Law's urgent list - 'the list is the one Law already carries', but it does not exist yet); P4.1 AUTH_ENABLED for clause 11
  - before sign in: clauses 1-10, FU-1033, FU-1056
  - after sign in: clause 11: a person's care record
- **Only the Owner can:**
  - a qualified clinical reviewer before any care tool is offered to the public (the Owner's to arrange; amended 2026-10-12 so a free tool may release on a calibrated agent's review, except a clinical score used in someone's direct care, which keeps a person); the MUST licence question stays the Owner's
- **First round:** Clause 4 plus the page sentences: in agentic_core/api/care.py add a required concern_about ('an adult' | 'a child or young person') to SafeguardingRequest; for a child return the children's route (the gov.uk report-child-abuse sentence with its read date, and 999) and call no composer; add the field to the safeguarding form in CareHub.tsx; correct CareHub.tsx l.60/75/126 and toolRegistry.ts l.51-53 (no MUST or Waterlow named as computed, no 'validated', no 'triage', no 'person-centred'); rewrite coverage row care-children-safeguarding. Extend test_care_the_falls_count_is_retired_and_the_safeguarding_form_is_the_adult_route_for_england with a child leg (no prompt captured, children's route first, 999 present), an adult leg and the made-up jurisdiction, plus a page leg failing on 'validated', 'Triage' or a withheld score named as computed; blinds red.

## P5.14 — Working with a person

- **Closes when:** ACCEPT: 'each of clauses 1 to 6 has a guard that drives the state and a blind driven red; clause 1 is shown on the method page; clause 4's list is reached from the first screen; the notes hold no lesson citing a round later than the method's data, or each such lesson has a stated reason.'
- **Delivered by:** build
- **Size:** 4–7 rounds. one open row (state + list, 1-2) + clause 6 question shape across every site (1-2) + clause 1 finish step and deriving the W678-W785 lessons (1-2, each batch ratified by the Owner) + design doc and guard (about 1)
- **Open rows:** count: 1; ids: FU-1043; basis: FU-1043 is a build; but see depends_on for whether its list is post-sign-in
- **Built now:**
  - Clause 1 measure: GET /api/v1/method/learning carries 'currency' (latest round a lesson cites vs latest round the history declares; UNMET when behind; NOT ASSESSABLE when history unreadable), printed on the method page (agentic_core/api/method.py _method_currency l.1155-1178, l.1196; apps/workstation-superapp/src/pages/governance/DeliveryMethod.tsx l.302-303; test_w678_the_method_says_how_far_it_trails_the_work (l.61985))
  - Clause 1 door: one change record per batch of lessons; 15 lessons entered by the ruling of 2026-10-13; method changes held for a person (method.py POST /amendment l.305; test_w696_a_batch_of_lessons_is_one_change_record_and_a_faulty_batch_files_none (l.63971); FU-1041 closed W696; W715)
  - Clause 2: an 'exchange' group of 8 lessons (M-EXCH-01..08) covering the five measured defects, each with its defect text; none has an enforcer (docs/DELIVERY_METHOD.json (117 lessons, group 'exchange'))
  - Clause 3: a project keeps first_description and its time, written once at creation, shown when it differs (agentic_core/projects/api.py l.151-155, l.392-393; apps/workstation-superapp/src/pages/projects/ProjectsHub.tsx l.381; FU-1042 closed W678)
  - Clause 5: an edit naming a field the record does not hold is refused with its name (projects/api.py UpdateProjectRequest model_config extra='forbid' l.170-175)
- **Remaining:**
  - work: Clause 4: a project cannot say it waits on the person (status Literal idle|running|done|error, projects/api.py l.147); the waiting state with reason and what is needed, and ONE list reached from the first screen of everything that waits on the person, read from the stores that exist (projects, submitted change records, the scholar queue, review records) - nothing of it exists; row: FU-1043 (its unknown-field half is already done)
  - work: Clause 1: the method trails again - its latest lesson cites W677 while the history declares W785 (108 round ids); no round finish step records 'a lesson was derived' or 'nothing new was learned' (nothing in scripts/ or method.py); the lessons held in the assistant's notes since W677 are not derived (the notes are on the Owner's machine and were not read here); row: none (item clause 1)
  - work: Clause 6: no question the platform puts to a person states what differs, the cost to undo, the recommendation, or confirmation vs decision; irreversible acts run on a bare window.confirm (ProjectsHub.tsx l.359 delete project, LivingMarketplace.tsx l.492, CreatorStudio.tsx l.334); row: none (item clause 6)
  - work: Clause 7: the design (no code) for the method's disciplines offered to a person's own project; row: none (item clause 7)
  - work: Clause 8: a guard that nothing in the product records how a person works; clause 2's guard over the exchange group not verified; row: none
- **Waits on:**
  - waits for: the Owner's ratification of each lesson batch (W715: a change to the method is held for a person)
  - before sign in: clauses 1, 2, 3, 5, 6, 7 (design), 8 - the Phase-5 split names 'the method's lessons' as pre-sign-in
  - after sign in: the Phase-5 split lists 'a waiting list' among things built after sign-in, which reads as clause 4's list (the item's own ruling put clauses 3, 4, 6 in one round) - to be confirmed; anything clause 7 would keep about a person
- **Only the Owner can:**
  - ratify each derived batch of lessons; the assistant's notes the ACCEPT checks are on the Owner's machine; a word on whether clause 4's list is the 'waiting list' the phase split defers
- **First round:** Clause 6 (pre-sign-in, unbuilt): one shared question component carrying what differs, cost to undo, which is recommended, and confirmation-or-decision; route the three window.confirm sites through it; deleting a project needs its title typed back, and DELETE /api/v1/projects/{id} refuses without the matching title server-side. Guard: a census over apps/workstation-superapp/src failing on any window.confirm/confirm( not using the component, plus a drive of DELETE with and without the title; blinds (plant a bare confirm; drop the server check) red.

## P5.15 — The review cell

- **Closes when:** ACCEPT: 'each of clauses 1 to 6 has a guard that drives the state and a blind driven red; one discipline (Care) has every tool at a stated tier on its page; the calibration set and its results are in the tree'. Release on the second tier is the Owner's switch and keeps a person for four exceptions.
- **Delivered by:** build
- **Size:** 6–10 rounds. ACCEPT scope: FU-1054 is three builds in one row (cases written, agent built, run recorded) at about 3-5 rounds; four unrowed clause gaps at about 3-4; clause 7's three later disciplines would add roughly 2-3 rounds each and are not in ACCEPT
- **Open rows:** count: 1; ids: FU-1054; need owner or owner machine: FU-1054; basis: a calibration run counts only in the 'model' configuration (calibration_of) and the only model is the local one on the Owner's machine; external models are barred from care content (ruling 29.4 item 10) and are off (P4.3)
- **Built now:**
  - Clause 1: every domain tool's answer states the highest tier its records support, 'Unreviewed' with none; an unreadable store is NOT KNOWN, never reviewed; carried into saved text (agentic_core/api/_review_tier.py review_statement l.108-153; agentic_core/api/_ai_provenance.py l.294-303; DomainTool.tsx l.106, l.388-394; test_w688 (l.63163, l.63225))
  - Clauses 2 and 5: one admin door records a rule check, an agent review or a signature and refuses a record short of its tier's rule; signature needs name, credential as stated, what was reviewed, an unexpired lapse date; every answer says the credential is not verified (agentic_core/api/review_cell.py POST /api/v1/review/record l.66-95; _review_tier.py counts() l.68-105; test_w689 (l.63271))
  - Review tab listing every record, whether it counts and why not (apps/workstation-superapp/src/pages/governance/ReviewRecords.tsx; test_w690 (l.63357))
  - Clause 3 arithmetic: an agent is calibrated only by its latest recorded run with a model serving on the current set; bar = every planted case for its reason and at most one false alarm in six clean; rates computed by the server (agentic_core/api/_review_calibration.py l.25-79, calibration_of l.100-118; review_cell.py POST /api/v1/review/calibration/run l.108; test_w691 (l.63402))
  - Care calibration set described (16 cases: 10 planted, 6 clean), version '1-described', runnable false (docs/CARE_REVIEW_CALIBRATION.json)
- **Remaining:**
  - work: Write the 16 cases out in full from the tree's own history and re-read their sources on the day (clean case K06 relies on NICE NG97, which docs/SOURCES.json marks named_not_read; C03/K02 rely on the NEWS2 chart, not yet read at its publisher), make the set runnable; build the Care reviewer agent with its own checklist over the sources, never the composing prompt (clause 4); run it with a model serving and commit the run and its rates; row: FU-1054
  - work: Clause 2: the record has no tool-version field, sources are free strings (no page and date, no row id), and 'what it could not check' is optional (review_cell.py l.37-58); row: none (item clause 2)
  - work: Clause 6: an entity's own short roster of specialists feeding its third tier - not built; row: none (item clause 6)
  - work: RELEASE/ACCEPT: 'both options shown wherever a tool is offered' (the tier, and a qualified person with when one is warranted; a chargeable option for a generated entity) - nothing found; the tier appears only under an answer (DomainTool.tsx l.388-394), not where a Care tool is offered; row: none
  - work: Clause 8: a miss found later recorded against the reviewing agent, entering the method by its door, a repeated miss becoming a check; row: none (item clause 8)
  - work: Clause 7, beyond ACCEPT: Law, Education and money-readiness disciplines (sets, agents, calibrations) after Care; row: none
- **Waits on:**
  - waits for: the register of sources (built W681 - the item's foundation); the Owner's machine with the local model for the calibration run; release: the Owner's switch (not needed for ACCEPT)
  - before sign in: tiers, records, calibration, both-options sentence (the phase split names 'each tool's review tier' as pre-sign-in)
  - after sign in: not ruled explicitly; clause 6's roster keeps people's names and may fall under 'anything that keeps something about a person'
- **Only the Owner can:**
  - run the calibration on his machine with the model on; release is his switch; qualified persons for the third tier are his to engage (not needed for ACCEPT); the four exceptions keep a person
- **First round:** FU-1054 part 1: rewrite docs/CARE_REVIEW_CALIBRATION.json as version 2 with every case written out from the defects the tree actually had (the CG161 falls entry, 999-not-first safeguarding text, respiratory rate 21 scored 1, the 'registered nurse' prompt, a medication section, a 9-year-old under the adult route, MUST 'computes', a handover 'verified against clinical guidance', 'NHS Standard', the unsaid second oxygen scale) and the clean cases as the current tree answers; read NG97 and the NEWS2 chart at their publishers and update their SOURCES rows; flip runnable only when every case has text and every clean case cites current rows. Guard: the calibration route refuses a run on a set with a case lacking text or a clean case citing a named_not_read row; blinds red. The agent and the run follow.

## P5.16 — What is charged (virtual WST throughout)

- **Closes when:** ACCEPT: 'clauses 1, 3, 4 and 5 each have a guard that drives the state and a blind driven red; the cycle's answer and the entity's page show profit, fee and the base the split used; the stages and the fee sum to the profit to the cent.'
- **Delivered by:** build
- **Size:** 3–5 rounds. FU-1057 is the main build (metabolism, ledger line, page, to-the-cent guards) at about 2-3; clause 5's guard once acceptance exists about 1; clause 6 about 0.5-1
- **Open rows:** count: 1; ids: FU-1057; basis: the build needs no Owner (his three questions were answered 2026-10-12, 29.4 item 7); it is sequenced after the first walk, which runs on the Owner's machine with the model on
- **Built now:**
  - Clause 1: the Quran platform is free for individuals and institutions; an institutional price above zero is refused naming the ruling and the retired rule; canon amended as a dated ruling with the earlier words kept (agentic_core/economy/qep_pricing.py INSTITUTIONAL_PRICE l.31, check_institutional_price l.59-81; W679 guard over both vision documents)
  - Clause 2: the 99-pound price once, credited against the first profit share, waived for charitable/non-distributing, stated with the three conditions and 'nothing charged'; posts nothing, only reads the real-money switch (agentic_core/economy/generation_price.py statement(), conditions_met(); agentic_core/api/genesis.py; FU-1058 closed W687)
  - The profit base the fee needs: distributable = revenue - declared costs - prudential reserve, floored at zero (no fee line) (agentic_core/economy/metabolism.py run_cycle l.266-283)
  - A structure pass earns nothing; the old earning path kept behind one constant (agentic_core/api/swarm.py l.1171-1182 (DELIVERY_EARNS_ON_GATE_PASS))
- **Remaining:**
  - work: Clauses 3, 4: the 25% fee taken first in run_cycle as one ledger line the owner sees; the split applied to what remains; no profit no fee; apex and non-distributing exempt; an unregistered simulation's fee shown and never posted; no loss carried; starts with the first profitable cycle (ruling 29.4 item 7); the 99 pounds credited against the first fee; cycle answer and entity page show profit, fee and split base; stages + fee = profit to the cent. The design the row names is on the Owner's machine, not in the tree; row: FU-1057
  - work: Clause 5: a delivery earns only an accepted contract's amount - needs the acceptance act; the constant path (SIM_DELIVERY_TARIFF_WST behind DELIVERY_EARNS_ON_GATE_PASS) still exists, so a guard must hold that a constant never earns; row: none here; acceptance rides FU-1003 (P5.3) and FU-1049 (P5.9)
  - work: Clause 6: an entity's cost of its own specialists entered as a declared cost; row: none (item clause 6; rests on P5.15 clause 6)
  - work: Trivial: qep_pricing.py docstrings still state 'cost + 5%' (l.7, l.60) above code that refuses any price over zero; row: none
- **Waits on:**
  - waits for: the first walk showing a real entity's books (SEQUENCE; 28.6 ruling 1; the single-tenant journey of P5.1, on the Owner's machine with the model on) for clause 3; an acceptance act (FU-1003 on P5.3, FU-1049 on P5.9) for clause 5; P5.15 clause 6 for clause 6; charging the price: a named reviewer's pass, a solicitor's view and P4.6 - out of scope
  - before sign in: clauses 1-4 and 6
  - after sign in: clause 5 - the phase split lists 'an acceptance' among things built after sign-in
- **Only the Owner can:**
  - the first walk on his machine; before real money (not in scope): a scholar's view on the fee's form, a solicitor's on the regulatory line and on consumer status, an accountant's on the books; the real-money switch stays his and off
- **First round:** Blocked by the ruled SEQUENCE until the first walk has run (or the Owner releases it for a scratch entity). Then: in agentic_core/economy/metabolism.py run_cycle compute platform_fee = 25% of distributable_profit when above zero and the form distributes (zero for the apex and non-distributing forms; computed and not posted for an unregistered simulation), post it as one ledger line, apply the split to the remainder, return profit, fee and split_base, credit the 99 pounds against the first fee. Guard: over a grid of revenues, costs and reserves, sum(splits) + fee == profit to the cent; zero profit leaves no fee line; apex and non-distributing pay none; a simulation posts nothing; blinds red.

## P5.17 — The Quran platform's four areas, each to a driven slice before the next

- **Closes when:** ACCEPT: 'each clause that is built has a row in the coverage register naming the test that drives its journey, a guard and a blind driven red; no answer anywhere carries a score, a rank, a count of mistakes or a synthesised reading of the Arabic; every audio or data source in use has a register row whose terms permit the use.' Fixed boundaries (not work): recitation is never scored, nothing appears to correct a live recitation, the Arabic is fetched never generated, no learner is ranked, a model-written explanation waits for a named scholar.
- **Delivered by:** build
- **Size:** 11–18 rounds. three open rows about 3-5 (one Owner-gated); pre-sign-in clause gaps (hear-yourself and pause-tap, scheduler and layout, accessibility, coverage rows) about 3-4; teaching about 3-5 and competitions about 2-4 after sign-in; competition detail is unsized until a real marking scheme is read
- **Open rows:** count: 3; ids: FU-1064; FU-1066; FU-1067; need owner or owner machine: FU-1067; FU-1066; basis: FU-1067 needs recordings the Owner supplies or approves, speech models downloaded (his 2026-11-06 ruling 'download no model candidate for now' stands against it unless he says otherwise) and his ruling on the numbers; FU-1066's letters are drafted by a round and SENT by the Owner
- **Built now:**
  - Clause 1 (most): portion plan in three tracks by ayah range, page (1-604, the fifteen-line Madinah page) or juz with no default portions; hidden-verse practice sending only what is shown; next word by position; similar verses computed by exact shared wording (agentic_core/religious_domain/memorization/practice.py; routes /api/v1/qep/hifz/practice, /next, /similar, /portion, /portions in agentic_core/religious_domain/api.py l.984-1105; apps/workstation-superapp/src/components/HifzPractice.tsx; coverage rows qep-portion-plan, qep-hidden-verse, qep-similar-verses = journey (test_w684_* l.62606-62721))
  - Clause 2 (listen slice): a named reciter's audio fetched per request from the Quran Foundation, never stored, credentials server-side; the words light as one verse plays (agentic_core/religious_domain/quran_foundation.py; api.py /recitation/source, /reciters, /audio l.637-680; QEPStudio.tsx startListening l.133-170; test_w704 (l.64697), test_w717 (l.65384))
  - Own progress, never a rank; points only after a recorded review; every answer carrying a learner id says it is unverified (W685 (test_w685 l.62749-62814); api.py _identity l.166-176 (test_w686 l.62830))
  - Nine Quran source rows (text licence, foundation developer terms, alquran.cloud, the leading app's recordings page, QUL data, everyayah, cpfair, ICO voice; KFGQPC named_not_read) (docs/SOURCES.json)
  - Developer account at the foundation opened by the Owner (W704 commit message)
- **Remaining:**
  - work: Rows for the method and competition sources (no primary hifz-method text or marking scheme opened; KFGQPC never reachable); a check that every source in use has terms permitting the use (sources_check.py has no terms field or check); the two permission letters (QUL data, KFGQPC audio and fonts) drafted - no draft found in the tree; row: FU-1066
  - work: Clause 3: the private place-finding test of clean-licence on-device models on lawful recordings of ordinary reciters; numbers and limits into the assessment; then the Owner rules; row: FU-1067
  - work: The learner id is typed (QEPStudio.tsx l.29 UID = 'local'); with authentication on the id must be the caller's own and another's not found; then export and delete; row: FU-1064
  - work: Clause 2 remainder: hear-yourself (record on the device, replay beside the reciter, keep or delete, nothing leaves the device) and the pause noticed by sound level with a tap for the next word - nothing records today; coverage row qep-listen-follow still says 'nothing here plays a recitation' though W704/W717 built it (stale), qep-hear-yourself nothing_built; row: none (item clause 2)
  - work: Clause 1 remainder: the card scheduler is not limited to isolated trouble spots (/hifz/schedule makes a card for every ayah in a range, api.py l.751-799); the page layout by line not built; default portions wait on a read method source; row: none (item clause 1)
  - work: Clause 6: audio-first operation - Arabic is rendered as plain lang='ar' text a screen reader would voice (HifzPractice.tsx l.130, l.166); no per-word labels or large-type mode found; row: none (item clause 6)
  - work: Clause 4 (after sign-in): circle with enrolment code, assigned portions, a recording shared by choice and kept on the Owner's machine in the invited stage, a teacher's note pinned to the word, facts-only teacher view, a teacher's attestation with scholar-reviewed wording; row: none (item clause 4)
  - work: Clause 5 (after teaching): circle's shared total, personal challenge, judged event with organiser criteria and named human judges; detail waits on a real marking scheme; row: none (item clause 5)
  - work: ACCEPT question: /api/v1/qep/tajweed/analyse returns text_similarity figures for typed recall and /gamification returns points, while the ACCEPT says no answer carries a score - needs a ruling or a rewording; row: none
- **Waits on:**
  - waits for: a named scholar or trusted institute (2026-10-12: before recitation or teaching is built; clauses 2-5 each wait in part - W717's listen-only slice was built on the Owner's word of 2026-10-13); the Owner seeing the private test before clause 3 is ruled; P4.1 sign-in and the invited stage (P4.2, teachers the Owner names) for clause 4; clause 4 before clause 5
  - before sign in: clauses 1, 2, 3, 6, FU-1066, and FU-1064 (built and driven with authentication on in a test process)
  - after sign in: clause 4 teaching, then clause 5 competitions
- **Only the Owner can:**
  - a named scholar or trusted institute; recordings for the private test and leave to use on-device speech models; sending the two permission letters; naming teachers; a safeguarding lead before children; a real competition marking scheme
- **First round:** FU-1066 plus the stale coverage row: in docs/SOURCES.json give each Quran source row a 'permits' field (what use its terms allow) and enter the method and marking-scheme sources (or rows saying never opened); extend scripts/sources_check.py so each source a route uses (the Tanzil text, the foundation's audio and timings) must have a row whose terms permit that use, failing otherwise; draft the two letters for the Owner to send; set docs/COVERAGE_REGISTER.json qep-listen-follow to journey driven by test_w717_a_reference_recitation_is_listened_to_and_nothing_listens_to_the_learner. Guard and blinds: a use with no permitting row goes red; qep-listen-follow back at nothing_built while a recitation route exists goes red.

## P5.18 — The enterprise's own agreements, as records that say only what is true of them

- **Closes when:** ACCEPT: 'each built clause has a row in the coverage register naming the test that drives its journey, a guard and a blind driven red; no answer shows an entity as a legal person, a virtual contract as an agreement, a provider's status as an execution, or a date with no source; the reserved documents are refused through the route a person would use.'
- **Delivered by:** build
- **Size:** 7–11 rounds. FU-1075 is two clauses with a state model and version hashes (2-3); FU-1077 is reading (1-2); six unrowed clauses (3-8) about 4-6
- **Open rows:** count: 2; ids: FU-1075; FU-1077; basis: FU-1077 is reading; FU-1075 waits on sign-in by SEQUENCE, not on the Owner's machine
- **Built now:**
  - Clause 4 (part): filing-shaped documents refused 409 and routed to the clerk; every deed held until a qualified person has read Schedule 2; no land-instrument template exists (agentic_core/legal/specialist.py FILING_SHAPED l.23, HELD_FOR_A_QUALIFIED_READ and held_for_a_qualified_read l.28-39; agentic_core/api/law.py _TEMPLATES l.38-48; test_w714_a_deed_is_held_until_a_qualified_person_has_read_the_schedule (l.65292))
  - Clause 7 reusable: a person's document travels as marked data with read-of-total stated (law.py analyse material= l.213; _ai_provenance.py wrap_material)
  - Clause 8 (part): source rows entered 2026-10-13 through a summarising fetch, each saying what was not read (hmlr-practice-guide-8, lpmpa-1989-s1, lsa-2007-sch2, hse-puwer-overview, frc-frs-102-periodic-review-2024, lawcom-business-tenancies-renewal, gov-ending-commercial-lease-early, ico-duaa-2025) (docs/SOURCES.json; test_w711_the_two_chartered_items_keep_their_boundaries_and_every_source_says_what_was_not_read (l.65129); assessment section 31)
  - The only contract object: a virtual service contract between two platform entities (agentic_core/api/economy.py)
- **Remaining:**
  - work: Clauses 1+2 as one driven slice on made-up parties: a party as a real person or registered body with where and when read, signatory authority as stated and unverified; an agreement record whose drafted/reviewed/approved/executed/in-force/ended states are separate facts with who and when, an approval bound to one version's hash, executed as a person's evidence entry; internal virtual contracts listed apart; row: FU-1075
  - work: Read at their publishers the Companies Act 2006 execution rule, the unfair-terms and consumer-rights legislation, the lifting-equipment regulations and the consumer-credit / regulated-hire regime; re-read the 14 rows entered through a summarising fetch; row: FU-1077
  - work: Clause 3: obligations and dates read from the text (clause + confirmer; dated rule from a read source; never a model; unknown notice period said; due items on the one waiting list - P5.14 clause 4); row: none (item clause 3)
  - work: Clause 4 remainder: land instruments, land-registration instruments, land contracts beyond a short lease and deeds for registration refused and routed through the route a person would use (today they are absent only because no template exists); row: none (item clause 4)
  - work: Clauses 5 and 6: premises records against their clauses; equipment arrangements (owns, possesses, maintains, insures, returns) with the accounting treatment handed to the finance item; row: none (item clauses 5-6)
  - work: Clauses 7 and 8: an uploaded agreement as data that stays on the machine; every statement of law naming a row and its date, what was not read listed; coverage rows for each built clause; row: none (item clauses 7-8)
- **Waits on:**
  - waits for: the standing tier-1 findings fixed: met in substance - every P2.40 row is closed at HEAD (0 open of 25), though the item P2.40 stays open and closes only on an audit; P4.1 sign-in (SEQUENCE: 'after the standing tier-1 findings are fixed and after sign-in'); P5.14 clause 4's list for due dates
  - before sign in: FU-1077 reading and source rows only
  - after sign in: every code clause, starting with clauses 1+2 on made-up parties; a person's own agreements
- **Only the Owner can:**
  - a qualified person's view before any public release (the Owner arranges); the solicitor's read of Schedule 2 for the held partnership deed is still not made; no e-signature provider, real payment or notice to anyone
- **First round:** FU-1077 (the part sign-in does not gate): read each named authority at legislation.gov.uk and the regulators' own pages, re-read the 14 rows of 2026-10-13, and record each in docs/SOURCES.json as a direct read with what was not read; extend test_w711 so no P5.18 source row may still rest on a summarising fetch without a re-read date; blinds red. FU-1075's slice waits for sign-in.

## P5.19 — Physical assets as records and evidence - nothing connected, nothing controlled

- **Closes when:** ACCEPT: 'each built clause has a row in the coverage register naming the test that drives its journey, a guard and a blind driven red; no answer merges the six facts or shows a lease as permission to operate; no route of this item opens a connection to anything outside the process.'
- **Delivered by:** build
- **Size:** 4–6 rounds. FU-1078 about 2; FU-1079 reading 0.5-1; three small unrowed clauses about 2-3
- **Open rows:** count: 2; ids: FU-1078; FU-1079; basis: FU-1079 may need a person to open the ISO and EUR-Lex pages that refused the reader
- **Built now:**
  - Nothing of the item; the boundary state holds: no device connected, telemetry labelled simulated, a twin is a text specification, and no robot/vehicle/drone/premises/insurance word in agentic_core (agentic_core/api/integration_surface.py /api/v290/iot/devices l.627-642, telemetry l.645-690; agentic_core/api/digital_twin.py; grep of agentic_core)
  - Clause 3 source rows read 2026-10-13 (through a summarising fetch) (docs/SOURCES.json hse-puwer-overview, si-2026-439-av-passenger-permits, av-act-implementation-programme, caa-drone-requirements, si-2026-867-machinery, pram-act-2025, ec-ai-omnibus-2026; test_w711 (l.65129))
- **Remaining:**
  - work: Clauses 1+2 slice on a made-up asset: an asset record tied to an agreement record; the six facts kept apart, each as attached evidence with who, when and lapse; no score; row: FU-1078
  - work: The EU machinery regulation's application date and four ISO robot-safety editions not readable at the publishers; no primary source permitting a robot on a footway; entered as not read, never stated as fact; row: FU-1079
  - work: Clause 3: the regime as a set of rows per context (workplace robot, road vehicle, footway robot, drone), each with what was read, the date and what was not; 'no source permitting this use was found' in those words; row: none (item clause 3)
  - work: Clause 4: a guard that no route of the item opens a connection, simulated rows stay labelled, a twin or simulation is never offered as safety evidence; row: none (item clause 4)
  - work: Clause 5: evidence past its date reads lapsed and a readiness declaration resting on it reads withdrawn until renewed; coverage rows; row: none (item clause 5)
- **Waits on:**
  - waits for: P5.18's first slice (FU-1075), on which clause 1 rests - so transitively P2.40 and P4.1 sign-in
  - before sign in: FU-1079 and the clause 3 source rows (documents only)
  - after sign in: the asset record and every code clause (through P5.18's sequence)
- **Only the Owner can:**
  - none for the build; whether the platform ever connects to a device stays a separate Owner ruling, not scheduled and not needed
- **First round:** FU-1079 with the clause 3 rows (unblocked documents): retry the machinery regulation's application date at EUR-Lex and the ISO editions at iso.org; enter each as read or named_not_read with what was not read; assemble the four contexts' rows in docs/SOURCES.json; extend test_w711 so each context has its row set and the 'no source permitting this use was found' sentence where none was; blinds red. The asset record waits for P5.18's slice.

## P5.20 — Quote, do not compose - and what is composed is checked by the platform's own AI, which may refuse and never approves

- **Closes when:** ACCEPT: 'each built clause has a row in the coverage register naming the test that drives its journey, a guard and a blind driven red; no answer presents an automated check as a person's review; a quoted passage that differs from its publisher's text by one character is refused; no work is shown whose terms are not a row; no judgment index exists without the licence row.'
- **Delivered by:** build
- **Size:** 6–10 rounds. two open rows about 3-4 (FU-1082 carries clauses 5 and 7); unrowed clauses 1-remainder, 4, 6-remainder and 8 about 3-6
- **Open rows:** count: 2; ids: FU-1081; FU-1082; need owner or owner machine: FU-1081; basis: if the foundation's terms page is silent on commentary, the foundation has to answer, and the Owner holds the developer account
- **Built now:**
  - Clauses 1 and 3 for statute: one provision fetched from legislation.gov.uk on request, shown as structured with publisher, address, version date, extent, unapplied changes and licence; text shown = text hashed; one differing character refuses; no model; nothing stored (agentic_core/legal/statute.py provision/fidelity/shown_text; agentic_core/api/law.py GET /api/v1/law/statute/{kind}/{year}/{number}/section/{section} l.373-387; apps/workstation-superapp/src/components/StatutePanel.tsx; test_w724 (l.65642); coverage row law-read-a-provision = journey; FU-1080 closed)
  - Clause 6 (legal half): one list of regulated and free legal help (names, links, one line of our own, each a source row), what the platform is not, how to complain to the Owner (law.py HELP_FROM_A_PERSON l.391-408, GET /api/v1/law/help l.411-425)
  - Clause 5 (refusal half, religious only): a request for a religious ruling is refused at the floor every AI door passes (W734; agentic_core/religious_domain/composed_text.py refuse_faith_ruling; test_w734 (l.66425))
  - Source rows for the item (docs/SOURCES.json legislation-gov-uk-reuse, tna-find-case-law-permission, lsb-ai-consumer-expectations-2026, dar-al-ifta-egypt-ai-fatwa-2025, quran-foundation-tafsir-terms (named_not_read), citizens-advice-terms (named_not_read), help-* rows)
- **Remaining:**
  - work: Commentary terms not read for any work; then clause 2: a commentary shown word for word beside the translation with author, work and source, only for a work whose terms are a row, under the fidelity check; row: FU-1081
  - work: Clause 5: recognise a request for a ruling on one's own case (religious, or advice on a live dispute), route it to people and show the published material verbatim; the screen may route, never clear. With it clause 7: the regulator's five expectations as rows with the test or NOT MET; row: FU-1082
  - work: Clause 1 remainder: official guidance fetched verbatim; one judgment fetched on request and quoted with nothing stored; a guard that no judgment index exists without the licence row; row: none (item clause 1)
  - work: Clause 4: a citation check on composed Law answers - an authority resolves to a row and fetched text, or is removed and the answer says so; row: none (item clause 4)
  - work: Clause 6 remainder: the one help page has no 'how to find a qualified scholar' and lives only on the Law route; row: none (item clause 6)
  - work: Clause 8: screening before a scholar reads (attach sources, flag, order the queue; never approve, release or change the text); row: none (item clause 8)
- **Waits on:**
  - waits for: FU-1081's terms (and the foundation's answer) for clause 2; a named scholar for clause 8 (SEQUENCE); clauses 3 and 4 travel with the clause each checks
  - before sign in: all of it - nothing here keeps anything about a person
  - after sign in: nothing
- **Only the Owner can:**
  - ask the foundation about commentary terms if its page is silent; name a scholar (clause 8); the National Archives licence only if a judgment index is ever wanted (not needed)
- **First round:** Clause 1 remainder with clause 6: add agentic_core/legal/caselaw.py and GET /api/v1/law/judgment/... fetching ONE judgment on request from the National Archives' Find Case Law, shown word for word with publisher, address, date fetched and licence, reusing statute.py's fidelity(); nothing stored, no index; put 'how to find a qualified scholar' beside the legal help on the one help page. Tests read a hand-made sample and never call the site: one differing character refuses; a guard that no store of judgments exists without the licence row; coverage row for the journey; blinds red.

## P5.21 — The children's Education and Quran tools, built and held, with one approval pack

- **Closes when:** ACCEPT: 'the pack assembles from the tree and the store; a decision on a changed pack is refused; the gate holds with sign-in off or the pack unapproved and opens only with both; every children's tool route is described in the pack; each clause driven red.'
- **Delivered by:** build
- **Size:** 8–12 rounds. the ruling fixes one tool a round for seven tools (7) plus the census guard (about 1); the tools needing a recording, a circle or a teacher's feedback rest on P5.17 and may cost more
- **Open rows:** count: 0; basis: no register row rides this item; its work is its own clause 4
- **Built now:**
  - Clauses 1-3: the pack (seven fixed rules, the tools section, every learner-facing text in the review store except adult research items) as a page and one Markdown document; one decision by a roster scholar bound to the pack's fingerprint, refused on a stale hash; any change re-opens review; the gate open only with sign-in on AND the current pack approved (agentic_core/religious_domain/approval_pack.py RULES l.32-46, pack_hash, decide, children_tools_open, as_document; agentic_core/api/scholar_review.py pack routes l.385-386; apps/workstation-superapp/src/components/qep/ChildrenApprovalPack.tsx in ScholarReviewPanel.tsx; test_w739_the_scholar_sees_and_decides_the_childrens_tools_as_one_pack (l.66733))
- **Remaining:**
  - work: Clause 4: seven tools, one a round, none built (CHILDREN_TOOLS = [] at approval_pack.py l.50): memorisation practice run by a parent or teacher; a child's challenge against their own past; a circle's shared total; teaching aids for a teacher; a tajwid companion (scholar-approved rules, a named reciter's example, record and listen back, the teacher's written feedback, no machine score); self-reported check-ins; private written reflection on scholar-approved prompts - each added to the pack and asking the gate; row: none (item clause 4)
  - work: ACCEPT 'every children's tool route is described in the pack': the module says a guard fails on an undescribed children's tool route (comment at approval_pack.py l.48-49) but no such guard exists - test_w739 does not check it and nothing else reads CHILDREN_TOOLS; row: none
- **Waits on:**
  - waits for: P5.17 clause 2 (recording on the device) for the tajwid companion; P5.17 clause 4 (circles, teachers - after sign-in) for the shared total and teacher feedback; opening (not building): P4.1 sign-in on AND a roster scholar's approval of the current pack; the standing rule of 2026-10-13 also needs a safeguarding lead, a scholar and the regulator's children's code as a source row
  - before sign in: build every tool and hold it; the pack and gate are built
  - after sign in: opening any children's tool; tools that need circles or teachers
- **Only the Owner can:**
  - name scholars to the roster (none is named); a safeguarding lead; the sign-in switch; the scholar approves the tajwid rules and the reflection prompts through the pack
- **First round:** The census guard first, then tool 1: put every children's tool route under one prefix (for example /api/v1/qep/children/) with a handler that asks children_tools_open(); a test enumerating the mounted routes under it fails when one is not in CHILDREN_TOOLS or does not answer HELD with the gate's basis while sign-in is off; then build memorisation practice run by a parent or teacher (reusing memorization/practice.py), held, with its CHILDREN_TOOLS entry (run_by, what_a_child_sees, wording, steps, arabic_from). Guard: the pack hash moves and the pack reads changed_since_approval after the addition; blinds red.

## P5.22 — The final audit - uncapped, census-partitioned, in both configurations

- **Closes when:** ACCEPT, each property driven red by a planted fault: '(1) every census surface is in exactly one slice, or the overlap is stated; (2) the union of the slices equals the census; (3) no region is capped; (4) a failed or empty region blocks completeness; (5) the measured commit is reported; (6) earlier ledgers stay byte-identical; (7) both configurations ran, or the one that did not says why.' It runs in the native-floor and the local-model configurations, after Phase 5 and the sign-in readiness round. (The 'COMPLETE when P5.1-P5.5 hold AND the whole rehearsal has run once...' line that follows it in the plan is Phase 5's completion line, not this item's ACCEPT.)
- **Delivered by:** build
- **Size:** 7–12 rounds. no census-partitioned or uncapped run has ever been made, so there is no measured rate; build about 4-6 rounds (partitioner and guard, workflow, renderer and property guards, calibration), runs about 2-4 (floor run, model run on the Owner's machine, render); findings' follow-up rows not counted
- **Open rows:** count: 1; ids: FU-1086; need owner or owner machine: FU-1086; basis: the local-model configuration exists only on the Owner's machine; the row's title still reads 'has no item that builds or runs it' though P5.22 was chartered in W754
- **Built now:**
  - A surface census computed from the tree: every app route (method + template) and every App.tsx page, exclusions listed; edition 17's census held 572 routes and 55 pages (today App.tsx has 76 <Route> entries and the code about 604 route decorators - counted by grep, the app was not imported) (scripts/audit_surface_census.py routes_of/parse_pages; counts from the parent's unexercised_v17.json)
  - The current fidelity instrument: six vision-section regions, one assessor and one refuter each (12 agents), a cap per region (default 20), floor configuration only (AI_DISABLE_LOCAL=1); W785 made the repository an argument (scripts/workflows/fidelity_audit_v7.js CAP l.49, REPO l.54, COMMON l.98-104, REGIONS l.167-180)
  - Coverage against the census and incompleteness at the cap reported; the next run pointed at what the last did not exercise (v17 left 176 routes and 14 pages unexercised) (scripts/render_fidelity_ledger.py coverage() l.211, cap reporting l.459-488; scripts/audit_unexercised.py)
  - A refutation whose agents died does not read as complete (scripts/refutation_gate.py after())
  - A fresh-store floor backend for audits; instruments refuse when they examined nothing (scripts/boot_audit_backend.py; W749 (test_w749), W777 instrument census)
- **Remaining:**
  - work: Partitioner: census to slices, each surface in exactly one slice or a stated overlap, union equals census (properties 1, 2) - new script and guard; row: FU-1086 (the item's one row)
  - work: An uncapped, census-partitioned workflow (v8): no cap (3), one assessor and one refuter per slice, a configuration argument; roughly 25-30 slices per configuration against v7's six regions; row: FU-1086
  - work: Completeness: a failed or empty slice blocks completeness (4) - v7 returns a failed assessor and an empty region the same way (fidelity_audit_v7.js l.186); the measured commit checked against the booted backend (5); row: FU-1086
  - work: Earlier ledgers byte-identical (6): a guard comparing git blobs, not working-tree bytes (the ledgers are CRLF and a Windows checkout converts unless switched off); row: FU-1086
  - work: Both configurations (7): the floor run (any machine) and the local-model run (the Owner's machine only), each saying which ran and why one did not; row: FU-1086
  - work: Calibration first (ruling 2026-10-12; P5.10 clause 5): known defects and false findings planted in one slice, one slice given to two assessors, find / false-accept / miss rates measured; row: FU-1086; shares P5.10 clause 5
  - work: The runs themselves after Phase 5, the ledger rendered, its findings registered (the follow-up rows they create are other items' work); row: FU-1086
- **Waits on:**
  - waits for: all of Phase 5 (P5.1-P5.21), which includes after-sign-in work, so transitively P4.1 sign-in; the sign-in readiness round (done, W683); P5.10 clause 5 calibration (shared); the Owner's machine for the local-model run
  - before sign in: build, guard and calibrate the instrument
  - after sign in: the run (because Phase 5 cannot finish before sign-in)
- **Only the Owner can:**
  - his machine with the local model for the second configuration; the sign-in switch, transitively; possibly a word on the agent budget an uncapped run needs
- **First round:** The partitioner and its guard: scripts/audit_census_partition.py reads audit_surface_census.py's JSON and writes slices (routes by mounted router module, pages by folder) with a declared overlap list, refusing an empty census; a test feeds a small census and plants a dropped surface, a surface in two slices with no stated overlap, an empty slice and a surface not in the census - each red with its own message - and the real tree's partition passes (properties 1, 2 and the empty half of 4).

