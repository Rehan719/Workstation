# PLAN ITEM SIZING — the eighteen items no round had ever measured

**Generated** by `scripts/`-less one-off from the W529 measurement pass; every figure below came from an
agent that read the item body and then checked the tree, and every estimate was then re-checked by a
second agent told to default to finding it wrong. 36 agents, 0 errors, 1384 tool uses.

**Why this document exists.** The pace generator reported `PROJECTION COVERAGE: 13 of 37 build item(s)
carry a registered row; the other 24 have never been sized`, and called its own projection *the weakest
number on this page*. These eighteen are the P2/P3 part of that 24. A projection averaged over work nobody
measured is arithmetic, not an estimate.

**The first thing it establishes, and it corrects a worry I had stated:** all eighteen DO carry an explicit
ACCEPT clause. The W505 problem — items with no bar to close against — does not apply here. These were
never measured, which is a different and more tractable fault.

**ONE ROUND** means roughly 2.5 hours: measuring live state, patching, a guard driven RED with an asserted
byte-restore, one full 53-minute suite, and a commit. It is the unit this programme actually moves in.

---

## The table

| item | first pass | VERIFIED | verifier | ACCEPT clause | owner-gated |
|---|---|---|---|---|---|
| **P2.11** | 2 | **2** | stands | yes |  |
| **P2.12** | 3 | **2** DOWN | overturned | yes | yes |
| **P2.14** | 2 | **2** | overturned | yes |  |
| **P2.15** | 3 | **3** | stands | yes |  |
| **P2.16** | 1 | **1** | stands | yes | yes |
| **P3.1** | 2 | **3** UP | overturned | yes |  |
| **P3.3** | 3 | **3** | overturned | yes |  |
| **P3.4** | 4 | **5** UP | overturned | yes | yes |
| **P3.5** | 3 | **2** DOWN | overturned | yes |  |
| **P3.6** | 4 | **5** UP | overturned | yes |  |
| **P3.7** | 3 | **4** UP | overturned | yes |  |
| **P3.8** | 3 | **5** UP | overturned | yes | yes |
| **P3.9** | 2 | **3** UP | overturned | yes | yes |
| **P3.10** | 2 | **2** | overturned | yes | yes |
| **P3.11** | 3 | **4** UP | overturned | yes | yes |
| **P3.21** | 2 | **1** DOWN | overturned | yes |  |
| **P3.22** | 3 | **3** | stands | yes |  |
| **P3.26** | 5 | **5** | stands | yes |  |
| | | **55** | | | |

**Total: 55 rounds** for these eighteen — roughly 138 hours at the measured 2.51h
median. The verification overturned 13 of 18 first-pass estimates: **seven went UP**, three down, three
held at the same number for different reasons. The first pass was optimistic more often than pessimistic,
which is the direction that costs, and is the whole argument for the adversarial stage.

---

## Per item — what was measured

### P2.11 — 2 round(s)

**ACCEPT (as transcribed):** ACCEPT: each compression state and each decision state is REACHABLE and asserted by a guard; the deterministic floor's run produces NOT_COMPRESSED with a reason (it is the common path, not an edge case); no field is filled by inference. THE RISK THIS ITEM MUST NOT REALISE: a compressor with no compressor writing a sentence about what the user "really" means - the brief's own `compress_noise_to_meaning` returned exactly that, hard-coded.

**Live state:** NOTHING EXISTS. Horizon is specification only; the kernel has no code at all.
· Grep over agentic_core for `HorizonObservation|IntentRecord|NOT_COMPRESSED|compress_noise_to_meaning`: NO MATCHES. A case-insensitive grep for "horizon" over agentic_core returns only unrelated `time_horizon`/`planning_horizon`/`horizon_steps` fields plus two self-describing lines in `agentic_core/constitution/CONSTITUTION_canonical.md:145-147`, which already say: "Currently NOT BUILT — Horizon is spec-only (docs/HORIZON_INTEGRATION.md)" and "Status: UNMET".
· `data/horizon/` does not exist (ls: No such file or directory); `data/` holds 30+ other stores.
· The register carries ZERO rows slotted to P2.11 (0 of 334 rows in docs/FOLLOWUPS.json). docs/WORKSTATION_IDBO_LIVING_PLAN.md:362 independently prints "P2.11 0". Per the standing rule, zero rows means UNEXAMINED, not nearly closed.
· ASKED THE ARCHIVE FIRST:

**Already satisfied:** 0 of 7 deliverables

**Paths the body names that DO NOT EXIST:** ["data/horizon/ \u2014 the directory does not exist (correctly: it is this item's own output)", "data/horizon/intent.json \u2014 does not exist", "main.py at the repo root \u2014 DOES NOT EXIST. `ls *.py` at root returns nothing and `find -maxdepth 2 -name main.py` finds nothing outside venv/_archive; the only app is agentic_core/app_mvp.py. P2.11's body does not name main.py, so this is not a broken citation in the item \u2014 but earlier notes in this programme refer to 'main.py' with 251 routes, and anyone planning 'register the middleware in main.py' would be planning against an absent file."]

**Blocked by:** ["ORDERING, by Owner ruling 2026-09-28 (docs/FABLE_DELIVERY_PROMPT.md:1757-1769): 'THE HORIZON ITEMS (P2.11\u2013P2.16) COME AFTER THE COGNITIVE ENGINES \u2026 P2.11\u2013P2.16 ", "Measured status of the gate items: P3.12 DONE W520, P3.13 DONE W524, P3.14 DONE W525, P3.15 DONE W526 (grep of '^ P3.1[2-9]' in docs/FABLE_DELIVERY_PROMPT.md). ", "NOT blocked on the Owner for content. All four Horizon decisions are RULED and their register rows are closed: FU-267 done (ruled (b), taxonomy-free \u2014 governs P", "One thing the planner must NOT plan as buildable: reaching the COMPRESSED state via a live external AI key. External providers are owner-gated. COMPRESSED has t"]

- **Surprise:** ZERO register rows ride P2.11 — 0 of 334 rows in docs/FOLLOWUPS.json, confirmed independently by docs/WORKSTATION_IDBO_LIVING_PLAN.md:362 ('P2.11 0'). By this programme's own rule that is UNEXAMINED, not nearly closed. Of the six Horizon items only P2.13 carries any rows (2).
- **Surprise:** A LIVE CANON DOC ALREADY DECLARES THIS ITEM'S ABSENCE. agentic_core/constitution/CONSTITUTION_canonical.md:145-147 states 'Currently NOT BUILT — Horizon is spec-only (docs/HORIZON_INTEGRATION.md); this article states the standing rule and its own absence' and 'Status: UNMET'. That is honest today, but it becomes a stale true-statement-turned-false the moment the kernel lands, and nothing in the register records it as a rider. It belongs in P2.11's edit set.
- **Surprise:** THE TWO SEAMS THE BODY NAMES ARE ACTUALLY ONE FILE. The body asks for 'a middleware in front of the domain routes PLUS a hook where the run paths already call operational_excellence.record_outcome'. Measured: agentic_core/api/_ai_provenance.py is a single 78-line function (ai_text) imported by law, religion, science, care, education, employment, career, refine, mega_project and management_systems — and it already calls record_outcome with served_by in hand. It has the prompt text, so it can serve OBSERVE too. An ASGI middleware would have to consume the request body to get that same raw text, which is the classic

**Verifier (estimate stands):** THE NUMBER STANDS AT 2, BUT TWO OF ITS FOUR LOAD-BEARING CLAIMS ARE WRONG AND THEY OFFSET.

WHAT I CONFIRMED. ACCEPT clause transcribed VERBATIM against docs/FABLE_DELIVERY_PROMPT.md:1801-1805 — no misquote. All 22 claimed paths exist at their stated anchors: config.py:73 atomic_write_json, config.py:282 `class store_lock`, operational_excellence.py:50 record_outcome (signature already accepts served_by/ref/run_id/vsb_id), taxonomy.py:11 DOMAINS + :84 normalise_domain, gaas/v5/__init__.py:29 intent_gate_result, _ai_provenance.py exactly 78 lines with record_outcome at :45 and exactly the 10 named importers, engine.py:4 "This is the FLOOR", orchestrator.py:256 prefer=="native" → order=["native"]. All 3 missing paths confirmed missing (`ls *.py` at root is empty; no data/horizon). LIVE STATE IS TRUE: grep for HorizonObservation|IntentRecord|NOT_COMPRESSED|compress_noise_to_meaning over agentic_core returns NO MATCHES; _archive holds only PurposeAlignmentEvaluator (unrelated); CONSTITUTION_canonical.md:145-147 says "NOT BUILT" and "Status: UNMET" verbatim. The one-round baseline is exac

- *Unverified:* The 53-minute suite runtime behind the middleware — I did not run the suite this pass. Memory corroborates it indirectly (suite ~36% of a 2.51h median round ≈ 54 min), but it is unmeasured here.
- *Unverified:* That a middleware reading the request body WOULD in fact break downstream handlers in THIS app — a known Starlette behaviour, not executed against app_mvp.py. (My Error 3 does not depend on it: the point is that the body need not be read in the middleware at all.)
- *Unverified:* Whether a reviewer would accept the _ai_provenance.ai_text seam in place of an ASGI middleware. That is a judgement about the bar, not a fact in the repo, and the item body currently says middleware.

---

### P2.12 — 2 round(s)

**ACCEPT (as transcribed):** ACCEPT: every refusal path is driven and asserted; each gate's stated limit is on the surface; the distress routes are data with a reviewed-on date shown beside them (OWNER must supply the list).

**Live state:** PARTLY DONE, and the two-thirds-complete pattern does NOT hold here - the three gates are 0.

WHAT DOES NOT EXIST. There is no gate module. Grepping the live tree for no_ruling / proof_claim / proof-claim / fail_closed / did_not_look returns nothing relevant. The word "distress" appears in NO live .py file in the repo - only in docs/ and in CONSTITUTION_canonical.md. Gate 2 (no scientific-proof claim over a theological truth) has zero code and zero precedent anywhere. There is no route-list data and no NOT SUPPLIED rendering. No guard exists: zero hits for P2.12 / Article 21 / Article 22 across the 486-test suite.

THE REPO ALREADY SAYS SO, IN ITS OWN CONSTITUTION. agentic_core/constitution/CONSTITUTION_canonical.md:143-147, Article 21: "*Verified:* the P2.12 guardrails, attached to the `gaas.v5` interceptor. Currently **NOT BUILT** - Horizon is spec-only (`docs/HORIZON_INTEGRATION.md`);

**Already satisfied:** roughly 1.5 of 8 deliverables. Satisfied: the canon refusals (A.9.5 AST-guarded by test_w513; source allow-list live in 5 modules; Articles 18/19/20 marked Verified). Half-satisfied: gate 1's REFERRAL WORDING ships as per-route disclaimer text in religion.py x3 and on ReligionHub.tsx:298 - but it is not a gate, it screens no request, states no coverage, and does not fail closed. Zero: gate 2 entirely, gate 3 entirely, the interceptor attachment, the per-gate coverage verdict, the fail-closed def

**Paths the body names that DO NOT EXIST:** ["agentic_core/horizon/ - no Horizon module exists at all", "data/horizon/ - absent (ls data/ shows no horizon dir); so no intent.json, no route-list store", "FATWA_PATTERNS - the brief's trigger regex exists NOWHERE in the repo, not even in _archive/. Named only in docs/HORIZON_INTEGRATION.md:121 as a thing from the Owner's brief. Must be written from scratch", "agentic_core/governance/gaas/v5/ EXISTS but holds only circuit_breaker_rl.py + hallucination_sandbox.py and NO interceptor and no __init__.py - a decoy 'gaas.v5' that cannot be the attachment point", "no guard anywhere: grep for 'P2.12', 'Article 21', 'Article 22' across integration_tests/test_mvp_spine.py (29,362 lines, 486 tests) returns ZERO hits"]

**Blocked by:** ["NOT BLOCKED for the build. FU-270 (docs/FOLLOWUPS.json) is the only register row slotted to P2.12 and its status is 'done', closed_by W505. Its note records: 'O", "OWNER-GATED DATA, not buildable: the distress route list CONTENT, its reviewer, and the review cadence. FU-270 lists four candidates to ratify (999, NHS 111, Sa", "SEQUENCING, not a block: P2.11 (the Horizon kernel) is unmarked in the plan and unbuilt - no agentic_core/horizon/, no data/horizon/. docs/HORIZON_INTEGRATION.m"]

- **Surprise:** The repo's own constitution already indicts this item. CONSTITUTION_canonical.md:145-147 Article 21 reads 'Currently **NOT BUILT**... *Status:* UNMET - the Horizon guardrails are specification only; no code implements them'. An article in the live canon documents its own absence. That is unusually honest and it means closing P2.12 requires editing the constitution under test_w473's path-existence guard.
- **Surprise:** The hardest clause of this item is already built for a different purpose. agentic_core/gaas/v5/__init__.py lines 12-40 (INTENT_GATE_SCOPE / intent_gate_result) and agentic_core/api/compliance.py lines 129-230 (ASSESSING_COVERAGE / COLOURING_COVERAGE / assessed() / NO_COVERAGE) together already implement 'a verdict that says what it did not look at' and 'a screen may escalate but may never clear'. P2.12 does not need to invent its coverage mechanism; it needs to apply an existing one. Nobody recorded that.
- **Surprise:** The attachment point named in the body is the wrong place. All 9 live gaas.v5 intercept() call sites are transformation / swarm / genesis / forge / economy / constitutional_gaas / board. Not one is religion, care, QEP or education. The interceptor's own comment says content_screened is False by construction. A religious question or a distress signal never reaches it.

**Verifier (OVERTURNED):** TOO HIGH BY ONE ROUND. 3 -> 2.

ACCEPT CLAUSE: transcribed CORRECTLY, word for word, against C:\Users\rehan\Workstation\docs\FABLE_DELIVERY_PROMPT.md:1819-1821. (The item title is paraphrased - the prompt says "WITH THEIR COVERAGE STATED" at :1806 - but the bar itself is exact.)

PATHS: all 17 claimed-existing paths exist; line counts check (gaas/v5 = 50+62+150+147+390 = 799, exactly as claimed). All 5 claimed-missing confirmed absent: no agentic_core/horizon/, no data/horizon/ (ls data/ has none), agentic_core/governance/gaas/v5/ holds only circuit_breaker_rl.py + hallucination_sandbox.py with no __init__.py, FATWA_PATTERNS nowhere. LIVE STATE CONFIRMED: zero hits for P2.12 / Article 21 / Article 22 in the 29,362-line suite; "distress" in agentic_core/ appears ONLY in CONSTITUTION_canonical.md:149/151. Archive checked independently - the only _archive hits for distress are two unrelated EmploymentTribunal health-impact timelines, and the only archived guardrail is _archive/jules-phase2/src/organism/python/ai_gateway/middleware/law_guardrail.py (UK Equality Act protected-characterist

- *Unverified:* Whether the new guardrails module actually lands at 250-350 lines - a forward projection, not checkable against the tree.
- *Unverified:* Whether a second refutation pass is genuinely needed in round 2, or whether one suffices. I accepted the estimate's historical base rate (W491 17/79, W503 9/46 vacuous blinds) rather than verifying it.
- *Unverified:* Whether the suite is currently green on this working tree. I did NOT run it (53m22s per W525's own record). The tree is dirty: agentic_core/api/cognitive.py, agentic_core/cognitive/__init__.py and integration_tests/test_mvp_spine.py are modified, plus an untracked agentic_core/cognitive/auxiliary/. Suite test-def count

---

### P2.14 — 2 round(s)

**ACCEPT (as transcribed):** ACCEPT: each tier's route is driven and asserted; a tier-3 proposal cannot be self-applied (the guard proves the refusal); the register shape is shared with P2.10, not forked.

**Live state:** NOTHING OF THIS ITEM EXISTS. `LessonRecord` appears in exactly two files repo-wide — docs/FABLE_DELIVERY_PROMPT.md and docs/HORIZON_INTEGRATION.md (Grep over the whole tree: 2 files, zero code). No "friction", "candidate_cause" or "not determined" string anywhere in agentic_core/*.py. No Horizon module, no Horizon router mounted in agentic_core/app_mvp.py, no data/horizon/ directory. ZERO follow-up rows are slotted to P2.14 (checked all 334 items in docs/FOLLOWUPS.json by `slot`; P2.13 has 2 open, P2.17 has 3, P2.14 has 0) — which per the W505 lesson means UNEXAMINED, not nearly closed. BUT the dependency is already satisfied and the scaffolding is unusually good: docs/HORIZON_INTEGRATION.md §8 lists P2.14's only blocker as **P2.10**, and P2.10 is ✅ DONE W508 (prompt line 1612). So P2.14 is unblocked today and does NOT require P2.11. What is reusable, read and confirmed: (1) the register

**Already satisfied:** 0 of 12 deliverables (the mechanism is ~1/3 PRECEDENTED by P2.10's breach loop, but 0/12 delivered — no LessonRecord type, no store, no hook, no tier router)

**Paths the body names that DO NOT EXIST:** ["data/horizon/ (the whole directory)", "data/horizon/lessons.json", "data/horizon/intent.json", "data/horizon/genome.json", "agentic_core/horizon/ (no Horizon module anywhere)", "agentic_core/api/horizon.py (no Horizon router; no /api/v1/horizon mount in agentic_core/app_mvp.py)"]

**Blocked by:** ["NOT blocked. docs/HORIZON_INTEGRATION.md \u00a78 names P2.10 as P2.14's ONLY blocker, and P2.10 is \u2705 DONE W508 (docs/FABLE_DELIVERY_PROMPT.md line 1612). P2.11/P2.12", "All four Horizon Owner decisions are RULED and closed: FU-267, FU-268, FU-269, FU-270 all carry status 'done' in docs/FOLLOWUPS.json, and HORIZON_INTEGRATION.md"]

- **Surprise:** The body says risk tiers 'map onto change_control's existing classes', but there is NO 0-5 tier scale anywhere in change_control. I read _TIER_MAP (agentic_core/api/change_control.py:271): 14 change_type strings over a FOUR-rank impact scale (LOW/MEDIUM/HIGH/CRITICAL). So the 0-5 -> class mapping does not exist to be reused — this item must INVENT and state it. The body glosses that as reuse.
- **Surprise:** A REAL TRAP in the mapping the spec does name. HORIZON_INTEGRATION.md §6 routes tier 2 to `config_minor`, and _TIER_MAP puts config_minor at LOW. I then read change_control.py:365 `awaiting_board_ratification()`: only an APPROVED change at HIGH or above waits for the Board. So anything Horizon files as config_minor can be approved without ratification. If a builder reaches for the only change_type the spec names and files tiers 3-5 as config_minor too, the ACCEPT's 'a tier-3 proposal cannot be self-applied' could pass INSIDE Horizon while change_control then approves it unratified — the refusal would be real and 
- **Surprise:** Work already done that nobody recorded against this item: method.py:900-1020 is substantively P2.14's mechanism already running at METHOD scope — a runtime ledger, a counted escalation, a submission to change_control with submitted_by set, a three-state verdict and a stated limit. P2.14 is largely a second instance of a loop that already works, which is why the item says 'ONE register shape, ONE arms-length gate'. The register shows zero rows on P2.14, so this reuse has never been written down.

**Verifier (OVERTURNED):** THE NUMBER SURVIVES, THE BASIS DOES NOT. 2 rounds stands, but the measurement's decisive premise is factually false and the cost sits somewhere else than it claims.

WHAT VERIFIED CLEAN. ACCEPT clause transcribed VERBATIM (docs/FABLE_DELIVERY_PROMPT.md:1839-1841; item head at :1832). All 12 claimed-existing paths exist, with the stated line counts: agentic_core/api/method.py 1778, agentic_core/gaas/v5/policy_gate.py 62, change_control.py _TIER_MAP at :271, POST /correct at method.py:1243, record_breach at :939 writing under store_lock+atomic_write_json (:957-967, not the cited 950-962), breach/escalation guard at integration_tests/test_mvp_spine.py:27410-27463. All 6 claimed-missing paths genuinely absent. docs/DELIVERY_METHOD.json is exactly 101 lessons / 12 mechanisms / 6 defect classes with fields id/group/rule/defect/apply/enforced_by/why_not_enforced. docs/FOLLOWUPS.json: 334 items, 45 open, P2.14 = 0 rows at ANY status (UNEXAMINED, per W505). Unblocked claim CONFIRMED: HORIZON_INTEGRATION.md:269 names P2.10 as P2.14's only blocker, and P2.10 is DONE W508 (prompt:1612).

LIVE ST

- *Unverified:* "Each round carries one 53-min serial suite" — I did not run the suite; the figure comes from the register/prior rounds, not from a measurement this pass.
- *Unverified:* Whether P2.14 needs a FastAPI-LEVEL raised-handler seam in addition to the interceptor's except-block. agentic_core/app_mvp.py has exactly ONE exception_handler (RequestValidationError at :66) and no generic Exception handler, so a global seam would be new code with suite-wide blast radius across a 29,362-line guard fi
- *Unverified:* I verified the ~10 intercept() call sites sit inside route handlers of routers mounted in app_mvp.py, but I executed NO route — so "the hook is reached by calling the route" is verified by reading, not by driving (which is precisely what the item's own ACCEPT demands be proven by driving).

---

### P2.15 — 3 round(s)

**ACCEPT (as transcribed):** ACCEPT (observables added W505 — the three claims were unfalsifiable as written, and "every figure traces to a measured fact" is a claim ABOUT claims, which is the shape this programme keeps being caught by):
(1) EVERY FIGURE TRACES: each field of a ConsumptionRecord names its source, and a guard drives a run whose provenance map is EMPTY and asserts the record says so rather than reporting 0 — a zero that means "not measured" is the defect, not the absence of a number;
(2) AN UNFILLED OWNER FIELD RENDERS AS UNFILLED: a guard reads a record the Owner has not touched and asserts the surface shows "not filled", never 0, "" or a default — driven on the PAGE, not only on the API, because a write

**Live state:** NOTHING of the ConsumptionRecord exists in code. `ConsumptionRecord` / `consumption_record` appear in exactly two files, both docs: docs/FABLE_DELIVERY_PROMPT.md and docs/HORIZON_INTEGRATION.md (ripgrep, whole tree). Every case-insensitive "consumption" hit under agentic_core/ is the unrelated ATP simulator (agentic_core/molecular/atp_simulator.py, agentic_core/organism/biobus.py, agentic_core/organism/heartbeat.py, agentic_core/app_mvp.py). No test in integration_tests/ mentions P2.15. There is no agentic_core/horizon/ package and no data/horizon/ store; `IntentRecord`, `HorizonObservation` and `NOT_COMPRESSED` exist only in those same two docs, so the P2.11 kernel this record joins to is not built. No Horizon page exists (the two "Horizon" hits in apps/workstation-superapp/src are the `MoreHorizontal` lucide icon in CEOChat.tsx and a `planning_horizon` form field in enterprise/Manageme

**Already satisfied:** roughly 0.8 of 3 ACCEPT clauses — clause (3) is ~80% met by an existing green guard, clauses (1) and (2) are 0; of the 6 named record fields, 1 (calls/what-served) has a reusable producer and it currently carries the exact defect clause (1) forbids

**Paths the body names that DO NOT EXIST:** ["agentic_core/horizon", "data/horizon", "data/horizon/intent.json", "the Horizon surfaces (clause 3 names these as a check target; no Horizon page or module exists anywhere in apps/workstation-superapp/src or agentic_core)"]

**Blocked by:** ["P2.11 (the Horizon kernel) is NOT built \u2014 no agentic_core/horizon/, no IntentRecord, no data/horizon/intent.json \u2014 so 'joined to each run' has no run identity t", "Clause (2) requires a PAGE. No Horizon surface exists; P2.16 (the companion surface) is unbuilt and its own register row FU-297 was DROPPED because P2.16 states", "The sequencing P2.11 itself names: 'Nothing in P2.11-P2.16 is Owner-blocked; the sequencing behind P3.12-P3.19 is what holds them.' Measured: P3.12 DONE W520, P", "NOT owner-gated and I checked: all four Horizon owner decisions are closed (FU-267, FU-268, FU-269, FU-270 all 'done'); the only open Horizon rows are FU-296 an"]

- **Surprise:** Clause (3) is almost already met and nobody recorded it. integration_tests/test_mvp_spine.py:28039 (test_w513_no_live_module_computes_a_spiritual_score) already sweeps agentic_core/ and products/ on the BINDING, with virtue_score/barakah_score/gratitude_score in its FORBIDDEN set and `assert checked > 200` so it is not vacuous. Missing only `spiritual_station`, `virtue_forged`, and .tsx coverage.
- **Surprise:** The defect clause (1) was written against is LIVE TODAY in the helper the item says to reuse. I executed it: `_provenance_summary([])` returns calls=0, floor_calls=0, model_calls=0 — a zero that means 'not measured'. The item reads as if the provenance map were a clean input to build on; it is not, it is part of the work.
- **Surprise:** A second instance of the same class in the same return value: `any_external: False` over zero calls asserts that no external model served a run nothing measured.

**Verifier (estimate stands):** THE NUMBER STANDS AT 3, BUT NOT FOR THE REASONS GIVEN. Two of its cost drivers are not real and two real ones were missed; the errors roughly cancel. Corrected arithmetic: clause (3) ~0.3 + clause (1) ~1.8 + clause (2) ~0.7 = ~2.8 -> 3.

VERIFIED TRUE: ACCEPT transcribed verbatim (docs/FABLE_DELIVERY_PROMPT.md:1842-1858, all three clauses word-for-word). All 9 claimed-existing paths exist; all 3 claimed-missing are absent. `ConsumptionRecord`/`consumption_record` really is only in two docs (HORIZON_INTEGRATION.md:149,270; FABLE_DELIVERY_PROMPT.md:1842,1849) -- and the archive is GIT-TRACKED (3679 files, so ripgrep covered it); the only archive "horizon" hit is _archive/legacy-archive/orphaned_dirs/recirculation/long_horizon_task.yaml, unrelated v17 legacy. `_provenance_summary` is at intelligence.py:344 with exactly the described keys and exactly 7 call sites at 528, 570, 675, 710, 919, 1201, 1440. The defect is live -- I extracted and executed the function standalone: `_provenance_summary([])` -> {'calls': 0, 'floor_calls': 0, 'any_external': False, ...}; `_run_summary_text(6, [])` 

- *Unverified:* "CLAUSE (1)'s DEFECT IS LIVE AND I DROVE IT" -- I confirmed the BEHAVIOUR by extracting the three helpers from intelligence.py and executing them standalone (empty run -> calls 0, any_external False), but I cannot verify the estimate itself executed anything. The defect is real either way.
- *Unverified:* The W513 guard's greenness UNDER PYTEST. I replicated its body exactly in a standalone script (647 files checked, 0 hits, `checked > 200` satisfied) but did not run pytest, so a fixture-level or collection failure is unverified. Deliberate: a round is in progress (integration_tests/test_mvp_spine.py is modified in the 
- *Unverified:* Whether the uncommitted working tree changes the measurements. I measured the tree AS IT STANDS, which includes modified agentic_core/api/cognitive.py, agentic_core/cognitive/__init__.py, integration_tests/test_mvp_spine.py and untracked agentic_core/cognitive/auxiliary/. A measurement at committed HEAD (002c48b1) coul

---

### P2.16 — 1 round(s)

**ACCEPT (as transcribed):** ACCEPT: the not-compressed and no-escalation states are reachable on the page and asserted by a probe; nothing on it claims an alignment the kernel did not evaluate.

**Live state:** NOTHING EXISTS. No Horizon membrane code is in the tree at all. Grep over the whole repo for IntentRecord|HorizonObservation|ConsumptionRecord|LessonRecord|NOT_COMPRESSED|"no station assigned" returns exactly TWO files, both prose: docs/FABLE_DELIVERY_PROMPT.md and docs/HORIZON_INTEGRATION.md. Grep -i "horizon" over agentic_core/ hits 11 files, every one of them a false positive on "horizontal" or a planning "time horizon" (spot-checked agentic_core/api/intelligence.py = "horizontal/vertical scaling"); over apps/workstation-superapp/src/ it hits 6 files, all "horizontal"/"MoreHorizontal" (Shell.tsx PanelGroup direction, CEOChat.tsx lucide icon). There is no agentic_core/api/horizon.py among the 71 entries of agentic_core/api/, no Horizon or Companion page among the 45 entries of apps/workstation-superapp/src/pages/, and `ls data/horizon` → "No such file or directory". So P2.16 is 0% buil

**Already satisfied:** 0 of 13 deliverables

**Paths the body names that DO NOT EXIST:** ["data/horizon/ \u2014 `ls data/horizon` \u2192 No such file or directory (checked against a data/ listing of ~40 entries)", "data/horizon/intent.json \u2014 the store the page is meant to read", "agentic_core/api/horizon.py \u2014 absent from the 71-entry agentic_core/api/ listing", "agentic_core/horizon/ \u2014 no such package anywhere (repo-wide find for *horizon* returns only docs/HORIZON_INTEGRATION.md, a venv kubernetes autoscaler, and _archive/legacy-archive/orphaned_dirs/recirculation/long_horizon_task.yaml)", "any Horizon/Companion page under apps/workstation-superapp/src/pages/"]

**Blocked by:** ["OWNER RULING, sequencing (docs/FABLE_DELIVERY_PROMPT.md:1758-1762): 'P2.11-P2.16 are not eligible for a round until the engine items are done, and a round that ", "P2.11 (data): docs/HORIZON_INTEGRATION.md:271 names P2.11 as P2.16's only blocker, and it is real \u2014 the ACCEPT's not-compressed and no-escalation states are sta", "P2.12 and P2.15 (partially, for completeness rather than for the bar): 'the escalations' are P2.12's gate verdicts and 'the consumption' is P2.15's ConsumptionR"]

- **Surprise:** THE REGISTER CARRIES A DROPPED ROW THAT WAS BUILT ON A MIS-MEASUREMENT OF THIS EXACT ITEM, and the correction is already recorded. FU-297 ('P2.16 states no ACCEPT bar, so the Horizon companion surface cannot be closed as written', slot P2.16, status dropped) was registered in W505 by a pattern that required ACCEPT at line start, while P2.16's sits mid-line at 1862. Its own note says so: 'A register row built on a mis-measurement sends a later round to fix nothing, which is worse than having no row.' The ACCEPT clause landed much earlier than W505 — git log -S dates it to d7b92043 (W495, the Horizon interrogation 
- **Surprise:** FU-297's correction note MIS-QUOTES the bar it corrected: it renders the clause as '...asserted by a guard' where the live prompt text says '...asserted by a probe'. Immaterial to the work, but it means the register's copy of the bar is not the prompt's copy, and the item must be closed against the prompt.
- **Surprise:** THE BODY AND THE ACCEPT DISAGREE ON WHICH STATES ARE BARRED. The body names TWO printed truths — 'not compressed' AND 'no station assigned'. The ACCEPT bars the first and substitutes a different second one: 'the not-compressed and no-escalation states'. So 'no station assigned' is a deliverable with no bar, and 'no-escalation' is a bar with no matching sentence in the body. Per the programme's own rule that an item's deliverables ARE its bar, the closing round should assert all three, not the two the ACCEPT happens to name.

**Verifier (estimate stands):** 1 ROUND STANDS. I defaulted to finding it wrong and could not. Every one of the 10 claimed-existing and 5 claimed-missing paths verified; every count exact (45 pages / 74 <Route / 71 api entries / app_mvp 689 lines, 81 include_router / test_mvp_spine 29,362 lines, 486 tests / data/horizon absent). ACCEPT transcribed VERBATIM at FABLE_DELIVERY_PROMPT.md:1859-1863. Calibration commit 20924ca1 matches line-for-line (18 files, 2,137 insertions, method.py +500, DeliveryMethod.tsx +210, DELIVERY_METHOD.json +371, test_mvp_spine.py +511). The live_state survives the archive check this repo's own lesson says usually breaks it: 5,031 files under _archive/, zero Horizon work; the sole filename hit long_horizon_task.yaml is a v17.0 biofoundry/tribunal manifest (the false positive the estimate itself named); repo-wide the record types return exactly two files, both prose. THREE DEFECTS, none of which moves the number. (1) THE REAL ONE - THE BASIS UNDERSTATES ITS PRECONDITION. It says "once P2.11 has landed; it is not buildable at all before then", naming ONE blocker. The actual gate is the Owner

- *Unverified:* P2.16's probe runtime: I did not run the suite and did not boot the app, so the estimate's own honest flag stands unresolved — the 486-test suite's cost is cited elsewhere as ~46 min (~19% of a round) but I did not measure it this session.
- *Unverified:* P2.11's own size: cannot be sized from P2.16's body, so the ~3-round pair figure for a bundled P2.11+P2.16 is unverified. It is the estimate's own flagged gap and I could not close it.
- *Unverified:* Whether the four open engine items (P3.16-P3.19) change P2.16's SCOPE rather than only its timing. The ruling at line 1766-1767 asserts it 'does not reduce their scope or change any of their ACCEPT criteria', but FU-333 shows P3.16's own wiring currently runs through an always-approving Mock regulator, so what the kern

---

### P3.1 — 3 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W508 by transcribing this item's own deliverables, which had never been stated as a bar):
(1) §4.6 Develop is a DISTINCT journey stage, present between design and operational intelligence — and
    its own stage verification appears in `stage_verifications` beside the others, not only in prose;
(2) it produces at least ONE buildable, checkable artefact of the three the item names (a costed bill of
    materials, a runnable prototype spec, or a parameterised model via factory/forge) — checked by the
    artefact EXISTING in a store, not by the stage having run;
(3) a REAL pass/fail is recorded in the journey for that artefact: a guard drives the FAILING case, so a
    run whos

**Live state:** NOTHING EXISTS — and for once the plan's claim and the tree agree, which I checked rather than assumed. (a) The journey has five fixed body stages: `stage_verifications` is built at agentic_core/api/genesis.py:613-618 with keys concept, research, design, operations, commercialisation (plus W506 derived stages appended at :623-627). There is no develop key, no sixth prompt, no §4.6 anything. (b) `JOURNEY_BODY_AGENTS` at genesis.py:883 is a fixed 5-tuple with no develop agent; the response payload at :707-710 jumps straight from `phase_2_design_development` to `stage_7_operational_intelligence`. (c) The live code itself records the gap: agentic_core/api/living_plan.py:46 comments "§4.6 Develop has no stage", and docs/WORKSTATION_IDBO_LIVING_PLAN.md:464 keeps row 1 at ◐ partly "and §4.6 Develop has no stage — plan P3.1". (d) A repo-wide ripgrep for `develop_artefact|develop_stage|stage_6|ge

**Already satisfied:** 0 of 4 ACCEPT legs (and 0 of 7 deliverables); the stage/verification/floor machinery it plugs into does exist

- **Surprise:** The body names ZERO file or directory paths, so the phantom-path failure mode the task warns about cannot apply here — the only identifiers it names are the response field `stage_verifications` (real, genesis.py:613) and the capability 'factory/forge' (real, agentic_core/api/forge.py).
- **Surprise:** P3.1 is NOT one of the owner-decision rows. P3.0 (docs/FABLE_DELIVERY_PROMPT.md:1965-1978) lists rulings for 3.10, 3.11, 3.5, 3.6, 3.4 and the five QEP A.12 items; 3.1 is absent from that list. Nothing about this item needs an owner ruling, and the test path needs no live key.
- **Surprise:** THREE existing assertions are hard-coded to the current five-stage journey and will go RED the moment a sixth stage lands — integration_tests/test_mvp_spine.py:8147 (`assert d.get("stages_floor_served") == 5`), :17748 and :17751 (`assert gr["calls"] == 5`). Plan the edit, or the round reads as a regression.

**Verifier (OVERTURNED):** ACCEPT transcribed VERBATIM correct (docs/FABLE_DELIVERY_PROMPT.md:1979-1992, all four legs word-for-word). All 7 claimed paths exist with the claimed line counts (genesis.py 1476, forge.py 275, vsb.py 2545, config.py 393, tsx 1254, test_mvp_spine.py 29362) and the claimed anchors are exact: stage_verifications at genesis.py:613 with the five keys and derived stages at :624-627; _verify_stage at :100; _floor at :602; JOURNEY_BODY_AGENTS 5-tuple at :883; payload jumping phase_2_design_development -> stage_7_operational_intelligence at :709-711; living_plan.py:46 comment; vsb.py:145 and :2243; config.py atomic_write_json:73, store_lock:282 (a class), data_path:379; tsx type :47, generic badge loop :680, export :255-257. LIVE STATE IS TRUE, archive included: with --no-ignore over _archive/ the only hit for bill_of_materials is a background directive .txt, no code; zero matches for genesis_develop/develop_artefact/artefact_check anywhere; "not buildable on the floor" exists only in the item body. 0 of 4 legs met. TWO THINGS PUSH IT PAST 2 ROUNDS. (1) The ripple set is not the "three meas

- *Unverified:* genesis.py:551 and :566 as the exact line numbers of the operations and commercial `_q` prompts - both calls are in that neighbourhood (read 540-575) but I did not pin the two numbers exactly
- *Unverified:* forge.py:61 and :69 as the `factory` and `generator` stage lines - not individually checked; the file and its _STAGES dict at :38 do exist
- *Unverified:* the ~53-min suite and the per-round hour figures are carried from prior measurement, not re-measured in this pass; I ran no tests

---

### P3.3 — 3 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables):
(1) a heartbeat-driven Strategic refresh (quarterly + market signal) and an Action-Plan refresh (weekly + KPI-triggered) each WRITE to the plan, driven by forcing the trigger rather than waiting for it;
(2) every written refresh carries its provenance and joins a history — a refresh that overwrites without a history entry fails this;
(3) the board-pack layers are assembled FROM those refreshes: a guard changes a refresh and asserts the pack changes, because a pack that reads elsewhere would look identical;
(4) the values in the pack come from the VSB's OWN constitution, and an entity with none says so rather than showing the platform's

**Live state:** NOTHING of the cadence exists; two supporting pieces are partly built. Measured: (a) grep for strategic_refresh|action_plan_refresh|market_signal|strategic_review across the tree hits ONE file and it is _archive/agentic_core/biochemical/rectification_engine.py — no live code; grep -i for 'quarterly|weekly' across agentic_core returns 6 hits, all prompt text or comments (api/v310/business.py, api/management_systems.py, layers/l11_civilisation, care/scoring.py) — no scheduler. (b) THE PLAN IS REAL and is per-VSB: agentic_core/api/business_plan.py keeps data/business_plans/<scope>.json, scope == vsb_id (seeded at establish, agentic_core/api/vsb.py:1716-1735, with objectives carrying kpi/timeline/progress_pct/status/reviews), and heartbeat.py:54 already reads it (screen_living_vsb). (c) A WRITER EXISTS but is manual and prose-based: POST /api/v1/business-plan/generate (business_plan.py:480-5

**Already satisfied:** 0 of 7 deliverables complete; 2 partly (a plan writer that records provenance but keeps no history, and a board pack whose layers honestly disclose that they are NOT the cadence layers)

**Paths the body names that DO NOT EXIST:** ["agentic_core/organism/cadence.py (no cadence module anywhere)", "agentic_core/api/cadence.py", "no per-scope plan history file: nothing under data/ holds business-plan versions (contrast data/vsb_compliance_history.json and data/vsb_board_packs, which do)"]

**Blocked by:** ["SOFT, not a gate \u2014 unruled Owner ruling 3.6 (docs/FABLE_DELIVERY_PROMPT.md:1965, P3.0: 'KPI gate ... until the owning VSB's objective KPIs are set and tracked, ", "'Market signal' has no source and must not acquire one by egress: the Owner's FU-167 ruling is no egress, and no external AI key is configured in this environme", "ACCEPT(4)'s positive leg cannot be proved until a per-VSB constitution values writer exists \u2014 none does (one constant string in all of agentic_core). The round "]

- **Surprise:** The item body names ZERO file or directory paths — so the path-rot failure mode cannot apply, but nothing in the item tells a builder where the work lands. The only pointer is docs/FOLLOWUPS.json's 'routes' table (slot 'P3.3' → agentic_core/api/business_plan.py, words: board pack / business plan / living business system).
- **Surprise:** ACCEPT(2)'s named defect is ALREADY SHIPPED in the nearest writer: provenance.generation in business_plan.py is one dict overwritten on every /generate, so today a refresh would overwrite without a history entry.
- **Surprise:** data/business_plans/ holds 1,895 files, overwhelmingly pytest fixtures — the same test-data accretion W417 found in the living roster (157 of 191 entries were fixtures, and the organism spent five sixths of its cycles on them). A round-robin cadence over the roster will do the same unless it is scoped.

**Verifier (OVERTURNED):** THE NUMBER STANDS; THE ROUND-2 SCOPE STATEMENT IS WRONG. ACCEPT is transcribed verbatim (FABLE_DELIVERY_PROMPT.md:2012-2020). All 11 claimed-existing paths exist; both claimed-missing are absent (no file named cadence* anywhere outside data/). Every live-state claim verified, and two are stronger than stated: 0 of 1,895 plan files on disk carry provenance or history (not just the two largest), and business_plan.py has no version/history machinery at all, only per-objective reviews — so ACCEPT(2) genuinely needs new machinery. Premise (d) confirmed and load-bearing: generate_plan writes nothing when served_by is native/unavailable, so the refresh MUST compute from live state. (e)/(f) confirmed verbatim, and _pack_content_hash(layers, economy, ...) does cover layers. (h) confirmed exactly: 334 items, 45 open, 0 with slot P3.3; the "slot":"P3.3" at line 6040 is in the routes table. UNSOUND BECAUSE: round 2's "a new opt-in flag through the 6 known points" is a measured error. The real surface is 7 backend sites (heartbeat.py 163/346/778/836/846/892 + api/heartbeat.py 55/62) PLUS two fron

- *Unverified:* The 53-minute suite cost per round and "collateral is likely" — I did not run the suite, as instructed not to edit or build; the basis itself also declares this unmeasured.
- *Unverified:* That the two refresh generators can in fact compute content from economy + §11 verdict + stage + objective progress — I verified each source EXISTS and is readable, but not that the composed output is substantive enough to satisfy ACCEPT(1) without a model.
- *Unverified:* Whether the new per-scope history should be one keyed file (vsb_compliance_history.json's shape, as proposed) or 1,895 sibling files — an undecided design point in the basis; either works, neither measured.

---

### P3.4 — 5 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables — Mode 2 per the Owner's ruling):
      (1) a per-founder model is BUILT from the explicit profile + instructions + decisions, and a Chief with
          no such inputs is reported as a ROLE and not as a modelled twin — the distinction W492 already
          forced onto the fidelity ledger;
      (2) the twin is invoked UNPROMPTED: the heartbeat's auto_align produces a board_directive with execute,
          driven by a beat rather than by a manual call;
      (3) every twin output is rendered WITH its basis — which inputs it was built from, and how many;
      (4) a per-VSB Chief is titled for its owner: a guard asserts no Chief is titl

**Live state:** THE BODY NAMES ZERO FILE OR DIRECTORY PATHS — it names only mechanisms (auto_align, board_directive, "of default"). Every path in paths_that_exist was resolved and opened BY ME, not named by the item; all 26 exist (no missing-path failure mode here).

Criterion-by-criterion, measured:

(4) ALREADY DONE, ALREADY GUARDED — 0 work. `grep "of default"` over all .py/.tsx returns ZERO occurrences outside docs. board.py:203-208 (`board_for_owner`) maps a 'default' owner to 'the founder' explicitly. A guard already exists at integration_tests/test_mvp_spine.py:17103-17109: `t = _board.board_for_owner("default")["chief"]["title"]; assert "Digital Twin of" not in t and "the founder" in t and "no twin model" in t`. W475/W492 landed this.

(1) ABOUT 40% PLUMBED, AND ITS THREE INPUTS ALL EXIST. The "explicit profile" the body names is REAL and built: agentic_core/ai/user_context.py (W428) holds PROFI

**Already satisfied:** 1 of 4 ACCEPT criteria fully satisfied and already guarded (criterion 4); criterion 2 ~70% plumbed (one hard-coded execute=False), criterion 1 ~40% (all three inputs exist as live stores, none wired to the Chief), criterion 3 ~10% (a boolean where a counted basis is required)

**Blocked by:** ["OWNER RULING 3.4 'Mode 2 scope', listed as OUTSTANDING at P3.0 (docs/FABLE_DELIVERY_PROMPT.md:1969) and never recorded as ruled. docs/WORKSTATION_IDBO_WHOLE_VIS", "The plan's own convention makes building first a defect: P3.8 ACCEPT (3) reads 'no ruling is implemented before it is ruled: an unruled item keeps saying so.'", "THE RULING IS NARROW AND CHEAP TO GET, and worth asking as one question: does Mode 2 mean (a) a COMPOSED per-founder model \u2014 the explicit profile + that owner's"]

- **Surprise:** The item's three named inputs are not hypothetical — all three stores exist and are live. The 'explicit profile' is a fully built W428 feature (agentic_core/ai/user_context.py + GET/PUT/DELETE /api/v1/user/profile), tenant-safe by design, and the gateway already injects it at gateway.py:294-295. Nobody connected it to the Chief. This item is a composition job over existing parts, not new capability.
- **Surprise:** CRITERION 4 IS ALREADY DONE AND ALREADY GUARDED. 'of default' has zero occurrences in any .py or .tsx; board.py:206 maps it away; test_mvp_spine.py:17103-17109 asserts it. The item's single most emphatic bar ('the exact string W492 found shipped') is historical.
- **Surprise:** THE ITEM'S CRITERION (2) HAS A PREMISE PROBLEM, the shape the task warned about. The chief_twin pillar at agentic_core/api/transformation.py:98-102 has exactly one evidence check — `_has(r, '/api/v1/board')`, a route-mount test. Every tier's router is imported at startup, so it CANNOT fail while the app answers; chief_twin is therefore permanently realisation 1.0 / 'realised', and cognition.py:148 skips realised pillars. The Chief gap can never reach auto_align's router at all. A beat-driven board_directive is still reachable through another Board-routed gap, but not deterministically, because align acts on the s

**Verifier (OVERTURNED):** ACCEPT transcribed verbatim (FABLE_DELIVERY_PROMPT.md:2021-2031); all 26 paths exist; every falsifiable live-state claim held when I read the files — "of default" absent from code, twin_basis/founder_basis/modelled_from zero matches repo-wide, gateway.py:358 is a bare bool, heartbeat.py:363 hard-codes execute=False, and the chief_twin determinism hole is real (transformation.py:97-101 has one evidence check, _has(r,"/api/v1/board"), so cognition.py:148 skips it forever). The archive holds nothing that reduces cost: its twin work is federation node twins and a mocked simulation bootstrap. Register claim confirmed (334 rows, no P3.4 slot, no OWNER row for ruling 3.4). The estimate is still too low by one round, understating in four measured places. (a) The sweep is ~22-24 live sites, not ~18, and misses two whole files: VSBSpawnStudio.tsx:503 is a RENDERED fallback title and change_control.py:1787 a docstring; VSBCockpit.tsx holds three sites, so Round 4 faces six surfaces not five. (b) A fourth existing guard goes red and is uncounted: test_mvp_spine.py:1699 test_tier_identity_and_fou

- *Unverified:* The 53-minute suite duration and the per-round pacing — I did not run the suite.
- *Unverified:* Whether the three non-Chief statements are in the sweep's scope: test_mvp_spine.py:10294-10295 (twin_prevalidation source_label 'no twin model — health gate only') and :20510 / VSBCockpit.tsx:1145 ('no twin model is simulated') stay TRUE under a founder model, since they concern /twin/models pre-validation and the casc
- *Unverified:* Whether Round 1's founder_model can be purely additive beside board.py:143 or must replace founder_profile — that depends on an implementation choice not yet made, and it decides whether the :1699 guard is rewritten or merely re-driven.

---

### P3.5 — 2 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables):
      (1) an OWNED vision resource reads an attached image into text — driven with a real image, and the text
          it produced is asserted to be non-empty and to come from that image;
      (2) where no such resource is installed it REFUSES with an accurate reason naming what is missing, and
          produces no text — a fabricated description is the defect this item exists to prevent, and it is the
          same class as the transcription mock W495 deleted;
      (3) the accept list states what IS supported, computed from the installed resource rather than written
          as a constant — a list that names a format nothing can

**Live state:** PARTLY DONE, but on the WRONG SURFACE — and the central premise holds (an owned vision resource genuinely exists), so this is not a disproved item.

What exists (measured, not inferred):
1. An owned vision path IS real: agentic_core/avatars/api.py:251-271 `_ollama_vision()` posts the base64 image to a LOCAL Ollama vision model (OLLAMA_VISION_MODEL, default "llava") and returns its text, or None. It is owned, no key, no external dependency. Legs 1 and 2 of ACCEPT are therefore buildable, not speculative.
2. Honest refusal already shipped, with four named states: avatars/api.py:347-400 sets image_status to read | failed_external | blocked_by_policy | no_vision_model, never fabricates a description, and marks image_is_external=True the moment transmission is ATTEMPTED (lines 362-369). The reader is wired too: VSBCockpit.tsx:1252-1262 prints status-specific copy. That was closed under P2.3/F

**Already satisfied:** 0 of 3 ACCEPT legs fully met, and 0 of 4 deliverables on the Describe surface the item is about. Counting the Converse-tab precursor (a different surface, closed under P2.3 at W490): leg 2 is ~70% met there, leg 1's production code exists but is unproven by any test, leg 3 is 0%.

**Paths the body names that DO NOT EXIST:** ["No vision router exists \u2014 I listed all 56 files in agentic_core/api/ and there is no vision.py; grep for image_to_text|describe_image|vision_model|image_intake across the repo returns only agentic_core/avatars/api.py, docs and .env.example", "No vision-capability DISCOVERY exists \u2014 nothing in the repo reads Ollama's model family metadata; grep for families|clip|mllama|llava|moondream in agentic_core/ hits only the five comment/env lines in agentic_core/avatars/api.py", "No OCR path exists \u2014 grep for \\bocr\\b|OCR repo-wide matches only _archive/frontend/pages/domains/QEPAIPortalPage.tsx and _archive/scripts/Religion/QuranEducation/ai/cv_simulator.py (both archived)", "No follow-up row rides P3.5 \u2014 docs/FOLLOWUPS.json has 334 items and the only P3.5 mention is FU-294 (the no-ACCEPT-bar sweep, status done). FU-191 (the avatar image-label shortfall) is slot P2.3, closed_by W490 \u2014 i.e. the Converse-tab half was closed under a DIFFERENT item."]

**Blocked by:** ["Nothing must land first \u2014 no owner decision gates this item, and no other plan item blocks it. docs/FOLLOWUPS.json carries no open rider on P3.5 (334 items; the", "Non-blocking environment rider, worth stating so it is not mistaken for a gate: for image intake to actually PRODUCE text on the owner's machine, a local vision", "Hard constraint on how leg (1) may be satisfied: agentic_core/avatars/api.py:362-369 routes to OpenAI gpt-4o-mini behind OPENAI_API_KEY AND AI_ALLOW_EXTERNAL. T"]

- **Surprise:** The item body names ZERO file or directory paths — unusual for this plan, and it means nothing here could be mis-pointed. I resolved both surfaces myself (Describe -> GenesisJourney.tsx:556 + AttachDocument.tsx; Converse -> VSBCockpit.tsx) and every file I resolved exists.
- **Surprise:** Work already done that nobody recorded against this item: the whole honest-refusal apparatus for image intake — four named statuses, no fabricated description, truthful is_external on an ATTEMPTED send, and status-specific reader copy — already shipped at W490. But it closed FU-191 under slot P2.3, so P3.5's register shows nothing and the item reads as untouched when roughly two-thirds of leg (2) is built on a neighbouring surface.
- **Surprise:** A live defect, directly in this item's class, that the body does not mention: agentic_core/avatars/api.py:257 reads OLLAMA_VISION_MODEL with a "llava" default and never presence-checks it, so with a vision model CONFIGURED BUT NOT INSTALLED the refusal at line 399 tells the user to "set OLLAMA_VISION_MODEL" — the variable they already set. This is exactly the class W492/FU-183 fixed for text models at model_resource.py:107-127 ('a default that is not present is not a default'), left unfixed on the vision path.

**Verifier (OVERTURNED):** ACCEPT clause: transcribed VERBATIM and correctly (docs/FABLE_DELIVERY_PROMPT.md:2036-2043). Every claimed-existing path checked — all 14 exist. Three claimed-missing facts hold: agentic_core/api/ has 71 files and no vision router; native_ai.py's _CAPABILITIES has exactly 16 entries and the word "vision" does not appear in the block; no FOLLOWUPS row has slot P3.5 (FU-294's slot is P2.2, it only mentions P3.5 — as stated). The live-state verdict stands. But the estimate is HIGH by one round, because the two things it declared unmeasured both resolved in the build's favour, and they are the two things it spent round 3 on.

MEASURED REDUCTIONS (I ran the probes it did not):
1. Leg (3)'s acknowledged weak point is gone. I queried the live Ollama (0.35.0) /api/tags on this machine: every model row carries a first-class `capabilities` array (llama2 → ['completion']; llama3.2 → ['completion','tools']) AND `details.families`. A vision model reports vision there, so leg (3) computes from a capability FIELD, not the "known-vision-model name list intersected with local_models()" fallback the e

- *Unverified:* I did not run the ~53-minute suite, so there is still no MEASURED timing for this item — the same gap the estimate declared. Round sizing leans on the remembered median (2.51h/round, suite ~36%).
- *Unverified:* That a pulled vision model reports the literal token "vision" in /api/tags `capabilities`. I verified the FIELD exists and its shape on three installed models (llama2, llama3.2, llama3.2:1b — all completion/tools); no vision model is installed on this machine, so the token itself is strong inference from Ollama 0.35.0'
- *Unverified:* Whether a refuter or the owner would ACCEPT a Pillow deterministic metadata read as satisfying leg (1)'s "reads an attached image into text". It satisfies the written bar literally and non-vacuously; whether it satisfies the item's intent (usable content from a diagram or screenshot) is a judgement I cannot settle, and

---

### P3.6 — 5 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables):
(1) useT reaches the hubs, DomainTool, Settings and the avatar — asserted by the surfaces reading the
    translation, not by the helper existing;
(2) an AI output in a requested language is HONOURED by the owned model, or LABELLED as not delivered in
    it: a guard drives a language the model cannot serve and asserts the label, since the defect is
    silent English;
(3) the 12-language list is trimmed to what actually HAS a dictionary, computed from the dictionaries
    present — a hard-coded list of twelve fails this whatever it contains.

**Live state:** PARTLY DONE — one of three legs is ~70% there, the other two are at zero, and leg 2 has a live second-writer defect I found while measuring. The item's central premise is NOT disproved; everything it names exists.

LEG 1 (useT across hubs/DomainTool/Settings/avatar) — NOTHING EXISTS. `grep "useT()"` over apps/workstation-superapp/src returns exactly four files: lib/i18n.tsx (the definition), components/layout/Sidebar.tsx:165, pages/DashboardNew.tsx:360-file, pages/domains/DomainsHub.tsx. None of the six domain hubs, nor QEPReligionHub, nor DomainTool.tsx, nor Settings.tsx, nor any avatar component reads a translation. Settings.tsx:6 imports coverageFor and applyDocumentDirection but NOT useT, so Settings DESCRIBES the translation it does not use. This exactly matches R5.7's own refuted-and-SURVIVED evidence in docs/VISION_FIDELITY_LEDGER_v3.md:648 ("useT() is consumed by exactly three pa

**Already satisfied:** roughly 0.7 of 3 deliverables. Leg 2 (honoured-or-labelled) is ~70% done: the backend condition, the note, the avatar label and two driving guards all exist and pass (agentic_core/avatars/api.py:451/:455, ConversationPanel.tsx:131, test_mvp_spine.py:24171-24214 and :19493-19496) — what is missing is the VSBCockpit second writer and the unexercised honoured branch. Leg 1 is 0% (useT reaches 3 of 13 target surfaces, and 0 of the 4 the item names). Leg 3 is 0% (12 hard-coded in userPrefs.ts:20-32, 

**Paths the body names that DO NOT EXIST:** ["frontend/ \u2014 there is no frontend/ directory at the repo root. The React app is apps/workstation-superapp/. An implementer reading 'useT across hubs/...' and grepping frontend/src finds zero hits and could wrongly conclude nothing exists.", "any frontend test runner \u2014 no vitest/jest/testing-library anywhere in apps/workstation-superapp/package.json, so the ACCEPT clause's 'asserted by the surfaces reading the translation' cannot be a component test; it has to be a python source-reading guard in integration_tests/test_mvp_spine.py (the pattern already used at :19490)."]

**Blocked by:** ["NOT blocked. Nothing here waits on an owner decision \u2014 the in-house dictionaries, the local owned model tier (ratified in the 2026-09-27 rulings) and the browse", "One scope question the planner (not the owner) should settle before the round starts: does 'useT across the hubs' mean the hubs' CHROME (headers, tab labels, CT", "One judgement call inside leg 3: ACCEPT (3) says 'trimmed to what actually HAS a dictionary', but the same 12-entry LANGUAGES list also supplies the BCP-47 code"]

- **Surprise:** A LIVE DEFECT, found while measuring, in the exact class ACCEPT (2) exists to prevent: apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx:373 sets `language_requested: r.data.language ?? null, language_honoured: r.data.language ?? null` — both from the SAME backend field. Because agentic_core/avatars/api.py:451 returns `language=None` precisely when the language was NOT honoured, the two fields go null together and the `requested && !honoured` condition is unreachable by construction. And grep shows neither field is rendered anywhere in that file. So the Cockpit's 11-language 'Response language' select
- **Surprise:** Settings.tsx DESCRIBES a translation it does not itself use: it imports coverageFor and applyDocumentDirection at :6 and prints an honest, runtime-computed coverage sentence at :135-147, but it never imports useT, so the page explaining the translation is one of the English-only pages.
- **Surprise:** THREE independent hard-coded language lists, not one. userPrefs.ts:20-32 (12 BCP-47 entries), useAvatarSession.ts:49-51 (_LANG_NAMES, 12 entries), and VSBCockpit.tsx:1305 (11 AI-response names). The Cockpit list includes Swahili, which appears in NO dictionary and in NO other list in the repo — it can only ever produce silent English. Trimming userPrefs.ts alone satisfies nothing.

**Verifier (OVERTURNED):** The ACCEPT clause is transcribed verbatim, all 25 paths exist, the archive confirms legs 1 and 3 are genuinely at zero, and the VSBCockpit second-writer defect is real — but the estimate undercounts leg 1. It misses 23 JSX-fragment descriptions that t() structurally cannot carry (translate() returns a string; i18n.tsx has no markup interpolation), and it contradicts itself by excluding the long honesty prose while counting the toolRegistry lever whose descs ARE that prose — a registry of 26 entries, not 24. Dictionary sizes are 90 each, not 64-90 (the 64 is a known line-anchored undercount R5.7 repeated). Leg 2 also needs new JSX, not a tweak: the Cockpit renders no label at all. 4 → 5 rounds at the chrome-plus-registry scope, which is the scope the ACCEPT clause's "reaches" bar actually requires.

- *Unverified:* "396 unique candidate visible strings" — not reproducible: the extractor lives in their scratchpad, not the repo. My own comment-stripped JSX-text-node + prop-literal pass over the same 13 files gives 408, with per-file drift (their ReligionHub 74 vs my 70, EmploymentHub 64 vs 68, CareHub 57 vs 51, QEPReligionHub 21 vs
- *Unverified:* "~120-140 new keys, ~480-560 new dictionary entries" — a judgement about a scope nobody has fixed; unverifiable in either direction until the chrome-vs-bodies decision is written down.
- *Unverified:* "the three surfaces already done needed 33 t() calls" — I count 29 literal-key t('…') call sites (DashboardNew 17, DomainsHub 12); Sidebar keys nav by id so no regex can count it. 33 is plausible, not reproduced.

---

### P3.7 — 4 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables):
      (1) a file/zip endpoint serves an entity's repo, driven by fetching a real file and a real zip and
          asserting the bytes are the repo's;
      (2) the tree is clickable and its preview links resolve from the Cockpit — a link that 404s fails this,
          and a raw anchor to a user-scoped route is the D-BEARER class: it 401s the moment auth is on;
      (3) the entity's products are listed on the marketplace WITH §12 pricing, and a product with no price
          says so rather than showing a default;
      (4) an entity with no repo is said to have none, never shown as an empty tree.

**Live state:** PARTLY DONE — the backend plumbing around the repo is mature, the four ACCEPT legs are not. Measured:

(1) FILE/ZIP ENDPOINT — ABSENT. agentic_core/api/vsb.py declares 29 routes (grep '@router'); the repo ones are POST/GET /{vsb_id}/repo, POST/GET /{vsb_id}/repo/ship, POST /{vsb_id}/repo/cascade. GET /{vsb_id}/repo (vsb.py:435-456) returns the MANIFEST only — "tree": sorted paths, "files": [{path, bytes}] — never a byte of content. No zipfile import exists in the whole backend. The three nearest routes, GET /{vsb_id}/website|webapp|mobile/page/{name} (vsb.py:714, :915, :1053), serve real HTML but are hard-limited to a four-name allowlist {index, about, solution, styles} out of one fixed subdir (vsb.py:718) — they cannot serve BUSINESS_PLAN.md, genome.json or compliance/QUALITY.md. So leg (1) is 0% built, though the store it must read is real: data/vsb_repos holds 295 repo directories, e.

**Already satisfied:** 0 of 7 deliverables fully satisfied; 3 are partly in the tree already — the "no price says so" wording and its computed counts (LivingMarketplace.tsx:387-393, :405, :414), the bearer-safe preview helper the links must use (lib/download.ts), and the API-level "no repository generated yet" refusal (vsb.py:440). Measured, not inferred: the file endpoint, the zip endpoint, the clickable tree, the Cockpit's repo read and the per-entity marketplace filter are each 0%.

**Paths the body names that DO NOT EXIST:** ["No route matching repo/file, repo/zip, repo/download, repo/tree or repo/archive exists anywhere in agentic_core/ or apps/workstation-superapp/src/ (Grep, zero matches)", "No zipfile/ZipFile import exists anywhere in agentic_core/ (Grep, zero matches) \u2014 the zip half has no mechanism at all", "No vsb_id query filter on GET /api/v1/marketplace/listings (marketplace.py:284-299 takes category, search, certified_only only)", "No marketplace call from any page under apps/workstation-superapp/src/pages/enterprise/ (Grep 'marketplace', zero matches) \u2014 the Cockpit never reads the entity's listings"]

**Blocked by:** ["SOFT, and worth the Owner's attention: unruled owner decision 3.6 (FABLE_DELIVERY_PROMPT.md:1968-1969, listed under P3.0 OWNER RULINGS) proposes to \"block deliv", "NOT blocked by anything else I could find: ruling 3.9 \u2014 the finding this item carries (FABLE_DELIVERY_PROMPT.md:558-561) \u2014 is a measured gap, NOT an owner rulin"]

- **Surprise:** The item names ZERO file or directory paths. Every target is named by concept ("§13 repo", "the Cockpit", "the marketplace", "§12 pricing"), so the named-path-does-not-exist failure mode cannot bite here — but it also means nothing in the body pins the work to a file, and I resolved all four surfaces myself and checked each.
- **Surprise:** ACCEPT leg (3)'s second half is ALREADY SATISFIED and nobody recorded it against this item. W444 and W491 did exactly "a product with no price says so rather than showing a default": LivingMarketplace.tsx:414 prints '—' not a number, :405 badges "unpriced — not for sale", and :387-393 prints a COMPUTED count of unpriced vs priced-but-held. marketplace.py:261 leaves price_wst=0.0 with the comment "unset, not free — nobody has priced this". Whoever builds this item must not re-do it, and the guard for leg (3) should assert the existing behaviour plus the new filter.
- **Surprise:** ACCEPT leg (2)'s stated hazard is already engineered away for the sibling surfaces. lib/download.ts was written (W338/W343) precisely because raw anchors 401 under auth, and GenesisJourney already previews website/webapp/PWA through openExport. The clause reads as an open risk; it is a solved pattern waiting to be applied.

**Verifier (OVERTURNED):** ACCEPT transcribed VERBATIM (docs/FABLE_DELIVERY_PROMPT.md:2054-2065, all four legs match). All 7 claimed paths exist. All 4 "missing" claims TRUE including _archive/ (zero Grep matches repo-wide for repo/file|zip|download|tree|archive; no zipfile in agentic_core/; GET listings takes only category/search/certified_only at marketplace.py:284-299; zero marketplace refs under pages/enterprise/). Every cited line checks out: vsb.py:271, :435-456, :440-441, :718, :295-330; marketplace.py:64/:261/:302-317/:603-620; LivingMarketplace.tsx:387-393/:405/:414; GenesisJourney.tsx:1025/:1052/:1081/:1112; test_mvp_spine.py:1319-1326/:1368/:2927-2941. Archive holds nothing recoverable (only _archive/jules-phase2/src/organism/python/utils/bundler.py, a tribunal-bundle zip writer over a documents list writing to disk — not a repo-serving endpoint).

TWO DEFECTS IN THE BASIS, both found by measurement:

(1) Leg 1's specified guard is UNSATISFIABLE BY CONSTRUCTION. The basis says a leg can "assert the zip's namelist equals manifest['tree']". But `tree` is built from `written` at vsb.py:414, and `(root/

- *Unverified:* "295 real repo directories with real files on disk" — 295 directories confirmed, but only 81 hold a manifest, so GET /repo can read 81 not 295; against the entity store only 19 of 219 are readable. The phrase overstates the readable population by 3.6x and framed the no-manifest case as one example rather than 37 of 219
- *Unverified:* The cited 53-minute suite time — I did not run the suite, so the per-round suite cost is taken from the basis and memory, not measured here.
- *Unverified:* "in this repo a frontend truth leg with a non-vacuous blind has reliably consumed a full round" — a pace claim from prior rounds I did not independently reconstruct from the journal.

---

### P3.8 — 5 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W509 from this item's own deliverables):
      (1) each ruling named here (3.5, 3.6, 3.10, 3.11) is implemented AS RULED, with the ruling quoted beside
          the change — an implementation that departs from its ruling is the defect;
      (2) the §4.5 shape is fixed: a lifecycle field that only ever holds its FINAL value is replaced by one
          that holds the state it is in, driven by asserting an intermediate state is observable;
      (3) no ruling is implemented before it is ruled: an unruled item keeps saying so.

**Live state:** NOTHING of P3.8 exists, and the premise of its most expensive branch is already disproved.

(A) ALL FOUR RULINGS ARE STILL UNRULED. docs/FABLE_DELIVERY_PROMPT.md:154-158 ("STILL WITH THE OWNER") lists the single lifecycle (3.10), whether §17.1's Products axis is built or amended (3.5) and whether §17.5's KPI gate is built or amended (3.6); row 3.11 at :571-581 says its attestation half CLOSED W449 and "the wording half stays P3.0". P3.0 (:1965-1979) is the item that PUTS all four to the Owner and is not done. The twelve rulings of 2026-09-30 (:1644-1701), the four of 2026-09-29 (:1702-1756) and the three of 2026-09-28 (:1770-1790) touch none of these four. So ACCEPT(1) has nothing it can be checked against yet, and the whole of leg 1 is 0 of 4.

(B) THE §4.5 SHAPE (ACCEPT 2) IS UNFIXED AND I MEASURED IT. Over data/vsb_entities, 219 of 219 records hold stage='commercialise', scope='commer

**Already satisfied:** 0 of 4 named deliverables fully; 1 of 4 partly. Leg 1 (four rulings as ruled) 0 of 4 — none ruled. Leg 2 (the §4.5 shape) 0 — measured 219 of 219 VSBs at stage 'commercialise' with no mover anywhere. Leg 3 (an intermediate state observable for a VSB) 0 — the mechanism exists only for projects (projects/api.py:50/:509), never for entities. Leg 4 (an unruled item keeps saying so) PARTLY — said in docs (LIVING_PLAN:300, WHOLE_VISION:740/:991) and on GET /api/v1/organism/lifecycle (organism_status.p

**Paths the body names that DO NOT EXIST:** ["configs/realms.yaml \u2014 GONE. Ledger row 2.9 and docs/FABLE_DELIVERY_PROMPT.md:112 both still say it \"still holds the drifted domain-shaped entries\"; `find . -name realms.yaml` returns nothing anywhere in the tree. The ledger evidence behind row 3.5's [R5.5] is stale on this point.", "src/organism/config/realms.yaml \u2014 absent (the ledger correctly reports sovereign_config.yaml:9 points at a file that does not exist; still true).", "agentic_core/api/genesis.py:687 and :852 \u2014 the LINE NUMBERS row 3.10 names have drifted. The two `\"stage\": \"commercialise\"` literals are now at genesis.py:1125 (the /establish entity) and genesis.py:1338 (the SSE birth path), with the matching `\"scope\": \"commercialise\"` at :1120 and :1336.", "agentic_core/api/vsb.py `_apply_derived_status()` \u2014 the comment at vsb.py:1958 names this helper as the thing that derives the status; no such function exists (grep returns only the comment). The derivation is inlined at :1983-1986."]

**Blocked by:** ["P3.0 (docs/FABLE_DELIVERY_PROMPT.md:1965-1979) must produce the rulings first. P3.8 ACCEPT(1) names 3.5, 3.6, 3.10 and 3.11; ACCEPT(3) forbids implementing any ", "Ruling 3.10 \u2014 the single lifecycle, options (A) canon five become the one gated lifecycle, (B) correct the canon, (C) NARROW: make VSB stage advance or rename i", "Ruling 3.5 \u2014 \u00a717.1 Products axis: build the grid picker feeding Genesis, or amend \u00a717.1 to \"design intent\". Owner choice; the two branches differ by roughly 2 r", "Ruling 3.6 \u2014 \u00a717.5 KPI gate: block deliverable/marketplace release until the owning VSB's objective KPIs are set and tracked, or amend \u00a717.5. Owner choice; roug"]

- **Surprise:** THE EXPENSIVE BRANCH'S PREMISE IS ALREADY DISPROVED. P3.0 offers to build §10's commercial-trio instruments "e.g. from the BMS unit-economics estimate". agentic_core/vbs/bms.py:36-51 already WITHHOLDS that verdict on purpose (W494/FU-103): the only cost input is a simulated $0.00015/Wh constant, so against the $0.01 target "it can only ever come out EFFICIENT" — one reachable branch, not a verdict. Ruling 3.11's build option cannot rest on the basis the plan names. This is the same shape as the "genuine PID regulator" case.
- **Surprise:** A CORRECT STAGE MACHINE ALREADY EXISTS IN THE REPO, on the wrong entity type. agentic_core/projects/api.py has STAGE_ORDER (:50), POST /{id}/advance (:509-553), POST /{id}/propose-advance (:557) and a real backward-advance refusal with its own W-round comment (:325-343). VSB entities, the ones the ledger counts 219 of, have no mover at all. Nobody recorded that the pattern was available — it makes ruling 3.10 option (C) roughly a 1-round build rather than new design.
- **Surprise:** AND IT HAS NEVER BEEN EXERCISED EITHER: data/projects holds 4 records, all at 'concept'. So the project pipeline's advance mechanism is correct and has never moved a project. The plan's §17.1 story of "two entry pipelines, four stage vocabularies, neither gated" understates it — one of the pipelines is gated and simply unused.

**Verifier (OVERTURNED):** The estimate's MEASUREMENTS are unusually good — I reproduced almost all of them — but the NUMBER is too low on its own branch (3 → 5), and its cheapness argument has a hole.

VERIFIED EXACTLY: ACCEPT clause transcribed verbatim (FABLE:2064, clause :2066-2071). All 15 claimed paths exist. realms.yaml absent tree-wide. 219/219 records at stage/scope/status = commercialise/commercialise/operational, zero variance. Writers at genesis.py:1120/:1125, :1336/:1338 and vsb.py:1954/:1960. No stage mover anywhere. Read paths serve the literal (_list_vsbs copies at :1626; get_vsb returns raw). _derived_status at :1406-1437 over four states, run at birth and stored. _apply_derived_status() named in the :1958 comment and nonexistent. projects/api.py STAGE_ORDER :50 / advance :511 / propose-advance :557 / backward refusal :336-341. bms.py:36-51 premise-disproved, verbatim — the strongest part of the estimate. No PRODUCTS in either taxonomy. Zero kpi reads in deliverables.py/marketplace.py. quality.py measures four of sixteen. organism_status.py:430 carries the stages_note. Zero follow-ups ride P3.

- *Unverified:* Frontend render behaviour: read from source only. I did not boot the backend or drive a browser — the same gap the estimate declared. The two render sites are unambiguous single-expression renders, so I share its confidence, but neither of us observed them.
- *Unverified:* Suite impact: I did not run pytest. Whether a stage derivation breaks existing assertions is unverified, and it is a live risk because the stage value feeds two LLM prompts (vsb.py:1178 board pack, :2205 evolve) whose generated output would change.
- *Unverified:* The post-ruling build-branch round counts (3.5 ~2, 3.6 ~1-1.5, 3.10(A) >=3, 3.11 >=2) are judgements about unbuilt work. I confirmed the ABSENCES they rest on (no PRODUCTS constant, no kpi gate reader, twelve unmeasured criteria), not the durations — and I found 3.10(A)'s basis overstated.

---

### P3.9 — 3 round(s)

**ACCEPT (as transcribed):** ACCEPT: a learner schedules 3 ayaat, reviews at q=4, and sees the interval, the e-factor and the 'a review count, not a hifz certification' basis on screen; a leaderboard ranks two seeded learners by recorded XP with its formula shown. GUARD: no route added under /qep may return a figure without a basis string.

**Live state:** PARTLY DONE — the backend is built, the screen is not, and the leaderboard does not exist at all.

SATISFIED (3 of 6 ACCEPT facts):
· "schedules 3 ayaat" — POST /api/v1/qep/hifz/schedule (agentic_core/religious_domain/api.py:506) validates the range against the real 114-surah ayah table (:517); QEPStudio.tsx:83-90 has the range form and calls it.
· "reviews at q=4" — POST /api/v1/qep/hifz/review (api.py:561) runs MemorizationEngine.calculate_next_review (engine.py:22, genuine SM-2: e-factor update, 1/6/×ef intervals, 1.3 floor, 36500-day cap); QEPStudio.tsx:249-253 renders quality buttons 0-5.
· "sees the interval" — QEPStudio.tsx:257 renders "next review in {reviewResult.new_interval_days} day(s)".

NOT SATISFIED:
· "sees the e-factor" — api.py:627 returns new_efactor, but QEPStudio's reviewResult type (line 94) declares only {new_interval_days, next_review_date, xp_awarded} and nothing

**Already satisfied:** 3 of 6 ACCEPT facts (schedule, review-at-q, interval-on-screen); 0 of the 2 named deliverables complete — memorisation UI is ~half built (flashcard/review yes, heatmap no), competitions+leaderboards 0%

**Paths the body names that DO NOT EXIST:** ["none \u2014 the body names NO file or directory path, so this item has no broken path reference (unlike the two items cited in the task). The only path-like token is the route prefix /qep, and three mounted routers serve it."]

**Blocked by:** ["NOT blocked for the ACCEPT bar. P3.0 (docs/FABLE_DELIVERY_PROMPT.md:1969-1971) states verbatim: \"A.12.1/A.12.2/A.12.5 shape P3.9's later features; A.12.4 gates ", "P3.9's REMAINDER is owner-gated on five unruled QEP rulings held in P3.0 (unruled: the plan's own counter line 792 shows P3.0 at 0 rows): A.12.1 corpus provenan", "No real-money rail, no live external AI key, no deploy and no managed Postgres is touched: SM-2 is arithmetic and an XP ranking is a sort over an existing on-di"]

- **Surprise:** A SECOND, UNREACHABLE SM-2 — WITH A WORKING HEATMAP — ALREADY EXISTS. agentic_core/reactor/religion/qep_flagship.py:88-143 reimplements SM-2 inline and computes an honest 30-day heatmap from recorded review events with heatmap_source and heatmap_recorded_since. It has NO live route: it is registered as CEO tool "qep_memorization" (agentic_core/api/v138/ceo.py:50, :109) and that file's router exposes only /ceo/meeting/log, /meeting/minutes, /chat, /vitals. docs/FABRICATION_LEDGER.md:281 confirms "no live route". This duplicate IS the private-QEP-stack shape the item forbids — wiring it would be the defect; the hea
- **Surprise:** MemorizationEngine.get_progress_matrix and recommend_hifz_path (engine.py:49, :63) have NO caller anywhere outside _archive. A progress-matrix composer is already written and unused — and hifz/progress:655 returns the raw cards dict under the key "progress_matrix" without calling it.
- **Surprise:** apps/workstation-superapp/src/components/QEPFlagshipFeatures.tsx:30 already says competitions have "no backend exists yet" while qep_flagship.py:33-36 persists two real tournaments with real participant lists. The line is inaccurate TODAY and becomes a second-writer defect the moment a leaderboard ships.

**Verifier (OVERTURNED):** TOO LOW — 3 rounds, not 2. The estimate's repo reading is near-perfect (ACCEPT transcribed verbatim vs FABLE_DELIVERY_PROMPT.md:2072-2080; 11+7+1=19 routes confirmed by grep; all four vision anchors land on their headings; hifz sessions trimmed [-200:] at api.py:607; new_efactor at :627; memorised_basis at :630/:648 and NOWHERE under apps/ — only test_mvp_spine.py:8576; QEPStudio reviewResult type at :94 declares just {new_interval_days,next_review_date,xp_awarded}; QEPStudio.tsx:230 paraphrases the basis as "memorised (>=1 successful review)"; qep_intelligence has exactly 3 "basis" occurrences across 7 routes with contributions[] keyed "rationale" at :168-183; _GAMI_STORE level_basis "1 + xp // 100" and streak_basis both present). Three things make it 3 rounds.

(1) THE GUARD IS ITS OWN ROUND. The estimate names the predicate as undefined ("needs a real definition of 'figure'") and proves a literal-keyed guard goes RED on correct code — then still budgets it inside round 1 beside two new routes. Verified no basis-coverage guard exists: the only route enumerator in test_mvp_spine.py 

- *Unverified:* Did not boot the app or run the 53-minute suite — every 'on screen' judgement is read from the JSX, same limitation the estimate declared.
- *Unverified:* Did not trace every caller of ceo.py's enclosing class, so 'the heatmap/leaderboard in qep_flagship.py are route-unreachable' rests on ceo.py's router declaring only 4 unrelated routes, not on an exhaustive call graph.
- *Unverified:* Whether the two reaching surfaces (ReligionHub tab 'qep' and QEPReligionHub) both actually render QEPStudio at runtime — asserted from the imports/JSX, not from a rendered page; per W503 a {false && ...} gate would not show in a grep.

---

### P3.10 — 2 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W508 from this item's own deliverables — and the GATE is part of the bar):
(1) curriculum content and classes ship ONLY behind the ruled scholar-review mechanism: until it is
    ruled, a guard asserts NO curriculum content is servable, driven by requesting it;
(2) the LearnTeach surface keeps saying NOT ESTABLISHED while the gate is unruled, and the guard asserts
    the words are present — the item's own instruction is that this "must not be dressed";
(3) when the mechanism IS ruled, every shipped module names the scholar review that cleared it, and one
    with no review is not servable.

**Live state:** MEASURED, not inferred. Item body is docs/FABLE_DELIVERY_PROMPT.md lines 2081-2090 (next item P3.11 at 2091); ACCEPT is lines 2084-2090.

ACCEPT (1) FAILS TODAY — curriculum content IS servable, from three live surfaces, none behind any review:
- agentic_core/api/education.py:56 `POST /api/v1/education/curriculum` — mounted at agentic_core/app_mvp.py:175 (`app.include_router(education_api.router)`), exercised green by integration_tests/test_mvp_spine.py:3856 (happy path, subject Mathematics) and :3887 (edge probe). It calls `ai_text(prompt, "education_curriculum", realm=req.realm)` and returns the generated `curriculum` text. Same router also serves /lesson-plan, /assessment, /feedback.
- apps/workstation-superapp/src/components/LearnTeachModule.tsx:28-33 — the Religion domain's own surface POSTs to that route with `subject: "Quran & Islamic Studies", level: "Intermediate", duration_week

**Already satisfied:** 0 of 3 ACCEPT criteria (1 fails — curriculum is servable from 3 live surfaces; 2 fails — the literal is absent from the named surface and present only on a different one; 3 unbuildable — no scholar-review mechanism exists). 0 of 2 titular deliverables (learning/ holds gamification only, educator/ is empty).

**Paths the body names that DO NOT EXIST:** ["religious_domain/ \u2014 NOT at the repo root; `ls religious_domain/` fails. The vision's status notes write it repo-relative (religious_domain/learning/, religious_domain/memorization/engine.py) but it lives at agentic_core/religious_domain/. This is the named-path failure mode the task warned about, present again.", "religious_domain/learning/ \u2014 same: only agentic_core/religious_domain/learning/ exists", "agentic_core/religious_domain/educator/ \u2014 the DIRECTORY exists but is completely empty (zero files, not even __init__.py), so the educator toolkit has no code whatsoever", "any live scholar-review module \u2014 no scholar_review/ScholarReview/scholar_verified/review_cleared symbol exists outside docs and _archive/", "any live ruling-state primitive \u2014 no A.12.3, OWNER_RULING, RULINGS, unruled, NOT_RULED or awaiting_ruling construct exists in any .py file"]

**Blocked by:** ["A.12.3 (owner ruling, sits in P3.0 at docs/FABLE_DELIVERY_PROMPT.md:1974-1976): curriculum ownership AND the scholar-review mechanism for AI-generated religious", "An owner/author decision on ACCEPT (2)'s wording: the criterion demands a literal ('NOT ESTABLISHED') that the named surface has never contained \u2014 it is present", "A scope decision on /api/v1/qep/tajweed/lesson: it already ships AI-generated religious instructional content with a disclaimer. If 'curriculum content' covers "]

- **Surprise:** The item's body names ZERO file or directory paths — no path to check. Everything measurable had to be resolved through the A.6 f5/f6 and A.12.3 cross-references. That is itself a defect in the item: there is nothing in it to grep against.
- **Surprise:** The item reads as pure future work ('ships ONLY behind the ruled mechanism'), but the breach it exists to prevent is ALREADY LIVE AND SHIPPING. The Religion domain's own LearnTeach surface asks a generic AI curriculum designer for 'Quran & Islamic Studies' curriculum and renders the result — AI-generated religious content reaching a user with no scholar review, which is the exact thing A.12.3 blocks. ACCEPT (1) is a regression check, not a greenfield build.
- **Surprise:** ACCEPT (2) is unmeetable as written, and the surface it names is MORE honest than the criterion. The W508 author merged two surfaces: vision A.6 f5 records LearnTeach saying 'No scholars are verified on this deployment'; 'NOT ESTABLISHED' is f7's QEP-intelligence compliance-audit wording. This is the W505 class again — a criterion worded against output that is already correct.

**Verifier (OVERTURNED):** FIGURE SURVIVES, BASIS DOES NOT. 2 rounds is right for the ruling-independent legs, but the stated plan would burn a round on its own wrong seam. Three measured errors.

WHAT VERIFIED (all of it, not a spot-check):
ACCEPT transcribed EXACTLY — FABLE_DELIVERY_PROMPT.md 2081-2090, P3.11 at 2091, confirmed word for word. education.py:56 POST /curriculum; app_mvp.py:175 mounts it; spine 3856 (Mathematics, green) and 3887 (edge probe); religious_domain/api.py:697 /tajweed/lesson with query_meta at 717; qep_flagship.py:212 fixed syllabus; _ai_provenance.py 78 lines with the realm directive at the seam; LearnTeachModule.tsx 124 lines, POSTs subject "Quran & Islamic Studies" and contains NO "NOT ESTABLISHED" — it says "No scholars are verified on this deployment" and "No class roster exists on this deployment"; the literal lives ONLY at QEPIntelligence.tsx:12 and :224, zero .py; ReligionHub imports LearnTeachModule at 10, renders at 117, does not import QEPIntelligence. educator/ is empty of even __init__.py. 11 routes in religious_domain/api.py, none for classes. Zero live ruling-state or s

- *Unverified:* gamification.py "47 lines" — confirmed present at 2121 bytes, not line-counted
- *Unverified:* the 53-minute suite figure — not run this pass; consistent with the recorded ~36% of a 2.51h median round
- *Unverified:* the post-ruling 6-10 round range for ACCEPT (3) + f5/f6 — agreed unmeasurable, correctly excluded

---

### P3.11 — 4 round(s)

**ACCEPT (as transcribed):** ACCEPT (written W508 from this item's own deliverables — A.8's own economic model):
(1) the QEP VSB's waterfall is configured as the Waqf/Trust instance A.8 describes and NOT the generic
    template: a guard asserts its proportions differ from the default, because inheriting the template
    is the defect;
(2) free at point of use for individuals, institutions at cost+5%, surplus cap ≤5% — each driven with a
    figure that would BREACH it and asserted to be refused;
(3) a Zakat-eligible charity channel and Sponsor-a-Student both exist and are reachable, and a
    contribution through either is recorded against the entity's books;
(4) the eight-attribute executive board (A.8) is the Religio

**Live state:** PARTLY DONE — the machinery exists, none of the configuration does. 1 of 9 deliverables holds.

ALREADY THERE (measured):
- §12 waterfall machinery is real and tested. agentic_core/economy/entities.py holds 9 ENTITY_TEMPLATES including `waqf` (capital_preserved, charity 0.30) and `trust`; DEFAULT_ENTITY = "waqf_ltd_hybrid" whose waterfall is _DEFAULT owner .20 / self .30 / capital .20 / users .15 / charity .15. agentic_core/economy/metabolism.py:51 validate_waterfall normalises + bounds a proposal; GET/POST /api/v1/economy/waterfall (agentic_core/api/economy.py:393, :498) read/write a per-vsb_id override store (data/economy_waterfall_overrides.json, path at metabolism.py:38), UEG-logged, and integration_tests/test_mvp_spine.py:4742 already drives the override end to end. So ACCEPT (1)'s mechanism is free; only the QEP configuration is missing.
- A real per-VSB double-entry ledger exists 

**Already satisfied:** 1 of 9 deliverables — and that one (virtual WST, no real-money rail) is a standing platform invariant (REAL_MONEY_ENABLED = False, agentic_core/economy/owner_payments.py:35), not work this item did. The other 8 are absent. Infrastructure for 4 of them (waterfall config, board composition seam, entity establishment, ledger postings) is already in place, which is why this sizes at 3 rounds rather than 6.

**Blocked by:** ["WHICH legal form the QEP VSB records is effectively irreversible by design, so it must be decided BEFORE the entity is established: POST /api/v1/economy/entity-", "WHAT counts as \"cost\" in cost+5% is a definition only the Owner/spec can fix. The ledger records exactly two cost-side accounts (agentic_core/economy/ledger.py:", "Adding a NEW entity-form template with its own bounds (the `waqf_trust` option, and the surplus-cap rule inside validate_waterfall) is a code_change, which agen", "NOT buildable and correctly out of scope: the QEP vision's \u00a714 Stripe billing, institutional invoicing and real donation processing (docs/QURAN_EDUCATION_PLATFO"]

- **Surprise:** ACCEPT (1)'s wording admits a reading that would let the defect through. It says the proportions must "differ from the default". If the QEP VSB records `waqf` and inherits waqf's own template waterfall unchanged, it differs from _DEFAULT (waqf_ltd_hybrid's owner .20/self .30/cap .20/users .15/charity .15) while still being a generic template verbatim — which is precisely what the clause's own next words call the defect ("because inheriting the template is the defect"). The guard must assert the QEP waterfall differs from BOTH entities.py's _DEFAULT AND from its own recorded form's template waterfall, or the bar p
- **Surprise:** The default vsb_id of GET /api/v1/economy/waterfall is "workstation-idbo" (agentic_core/api/economy.py:394) and NO such entity exists in the entity store — _load_vsb('workstation-idbo') returns nothing. The route still answers, falling back to the template. So there is no precedent in this repo of a seeded, named, first-class VSB; the QEP VSB has to be established like any other, and the guard must drive that establishment rather than observe ambient state.
- **Surprise:** All 36 registered living entities carry the SAME form, `waqf_ltd_hybrid` — not one of the 9 templates has ever been exercised in the live registry. The 9-template system is live code with a single real user.

**Verifier (OVERTURNED):** ACCEPT transcription is EXACT (docs/FABLE_DELIVERY_PROMPT.md:2096-2107, all five clauses verbatim). All 20 claimed paths exist; missing-paths [] is correct. The measurement is unusually strong on facts — I confirmed _DEFAULT (.20/.30/.20/.15/.15) at entities.py:15, 9 ENTITY_TEMPLATES incl. waqf (capital_preserved, charity .30) and trust, validate_waterfall's exactly-two rules at metabolism.py:65-68, the override store at metabolism.py:38, test_mvp_spine.py:4742 = test_economy_waterfall_owner_sovereignty driving the override end to end, ledger.py operating_costs:308 + net_profit_wst computed from real postings + post:401/record:439, EstablishRequest's domain+entity_type, _register_living at genesis.py:1182, enrich_vsb_entity(vsb.py:1670) carrying domain, board_for_owner(board.py:198) ignoring it, /board/status?scope= reading the stored board, REAL_MONEY_ENABLED=False, _BOARD as ONE 8-row constant with "religion" appearing zero times in board.py, _relevant_directors:587 + its exact-set assertion at test_mvp_spine.py:1770, living_vsbs.json = 36 entities ALL waqf_ltd_hybrid with ZERO rel

- *Unverified:* The 53-minute suite runtime — I did not run the suite (memory's ~36% of a 2.51h median round is consistent, so I treat it as plausible rather than measured here)
- *Unverified:* That POST /api/v1/economy/waterfall actually accepts a Waqf/Trust proportion set for the chosen template — not executed; validate_waterfall's bounds (capital_fund>0 for waqf/trust) read as satisfiable but were not driven
- *Unverified:* Whether the heartbeat economy lever being off (living_statement's W475 note) affects a contribution posting into the per-VSB ledger for clause (3) — not traced

---

### P3.21 — 1 round(s)

**ACCEPT (as transcribed):** ACCEPT: each of the three verdicts is reachable and asserted; a withheld output states which check failed; no float is read as a verdict anywhere in the chain.

**Live state:** NOTHING for this item exists. A grep for "P3.21" and "P3.22" across every .py in the tree returns NO MATCHES — the verifier is greenfield, and so is the index it reads. No agentic_core/horizon, /fabric, /knowledge or /index directory exists (checked with ls).

THE BODY NAMES ZERO FILE PATHS — unusually for this plan, there is nothing to catch out. It names three code SHAPES by description instead. I resolved and checked all three:
(1) "a quality pipeline that starts at 0.90 and adds 0.05 per iteration without reading the content (on the BME item)" = agentic_core/quality/vrpr_pipeline.py, 26 lines: line 10 `it, curr, conf, trace = 0, draft, 0.90, {}`, line 13 `if val.passed and conf >= 0.95: return await self._polish(...)`, line 22 `conf += 0.05`. REAL and LIVE — agentic_core/avatars/core/recirculation_orchestrator.py:22 imports it, line 76 instantiates it. It is registered as FU-233 and 

**Already satisfied:** 0 of 4 deliverables. No citation check, no three-state verdict over a citation, no withhold and no float-free citation contract exists. But 1 of the 3 float shapes the body cites is already remedied (the consultation contract), and 2 reusable precedents exist (the MET/UNMET/NOT_ASSESSABLE vocabulary in api/method.py, the per-check verdict record in clearance_chain.py).

**Paths the body names that DO NOT EXIST:** ["agentic_core/horizon/", "agentic_core/fabric/", "agentic_core/knowledge/", "agentic_core/index/"]

**Blocked by:** ["NOT BLOCKED. docs/NATIVE_AI_FABRIC_ROADMAP.md:143 gives P3.21 an empty 'Blocked by' column; P3.23 is the one that depends on P3.21 and P3.22, not the reverse.", "SOFT, and avoidable: the body says a citation must 'resolve to a document in the index', and that index is P3.22, which does not exist (no agentic_core/knowledg", "FU-272 (Owner decision: may the platform index the live legal matter's documents) does NOT block this item \u2014 it is slotted to P3.23 and gates the archive half o"]

- **Surprise:** The body names ZERO file paths — so the known failure mode (an item citing a path that moved or was deleted) cannot bite here. It names three code shapes by description, and all three resolve to real locations I checked.
- **Surprise:** ONE OF THE BODY'S THREE PREMISES IS ALREADY FALSE, in the good direction. 'a consultation contract that REQUIRES a float, which is why every implementer returns 0.96' — agentic_core/consultation/interface.py:71 now has `confidence: Optional[float] = Field(default=None, ...)` with a `confidence_basis`, and its docstring records the fix. The item body is stale on this point and should be corrected before the round starts, or someone will 'fix' what is already fixed.
- **Surprise:** THE REAL FLOAT DEFECT IS ONE THE BODY DOES NOT MENTION: `class Citation` at agentic_core/consultation/interface.py:35-39 carries a REQUIRED `confidence: float` and NO location field. A citation that must carry a confidence number and cannot carry the line it came from is the exact inversion of what P3.21 asks for, and it sits inside the consultation contract the body praises as 'the engine item'. This is the item's cheapest and highest-value fix.

**Verifier (OVERTURNED):** TOO HIGH by one round. The measurement's facts are unusually clean — 16/16 paths correct (12 exist, 4 missing), the ACCEPT clause transcribed VERBATIM from docs/FABLE_DELIVERY_PROMPT.md:2229-2230, and live_state "nothing exists" is TRUE even against _archive/, which the measurement did not check and I did: no archived .py contains NOT_ASSESSABLE or a withhold, and the archive's only citation validator is _archive/agentic_core/domains/law/sovereign_validator_v19_1.py:22 `validate_citation(filename, page, hash_provided) -> bool` — a hardcoded dict of five SHA-512 hashes over the Owner's real case PDFs returning ONE bool, no location, no verdicts, and part of the fabricated law corpus, so it must not be recovered. But the measurement UNDERCOUNTED the free precedents and priced the piece it missed into round 2. It named two (method.py:45-47/242/246-346 MET/UNMET/NOT_ASSESSABLE with per-requirement bases and block-on-UNMET-only; clearance_chain.py:61-62 verdict+basis with a third not_evaluated state — both confirmed). There are at least four: THE WITHHOLD ALREADY EXISTS TWICE — agentic_co

- *Unverified:* The ~53-min suite cost, which is the single biggest lever on this estimate. I confirmed integration_tests/test_mvp_spine.py is 29,362 lines and 486 tests but did NOT run it. The measurement admits the 53-min figure is the plan's own, not today's — and the commit cadence argues against it: W524 (1h09) and W525 (1h00) ea
- *Unverified:* Whether the Owner reads clause 3's 'anywhere in the chain' as the citation->verify->withhold path (my reading, giving 1 round) or as agentic_core/avatars/core/clearance_chain.py (giving 2, because gate 4's `_risk > 0.15` at line 196 would come into scope). OWNER DECISION — flag it at the top of the round rather than gu
- *Unverified:* Whether agentic_core/mjm/recursive_meta_learner.py:53 `return 0.96  # Based on MJMOrchestratorV4.consult confidence` falls under clause 3. Confirmed present and still hardcoded; it is a learner self-report with no verdict role today, so I read it as out of scope, but it shares the ambiguity above.

---

### P3.22 — 3 round(s)

**ACCEPT (as transcribed):** ACCEPT: a passage without a resolvable location cannot be cited; the index reports what it did not read and why; nothing unread is in the knowledge base (the FU-124 rule).

**Live state:** NOTHING OF THIS ITEM EXISTS. Item body is docs/FABLE_DELIVERY_PROMPT.md lines 2231-2238 (next item P3.23 starts at 2239, so the body is exactly 8 lines and I read all of it).

NO INDEX MODULE EXISTS. `ls` of agentic_core/fabric, agentic_core/horizon, agentic_core/knowledge, agentic_core/index: all four "No such file or directory". Grep for size_cap|file_cap|scan_bounds|EXCLUDED|NOT_READ|id_rsa|exclusion across **/*.py returns 8 files, and the only two non-archive hits (agentic_core/api/integration_surface.py:227, agentic_core/api/method.py:724) are unrelated prose. There is no bounded repo scanner, no recorded-exclusion list, no per-file three-state over a scan, no lexical index, no citation graph, no passage-location store. data/ holds 37 json files and data/genomes/ (entity genomes from organism/genome.py, e.g. genome-036e0f5b3e.json), not an asset index.

WHAT IS GENUINELY REUSABLE (m

**Already satisfied:** 0 of 10 deliverables built. 1 of the 3 ACCEPT legs (leg 3, the FU-124 unread rule) has working code and a driven guard — but on the UPLOAD surface only, so it is satisfied vacuously for an index that does not exist.

**Paths the body names that DO NOT EXIST:** ["agentic_core/fabric/ \u2014 checked with ls, No such file or directory", "agentic_core/horizon/ \u2014 checked with ls, No such file or directory", "agentic_core/knowledge/ \u2014 checked with ls, No such file or directory", "agentic_core/index/ \u2014 checked with ls, No such file or directory", "C:\\Users\\rehan\\Desktop\\ \u2014 DOES NOT EXIST AT ALL; the Desktop is OneDrive-redirected to C:\\Users\\rehan\\OneDrive\\Desktop. Any implementation that resolves ~/Desktop would scan nothing and could report full coverage over zero files.", "app_mvp.py at the repo root \u2014 it is at agentic_core/app_mvp.py (P3.25's body names it bare; not this item's problem but the same naming hazard)", "pypdf \u2014 absent from the venv AND absent from requirements.txt entirely (grep returns nothing), despite FU-269's ruling to install it", "python-docx \u2014 in requirements.txt:213 but NOT importable in this interpreter (pip show: 'Package(s) not found'); `import docx` fails"]

**Blocked by:** ["NOT owner-gated, and the body's '(gated)' is STALE. FU-268 ('may the platform read the four desktop archives') is status 'done', owner_gated false, closed_by W5", "P2.13 IS UNBUILT and P3.22 says it SHARES P2.13's scan bounds, secret rules and three-state. P2.13 carries no DONE marker (only P3.12/P3.13/P3.14/P3.15 are mark", "FU-296 (open, slot P2.13, owner_gated false) \u2014 install pypdf + python-docx. This gates ONLY the 9 .docx + 5 .pdf book files and the 4 p3 .docx. It does NOT gate", "A SCOPING DECISION THE BODY DOES NOT ADDRESS, and the one thing I would escalate: does the index cover _archive/ and products/Law/? Grep for 'Simulated content "]

- **Surprise:** THE BODY NAMES ZERO FILESYSTEM PATHS. Eight lines, and the only backticked token is the required literal `embeddings: none installed`. Every path in scope is inherited by reference through P2.13. So the usual 'body names a path that does not exist' failure mode cannot occur here — but the item also gives an implementer no home for the module, which is why I checked four plausible ones (all absent).
- **Surprise:** C:\Users\rehan\Desktop DOES NOT EXIST. The Desktop is OneDrive-redirected to C:\Users\rehan\OneDrive\Desktop. HORIZON_INTEGRATION.md writes the four folders as '…\Desktop\X' with a leading ellipsis, so the doc is not strictly wrong — but an implementation resolving ~/Desktop or %USERPROFILE%\Desktop finds nothing, and a scanner that walks an absent root reports zero files read, which this platform's own discipline says must be an absent-with-reason, not a clean pass.
- **Surprise:** THE OWNER GATE IS ALREADY OPEN AND THE PLAN DOES NOT SAY SO. P3.22 says '(gated) the Owner's archives', and P2.13's body still ends 'BLOCKED BY the Owner's answers on reading the folders at all and on installing a docx/pdf extractor'. Both FU-268 and FU-269 were RULED 2026-09-27 and closed W505. The plan bodies are stale against the register — the opposite of the usual direction, and it means P3.22 has been carried as blocked while being buildable.

**Verifier (estimate stands):** 3 ROUNDS STANDS, but the risk is in the WRONG ROUND and five sub-claims are wrong.

WHAT I VERIFIED (all of it holds):
- ACCEPT clause transcribed VERBATIM. docs/FABLE_DELIVERY_PROMPT.md:2231-2238, P3.23 at 2239 — exactly 8 lines, as claimed.
- Live state empty, INCLUDING _archive. agentic_core/{fabric,horizon,knowledge,index} all absent. Grep of _archive for inverted_index|citation_graph|knowledge_index|lexical|bm25|tf_idf hit 5 files and all are prose ("lexical_divergence" scores in digestion/ and novelty_assessor.py) — no index implementation anywhere. "NOTHING OF THIS ITEM EXISTS" is TRUE.
- Every spot-checked path exists at the claimed line: app_mvp.py:98 ingestion mount; config.py atomic_write_json:73, read_json_strict:130, store_lock:282, data_path:379; ingestion/api.py _pdf_docx_extractor:37 + the four fields declared at 66-69; test_mvp_spine.py:21262-21294; hallucination_sandbox.py:61 no-op docstring; knowledge_synthesis.py _embed returns []; requirements.txt:34 chromadb==1.5.5 and :213 python-docx==1.2.0 (both exact).
- Package premise exact: sentence_transformers/neo4j/who

- *Unverified:* "Each round is ~1.5h of real work after the 53-min suite" — I did not run the suite. Neither the 53-min figure nor the work/suite split is measured here; stored context corroborates ~36% of a ~2.51h median round, but that is not my measurement.
- *Unverified:* Escape hatch (a) — whether the Owner wants the index to carry a provenance state for fabricated content. An Owner decision, unverifiable by reading the repo. Related open row FU-272 is unslotted.
- *Unverified:* The exact 714 count of "Simulated content for" — I reproduce 700 across 10 files inside _archive and did not search outside it, so the remaining 14 may or may not exist elsewhere.

---

### P3.26 — 5 round(s)

**ACCEPT (as transcribed):** ACCEPT:
      (1) a LINEAGE field exists on an entity and is written by whatever creates it: a guard drives a
          creation and reads the parent back, and an entity with no parent says so rather than showing null
          as though it were an answer;
      (2) an entity state machine with juvenile · mature · senescent · dormant · retired, where DORMANCY is
          self-service (it stops consuming and operating, reversibly, and costs nothing) and DEATH is
          governed through Change Control — a guard drives dormancy and asserts the beat stops operating it;
      (3) APOPTOSIS CONSERVES: what a retired entity held returns to the reservoirs and its RECORD is
          retained — a

**Live state:** PARTLY DONE: the primitives exist, the mechanism does not. 1 of 7 clauses already holds; 6 are absent. Measured:

CLAUSE 1 (lineage) — ABSENT. I loaded all 219 records in data/vsb_entities/ with a script: 219 have vsb_id + generation + status + realm + domain; ZERO have parent, parent_vsb_id or lineage. A sample record (data/vsb_entities/vsb-000b75b0c4.json) carries generation: 0 and no parent. There are FIVE establish writers, not one: four funnel through enrich_vsb_entity (agentic_core/api/vsb.py:1670, called from genesis.py:1354, synthesis_studio.py:326 and :416, vsb.py:1974), but the BLOCKING genesis establish at agentic_core/api/genesis.py:1115-1135 builds its record inline and does its own board/economy/register enrichment (genesis.py:1163-1193) without calling enrich_vsb_entity — a one-place fix misses it (the W475 every-writer class). Note synthesis_studio keys its records by ent

**Already satisfied:** 1 of 7 ACCEPT clauses (clause 6, true by construction but with no guard); 0 of the other 6

**Paths the body names that DO NOT EXIST:** ["(no path is named in the item body, so none could be mis-pointed; the referents that DO NOT EXIST are conceptual, not paths: a stored entity constitution, a QEP VSB entity, a persisted ruling-to-entity reference, and any retire-or-relabel mechanism in code)"]

**Blocked by:** ["NOT blocked by P3.14 \u2014 SATISFIED. agentic_core/avatars/core/clearance_chain.py:16-34 and :103-112 carry the P3.14 per-gate verdicts and the block-on-absence cha", "OWNER DECISION (blocks clause 4 closure, not the build): which entity is \"the QEP entity\"? None exists \u2014 0 of 36 roster entries in data/living_vsbs.json and 0 o", "OWNER DECISION (blocks clause 4 closure): what is the durable \"named in a ruling\" reference? _rulings at agentic_core/api/council_judiciary.py:66 is an in-memor", "OWNER DECISION (blocks clause 5 closure): what IS the inheritable \"constitution\"? Nothing stores one. agentic_core/api/vsb.py:1165-1171 derives `constitutional`"]

- **Surprise:** The item body names NO file or directory path at all — so nothing in it could be mis-pointed, but equally every clause had to be resolved against code by reading rather than by checking a path.
- **Surprise:** Clause 6 (MEIOSIS) is already TRUE by construction and nobody recorded it: crossover_genomes writes only to data/genomes/ via _save_genome (agentic_core/organism/genome.py:39,74-77), nothing anywhere establishes an entity from a crossover, and the route has no caller at all — not in agentic_core, not in the frontend. It needs a guard, not a build.
- **Surprise:** Clause 5's central premise is partly disproved — the same shape as the "genuine PID regulator that does not exist" failure. It plans to inherit a constitution VERBATIM, but no entity stores a constitution; agentic_core/api/vsb.py:1160-1171 derives it at read time from the entity's own challenge, so a child's derived constitution can never equal its parent's.

**Verifier (estimate stands):** THE NUMBER STANDS AT 5, but its basis holds one verified-FALSE claim and two accounting errors that happen to offset. I defaulted to finding it wrong and could not.

VERIFIED TRUE (everything I checked at the stated line numbers): ACCEPT clause transcribed word-for-word against docs/FABLE_DELIVERY_PROMPT.md:2287-2314 — no misquote. All 23 claimed paths exist. C1: 219 records, keyset has vsb_id/generation/status/realm/domain on all 219 and ZERO parent, parent_vsb_id, lineage, constitution or life_stage; five establish writers confirmed — enrich_vsb_entity defined vsb.py:1670, called at vsb.py:1974, genesis.py:1354, synthesis_studio.py:326 and :416, while the BLOCKING genesis /establish (route at genesis.py:1073, a function that ends before 1275) builds its entity inline at 1113 and never calls enrich — /establish/stream at 1276 is a separate function, so the one-place fix really does miss it. C2: 36 roster entries, exactly one distinct status "living"; operate_one (living_vsbs.py:414+) filters only on isinstance(vsb_id, str) and reads no status; the tie-break sorts by (last_operated, 

- *Unverified:* I did not run the 486-test suite — no figure for current green/red state or runtime, and the measurement did not either.
- *Unverified:* Clause 2's full surface cost beyond VSBEconomy.tsx: I enumerated which of 19 frontend pages touch vsb_id/generation but did not read each page's rendering to price displaying five life stages.
- *Unverified:* Whether the two owner decisions (build a QEP entity; allow a ruling to reference an entity) would be answered in-round — a scheduling risk I priced but cannot verify.

---

## What this does NOT establish

- **A size is not a schedule.** Six of these (P2.11-P2.16) are held behind the cognitive-engine items by
  the Owner ruling at `docs/FABLE_DELIVERY_PROMPT.md:1757`, and P3.16-P3.19 are still open. Sized is not
  eligible.
- **Seven are owner-gated** and cannot be planned as buildable without a decision.
- **The numbers are projections, not measurements of work done.** Each rests on a reading of the tree that
  was correct when taken; a later round changes the tree. Re-measure before committing to any of them.
- **Each item's `unverified_claims` list is part of its figure.** Where an agent could not check something,
  it said so, and those gaps are reproduced above rather than smoothed away.
