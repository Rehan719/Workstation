# V44 ROUNDS PREP - the rounds after the v44 assessment (W1194-W1232)

Dated 2026-11-22, written by W1193 from a read-only design pass made the same day. A WORKING PLAN, not a claim the work is done: the register (`docs/FOLLOWUPS.json`) and the plan (`docs/FABLE_DELIVERY_PROMPT.md`) stay the authority, and where this document and the tree disagree, the tree is right and this document is wrong. Section 35 of `docs/INSTRUMENT_CELL_BRIEF_ASSESSMENT.md` is the assessment it comes from.

The pass had four planners, one for each group of rounds, a refuter for each planner, and one agent that bundled and ordered the rounds. READ EACH ROUND'S REFUTATION BEFORE BUILDING IT: three of the thirty-six verdicts were SOUND; 33 designs are printed below (the two record-round plans and D-CANVAS are not), each as its planner wrote it, followed by what its refuter found and the fixes it asked for. The schedule and each round's heading already carry the lead's rulings on those fixes; the plan text beneath them does not.

ANSWERED ON THE MORNING OF 2026-11-22 (W1193c), the text below kept as it was written: the Owner accepted the six recommendations as they were put in chat at 03:04 UTC ("I accept all six recommendations, proceed", 07:25 UTC): the five listed under What goes to the Owner in chat, worded for the chat, and a sixth, from the re-measurement of the remaining work, on when the final audit runs. Where the words put in chat differ from the five below, the words put in chat govern, and W1193c recorded those: chromadb is to be removed from the dependency list once the retired memory is removed, the same way the unused streamlit, plotly and pandas packages were taken out, with a full test run on a fresh install, and the re-checks of test_w583 L5 and test_w907 stay this plan's notes, not the ruling; the two legal-form descriptions are to be reworded to say what each template models, the nine names kept and the old words kept in a dated note, and the example wordings and the note's place in section 2 stay this plan's proposal, not the ruling; and the business plan's dated note also says that the 20% goes to each entity's own owner. The answers are recorded at P3.32 (chromadb), P5.18 and FU-1868 (the two descriptions), P4.2 and FU-1817 (retention and erasure), in the canvas (its credit line's note), in the business plan (the fee and the owner's share, under Concept) and at P5.22 and FU-1086 (the final audit). W1230 (A3b) and W1231 (C5b) are no longer held on the Owner (W1230 still follows W1196, W1231 W1216); W1193c made W1232's canvas note and the business plan's dated amendment, which no round held, so W1232 is not to be built. W1200 is to keep FU-1086's ruling of the morning of 2026-11-22, and P5.22's BUILT line is to say the audit runs in December; and W1216 leaves FU-1868 open, which W1231 closes.

## Honest status of this document

| fact | value |
|---|---|
| Dated | 2026-11-22, by W1193, against the tree as W1192 left it: W1191 landed as 7b93affe, and W1192 after it. |
| Read at | The design read the tree at 89c25eed (W1190), read-only: no suite, container or network was run. Every line number and state verdict below is as read there. W1191 changed the release machine's startup script, the deploy guide and the sign-in module, and W1192 the plan, the register and nine documents, so re-read each cited line before building on it. |
| Numbering | W1192 is the round that recorded the Owner's twenty decisions of 2026-11-22. That moved the record round to W1193, its rows to FU-1841 onward and the builds to W1194. Where a plan below says W1192 registers a row, read W1193, and the row id given in the round's heading. |
| The business plan | Unamended. W1192 amended only the ratified canvas, on the Owner's word, and gave the vision's section 12 and the economic model dated notes; whether the business plan's Concept bullet, which already names each enterprise's own owner, gains the platform's 25% of profit, taken first, is put to the Owner in chat. Where a plan below says W1192 amends the business plan, it did not. Answered on the morning of 2026-11-22 (W1193c): on the Owner's word the business plan's Concept bullet gained a dated note, its earlier words kept: the platform's 25% fee comes first, and 20 parts in a hundred of what remains go to each entity's own owner. |
| Rounds planned | 35 by the four planners: A 12, B 9, C 9, D 4, plus the record round, which all four planned in parts. The bundled schedule holds 43 designs. Nine were added from the refutations and the bundle: A3b, B5b, B10, D-RETURN, D-GATE, D-CREDIT, D-TERMS, C5b and CANVAS-CREDIT. One was superseded: D-CANVAS, which W1192 already does. |
| Plans judged sound by their refuter | 3 of 36 verdicts: A4, A12 and B4. 31 NEEDS_FIXES. 2 UNSOUND, both re-planned here: A3, and the record round as cluster D planned it. |
| Wrong state verdicts found | 33 listed by the refuters (A 11, B 10, C 6, D 6). 32 hold. The one that does not is cluster D's 'W1191's W729 row is unconfirmed': the working tree has it as FU-1837 (OWNER, high). |
| Guard legs that could not fail | 13 legs, in 12 findings. Another 8 legs would fail on a correct change. 3 legs hold a state that the Owner's rulings of 2026-11-22 replaced: A3's legs 3 and 4, and the record round's leg D. |
| Bar demands the plans missed | 69: A 21, B 19, C 17, D 12. The refuters also named 10 missing rounds: A 1, B 2, C 2 (both folded into C1 and C5), D 5. |
| Sum of the estimates | The planners sized the work at 38.5 rounds. Their refuters re-sized the same work to about 40: B1, B3, C5 and C6 at 1.5; B5 at 2; C1 at 1.25; C4 batched into C3. With the nine added designs, and without D-CANVAS, it is about 44.5. |
| Bundled schedule | 40 numbered rounds, W1193 to W1232, after W1192: 37 unheld (W1193-W1229) and 3 HELD (W1230-W1232). Four numbers carry bundles, each checked disjoint in code and page files: W1200, W1201, W1204 and W1207. C8, B7 and B8 take two numbers each. This is a floor, not a forecast: B1, B3, C5 and C6 were re-sized to 1.5 rounds but hold one number each. Answered on the morning of 2026-11-22 (W1193c): W1230 and W1231 are no longer held, and W1232 is not to be built (W1193c made its note). |
| Rounds HELD on the Owner | 3: A3b (chromadb's declaration), C5b (the two approved legal-form descriptions) and CANVAS-CREDIT (the ratified canvas's credit line). Answered on the morning of 2026-11-22 (W1193c): none is held on the Owner now; W1230 still follows W1196 and W1231 W1216, and W1232 is not built (W1193c made the note). |
| Rows the record round registered | 49. The bundle's 43, FU-1841 to FU-1883: one of them the Owner's (FU-1882, the Quran Foundation developer account), and one, the round protocol (FU-1877), registered and closed by W1193. And six found by the completeness critic of the re-measurement of the fifteen open plan items, FU-1884 to FU-1889, each checked at 89c25eed before it was registered; they have no round here yet. Four of the bundle's rows have no closing round in this schedule: the unlocked-write census (FU-1851), the local platform's CORS default (FU-1855), the DPIA draft (FU-1883, P5.8's own rounds) and the developer account (the Owner's act). |
| Owner questions | None from before is open: the Owner answered the fourteen of 2026-11-21 and the v40 questions on 2026-11-22, and W1192 recorded the answers. No OWNER question row is registered. Five questions go to the Owner in chat, listed below. Answered on the morning of 2026-11-22 (W1193c): the Owner accepted them as put in chat, with a sixth on the final audit (the note at the head says where the words differ). |

THE ROUND COUNT IS A FLOOR, NOT A FORECAST. Four refuters re-sized their rounds upward, and each round's own refutation below is the size to build from.

## Before the schedule

- W1192 recorded the Owner's twenty decisions of 2026-11-22 at the items they govern, amended the ratified canvas on the Owner's word, and registered FU-1838 (the scholar), FU-1839 (the channel and price tests, with three deferred measures) and FU-1840 (the lessons sitting).
- W1193 wrote section 35 and the standing answer for the "digital mitochondria" line, registered the rows above, put the developer account on the Owner's list and in the local notes, applied the corrections this schedule left to it, and wrote this document.

## The schedule

| round | keys | title | held on |
|---|---|---|---|
| W1194 | C1 | The Law draft form drafts only the templates it lists: any other id, a reserved instrument among them, is refused before anything is composed, and routed to where a solicitor can be found | W1193 (the row) |
| W1195 | C7 | A reserved instrument asked for in a listed template's instructions or parties, or named as the clerk's template, is refused and routed; the Law page says which documents are reserved | W1194 (same files) |
| W1196 | A3 | The avatar and upload memory the Owner retired is removed: nothing writes it, nothing fetches a model for it, and the delete answer says what may remain elsewhere | W1193 |
| W1197 | A1 | The composition preview computes the gate's verdict and records nothing; POST /compose and PUT /compositions/{cid} still seal | W1193 |
| W1198 | B2 | An account is removed by a command run over SSH that reads the users store whole, never by editing users.json by hand | W1191 landed (set_password.py's pattern, step 12) |
| W1199 | D-SCHOLAR-REQUEST | The request to a scholar or trusted institute is drafted for the Owner to send, naming everything withheld now | W1192 (FU-1838) |
| W1200 | C3, C4, D-FU1086 | The plan says what is held and what was built: PLAN NOW names the hold on P5.22, a test holds the optimiser's queue disclosure, FU-1086 says what remains, and P5.22 records W970-W977 | W1193 |
| W1201 | D-FIRST-OFFER, D-GATE, C2 | Before the teacher interviews, the first-offer papers say the Domain tool is free; the seventh gate reads the Owner's bar; the business guard reads row status and counts money however it is written | W1193 (the map, the cost model's cell and the brand screen are restated first) |
| W1202 | B1 | Through the SSH tunnel no page from another site acts on the platform: an Origin check on writes and on the stream socket, and a Host allowlist, keyed on a setting only the release machine passes | W1191 landed; W1198 first (DEPLOYMENT.md) |
| W1203 | A11 | A model becomes the serving default only when an administrator promotes an evaluated build whose licence text the runtime holds | W1193 |
| W1204 | D-TERMS, D-CREDIT | What the Owner ruled on 2026-11-22 is said where it is read: an entity repository says no terms have been chosen, and the generation credit carries forward | W1193 |
| W1205 | A5 | The document-control registry appends one record per version, reads its store whole or refuses, and says when a version was not kept | W1197 (quality.py), W1204 (vsb.py) |
| W1206 | A6 | A store read tolerantly into an object is never written back from it: the QMS refuses its write, and the guard watches the attribute door | W1205 (the DCMS must already read strictly) |
| W1207 | A4, B4 | The archive says its index uses no embedding; every entity route with a second path parameter answers a second person as no entity | W1193 |
| W1208 | B9 | The privacy screen reads git history for credentials, read-only, and says where a shallow walk stopped | W1193 |
| W1209 | A2 | The fabric preview says a composition runs one stage at a time, and what the org cascade is granted, instead of 'fits' or 'over capacity' | W1197 (resource_fabric.py) |
| W1210 | A7 | Every duration the platform records is read from a monotonic clock | W1196, W1197, W1203, W1205, W1209 (shared files) |
| W1211 | A8 | An attempt the caller abandons is recorded once, as abandoned, spends what it ran, and counts against no model | W1210 (gateway.py starts), W1196 (ceo.py) |
| W1212 | A9 | The run history, the Learning Loop and the work budget say that a run whose process ended before it finished left no outcome of its own and spent nothing | W1210, W1211 |
| W1213 | A10 | Two composition runs finishing together both reach the history: the completed-run write takes the store's lock | W1212 |
| W1214 | B3 | The work budget says its figure is the platform's wherever it is read, lists every reader, and the brief's limits and the guide's switches are held to the code | W1198 and W1202 (DEPLOYMENT.md), W1209 and W1212 (ResourceFabric.tsx, work_budget.py) |
| W1215 | B10 | With the throttle on, admission and every reader of the energy figure read the platform's total until a second person runs work, then each run's own chain, as the Owner ruled | W1214 |
| W1216 | C5 | Wherever a founder chooses or sees an entity's legal form, the platform says in one wording that no company is formed, nothing is registered and no liability is limited | W1205 and W1210 (vsb.py), W1214 (VSBEconomy.tsx, VSBCockpit.tsx) |
| W1217 | C6 | One journey establishes one entity: a repeat from the same journey, including the page's own fallback after a cut stream, is answered with the first entity and creates nothing | W1216 (genesis.py, GenesisJourney.*) |
| W1218 | B5a | With sign-in on, a founder instructs their own entity's Chief through an entity-scoped route grounded in the entity's own record; the apex Board stays the administrator's | W1210 (board.py), W1216 (VSBCockpit.tsx, vsb.py) |
| W1219 | B5b | With sign-in on, a founder reads their own entity's Board and sees their entity's own work-budget figure, and no one else's | W1218 |
| W1220 | C8 | The read census, part 1: every mounted GET and every declared preview is called on a fresh data root, as nobody and as a reader; the five reads that advance the simulator and the registry read are fixed | W1197 (the preview), W1214 and W1215 (capital_fund.py, organism_status.py), W1216 (economy.py), W1219 (its new GETs walked) |
| W1221 | C8 | The read census, part 2: what its first run found beyond the named instances is fixed, or carried as a defect entry on an open row | W1220 |
| W1222 | C9 | A reading route answers what is stored and never runs a model: the change impact and the portfolio forecast compose only on a write | W1221, W1210 (products.py) |
| W1223 | B6 | The platform measured under the release machine's caps, the gateway's pacing reported apart, from a committed raw record the guard recomputes | W1214 (the brief's part 7). It needs Docker on the round's machine. |
| W1224 | D-RETURN | The return measurement the Owner scheduled is built as a pre-flight of the invited stage: how many people come back, counted across people only | W1198 (the users store's command); before W1225 (so the retention register lists its store) |
| W1225 | B7 | Every store says whether a person's data reaches it, in which fields, what of it is kept by rule, and that its period is the Owner's (part 1: the enumerator and the register) | W1196 (memory_v01 gone), W1198, W1223 (the brief), W1224 |
| W1226 | B7 | The retention register is held true by a canary drive (part 2) | W1225 |
| W1227 | B8 | An administrator's erasure of one made-up person (part 1: erase() and the command over SSH) | W1226, W1198 |
| W1228 | B8 | The erasure driven end to end and read back (part 2), and the brief's part 8 restated | W1227 |
| W1229 | A12 | TopologyDefense reports no repair it did not make: simplicial_repair is deleted, as its ledger rule says, and _interrupt_agent is recorded as latent | Ordered last by the lead ruling |
| W1230 | A3b | HELD - chromadb's direct declaration, which brings onnxruntime, is dropped once nothing imports it | The Owner's answer to the chromadb question (in chat), and W1196. Answered on the morning of 2026-11-22 (W1193c): no longer held; still after W1196 |
| W1231 | C5b | HELD - the two approved legal-form descriptions say what each template models | The Owner's answer to the template question (in chat), and W1216. Answered on the morning of 2026-11-22 (W1193c): no longer held; still after W1216 |
| W1232 | CANVAS-CREDIT | HELD - the ratified canvas's credit line gains a dated note for the carry-forward ruling, the earlier words kept | The Owner's answer to the canvas question (in chat). Answered on the morning of 2026-11-22 (W1193c). Not built: W1193c made the note |

Each round's files, `-k` selector, rows and design follow, in order.

## W1194 - C1: The Law draft form drafts only the templates it lists: any other id, a reserved instrument among them, is refused before anything is composed, and routed to where a solicitor can be found

**Closes:** The template-id door of the law.py defect (P5.18 clause 4), and its row

**Owning item:** P5.18 clause 4 and its ACCEPT

**Held on:** W1193 (the row)

**Rows:**

- FU-1866 (P5.18, medium): A reserved instrument is drafted under any template id the generator does not list

**Files:** agentic_core/legal/specialist.py; agentic_core/api/law.py; docs/COVERAGE_REGISTER.json; scripts/coverage_register.py

**-k:** -k "p518_a_reserved_instrument_is_refused or test_w714_ or test_endpoints_no_500_on_edge_inputs or test_law_ or test_forms_a_composition_calls_a_domain_form or test_domain_tools_reachable_in_house or test_w642_ or test_p3a_r1_ or test_w825_ or test_w866_ or test_w996_ or test_w1170_ or test_registers_a_named_source or test_w953_ or test_w1081_ or test_w1083_ or test_w711_ or test_w1187_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- reserved_reason is built only from lsa-2007-sch2's names, page, read_on and not_read, never its 'says'. 'says' names two Acts that no source row holds, and test_registers... needs names_with_no_row == [] (P5.11 clause 6). The reason lists what was not read (clause 8), and a leg runs the authorities screen over the reserved block.
- Two separate sentences. UNLISTED_REASON (listing the drafted templates) is given for every unlisted id. A 'what this generator refuses' line never says the asked id is reserved, and agrees with the deed hold.
- scripts/coverage_register.py gains an optional, checked field naming the suite test that guards a route_only row. It is used on law-reserved-instruments, so that P5.18's ACCEPT ('a row naming the test') holds.
- P5.18's UPDATED line says only that the template-id door is closed, and that the instructions, the parties and the clerk are W1195's.
- There are 30 Law rows, not 29.
- The row carries slot_source.

test_w714 leg 2 is changed on purpose.

### C1 as planned (cluster C; size S, 1 round(s))

**Title:** The Law draft form drafts only the templates it lists; any other id, a reserved instrument among them, is refused before anything is composed and routed to where a solicitor can be found

**Closes:** law_py_defect, the template-id door of P5.18 clause 4. Closes the W1192 row 'A reserved instrument is drafted under any template id the generator does not list'.

**Owning item:** P5.18, clause 4 and its ACCEPT 'the reserved documents are refused through the route a person would use' (FABLE:7431-7435, 7449-7450).

**Owner-gated:** No. The reserved kinds are clause 4's own words, as read in source row lsa-2007-sch2. Whether a particular deed is reserved stays the qualified person's reading: the W714 hold is unchanged.

**Depends on:** W1192 registers the row. It comes first in this cluster's order because it closes a reserved-activity hole and is small.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | POST /api/v1/law/generate drafts any template_id it does not list, through a generic prompt | agentic_core/api/law.py:403-407: base_prompt = _TEMPLATE_PROMPTS.get(req.template_id, f"Draft a comprehensive {req.template_id.replace('_', ' ')} agreement under {req.jurisdiction} law. ..."). Only FILING_SHAPED (389-396) and the deed hold (398-402) refuse first, so 'land_transfer', 'tr1' or 'contract_for_sale_of_land' reach ai_text. |
| EXISTS | _TEMPLATES lists ten ids but _TEMPLATE_PROMPTS holds four, so three listed templates already draft from the generic text | law.py:38-49 lists ten ids (nda … data_processing_agreement). law.py:51-81 has prompts only for nda, employment_contract, service_agreement and privacy_policy, so terms_of_service, ip_assignment and data_processing_agreement must keep drafting. |
| EXISTS | The deed hold reads words, never substrings | agentic_core/legal/specialist.py:35-39: 'deed' in re.split(r'[^a-z]+', tid). HELD_FOR_A_QUALIFIED_READ is at :28 and HELD_REASON at :29-33. |
| ABSENT | A refusal for the land instruments clause 4 names | No code names the Land Registration Act or a transfer or charge. The only reserved-activity text is the deed hold (specialist.py:25, :29). |
| EXISTS | The reserved kinds have been read at their publisher, and there is a place to send a person | docs/SOURCES.json row lsa-2007-sch2 (read whole on 2026-11-20, W1148). Para 5(1): preparing an instrument of transfer or charge for the purposes of the Land Registration Act 2002, and making an application or lodging a document for registration under it. Para 5(3)-(4): an instrument includes a contract for the sale or other disposition of land, except a contract to grant a short lease. Row help-gov-find-legal-advice (read 2026-10-13) is served by GET /api/v1/law/help (where_help.py:48-50). |
| PARTIAL | FU-1076 recorded clause 4 as met | docs/FOLLOWUPS.json:21545 slot_source says 'it is the item's fourth clause met in existing code', but its close note covers only the deed hold (W714). The land instruments were never refused. |
| EXISTS | The fabric's form passes a free template_id to the same handler | agentic_core/api/resource_fabric.py:538-557 (form_law_generate, handler generate_document, template_id 'str'). test_forms_a_composition_calls_a_domain_form_through_its_own_door holds that the same door gives the same answer (62543-62545). |
| EXISTS | The Law page offers only listed ids and draws the held block | LawHub.tsx:244 offers a select from GET /api/v1/law/templates, falling back to the ten listed ids. It draws the held block at :234-237 (data-testid law-templates-held). |
| EXISTS | test_w714 leg 2 expects an unlisted id to draft | integration_tests/test_mvp_spine.py:65589-65594: 'indeed_agreement' answers 200, and sent == ['law_generator', 'law_generator']. |
| ABSENT | A coverage-register row for reserved documents | docs/COVERAGE_REGISTER.json has 29 Law rows and none for reserved instruments; law-draft is 'frame'. scripts/coverage_register.py check() requires a route_only row to name a route and refuses one that names a test. |
| EXISTS | The clerk assembles any template id | specialist.assemble (149-185) composes no text but labels and stores an artefact under any id. Tests post nda (test_w610, 46231) and witness_statement (test_w816, 72026). This door is left to C7. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- A reserved instrument is drafted under any template id the generator does not list (P5.18, medium)

**Rows it closes:**

- The row above, closed as built in this round. FU-1076 stays done: its deed hold is unchanged and still guarded by test_w714. W1192 adds a note to it.

**Changes:**

- agentic_core/legal/specialist.py: RESERVED_INSTRUMENTS: the four kinds in clause 4's words, each naming source row lsa-2007-sch2. reserved_reason(): one sentence built from that row's page and read_on through the sources-register reader the time limits use, never typed. It says preparing these is reserved to authorised persons and that a solicitor can prepare one, points to GET /api/v1/law/help, and ends with NOT_LEGAL_ADVICE. UNLISTED_REASON. HELD_REASON and held_for_a_qualified_read are unchanged.
- agentic_core/api/law.py: In generate_document, after the filing-shaped and deed checks and before any prompt is built, a template_id that is not a listed id answers 404 with UNLISTED_REASON followed by reserved_reason(). The generic prompt is kept only for a listed id with no prompt of its own. list_templates gains a 'reserved' block (kinds, reason, source) beside 'held'.
- docs/COVERAGE_REGISTER.json: New row law-reserved-instruments: Law, 'England and Wales', route_only, route help-gov-find-legal-advice. Its 'today' text: the draft form drafts only the templates it lists; any other id is refused before anything is composed, with the kinds Schedule 2 names and where a solicitor can be found; a deed is held (W714).
- docs/FABLE_DELIVERY_PROMPT.md: Under P5.18, after the OWNER RULING 2026-11-21 line, an UPDATED line: clause 4's reserved documents are refused at the draft form and the fabric's form, with the guard named; the free-text door and the clerk are C7's row. The substrings test_w711 and test_w1187 read are kept.
- docs/FOLLOWUPS.json: Close the row as built.
- integration_tests/test_mvp_spine.py: The new guard, and test_w714 leg 2 changed on purpose.

**Guard:** test_wXXXX_p518_a_reserved_instrument_is_refused_at_the_draft_form_before_anything_is_composed

- Each reserved kind posted as an id is refused with 404: 'transfer_of_registered_land', 'tr1', 'legal_charge_over_land', 'contract_for_sale_of_land' and 'land_registry_application'. The detail carries reserved_reason() and names GET /api/v1/law/help, and a spy on law.ai_text records no call. FAILS IF: The generic fallback answers an unlisted id (200, with a prompt sent), or the refusal comes after composing.
- Ordinary unlisted ids ('indeed_agreement', 'wXXXX_made_up') are refused the same way, and the detail does not contain the deed hold's 'is held and is not generated here'. FAILS IF: The refusal is keyed on reserved words instead of the list, or the deed hold fires on a substring.
- Every listed template that is neither filing-shaped nor held still drafts (200, the captured text), including terms_of_service, ip_assignment and data_processing_agreement. FAILS IF: The round refuses listed templates, for example those missing from _TEMPLATE_PROMPTS.
- The fabric's form_law_generate with 'tr1' is refused with the route's own status and detail, and its output is None. FAILS IF: The runner reaches a door that composes.
- GET /api/v1/law/templates carries 'reserved' beside 'held', and its reason names lsa-2007-sch2's page and read_on. With the sources reader monkeypatched to return another read_on, the reason follows it. FAILS IF: The block is missing, or the reason is a typed copy.
- The law-reserved-instruments row is route_only, its route is a row of docs/SOURCES.json, and coverage_register.check() reports no problem. FAILS IF: The row is absent, names a test, or names no route.

**Blinds:**

- Restore the _TEMPLATE_PROMPTS.get(req.template_id, f'Draft a comprehensive ...') fallback and drop the unlisted refusal. -> Legs 1 and 2 answer 200 and a prompt is sent.
- Refuse only ids containing 'land' or 'transfer'. -> Leg 2 goes red because the ordinary and made-up ids draft; leg 1 goes red on 'tr1'.
- Move the unlisted refusal below the ai_text call. -> Leg 1's no-call spy records a call.
- Refuse every id that has no entry in _TEMPLATE_PROMPTS. -> Leg 3 goes red: three listed templates are refused.
- Type the read_on date into the reason instead of reading the source row. -> Leg 5's monkeypatched date is not followed.

**Pins:**

- test_w714_a_deed_is_held_until_a_qualified_person_has_read_the_schedule (65589-65594): for tid in ("nda", "indeed_agreement"): ... assert r.status_code == 200 and r.json()["document"] == "w714 captured" ... assert sent == ["law_generator", "law_generator"], sent -> Change on purpose. Keep held_for_a_qualified_read(tid) is False for both ids, since the property this leg holds is that the hold reads words. 'nda' still drafts. 'indeed_agreement' is now refused as unlisted (404) and its detail must not say 'is held and is not generated here'. Expect sent == ['law_generator'], with a comment saying why.
- test_w714_a_deed_is_held_until_a_qualified_person_has_read_the_schedule (65596-65597): held["templates"] == ["partnership_deed"] and held["reason"] == _sp.HELD_REASON -> Unchanged. The new 'reserved' block sits beside 'held'.
- test_endpoints_no_500_on_edge_inputs (4115): ("/api/v1/law/generate", {"template_id": "nonexistent", "parties": {}}) -> Unchanged. It now answers 404, which is still below 500.
- test_law_a_filing_shaped_document_has_one_door_and_no_prompt_claims_a_role_or_a_forecast (60993-60995): listed ids that are not filing-shaped and not held -> 200 and 'w-law captured' -> Unchanged.
- test_forms_a_composition_calls_a_domain_form_through_its_own_door (62543-62545): _g["refused"] is True and _g["status"] == _p.status_code == 409 -> Unchanged (et1_claim).
- test_w711_the_two_chartered_items_keep_their_boundaries_and_every_source_says_what_was_not_read (65413-65425): P5.18 charter substrings, including 'are refused and routed' -> Kept. The UPDATED line only adds text.
- test_w1187_the_owners_five_decisions_of_2026_11_21_are_recorded_and_the_calibration_holds_three_of_them (98018-98025): P5.18 clause 4's finance-product ruling text -> Kept.

**Rulings it rests on:**

- P5.18 clause 4 and its ACCEPT (FABLE:7431-7435, 7449-7450): reserved documents are refused and routed, through the route a person would use.
- P5.18 clause 8: the reason names lsa-2007-sch2 and the day it was read, and states nothing beyond that row's words.
- OWNER RULING 2026-10-13 (W714, FU-1076): a deed is held until a qualified person has read the Schedule. Unchanged.
- OWNER RULING 2026-11-21 (FU-1817): no named finance product is compared. Untouched.
- P5.18 BOUNDARY: no public release without the qualified person's view (FU-1817). Nothing is released.
- W1172 and W953: the platform says it is not a solicitor, and the one page of where help is serves as the route.

**Risks:**

- The reason may say only what lsa-2007-sch2 says. Para 5(2)'s fee condition is not in the row, so the sentence says the activity is reserved, never that drafting here is an offence.
- A route_only coverage row cannot name its test, so clause 4's 'row naming the test' is met by the plan's UPDATED line and the row's close note.
- The free-text door (instructions on a listed template) and the clerk stay open until C7, and the row says so.

### C1's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'docs/COVERAGE_REGISTER.json has 29 Law rows' is wrong: there are 30 Law rows of 84 (counted over rows with domain == 'Law'). The rest holds: the fallback at law.py:403-407, the ten listed ids with four prompts, the deed hold reading words (specialist.py:35-39), no code naming the Land Registration Act or a transfer or charge (grep of agentic_core finds none), the fabric form at resource_fabric.py:538, test_w714 leg 2 at 65589-65594, and the clerk accepting any id (specialist.assemble 149-184).

**Guard legs that could not fail:**

- None. Leg 3 repeats test_law_a_filing_shaped_document_has_one_door... at 60993-60995, but it is live against the 'refuse ids with no prompt' blind.

**Pins the plan missed:**

- test_registers_a_named_source_has_a_row_and_a_claimed_journey_names_its_test asserts _real['names_with_no_row'] == [] (test_mvp_spine.py:62492-62493). The sources scan reads agentic_core .py and .json with the pattern '(?:[A-Z][A-Za-z']+ )+Act (?:19|20)\d{2}' (SOURCES.json 'scan' and 'patterns'). lsa-2007-sch2's 'says' names the Land Registration Act 2002 and the Law of Property Act 1925, and neither has a row of its own. If the apply types either name into specialist.py or law.py, this test goes red. It is in the -k, but the plan does not list it against that string.

**Conflicts with a ruling:**

- P5.18 ACCEPT (FABLE:7447-7448) requires 'each built clause has a row in the coverage register naming the test that drives its journey'. coverage_register.check() reports a non-journey row that names driven_by as a problem, and route_only needs 'route'. So the route_only row cannot satisfy the ACCEPT. The plan's workaround, an UPDATED line naming the guard, is not the register row the ACCEPT asks for.
- P5.11 clause 6 (DONE, FABLE:7077-7079): 'no named authority is shown unless it resolves against a held source'. A reserved_reason built from the row's 'says' would show Acts that no SOURCES row holds. The only nearby rows are 'Law of Property (Miscellaneous Provisions) Act 1989 s.1' and 'HM Land Registry Practice Guide 8'.
- W714 (OWNER RULING 2026-10-13; HELD_REASON at specialist.py:29-33 says 'This is a hold, and says nothing about whether this particular deed is reserved'). Appending reserved_reason to every unlisted id, such as 'nonexistent' or 'employment_handbook', reads as a finding that the document asked for is reserved. A deed of transfer still gets the deed hold's 'says nothing about whether...' while clause 4 says such deeds are reserved; this needs one consistent sentence.
- Numbering: the row is registered by W1193, not W1192 (cluster input owner_decisions_2026_11_22).

**Bar demands the plan missed:**

- P5.18 clause 8 (FABLE:7444-7446): 'what was not read is listed as not read'. lsa-2007-sch2's not_read is 'Schedule 3 (exempt persons); who is entitled, under section 13'. The reason and the 'reserved' block carry only page and read_on, and leg 5 checks only read_on.
- ACCEPT 'refused through the route a person would use'. The Law page offers only listed ids (LawHub.tsx:244, with a fallback to the ten). A person reaches a reserved instrument only through custom_instructions or parties (law.py:409-424). The planned UPDATED line, 'refused at the draft form and the fabric's form', overstates what C1 does until C7 lands.

**Fixes asked for:**

- Give coverage_register.py an optional checked field for refusal rows, for example 'guarded_by' on route_only/excluded, required to be a suite test. Use it on law-reserved-instruments and extend leg 6. Otherwise record a dated ruling that clause 4's row is route_only with no test.
- Build reserved_reason from the row's names, page, read_on and not_read only, and never from its 'says'. Add a leg that runs legal.authorities.screen over the reserved block (no Act withheld) and asserts not_read appears. Follow the monkeypatched reader.
- Keep two sentences: UNLISTED_REASON, which lists the drafted templates, for every unlisted id; and a separate 'what this generator refuses' line, which never says the asked id is a reserved kind.
- Word the UPDATED line as 'the template-id door is closed; the instructions and parties door and the clerk are C7's'.
- Fix the count to 30. List docs/WORKSTATION_IDBO_LIVING_PLAN.md and add test_w469 to the -k. Carry slot_source on the P5.18 row. Depend on W1193.

**Re-sized:** S, 1 round (plus a quarter round if the coverage-register field is added here).

## W1195 - C7: A reserved instrument asked for in a listed template's instructions or parties, or named as the clerk's template, is refused and routed; the Law page says which documents are reserved

**Closes:** The free-text and clerk doors of the law.py defect, and their row

**Owning item:** P5.18 clause 4

**Held on:** W1194 (same files)

**Rows:**

- FU-1867 (P5.18, medium): A reserved instrument asked for in a listed template's instructions or parties is drafted, and the clerk labels an artefact with any template id

**Files:** agentic_core/legal/specialist.py; agentic_core/api/law.py; scripts/screen_phrasings.py; apps/workstation-superapp/src/pages/domains/LawHub.tsx; apps/workstation-superapp/src/pages/domains/LawHub.test.tsx; apps/workstation-superapp/src/pages/domains/LawHub.fixture.json

**-k:** -k "p518_a_reserved_instrument or test_w714_ or test_w580_ or test_w1167_ or test_w610_ or test_w816_ or test_w821_ or test_w825_ or test_w996_ or test_w1142_ or test_w1014_ or test_law_a_filing_shaped or test_forms_a_composition_calls_a_domain_form or test_w462_ or test_w469_" plus vitest LawHub.test.tsx

**Notes from the lead:**

Moved up next to C1. The Law page offers only listed ids, beside 'parties' and 'custom_instructions' fields (LawHub.tsx:241-246), so free text is the door a person would actually use.

Refuter fixes applied:
- C1's rules for the reason apply here.
- test_w580 drives only four screens. The new guard therefore drives the RESERVED list itself and asserts its results.append line in screen_phrasings.main() (W1167's pattern).
- The answer and the row say that the screen routes what it recognises and clears nothing, and that the studio and synthesis generators are not screened.
- The LawHub case waits as test_w1014 requires.

### C7 as planned (cluster C; size S, 1 round(s))

**Title:** A reserved instrument asked for in a listed template's instructions or parties, or named as the clerk's template, is refused and routed, and the Law page says which documents are reserved

**Closes:** The free-text and clerk doors of P5.18 clause 4. Closes the W1192 row 'A reserved instrument asked for in the instructions of a listed template is drafted, and the clerk labels any id'.

**Owning item:** P5.18 clause 4, and its ACCEPT that refusal comes through the route a person would use: on the page, that is a listed template with typed instructions.

**Owner-gated:** No.

**Depends on:** C1 (same files: law.py, specialist.py, test_w714).

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The instructions and party values reach the prompt unscreened | law.py:409-423 appends custom_instructions and parties to the prompt, and person_said passes them as the person's words. |
| EXISTS | The clerk accepts any template id | specialist.assemble (149-185). Tests post nda (test_w610, 46231) and witness_statement (test_w816, 72026). |
| EXISTS | A labelled screen method exists | scripts/screen_phrasings.py (W580): phrasings are labelled 'for' or 'not-for' before the result is known. test_w580 (39013) drives them. boundaries.py follows the same 'routes, never clears' rule (W1167). |
| EXISTS | The Law page draws only the held block | LawHub.tsx:234-237 (law-templates-held). LawHub.test.tsx:155-160. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- A reserved instrument asked for in the instructions of a listed template is drafted, and the clerk labels any id (P5.18, medium)

**Rows it closes:**

- The row above, closed as built.

**Changes:**

- agentic_core/legal/specialist.py: reserved_kind(text), a word-boundary screen for the four kinds: a transfer, charge or mortgage of land or property, a Land Registry application or form name, a contract for the sale of land, a house or a flat, and a lease that is a deed. It may route and never clears, and its coverage limit is stated.
- agentic_core/api/law.py: generate_document screens template_id, custom_instructions and party values before composing, and answers 409 with reserved_reason() and nothing sent. matter_assemble refuses an id that reserved_kind recognises, with the same reason; nda and witness_statement are unchanged. The 'reserved' block gains 'screen_basis'.
- scripts/screen_phrasings.py: A RESERVED list of 'for' and 'not-for' phrasings, labelled first, for example 'service agreement for a property management firm' and 'NDA about a land survey project' as not-for.
- apps/workstation-superapp/src/pages/domains/LawHub.tsx, LawHub.test.tsx and LawHub.fixture.json: Draw the templates answer's reserved kinds and reason beside the held line (data-testid law-templates-reserved), from a captured answer.
- docs/FOLLOWUPS.json and FABLE (P5.18 UPDATED): Close the row.
- integration_tests/test_mvp_spine.py: The new guard.

**Guard:** test_wXXXX_p518_a_reserved_instrument_asked_for_in_words_is_routed_and_the_page_says_which_are_reserved

- Each 'for' phrasing, as the instructions of a listed template, is refused with reserved_reason() and nothing is sent. FAILS IF: Only template_id is screened.
- Each 'not-for' phrasing drafts (200). FAILS IF: The screen over-routes.
- A reserved phrase in a party value is refused. FAILS IF: The parties are not screened.
- The clerk refuses 'tr1_transfer' with the same reason, and still assembles nda and witness_statement. FAILS IF: The clerk is unscreened, or over-refuses.
- The answer states the screen's coverage: it routes what it recognises and clears nothing. FAILS IF: A recognised-nothing answer reads as cleared.
- Vitest: the draft tab shows the reserved line with the captured reason. FAILS IF: The page drops it.

**Blinds:**

- Screen only template_id. -> Leg 1 goes red.
- Screen after composing. -> Leg 1's no-call spy records a call.
- Match 'property' alone. -> Leg 2 goes red.
- Leave assemble unscreened. -> Leg 4 goes red.
- The page omits the reserved line. -> The vitest goes red.

**Pins:**

- test_w714_a_deed_is_held_until_a_qualified_person_has_read_the_schedule (65589-65594 (as changed by C1)): 'nda' drafts; 'indeed_agreement' refused as unlisted -> Kept.
- test_w610_p323_the_legal_specialist_assembles_with_provenance_and_never_invents_a_particular (46231): client.post("/api/v1/law/matter/assemble", json={**_spec, "template_id": "nda"}) -> Kept: nda is not reserved.
- test_w816_the_law_authorities_are_typed_and_the_curriculum_select_shows_names (72026-72029): "template_id": "witness_statement" -> Kept.
- test_w825_the_law_and_care_selects_read_the_api_lists_and_the_employment_tabs_match_its_services (72317): 'data-testid="law-templates-held"' in law and "{templatesHeld!.reason}" in law -> Kept. The reserved line is added beside it.
- LawHub.test.tsx (155-160): getByTestId('law-templates-held').textContent).toContain(held.reason) -> Kept.
- test_w580_every_screen_is_driven_by_the_method_that_found_the_distress_miss (39013-39040): loads scripts/screen_phrasings.py and drives each screen's labelled list -> Kept. The RESERVED list joins it.

**Rulings it rests on:**

- P5.18 clause 4, ACCEPT and clause 8.
- W580's method: phrasings labelled before the result is known, so a defect is told apart from a stated limit.
- W1167: a screen routes and never clears.
- OWNER RULING 2026-10-13: the deed hold stays.

**Risks:**

- Over-routing ordinary property-services drafts. The 'not-for' list and leg 2 hold it.
- A screen cannot prove absence, so the answer says so.

### C7's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- None. Verified law.py:409-424 (instructions and party values reach the prompt), specialist.assemble 149-184, scripts/screen_phrasings.py (labelled lists; main() runs six tables), test_w580 at 39013, LawHub.tsx 234-237 and LawHub.test.tsx 155-160.

**Guard legs that could not fail:**

- None. Leg 3 (parties) is covered by the 'screen only template_id' blind; a separate 'screen instructions, not parties' blind would make it explicit.

**Pins the plan missed:**

- test_w580 drives only four screens with per-screen minimums (39046-39083), so RESERVED is not driven there. Follow W1167's pattern (95758-95772): the new guard drives RESERVED itself and asserts a results.append(_table(...RESERVED...)) line in screen_phrasings.main(). Add test_w1167 to the -k.
- test_w1014 (84614) governs the new LawHub vitest case. It is not in the -k.

**Conflicts with a ruling:**

- The shared reserved_reason carries C1's two conflicts: P5.11 clause 6 (named Acts must resolve) and P5.18 clause 8 (not_read listed). Numbering: W1193.

**Bar demands the plan missed:**

- The row should state its scope. Free-text generators outside Law, such as the studio and synthesis generators, are not screened, while P5.18 clause 4 is general.

**Fixes asked for:**

- Apply C1's reason fixes. Add test_w1167 and test_w1014 to the -k, re-render the living plan on close, and state the screen's scope in the row and the answer.

**Re-sized:** S to M, 1 round.

## W1196 - A3: The avatar and upload memory the Owner retired is removed: nothing writes it, nothing fetches a model for it, and the delete answer says what may remain elsewhere

**Closes:** Gap 1, correction 9 and its row. It also makes knowledge_synthesis.py:71's 'no in-process embedding model' true again.

**Owning item:** P3.32 (the Owner's ruling of 2026-11-22, recorded by W1192)

**Held on:** W1193

**Rows:**

- FU-1843 (P3.32, medium): The avatar and upload memory the Owner ruled retired on 2026-11-22 is still written by every avatar message and extracted upload, embeds each with chromadb's default model fetched from an outside host on first use, and says it is persisted

**Files:** agentic_core/ai/ceo/memory_v01.py; agentic_core/api/v138/ceo.py; agentic_core/avatars/api.py; agentic_core/ingestion/api.py; agentic_core/ai/logger.py; scripts/purge_memory_contamination.py; docs/LITERAL_OUTCOMES.json (only if the status word changes)

**-k:** -k "memory_v01 or test_two_authenticated_users_memory_isolated or test_w885_ or test_w507_fu167 or test_w583_p325 or test_w886_ or test_w1076_ or test_w966_ or test_w1192_ or test_w462_ or test_w469_ or ingest or avatar"

**Notes from the lead:**

Re-planned from the UNSOUND verdict.
- Removed: MemoryV01 and its instance. ceo.py:11 imports only meeting_log, and MeetingLog stays because ceo.py uses it. Also removed: avatars/api.py:43 and :648, and ingestion/api.py:13 and :159.
- Restated: avatars/api.py:18; ingestion/api.py:21, :153-154 and :265-271; ai/logger.py:17; the purge script's note at :62.
- The delete route's what_remains, extracted_text_may_still_be_recalled and not_claimed say what may remain elsewhere (the interaction log and VectorMemory keep a generation's prompt). They never say that nothing remains.
- The module states the ruling's reason: any later memory is built after sign-in, with retention and no outside download.

Pins changed on purpose:
- test_w507_fu167 :27494-27498;
- the memory_v01 legs of test_two_authenticated_users_memory_isolated (:5574-5580; its VectorMemory legs stay);
- test_w885 leg 4 (:76230-76233);
- test_w583 L5's comment and message. Its pin regex stays, because chromadb is still declared.

Guard:
- an AST leg: nothing under agentic_core, scripts or products imports chromadb;
- a subprocess with HOME and USERPROFILE empty before import and sockets recorded drives the avatar chat route and an extracted upload. It finds no ~/.cache/chroma, no connection attempt, and no chromadb in sys.modules.

Blinds: restore either add_exchange; restore the import; restore 'long-term memory'.

chromadb's declaration stays until A3b.

### A3 as planned (cluster A; size S, 1 round(s))

**Title:** The avatar and upload memory fetches no model, caps what it holds, and says it is held in this process only

**Closes:** Gap 1 (v43 G5) and correction n=9 (memory_v01.py:4-6)

**Owning item:** P3.30, tier 3: no user reads the store, and the fix removes an undisclosed model fetch and restates two claims (ACCEPT 1). The plan's false sentences at P2.13, P3.22 and P3.32 are corrected in W1192.

**Owner-gated:** The round stops chromadb's default model because downloading a model is already the Owner's and is ruled off (FU-1130, 2026-11-06). It decides neither residual question: whether to retire the store, and whether to drop chromadb's declaration. Those are two OWNER rows (M-EXEC-07).

**Depends on:** W1192 (the row, the plan corrections, the two OWNER rows). It is independent of A1 and A2, and must come before A7, because both edit avatars/api.py: A3 its docstring at :18, A7 its timing at :305 and :327.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | memory_v01 opens a chromadb collection with no embedding function, built at import | memory_v01.py:19-23, chromadb.Client().get_or_create_collection('memory_v01'); the module instance is at :63 |
| EXISTS | Its docstring says the memory is 'genuinely persisted and semantically searchable' | memory_v01.py:4-6 |
| EXISTS | In chromadb 1.5.5 the default embedding downloads all-MiniLM-L6-v2 from chroma's S3 host into Path.home()/.cache/chroma on first use, and the path is a class attribute bound at import | Read in the W1147 venv: chromadb/api/client.py:285-287 (DefaultEmbeddingFunction() is the default); api/types.py:947-960 (it delegates to ONNXMiniLM_L6_V2); utils/embedding_functions/onnx_mini_lm_l6_v2.py:36-43 (DOWNLOAD_PATH and MODEL_DOWNLOAD_URL) and :258-310 (__call__ downloads if missing, then runs onnxruntime) |
| EXISTS | Client() is ephemeral | chromadb/config.py:159, is_persistent False. Nothing in the repo sets IS_PERSISTENT; the Dockerfile ENV at :62-66 has none. |
| EXISTS | The model archive is in this environment's cache | ~/.cache/chroma/onnx_models/all-MiniLM-L6-v2/onnx.tar.gz, 83,178,821 bytes, written 2026-11-06 18:33 |
| EXISTS | Writers are every avatar message and every extracted upload | avatars/api.py:648, and ingestion/api.py:159 (only when the status is EXTRACTED) |
| ABSENT | A production reader of memory_v01.query exists | A grep over agentic_core finds no call. The gateway's recall reads VectorMemory (gateway.py:375-379 → ai/memory.py). api/v138/ceo.py:11 imports memory_v01 but uses only meeting_log. Only the suite queries it (test_mvp_spine.py:5578-5580, :76232-76233). |
| EXISTS | Comments say the AI CEO and the avatars read the store | ingestion/api.py:21, :153-154, :265-266; avatars/api.py:18 ('the real memory_v01 ChromaDB store') |
| EXISTS | The delete route says the text is in 'the AI's long-term memory' | ingestion/api.py:308-312, pinned by test_w507_fu167 (:27496-27497) |
| EXISTS | The image installs chromadb and onnxruntime, never prefetches the model, and runs as app with a home outside /app/data | Dockerfile:33-37 and :59-60 (useradd -m app); requirements.txt:16 and :92 |
| ABSENT | chromadb's telemetry calls out | chromadb/telemetry/product/posthog.py:10-11: capture is pass |
| ABSENT | Anything else imports chromadb | A grep over agentic_core, scripts and products finds only memory_v01.py:20 |
| EXISTS | The tenancy tests pass on the substring store | By reading: 'private board notes' is a substring of the stored prompt (test_mvp_spine.py:5575-5580), and the upload's own text is the query (:76232). |
| ABSENT | The dict store is bounded | memory_v01.py:17 and :33 have no cap. MeetingLog in the same file caps at 500 (:78, :91). |
| EXISTS | test_w583 L5's message calls chromadb part of the recall path | test_mvp_spine.py:38641-38643 and :38650-38652 |
| EXISTS | CI runs Python 3.12 with chromadb installed and caches no ~/.cache/chroma | .github/workflows/spine.yml (python-version '3.12'; pip install -r requirements.txt) |
| ABSENT | A row covers it | FU-1130 is dropped (the ruling, on a false premise). FU-282 is dropped, and its note calls memory_v01 a recall path. FU-079 and FU-220 concern an older persistent store. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The avatar and upload memory embeds every exchange with chromadb's default model, fetched from chroma's host on first use, and keeps it in this process only while its docstring says it is persisted (P3.30, medium)
- OWNER DECISION: retire memory_v01, which every avatar message and extracted upload writes and nothing in the platform reads, or keep it in-process (OWNER, low)
- OWNER DECISION: drop chromadb's direct declaration, which brings onnxruntime, once nothing imports it (OWNER, low)

**Rows it closes:**

- The A3 row registered by W1192: closed as built. The two OWNER rows stay open.

**Changes:**

- agentic_core/ai/ceo/memory_v01.py: Remove the chromadb import and the collection. MemoryV01 keeps its dict, the tenancy filter and substring recall, and gains MAX_EXCHANGES = 500 (the oldest are dropped, as in MeetingLog). The docstring says the store is held in this process only, lost on restart and not shared between processes; recall is a substring match with no embedding and no model; nothing in the platform reads it back today, because the AI CEO and the avatars recall from VectorMemory (ai/memory.py).
- agentic_core/ingestion/api.py: Restate the comments at :21, :153-154 and :265-271. what_remains (:308-312) says the text went into the in-process memory store at upload, is kept until the platform restarts or 500 newer exchanges displace it, and is read back by nothing in the platform today; it keeps 'CANNOT be removed by file id'. extracted_text_may_still_be_recalled is unchanged.
- agentic_core/avatars/api.py: :18 'the real memory_v01 ChromaDB store' becomes 'the in-process memory_v01 store (no embedding; read back by nothing today)'.
- integration_tests/test_mvp_spine.py: Append the new guard. Restate test_w583's L5 comment (:38641-38643) and message (:38650-38652): opentelemetry-api and -sdk are required by chromadb, which pyproject.toml still declares (and -api by anthropic), and a lock lists transitive dependencies by design. The anchored pin assertion is unchanged.
- docs/FABLE_DELIVERY_PROMPT.md: Under W1192's CORRECTED notes at P3.32 (and P2.13, P3.22), add one dated line: memory_v01 embeds nothing now; chromadb stays declared until the Owner rules.
- docs/FOLLOWUPS.json, plan blocks, living plan: Close the row.

**Guard:** test_wNNNN_the_avatar_and_upload_memory_fetches_no_model_and_says_it_is_held_in_process

- In a subprocess, with HOME and USERPROFILE set to an empty temp directory before anything is imported, and socket.create_connection and socket.socket.connect replaced by a recorder that raises: import agentic_core.ai.ceo.memory_v01, add_exchange a marker for owner 'a', and query as 'a' and as 'b'. The marker is recalled for 'a' only, no connection is attempted, no <HOME>/.cache/chroma exists, and neither 'chromadb' nor 'onnxruntime' is in sys.modules. FAILS IF: Red at HEAD: chromadb is imported, and the first add creates .cache/chroma and tries chroma-onnx-models.s3.amazonaws.com.
- Precondition: importlib.util.find_spec('chromadb') finds it in the environment, so leg 1's silence is a measurement FAILS IF: The test errors with that reason in an environment without chromadb, so the blind cannot pass vacuously.
- 600 add_exchange calls leave 500 entries, and the first hundred markers are not recalled FAILS IF: Red at HEAD (no cap).
- memory_v01.__doc__ says the store is held in this process and lost on restart, and contains no 'persisted' FAILS IF: Red at HEAD.
- Upload a text file and delete it: what_remains says 'until the platform restarts', keeps 'CANNOT be removed by file id', and contains no 'long-term' FAILS IF: Red at HEAD.

**Blinds:**

- Restore chromadb.Client().get_or_create_collection('memory_v01') -> Leg 1: chromadb is in sys.modules, a connection to the S3 host is recorded, and .cache/chroma is created.
- Remove the 500 cap -> Leg 3.
- Restore 'is genuinely persisted' in the docstring -> Leg 4.
- Restore 'the AI's long-term memory' in what_remains -> Leg 5.
- Drop the owner filter from query -> Leg 1: 'b' recalls 'a''s marker.

**Pins:**

- test_two_authenticated_users_memory_isolated (test_mvp_spine.py:5574-5580): memory_v01.query("private board notes", owner_id="alice343") recalls ORCHID-NINE; bob343 does not -> Keep: it passes on the substring store.
- test_w885_with_sign_in_on_a_second_person_reaches_none_of_the_first_persons_uploads (test_mvp_spine.py:76231-76233): _mem885.query(secret, owner_id=who["one"]) recalls; who["two"] does not -> Keep.
- test_w507_fu167_a_removal_deletes_the_bytes_and_says_what_it_cannot_reach (test_mvp_spine.py:27496-27497): out["extracted_text_may_still_be_recalled"] is True / "CANNOT be removed by file id" in out["what_remains"] -> Keep the field and the phrase. The sentence around them changes on purpose.
- test_w583_p325_what_the_platform_records_when_it_fails (test_mvp_spine.py:38641-38643, :38650-38652): chromadb, which agentic_core/ai/ceo/memory_v01.py imports on the cross-request recall path -> Restate the comment and message on purpose. The regex pin on opentelemetry-api and -sdk is unchanged.

**Rulings it rests on:**

- Owner ruling 2026-11-06 (FU-1130, FABLE:294-295): download no model candidate for now. Its slot_source says downloading a model is the Owner's (M-EXEC-07).
- P3.32 BOUNDARY (Owner ruling 2026-10-10): embeddings are not now; they need a backend, a model download and memory this machine does not have spare.
- Owner ruling 2026-10-12: anything that keeps something about a person is built after sign-in. So the round opens no persistent client at CHROMA_DB_PATH (store_paths.py:37).
- P4.5 (Owner ruling 2026-10-12): the first deploy runs the floor only.
- M-EXEC-07: retiring the store and dropping chromadb are do-X-or-Y fixes, so they are OWNER rows.

**Risks:**

- ONNXMiniLM_L6_V2.DOWNLOAD_PATH binds Path.home() at import, and this machine already holds the archive. Only a child process with HOME and USERPROFILE set first can see a fresh cache.
- On Windows Path.home() reads USERPROFILE, so the child sets both. The Windows CI job runs this test.
- Semantic recall leaves memory_v01, but nothing reads it in production, so no answer changes.

### A3's refutation: **UNSOUND**

**Wrong state verdicts - trusting these skips or redoes real work:**

- owner_gated is out of date. The plan says the round 'decides neither residual question: whether to retire the store ...' and registers an OWNER row to ask it. The Owner answered on 2026-11-22 (Q2: the avatar/upload memory RETIRED; any later memory built after sign-in with retention and no outside download).
- Incomplete list of claims: agentic_core/ai/logger.py:17 ('parallel to VectorMemory + memory_v01') and scripts/purge_memory_contamination.py:62 ('unscoped memory_v01 collection') also describe the store; neither is in the change list.

**Guard legs that could not fail:**

- Under the plan's design the legs can fail. Under the ruling the design is replaced, so its legs 3 (500 cap) and 4 (docstring says in-process) test a store that must not exist.

**Pins the plan missed:**

- Under the ruled retirement these change on purpose and are missing from the pin list: test_w507_fu167 (test_mvp_spine.py:27494-27498: status REMOVED, extracted_text_may_still_be_recalled True, 'CANNOT be removed by file id', 'overstate' in not_claimed); test_two_authenticated_users_memory_isolated (:5574-5580, the memory_v01 legs; its VectorMemory legs at :5568-5572 stay); test_w885 (:76230-76233, leg 4); test_w583 L5's comment and message (:38641-38643, :38650-38652).
- docs/LITERAL_OUTCOMES.json carries (agentic_core/ingestion/api.py, delete_ingested_content, status, REMOVED). If retirement changes the status word, the P5.10 clause 4 screen (test at :81699ff) fails on the stale entry unless the entry changes in the same commit.

**Conflicts with a ruling:**

- Owner ruling 2026-11-22 Q2: memory_v01 is RETIRED. The plan keeps it in-process with a 500 cap and asks the Owner whether to retire it.
- Owner decisions 2026-11-22, 'no Owner QUESTION rows': the plan's second OWNER row (drop chromadb's declaration) is a new question. The precedent FU-1174 made such a removal an Owner decision, so it goes to the lead, not into the register.

**Bar demands the plan missed:**

- The restated what_remains must not claim nothing remains. When a generation reads an uploaded file, the gateway keeps the full prompt in the interaction log and in VectorMemory ('User: {prompt}', gateway.py:553-578), and the avatar and CEO recall from VectorMemory. Cluster B's P4.2 deletion drill owns that store.
- The ruling's own reasons should be in the module: 'any later memory is built after sign-in with retention and no outside download'.

**Fixes asked for:**

- Redesign A3 as the retirement the Owner ruled. Remove MemoryV01 and its instance from memory_v01.py, keeping MeetingLog and meeting_log, which ceo.py uses (:205-208, :454-455, :592-599). Change ceo.py:11 to import meeting_log only. Remove avatars/api.py:43 and :648, and ingestion/api.py:13 and :159. Restate avatars/api.py:18, ingestion/api.py:21, :153-154 and :265-271, ai/logger.py:17, and the delete route's what_remains, extracted_text_may_still_be_recalled and not_claimed (and the LITERAL_OUTCOMES entry if the status word changes). Restate test_w507, test_w885 leg 4, the memory_v01 legs of test_two_authenticated_users, and test_w583 L5's text. The pin regex stays: chromadb is still declared and still requires opentelemetry.
- Guard: an AST leg that no module under agentic_core, scripts or products imports chromadb. Keep the subprocess leg (HOME and USERPROFILE empty before import, sockets recorded): drive POST /api/v1/avatar/chat and an extracted upload; assert no ~/.cache/chroma, no connection attempt, and chromadb absent from sys.modules. Add a leg that the upload's delete answer names what may remain elsewhere. Blinds: restore either add_exchange call; restore the chromadb import; restore 'long-term memory' in what_remains.
- Raise the chromadb/onnxruntime declaration with the lead.

**Re-sized:** S-M: one retirement round across four modules, with four tests restated on purpose.

## W1197 - A1: The composition preview computes the gate's verdict and records nothing; POST /compose and PUT /compositions/{cid} still seal

**Closes:** Gap 2, correction 8 and its row

**Owning item:** P3.30 (the route of FU-1108)

**Held on:** W1193

**Rows:**

- FU-1841 (P3.30, low): The composition preview seals a quality record, logs a UEG screen event, fires a cognitive signal and, on a compliance fail or escalation, records with the immune system, while it says nothing is saved

**Files:** agentic_core/vbs/quality.py; agentic_core/api/resource_fabric.py; agentic_core/ai/native/homeostasis.py

**-k:** -k "composition_preview or test_resource_compose or test_resource_composition_run_on_native_swarm or test_compliance_sealed_ueg_immune_and_routed or test_w449_ or test_w742_ or test_w853_ or test_w917_ or test_p330_r6_ or test_vbs_living_systems_integrated_in_house or test_w506_p27_layers or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- With record=False, the preview's Nervous and Endocrine layers report as not engaged on this call. They use an allowed state, implemented_not_on_this_path (test_w506 :26052-26060), with a basis naming the preview, and layers_note is computed per record. A leg and a blind (restoring the static states) hold it.
- assure_delivery refuses record=False when the content is not floor-served. A leg drives a model-served call and asserts that qms gates_run and defects do not move (W489's rule).
- quality.py:383-385 ('the record is still sealed') is restated for record=False.
- UEGLogger.log is spied on by wrapping, never by replacing.
- The row's why adds escalation (quality.py:589-597).

### A1 as planned (cluster A; size S, 1 round(s))

**Title:** The composition preview computes the gate's verdict and records nothing; POST /compose and PUT /compositions/{cid} still seal

**Closes:** Gap 2 (v44 V44-G1; v43 G2; v42/v41 G1) and correction n=8 (resource_fabric.py:3907 'Nothing is saved.', :3921 'not saved')

**Owning item:** P3.30, as FU-1108 (W742) was: the same route and class. resource_fabric.py is in an area retired with P2.18, so the row names its slot.

**Owner-gated:** No. The round makes the preview keep no record, which is what it already claims.

**Depends on:** W1192 registers the row. This is the first of the rounds that edit resource_fabric.py (A2, A7, A9 and A10 follow) and the first of two that edit vbs/quality.py (A5 follows).

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | simulate_composition says 'Nothing is saved.', answers saved False and the note 'not saved' | resource_fabric.py:3904-3923 (docstring :3907, saved False :3917, note :3921) |
| EXISTS | The preview reaches assure_delivery(label='composition', served_by='template') | resource_fabric.py:3914 calls _simulate_configuration (:3864-3888), which calls assure_delivery at :3877 |
| EXISTS | Every call seals a version of qms_record:composition and counts a controlled document | quality.py:543 calls qms.control_document. qms.py:372-377 calls commit_artifact and increments controlled_documents at :376. dcms.py:52-67 appends and rewrites dcms_registry.json. document_controlled is set True at quality.py:558. |
| EXISTS | Every call logs a compliance.screen UEG event | quality.py:574-580 UEGLogger().log({'type': 'compliance.screen', 'label': label, ...}) |
| EXISTS | A compliance fail or escalation records with the immune system | quality.py:591-597 immune.record(f'compliance:{label}', ...). Only a fail moves the threat ladder: escalation is a review flag (immune.py:165 REVIEW_FLAG_TYPES). |
| EXISTS | Every call fires a cognitive nervous signal | quality.py:670 biobus.fire_signal('cognitive', f'qms.{label}', ...) |
| ABSENT | A preview routes to Change Control | 'composition' is not in _MATERIAL (quality.py:604-605) and does not start with 'economy' |
| EXISTS | The gate itself does not run for a template | floor_served('template') gives qms_gate_passed None (quality.py:504-510). Asserted at test_mvp_spine.py:2917. |
| EXISTS | POST /compose and PUT /compositions/{cid} share the function and must keep sealing | resource_fabric.py:3937 (compose) and :1566 (update). Both are save paths. |
| EXISTS | The lifecycle basis says a simulation stores nothing | resource_fabric.py:1263, copied in ResourceFabric.fixture.json:45, :89 and :147. The sentence becomes true; no edit is needed. |
| EXISTS | homeostasis concedes the preview may change other state | homeostasis.py:64-65 '(a caller such as the composition preview may still change other state)' |
| ABSENT | An open row covers the seal | FU-1108 is done and its close_note names the residue ('The preview's QMS gate still fires its cognitive signal and writes its UEG screen event'). No open row names the DCMS seal. |
| EXISTS | The page draws the note; the preview chip claims no document control | ResourceFabric.tsx:707 draws sim.note. lib/api.ts:356-366: qmsChip's not-assessable branch prints no 'doc-controlled'. |
| EXISTS | The UEG logger is a per-path singleton whose default path is fixed at import | gaas/v5/ueg.py:45 and :141-170. test_compliance_sealed reads events through GET /api/v1/gaas/ueg/events (test_mvp_spine.py:1759). |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The composition preview seals a quality record, logs a UEG screen event, fires a cognitive signal and, on a compliance fail, records with the immune system, while it says nothing is saved (P3.30, low)

**Rows it closes:**

- The A1 row registered by W1192: closed as built

**Changes:**

- agentic_core/vbs/quality.py: assure_delivery gains the keyword record: bool = True. With record=False, the stub screen, the compliance screen, the gate decision and the bar are computed and returned as now. Nothing is recorded: control_document is not called (no version and no controlled_documents increment); quality_record_hash is None; document_controlled is False with document_control_basis 'not recorded: a preview keeps no record; POST /compose and PUT /compositions/{cid} gate and seal the same text'; there is no UEGLogger().log, no immune.record and no Change Control routing. The biomimetic block still reads immune.status() and the circadian cycle, so layers keeps 'Immune', but it does not fire_signal. The docstring says that a record=False call never opens a defect.
- agentic_core/api/resource_fabric.py: _simulate_configuration(name, rids, usage_area, cfg, *, preview=False) passes record=not preview. simulate_composition passes preview=True, and its docstring and note say the gate's verdict and the compliance screen were computed and nothing was recorded, sealed or logged. compose (:3937) and update (:1566) are unchanged and keep sealing. The lifecycle basis at :1263 is unchanged; it is now true.
- agentic_core/ai/native/homeostasis.py: Remove the parenthesis at :64-65 '(a caller such as the composition preview may still change other state)'.
- integration_tests/test_mvp_spine.py: Append the new guard. test_resource_compose_model_and_simulate_before_commit's comments at :2909 and :2930 cite the round; its assertions are unchanged.
- docs/FOLLOWUPS.json, docs/FABLE_DELIVERY_PROMPT.md (generated blocks), docs/WORKSTATION_IDBO_LIVING_PLAN.md: Close the row as built, with a close note naming the guard and its blinds.

**Guard:** test_wNNNN_the_composition_preview_computes_its_verdict_and_records_nothing

- POST /compose/simulate named 'wNNNN alcohol sales and gambling revenue' (W287's fail wording), with resources bdp, ddpie and genesis and usage area design, answers 200 with simulation.quality.compliance.overall 'fail', qms_gate_passed None, saved False, quality_record_hash None, and document_controlled False with its basis naming POST /compose FAILS IF: Red at HEAD (a hash is returned and document_controlled is True). Also red if the record=False path stops computing the verdict.
- Across that preview and a second whose name carries only an escalation term, six counters are unchanged: len(dcms.registry['qms_record:composition']); the same count in a fresh DocumentControlManagementSystem read from the store; qms.controlled_documents; immune._events whose endpoint is 'compliance:composition'; a spy on the UEGLogger.log class attribute for payloads of type compliance.screen with label composition; and a spy on biobus.fire_signal for ('cognitive', 'qms.composition') FAILS IF: Red at HEAD, where every counter moves on every call.
- POST /compose with the same body adds exactly one version of qms_record:composition (in memory and in a fresh instance), one controlled document, one compliance.screen event labelled composition (in the spy and in GET /api/v1/gaas/ueg/events), one immune 'compliance:composition' event and one 'qms.composition' signal, and answers document_controlled True FAILS IF: A keep leg. Red under blind 5, a fix that also stops a commit sealing.
- PUT /compositions/{cid} on that composition adds exactly one version FAILS IF: A keep leg. Red under blind 6, which routes the save path through the preview flag.
- The preview's answer names what was not recorded: document_control_basis names POST /compose and PUT /compositions/{cid} FAILS IF: Red at HEAD (no such field). Also red if the basis is dropped.

**Blinds:**

- Ignore record=False in the control_document branch -> Leg 2: the version count and controlled_documents rise on each preview.
- Restore UEGLogger().log on the preview path -> Leg 2: the compliance.screen spy sees label composition.
- Restore immune.record on the preview path -> Leg 2: the fail preview adds a 'compliance:composition' event.
- Restore biobus.fire_signal on the preview path -> Leg 2: the spy sees ('cognitive', 'qms.composition').
- Pass record=False from compose as well -> Leg 3: a commit no longer seals or counts.
- Call _simulate_configuration(..., preview=True) from PUT /compositions/{cid} -> Leg 4: a save adds no version.

**Pins:**

- test_resource_compose_model_and_simulate_before_commit (test_mvp_spine.py:2913): assert sim["saved"] is False -> Keep.
- test_resource_compose_model_and_simulate_before_commit (test_mvp_spine.py:2917-2918): q["qms_gate_passed"] is None and "not assessable" in q["qms_basis"] and len(q["bar"]) >= 12 ... sim["simulation"]["biomimetic"]["layers"] -> Keep. record=False must still compute qms_basis and the bar and read immune.status(), so layers still carries 'Immune'.
- test_resource_compose_model_and_simulate_before_commit (test_mvp_spine.py:2909, :2930): nothing is saved by the preview / # the preview saved nothing -> Comments only. Both become true; cite the round.
- test_resource_compose (test_mvp_spine.py:2904): body["quality_assurance"]["quality"]["document_controlled"] is True -> Keep: a commit still seals.
- test_compliance_sealed_ueg_immune_and_routed (test_mvp_spine.py:1752-1768): assure_delivery(... label="cascade") ... compliance.screen ... Compliance FAIL routed -> Keep: record defaults to True.
- test_w853_a_defect_leaves_the_loop_closed_as_source_retired_or_not_reproducible_and_neither_is_a_gate_pass (test_mvp_spine.py:74010-74030): label=([^,\n]+?) parsed from every assure_delivery call; used == LIVE_GATE_LABELS -> Keep. The preview call keeps label="composition"; record= is another keyword; LIVE_GATE_LABELS is untouched.
- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67558-67572): the preview did not project at all ... a read-only projection advanced the shared ATP simulator -> Keep. The projection is unchanged.
- test_w917_fu609_the_fabric_page_shows_each_compositions_lifecycle_against_the_apis_own_answers (test_mvp_spine.py:78033-78060): set(c["lifecycle"]) == set(live["lifecycle"]) -> Keep. The lifecycle basis text is unchanged.

**Rulings it rests on:**

- P3.30 ACCEPT (1): a DOC_OVERCLAIM ('Nothing is saved.') is made true. ACCEPT (4): it is guarded on the property and driven red.
- Owner ruling 2026-10-09: tier-3 findings ride P3.30, one row per region. FU-1108 (same route) is the precedent.
- P3.31 clause 4: a proposal 'saves nothing and runs nothing'. This is the standing text closest to a preview.
- W287 ('every screen seals a UEG event') and W489 are about deliveries and what-if gates. A preview is neither, and its gate is not assessable (W449). The round record says so.
- W637: an escalation is a review flag and moves no threat, so the immune leg drives a fail.
- W742 (FU-1108): the projection's read-only property is unchanged and still held by test_w742 leg 8.

**Risks:**

- A preview of a name with prohibited terms no longer files compliance_fail with the immune system. That is the intent, but a person probing names now leaves no trace; the commit still records.
- The UEG path is fixed at import (ueg.py:45), so the guard spies on the class attribute and filters events by type and label. Concurrent beats cannot move it.
- If a future caller previews model-served text with record=False, the non-floor gate branch would run. The round keeps that branch from opening a defect and says so in the docstring.

### A1's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- None is dead. Leg 3 asserts the compliance.screen event both 'in the spy and in GET /api/v1/gaas/ueg/events', which needs a spy that calls through to the real UEGLogger.log. A replacing spy makes the GET half fail on a correct change.

**Pins the plan missed:**

- test_w506_p27_layers_state_per_layer_and_the_reachability_is_checked (test_mvp_spine.py:26052-26060) holds LAYER_STATE to six allowed states. A per-record override for a preview's Nervous/Endocrine state must use one of them (e.g. implemented_not_on_this_path), or this test goes red.

**Conflicts with a ruling:**

- W449's design rule, stated in assure_delivery's own docstring (quality.py:383-385: 'the record is still sealed, so the DCMS holds the not-assessable verdict rather than nothing'), is what the round makes an exception to. The docstring must be restated for record=False, or it becomes a new overclaim in the code this cluster cleans.
- W489's refutation (qms.py:120-131: 'Excluding a run from the RATE and refusing to RECORD it are different things') forbids a gate that runs and opens no defect. record=False with a non-floor served_by would reach qms.run_quality_gates (quality.py:526-528), which always writes. The plan's docstring promise ('a record=False call never opens a defect') is untested and sits against that rule.

**Bar demands the plan missed:**

- The preview's own biomimetic block would then claim an engagement it no longer has. LAYER_STATE marks Nervous and Endocrine 'engaged_no_value' because 'the fire_signal below routes into the NervousSystem' / 'this record's own fire_signal travels on it' (quality.py:46-48, :64-75). layers_note prints 'Engaged on this path without contributing a value' statically (:700-703). With record=False skipping fire_signal, the preview's answer says both layers engaged when nothing was fired.
- No leg checks the record=False contract beyond the template path.

**Fixes asked for:**

- With record=False, report Nervous and Endocrine as not engaged on this call (an allowed state, with a basis naming the preview). Add a leg: the preview's layer_states/layers_note does not list them as engaged. Blind: restore the static states.
- Make assure_delivery raise ValueError (or refuse) when record=False and the content is not floor-served (or sections_by_construction is not given). Add a leg driving a model-served record=False call and asserting it is refused and that qms gates_run and defects do not move.
- Restate quality.py:383-385 for record=False.
- Spy on UEGLogger.log by wrapping, not replacing. In the row's why, add that an escalation also records with the immune system (compliance_escalation, quality.py:589-596).

**Re-sized:** S (unchanged).

## W1198 - B2: An account is removed by a command run over SSH that reads the users store whole, never by editing users.json by hand

**Closes:** FU-1836 (W1191's row)

**Owning item:** P4.1

**Held on:** W1191 landed (set_password.py's pattern, step 12)

**Rows:** none of its own; see its notes.

**Files:** agentic_core/auth/remove_account.py (new); docs/DEPLOYMENT.md

**-k:** -k "remove_account or test_w1191_ or test_w1134_ or test_user_store_survives_concurrent_writes or test_w864_ or test_w865_ or test_auth_login or test_auth_me_single_user or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- Anchor on W1191's landed step 12. It prints name, role and created_at: 'It prints admin's line, and one for each account the Owner made', and test_w1191 asserts that 'It prints ['admin']' is absent.
- Keep its pinned phrases and its restore advice for an account made while sign-in was off. The stand-in admin may have done more than make an account.
- Add the command as a separate block, for an account the Owner made and no longer wants.
- Leg 3 asserts the reason for the refusal: the store could not be read whole, or is not there. Without that, blind 5 cannot turn it red.
- Catch core._users_mutation's 503 (core.py:144-150) and refuse with a sentence.

FU-1834 stays open: the boot still replaces a torn store.

### B2 as planned (cluster B; size S, 1 round(s))

**Title:** An account is removed by a command run over SSH that reads the users store whole, never by editing users.json by hand (FU-1836)

**Closes:** FU-1836: W1191's fourth new row, 'No command removes an account from the users store, so an unwanted one is removed only by editing users.json by hand'. Read its id once W1191 lands; FU-1836 is expected.

**Owning item:** P4.1

**Owner-gated:** Running the command is the Owner's, over SSH on the machine, like set_password. The round only builds it and drives it on made-up stores. It never removes the admin, and it touches no other store: a person's other records are B8's.

**Depends on:** W1191 landed: agentic_core/auth/set_password.py as the pattern, step 12's accounts check, and FU-1836. It does not depend on FU-1834 (left open by W1191): the command reads the store strictly before core is imported, so it is safe either way. B8 reuses it.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | No route or command removes an account | auth/core.py serves only DELETE /api-key/{key_id} (:597-616). No remove_account, delete_user or remove_user in agentic_core/auth, scripts, deploy or docs/DEPLOYMENT.md. |
| EXISTS | _users_mutation serialises a read-modify-write across threads and processes | core.py:139-150 (store_lock; a timeout becomes a 503) |
| EXISTS | An unreadable store is read as no accounts, and importing core then writes a store holding only admin | core.py:117-123 (except: pass; return {}) and :157-184 (_create_default_admin runs at import). This is FU-1834's subject. |
| EXISTS | _save_users writes atomically | core.py:126-136 (atomic_write_json) |
| EXISTS | read_json_strict raises StoreUnavailable for a store that exists but cannot be read whole | agentic_core/config.py:152 and :165 |
| ABSENT | set_password.py (the strict-read-before-import pattern) | Not at 89c25eed. W1191 adds it (a scratch copy outside the tree): _account() reads strictly, core is imported after, and the store is read again under core._users_mutation(). |
| EXISTS | A removed account's token stops at its next request | get_current_user looks the user up on every call and answers 401 'User not found.' (core.py:276-279) |
| ABSENT | Step 12 checks the accounts before the domain and gives no way to remove one | Not at 89c25eed. W1191's scratch DEPLOYMENT.md step 12: 'It prints ['admin']. Any other name is an account made through the tunnel while sign-in was off, and the domain is not set while it is there.' |
| ABSENT | FU-1836 and FU-1834 are in the register | Highest id at 89c25eed is FU-1832. W1191's apply registers the torn-store row (medium) and the removal row (low) on P4.1 (a scratch copy outside the tree). |

**Rows it closes:**

- FU-1836 (built)

**Changes:**

- agentic_core/auth/remove_account.py (new): 'python -m agentic_core.auth.remove_account USERNAME', on set_password's pattern. Refused before anything is read: no argument, more than one, or one starting with '-' (exit 2). The users store is then read strictly, BEFORE agentic_core.auth.core is imported. A store that is missing or cannot be read whole is refused and left byte for byte, and core's _USER_STORE must be the file that was read. Also refused: 'admin', and a name the store does not hold. The Owner types the name again, and a mismatch is refused. Under core._users_mutation() the store is read whole again, the account is removed, and core._save_users writes it. The command prints the name, its role and how many API keys went with it, and says that the person's records in other stores are not touched. It writes nothing else: no event, no file of its own.
- docs/DEPLOYMENT.md: Step 12, after the accounts check's 'Any other name...' sentence: the command once, in its own bash block ('sudo docker exec -it workstation python -m agentic_core.auth.remove_account NAME'), then run the check again. Add one sentence: a store the command says cannot be read whole is not edited, and the platform is not restarted on it before the data disk is restored (step 9), because its boot replaces such a store (FU-1834). The order rule, then accounts, then domain is unchanged.
- docs/FOLLOWUPS.json: FU-1836 closed as built.
- integration_tests/test_mvp_spine.py: test_wNNNN_fu1836_an_account_is_removed_by_a_command_that_reads_the_store_whole_and_never_by_hand appended.

**Guard:** test_wNNNN_fu1836_an_account_is_removed_by_a_command_that_reads_the_store_whole_and_never_by_hand

- Removal: in its own process with DATA_DIR and WORKSTATION_DATA_DIR on a temp folder holding {admin, alice with one API key, bob}, the command for alice with stdin 'alice' exits 0. The store then holds admin and bob, each equal to before; alice and her key are gone; the output says her other records were not touched FAILS IF: another account changes, alice stays, or the output claims more than the users store
- Refusals: no argument, two arguments, '--all', 'admin', 'carol' (not held) and a mismatched confirmation each exit non-zero with the store byte for byte unchanged FAILS IF: any of them writes the store
- An unreadable store: with users.json missing, the command refuses and no users.json is created; with users.json truncated mid-JSON, it refuses and the bytes are unchanged, not replaced by an admin-only store FAILS IF: core is imported before the strict read, or the store is read tolerantly
- Read again under the lock: driven in process, with input() patched to add 'dave' to the store before answering, dave is still there after alice is removed FAILS IF: the command writes the first read's dict back
- The effect: in process with sign-in on (monkeypatched), a token issued to alice before the removal gets 401 'User not found.' on GET /api/v1/auth/me after it FAILS IF: a removed account keeps signing in
- The guide and the row: step 12 gives the command once, between the accounts check and the domain command, and FU-1836 is closed by this round as built FAILS IF: the guide still offers only a hand edit or a restore, or the order changes

**Blinds:**

- Import agentic_core.auth.core before the strict read -> Leg 3: importing core makes a users.json where none was, and replaces the truncated one with an admin-only store.
- Save the first read's dict instead of reading again under the lock -> Leg 4: dave is lost.
- Allow 'admin' to be removed -> Leg 2: the admin refusal writes the store.
- Skip the typed confirmation -> Leg 2: the mismatch leg removes alice.
- Read the store with json.load and a fallback to {} -> Leg 3: the truncated store is treated as empty and the command proceeds or writes.

**Pins:**

- test_w1191_the_release_machine_serves_publicly_only_with_its_domain_https_and_sign_in_on (lands with W1191) (the S4 step 12 list and order check, about test_mvp_spine.py:99061-99068 in the scratch copy): 'Create step 6's rule now', 'GET /api/v1/auth/users', 'It prints ['admin']', '--metadata=domain=DOMAIN,auth-enabled=true', with the rule before the accounts and the accounts before the domain -> Keep every phrase and the order. The new block goes between the accounts check and the domain command.
- test_w1191_the_release_machine_serves_publicly_only_with_its_domain_https_and_sign_in_on (S4 blocks.count(cmd) == 1, and the S2 scan): the set_password command and the users.json print each appear once; no file sets AUTH_ENABLED to true or sets a credential setting or a credential setting -> The new command is a distinct block and the module sets none of these. No change.
- test_w1134_fu603_the_google_cloud_deploy_is_written_from_googles_pages_and_no_disk_with_records_is_formatted (test_mvp_spine.py:92786-92805): step tags must be listed pages -> The new text carries no bracketed token.

**Rulings it rests on:**

- OWNER RULING 2026-11-21 (afternoon): the password and the signing secret are kept on the machine, never in the repository (P4.1, FABLE:6746-6747)
- OWNER RULING 2026-11-20 (evening): no round switches sign-in on in the tree (FABLE:6737-6739)
- FU-1834 (W1191, open): the platform's boot replaces a store it cannot read; this command refuses such a store and does not fix the boot

**Risks:**

- FU-1834 stays open. The command refuses a torn store, but the platform's next boot replaces it. The guide's new sentence says not to restart on such a store; the real fix is FU-1834's.
- On Windows CI, stdin for the subprocess must be given as text with a newline, and the store's bytes must be compared raw.
- W1191's landed step 12 may word the accounts check differently from the scratch copy. Anchor the insertion on the landed text.

### B2's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'Step 12 ... gives no way to remove one' quotes a superseded scratch step 12 ('It prints ['admin']. Any other name ...'). W1191's current step 12 (a scratch copy outside the tree) prints name, role and created_at. It says 'It prints one line, admin's. Any account the Owner did not make is a reason to stop', and it gives a way forward: restore the data disk from a snapshot, or start on a blank data disk, and find what reached the forwarded port. test_w1191 asserts that 'It prints ['admin']' is NOT in step 12.
- Minor line drift: _load_users is auth/core.py:115-121 and _save_users is :124-134.

**Guard legs that could not fail:**

- Blind 5 (json.load with a fallback to {}) cannot turn leg 3 red as written. The tolerant read gives {}, so 'alice' is 'not held' and the command refuses before core is imported. The bytes stay unchanged, and with a missing store no file appears. Leg 3 must also assert the refusal's reason: the store could not be read whole, or it is not there.

**Pins the plan missed:**

- test_w1191, S4 step-12 list (W1191's staged guard (a session work file, not in the tree):495-513). The plan's 'keep It prints ['admin']' is inverted: the test asserts it absent. The pinned phrases to keep:
  - 'It prints one line, admin's. Any account the Owner did not make is a reason to stop, and one made before sign-in was turned on is the kind to distrust'
  - 'The data disk is restored from a snapshot taken before that account (step 9; ...)'
  - 'the platform starts again on a blank data disk'
  - 'what reached the forwarded port is found before a tunnel is opened again'
  - the rule, then the accounts, then the domain order assert.
  The new block must not contradict the guide's 'Then the domain is not set.'

**Bar demands the plan missed:**

- Keep W1191's restore advice for an account made while sign-in was off: the stand-in admin may have done more than make an account, which is FU-1835's mechanism. Offer the command for an account made with sign-in on that the Owner no longer wants. Leg 6's 'fails_if the guide still offers only ... a restore' must not push the restore out.
- core._users_mutation raises HTTPException(503) on a lock timeout (auth/core.py:144-150). The command must catch it and say it as a refusal.

**Fixes asked for:**

- Anchor on W1191's landed step 12. Keep its pinned phrases. Add the command as a distinct block for accounts the Owner made, without dropping the restore path.
- Leg 3 asserts the refusal reason in both cases.
- Catch the 503 and refuse with a sentence.

**Re-sized:** S, 1 round

## W1199 - D-SCHOLAR-REQUEST: The request to a scholar or trusted institute is drafted for the Owner to send, naming everything withheld now

**Closes:** Preparation for FU-1838 (W1192's row). The row stays open until the Owner's dated engagement or a ruling that defers it.

**Owning item:** OWNER (FU-1838); P5.17 clause 7

**Held on:** W1192 (FU-1838)

**Rows:** none of its own; see its notes.

**Files:** docs/letters/SCHOLAR_REVIEW_REQUEST.md (new); docs/RESUME_ON_MY_MACHINE.md

**-k:** -k "scholar_request or test_w1192_ or test_w1132_ or test_w948_ or test_w594_ or test_w1131_ or test_w1164_ or test_w1180_ or test_w1190_ or test_w462_ or test_w469_ or test_w1143_ or test_w1135_ or test_w732_"

**Notes from the lead:**

Not conditional: the Owner accepted it on 2026-11-22 (NG6).

Refuter fixes applied:
- The letter also names the five Religion research tools' withheld model answers (the Owner's ruling of 2026-10-11; vision :1439-1440). These sit beside A.12.3's adult curriculum and tajweed items, P5.17 clause 4's attestation wording, and P5.21's pack, whose gate stays closed.
- 'fee' is matched as a whole word.
- Append to FU-1838's list line and why. Keep test_w1192's pinned text and its order asserts.
- The bullet goes in 'Still yours', not in step 5.
- No Arabic script, no fee's form, no a gendered pronoun.

### D-SCHOLAR-REQUEST as planned (cluster D; size S, 1 round(s))

**Title:** The request to a scholar or trusted institute is drafted for the Owner to send, naming what is withheld now

**Closes:** Preparation for v40 new gap 6. The scholar row stays open until the Owner's engagement or a ruling.

**Owning item:** OWNER (the scholar row). The draft makes P5.17 clause 7's 'WITH THE OWNER' sendable.

**Owner-gated:** Choosing, engaging, naming or rostering a scholar, and sending the request, are the Owner's. The roster is the Owner's (P5.21). If the Owner declines the recommendation, this round is dropped.

**Depends on:** W1192 (the row). Recommended after the Owner's answer, or before it as preparation, as FU-1283's draft was.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| ABSENT | A drafted request to a scholar | docs/letters/ holds KFGQPC_PERMISSION_REQUEST.md, QUL_DATA_PERMISSION_REQUEST.md and QURANIC_AUDIO_DATASET_REQUEST.md only. |
| EXISTS | The letter pattern to follow | test_w1132 (:92411-92451) holds 'DRAFTED FOR THE OWNER TO SEND', 'Nothing has been sent', '[your name]' and '[your address]', an OWNER row naming the path, and the list line 'FU-x (Wnnn): send the request drafted in docs/letters/...'. |
| EXISTS | What would be reviewed now | - R7 / A.12.3 (FABLE:2376-2382). - P5.17 clause 4: 'a teacher's own attestation ... its wording reviewed by a scholar first' (FABLE:7390-7391). - P5.21's approval pack (FABLE:7538); its gate stays closed until P5.12's headings and a safeguarding review (:7554-7555). - The roster is empty (WORKSTATION_IDBO_WHOLE_VISION.md:1729-1731). |

**Changes:**

- docs/letters/SCHOLAR_REVIEW_REQUEST.md: New, LF. 'DRAFTED FOR THE OWNER TO SEND (WNNNN, FU-x). Nothing has been sent.' Addressed to '[the scholar or institute]' from '[your name]' at '[your address]'. It offers the work to 'a scholar or a trusted institute' and names what is withheld now: the adult curriculum and tajweed items (A.12.3), P5.17 clause 4's attestation wording, and P5.21's approval pack, whose gate stays closed until P5.12's headings and a safeguarding review. It says an approval binds the exact text, nothing is shown before it, the platform composes no Quran Arabic and scores no recitation, and children do not use the tools. It contains no scripture, no fee's form and no personal detail.
- docs/FOLLOWUPS.json: The scholar row's why names docs/letters/SCHOLAR_REVIEW_REQUEST.md, and its RECOMMENDED becomes 'send it as drafted'.
- docs/FABLE_DELIVERY_PROMPT.md: The row's list line names the draft, keeping 'FU-x (W1192):' and 'Recommended'. Re-render.
- docs/RESUME_ON_MY_MACHINE.md: The scholar bullet names the letter in `docs/letters/`.
- integration_tests/test_mvp_spine.py: Append the new test.

**Guard:** test_wNNNN_the_scholar_request_is_drafted_for_the_owner_offers_a_scholar_or_an_institute_and_names_what_is_withheld

- 1. The letter exists, carries 'DRAFTED FOR THE OWNER TO SEND', 'Nothing has been sent', '[your name]' and '[your address]', and offers 'a scholar or a trusted institute'. FAILS IF: It is absent (it is on the unchanged tree) or a fragment is dropped.
- 2. It names 'A.12.3', 'P5.17 clause 4' and 'P5.21', and says that gate stays closed until P5.12's headings and a safeguarding review. FAILS IF: A scope item or the closed gate is dropped.
- 3. It holds no Arabic-script character (U+0600–U+06FF, U+0750–U+077F, U+08A0–U+08FF, U+FB50–U+FDFF, U+FE70–U+FEFF), no 'fee', and nothing matching _W963_PERSONAL. FAILS IF: A verse, the fee's form or a named person is added.
- 4. The scholar row (found by title) names the letter's path in its why. Its list line names the path. The notes name the row and the letter. FAILS IF: Any of the three links is missing.

**Blinds:**

- Remove 'Nothing has been sent'. -> Leg 1.
- Insert an Arabic phrase. -> Leg 3.
- Add 'and the form of the platform's fee'. -> Leg 3.
- Drop 'A.12.3'. -> Leg 2.
- Remove the path from the row's why. -> Leg 4.

**Pins:**

- test_w594_the_owners_rulings_of_2026_10_05b_hold_in_code_and_in_canon (42645-42672): open gated ids in the list -> Keep the row's id in its amended line.
- test_w1131_the_local_prompt_names_every_row_waiting_on_the_owner_and_keeps_off_the_cloud_branch (92373-92395): every open gated id named in the notes -> Keep.
- test_w1192_the_v44_assessment_is_section_35_its_kept_gaps_are_rows_and_each_owner_row_is_listed_twice (leg E): 'FU-x (W1192):' with 'Recommended' -> Keep both in the amended line.

**Rulings it rests on:**

- P5.17 clause 7: WITH THE OWNER, a named scholar or trusted institute
- R7 / A.12.3: a named scholar approves composed religious teaching before a learner sees it
- OWNER RULING 2026-10-06 (FU-448: the gate covers the learner path only)
- OWNER RULING 2026-11-20 evening: P5.21's gate closed until P5.12's headings and a safeguarding review
- Never AI-generate Quran Arabic; never score recitation; children do not use the tools (2026-10-13)

**Risks:**

- The Owner may prefer to approach a scholar personally. Draft only if the Owner accepts or asks.
- A letter written in the session's voice must avoid a gendered pronoun (test_w1143).

### D-SCHOLAR-REQUEST's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 3's 'no fee' is a substring check. It would also match 'feedback', so a correct letter could go red. Match 'fee' as a whole word.

**Pins the plan missed:**

- None missed. test_w948 reads only its two named letters, and test_w1132 only its own letter. test_w1190's notes strings for the letters (:98648 and the FU-1283 line) are kept by a new bullet. No test globs docs/letters.

**Conflicts with a ruling:**

- 'Preparation only ... If the Owner declines the recommendation, this round is dropped' is overtaken. NG6 (2026-11-22) accepted an OWNER row to ask a scholar or trusted institute now. The recommendation it accepted had the cloud session draft the request, as FU-1283's was drafted. The row's why reads 'RECOMMENDED (accepted 2026-11-22)', and the round is not conditional.

**Bar demands the plan missed:**

- The letter's 'what is withheld now' leaves out the five Religion research tools. On those tools a model's composed answer is withheld until a named scholar on the roster approves that exact text (OWNER ruling 2026-10-11; vision :1439-1440; held by test_rel_a_model_composed_religious_answer_is_withheld_until_a_named_scholar_approves_that_text). P5.20 clause 8's screening before a scholar reads also starts only once a scholar is named.

**Fixes asked for:**

- Name the research tools' withheld model answers in the letter beside the existing scope: A.12.3's adult curriculum and tajweed items, P5.17 clause 4's attestation wording, and P5.21's approval pack, whose gate stays closed until P5.12's headings and a safeguarding review.
- The list line and leg 4 follow whichever round registers the row, normally W1192: 'FU-x (W1192): ask a scholar or a trusted institute now, sending the request drafted in docs/letters/SCHOLAR_REVIEW_REQUEST.md. Recommended, and accepted on 2026-11-22.' The notes bullet goes in 'Still yours', not step 5 (test_w1164, test_w1180 and test_w1188 pin step 5 to FU-1165).
- Checked otherwise:
  - docs/letters holds three files today;
  - the test_w1132 letter fragments;
  - the roster stays the Owner's (P5.21 :7550);
  - the letter carries no Arabic script, no fee's form and no a gendered pronoun (test_w1143).

**Re-sized:** S. After W1192 registers the row.

## W1200 - C3, C4, D-FU1086: The plan says what is held and what was built: PLAN NOW names the hold on P5.22, a test holds the optimiser's queue disclosure, FU-1086 says what remains, and P5.22 records W970-W977

**Closes:** Gap 21 and correction 17 (C3); gap 24 (C4); correction 3, with the v40 body's merged P5.22 evidence (D-FU1086); their rows

**Owning item:** P5.22 (C3, D-FU1086); P2.40 (C4)

**Held on:** W1193

**Rows:**

- FU-1874 (P5.22, low): PLAN NOW names P2.40 as next and says neither that it closes only on the final audit nor that its rows can be worked now
- FU-1875 (P2.40, low): No test holds the optimiser's statement that nothing drains its queue

**Files:** agentic_core/plan_followups.py (C3 only); (C4 and D-FU1086 touch only the shared register, plan and spine)

**-k:** -k "plan_now_says_an_item_held or queued_allocation_says_nothing_drains or fu1086 or test_w462_ or test_w469_ or test_w478_ or test_w486_ or test_w487_ or test_w499_ or test_w501_ or test_w549_ or test_w786_ or test_w787_ or test_w999_ or test_w1107_ or test_w747_ or test_w970_ or test_w972_ or test_w973_ or test_w977_ or test_w492_ or test_resource_optimizer_surfaced or test_endpoints_no_500_on_edge_inputs or test_w1143_"

**Notes from the lead:**

Disjointness: only C3 changes code (plan_followups.py), so this is a bundle.

C3:
- The Next line says a held item's rows can be worked now, and names separately the first open build item a round can close.
- 'Then, in order' marks each held item with its open count.
- P3.30's text has no hold today (ABSENT, not PARTIAL), so its HELD UNTIL line is new.
- The hold lines go at i40+2 and i41+2 (test_w786).
- slot_source on the P5.22 row.

C4: on the circuit-open path, assert queue_depth == 0 or reword that path's basis.

D-FU1086:
- The title becomes 'The final audit's instrument is built (W970-W977); it is not yet calibrated or run'.
- Leg 2 matches 'no region capped' or 'nothing capped', because the why already says 'uncapped'.
- The why must not use 'Read from code' (test_w747 :67128-67130).
- The BUILT line names no FU id but FU-1086.
- test_w747 :67104 and :67126 change on purpose.

### C3 as planned (cluster C; size S, 1 round(s))

**Title:** PLAN NOW says that P2.40, P2.41 and P3.30 are held until the final audit, and names the first open build item that is not held

**Closes:** Gap 21 (n=21), correction 17 and the W1192 row for the Next line.

**Owning item:** P5.22. The hold being stated is P5.22's, and the renderer's files sit in an area retired with P2.18, so the row names its own slot.

**Owner-gated:** No. It states the Owner's rulings of 2026-10-11 and 2026-10-12, as W786 recorded them, and keeps W469's 'next in plan order'.

**Depends on:** W1192 (the row). Independent of the other rounds.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | plan_now names the first open item in plan order | agentic_core/plan_followups.py:551-591 ('next': open_items[0]). |
| EXISTS | render_plan_now writes the Next sentence from row counts alone, with no hold | plan_followups.py:1415-1437. No reader of a hold exists, which is the gap. |
| EXISTS | plan_items reads only each item's header line | plan_followups.py:198-231 matches ^ (P\d+\.\d+)\b; continuation lines are never read. |
| EXISTS | P2.40 and P2.41 state the hold in their own text | FABLE:4801 ('This item closes on that audit') and 4803 ('this item closes on it'). The Next line is at FABLE:1123 and WORKSTATION_IDBO_LIVING_PLAN.md:361. |
| PARTIAL | P3.30's ACCEPT (5) is held on the final audit in its own text | FABLE:6622 says only that 'M3 re-runs with M1 and M2'. REMAINING_WORK_MEASURED.md:86 and :89 record that this is the final audit. |
| EXISTS | P4's items are the Owner's switches, declared in the phase heading | FABLE:6712 'delivered_by: owner-switch', read at plan_followups.py:215-229. No per-item marker is needed to skip P4.x. |
| EXISTS | Guards pin the Next line's opening and its rider count | test_w469 at 16068-16069 (block equality in both docs), 16075 (f"  Next: {first_open} "), 16434-16443 (the rider count is the word before the first word starting 'follow-up') and 16461. test_w786 at 70673-70682 pins lines i40+1 and i41+1. test_w549 at 33590-33612 renders a fake plan. |
| EXISTS | The dashboard's Next line is drawn from plan_now.next and pinned | TransformationDashboard.tsx:493-499; TransformationDashboard.test.tsx:184; test_w1107 at 91242. Not changed by this round. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- PLAN NOW names P2.40 as next and does not say it closes only on the final audit (P5.22, low)

**Rows it closes:**

- The row above, closed as built.

**Changes:**

- agentic_core/plan_followups.py: plan_items reads a structured hold line in an item's own block, '      HELD UNTIL P#.#:', into held_until; a mention elsewhere in prose is never read. plan_now gives each open item held_until and held (true while that item is open) and adds next_unheld: the first open item with delivered_by 'build' that is not held. render_plan_now keeps '  Next: <slot> <title> — <rider sentence>'. After it, it adds that the item is held until the named item has run, and names the first open build item not held, with its riders. It marks each held item in 'Then, in order'. check() reports a hold that names no plan item, or names the item itself.
- docs/FABLE_DELIVERY_PROMPT.md: Three hold lines. After P2.40's W786 line (i40+2) and after P2.41's (i41+2): 'HELD UNTIL P5.22: this item closes only on the final audit, after the fifth phase and the sign-in readiness round (the rulings of 2026-10-11 and 2026-10-12 recorded above).' After P3.30's ACCEPT: 'HELD UNTIL P5.22: ACCEPT (5)'s re-run of M3 with M1 and M2 is the final audit, by the rulings recorded at P2.40; its rows can still be closed by rounds.' Then the PLAN NOW block, re-rendered by scripts/followups.py render.
- docs/WORKSTATION_IDBO_LIVING_PLAN.md: The PLAN NOW block re-rendered (CRLF).
- docs/FOLLOWUPS.json: Close the row.
- integration_tests/test_mvp_spine.py: The new guard.

**Guard:** test_wXXXX_p522_plan_now_says_an_item_held_for_the_final_audit_is_held_and_names_the_first_a_round_can_work_on

- Render a fixture plan with two build items held until a third, an owner-switch item and a free build item. The Next line opens '  Next: <first held> ', says it is held until the named item, and names the free build item as the first open build item not held. FAILS IF: The marker is ignored, or the first item not held is chosen wrongly.
- The same fixture with the named item marked ✅ DONE. No hold is said and nothing is held. FAILS IF: A hold is said whatever state the named item is in.
- 'Then, in order' marks each held item and no free one. FAILS IF: A held item is listed like a free one.
- The owner-switch item is never named as the first build item not held. FAILS IF: delivered_by is ignored.
- On the real plan and register: next['slot'] == 'P2.40'; P2.40, P2.41 and P3.30 have held_until 'P5.22'; both docs' blocks equal render_plan_now's output and their Next line contains the hold. FAILS IF: The markers are missing or the documents were not re-rendered.
- A fixture whose hold names 'P99.9' gives a check() problem. FAILS IF: A mistyped hold silently holds nothing.
- 'HELD UNTIL P9.3' written mid-sentence in another item's prose holds nothing. FAILS IF: The marker is parsed anywhere in the text.

**Blinds:**

- plan_items ignores the hold line. -> Legs 1 and 5 go red.
- Say 'held' whenever held_until is set, whatever the named item's state. -> Leg 2 goes red.
- Pick the first open item as the first one not held. -> Leg 1 goes red.
- Drop the delivered_by filter. -> Leg 4 goes red.
- Commit without re-rendering the docs. -> Leg 5 and test_w469's block equality go red.

**Pins:**

- test_w469_the_plan_carries_every_followup_and_keeps_itself_current (16068-16069): fu._block(prompt, fu.PLAN_BEGIN, fu.PLAN_END) == now == fu._block(living, fu.PLAN_BEGIN, fu.PLAN_END) -> Re-render both blocks in the round. No test edit.
- test_w469_the_plan_carries_every_followup_and_keeps_itself_current (16075): assert f"  Next: {first_open} " in now -> Kept: 'Next: P2.40 ' still opens the line.
- test_w469_the_plan_carries_every_followup_and_keeps_itself_current (16434-16443): _idx592 = next((i for i, w in enumerate(_words592) if w.startswith("follow-up")), None) ... _words592[_idx592 - 1] == str(_openride592) -> Kept: the hold text follows the rider sentence, so the first 'follow-up' word is still the rider count's.
- test_w469_the_plan_carries_every_followup_and_keeps_itself_current (16461): assert f"  Next: {second_open} " in doc and f"  Next: {second_open} " in living_doc -> Kept.
- test_w786_p240_and_p241_say_they_close_on_the_final_audit (70679-70682): assert p[i40 + 1].startswith("      UPDATED 2026-11-10 (W786)") ... assert p[i41 + 1].startswith("      UPDATED 2026-11-10 (W786)") -> Kept: the hold lines go at i40+2 and i41+2.
- test_w549_the_horizon_spec_agrees_with_the_code_it_routes_into (33600-33612): "2 have" in _joined or "0/2" in _joined; "closes on its ACCEPT clause" in _rendered; "UNEXAMINED" -> Kept: the fake plan has no hold line.

**Rulings it rests on:**

- OWNER RULINGS 2026-10-11 and 2026-10-12, recorded at P2.40: one mid-way audit, and the next audit is the final one, after the fifth phase and the readiness round.
- W469: PLAN NOW says what is next in plan order. Kept, since P2.40 stays first.
- W786: P2.40 and P2.41 close on the final audit.
- W499: P4 is delivered_by owner-switch.
- P5.22 ACCEPT (FABLE:7556-7567).

**Risks:**

- P5.22's parsed title ends with a comma ('THE FINAL AUDIT — UNCAPPED,'). Trim trailing punctuation when quoting it.
- A hold line must never begin ' P' (plan_items would read it as an item). It begins with six spaces and 'HELD'.
- If W1192 adds the optimiser row to P2.40, the Next line reads '1 follow-up rides it'. The design handles riders above zero.

### C3's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'P3.30's ACCEPT (5) is held on the final audit in its own text: PARTIAL' should be ABSENT. FABLE:6622 reads only '(5) M3 re-runs with M1 and M2 when this item's rows close...', and no line follows it: 6623 is P3.31. The rest holds: plan_now 551-591, render_plan_now 1415-1437 (the 'Then, in order' line at 1454-1456), plan_items matching '^ (P\d+\.\d+)\b', P4's delivered_by owner-switch (FABLE:6712), the Next line at FABLE:1123 and LIVING:361.

**Guard legs that could not fail:**

- None. Legs 6 and 7 fail on loose parsing. Leg 5 overlaps test_w469 but adds held_until.

**Pins the plan missed:**

- None that break. test_w469 16068-16069 needs a re-render; 16075 keeps '  Next: P2.40 '. 16434-16443 runs in a scratch copy where first_open has riders, so the first 'follow-up' word stays the rider count while the hold text follows it. 16461; test_w786 70679-70682 pins i40+1 and i41+1 only; test_w549 33600-33612; test_w1107 checks only key inclusion (91233).

**Conflicts with a ruling:**

- W469 ('next in plan order') and OWNER RULING 2026-10-12 (P2.40's rows fixed before the fifth phase). After W1193, P2.40 carries C4's open row, and P3.30 carries cluster A's new rows on top of its open one ('P3.30 1/179' at FABLE:1133). A Next line that names 'the first open build item not held' (P3.32) points a reader past rows a round can work now. The hold is on each item's close, not on its rows, and the plan's own P3.30 hold line says its rows can still be closed.

**Bar demands the plan missed:**

- For a held item with open riders, the line must say its rows can be worked now. 'The first item a round can close' must be named separately from 'where a round works next'.

**Fixes asked for:**

- Render, for example: 'Next: P2.40 ... — N follow-up(s) ride it; its rows can be worked now, and the item closes only on the final audit (P5.22). The first open build item a round can close: P3.32 ...'. Mark held items in 'Then, in order' with their open count.
- Add a leg: a held fixture item with open riders is said as workable, and is still skipped for 'can close'.
- Fix the P3.30 verdict. Carry slot_source on the P5.22 row (agentic_core/plan_followups.py is in a retired area). Depend on W1193.

**Re-sized:** S, 1 round (C4 can be batched in).

### C4 as planned (cluster C; size XS, 1 round(s))

**Title:** A queued allocation says that nothing drains its queue and nothing is pending, and a guard holds it

**Closes:** Gap 24 (n=24) and the W1192 row for it.

**Owning item:** P2.40, the register's route for agentic_core/optimizer/. The row closes on its own; the item closes only at P5.22.

**Owner-gated:** No.

**Depends on:** W1192. Independent of the other rounds.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | Both QUEUED returns carry pending False and a queue_basis | agentic_core/optimizer/scheduler.py:19-30 (_queue_disclosure), spread at :53 (circuit-open path) and :58. engine.py:43-47 passes it up, to the top of POST /api/v1/optimizer/allocate. |
| EXISTS | No suite test reads pending or queue_basis | test_w492 at 20968-20972 asserts only tier_recognised False and status in (QUEUED, REJECTED). test_resource_optimizer_surfaced (4042-4057) drives SUCCESS only. |
| EXISTS | The property is asserted only by a manual probe | scripts/_w492_probe.mjs:58-60. .github/workflows holds only documentation_sync.yml and spine.yml, and neither runs it. |
| EXISTS | The fabric quotes the basis in its 'not executed' error | resource_fabric.py:2183-2187. |
| EXISTS | A fresh optimiser per request means REJECTED cannot come back on this call | scheduler.py:13-17 builds circuit_open False per instance, and the route builds the engine per request. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- No test holds the optimiser's statement that nothing drains its queue (P2.40, low)

**Rows it closes:**

- The row above, closed as built.

**Changes:**

- integration_tests/test_mvp_spine.py: A new test only. test_w492 is not edited.

**Guard:** test_wXXXX_p240_a_queued_allocation_says_nothing_drains_it_and_nothing_is_pending

- POST /api/v1/optimizer/allocate with an unrecognised tier answers status == 'QUEUED' exactly, pending is False, and queue_basis contains 'nothing drains' and 'NOT scheduled'. FAILS IF: The disclosure is dropped or pending becomes true.
- The scheduler called directly with a monitor reporting usage past the threshold answers QUEUED with the same disclosure. FAILS IF: The circuit-open spread at :53 is lost.
- The fabric's resource_optimizer composition with an unrecognised tier gives a 'not executed' error that carries the queue_basis text. FAILS IF: The fabric drops the basis.
- A recognised tier answers SUCCESS with no queue_basis. FAILS IF: The disclosure is spread onto work that did run.

**Blinds:**

- Remove **self._queue_disclosure() from the return at :58. Do not delete the method, which would fail with AttributeError for the wrong reason. -> Leg 1 goes red.
- Set 'pending': True. -> Leg 1 goes red.
- Drop 'which nothing drains' from queue_basis. -> Leg 1 goes red.
- Remove the spread at :53. -> Leg 2 goes red.
- Drop queue_basis from the fabric's error. -> Leg 3 goes red.

**Pins:**

- test_w492_the_page_says_what_the_engine_said (20968-20972): assert al2.get("tier_recognised") is False, al2 / assert al2["status"] in ("QUEUED", "REJECTED"), al2 -> Unchanged. The new test holds 'QUEUED' and the disclosure.
- test_resource_optimizer_surfaced (4042-4057): a["status"] == "SUCCESS" ... -> Unchanged.
- test_endpoints_no_500_on_edge_inputs (4121): ("/api/v1/optimizer/allocate", {"domain": "x", "requirements": {"CPU": "lots", "RAM": ""}}) -> Unchanged.

**Rulings it rests on:**

- P5.10 clause 2: a fix is guarded on its property over the whole payload.
- P5.10 clause 8 (triage): a small row is batched or done cheaply.
- W492: the disclosure itself. FU-617's ruling (W754) archived optimization/aro.py, a different module.

**Risks:**

- Adding the row to P2.40 in W1192 changes PLAN NOW's Next line until this round closes it.

### C4's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- None. Verified scheduler.py:19-30 with the spreads at :53 and :58, engine.py:43-47, test_w492 20968-20972, test_resource_optimizer_surfaced 4042-4057 (SUCCESS only), the fabric's error at resource_fabric.py:2183-2187, and a fresh scheduler per request (circuit_open False at :16).

**Guard legs that could not fail:**

- None. Each blind turns a named leg red, and removing the spread rather than the method avoids the AttributeError false red.

**Pins the plan missed:**

- None. The round adds a test only. test_w492 (20968-20972), 4042-4057 and the 4121 edge probe are unchanged.

**Conflicts with a ruling:**

- None on rulings: FU-617 (W754) covered optimization/aro.py. Numbering: the row is W1193's.

**Bar demands the plan missed:**

- P5.10 clause 2 (whole payload). On the circuit-open path (:50-53) nothing is put on the queue (queue_depth 0), yet the basis says 'queued on this request's own in-process queue'. Leg 2 would hold that sentence as true. Assert queue_depth == 0 there, or reword that path's basis.

**Fixes asked for:**

- Closing the P2.40 row re-renders PLAN NOW: the Next line goes from '1 follow-up rides it' back to none. List docs/FOLLOWUPS.json, docs/FABLE_DELIVERY_PROMPT.md and docs/WORKSTATION_IDBO_LIVING_PLAN.md, and add test_w469 to the -k.
- Batch it into C3 (P5.10 clause 8: a small row rides a round already in the file).

**Re-sized:** XS; batch into C3 rather than a round of its own.

### D-FU1086 as planned (cluster D; size XS, 1 round(s))

**Title:** FU-1086 says what remains of the final audit, and P5.22 records what W970–W977 built

**Closes:** Correction n=3 (FU-1086's title and why), together with v40 merged evidence 0 and its insight (P5.22 carries no BUILT line).

**Owning item:** P5.22 (FU-1086 is its one row)

**Owner-gated:** None for the text. The Owner ruled on 2026-11-06 (W754). The runs come after Phase 5 and the sign-in readiness round, and the local-model run is on the Owner's machine.

**Depends on:** W1192, for order only. It should land before cluster C's LIVING_STRATEGY_MAP.md round (correction 4 there quotes FU-1086's new title in the Authorise step at :64). This round does not touch that file.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| PARTIAL | FU-1086's title and why | Open, high, slot P5.22, owner_gated false, source W747. Title: 'OWNER DECISION: the uncapped, census-partitioned final audit has no item that builds or runs it'. The why lists six properties and lacks '(7) both configurations ran'. slot_source: 'Owner ruling 2026-11-06 (W754) ...'. |
| EXISTS | test_w747's pins | test_mvp_spine.py:67104 pins the title. :67126 asserts ruled[0]['title'].startswith('OWNER DECISION:'). :67118-67121 require source == 'W747' and slot P5.22. These are the only spine pins on FU-1086 (grep). |
| ABSENT | A BUILT record in P5.22 | FABLE:7556-7567 holds the charter and ACCEPT (1)-(7) only. |
| EXISTS | The built instrument | Commits ac4628ca (W970), 70282db5 (W972), fc19be10 (W973) and 6b6162c4 (W977), all 2026-11-13. Guards test_w970 (:81947), test_w972 (:82072), test_w973 (:82185) and test_w977 (:82484). Scripts scripts/audit_surface_census.py, scripts/audit_completeness.py and scripts/workflows/fidelity_audit_final.js. |
| EXISTS | What remains, on P5.10 | FU-993 (planted defects) and FU-1036 (both configurations): both open, slot P5.10. |
| EXISTS | P5.22's text may not name FU-993 or FU-1036 | plan_followups.check (:1716-1727) reports an open item's text that names an open row riding another item. |
| EXISTS | Generated copies of the title | FABLE:1196 and WORKSTATION_IDBO_LIVING_PLAN.md:431, rendered in lockstep (test_w462). |
| EXISTS | REMAINING_WORK_MEASURED.md:41 'No such instrument exists' | Stale: dated 2026-11-10, before W970. test_w787's docstring says the page is re-measured, not edited. |

**Changes:**

- docs/FOLLOWUPS.json: FU-1086 title: 'The final audit is built but not yet calibrated or run: calibration against planted defects, then a run in each configuration after Phase 5 and the sign-in readiness round'. The why says:
  - P5.22 is the item, on the Owner's ruling of 2026-11-06 (W754);
  - W970 built properties 1-2 (exactly one slice, union equals census); W972 built 6 (earlier ledgers pinned); W973 built 3, 4, 5 and 7 (nothing capped, a failed or empty slice blocking completeness, the measured commit, both configurations); W977 built the workflow;
  - what remains: calibration first (P5.10 clause 5, FU-993), the local-model configuration on the Owner's machine (FU-1036), then both runs, on which P2.40 and P2.41 close;
  - a 'RETITLED' note quoting the old title.
  Severity high, slot P5.22, source W747 and not gated: all kept. Then render. Answered on the morning of 2026-11-22 (W1193c): the why also keeps FU-1086's ruling of the morning of 2026-11-22.
- docs/FABLE_DELIVERY_PROMPT.md: P5.22, after ACCEPT (7): 'BUILT (W970–W977, 2026-11-13): (1)-(2) W970 (scripts/audit_surface_census.py); (6) W972; (3), (4), (5), (7) W973 (scripts/audit_completeness.py); the workflow W977 (scripts/workflows/fidelity_audit_final.js). NOT YET: calibration against planted defects (P5.10 clause 5) and the two runs, after Phase 5 and the sign-in readiness round.' It names no FU id but FU-1086. Answered on the morning of 2026-11-22 (W1193c): the BUILT line is also to say the audit runs in December.
- docs/WORKSTATION_IDBO_LIVING_PLAN.md: Re-rendered, keeping CRLF.
- integration_tests/test_mvp_spine.py: test_w747: change the expected title (:67104). Replace the startswith('OWNER DECISION:') assertion (:67126) with 'not owner_gated, and the title does not say no item builds or runs it', and add a comment saying why. Append the new test.

**Guard:** test_wNNNN_fu1086_the_final_audits_row_says_what_remains_and_p522_records_what_w970_to_w977_built

- 1. FU-1086 is open on P5.22: severity high, not gated, source W747. Its title neither contains 'no item that builds or runs it' nor starts 'OWNER DECISION:', and it names calibration and the runs. FAILS IF: The old title stays (it does on the unchanged tree).
- 2. FU-1086's why carries each of P5.22's seven properties by its distinctive words: 'exactly one slice', 'union', 'capped', 'failed or empty', 'measured commit', 'earlier ledgers', 'both configurations'. FAILS IF: A property is missing. Property 7 is missing today.
- 3. P5.22's text has a line starting 'BUILT' that:
  - names W970, W972, W973 and W977, each with a spine guard 'def test_w{n}_p522_';
  - names three scripts that exist;
  - says the calibration and the two runs are still to come;
  - names no FU id other than FU-1086. FAILS IF: No BUILT line (the case today), a round named without its P5.22 guard, a missing script, or a row riding P5.10 named in P5.22's text.

**Blinds:**

- Restore the old title. -> Leg 1 (and test_w747's updated pin).
- Drop 'both configurations' from the why. -> Leg 2: property 7 is missing.
- Delete the BUILT line. -> Leg 3 finds no BUILT line.
- Write 'calibration is FU-993' into the BUILT line. -> Leg 3 sees an FU id other than FU-1086. fu.check, and with it test_w462, also go red.
- Name W974 in the BUILT line. -> Leg 3: the spine has no test_w974_p522_ guard.

**Pins:**

- test_w747_the_external_prompts_review_is_recorded_and_its_gaps_are_registered (67104): ('OWNER DECISION: the uncapped, census-partitioned final audit has no item that builds or runs it', 'P5.22') -> Change on purpose to the new title. Slot P5.22 and source W747 stay.
- test_w747_the_external_prompts_review_is_recorded_and_its_gaps_are_registered (67126): ruled[0]["title"].startswith("OWNER DECISION:") -> Replace with: not owner_gated, and the title does not claim that nothing builds it. Comment that the Owner ruled on 2026-11-06 and W970-W977 built the instrument.
- test_w462_followup_register_is_scheduled_and_in_lockstep (11328+): the generated blocks equal render() of the register (FABLE:1196, LIVING_PLAN.md:431) -> Re-render.

**Rulings it rests on:**

- OWNER RULING 2026-11-06 (W754): FU-1086 chartered as P5.22, with seven properties each driven red (FABLE:288)
- Ruling 2026-10-12: the final audit is uncapped and census-partitioned, its instrument calibrated first, and run after Phase 5 and the sign-in readiness round
- P2.40 and P2.41 close on the final audit (FABLE:4801, :4803)
- FU-993 and FU-1036 ride P5.10

**Risks:**

- Cluster C's map round must take the new title. If it lands first, its Authorise line will name an old title.
- REMAINING_WORK_MEASURED.md:41 stays wrong until it is re-measured. A local session reads it first (RESUME step 2), but the plan's P5.22 now says BUILT.

### D-FU1086's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 2's 'capped' is already met by 'uncapped' in FU-1086's current first sentence ('the final audit is uncapped'). A blind that drops property 3 would stay green. Match 'no region capped', 'no slice capped' or 'nothing capped' instead.

**Pins the plan missed:**

- None beyond the plan's. No other spine or vitest pin carries FU-1086's title. MethodAppraisal.fixture.json:350 holds the old title in a frozen fixture, and test_w1003's read at :83991 does not compare titles. One extra constraint: test_w747 :67128-67130 requires any row whose why contains 'Read from code' to have a HYPOTHESIS title, so the new why must not use that phrase.

**Bar demands the plan missed:**

- The proposed title 'The final audit is built but not yet calibrated or run' overstates. W970 to W977 built the instrument, and the audit itself has not run (P5.22 :7558-7560). Use 'The final audit's instrument is built (W970-W977); it is not yet calibrated or run ...'.

**Fixes asked for:**

- Retitle FU-1086 to say that the instrument is built. Keep severity high, slot P5.22, source W747, tier 2 and not gated. The why carries property 7 as 'both configurations'.
- Tighten leg 2's property-3 match as above. Keep leg 3's rule that the BUILT line names no FU id other than FU-1086, since FU-993 and FU-1036 ride P5.10 and fu.check forbids naming them.
- Checked and sound otherwise:
  - test_w747 pins at :67104 and :67126;
  - the generated copies at FABLE:1196 and LIVING_PLAN.md:431;
  - the commits ac4628ca, 70282db5, fc19be10 and 6b6162c4 (2026-11-13), and fc19be10's message covers 'both configurations, or why not';
  - the guards test_w970_p522_, w972_p522_, w973_p522_ and w977_p522_;
  - the three scripts exist;
  - W974 is not a P5.22 guard, so that blind is valid.

**Re-sized:** XS. Land after W1193 and before cluster C's LIVING_STRATEGY_MAP.md round, which quotes the new title at :64.

## W1201 - D-FIRST-OFFER, D-GATE, C2: Before the teacher interviews, the first-offer papers say the Domain tool is free; the seventh gate reads the Owner's bar; the business guard reads row status and counts money however it is written

**Closes:** Gap 3 and correction 12 (D-FIRST-OFFER); the seventh gate's computation (D-GATE); gaps 20 and 25 (C2); their rows

**Owning item:** P3.30 (first offer); P5.10 (gate computation, both guard rows; the money row under clause 2)

**Held on:** W1193 (the map, the cost model's cell and the brand screen are restated first)

**Rows:**

- FU-1872 (P5.10, low): The business documents' guard checks only that a named row exists, so two documents named closed rows as standing between a step and being relied on
- FU-1873 (P5.10, low): The business documents' guard counts a money figure only when the currency comes first
- FU-1876 (P3.30, medium): The first-offer papers present a free Domain tool as something people pay for, and the drafts' cost answer says a price may come
- FU-1879 (P5.10, low): The seventh investment gate is computed as evidenced when any docs file is named 'interview', where the Owner ruled on 2026-11-22 that it needs five recorded interviews and the Owner's recorded choice

**Files:** docs/business/FIRST_OFFER_CANDIDATES.md; docs/business/public/FIRST_OFFER_DRAFTS.md; docs/business/NAME_AND_BRAND_SCREEN.md; (D-GATE and C2 touch only the spine)

**-k:** -k "the_first_offer or business_document_calls_open or test_w703_ or test_w903_ or test_w912_ or test_w913_ or test_w920_ or test_w923_ or test_w962_ or test_w963_ or test_w1126_ or test_w1136_ or test_w1137_ or test_w1149_ or test_w1150_ or test_w1151_ or test_w1153_ or test_w1154_ or test_w1155_ or test_w1120_ or test_w1174_ or test_w1192_ or test_w462_ or test_w469_ or test_w1143_"

**Notes from the lead:**

D-FIRST-OFFER:
- :59 says that nothing is charged for using a Domain tool. The Owner's charges fall only on generating an enterprise (a price once, set and not yet charged) and on that enterprise's profit (a quarter, taken first). No figure is given.
- :13 and NAME_AND_BRAND_SCREEN.md:62 are reworded to match.
- Anchor on W1192's interview-guide text: both outputs, labelled, are already recorded there.
- Leg 6 reads the row after the apply has closed it.
- The brand screen's LICENSE bullet is a negative control for leg 4.
- P5.7's note goes after W1192's ruling there.

D-GATE: test_w1126 reads the gate as evidenced only with five filled notes in the template and a dated record of the Owner's choice, never a file named 'interview'. COST_MODEL.md's bar is W1192's.

C2:
- Label every plant and assert each plant's own message.
- Add the blind 'drop rule (b)'.
- 17 call lines read statuses from root/docs/FOLLOWUPS.json.
- The money row is on P5.10 clause 2, with slot_source.
- Any round that later closes FU-417, FU-1072 or FU-1086 must restate the map.

### D-FIRST-OFFER as planned (cluster D; size S, 1 round(s))

**Title:** The first-offer papers say the Domain tool is free and ask only what a person spends today, before the teacher interviews

**Closes:** Gap 3 (cluster D n=3) and correction n=12. Closes the first-offer row on P3.30.

**Owning item:** P3.30 (the row W1192 registers), with a dated note at P5.7 clause 1

**Owner-gated:** The interview guide's questions, the willingness-to-pay questions about today's spending and the notes template were accepted by the Owner (FU-1818, 2026-11-20 evening) and are not rewritten. The added question on taking an idea on to an entity is put to the Owner and not added. The interviews and the choice of first offer stay the Owner's.

**Depends on:** W1192 (the row). Must land before FU-1818's interviews. Independent of cluster C's _w703_faults rounds: it does not edit that function, but its documents must pass whatever rules those rounds add.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The candidates paper frames the tool as bought | FIRST_OFFER_CANDIDATES.md: - :40 'will use, and pay for, a tool'; - :42 'the person who would pay is a school whose buying route this business cannot reach'; - :31 '\| Would anyone pay \| NOT MEASURED ×3 \|'. Two present-spend places are kept: :6 and :62-67 'Willingness-to-pay questions that do not lead', and :74 'Who decides and who pays'. |
| EXISTS | The public drafts ask whether anyone would pay and answer that a price may come | FIRST_OFFER_DRAFTS.md: - :32 'whether anyone would pay, and who would buy it'; - :40 'demand, the price and the buyer'; - :59 'No price is set; a price is the Owner's to set, by the formula the Owner ruled. [owner decision]'. :13 says that no price is named in any draft. |
| EXISTS | The brand screen's claim row | NAME_AND_BRAND_SCREEN.md:59 'Demand, the price and the buyer are not measured \| `docs/business/FIRST_OFFER_CANDIDATES.md` \| 2, 3'. test_w1153 (:94168-94192) requires the register to equal the drafts' citations; the claim text only needs to be longer than 20 characters. |
| EXISTS | The rulings the papers break | P5.16 clause 1 (FABLE:7328-7330); the canvas at :26 and :52-53; COST_MODEL.md:59. P5.7 clause 1 (FABLE:6896-6899, chartered 2026-10-11) asks for 'the willingness-to-pay questions'. P5.7 carries no note on P5.16's narrowing. |
| EXISTS | test_w913's pins | - :77769: 'Would anyone pay' with NOT MEASURED ×3. - :77775: the hypothesis section has at least 2 '[hypothesis]', 'It would be refuted by' and '[owner decision]'. - :77779-77781: the WTP section's title; no digit anywhere in that section; 'Never name a price'. |
| EXISTS | test_w1151's pins | :94065 'Teachers and tutors who plan lessons against a named framework will use' (the new hypothesis keeps this prefix); :94073 'No price is set'. |
| ABSENT | A rule in _w703_faults against presenting a paid Domain tool | _w703_faults (:64827-64893) checks labels, paths, rows, routes, money figures, people counts, W963 claims and personal detail, not what is charged. test_w1155 (:94294-94298) reads only route modules. |

**Rows it closes:**

- The first-offer row (P3.30), closed as built

**Changes:**

- docs/business/FIRST_OFFER_CANDIDATES.md: - :40 becomes 'Teachers and tutors who plan lessons against a named framework will use a tool that drafts the plan and the feedback for them to check, and come back to it, because they check it anyway. [hypothesis]'.
  - :42's third refutation becomes '...or a school does not let its staff use a free outside tool for planning'.
  - :31's row becomes 'Would anyone use it again', NOT MEASURED ×3.
  - 'How to read this document' gains a bullet: the Domain tools are free by the Owner's ruling (plan item P5.16), so the willingness-to-pay questions ask what a person spends today [owner-defined, 2026-10-12]. It goes there because the WTP section may hold no digit.
  - :62-67 and :74 are unchanged.
- docs/business/public/FIRST_OFFER_DRAFTS.md: - :32 becomes '...whether teachers find a draft good enough to start from, whether they would come back to it, and how often the need recurs. NOT MEASURED. [observed: `docs/business/FIRST_OFFER_CANDIDATES.md`]'.
  - :40 becomes 'whether teachers would use it again, and how often the need recurs, each NOT MEASURED' with the same citation.
  - :59 becomes 'What does it cost? Nothing: the Domain tools are free, for individuals and for institutions, by the Owner's ruling of 2026-10-12 (plan item P5.16); the only charge the Owner has set is for generating an enterprise, shown as set and not yet charged. [owner-defined, 2026-10-12]'. No figure: :13 says no price is named in any draft.
- docs/business/NAME_AND_BRAND_SCREEN.md: :59's claim becomes 'Whether teachers would use it again, and how often the need recurs, are not measured'. Its evidence and sections (2, 3) are unchanged.
- docs/FABLE_DELIVERY_PROMPT.md: P5.7, after its 2026-11-20 ruling, adds 'WNNNN (a note, not a ruling): P5.16 clause 1, ruled on 2026-10-12, the day after this item was chartered, makes every Domain free for individuals and institutions, so clause (1)'s willingness-to-pay questions ask what a person spends today and never price the tool; the first-offer papers say so.' Re-render after the row closes.
- docs/FOLLOWUPS.json: Close the P3.30 row --because built.
- integration_tests/test_mvp_spine.py: test_w913:77769 now reads the renamed row. test_w1151:94073 now holds the free answer: 'free', 'plan item P5.16' present; 'No price is set' and 'a price is the Owner's to set' absent. Append the new test.

**Guard:** test_wNNNN_the_first_offer_papers_say_the_domain_tool_is_free_and_ask_only_what_a_person_spends_today

- 1. The leading hypothesis section states no pay, paid, buy, bought, price, licence or subscription. FAILS IF: ', and pay for,' or 'the person who would pay' is restored.
- 2. No comparison criterion asks whether anyone would pay or buy, and the three demand rows are NOT MEASURED ×3. FAILS IF: The row is renamed back to 'Would anyone pay', or a demand cell is filled in.
- 3. The drafts' cost line says 'free', names 'plan item P5.16' and '2026-10-12', and says generating an enterprise is the only charge set and not yet charged. The drafts carry neither 'No price is set' nor 'a price is the Owner's to set' nor 'the price and the buyer', and the brand-screen row no longer says 'the price and the buyer'. FAILS IF: :59 or :40 is restored, or row 59 is not changed.
- 4. No sentence in the three documents pairs a reference to the tool with a money word. Tool references: 'the tool', 'this tool', 'lesson-plan tool', 'a tool that drafts', 'candidate A/B/C', 'Domain tool(s)', 'the offer'. Money words: pay/paid/buy/bought/price/priced/licence/subscription. Exempt: a sentence where 'no', 'not', 'never', 'nobody', 'none' or 'free' comes first. 'would' does not exempt a sentence. Negative controls, run through the same function: 'What do you pay now, in money or in time, for the way you do this?', 'When did you last pay for a tool for this kind of work?' and the canvas's 'Nobody pays for a domain tool' are not flagged. FAILS IF: A planted priced sentence passes, or a control is flagged.
- 5. P5.7's text carries the dated note naming 'P5.16 clause 1' and 'spends today'. FAILS IF: The note is removed.
- 6. The P3.30 row (found by title) is done, closed_by this round. FAILS IF: The row stays open.

**Blinds:**

- Restore ', and pay for,' at :40. -> Legs 1 and 4.
- Add '- A school would buy a licence for the lesson-plan tool. [hypothesis]' to the drafts' section 2. -> Leg 4. 'would' does not exempt it.
- Restore :59's 'No price is set; a price is the Owner's to set, by the formula the Owner ruled.' -> Leg 3.
- Rename the row back to 'Would anyone pay'. -> Leg 2.
- Delete the P5.7 note. -> Leg 5.
- Remove 'nobody' from leg 4's exempting words. -> The canvas control is flagged, which shows the rule is not over-broad when it passes.

**Pins:**

- test_w913_fu806_three_first_offers_are_compared_on_their_evidence_and_the_interviews_that_would_test_one (77769): for demand in ("Would anyone pay", "How often the need recurs", "What a person uses today") -> Change 'Would anyone pay' on purpose to the new label.
- test_w913_fu806_three_first_offers_are_compared_on_their_evidence_and_the_interviews_that_would_test_one (77779-77781): section("Willingness-to-pay questions that do not lead"); no \d in it; "Never name a price" -> Keep. Add nothing, and no dated label, to that section.
- test_w913_fu806_three_first_offers_are_compared_on_their_evidence_and_the_interviews_that_would_test_one (77775): lead.count("[hypothesis]") >= 2 and "It would be refuted by" and "[owner decision]" -> Keep.
- test_w1151_fu809_each_public_draft_is_headed_and_every_claim_names_a_test_that_runs_without_an_outside_model (94065): Teachers and tutors who plan lessons against a named framework will use -> Keep. The new hypothesis still contains it.
- test_w1151_fu809_each_public_draft_is_headed_and_every_claim_names_a_test_that_runs_without_an_outside_model (94073): assert "No price is set" in flat -> Change on purpose to the free answer, naming plan item P5.16.
- test_w1153_p57_each_name_says_what_was_searched_and_each_public_claim_is_one_row_of_the_register (94176-94192): the claims register equals the drafts' [observed: ...] citations by section -> Keep. Row 59's evidence and sections are unchanged. :59 cites no test.

**Rulings it rests on:**

- P5.16 clause 1 (2026-10-12): Domains free for individuals and institutions
- The canvas, ratified 2026-10-13: 'The tools are free', 'Nobody pays for a domain tool'
- P5.7 clause 1 (chartered 2026-10-11) and P5.7's BOUNDARY: nothing sent or published
- OWNER RULING 2026-11-20 evening: the first offer is chosen after five to eight interviews using the drafted scripts; nothing is published until then (FU-1818)
- FU-1185: the price formula prices an entity's deliverables, not a Domain tool

**Risks:**

- Leg 4 is a natural-language rule. Keep its word lists narrow and keep the controls, or it will collide with P5.7's required questions.
- Cluster C's new _w703_faults rules (currency after the figure; closed rows named as open) also apply to these papers. Run test_w703 after both.
- If the Owner rules on the interview questions first (chat question n=9), fold that change in here.

### D-FIRST-OFFER's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 6 reads the first-offer row's status. Close the row in the apply before the guard reads it (W1149 ran twice for this), or the leg is red in the very round that does the work.

**Pins the plan missed:**

- test_w1120 (:91764-91774) reads P5.7's block for its 2026-11-19 ruling. The round adds a dated note to P5.7, and the test is not in its -k.
- test_w1174 (:96353-96361) pins FU-1818's title prefix, OWNER and gated, source 'W1174 ', 'RECOMMENDED (accepted 2026-11-20, evening)', and '(FU-1818)' in P5.7's text. The Q9 record lands in FU-1818, and the test is not in the -k.
- test_w1153 (:94174) holds 'assert "[observed]" not in sec' for every numbered section of a public draft. The new :59 answer and any added bullet must cite with [observed: X] or use another label.
- If Q10 is folded in, three more pins apply. test_w1126 (:92064-92103) computes the seventh gate. test_w962 (:81451) forbids any '%' figure after '## Unit economics' in COST_MODEL.md, and the gates section (:61) comes after it. test_w1136 and test_w1137 also read COST_MODEL.md.

**Conflicts with a ruling:**

- Q9 (b), ruled 2026-11-22 (show the floor's and the local model's output on the same invented sample, each labelled with what served it), conflicts with this round's owner_gated line that the interview guide 'is not rewritten'. FIRST_OFFER_CANDIDATES.md:59 still says 'then only the floor's output on invented data'.
- Q10 (a), ruled 2026-11-22 (the seventh gate reads as evidenced at five interviews recorded in the notes template plus the Owner's recorded choice), was left to chat by the plan. COST_MODEL.md:65 and test_w1126 still read any docs/ file named 'interview' as evidence.

**Bar demands the plan missed:**

- The new :59 answer, 'the only charge the Owner has set is for generating an enterprise', is false. P5.16 clause 3 (FABLE:7339-7342; metabolism.PLATFORM_FEE_RATE = 0.25) also takes a quarter of each generated, profit-distributing entity's profit. It would repeat gap 7's own omission in a public draft. Say instead that nothing is charged for using a Domain tool, and that the Owner's charges fall only on generating an enterprise (a price once, set and not yet charged) and on that enterprise's profit (a quarter, taken first). Use no figure, because :13 says no price is named in any draft.
- The new answer contradicts two lines that stay. FIRST_OFFER_DRAFTS.md:13 says 'No price ... is named in any draft, because none exists', and NAME_AND_BRAND_SCREEN.md:62 says 'No claim in the drafts is about ... a price'. Reword both.
- Fold Q9 in. FIRST_OFFER_CANDIDATES.md:59 shows both outputs, each labelled. The notes template (:71-76) records which output the teacher judged. FU-1818's why carries the ruling.
- Fold Q10 in, or give it its own round. COST_MODEL.md:65 states the ruled bar, and test_w1126's 'A first offer the interviews support' changes from any file named 'interview' to the ruled count plus the recorded choice. Keep 'OWNER RULING 2026-11-19 (FU-1191)' and 'So no gate is evidenced today.'

**Fixes asked for:**

- Land after D-CANVAS, so that the public Q&A and the amended canvas name the fee the same way.
- Place the P5.7 dated note after W1192's 2026-11-22 rulings at P5.7. It names P5.16 clause 1 and 'spends today'.
- Leg 4's controls hold: the willingness-to-pay questions, 'When did you last pay for a tool' and the canvas's 'Nobody pays for a domain tool'. Add the brand screen's new LICENSE bullet from W1193 as a control, so that 'licence' in it is not flagged.
- Add test_w1120 and test_w1174 to the -k. With Q10 folded in, also add test_w962, test_w1136 and test_w1137.
- Checked and sound otherwise:
  - CANDIDATES :6, :31, :40, :42, :62-67 and :74;
  - DRAFTS :32, :40 and :59;
  - the brand screen's :59;
  - the test_w913 pins at :77769, :77775 and :77779-77781;
  - the test_w1151 pins at :94065 and :94073;
  - test_w1153's register stays equal to the drafts' citations, because :59 adds no [observed: X].

**Re-sized:** S if Q10 gets its own round. S to M with Q9 and Q10 folded in. Before FU-1818's interviews and after D-CANVAS.

*D-GATE has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

### C2 as planned (cluster C; size S, 1 round(s))

**Title:** Every business document calls open only a row that is open, names the rows it says are open, and has its money counted however it is written

**Closes:** Gap 20 (n=20), gap 25 (n=25) and the two W1192 rows for them. It also holds W1192's restatement of correction 4 and of the COST_MODEL.md:69 cell.

**Owning item:** P5.10 clause 1: the class guard at the mechanism every business document passes (_w703_faults). The clauses broken are P5.6 clause 5 and the P5.6/P5.7 money rule; both items are DONE and are not reopened.

**Owner-gated:** No. The Owner-ratified BUSINESS_PLAN.md and BUSINESS_MODEL_CANVAS.md are not edited. The rules are scoped so that their citations of closed rows (BUSINESS_PLAN.md:133, FU-1061) stay legal.

**Depends on:** W1192, which restates LIVING_STRATEGY_MAP.md steps 4-6 and COST_MODEL.md:69. Afterwards, every round that edits docs/business (in clusters B and D too) carries this test in its -k.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | _w703_faults checks only that a named row exists | test_mvp_spine.py:64848-64850 (for rid in re.findall(r"row (FU-\d+)", text): if rid not in row_ids). Its signature (64827) receives ids, not statuses, from 13 call sites. |
| EXISTS | Only the hardening brief's guard reads status | test_w912 at 77729-77733 requires every named row open, with FU-812 exempt. test_w903 (77306-77341) requires only that each step has a 'Between this step and being relied on' line. |
| EXISTS | The map names done rows and a mislabelled row | At HEAD: LIVING_STRATEGY_MAP.md:77-78 names FU-849 (done W1127); :90-92 name FU-1151 (done W1121) and FU-1040 (done W1133l); :64-65 label FU-1086 [owner decision], though it is open on P5.22 and not owner-gated. W1192 restates all three steps. |
| EXISTS | COST_MODEL.md:69 says the readiness round's rows are open and names none | The cell reads '...the readiness round's rows are open'. P4.1 shows 0/13 at HEAD, and after W1191 it carries FU-1834 and two more open rows. A rule keyed only on the item would therefore pass the stale sentence, so the rule requires named rows. |
| EXISTS | The money check counts only the currency first | 64872: \b(GBP\|USD\|EUR)\s*\d\|[£$€]\s*\d. The same pattern is copied in test_w923 at 78566-78568. |
| EXISTS | No business document today states money after the number or in words without a ruling | A grep of docs/business finds no amount followed by a currency word. The only figure in words, COST_MODEL.md:52's 'ninety-nine pounds', carries [owner-defined, 2026-10-13]. |
| EXISTS | Other documents cite done rows as evidence | METRICS_MEASURED.md:44 (FU-1010, built in W881), BUSINESS_PLAN.md:133 (FU-1061, Owner-ratified), FOUNDERS_GUIDE.md:83 and :91 (FU-603), COST_MODEL.md:19 (FU-603). This is why the brief's document-wide rule is not copied. |
| EXISTS | A test pins an exact fault list | test_w920 at 78355-78357 expects exactly two file faults for a planted guide that names no row and no money, so the new rules add nothing to it. |
| EXISTS | Sentences saying 'open row' without an id exist and must stay clean | LIVING_STRATEGY_MAP.md:10, :14, :19 and :97, BUSINESS_PLAN.md:93, PRODUCTION_HARDENING_BRIEF.md:70. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The business documents' guard checks only that a named row exists, so two documents name closed rows as standing between a step and being relied on (P5.10, low)
- The business documents' guard counts a money figure only when the currency comes first, so '750,000 GBP' or 'two million pounds' stands with no ruling (P5.10, low)

**Rows it closes:**

- Both rows above, closed as built.

**Changes:**

- integration_tests/test_mvp_spine.py: _w703_faults gains four rules. (a) On a bullet that begins 'Between this step and being relied on': each row named is open, a row labelled [owner decision is slotted OWNER or is owner-gated, and a plan item named is not DONE. (b) Anywhere: a row that its sentence calls open, still open or the Owner's to rule or decide must be open. (c) A sentence or table cell saying rows are, stay or remain open names at least one row, and each one named is open. (d) One module-level _W703_MONEY pattern and a _w703_money(block) helper. The pattern matches a code or symbol before a number; a number, optionally followed by million, thousand, bn, m or k, then GBP, USD, EUR, pounds, dollars, euros, pence or sterling as a whole word; and number words before pounds, dollars, euros or pence. The [owner-defined and SOURCED exemptions are unchanged. Statuses are read from root/docs/FOLLOWUPS.json, or from an optional register argument a test passes, so the 13 callers keep their arguments. test_w923's loop calls _w703_money. The new guard.

**Guard:** test_wXXXX_p510_a_business_document_calls_open_only_a_row_that_is_open_and_its_money_is_counted_however_written

- Every document under docs/business passes the extended _w703_faults against the real register. FAILS IF: A document still names a done row on a 'Between' line, calls one open, says rows are open without naming open ones, or states money after its number or in words with no ruling.
- Each fault planted in the good fixture is found: a 'Between' line naming FU-849; a 'Between' line naming FU-1086 [owner decision]; a cell '| P4.1 sign-in | the readiness round's rows are open | no |'; '- Row FU-849 is open'; a 'Between' line naming plan item P5.6; '- Pre-money 750,000 GBP [hypothesis].'; '- It is valued at 2.5 million pounds [observed].'; and '- Worth two million pounds [inference].'. FAILS IF: Any status, label, named-row or money rule is missing.
- These stay clean: '- Revenue is recorded (row FU-1010, built in W881) [observed].'; '- The price is ninety-nine pounds [owner-defined, 2026-10-13].'; '- Between this step and being relied on: no open row stands between it and being relied on [observed: `docs/FOLLOWUPS.json`].'; '- The machine has 1 GB of memory [observed].'; and '- The register of open rows is kept [observed].'. FAILS IF: A rule is over-broad: document-wide status, 'GB' read as a currency, the [owner-defined exemption lost, or 'open row' with no id read as a claim.
- With a register copy passed in which FU-1095 is marked done, the map's Observe step is a fault, and with the real register it is not. FAILS IF: The status rule ignores the register it is given.
- _w703_money is what test_w923's loop calls, and it finds '750,000 GBP' and 'two million pounds'. FAILS IF: The guide's copy keeps the old currency-first pattern.

**Blinds:**

- Drop rule (a)'s status check and keep existence only. -> Leg 2's FU-849 plant is not found.
- Apply rule (b) to every named row in every document, as the brief's rule does. -> Leg 3's FU-1010 line goes red, and leg 1 goes red on METRICS_MEASURED.md and BUSINESS_PLAN.md.
- Let rule (c) accept 'rows are open' with no id. -> Leg 2's cost-model cell plant is not found.
- Revert _W703_MONEY to currency-first. -> Leg 2's three money plants and leg 5 go red.
- Drop the [owner-defined exemption for amounts in words. -> Leg 3 goes red, and leg 1 goes red on COST_MODEL.md:52.
- Remove the [owner decision label check. -> Leg 2's FU-1086 plant is not found.

**Pins:**

- test_w703_the_business_documents_are_labelled_drafts_that_name_only_what_exists (64944-64962): good -> []; planted "a price as fact": good + "- It costs GBP 50 a month [observed].\n" -> Unchanged. Good stays clean and every plant is still found.
- test_w920_fu742_the_founders_guide_gives_only_commands_a_guard_runs_on_the_tree_it_ships_with (78355-78357): == ["it names a file that is not in the tree: start_workstation.ps1", "it names a file that is not in the tree: scripts/serve.js"] -> Unchanged. The planted text names no row and no money.
- test_w923_fu742_the_guides_price_section_is_put_to_the_owner_with_the_recommendation (78566-78568): if re.search(r"[£$€]\s*\d|\b(GBP|USD|EUR)\s*\d", _blk): -> Change on purpose: the loop calls _w703_money(_blk).
- test_w912_fu812_the_production_hardening_brief_scopes_each_part_by_its_evidence (77729-77733): closed = [rid for rid in named if rid != "FU-812" and status.get(rid) != "open"] -> Unchanged. The brief keeps its stricter rule.
- test_w903_fu744_the_living_strategy_map_names_a_real_component_test_and_row_for_each_step (77339-77341): between = [ln for ln in body.split("\n- ") if ln.startswith("Between this step and being relied on")] -> Kept. W1192's restated Record step keeps the prefix.
- test_w1126_fu1280_the_cost_model_marks_each_of_the_seven_gates_from_what_the_tree_shows (92098-92106): rows = dict(re.findall(r"^\| (.+?) \| .+? \| (yes|no) \|$", gates, re.M)) -> Kept. The restated cell keeps the three-column shape with no pipe inside it.

**Rulings it rests on:**

- P5.6 clause 5 (FABLE:6878-6880, DONE W1154): the map lists the open rows between each step and being relied on.
- P5.6 and P5.7 ACCEPT (DONE): no metric figure without a named source; every money figure carries a source and date or ASSUMED.
- P5.10 clause 1 (FABLE:7032-7034): a recurring class gets its guard at the mechanism every caller passes.
- OWNER RULING 2026-11-19 (FU-1176): a provider's published price may stand as SOURCED. The exemption is kept.
- The Owner ratified BUSINESS_PLAN.md and BUSINESS_MODEL_CANVAS.md on 2026-10-13. Neither is edited.
- OWNER RULING 2026-11-21 (P5.1): FU-417 and FU-1072 close as not reproduced after twenty green CI runs, and the map will need restating when they do.

**Risks:**

- When a row named on a 'Between' line closes (FU-417, FU-1072, FU-1036, FU-993, FU-1095, FU-1086), the guard fails until the map is restated. That is intended, as with test_w912, but whichever round closes the row must restate the map.
- Cluster B (gap 13, correction 5) and cluster D (gaps 3 and 7) edit docs/business too. They must pass this guard, and whichever lands later carries it in its -k.
- Reading statuses from the real register couples the helper to it. The optional register argument keeps the planted legs independent of the register.

### C2's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'receives ids... from 13 call sites' is wrong. There are 16 call statements (17 call expressions): 64910-64911, 64945, 64960, 77322 (two), 77323, 77708, 77754, 78355, 78358, 81421, 81486, 93927 (two), 93992 (two), 94046, 94125 and 94233. All pass the real repository root, so reading root/docs/FOLLOWUPS.json works. The other claims hold: the row check at 64848, money at 64872 with its copy at 78567, and the map at 64-65, 77-78 and 90-92. COST_MODEL.md:69 moves to :70 after W1192.

**Guard legs that could not fail:**

- Leg 2's plant '- Row FU-849 is open' carries no label. _w703_faults already reports 'a statement carries no label' for it (the label loop after 64858), so the plant is 'found' whether or not rule (b) exists. No blind drops rule (b), so the 'calls open / still open / the Owner's to rule' rule is unguarded. Any 'Between' plant written without a label is masked the same way. Leg 2 must assert each plant's own fault text, not a non-empty list as test_w703 does at 64960.

**Pins the plan missed:**

- None that break. Checked test_w703 (64944-64962), test_w903 (77322-77341; its test-name scan means a restated step may name only real tests), test_w912 (77729-77733), test_w920 (78355-78357; the planted guide names no row and no money), test_w923 (78566-78568, changed on purpose), test_w962 (81421), test_w1149-w1154 (93927-94233) and test_w1126 (92098-92106: only the column and the shape). A scan of every docs/business sentence that names a row next to 'open' or 'the Owner's to rule' finds only the map's FU-849 line. The hardening brief's 'the Owner's to buy (row FU-1289)' does not trigger it.

**Conflicts with a ruling:**

- Gap 25's rulings-lens correction: P5.10 clause 1 is about a returning finding, and none has returned. The nearest charter is clause 2, 'its guard asserts the property over the whole payload', or the row's own slot. The plan cites clause 1 for the money row.
- depends_on 'W1192, which restates the map and COST_MODEL.md:69': W1192 restates neither. Both are W1193's.

**Bar demands the plan missed:**

- Both rows carry files under integration_tests/, a retired area (W588), and are slotted P5.10 by hand. They need slot_source, or test_w469 16035-16062 fails. The record round must say so.
- Rule (c) passes a cell that names one open P4.1 row while others are open. The restated P4.1 cell must name every open P4.1 row, including the model-run row W1193 itself registers for C9, or state that it names only W1191's.

**Fixes asked for:**

- Label every plant, for example '- Row FU-849 is open [observed].', and assert each plant's own message. Add a blind 'drop rule (b)': leg 2 red.
- Add docs/FOLLOWUPS.json and both plan documents to the change list (two rows close), and add test_w469 and test_w462 to the -k.
- Slot the money row on P5.10 clause 2, or its own slot, with slot_source.
- Depend on W1193.

**Re-sized:** S, 1 round.

## W1202 - B1: Through the SSH tunnel no page from another site acts on the platform: an Origin check on writes and on the stream socket, and a Host allowlist, keyed on a setting only the release machine passes

**Closes:** FU-1835 (W1191's row)

**Owning item:** P4.1

**Held on:** W1191 landed; W1198 first (DEPLOYMENT.md)

**Rows:** none of its own; see its notes.

**Files:** agentic_core/request_guard.py (new); agentic_core/app_mvp.py; deploy/gcp/startup.sh; deploy/https_drill.sh; docs/DEPLOYMENT.md; .env.example

**-k:** -k "fu1835 or test_w1191_ or test_w1134_ or test_w1140_ or test_w505_p26_ or test_w683_ or test_self_serve_signup_owner_gated or test_auth_login or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- The guard is keyed on a dedicated setting that only startup.sh's two runs and the drill's front pass. Origins are parsed strictly as scheme://host[:port]; anything else leaves the guard off and says so. It is never keyed on CORS_ORIGINS being other than '*': with a .env made from .env.example, CORS_ORIGINS becomes its own inline comment (dotenv parser.py:24, :125-127; .env.example:40). Legs drive that value and '' (guard off), with a blind keyed on 'non-empty'.
- Served hosts come from their own setting. A leg covers a split deployment such as Render's separate frontend.
- The module and the guide state the residual: a cross-site GET still runs, and GET /api/v1/qep/adaptation/registry writes until W1220. Alternatively, refuse GETs that carry Sec-Fetch-Site: cross-site.
- The middleware goes after both the CORS line and _horizon_observe, and says whether a refused request is observed.
- Step 7's CORS sentence and startup.sh:183-184's comment are reworded, changing test_w1191's two pins on purpose. Re-read the landed test first.
- .env.example's CORS_ORIGINS comment moves to its own line.

The local-platform row stays open.

### B1 as planned (cluster B; size M, 1 round(s))

**Title:** Through the SSH tunnel no page from another site acts on the platform: an Origin check on writes and on the stream socket, and a Host allowlist (FU-1835)

**Closes:** FU-1835: W1191's third new row, 'With sign-in off, any page in the Owner's browser can act on the platform through the SSH tunnel: nothing checks a request's Origin or Host'. Read its id from the register once W1191 lands; FU-1835 is expected.

**Owning item:** P4.1

**Owner-gated:** Nothing here decides an Owner's question. Sign-in stays the machine's own switch, and the tree holds no setting of AUTH_ENABLED to true. The check reads only the CORS_ORIGINS that W1191's startup script already passes. The local platform's '*' default is not changed here, because that would change the Owner's own machine; W1192 registers it as its own row.

**Depends on:** W1191 landed: FU-1835 is in the register, startup.sh passes CORS_ORIGINS=http://localhost:8800 with no domain and https://DOMAIN behind the front, and step 7 has its CORS sentence. W1192 registers the local-platform row. B2 (step 12) and W1192's table edit also touch docs/DEPLOYMENT.md: land one, re-read, then the next.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | CORS is the only origin control: CORSMiddleware with allow_origins from settings, allow_credentials=True and every method | agentic_core/app_mvp.py:37-43. The list is '*' unless CORS_ORIGINS is set (agentic_core/config.py:38-41). |
| ABSENT | An Origin or Host check of any kind (TrustedHostMiddleware or custom) | app_mvp.py has one add_middleware (CORS, :37) and one @app.middleware('http') (_horizon_observe, :134), which observes and grants nothing. No Host or Origin test exists in app_mvp.py or config.py. |
| EXISTS | POST /api/v1/heartbeat/stop takes no body and acts at once | agentic_core/api/heartbeat.py:57-60, mounted with require_admin at app_mvp.py:535 |
| EXISTS | While sign-in is off, require_admin returns a stand-in admin, so POST /api/v1/auth/register makes an account for anyone who reaches the port | agentic_core/auth/core.py:285-287 (returns {'username': 'admin', 'role': 'admin'}); register at core.py:460-480 |
| EXISTS | The stream socket accepts any Origin and broadcasts host vitals every 5 s | app_mvp.py:875-882 (connect with no check) and :885-912 (_vitals_loop: cpu, memory, project counts, connections) |
| EXISTS | The page opens the socket on its own origin | apps/workstation-superapp/src/components/layout/Shell.tsx:88-89 (window.location.origin unless VITE_API_BASE_URL is set) |
| ABSENT | The release machine passes CORS_ORIGINS for its one origin | At 89c25eed, deploy/gcp/startup.sh:84-88 and :133-137 pass only FORWARDED_ALLOW_IPS. W1191's scratch copy (a scratch copy outside the tree) passes --env=CORS_ORIGINS=http://localhost:8800 on the no-domain run and --env=CORS_ORIGINS="https://$3" in start_front. Lands with W1191. |
| ABSENT | Step 7 says CORS stops a page from reading, not from acting | Not in the tree at 89c25eed. W1191's scratch docs/DEPLOYMENT.md step 7: 'The script lets the platform answer a browser only for pages from http://localhost:8800 itself (CORS_ORIGINS), so a page from another site cannot read what it answers; a program on the computer is not stopped by that.' |
| ABSENT | FU-1835 is in the register | The highest id at 89c25eed is FU-1832. W1191's apply (a scratch copy outside the tree) registers ORIGIN_TITLE open on P4.1, medium, files agentic_core/app_mvp.py. |
| EXISTS | The image's health check reaches the platform as Host localhost | Dockerfile:70-71 (urlopen('http://localhost:%s/health')) |
| EXISTS | No test sets CORS_ORIGINS or drives the stream socket | No CORS_ORIGINS in integration_tests/conftest.py or test_mvp_spine.py, and no websocket_connect anywhere. TestClient's default Host is 'testserver', so a check keyed to an explicit list stays off in the suite. |
| EXISTS | Starlette 0.52.1 and FastAPI 0.129.2 are what run | requirements.txt:145 and :37 |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- With CORS_ORIGINS unset, as on the Owner's own machine, a page from any site in the Owner's browser can act on the local platform while sign-in is off (P4.1, medium)

**Rows it closes:**

- FU-1835 (built)

**Changes:**

- agentic_core/request_guard.py (new): A pure ASGI middleware covering the http and websocket scopes; lifespan passes through. It acts only when CORS_ORIGINS, read at each request, is an explicit list with no '*'. Allowed hosts are localhost, 127.0.0.1 and ::1 on any port, plus the host of each listed origin. Any request with another Host gets 400 and a sentence naming the host it gave and the hosts served; nothing runs. A POST, PUT, PATCH or DELETE whose Origin is present and not listed, 'null' included, or that has no Origin but carries Sec-Fetch-Site: cross-site, gets 403 and a sentence; nothing runs. A websocket handshake with an unlisted Origin or Host is closed with code 1008 before it is accepted. A request with no Origin (a program, curl, the drills) passes, and the module says so.
- agentic_core/app_mvp.py: app.add_middleware(OriginHostGuard) once, after the CORS middleware so that it is the outermost layer, with a comment naming FU-1835.
- docs/DEPLOYMENT.md: Step 7: one sentence after W1191's CORS sentence. Since this round the platform also refuses a write or a stream socket from a page of any other origin, and any request whose host name is not localhost, 127.0.0.1 or the machine's domain, so a page in the browser cannot act through the tunnel either. A program on the computer still can, which is why sign-in is turned on right after the password. Nothing else in step 7 changes.
- docs/FOLLOWUPS.json (scripts/followups.py close): FU-1835 closed as built. The close note names the module, what it refuses, and what it does not refuse: programs and preflights.
- integration_tests/test_mvp_spine.py: test_wNNNN_fu1835_through_the_tunnel_no_page_from_another_origin_or_host_acts_on_the_platform appended.

**Guard:** test_wNNNN_fu1835_through_the_tunnel_no_page_from_another_origin_or_host_acts_on_the_platform

- Off by default: with CORS_ORIGINS unset, a POST with Origin http://evil.example and Host testserver reaches the patched heartbeat stop once, and GET /health answers 200 FAILS IF: the check acts without an explicit origin list, which would also refuse every TestClient request in the suite
- The tunnel's own page acts: with CORS_ORIGINS=http://localhost:8800 (monkeypatched) and a TestClient on base http://localhost:8800, GET /health answers 200, and POST /api/v1/heartbeat/stop with Origin http://localhost:8800 calls the patched stop once FAILS IF: the listed origin or the tunnel's host is refused, for example by an allowlist that compares ports
- Another site cannot act: the same POST with Origin http://evil.example, with Origin null, and with no Origin but Sec-Fetch-Site: cross-site each answers 403 with the sentence, and the patched stop is never called FAILS IF: any of the three reaches the handler
- The registration exploit: POST /api/v1/auth/register with Origin http://evil.example and a JSON body sent with no Content-Type answers 403, and users.json's bytes are unchanged FAILS IF: the check lets a simple request through, or runs after the handler
- A program is not a page: the POST with no Origin and no Sec-Fetch-Site reaches the handler FAILS IF: programs are refused. The guide says they are not, and set_password, the drills and curl send no Origin.
- DNS rebinding: GET /api/v1/auth/users with Host evil.example:8800 answers 400 and its body names no account FAILS IF: the host check is skipped for reads
- The stream socket: a websocket to /api/v154/ws/streams with Origin http://evil.example is refused (WebSocketDisconnect, code 1008); with Origin http://localhost:8800 it is accepted; with Host evil.example it is refused FAILS IF: the websocket scope passes through unchecked
- Behind the front: with CORS_ORIGINS=https://app.example.com, GET /health answers 200 for Host app.example.com and for Host localhost:8000 (the image's health check), and a POST with Origin http://localhost:8800 is refused FAILS IF: the domain or the health check's host is refused, or the tunnel's origin is accepted on a run that names only the domain
- The guide and the row: step 7 says a page of another origin cannot act through the tunnel and a program still can; W1191's two pinned sentences still stand; FU-1835 is closed by this round as built FAILS IF: the guide still says only that a page cannot read the answers, or the row stays open

**Blinds:**

- Check the Origin only when Content-Type is application/json -> Leg 4's simple request registers an account (users.json changes), and leg 3's POST with no Content-Type runs the stop.
- Let the websocket scope pass straight through -> Leg 7: the evil-origin socket is accepted.
- Build the allowed hosts from CORS_ORIGINS alone, without localhost and 127.0.0.1 -> Leg 8: the image's health check (Host localhost:8000) is refused behind the front.
- Treat Origin: null as no Origin -> Leg 3: the null-origin POST runs the stop.
- Apply the Host check to unsafe methods only -> Leg 6: the rebound GET of /api/v1/auth/users answers with the account list.
- Act when CORS_ORIGINS is '*' as well -> Leg 1: the request with Host testserver is refused.

**Pins:**

- test_w1191_the_release_machine_serves_publicly_only_with_its_domain_https_and_sign_in_on (lands with W1191) (the S4 step 7 list, about test_mvp_spine.py:99045-99052 in W1191's scratch copy): '(CORS_ORIGINS)' and 'While the tunnel is open and sign-in is off, anything on the Owner's computer that opens the forwarded port acts as the platform's administrator' -> Keep both verbatim. The new sentence goes after the CORS sentence; the second sentence stays true of programs. Re-read the landed test first.
- test_w1134_fu603_the_google_cloud_deploy_is_written_from_googles_pages_and_no_disk_with_records_is_formatted (test_mvp_spine.py:92786-92805): every [lowercase] token in a step is a listed page; steps numbered 1 to 12 -> The new sentence carries no bracketed token. No change to the test.
- test_w505_p26_the_governing_routers_have_an_admin_perimeter (test_mvp_spine.py:25336-25363): require_admin mounted on /api/v1/heartbeat/stop and the board -> None: no mount changes.

**Rulings it rests on:**

- OWNER RULING 2026-11-20 (evening): sign-in is switched on only on the Owner's private deployed machine, and no round switches it on in the tree (P4.1, FABLE:6737-6739)
- OWNER RULING 2026-11-21 (afternoon): with no domain the machine publishes no port and the Owner reaches it through an SSH tunnel; sign-in is the machine's own setting (P4.1, FABLE:6740-6747)
- P2.6 (W505): require_admin gives a stand-in admin while sign-in is off; this round changes no perimeter
- FU-1835's why (W1191's second review) names this fix

**Risks:**

- A preflight (OPTIONS) is a safe method and is not refused. CORS still answers it, so the browser stops a page's non-simple request and this check stops its simple one; the module says so.
- CORSMiddleware reads CORS_ORIGINS at import, and the guard reads it at each request. They can disagree only in a process whose environment changed after import, which no deploy does. The test sets the variable only around its own requests.
- https_drill.sh's front now runs the check, because start_front passes CORS_ORIGINS=https://workstation.localhost. Its curl probes send that host and no Origin, so they pass, but the drill is not re-run here and the commit must say so. deploy/drill.sh passes no CORS_ORIGINS, so the check is off there.
- A Host of '[::1]:8000' must be parsed with its brackets.
- W1191's landed test may pin step 7 differently from the scratch copy.

### B1's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'Step 7 says CORS stops a page from reading, not from acting' (ABSENT at HEAD, correct) is evidenced with a superseded scratch sentence. W1191's current step 7 (a scratch copy outside the tree) reads: '(CORS_ORIGINS) stops a page from another site reading the platform's ordinary answers, not sending it requests: while sign-in is off the platform acts on those requests as for the administrator, making an account included, and its stream socket and a host name rebound to the machine are outside that setting.' W1191's staged guard (a session work file, not in the tree)'s list of phrases that must be gone includes 'so a page from another site cannot read'.
- 'The release machine passes CORS_ORIGINS' evidence: at HEAD the no-domain run (startup.sh:133) passes no --env at all. Only the front (:85) passes FORWARDED_ALLOW_IPS.
- The conclusion drawn from 'No test sets CORS_ORIGINS' ('a check keyed to an explicit list stays off in the suite') fails on any machine with a repo-root .env:
  - app_mvp.py:22 calls load_dotenv(), and README.md:65 says to make .env with cp .env.example .env.
  - python-dotenv's parser reads .env.example:40 (`CORS_ORIGINS=   # your frontend URL(s)...`) as the comment text. _equal_sign consumes '=' and the spaces (parser.py:24), and then the inline-comment strip, which needs whitespace before the '#', no longer matches (:125-127).
  - CORS_ORIGINS is then an explicit list with no '*'.

**Guard legs that could not fail:**

- Leg 9 ('W1191's two pinned sentences still stand') holds a sentence B1 makes false, so it cannot be the leg. It must assert the reworded step-7 sentence and the absence of 'while sign-in is off the platform acts on those requests as for the administrator, making an account included, and its stream socket and a host name rebound to the machine are outside that setting'.

**Pins the plan missed:**

- test_w1191, S4 step-7 list (a scratch copy outside the tree) pins the whole CORS sentence quoted above. B1 makes it false, so the pin must be changed on purpose. The plan says to keep both sentences verbatim.
- test_w1191, S1 (W1191's staged guard (a session work file, not in the tree):223-224) pins the startup.sh comment 'CORS_ORIGINS stops a page from another site reading its ordinary answers, not sending it requests' (scratch startup.sh:183-185). B1 changes no script, so after B1 the comment says less than CORS_ORIGINS now does. It needs a deliberate rewording and pin change.
- test_w1191's list of phrases that must be gone (W1191's staged guard (a session work file, not in the tree):488-490) constrains the new step-7 sentence: 'so a page from another site cannot read', 'the tree never turns it on', 'it is the Owner's to choose'.

**Conflicts with a ruling:**

- B1's own boundary is 'the local platform's '*' default is not changed here, because that would change the Owner's own machine'. Its activation rule breaks it. With a .env made by README step 2, the guard acts on the Owner's machine:
  - every TestClient request (Host testserver) answers 400, so the full-suite run of RESUME_ON_MY_MACHINE.md step 4 goes red;
  - the Vite dev UI's writes and its socket are refused, because vite.config.js:22-27 proxies with changeOrigin and ws, which keeps Origin http://localhost:5173.
- 'W1192 registers the local-platform row' is wrong: W1192 is the Owner-decisions round (FU-1838 to FU-1840). The row belongs to W1193.

**Bar demands the plan missed:**

- Activation must not depend on CORS_ORIGINS merely being something other than '*'. Either use a dedicated setting passed only by deploy/gcp/startup.sh and the drill's front, or parse strictly so that an entry that is not scheme://host[:port] leaves the guard off and says so. Add a leg that drives the .env.example value and '' (guard off), with a blind keyed on 'non-empty'.
- The Host allowlist is built from the allowed Origins, which conflates two things. On the documented Render backend (render.yaml:22-23; DEPLOYMENT.md:20-34), CORS_ORIGINS names a separate frontend, so the backend's own Host would be refused on every request. Take the served hosts from a setting of their own (the startup script knows the domain), or drive the split case and state it in the guide.
- Cross-site GETs still run, and at least one writes: GET /api/v1/qep/adaptation/registry saves its store (qep_intelligence.py:449-457). Say so in the module and the guide, or refuse GETs that carry Sec-Fetch-Site: cross-site.
- Placement: adding the guard right after the CORS line (app_mvp.py:37-43) makes it outermost only if it is also after @app.middleware('http') _horizon_observe (:134). Name the line, and say whether a refused request is observed by the membrane.

**Fixes asked for:**

- Re-read W1191's landed test. Reword step 7's CORS sentence and startup.sh's comment, changing both test_w1191 pins on purpose.
- Key activation on a dedicated variable, or on strict origin parsing, as above. Add the .env and empty-value legs and their blind. Consider os.environ.setdefault('CORS_ORIGINS','*') in conftest.
- Take the Host allowlist from its own setting. Add a leg for a split deployment.
- State the GET residual, or check Sec-Fetch-Site on every method.
- Register the local-platform row in W1193. Its why must not say CORS_ORIGINS is unset on the Owner's machine: a .env from .env.example sets it.

**Re-sized:** M, 1.5 rounds (an activation and host-source design, plus two W1191 pins changed on purpose)

## W1203 - A11: A model becomes the serving default only when an administrator promotes an evaluated build whose licence text the runtime holds

**Closes:** v40 gap 3 and its two rows (licence, P3.32; perimeter, P4.1)

**Owning item:** P3.32 and P4.1

**Held on:** W1193

**Rows:**

- FU-1852 (P3.32, low): A model is made the serving default with no licence read: W841 built FU-1087's evaluation and digest checks but not the licence refusal it proposed
- FU-1853 (P4.1, medium): With sign-in on, any signed-in person can promote, retire, reinstate or evaluate a local model, or run or reproduce a baseline: the lifecycle's writes sit behind get_current_user, not the administrator perimeter

**Files:** agentic_core/ai/native/model_resource.py; agentic_core/api/native_ai.py; apps/workstation-superapp/src/pages/developers/NativeAI.fixture.json

**-k:** -k "administrator_promotes_an_evaluated_build or test_w841_ or test_owned_model_lifecycle or test_w458_ or test_w641_ or test_p3d_r8_ or test_w577_p218a_ or test_w505_p26_ or test_tenancy_matrix_user_data_routes or test_w1048_ or test_w1192_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- Leg 4 also drives POST /baseline/{run_id}/reproduce (native_ai.py:960), with a blind that drops its dependency.
- The refusal and the row cite the Owner's ruling of 2026-11-22: no override. OLLAMA_MODEL remains the Owner's own way to serve such a build.
- A7 edits native_ai.py's durations later; anchor both by text.

### A11 as planned (cluster A; size S, 1 round(s))

**Title:** A model becomes the serving default only when an administrator promotes an evaluated build whose licence text the runtime holds

**Closes:** v40 new gap 3 (FU-1087's licence half, narrowed by its refuter) and the P4.1 gap its refuter found: the model lifecycle's writes are open to any signed-in person. These are bundled: one guard holds both, and native_ai.py and model_resource.py are touched by no other round in this cluster.

**Owning item:** P3.32 for the licence (FU-1087 rode it) and P4.1 for the perimeter (its readiness instrument reads each route's mounted dependency)

**Owner-gated:** No override is built. Whether an administrator may force a build with no licence text is put to the Owner as a question; no row is recommended.

**Depends on:** W1192. It is independent of A1-A10. It lands after W1191's P4.1 rows.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| ABSENT | promote_model reads a licence | native_ai.py:1273-1310 refuses an undiscovered name, a missing digest and a missing evaluation, then sets default_local and default_local_digest |
| EXISTS | The runtime's licence is read per build | model_resource.py:373-446: describe_installed posts /api/show per model, 20 s each; licence at :428-436 (first line, length, sha256) |
| ABSENT | The research-only lead can be matched to an installed build | model_resource.py:477-478 has runtime_tag None, and :517-521 cannot match a lead with no tag |
| EXISTS | FU-1087 proposed the licence refusal and its close note omits it | FU-1087 why ('refuses ... when no licence text is held'); close_note names only the evaluation and the digest |
| EXISTS | test_w841 promotes successfully with no licence stub | test_mvp_spine.py:73139-73140 |
| EXISTS | The native-ai router is mounted behind get_current_user only, and promote takes no user | app_mvp.py:565; native_ai.py:1271-1273 |
| EXISTS | The administrator perimeter exists and is inert with sign-in off | app_mvp.py:377-380 (require_admin returns a synthetic admin); test_w505_p26 :25336-25365 |
| EXISTS | The lifecycle writes | native_ai.py:616 (/lifecycle/evaluate), :874 (/baseline/run), :960 (/baseline/{run_id}/reproduce), :1271 (/lifecycle/promote), :1314 (/lifecycle/retire), :1333 (/lifecycle/reinstate) |
| EXISTS | The page prints licence lines | NativeAI.tsx:1122 (each installed build) and :1134-1135 (the research-only lead) |
| EXISTS | The levels-table text for promote, captured in the page fixture | native_ai.py:1042-1043; NativeAI.fixture.json:392-394 |
| ABSENT | A candidate is downloaded | Owner ruling 2026-11-06 (FABLE:294-295) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- A model is made the serving default with no licence read: W841 built FU-1087's evaluation and digest checks but not the licence refusal it proposed (P3.32, low)
- With sign-in on, any signed-in person can promote, retire, reinstate or evaluate a local model: the model lifecycle's writes sit behind get_current_user, not the administrator perimeter (P4.1, medium)

**Rows it closes:**

- The A11 licence row (P3.32): closed as built
- The A11 perimeter row (P4.1): closed as built

**Changes:**

- agentic_core/ai/native/model_resource.py: Add describe_installed_one(name). It makes one /api/show call and returns the same row shape as describe_installed (licence, show_read, show_basis) without describing every model.
- agentic_core/api/native_ai.py: promote_model reads this build's description. It refuses with 409 when the runtime reports no licence text, and separately with 409 when the description could not be read (show_read False is not 'no licence'). On success it stores default_local_licence {first_line, chars, sha256} beside default_local_digest and returns it. The levels table at :1042-1043 says the promotion also rests on the runtime's licence text. Routes :616, :874, :960, :1271, :1314 and :1333 gain dependencies=[Depends(require_admin)]; the reads stay behind get_current_user. No override and no research-lead match are built.
- apps/workstation-superapp/src/pages/developers/NativeAI.fixture.json: Recapture the route-level row at :392-394.
- integration_tests/test_mvp_spine.py: Append the new guard. test_w841's stub gains a licence so its success leg holds on purpose.

**Guard:** test_wNNNN_a_model_becomes_the_default_only_when_an_administrator_promotes_an_evaluated_build_whose_licence_the_runtime_holds

- With test_w841's stubs (local_models, local_model_digest, an evaluation on the pinned set) and describe_installed_one returning show_read True with licence None: promote answers 409 naming the missing licence text, and default_local is unchanged FAILS IF: Red at HEAD (200).
- describe_installed_one returns show_read False: 409 naming the unread description FAILS IF: Red at HEAD.
- Licence text 'Apache License 2.0 ...': promote answers 200 with licence.first_line and licence.sha256 equal to sha256 of the stub's text, and the lifecycle record holds default_local_licence FAILS IF: Red at HEAD (no licence returned or stored).
- With AUTH_ENABLED=true set in the test process only, plus a user and an admin made as test_w885 does: as the user, POST /lifecycle/promote, /retire, /reinstate, /evaluate and /baseline/run each answer 403; as the admin, promote reaches the route (409 undiscovered); GET /lifecycle answers 200 for the user FAILS IF: Red at HEAD (the user reaches every route).

**Blinds:**

- Remove the licence read -> Leg 1: the build is promoted.
- Treat show_read False as licensed -> Leg 2.
- Store the candidate lead's research string instead of the runtime's text -> Leg 3: the hash differs.
- Drop require_admin from /lifecycle/retire -> Leg 4: the user is not refused.
- Replace require_admin with get_current_user on promote -> Leg 4.

**Pins:**

- test_w841_a_model_is_made_the_serving_default_on_an_evaluation_of_that_build_not_on_being_installed (test_mvp_spine.py:73139-73140): ok.status_code == 200 and ok.json()["digest"] == "sha256:w841aaaa" -> Change on purpose: stub describe_installed_one with licence text so the evaluated build is still promoted.
- test_owned_model_lifecycle (test_mvp_spine.py:2069-2074): promote undiscovered → 409; retire/reinstate persist -> Keep. With sign-in off, require_admin is a synthetic admin.
- test_w505_p26_the_governing_routers_have_an_admin_perimeter (test_mvp_spine.py:25336-25365): admin_paths and auth_paths sets -> Keep. The new test holds the lifecycle routes.
- test_w1048_fu399_the_native_ai_page_says_each_failure_beside_the_action_that_met_it (test_mvp_spine.py:86501): NativeAI.fixture.json answers -> Keep. The fixture is recaptured at :392-394.

**Rulings it rests on:**

- FU-1087 (W841, P3.32) proposed the licence refusal.
- Owner ruling 2026-11-06 (FU-1130): no candidate is downloaded, so exposure today is nil.
- P4.1: each readiness finding is a register row, driven with sign-in on in a test process only. Owner rulings of 2026-11-20 and 2026-11-21: no round switches sign-in on in the tree.
- W505 (P2.6): routers that govern the platform go behind require_admin.

**Risks:**

- With sign-in off nothing changes. The guard's role leg runs only under monkeypatched AUTH_ENABLED in the test process.
- The OLLAMA_MODEL fallback is the Owner's own way to serve a build that has no licence text. The round says so in the refusal.

### A11's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'native_ai.py and model_resource.py are touched by no other round in this cluster' is false once A7 carries native_ai.py:622-638 and :819-843.

**Guard legs that could not fail:**

- Leg 4 drives promote, retire, reinstate, evaluate and baseline/run. It does not drive POST /baseline/{run_id}/reproduce (native_ai.py:960), which the change also puts behind require_admin, so dropping that one dependency stays green.

**Conflicts with a ruling:**

- NG3 is decided (Owner 2026-11-22: 'no override: refuse promotion with no licence read'). The plan still frames the override as 'put to the Owner as a question'. Cite the ruling in the refusal and in the row.

**Fixes asked for:**

- Add /baseline/{run_id}/reproduce to leg 4 and a blind that drops its dependency.
- Sequence A11 against A7 (both edit native_ai.py) and anchor the edits by text.
- Cite NG3.

**Re-sized:** S (unchanged). Checked: native_ai.py:1271-1310 and :1036-1048; model_resource.py:373-446 and :477-478; FU-1087's why and close note; NativeAI.fixture.json:392-394; app_mvp.py:565; that test_w505 checks named paths only; that no sign-in-on test calls the lifecycle write routes.

## W1204 - D-TERMS, D-CREDIT: What the Owner ruled on 2026-11-22 is said where it is read: an entity repository says no terms have been chosen, and the generation credit carries forward

**Closes:** Two rows: the entity repository's terms (the interim the Owner accepted with Q6) and the credit's basis (Q11)

**Owning item:** P3.30 (P5.4 and P5.16 are done)

**Held on:** W1193

**Rows:**

- FU-1880 (P3.30, low): A handed-over entity repository says nothing about its terms, where the Owner accepted on 2026-11-22 that its README says no terms have been chosen
- FU-1881 (P3.30, low): The generation credit is said to come off the first share or the first fee only, where the Owner ruled on 2026-11-22 that it carries forward against later fees until it is used up

**Files:** agentic_core/api/vsb.py (D-TERMS); agentic_core/economy/metabolism.py; agentic_core/economy/generation_price.py; apps/workstation-superapp/src/components/GenerationPrice.fixture.json (D-CREDIT)

**-k:** -k "no_terms_have_been_chosen or credit_carries_forward or test_w936_ or test_w937_ or test_w938_ or test_vsb_repo_generation or test_genesis_blueprint_reaches_the_entity_surfaces or test_w1124_ or test_w1125_ or test_w1139_ or test_w1155_ or test_price_of_generating_an_entity_is_stated_once or test_w1117_ or test_w462_ or test_w469_" plus vitest GenerationPrice.test.tsx

**Notes from the lead:**

Sketched by the bundler from W1192's notes and the Owner's accepted options. The two halves are disjoint.

D-TERMS:
- The README writer (vsb.py:170) adds that no licence terms have been chosen for the repository, and that until they are, nothing in it grants a licence.
- No LICENSE file is added and no licence is named.
- Guard: a generated repository's README carries the sentence. Blind: drop it.

D-CREDIT:
- metabolism.py:133 and generation_price.py:58-59 say that the credit is taken off the platform's fees as they fall due, from the first, until it is used up.
- The boolean field credited_against_first_profit_share keeps its name, because it is pinned at :63186, :91609 and GenerationPrice.test.tsx:46.
- The fixture is recaptured from the route.

*D-TERMS has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

*D-CREDIT has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## W1205 - A5: The document-control registry appends one record per version, reads its store whole or refuses, and says when a version was not kept

**Closes:** Gap 8 for the DCMS, and its row

**Owning item:** P3.30

**Held on:** W1197 (quality.py), W1204 (vsb.py)

**Rows:**

- FU-1845 (P3.30, medium): The document-control registry is rewritten whole on every gated answer, grows without bound in memory and on disk, takes an unreadable store as its next write base, and a version that failed to write still reads as document-controlled

**Files:** agentic_core/vbs/dcms.py; agentic_core/vbs/qms.py; agentic_core/vbs/quality.py; agentic_core/api/vsb.py; agentic_core/api/vbs_systems.py; scripts/soak_organism.py

**-k:** -k "document_control_registry_appends or test_tamper_evidence_is_genuinely_evident or test_vbs_living_systems_integrated_in_house or test_w440_ or test_resource_compose or test_resource_composition_run_on_native_swarm or test_reactor_experimentation_whatif or test_reactor_studio_visual_analytics or test_vsb_repo_generation or test_w449_ or test_w577_p218a_ or test_w838_ or test_w452_ or test_w1088_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- Name vsb.py:3084 and :3134 and vbs_systems.py:318, the direct callers with no try. Each answers 503 with its reason, or saves the decision and says the seal failed, and has a leg of its own.
- Blinds for legs 2 and 8: replay drops the last line; integrity is tallied at append rather than recomputed.
- Leg 6 commits once more after migrating, then asserts that dcms_registry.json is byte-identical and that the ledger holds the migration line.
- A torn last line's refusal says how the Owner repairs the ledger (P1.15).

Step 0's measurement is recorded in the round record.

### A5 as planned (cluster A; size M, 1 round(s))

**Title:** The document-control registry appends one record per version, reads its store whole or refuses, and says when a version was not kept

**Closes:** Gap 8 (v43 G1) for the DCMS

**Owning item:** P3.30, as FU-1297, the same whole-file ledger class in the genome registry. P4.5's memory claim is served by the round's resident-size measurement, not by a P4.5 row.

**Owner-gated:** No. The Owner's existing dcms_registry.json is carried over once and kept beside the new ledger, never deleted.

**Depends on:** W1192, then A1 (both edit vbs/quality.py around control_document). It must come before A6, whose widened guard would flag the DCMS at HEAD.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | Each commit appends up to 16,000 serialised characters to one in-memory registry | dcms.py:18 and :52-67; the registry singletons are at vbs/registry.py:24-28 |
| EXISTS | _persist rewrites the whole file under a bare except | dcms.py:45-50 (atomic_write_json, config.py:108) |
| EXISTS | An unreadable store loads as {} or its prefix, with the reason in _store_incomplete | dcms.py:28-43; read_json_reported answers OSError with the default (config.py:245-280) |
| ABSENT | _store_incomplete is read anywhere | A grep over agentic_core finds only dcms.py:29 and :42 |
| EXISTS | A failed write still reads as document-controlled | qms.py:372-377 returns the hash whatever happened; quality.py:558 sets document_controlled True; lib/api.ts:360 prints 'doc-controlled' |
| EXISTS | Callers outside assure_delivery | orchestrator.py:868-876 (tree:<goal[:48]>, which reads len(dcms.registry[...])); swarm.py:1237 (four '{run_id}:{aid}' keys per cascade run); vbs_systems.py:315-321 (reads dcms.registry and calls get_audit_integrity on every commit) |
| EXISTS | get_audit_integrity re-hashes every version on each call | dcms.py:88-98, called by qms.document_control_status (qms.py:385) and the commit route |
| ABSENT | verify_artifact has a production caller | Only the suite calls it (test_mvp_spine.py:5829, :5832) |
| EXISTS | One process, with no await between the append and the write | Dockerfile:73 (no --workers); dcms.py:65-66 |
| EXISTS | The growth figure was measured on August's code with three auto flags on | AUTONOMOUS_PROGRESS.md:2274-2277; scripts/soak_organism.py:59; dcms_bytes reads dcms_registry.json at :85-86 |
| EXISTS | The dry run measured memory only at boot and after five probes | DEPLOYMENT.md:107 (225 and 253 MiB) |
| EXISTS | The tamper test tampers the in-memory registry | test_mvp_spine.py:5826-5833 |
| ABSENT | W577's guard catches a read in _load and a write in _persist | test_mvp_spine.py:39618-39680 checks one function at a time |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The document-control registry is rewritten whole on every gated answer, grows without bound in memory and on disk, takes an unreadable store as its next write base, and a version that failed to write still reads as document-controlled (P3.30, medium)

**Rows it closes:**

- The A5 row registered by W1192: closed as built

**Changes:**

- agentic_core/vbs/dcms.py: Step 0 first: on a scratch copy with default settings, 200 gated answers and 20 beats, measuring bytes per gated answer and per beat, and the resident size of the registry (tracemalloc), recorded in the round record. Then the store becomes data_path('dcms_ledger.jsonl'), one JSON line per version: artifact_id, version, hash, actor, timestamp, content (capped at 16,000 or null), content_stored. Each commit appends under store_lock with flush and fsync; an OSError propagates. dcms.registry stays a dict of artifact id to a list of version stubs (version, hash, actor, timestamp, content_stored, offset) with no content, so len() still works for orchestrator.py:876, vbs_systems.py:319 and qms.py:384. The load is strict: transient PermissionError is retried as read_json_strict does; a torn last line or an unparseable line sets _store_incomplete and commit_artifact refuses with StoreUnavailable. Migration runs once: dcms_registry.json is read strictly, carried in behind a first migration line naming its sha256 and entry count, and the old file is kept untouched. verify_artifact and get_audit_integrity stream the file and recompute from it, with memory bounded.
- agentic_core/vbs/qms.py: document_control_status adds store_incomplete, read from dcms._store_incomplete. control_document is unchanged; it increments only after a successful commit.
- agentic_core/vbs/quality.py: control_document gets its own try inside assure_delivery. On failure, quality_record_hash is None, document_controlled is False, and document_control_basis gives the reason. The outer except stays for other faults.
- scripts/soak_organism.py: dcms_bytes (:85-86) reads dcms_ledger.jsonl.
- integration_tests/test_mvp_spine.py: Append the new guard. test_tamper_evidence_is_genuinely_evident (:5826-5833) is changed on purpose to tamper one line of the ledger in an isolated data root.

**Guard:** test_wNNNN_the_document_control_registry_appends_each_version_and_refuses_a_store_it_cannot_read_whole

- On an isolated data root, 300 commits of mixed sizes: each commit grows the store by exactly its own record line, and the first kilobyte of the file never changes FAILS IF: Red at HEAD: every write re-serialises the whole registry.
- A fresh instance replays the same version counts for every id, and verify_artifact is valid for each FAILS IF: Red if replay loses or reorders versions.
- With the last line torn: the new instance's document_control_status says store_incomplete, commit_artifact raises StoreUnavailable, and the file's bytes are unchanged FAILS IF: Red at HEAD: a {} or prefix base is written back over the history.
- The reader raises PermissionError twice and then reads: the store loads whole. If it raises persistently, the load refuses and nothing is written FAILS IF: Red at HEAD: an OSError is answered with {}.
- With the append forced to raise OSError: assure_delivery answers document_controlled False with the reason, and controlled_documents does not move FAILS IF: Red at HEAD: True after a failed write.
- A planted dcms_registry.json with 3 artifacts × 2 versions migrates: 6 versions verify, and the old file is byte-identical afterwards FAILS IF: Red if the old store is lost or rewritten.
- After 300 commits of about 10 KB each, the in-memory stubs hold no content strings FAILS IF: Red at HEAD: content is resident.
- One line's content tampered in the file: verify_artifact is invalid, and get_audit_integrity is below 1.0 FAILS IF: Red if integrity is cached rather than recomputed.

**Blinds:**

- Restore whole-file rewriting (atomic_write_json of the registry per commit) -> Leg 1.
- Restore the bare except in the write path -> Leg 5.
- Read a torn ledger as its readable prefix and keep appending -> Leg 3.
- Keep content in the in-memory stubs -> Leg 7.
- Replace dcms_registry.json during migration -> Leg 6.

**Pins:**

- test_tamper_evidence_is_genuinely_evident (test_mvp_spine.py:5826-5833): dcms.registry["w327t-doc"][0]["content"] = '{"body": "TAMPERED"}' ... "w327t-doc" in type(dcms)("x").registry -> Change on purpose: tamper the ledger file in an isolated data root. Keep the verify, integrity and persistence assertions.
- test_vbs_living_systems_integrated_in_house (test_mvp_spine.py:4419-4430): b["version"] == a["version"] + 1 ... dc["audit_integrity"] == 1.0 -> Keep: stub lists keep len(), and the integrity stays 1.0 on an untampered store.
- test_w440_vbs_cluster_disclosures_hold (test_mvp_spine.py:9127-9129): "per-process counter" in dc["note"] -> Keep.
- test_resource_compose / test_resource_composition_run_on_native_swarm / test_reactor_experimentation_whatif / test_reactor_studio_visual_analytics / test_vsb_repo_generation / test_w449_floor_served_gate_is_not_assessable_both_ways (test_mvp_spine.py:2904, :2960, :3004, :3024, :3164, :3187, :3214, :3245, :4011, :9495): document_controlled is True -> Keep: a successful append still reads True.

**Rulings it rests on:**

- P1.15 (W472): stores refuse, never replace.
- W577 (FU-395, FU-298): a tolerant read is never a write base. FU-298 converted only this reader.
- Owner ruling 2026-10-09: tier-3 findings ride P3.30, one row per region. FU-1297 is the same mechanism.
- P4.5 (Owner rulings 2026-10-12 and 2026-11-20): the first deploy goes ahead only after its memory fits. The deploy is the Owner's, whenever it suits.
- Never delete an entity: the old registry file is kept.

**Risks:**

- The Owner's machine holds a live dcms_registry.json. If migration fails, the old file must stay the store and the refusal must be said; the migration leg is the check.
- Stub memory still grows by about one small record per version (Step 0 measures it). Rotating to a closed archive file is not proposed until a measured need.
- get_audit_integrity becomes a linear file read per status call. Step 0 times it at the measured size.

### A5's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'Callers outside assure_delivery' is listed as orchestrator.py:868, swarm.py:1237 and vbs_systems.py:318 only. vsb.py also calls qms.control_document directly: :2357 (board pack, inside a try), :3084 (setting review gates) and :3134 (a review decision), the last two with no try.

**Guard legs that could not fail:**

- Legs 2 (a fresh instance replays the counts and verify is valid) and 8 (a tampered line makes integrity below 1.0) pass on the unchanged tree, and none of the five blinds turns them red.
- Leg 6 (a planted dcms_registry.json migrates, 6 versions verify, the old file is byte-identical) also passes at HEAD, because loading and verifying change nothing there. Only blind 5 reaches it, and it does not show that a migration happened.

**Bar demands the plan missed:**

- With commit_artifact now raising (OSError propagates; StoreUnavailable on an incomplete ledger), vsb.py:3084 and :3134 and vbs_systems.py:318 would answer 500 through route_failure. At :3084/:3134 the review-gate change or decision is not saved, because _save_vsb runs after control_document. Each must refuse with 503 and its reason, or save the decision and say the seal failed.
- A torn final line after a crash refuses every later commit for good. The refusal must say how the Owner repairs the ledger (P1.15: refuse and say so; the store is never replaced).

**Fixes asked for:**

- Name vsb.py:3084, :3134 and vbs_systems.py:318 in the change list, with their refusal shape and a leg each.
- Add blinds for legs 2 and 8: replay drops the last line; integrity is tallied at append and not recomputed.
- Strengthen leg 6: after migrating, commit one more version and assert dcms_registry.json is still byte-identical (HEAD rewrites it on every commit) and that the ledger holds the migration line.

**Re-sized:** M (unchanged).

## W1206 - A6: A store read tolerantly into an object is never written back from it: the QMS refuses its write, and the guard watches the attribute door

**Closes:** Its row (high, P5.10), FU-395's class returning through an attribute

**Owning item:** P5.10 clause 1

**Held on:** W1205 (the DCMS must already read strictly)

**Rows:**

- FU-1846 (P5.10, high): FU-395's class returns through an attribute: the QMS reads its store tolerantly into self._state and writes it whole from another method, which W577's per-function guard cannot see

**Files:** agentic_core/vbs/qms.py

**-k:** -k "read_tolerantly_into_an_object or test_w534_ or test_w1091_ or test_w577_p218a_ or test_w853_ or test_vbs_living_systems_integrated_in_house or test_w440_refuter_pass_findings_stay_fixed or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- The matcher accepts a writer guarded by a raise on the reason the tolerant read bound, with a planted negative case. Without that, leg 2 is red on the fixed tree.
- The row cites FU-1834. auth/core.py:117-123's except-default loader is a third door that this matcher leaves to P4.1, which has no round (see completeness).
- The row says why FU-395 is not reopened: scripts/followups.py has no reopen, and FU-395's ten paths still hold.
- The summary says the refusal lasts until restart.

### A6 as planned (cluster A; size S, 1 round(s))

**Title:** A store read tolerantly into an object is never written back from it: the QMS refuses its write, and the guard watches the attribute door

**Closes:** The class gap 8 exposed: FU-395's tolerant-read-as-write-base returning through an object attribute, with the QMS as the remaining instance once A5 lands

**Owning item:** P5.10 clause 1: a return of a closed class gets a guard at the mechanism every caller passes. There is a new row citing FU-395, since the house precedent (FU-321) registers a new row rather than reopening one.

**Owner-gated:** No.

**Depends on:** A5. The DCMS must already read strictly, or the widened guard is red on it.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The QMS fills self._state from a tolerant read | qms.py:87-95 read_json_reported(data_path(self._store_name), {'gates_run': 0, 'defects_total': 0, 'defects': []}) |
| EXISTS | _save_state writes self._state whole whatever _store_unreadable says | qms.py:97-100; called at :164, :219, :233, :275, :297 |
| EXISTS | An unreadable QMS store reads as its prefix or the defaults | config.py:259-280; W534 discloses it on reads only (qms.py:322-323, :366-370) |
| PARTIAL | The shape census: a tolerant read in one method and a write in another | An AST scan at 89c25eed finds three. DocumentControlManagementSystem (dcms.py _load/_persist) is a true positive, fixed by A5. QualityManagementSystem (qms.py _load_state/_save_state) is a true positive. OrganismHeartbeat (heartbeat.py _compliance_beat reads vsb_compliance_history.json, while _save_autonomy writes the autonomy store) is a false positive: different stores. |
| EXISTS | W577's guard sees only a read and a write in the same function | test_mvp_spine.py:39643-39645 |
| ABSENT | FU-395 listed the QMS | FU-395 (done W577, high) named nine write paths and not this one |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- FU-395's class returns through an attribute: the QMS reads its store tolerantly into self._state and writes it whole from another method, which W577's per-function guard cannot see (P5.10, high)

**Rows it closes:**

- The A6 row registered by W1192: closed as built

**Changes:**

- agentic_core/vbs/qms.py: _save_state raises StoreUnavailable(path, reason) while _store_unreadable is set, so the write is refused and the store keeps its bytes. run_quality_gates and the defect writers catch it, still return the verdict, and record last_write_refused with the reason. defect_summary and the defects route already say the store is incomplete; they add that writes are refused.
- integration_tests/test_mvp_spine.py: Append the new guard, with the attribute-door AST check. test_w577 is untouched.

**Guard:** test_wNNNN_a_store_read_tolerantly_into_an_object_is_never_written_back_from_it

- A QualityManagementSystem on a truncated store ('{"gates_run": 4, "defects_total": 2, "defe'), then run_quality_gates with a failing metadata: the verdict returns False, the file's bytes are unchanged, and defect_summary says the store is incomplete and writes are refused FAILS IF: Red at HEAD: the truncated store is overwritten with the defaults plus one defect.
- An AST check over agentic_core, outside _archive: no class assigns an attribute from a tolerant read, directly or through its own method's return, and passes that attribute to a writer (atomic_write_json or a known saver) in another method FAILS IF: Red at HEAD on qms.py, and on dcms.py before A5.
- The matcher flags a planted source with HEAD's DCMS shape, and does not flag the heartbeat's shape (a tolerant read of one store, a write of another) FAILS IF: Red if the matcher is vacuous, or so wide it accuses different-store code.

**Blinds:**

- Restore _save_state writing regardless of _store_unreadable -> Leg 1.
- Make the matcher ignore method-return flow -> Leg 3: the planted DCMS shape is not flagged.
- Plant self.cache = self._load_tolerant() and atomic_write_json(path, self.cache) in a scratch module under agentic_core -> Leg 2.

**Pins:**

- test_w534_the_preflight_stops_reading_comparisons_as_keys_and_qms_discloses_its_store (test_mvp_spine.py:31094-31136): counts_are_incomplete True; THIS RATE IS INCOMPLETE; may be better; listing_is_incomplete -> Keep. Reads are unchanged, and the shared store is restored in its finally.
- test_w1091_fu1270_the_one_list_reads_a_support_answer_and_a_quality_defect (test_mvp_spine.py:89845): qms = data_path("qms_state_vbs.json") kept and restored -> Keep.
- test_w577_p218a_a_tolerant_read_is_never_a_write_base_and_a_reader_is_told (test_mvp_spine.py:39618-39680): _TOLERANT577 / _WRITERS577 per-function legs -> Unchanged. The attribute door is held by the new test.

**Rulings it rests on:**

- P5.10 clause 1: a return of a class gets a guard at the mechanism.
- P1.15 and W577 (FU-395, high): a tolerant read is never a write base.
- W534 (FU-298): the QMS discloses an incomplete store on reads; this round adds refusing on writes.
- assure_delivery's rule 'never break a delivery on a QMS hiccup' holds: the verdict still returns.

**Risks:**

- A refused QMS write loses that gate's defect from the store until the store is repaired. That is the intended trade, and it is said on the summary.
- The attribute-door matcher is a heuristic. The planted positive and negative legs bound it.

### A6's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 2, as specified, cannot pass on the fixed tree. After the fix, qms.py still assigns self._state from read_json_reported (:93-94) and passes it to atomic_write_json in _save_state (:97-100), which is exactly the shape the matcher flags. Unless the matcher recognises the refusal guard (an 'if self._store_unreadable: raise StoreUnavailable' before the write), the round's own test is red after the change.

**Conflicts with a ruling:**

- P5.10 clause 1 says 'a return reopens the row' (FABLE:7032-7034; FU-990's why: 'reopen the returned rows'). scripts/followups.py has no reopen subcommand. FU-321's precedent was a dropped row, not a done one. The new row must say why FU-395 is not reopened.

**Bar demands the plan missed:**

- FU-1834 (registered by W1191, open on P4.1: a torn users.json is replaced by a fresh bootstrap store) is FU-395's class through a third door. auth/core.py:117-123 returns {} on any decode error, and callers write that back through _save_users (:126-135). Neither W577's per-function guard nor A6's attribute matcher can see it. A6 claims the class guard 'at the mechanism every caller passes', so it must either cover the except-default loader door or name FU-1834 and the round that guards it.
- The refusal lasts for the life of the process: _state is cached at first load (qms.py:87-95), so a repaired store is not re-read until restart. The summary should say so.

**Fixes asked for:**

- Specify that the matcher accepts a writer guarded by a raise on the reason the tolerant read bound. Add a planted negative: the guarded shape is not flagged.
- Cite FU-1834 and either extend the matcher or state the door it leaves to P4.1.
- State in the row why FU-395 is not reopened.

**Re-sized:** S (unchanged).

## W1207 - A4, B4: The archive says its index uses no embedding; every entity route with a second path parameter answers a second person as no entity

**Closes:** Correction 10 (code half) and its row (A4); gap 16 and its row (B4)

**Owning item:** P3.30 (A4); P5.1 (B4)

**Held on:** W1193

**Rows:**

- FU-1844 (P3.30, low): The archive's search basis and the Horizon page say no embedding backend is installed, while chromadb and its ONNX runtime are
- FU-1858 (P5.1, medium): W1075's census passes over every entity route with a second path parameter, so eight routes are driven for no second person with sign-in on

**Files:** agentic_core/horizon/archive.py; apps/workstation-superapp/src/pages/governance/HorizonCompanion.tsx; apps/workstation-superapp/src/pages/governance/HorizonCompanion.test.tsx; apps/workstation-superapp/src/pages/governance/HorizonCompanion.fixture.json; apps/workstation-superapp/src/components/ArchiveSearchPanel.tsx; apps/workstation-superapp/src/components/ArchiveSearchPanel.fixture.json; (B4 touches only the spine)

**-k:** -k "index_uses_no_embedding or second_path_parameter or test_w552_ or test_w599_p322_ or test_w978_ or test_w1118_ or test_w1075_ or test_w1097_ or test_w932_ or test_w934_ or test_w1088_ or test_pervsb_management_surfaces_tenant_isolated or test_w1077_ or test_w462_ or test_w469_" plus vitest HorizonCompanion.test.tsx and ArchiveSearchPanel.test.tsx

**Notes from the lead:**

Both were judged SOUND. Disjoint: B4 is spine-only.

A4: the apply also rewrites HorizonCompanion.tsx:361's comment ('embeddings: none installed') and :136-137's split quote of P3.22's words, or leg 2 stays red.

B4: take the row id from W1193.

### A4 as planned (cluster A; size XS, 1 round(s))

**Title:** The archive's search and the Horizon page say this index uses no embedding, and no longer say none is installed

**Closes:** Correction n=10, code half: archive.py:29 and :253, HorizonCompanion.tsx:361-364, ArchiveSearchPanel.tsx:10, and two captured fixtures

**Owning item:** P3.30 (a DOC_OVERCLAIM re-stated, ACCEPT 1)

**Owner-gated:** No.

**Depends on:** W1192 carries the plan half of correction 10. A4's files are touched by no other round. It can land before or after A3.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The module docstring says 'There is no embedding backend installed' | horizon/archive.py:29 |
| EXISTS | The manifest's search_basis says 'There is no embedding backend installed' | archive.py:252-254; embedding_backend None at :251 and :348 |
| EXISTS | The page draws 'embeddings: none installed' | HorizonCompanion.tsx:361-364, comment at :330 |
| EXISTS | The vitest pins the text | HorizonCompanion.test.tsx:131 (title) and :139 toBe('embeddings: none installed') |
| EXISTS | Captured fixtures hold the old sentence | HorizonCompanion.fixture.json:301 and ArchiveSearchPanel.fixture.json:96 |
| EXISTS | The ArchiveSearchPanel comment says 'no embeddings are installed' | ArchiveSearchPanel.tsx:10 |
| EXISTS | An embedding backend is installed | requirements.txt:16 (chromadb) and :92 (onnxruntime). A3 leaves them declared. |
| EXISTS | The suite needs only 'no embedding' in the basis, embedding_backend None and the testid | test_w552 :34094-34096; test_w599_p322 :43895-43910 |
| EXISTS | The fixture checks compare keys, or the search bodies, not the scan's basis | test_w978 :82636-82645; test_w1118 :91641-91664 (scan compared by counts; search()'s basis at archive.py:343-347 has no 'installed') |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The archive's search basis and the Horizon page say no embedding backend is installed, while chromadb and its ONNX embedding model are (P3.30, low)

**Rows it closes:**

- The A4 row registered by W1192: closed as built

**Changes:**

- agentic_core/horizon/archive.py: :29 and :252-254 become: search is this platform's OWN LEXICAL index — exact token matching, no embedding, no stemming and no synonyms; this index uses no embedding model, so it is not semantic recall.
- apps/workstation-superapp/src/pages/governance/HorizonCompanion.tsx: The :330 comment changes, and :361-364 draws 'embeddings: none used by this index'. The data-testid="horizon-archive-embeddings" is kept.
- apps/workstation-superapp/src/pages/governance/HorizonCompanion.test.tsx: The :131 title and the :139 expectation change to the new words.
- HorizonCompanion.fixture.json:301 and components/ArchiveSearchPanel.fixture.json:96: Recapture search_basis from the live route.
- apps/workstation-superapp/src/components/ArchiveSearchPanel.tsx: The :10 comment says this index uses no embedding.
- docs/FABLE_DELIVERY_PROMPT.md: Add a dated note at P3.22 (:6157-6158, :6179): the surface now says 'none used by this index'.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_the_archive_says_its_index_uses_no_embedding_and_claims_nothing_about_what_is_installed

- Scan a temp inbox (archive._inbox and _store monkeypatched) and GET /api/v1/horizon/archive: manifest.embedding_backend is None, 'no embedding' is in search_basis, and 'installed' is not FAILS IF: Red at HEAD.
- No backend module under agentic_core and no page under apps/workstation-superapp/src carries 'no embedding backend installed', 'embedding backend installed', 'no embeddings are installed' or 'none installed' FAILS IF: Red at HEAD, on four sites.
- The captured fixtures' search_basis equals the live manifest's FAILS IF: A keep leg. Red if a fixture is left stale.
- vitest: the panel draws 'embeddings: none used by this index' with the server's basis beside it FAILS IF: Red on HEAD's page.

**Blinds:**

- Restore archive.py:253's sentence -> Legs 1 and 3.
- Restore 'none installed' in HorizonCompanion.tsx -> Leg 2 and the vitest.
- Restore the ArchiveSearchPanel.tsx:10 comment -> Leg 2.
- Leave HorizonCompanion.fixture.json:301 unrecaptured -> Leg 3.

**Pins:**

- HorizonCompanion.test.tsx (HorizonCompanion.test.tsx:139): toBe('embeddings: none installed') -> Change on purpose to 'embeddings: none used by this index'.
- test_w552_the_asset_index_counts_match_a_recount_and_no_secret_is_indexed (test_mvp_spine.py:34094-34096): "no embedding" in _m2["search_basis"].lower() -> Keep: the new sentence contains 'no embedding'.
- test_w599_p322_a_passage_without_a_resolvable_location_cannot_be_cited (test_mvp_spine.py:43895-43910): data-testid="horizon-archive-embeddings" in some .tsx; "not semantic recall" in _res["basis"] -> Keep the testid. search()'s basis is unchanged.
- test_w978_fu399_the_companion_reads_the_index_it_is_given_and_says_a_failed_read (test_mvp_spine.py:82610-82623): "{archive.manifest.search_basis}" in page; "Search here is this platform’s own LEXICAL index" not in page -> Keep. The page still draws the server's basis.
- test_w1118_fu399_the_archive_search_says_each_passage_by_its_line_and_what_it_could_not_look_inside (test_mvp_spine.py:91661-91664): live.json() == fx[key]["body"] for found and none -> Keep. search() bodies are unchanged; the scan body is recaptured.

**Rulings it rests on:**

- P2.13 and P3.22: the surface says lexical, not semantic recall. That property is kept.
- P3.30 ACCEPT (1).

**Risks:**

- If the Owner later drops chromadb, 'none installed' would be true again. The new words stay true either way.

### A4's refutation: **SOUND**

**Bar demands the plan missed:**

- HorizonCompanion.tsx:361 is a comment that itself says 'embeddings: none installed'. It sits inside the :361-364 range the change names; the apply must rewrite the comment line, or leg 2 stays red.
- HorizonCompanion.tsx:136-137 quotes P3.22's clause words split across two lines, so leg 2 cannot see them. Restate them for consistency with the dated note at P3.22, which is a done item whose clause (FABLE:6157-6158) names the surface words.

**Fixes asked for:**

- Name :361's comment and :136-137 in the apply.

**Re-sized:** XS (unchanged). Checked: archive.py:29, :251-254, :343-348; the fixtures at :300-301 and :95-96; HorizonCompanion.test.tsx:131, :139-140; pins in test_w552 (:34094-34096), test_w599 (:43894-43909), test_w978 (:82610-82623) and test_w1118 (:91641-91664) all survive the new sentence.

### B4 as planned (cluster B; size S, 1 round(s))

**Title:** Every entity route with a second path parameter is driven as a second person against real seeded state, and named with the test that holds it

**Closes:** The census row W1192 registers on P5.1

**Owning item:** P5.1, beside FU-1262, FU-1263 and FU-1274, whose census this extends

**Owner-gated:** Nothing. Sign-in is switched on only inside the test process (monkeypatched), as in test_w1075.

**Depends on:** Nothing else in this cluster, and W1192's row. If B5 lands first, its new route has only an entity parameter, so W1075's walk drives it and this test's set is unchanged.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The census skips any route with a non-entity path parameter | integration_tests/test_mvp_spine.py:88010 ('if [n for n in pn if not entityish(n)]: continue') |
| EXISTS | Eight mounted routes have an entity path parameter beside another one | vsb.py:1435 (website page), :1669 (webapp page), :1828 (mobile page), :2031 (body section), :3098 (review-gate status), :3108 (review-gate decision); entity_specialists.py:230 (retire), :338 (sign). Prefixes are /api/v1/vsb (vsb.py:44) and /api/v1/entity-specialists (entity_specialists.py:63). |
| EXISTS | Each of them checks access first | _require_vsb_access at vsb.py:1438, :1672, :1831, :2038, :3101, :3111; _require_entity at entity_specialists.py:233 and :344 |
| EXISTS | The trailing-slash mobile route is reached by the census but not guarded in effect | vsb.py:1827 has no second parameter. The census establishes with ship_output False (test_mvp_spine.py:87975), so both ids answer 404 'No phone app generated'. |
| EXISTS | The census compares statuses unless both answers are 200 | test_mvp_spine.py:88053-88056 |
| EXISTS | The seeding routes exist | POST /{vsb_id}/website, /webapp and /mobile (vsb.py:1288, :1601, :1757); POST /{vsb_id}/review-gates (vsb.py:3070-3095); POST /api/v1/entity-specialists/{vsb_id} (entity_specialists.py:186-225; Signing at :108-113) |
| EXISTS | The pattern for naming routes with the test that holds them | test_w1097 HELD dict (test_mvp_spine.py:90519-90561) |
| PARTIAL | Second-person cover elsewhere | Only sign is driven for a second person (test_w934, :79221). test_w932 (:79031) drives retire with sign-in off only. test_w1088 (:89466) drives the decision for the first person only. FU-1262's close note says 'a census over every such route'. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- W1075's census passes over every entity route with a second path parameter, so eight routes are driven for no second person with sign-in on (P5.1, medium)

**Rows it closes:**

- the census row W1192 registers (built)

**Changes:**

- integration_tests/test_mvp_spine.py: test_wNNNN_every_entity_route_with_a_second_path_parameter_answers_a_second_person_as_no_entity appended. With sign-in on and two made-up people: person one establishes an entity and generates its website, webapp and mobile pages; attaches one specialist (a discipline from DISCIPLINES, lapse date after today); produces a deliverable; and gates stage 'design'. Each of the eight routes, and /mobile/page/, is called with second-parameter values the route accepts ('index', 'design', the real specialist id) and a body that passes validation ({'reason': ...}, {'decision': 'approve'}, {'text': 'a made-up design section'}, a Signing body). The second person is compared with an id that names no entity on status and normalised body (W1075's norm). Person one is driven last as the positive control. A HELD dict names each route with this test (and test_w934 for sign); the enumerated set must equal HELD. test_w1097's docstring sentence 'W1075's walk drives every route that takes an entity's id' is corrected (it is not an assert).
- docs/FOLLOWUPS.json: The row is closed as built. If a hole is found, the handler is fixed in this round and the close note says which.

**Guard:** test_wNNNN_every_entity_route_with_a_second_path_parameter_answers_a_second_person_as_no_entity

- The census of this class: the mounted routes with an entity path parameter and another path parameter equal HELD's eight, each naming the test that holds it FAILS IF: a new such route appears unnamed, or a named one is removed
- Positive control: person one is answered on each of the eight and on /mobile/page/ with something other than the not-found answer (200 for the pages, the gate status, the body section and the decision; past the entity check for sign and retire) FAILS IF: the setup leaves the owner at not-found, which would make every second-person leg vacuous
- The second person gets exactly the answer, status and normalised body, that an id naming no entity gets, and no answer carries person one's canary FAILS IF: any route answers the second person past its access check
- No call in the test answers 500 FAILS IF: a broken check (a NameError, or a None entity) passes as a refusal
- Nothing of person one's changed under the second person's calls: the specialist is still active, the design gate has no decision, the design section holds person one's text FAILS IF: a write route acted for the second person

**Blinds:**

- In decide_review_gate, replace _require_vsb_access with an unchecked _load_vsb -> Leg 3: the second person's approve answers 200 against a 500 or 404 for no entity, and leg 5's gate shows a decision.
- In retire, replace _require_entity with an existence-only check -> Legs 3 and 5: the real specialist is retired by the second person.
- Drop the check from get_vsb_website_page -> Leg 3: the generated page is served to the second person.
- Replace the body section's check with _load_vsb -> Legs 3 and 5: the second person writes the design section.
- Remove one route from HELD -> Leg 1's set equality.
- Leave out the page generation in setup -> Leg 2: the owner gets 404 'No website generated', so the positive control fails.

**Pins:**

- test_w1097_fu1274_every_route_the_entity_walk_passes_over_is_named_and_held (test_mvp_spine.py:90520 (docstring)): 'W1075's walk drives every route that takes an entity's id as a second person' -> Correct the docstring to name the class this test now holds. There is no assertion to change.
- test_w1075_fu1262_with_sign_in_on_no_route_reads_or_writes_another_persons_entity_by_its_id (test_mvp_spine.py:88010): the skip of routes with a second path parameter -> Unchanged. The new test holds the class the skip passes over, and the census docstring is left as it is.

**Rulings it rests on:**

- §17.5 invariant 1 (user isolation), as FU-1061 and FU-1262 measured it route by route
- OWNER RULING 2026-11-20 (evening): sign-in only in a test process until the Owner's machine (FABLE:6737-6739)
- FU-1262 and FU-1274 ride P5.1, and this row rides beside them

**Risks:**

- Generating three page sets on the floor makes the test slower. Generate once and reuse the entity across legs.
- The decision changes the entity's derived status. Drive the owner's approve last.
- If a handler turns out to leak, the fix lands in this round and the round grows past S.

### B4's refutation: **SOUND**

**Fixes asked for:**

- Checked and found right:
  - A static scan of route decorators in agentic_core finds exactly the eight mixed-parameter entity routes, and no router prefix carries a parameter.
  - Each handler calls _require_vsb_access or _require_entity first.
  - The census skips at test_mvp_spine.py:88010, establishes with ship_output False (:87975) and compares only statuses unless both answers are 200 (:88053-88056).
  - The seeding routes and the body models fit the plan: _FOUNDER_SECTIONS, GateDecisionRequest, Signing, Retirement.
  - Generating the pages before gating 'design' avoids _refuse_gated (vsb.py:1297).
  - test_w1097's census (:90546-90565) excludes these routes, so only its docstring changes.
  - Each blind changes the answer the second person gets.
  Only note: take the row's id from W1193's registration, not W1192's.

**Re-sized:** S, 1 round

## W1208 - B9: The privacy screen reads git history for credentials, read-only, and says where a shallow walk stopped

**Closes:** Its row (P4.5), the history half of v40 gap 4

**Owning item:** P4.5

**Held on:** W1193

**Rows:**

- FU-1864 (P4.5, low): The privacy screen reads only the current tree: nothing reads git history for a credential

**Files:** agentic_core/privacy_exposure.py; scripts/privacy_check.py; config/privacy_history_allow.json (new); docs/PRIVACY_EXPOSURE_RUNBOOK.md

**-k:** -k "reads_history_for_credentials or test_w732_ or test_w808_ or test_w749_ or test_w462_ or test_w469_" plus integration_tests/test_no_committed_credentials.py

**Notes from the lead:**

Refuter fixes applied:
- It points to FU-1837 (W1191), never a W1192 row. A sentence is appended to FU-1837's why naming the history run as a later step, after the host's alert list.
- A full-clone finding that FU-1837 already covers is recorded under it.
- Leg 3 clones with file:// and --depth 1, because git ignores --depth on a local path.
- Pins at test_w732 :66372 and :66445 are kept.

### B9 as planned (cluster B; size S, 1 round(s))

**Title:** The privacy screen reads git history for credentials, read-only, and says where a shallow walk stopped

**Closes:** The history-mode row W1192 registers on P4.5

**Owning item:** P4.5, with the slot's reason stated: before the release machine holds anyone's data, the Owner's provider accounts must be known clean. History never ships in the image (.dockerignore excludes .git), so it rides the deploy's pre-flights.

**Owner-gated:** Revoking any credential is the Owner's: cluster D's OWNER row for W729's values goes in W1192 and should name this mode's run as its first step. Rewriting history is the Owner's and is never done. The run on a full clone is for a session on the Owner's machine, because this clone is shallow. Each distinct finding there becomes one OWNER row per provider account.

**Depends on:** Nothing in this cluster. W1192 registers the row (cluster D's W729 OWNER row alongside).

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The screen reads only the tracked tree, and history_scanned is hard-coded False | agentic_core/privacy_exposure.py:180-221 (209-212) |
| EXISTS | test_w732 asserts the tree report says history was not scanned, and the default CLI prints so | test_mvp_spine.py:66345-66349 ('NOT SCANNED: git history was NOT scanned') |
| EXISTS | The CLI has a staged mode only | scripts/privacy_check.py:26-58 |
| EXISTS | Allowances are by path and kind, with a reason | privacy_exposure.py:103-113 (load_allowed); config/privacy_allow.json is a list of {path, kind, reason}. An entry with a commit would be read as a tree allowance, so history allowances need a file of their own. |
| EXISTS | This clone is shallow, and W729's commit is in it | git rev-parse --is-shallow-repository gives true, .git/shallow names a27f491b (2026-10-03), and 50abf919 (W729, 2026-10-14) is present |
| EXISTS | The script census requires a refusal for an empty set | test_mvp_spine.py:69608-69653 lists scripts/privacy_check.py; test_w808 drives it over an empty set (:71517) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The privacy screen reads only the current tree: nothing reads git history for a credential, so a key removed before W729 is reported nowhere (P4.5, low)

**Rows it closes:**

- the history-mode row (built; the full-clone run parked for a session on the Owner's machine)

**Changes:**

- agentic_core/privacy_exposure.py: scan_history(root, refs='--all'): git rev-list --objects over the refs, each distinct blob read once through git cat-file --batch and scanned for the credential kind only. Each finding gives the commit that introduced the blob, the path, the kind and the line, never the value. history_scanned is True only when the clone is not shallow and the walk completed, with history_basis naming the refs walked and the blob count. On a shallow clone it stays False and names the boundary commits. Allowances come by (commit, path, kind), with a reason, from config/privacy_history_allow.json; load_allowed is unchanged. scan() is unchanged.
- scripts/privacy_check.py: --history: prints the findings and the basis. Exit 1 on a finding, 0 on none, 2 when it could not run or examined nothing. A shallow clone is said as partial and is never a pass.
- config/privacy_history_allow.json (new): An empty list, with the format documented.
- docs/PRIVACY_EXPOSURE_RUNBOOK.md: Step 6 gains one line: the read-only history mode, that it changes nothing, and that a shallow clone stops it.
- integration_tests/test_mvp_spine.py: The new test, run in temporary repositories.

**Guard:** test_wNNNN_the_privacy_screen_reads_history_for_credentials_and_says_where_its_walk_stopped

- History is read: in a temp repository, commit 1 adds notes/k.txt holding a key-shaped value built at runtime, and commit 2 removes it. scan() of the tree finds nothing; scan_history finds one credential finding naming commit 1, notes/k.txt and its line FAILS IF: only HEAD's tree is walked
- No value travels: no eight-character piece of the value appears in the report's JSON or the CLI's output FAILS IF: the matched text is put in a finding
- Coverage said: the full walk sets history_scanned True with its refs and blob count; on a --depth 1 clone of the temp repository, history_scanned is False and the basis names the boundary commit FAILS IF: the mode claims a full walk on a shallow clone
- Allowances by commit: a (commit, path, kind) entry with a reason suppresses only that finding; one without a reason is not honoured; load_allowed reads nothing from the history file FAILS IF: an unexplained allowance is honoured, or a history allowance clears the same path in the tree
- The CLI: --history exits 1 with the finding, 0 once it is allowed, and 2 with 'examined nothing' on a repository with no commits; the default mode still prints 'NOT SCANNED: git history was NOT scanned' FAILS IF: exit codes differ, or test_w732's default output changes

**Blinds:**

- Walk HEAD's tree instead of every blob -> Leg 1: the removed value is missed.
- Put the matched text in a finding -> Leg 2.
- Set history_scanned True without checking for a shallow clone -> Leg 3.
- Honour an allowance with no reason -> Leg 4.
- Read the history allowances into load_allowed -> Leg 4: the tree path is allowed too.

**Pins:**

- test_w732_the_public_tree_holds_no_privacy_exposure (test_mvp_spine.py:66345-66349, :66404): scan()['history_scanned'] is False and 'history was NOT scanned'; the CLI's 'NOT SCANNED: git history was NOT scanned'; the hook runs privacy_check.py --staged -> Keep: scan() and the default output are unchanged.
- test_w808_fu1154_six_instruments_refuse_when_they_examined_nothing (test_mvp_spine.py:71517 onward): privacy_check refuses an empty set -> --history refuses too, with the same words.
- test_w749_an_instrument_that_examined_nothing_refuses_and_reads_what_it_names (test_mvp_spine.py:69617): scripts/privacy_check.py carries 'examined nothing' -> Keep.

**Rulings it rests on:**

- OWNER RULING 2026-10-14: history is kept unrewritten (FABLE:191-193, :296-297; runbook :53-56); a read is not a rewrite
- Runbook step 3: revoke a credential at its provider first, which only the Owner can do
- V6 (FABLE:1035): an Owner's action is never recorded only in a commit message (cluster D's W729 row)

**Risks:**

- Walking every blob of a large history is slow. Read each distinct blob once, cap the bytes per blob as scan() does, and say what was not read whole.
- Finding the commit that introduced a blob costs a git log --find-object per finding. Do it only for findings.
- Known non-credentials (generated demo keys) will need allowances by commit on the full run. That is the session's work on the full clone, not this round's.

### B9's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'cluster D's OWNER row for W729's values goes in W1192' is wrong. W1191 registers that row as FU-1837 (OWNER, high; a scratch copy outside the tree:239-258, :356-358). W1192 then appends 'the revocation is to be done on 2026-11-22, beginning with the repository host's secret-scanning alert list' (W1192's staged apply (a session work file, not in the tree):99-100).

**Guard legs that could not fail:**

- Leg 3 and blind 3: git ignores --depth when cloning a local path ('use file:// instead'). The clone would be full, history_scanned would be honestly True, and the shallow branch would never be driven. Clone with file://.

**Pins the plan missed:**

- test_w732 also asserts history_scanned False at test_mvp_spine.py:66372 (the staged scan) and :66445 (the route's answer). scan() must stay unchanged for those too.

**Conflicts with a ruling:**

- OWNER DECISION 2026-11-21 23:59: W1191, not the record round, registers the W729 row, and the record round must not register it again. The accepted first step is the host's secret-scanning alert list. B9 may add a sentence to FU-1837's why naming the history run as a later step, but not as 'its first step', and no second row for those values.

**Bar demands the plan missed:**

- A full-clone finding already covered by FU-1837 is recorded under that row, not as a new OWNER row.

**Fixes asked for:**

- Point to FU-1837 instead of a W1192 row.
- Use a file:// --depth 1 clone in leg 3.
- List the two further test_w732 asserts as pins.

**Re-sized:** S, 1 round

## W1209 - A2: The fabric preview says a composition runs one stage at a time, and what the org cascade is granted, instead of 'fits' or 'over capacity'

**Closes:** Gap 22, the v40 merged insight (observed concurrency) and its row

**Owning item:** P3.32 (beside FU-1826 and FU-1829)

**Held on:** W1197 (resource_fabric.py)

**Rows:**

- FU-1842 (P3.32, medium): The fabric preview draws 'over capacity' in amber for a composition that runs one stage at a time, and says nothing of what the org cascade is granted

**Files:** agentic_core/api/swarm.py; agentic_core/api/resource_fabric.py; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.test.tsx; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.fixture.json

**-k:** -k "says_how_a_composition_runs or test_w742_ or test_w756_ or test_p330_r6_ or test_w917_ or test_compliance_sealed_ueg_immune_and_routed or test_w829_ or test_w902_ or test_w462_ or test_w469_ or cascade or fabric or homeostasis" plus vitest ResourceFabric.test.tsx

**Notes from the lead:**

Refuter fixes applied:
- Leg 4 records every simulator update made on the test's thread during the two previews. A 0.2 filter cannot work: the cascade projection's load is min(1.0, 0.2 + 18 x 0.08) = 1.0 (homeostasis.py:66).
- The tooltip's energy clause is restated.
- work_budget.basis stays inside test_w756's 200-character window.
- The platform wording of the S18.1 ruling of 2026-11-22 is carried.
- organism is taken from snapshot() unchanged (test_p330_r6 leg E).
- The vitest reads the expected grant from the captured fixture.

### A2 as planned (cluster A; size S, 1 round(s))

**Title:** The fabric preview says a composition runs one stage at a time, and what the org cascade is granted, instead of 'fits' or 'over capacity'

**Closes:** Gap 22 (v43 G3) and the v40 merged insight (the cascade's concurrency guard holds only the reported grant)

**Owning item:** P3.32, beside FU-1826 and FU-1829, the fabric page's open rows. This follows FU-1828/1829's slot_source 'beside FU-1826'. The files are in an area retired with P2.18, so the row names its slot.

**Owner-gated:** No.

**Depends on:** W1192, then A1 (both edit resource_fabric.py's preview path). It must come before A7, which edits swarm.py lines this round's helper sits near.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The chip prints 'admits N · fits / over capacity' from homeostasis.project(len(resolved)) | ResourceFabric.tsx:667-676 and resource_fabric.py:3858 |
| EXISTS | project() compares the count with snapshot()'s cap for four parallel nodes | homeostasis.py:198-213 and :216-219 |
| EXISTS | A composition's stages run in sequence | orchestrator.py:1088 assesses with requested_parallel=1, with the comment 'the cascade runs sequentially, so concurrency isn't capped', and awaits each stage (:1089-1117) |
| EXISTS | Real resources run one at a time | resource_fabric.py:3071-3078, a for loop that awaits each resource |
| EXISTS | Only the org cascade runs officer pairs concurrently, under its own grant | swarm.py:662-673: demand is 3+2×roles+CoEs+3+6 and requested_parallel is min(4, roles). swarm.py:881-891 uses Semaphore(_granted); with a grant of 1 it runs in sequence (:892-896). |
| ABSENT | Something refuses five resources | The only ceiling is MAX_STAGES, enforced at resource_fabric.py:2866-2870 before anything runs |
| ABSENT | project() has a caller other than the fabric | A grep over agentic_core finds only resource_fabric.py:3858 |
| ABSENT | The cascade guard observes concurrency | test_w742 :67459-67466 asserts granted_parallel and csuite_concurrent, both computed from _granted; the Semaphore at swarm.py:883 is a separate use |
| EXISTS | FU-1114's budget-reason span and FU-1112's budget-off span are on the chip | ResourceFabric.tsx:674 and :680-684, pinned by test_w756_fu1114 (:69977-69983) and test_p330_r6 leg E (:56081-56083) |
| ABSENT | A rendered test draws the chip | ResourceFabric.test.tsx serves simulate only for a refusal (:43, :141-148) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The fabric preview draws 'over capacity' in amber for a composition that runs one stage at a time, and says nothing of what the org cascade is granted (P3.32, medium)

**Rows it closes:**

- The A2 row registered by W1192: closed as built. The merged insight is closed by leg 5; it has no row of its own.

**Changes:**

- agentic_core/api/swarm.py: Factor the cascade's role selection, demand and request (:661-665) into a module function cascade_demand(csuite_roles, coe_specialisms) -> (roles, demand_nodes, requested_parallel). cascade_orchestration and the fabric preview both use it, so there is one formula. homeostasis_adaptation's keys are unchanged.
- agentic_core/api/resource_fabric.py: In _model_configuration (:3853-3860), organism_capacity takes projected_posture, organism and work_budget from homeostasis.snapshot() (read-only). It adds stage_concurrency 1 and stage_concurrency_basis: a composition's stages run one after another and its real resources one at a time; nothing caps or refuses that, and a held work budget changes nothing about it. cascade is null, or, for a composition with vsb_org_swarm, {requested_parallel, demand_nodes, granted_parallel, held_by_work_budget, basis}, where granted_parallel comes from homeostasis.assess(demand, requested, read_only=True) and the roles come from the resource's non-placeholder csuite_roles. fits_current_capacity and admitted_max_parallel leave this payload, and project() is no longer called.
- apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx: The type at :112-114 and the chip at :667-676 change. The chip reads '§8 capacity: {posture} · stages run one at a time', plus for the cascade ' · the org cascade: up to {granted} C-Suite pairs at once'. It is violet in both cases and drops 'fits' and 'over capacity'. The tooltip line 'The run will be homeostatically governed at execution time.' says instead what governs the run. The data-testid="fabric-work-budget-reason" span stays and says the budget limits only the cascade's concurrency. The fabric-budget-off block stays verbatim.
- apps/workstation-superapp/src/pages/synthesis/ResourceFabric.test.tsx and ResourceFabric.fixture.json: Add two simulate answers captured from the live route on a fresh store: five sequential resources, and a composition with vsb_org_swarm and csuite_roles CSO,CFO,CTO. Add a rendered case for the chip.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_the_fabric_preview_says_how_a_composition_runs_not_that_it_is_over_capacity

- Simulate five sequential resources: organism_capacity.stage_concurrency == 1, cascade is None, fits_current_capacity is absent or not False, and the basis names sequential execution FAILS IF: Red at HEAD: the field is absent and fits is False, since 5 > 4.
- The same with work_budget.gate monkeypatched to hold: stage_concurrency is still 1, nothing says over capacity, and work_budget.holds True is carried FAILS IF: Red at HEAD (admitted 1, fits False). Also red if the hold is drawn as limiting a sequential run.
- With vsb_org_swarm and csuite_roles 'CSO,CFO,CTO': cascade.requested_parallel == 3, demand_nodes == 18, and granted_parallel equals homeostasis.assess(18, 3, read_only=True)['max_parallel'] FAILS IF: Red at HEAD (no cascade block). Also red if the grant is computed from len(resolved).
- A spy on the ATP simulator, as in test_w742 leg 8, sees no advance during either preview FAILS IF: Red under blind 5, where assess is called without read_only.
- POST /api/v1/swarm/cascade with five roles, homeostasis.assess stubbed to grant 2, and gateway.query_meta replaced by a stub that counts in-flight C-Suite and CoE calls with a 50 ms await: at most 2 are in flight, exactly 2 at peak, and with a grant of 1 at most 1 FAILS IF: A keep leg (the merged insight). Red under blind 3, a fixed Semaphore(4).
- The captured simulate answers in ResourceFabric.fixture.json carry the live route's organism_capacity keys FAILS IF: Red if the fixture drifts from the route.
- vitest: the rendered chip for five sequential resources reads 'stages run one at a time' and contains no 'over capacity'; the cascade case reads 'up to 2 C-Suite pairs at once' FAILS IF: Red on HEAD's chip text.

**Blinds:**

- Restore homeostasis.project(len(resolved)) in _model_configuration -> Legs 1-3: there is no stage_concurrency, and fits is False for five.
- Drop the cascade block -> Leg 3.
- Replace Semaphore(_granted) with Semaphore(4) in swarm.py -> Leg 5: 4 calls in flight with a grant of 2.
- Restore the old chip JSX -> The vitest finds 'over capacity'.
- Call homeostasis.assess without read_only=True in the preview -> Leg 4: the simulator advances.

**Pins:**

- test_w756_fu1114_admits_one_carries_its_reason_while_the_budget_holds (test_mvp_spine.py:69977-69983): data-testid="fabric-work-budget-reason" followed within 200 characters by work_budget.basis -> Keep the span and its basis reference.
- test_p330_r6_each_capability_gap_is_stated_where_a_person_meets_it (test_mvp_spine.py:56076-56083): {sim.model.organism_capacity?.organism && !sim.model.organism_capacity.organism.energy_acts && ( ... data-testid="fabric-budget-off" ... limits nothing -> Keep organism on the payload and the block verbatim.
- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67448, :67532): bp["admitted_max_parallel"] == 1 and bp["fits_current_capacity"] is False / ep[...] -> Untouched: project() itself is unchanged.
- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67463-67466): _ha["granted_parallel"] == 1 and _ha["csuite_concurrent"] is False -> Keep. cascade_demand must give the same demand and request.
- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67566-67567): (sim.json()["model"].get("organism_capacity") or {}).get("organism") -> Keep organism.
- test_w917_fu609_the_fabric_page_shows_each_compositions_lifecycle_against_the_apis_own_answers (test_mvp_spine.py:78014-78027): ids read are rendered; page.count("setActErr(await refusalOf(r))") == 6 -> Keep. New testids are added and the count does not change.

**Rulings it rests on:**

- S18.6 (carrying capacity is derived from the work budget). FU-1114 (W756) kept the budget's reason on this chip.
- FU-596's class (W637): a posture word asserting a state the run is not in.
- W742: the projection is read-only (the guard's leg 4).
- P5.10 clause 8: tier-3 rows are batched by file. This row is a misleading-surface row, so it is sequenced with FU-1826/1828/1829 rather than batched with them.

**Risks:**

- project() loses its only production caller. It stays, accurate and tested (test_w742 legs 2 and 7, test_w756); see not_proposed.
- The cascade's grant can change between the preview and the run (immune posture, budget, circadian cycle), so the basis says 'granted now'.
- The concurrency leg must stub gateway.query_meta, not _run_officer, which is a closure, and must count only the cascade's tier calls.

### A2's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 4 is specified 'as in test_w742 leg 8'. That leg filters on load 0.2, which only zero-demand projections carry (test_mvp_spine.py:67541-67544). The new cascade projection assesses demand 18, so load = min(1.0, 0.2+18x0.08) = 1.0 (homeostasis.py:66). Under blind 5, assess(18, 3) without read_only advances the simulator at 1.0 and a 0.2 filter stays green. The heartbeat advances at 0.3 concurrently, so the spy must be keyed by thread and catch any load.

**Pins the plan missed:**

- test_w756_fu1114 (test_mvp_spine.py:69980-69983) needs 'work_budget.basis' within 200 characters after data-testid="fabric-work-budget-reason". The restated wording must sit after the basis expression or stay inside that window.
- test_p330_r6 leg E (:56076-56078) asserts organism_capacity.organism.atp_can_fall is a bool whenever organism is a dict. Take organism from snapshot() unchanged.

**Conflicts with a ruling:**

- Not a conflict yet, but it needs sequencing. Owner ruling 2026-11-22 Q3+NG1 ('platform total until a second person runs work ... every reading says it is the platform's') is designed in cluster B. The chip's budget span is a reading of the platform-wide gate (work_budget.py:422-437), so A2's restated span must say it is the platform's budget, or be sequenced with B's NG1 round.

**Bar demands the plan missed:**

- The tooltip clause '(the budget is switched on, so below 30% it holds the run to one node at a time' (ResourceFabric.tsx:671) misstates a sequential composition in the same way. The change list restates only the last sentence of that tooltip.
- The vitest's 'up to 2 C-Suite pairs at once' should read the grant from the captured fixture. A live capture's grant depends on the organism state at capture time.

**Fixes asked for:**

- Leg 4: record every simulator update made on the test's thread during the two previews and assert none happened.
- Restate the energy clause of the tooltip. Keep work_budget.basis inside test_w756's 200-character window. Carry NG1's platform wording.
- Read the expected grant from ResourceFabric.fixture.json in the vitest.

**Re-sized:** S (unchanged).

## W1210 - A7: Every duration the platform records is read from a monotonic clock

**Closes:** Gap 15 and its row (about 34 sites in 21 files)

**Owning item:** P3.30

**Held on:** W1196, W1197, W1203, W1205, W1209 (shared files)

**Rows:**

- FU-1847 (P3.30, low): About thirty-four durations are taken from the settable wall clock, ten of them reaching record_outcome and the work budget

**Files:** agentic_core/ai/gateway.py; agentic_core/api/resource_fabric.py; agentic_core/api/swarm.py; agentic_core/api/board.py; agentic_core/api/deliverables.py; agentic_core/api/transformation_orchestration.py; agentic_core/api/products.py; agentic_core/api/forge.py; agentic_core/api/synthesis_studio.py; agentic_core/api/sovereign_evolution.py; agentic_core/api/vsb.py; agentic_core/api/native_ai.py; agentic_core/avatars/api.py; agentic_core/avatars/core/recirculation_orchestrator.py; agentic_core/avatars/output/multimodal_renderer.py; agentic_core/change_control/regulator.py; agentic_core/consultation/mushawara/mushawara_bridge_2.py; agentic_core/gaas/v5/uci_v16_omega.py; agentic_core/governance/uci_interceptor.py; agentic_core/mesh/consensus/consensus.py; agentic_core/mesh/discovery/discovery.py; agentic_core/vbs/backbone.py

**-k:** -k "duration_is_read_from_the_monotonic or test_w741_ or test_w742_ or test_w743_ or test_w847_ or test_w772_ or test_w773_ or test_w757_ or test_w829_ or test_w870_ or test_w898_ or test_w941_ or test_w1048_ or test_w641_ or test_p3d_r8_ or test_resource_composition_run_on_native_swarm or test_w462_ or test_w469_ or budget or stream or swarm or deliverable or board or transformation or forge or synthesis or sovereign or vsb"

**Notes from the lead:**

Refuter fixes applied:
- native_ai.py's two sites are added (import time as _t at :622 and :819; durations at :638 and :843). The exact count is recorded; it is about 34, not 32.
- Follow host_observation.py:67's precedent (perf_counter, which is also monotonic), or record why monotonic was chosen instead.
- native_ai.py is edited after A11.
- The row names P3.30 with slot_source, because its avatars/ files would otherwise route it to P2.40.

### A7 as planned (cluster A; size M, 1 round(s))

**Title:** Every duration the platform records is read from the monotonic clock

**Closes:** Gap 15 (v42/v41 G3), widened to the class: about 32 durations in about 20 files

**Owning item:** P3.30, as FU-1121, a budget accounting defect, did. FABLE:6358 says 'a reader of the capacity rides P3.30'.

**Owner-gated:** No. S18.1's 'wall-clock seconds' means elapsed real time, which a monotonic clock measures; the round record says so.

**Depends on:** W1192, then A1, A2 and A3. A7 edits resource_fabric.py, swarm.py and avatars/api.py at lines those rounds do not touch, and its apply script runs on their tree. It must come before A8 (gateway.py) and A10 (the run row's duration at resource_fabric.py:3253).

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | 41 textual 'time.time() -' lines outside _archive, 8 of which are ages of stored stamps or cutoffs that must stay on the wall clock | The eight: orchestrator.py:278, mesh/health/monitor.py:13, config.py:342, organism_status.py:67, products.py:930, economy.py:1667, gaas/v5/circuit_breaker_rl.py:92, work_budget.py:89 |
| EXISTS | Durations taken from a wall-clock start in the same scope, an enclosing scope or a helper | gateway.py:778 (starts at :823, :860, :892, :925); resource_fabric.py:2943/:2995/:3253, :3075/:3078, :3100, :3689/:3709; swarm.py:155, :265, :743, :1243, :1357; board.py:170, :182; deliverables.py:286/:311; transformation_orchestration.py:613; avatars/api.py:305/:327 (alias _time, tuple assignment); products.py:133, :210; forge.py:262; synthesis_studio.py:350, :398; sovereign_evolution.py:375; vsb.py:3677; avatars/core/recirculation_orchestrator.py:236/:273; avatars/output/multimodal_renderer.py:75; change_control/regulator.py:33; consultation/mushawara/mushawara_bridge_2.py:82; gaas/v5/uci_v16_omega.py:148; governance/uci_interceptor.py:124; mesh/consensus/consensus.py:41; mesh/discovery/discovery.py:14; vbs/backbone.py:57. The AST scan found 30 same-scope sites; the gateway helper and the avatar alias were found by reading. |
| EXISTS | Ten of them reach record_outcome and so the budget | resource_fabric.py:2992 and :3720; swarm.py:153 and :741; board.py:168 and :181; deliverables.py:374; transformation_orchestration.py:610; avatars/api.py:326; gateway.py:776 |
| EXISTS | A negative duration spends nothing and is stored raw | operational_excellence.py:199 (max(0, ...)) and :234 (raw); work_budget.py:135-136 (returns when seconds <= 0 and there are no tokens) |
| EXISTS | Sites already on the monotonic clock | app_mvp.py:172-174 (P2.15); orchestrator.py:69; _ai_provenance.py:321 and :338 |
| EXISTS | A start that doubles as a timestamp | recirculation_orchestrator.py:236 start_time also makes cycle_id at :240, so it needs two readings |
| ABSENT | A test pins the clock expressions at these sites | A grep of the suite finds none |
| EXISTS | Tests move a process clock | test_w898 (time.monotonic, :76956-76958); test_w941 (time.time +1000 days, :79863-79866); test_w658 (the immune window) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- About thirty durations are taken from the settable wall clock, ten of them reaching record_outcome and the work budget, so a backward clock step books a run as no work and a forward step books the jump as work (P3.30, low)

**Rows it closes:**

- The A7 row registered by W1192: closed as built

**Changes:**

- agentic_core/ai/gateway.py: The starts at :823, :860, :892 and :925 become time.monotonic(), and _record (:778) subtracts from time.monotonic().
- agentic_core/api/resource_fabric.py, swarm.py, board.py, deliverables.py, transformation_orchestration.py, products.py, forge.py, synthesis_studio.py, sovereign_evolution.py, vsb.py; agentic_core/avatars/api.py, avatars/core/recirculation_orchestrator.py, avatars/output/multimodal_renderer.py; change_control/regulator.py; consultation/mushawara/mushawara_bridge_2.py; gaas/v5/uci_v16_omega.py; governance/uci_interceptor.py; mesh/consensus/consensus.py; mesh/discovery/discovery.py; vbs/backbone.py: Each listed duration's start and end become time.monotonic(). created_at and other stamps stay on the wall clock. recirculation_orchestrator.py takes two readings: wall for cycle_id, monotonic for the duration. The eight stored-stamp ages are untouched.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_every_duration_is_read_from_the_monotonic_clock

- An AST check over agentic_core, outside _archive, finds no match of either shape. Shape (a): a subtraction whose left side is a wall-clock read (time.time() under any alias, including from-imports) and whose right side is a name bound to a wall-clock read in the same or an enclosing function, tuple assignments included. Shape (b): a function that subtracts one of its own parameters from a wall-clock read. Each site kept on purpose is named in the test with its reason; the expected one is mesh/health/monitor.py:13, the age of a stored last-seen stamp. FAILS IF: Red at HEAD (about 32 matches; the round records the exact count).
- The matcher flags a planted '_t0 = time.time(); ...; d = time.time() - _t0', a planted '_t0, x = _time.time(), 1' with alias, and a planted helper 'def _r(t0): return time.time() - t0'. It does not flag work_budget.py:89's shape FAILS IF: Red if the matcher is vacuous, or wide enough to flag stored ages.
- With resource_fabric's time module swapped for a proxy whose time() steps back an hour after the first call (monotonic, strftime, gmtime and the rest pass through), run a saved floor composition through POST /compositions/{cid}/run. The composition_run outcome row's duration_ms is between 0 and the test's own monotonic elapsed plus 50 ms, and seconds_spent in an isolated work-budget store rose by that duration FAILS IF: Red at HEAD: about -3,600,000 ms is stored and nothing is spent.
- The same with a forward step of one hour: duration_ms is not above elapsed plus 50 ms, and the spend does not rise by an hour FAILS IF: Red at HEAD.
- With gateway's time module proxied the same way, drive gateway.stream_meta to the floor (AI_DISABLE_LOCAL is set in the suite). The stream:<agent> model_attempt row's duration_ms lies between 0 and elapsed plus 50 ms FAILS IF: Red at HEAD.

**Blinds:**

- Revert resource_fabric.py:2943 and :2995 to time.time() -> Leg 1 (an AST match) and leg 3 (a negative duration).
- Revert gateway's _floor_t0 to time.time() while _record subtracts from monotonic -> Leg 5 (a nonsense duration). Leg 1 also catches it if _record keeps time.time().
- Revert avatars/api.py:305 to the wall-clock tuple assignment -> Leg 1, through alias and tuple coverage.
- Use one wall-clock reading for both cycle_id and the duration in recirculation_orchestrator.py -> Leg 1.

**Pins:**

- test_w898_the_rate_limiter_takes_no_debt_from_a_clock_read_behind_its_last_refill (test_mvp_spine.py:76956-76958): monkeypatch.setattr(_t898, "monotonic", lambda: ahead) -> Keep. It moves the process's monotonic clock only around the limiter calls.
- test_w941_p53_a_claim_that_an_output_is_wrong_stays_open_until_a_person_answers_it (test_mvp_spine.py:79863-79866): monkeypatch.setattr(_time, "time", lambda: real() + 1000 * 86400) -> Keep. Durations no longer move with it.
- test_w742_the_metabolism_tells_the_truth / test_w743_each_entity_has_its_own_work_budget_and_the_platform_derives_its_carrying_capacity / test_w847_only_the_outermost_run_of_a_nest_spends_the_work_budget (test_mvp_spine.py:67372, :67650, :73518): spend driven with stated seconds; spans hold and spend -> Keep. In the -k run.

**Rulings it rests on:**

- S18.1 (FABLE:2760): the unit is tokens and wall-clock seconds, meaning seconds actually spent. A monotonic clock measures those, so the ruling is untouched.
- P2.15 (FABLE:3368-3369; app_mvp.py:172-174) is the request seam's design note. It is the precedent, not the rule.
- W742 (operational_excellence.py:184): a duration that is not work is not spent.
- FU-1121 (W847): spans are unchanged.

**Risks:**

- On Windows before Python 3.13, time.monotonic ticks in steps of about 15.6 ms, per the Python documentation's 3.13 change note. A sub-16 ms run can read 0 ms there and then spend nothing, as orchestrator.py:69 already does. The Windows CI job is the check.
- About 22 files change. The apply script must be one mechanical edit per listed line, and the AST count must equal the listed sites.

### A7's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- The site list misses agentic_core/api/native_ai.py: 'import time as _t' at :622 and :819, starts at :628 and :824, and the durations '"ms": int((_t.time() - _p0) * 1000)' at :638 (the evaluation probes) and :843 (the baseline cases). These are wall-clock durations in the same scope through an alias. Leg 1's matcher ('time.time() under any alias') will find them, so after the planned edits the round's own leg 1 is red.
- The counts are off: 39 lines contain 'time.time() -', and 42 subtraction lines exist counting mushawara_bridge_2.py:82's no-space form and the _t alias. Eight are kept ages, so about 34 durations, not 32.

**Bar demands the plan missed:**

- Adding native_ai.py makes A11's 'native_ai.py and model_resource.py are touched by no other round' false. The two rounds must be ordered and their edits anchored by text.
- The tree already ruled on this clock choice: host_observation.py:67 uses time.perf_counter, 'not monotonic: on Windows before Python 3.13 monotonic() ticks in ~15.6 ms steps'. Either follow that precedent (perf_counter is also monotonic) or say why not. The plan's risk names the tick, but not the precedent.

**Fixes asked for:**

- Add native_ai.py's two sites to the change list and the expected count; order A7 against A11.
- Use time.perf_counter for durations, as W746 does, or record the reason for monotonic.

**Re-sized:** M: about 34 sites in 21 files.

## W1211 - A8: An attempt the caller abandons is recorded once, as abandoned, spends what it ran, and counts against no model

**Closes:** v40 gap 2 and its row

**Owning item:** P3.30

**Held on:** W1210 (gateway.py starts), W1196 (ceo.py)

**Rows:**

- FU-1848 (P3.30, low): A stream the caller closes, or a model attempt whose task is cancelled, records no outcome and spends nothing

**Files:** agentic_core/ai/gateway.py; agentic_core/ai/native/orchestrator.py; agentic_core/api/operational_excellence.py; agentic_core/horizon/membrane.py; agentic_core/api/v138/ceo.py; agentic_core/projects/api.py; agentic_core/api/v310/business.py; agentic_core/synthesis/api.py

**-k:** -k "caller_abandons or test_w772_ or test_w757_ or test_w847_ or test_w741_ or test_w870_ or test_w986_ or test_w1048_ or test_w554_ or test_w462_ or test_w469_ or stream or sse or ceo or projects or business or synthesis"

**Notes from the lead:**

Refuter fixes applied:
- The fake model waits 0.3 s before its first token, or the test waits 0.3 s between the token and aclose(). As written, the record would show about 0 ms.
- Add only the new kind to each existing filter: :522, :594 and :719 hide model_attempt only, and :542 hides both. Folding model_quality in elsewhere would hide rows from the listing, rankings and summary.
- Add model_attempt_abandoned to membrane.NOT_OBSERVED_KINDS with its reason (test_w554 pins :34388).

### A8 as planned (cluster A; size S, 1 round(s))

**Title:** An attempt the caller abandons is recorded once, as abandoned, spends what it ran, and counts against no model

**Closes:** v40 new gap 2 (reader 2481-3600 gap B), with its refuter's sketch changes

**Owning item:** P3.30, as FU-1103 (W772) and FU-1121 (W847) were

**Owner-gated:** No.

**Depends on:** A7, so gateway.py's starts are already monotonic and the new record uses them.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The owned-model stream records only on success, an empty answer, or in except Exception | gateway.py:823-851 |
| EXISTS | The Claude and OpenAI branches have the same shape, and the floor records after its chunk loop | gateway.py:860-889, :892-922, :925-937 |
| ABSENT | A CancelledError, GeneratorExit or BaseException handler exists in gateway.py, orchestrator.py or operational_excellence.py | A grep finds the only finally blocks at gateway.py:237 and operational_excellence.py:105 |
| ABSENT | stream_meta closes its inner generator | gateway.py:671-688 iterates _stream_meta_inner with no aclosing; contextlib is not imported |
| ABSENT | The orchestrator's attempt loop catches more than ResourceSkipped and Exception | orchestrator.py:429-456 |
| EXISTS | A failure record moves the immune sensor, the breaker and model health | gateway.py:765-771 (immune ai_failure); self_healer.record_failure; orchestrator.py:156-175 (_organism_report); operational_excellence.py:389-421 (kinds at :401); served-last at :465-472; _reorder_by_health at orchestrator.py:254 |
| EXISTS | The infra kinds hidden from the Learning Loop | operational_excellence.py:522, :594 and :719 hide model_attempt; :543 hides (model_attempt, model_quality) |
| EXISTS | SSE consumers of stream_meta | api/v138/ceo.py:558, projects/api.py:567, api/v310/business.py:107, synthesis/api.py:567 |
| ABSENT | A test closes a stream with aclose() | The suite has no aclose. Its CancelledError sites (:68509, :76653) test other code. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- A stream the caller closes, or a model attempt whose task is cancelled, records no outcome and spends nothing: the stream and attempt loops record only on return or Exception (P3.30, low)

**Rows it closes:**

- The A8 row registered by W1192: closed as built

**Changes:**

- agentic_core/ai/gateway.py: Each branch of _stream_meta_inner carries one recorded flag. A finally block records an abandoned attempt through a new helper _record_abandoned(served_by, is_external, t0, tokens) only when no other path recorded. The helper calls record_outcome with kind 'model_attempt_abandoned' and basis 'abandoned by the caller after N s', and calls neither immune.record nor self_healer.record_failure. The floor branch is covered too. stream_meta wraps the inner generator in contextlib.aclosing.
- agentic_core/ai/native/orchestrator.py: The attempt loop gains 'except asyncio.CancelledError: record the abandoned attempt; raise', and calls neither _record_model(False) nor _organism_report.
- agentic_core/api/operational_excellence.py: One _INFRA_KINDS = ('model_attempt', 'model_quality', 'model_attempt_abandoned') is used at :522, :543, :594 and :719. model_health and served-last keep their kind filters, so they never read the new kind.
- agentic_core/api/v138/ceo.py, agentic_core/projects/api.py, agentic_core/api/v310/business.py, agentic_core/synthesis/api.py: Each SSE generator iterates gateway.stream_meta under contextlib.aclosing.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_an_attempt_the_caller_abandons_is_recorded_once_as_abandoned_and_counts_against_no_model

- Set up an isolated outcomes store, AI_DISABLE_LOCAL unset, and _stream_owned_model replaced by a fake that yields 'a', waits 0.3 s, then yields 'b'. Take one token from gateway.stream_meta, then await aclose(). Immediately, with no loop tick, there is exactly one model_attempt_abandoned row, with served_by ollama, duration_ms of at least 300 and the abandoned basis, and seconds_spent rose by that duration FAILS IF: Red at HEAD (no row).
- Before and after that: model_health()['ollama'] window_runs and success_rate, the self_healer state for 'ollama', and the immune sensor's errors for 'model:ollama' are all unchanged FAILS IF: Red under blind 5 (the abandonment recorded as a failure).
- Cancel an orchestrator completion 0.2 s into a 1 s fake model: exactly one abandoned row with duration_ms of at least 200, and the breaker and health are unchanged FAILS IF: Red at HEAD.
- The Learning Loop's default outcomes listing (GET /api/v1/operations/outcomes) shows no model_attempt_abandoned row FAILS IF: Red if the new kind is not in _INFRA_KINDS.
- The empty-answer case still records one failed model_attempt and no abandoned row FAILS IF: Red under blind 4 (a double record).

**Blinds:**

- Record only after the loop, as at HEAD -> Legs 1 and 3: no row.
- Record a duration of 0 -> Leg 1: the spend does not move.
- Record success True or kind model_attempt -> Legs 1 and 2: the kind or basis assertion fails, or health moves.
- Record in both the finally and the except path -> Leg 5 and 'exactly one'.
- Record through _record(..., ok=False) -> Leg 2: immune records ai_failure and the success rate falls.
- Remove aclosing from stream_meta -> Leg 1: the inner finally has not run when aclose() returns.

**Pins:**

- test_w772_fu1103_an_empty_local_answer_in_the_stream_is_a_recorded_failure (test_mvp_spine.py:70395): an empty local answer is one failed model_attempt with its count -> Keep. The flag stops the finally from adding a second record.
- test_w757_fu1123_the_immune_sensor_hears_a_streamed_model_serve (test_mvp_spine.py:69998): the immune sensor observes a served stream and records a failed attempt -> Keep.
- test_w1048_fu399_the_native_ai_page_says_each_failure_beside_the_action_that_met_it (test_mvp_spine.py:86501-86520): served-last read from model_attempt rows -> Keep. Served-last ignores the new kind.

**Rulings it rests on:**

- FU-1103 (W772): an attempt the budget never saw is a defect.
- FU-1121 (W847): spans hold an inner record, so an abandoned attempt inside a run is held by that run.
- W375 and W380: a false failure must not demote the owned model below the floor. Hence the separate kind.
- S18.1: seconds actually spent are spent, so the abandoned seconds are spent.

**Risks:**

- The immediate-assertion leg depends on aclosing closing the inner generator inside aclose(). Without it, the asyncio finalizer schedules the close as a task, which is why blind 6 is red.
- Four SSE routes change their iteration. Their stream tests are in the -k.

### A8's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Leg 1 as written fails on a correct change. The fake yields 'a', waits 0.3 s, then yields 'b'. The test takes one token and calls aclose() at once, so the inner generator is closed at the yield of 'a' before the wait starts (ArabicStreamFilter.feed does not buffer, composed_text.py:157-170). The recorded duration is about 0 ms, not 300 or more, so blind 2 ('record a duration of 0') is not told apart either.

**Bar demands the plan missed:**

- One _INFRA_KINDS at :522, :542, :594 and :719 changes behaviour the round does not claim. :522 (the default /outcomes listing), :594 (/rankings) and :719 (/summary) exclude only model_attempt today; :542 alone excludes model_quality too. Folding model_quality in newly hides those rows from the Learning Loop's listing, rankings and summary.
- horizon/membrane.py:54-60 keeps NOT_OBSERVED_KINDS as a disclosure ('an exclusion nobody can see is indistinguishable from a path the seam failed to reach'). The new mechanism-inside-a-run kind belongs there with its reason, beside model_attempt (pinned at test_mvp_spine.py:34388).

**Fixes asked for:**

- In leg 1, make the fake wait 0.3 s before its first token, or have the test wait 0.3 s between the token and aclose(). Keep 'immediately after aclose()'.
- Add only the new kind to each existing filter (or make the model_quality change a stated change with its own leg).
- Add 'model_attempt_abandoned' to NOT_OBSERVED_KINDS with its reason.

**Re-sized:** S (unchanged).

## W1212 - A9: The run history, the Learning Loop and the work budget say that a run whose process ended before it finished left no outcome of its own and spent nothing

**Closes:** Gap 9, restated, and its row

**Owning item:** P3.30

**Held on:** W1210, W1211

**Rows:**

- FU-1849 (P3.30, low): The Learning Loop says it shows the outcomes of every run and the runs listing says every run persists, but a run whose process ends before it returns leaves no row and spends nothing

**Files:** agentic_core/api/resource_fabric.py; agentic_core/molecular/work_budget.py; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.test.tsx; apps/workstation-superapp/src/pages/OperationalExcellence.tsx; apps/workstation-superapp/src/pages/OperationalExcellence.test.tsx

**-k:** -k "process_ended_left_nothing or test_w742_ or test_w986_ or test_w917_ or test_w462_ or test_w469_" plus vitest OperationalExcellence.test.tsx, ResourceFabric.test.tsx, InstrumentCellPanel.test.tsx

**Notes from the lead:**

Refuter fix: the wording does not overclaim. A run whose process ended before it finished records no outcome of its own and spends nothing, but the model attempts it made stay listed, unattributed, under model_attempt (orchestrator.py:58-71). The same words go in runs_basis, spend_basis and the page, with a vitest assertion on them.

### A9 as planned (cluster A; size S, 1 round(s))

**Title:** The run history, the Learning Loop and the work budget say that a run whose process ended before it finished left no row and no spend

**Closes:** Gap 9 (v42/v41 G2), restated as refuter_rulings recommended. The M build of start rows is not proposed.

**Owning item:** P3.30

**Owner-gated:** No.

**Depends on:** A7 (resource_fabric.py), and A8 if the spend basis is to mention abandoned attempts.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | Only a refused run is written before the pipeline | resource_fabric.py:2952-2967 (W762, under store_lock) |
| EXISTS | The completed run's row and its record_outcome come only after the pipeline returns | resource_fabric.py:2985-3001 and :3201-3256 |
| ABSENT | A started or in-progress run state | grep: 'in_progress' in resource_fabric.py is a plan objective's status |
| EXISTS | A raised run's held seconds are spent | operational_excellence.py:72-89 (_span_close) and :96-108. Only a killed process loses them. |
| EXISTS | The Learning Loop header claims every run | OperationalExcellence.tsx:93 'The real, recorded outcomes of every run' |
| EXISTS | The runs listing claims every run persists | resource_fabric.py:1496-1499; its answer carries store_incomplete and listing_is_incomplete only |
| EXISTS | The spend basis is silent on a run whose process died | work_budget.py:348-354; test_w742 pins 'not counted' at :67518 |
| EXISTS | Pages read the runs listing | ResourceFabric.tsx:411; InstrumentCellPanel.tsx:173 |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The Learning Loop says it shows the outcomes of every run and the runs listing says every run persists, but a run whose process ends before it returns leaves no row and spends nothing (P3.30, low)

**Rows it closes:**

- The A9 row registered by W1192: closed as built

**Changes:**

- agentic_core/api/resource_fabric.py: The list_composition_runs docstring is restated. The answer gains runs_basis: a run is written when it returns or is refused, so a run whose process ended before it finished (a restart, a release, an out-of-memory kill) leaves no row.
- apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx (with ResourceFabric.test.tsx): The run history draws runs_basis when present (data-testid fabric-runs-basis), with a rendered case.
- apps/workstation-superapp/src/pages/OperationalExcellence.tsx (with OperationalExcellence.test.tsx): The :92-96 header says the recorded outcomes of the runs that returned or were refused, and that a run whose process ended before it finished leaves none, with a rendered assertion.
- agentic_core/molecular/work_budget.py: spend_basis (:348-354) adds that a run whose process ended before it recorded its outcome spends nothing. It keeps 'not counted'.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_the_run_history_and_the_budget_say_that_a_run_whose_process_ended_left_nothing

- GET /api/v1/resources/compositions/runs answers runs_basis naming a process that ended before the run finished FAILS IF: Red at HEAD.
- work_budget.state()['spend_basis'] says a run whose process ended before it recorded its outcome spends nothing, and still says 'not counted' FAILS IF: Red at HEAD.
- list_composition_runs.__doc__ no longer says 'every run persists' FAILS IF: Red at HEAD.
- vitest: the Learning Loop header contains no 'every run' and says what a run that never returned leaves; the fabric's run history draws runs_basis FAILS IF: Red at HEAD's pages.

**Blinds:**

- Restore 'every run' in OperationalExcellence.tsx -> The vitest leg.
- Drop runs_basis from the listing -> Legs 1 and 4.
- Restore the old spend_basis -> Leg 2.

**Pins:**

- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67518): "not counted" in wb.state()["spend_basis"] -> Keep.
- ResourceFabric.test.tsx (ResourceFabric.test.tsx:45): reply(200, { runs: [], listing_is_incomplete: false }) -> Add runs_basis to the serve. The page draws it only when present.
- test_w917_fu609_the_fabric_page_shows_each_compositions_lifecycle_against_the_apis_own_answers (test_mvp_spine.py:78014-78027): ids read are rendered; setActErr count == 6 -> Keep.

**Rulings it rests on:**

- P3.30 ACCEPT (1) re-stated, and (2): the disclosure is driven at the page, not only in the API.
- W762 (FU-902): refused runs are recorded. W847: a raised run spends what it held.

**Risks:**

- The InstrumentCellPanel also reads the listing. It ignores the new field, which its vitest confirms.

### A9's refutation: **NEEDS_FIXES**

**Bar demands the plan missed:**

- The restated Learning Loop header ('a run whose process ended before it finished leaves none') would overclaim in its turn. As each stage's model call finishes, _record_model appends a model_attempt row (orchestrator.py:58-71). These rows carry no run id and no owner, and they stay after a killed run, hidden from the default listing but in the store (the gap-9 refuter's evidence correction 4, which overrides the synthesis).

**Fixes asked for:**

- Word it as: a run whose process ended before it finished records no outcome of its own, and spends nothing; the model attempts it made may be listed unattributed under model_attempt. Use the same wording in runs_basis and spend_basis. Add a vitest assertion on the wording.

**Re-sized:** S (unchanged). Checked: OperationalExcellence.tsx:92-96, resource_fabric.py:1496-1514, work_budget.py:348-354. No pin on the three sentences beyond test_w742's 'not counted' (:67518).

## W1213 - A10: Two composition runs finishing together both reach the history: the completed-run write takes the store's lock

**Closes:** Its site row

**Owning item:** P3.30

**Held on:** W1212

**Rows:**

- FU-1850 (P3.30, low): The completed composition run's history row is written by a read-modify-write of composition_runs.json without the store's lock, so two runs finishing together in two processes or threads can drop one

**Files:** agentic_core/api/resource_fabric.py

**-k:** -k "two_runs_finishing_together or test_resource_composition_run_on_native_swarm or test_lgc_spec_ or test_w829_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fix: the row states its condition. There is no await between read_json_strict (:3209) and atomic_write_json (:3256), so the loss needs two processes or threads. The class census row stays open on P5.10 with no round here. It leads with swarm.py's tier stores and drops agent_hub.py, whose read-modify-writes are under store_lock (:287-291, :394-408).

### A10 as planned (cluster A; size XS, 1 round(s))

**Title:** Two composition runs finishing together both reach the history: the completed-run write takes the store's lock

**Closes:** The race both gap-9 refuters found alongside gap 9 (resource_fabric.py:3203-3256 without store_lock). It also registers, and does not build, the census of the same shape.

**Owning item:** P3.30 for the site. The five other shape matches go to P5.10 as an open class row.

**Owner-gated:** No.

**Depends on:** A7 (the duration line :3253 in the same block), and after A9.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The completed-run write reads, appends and replaces composition_runs.json with no store_lock | resource_fabric.py:3203-3256 (read_json_strict :3209, atomic_write_json :3256) |
| EXISTS | The refused path takes the lock | resource_fabric.py:2955-2966 |
| PARTIAL | Other strict read-modify-writes with no lock around the write | An AST census at 89c25eed finds agent_hub.py post_message (:279) and register_agent (:418), integration_surface.py spawn_twin (:633), swarm.py cascade_orchestration (:1061, :1211, :1212, :1470) and heartbeat.py screen_living_vsb (:164). It is a syntax match: a caller may hold the lock, or the write may be to another store. |
| ABSENT | A repo-wide lock guard exists | The only AST lock check is W752's, scoped to runtime config (test_mvp_spine.py:68853-68880) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The completed composition run's history row is written by a read-modify-write of composition_runs.json without the store's lock, so two runs finishing together can drop one (P3.30, low)
- Five more functions read a shared store strictly and write it back with no lock around the write (agent_hub post_message and register_agent, integration_surface spawn_twin, swarm cascade_orchestration at four sites, heartbeat screen_living_vsb), measured by syntax and each still to be read (P5.10, medium)

**Rows it closes:**

- The A10 site row (P3.30): closed as built. The P5.10 class row stays open.

**Changes:**

- agentic_core/api/resource_fabric.py: The end-of-run write is factored into _append_run_row(row), which reads strictly, appends, caps at _cr[-100:] and writes inside 'with store_lock(_cr_store):'. It is the same idiom as :2955.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_two_runs_finishing_together_both_reach_the_history

- read_json_strict is monkeypatched to sleep 0.2 s after reading composition_runs.json, and four threads call _append_run_row with distinct run ids: all four rows are in the store FAILS IF: Red at HEAD (each thread writes the same base, so three rows are lost).
- AST: every atomic_write_json on composition_runs.json in resource_fabric.py sits inside a with store_lock(...) on the same path FAILS IF: Red at HEAD (:3256).
- A real floor composition run still files one row, with run_record persisted True FAILS IF: A keep leg: red if the refactor breaks the run.

**Blinds:**

- Remove the store_lock around _append_run_row's body -> Legs 1 and 2.
- Lock only the write, not the read -> Leg 1: interleaved reads still lose rows.

**Pins:**

- test_lgc_spec_a_kept_proposal_is_immutable_versioned_linked_to_its_run_and_run_again (test_mvp_spine.py:57995): a refused replay is filed, refused, with its specification link (FU-902) -> Keep.
- test_resource_composition_run_on_native_swarm (test_mvp_spine.py:2935-2960): the run persists and is QMS-gated -> Keep.

**Rulings it rests on:**

- P1.15 and W442-W468: a shared store is read and written under its lock.
- P5.10 clause 1: the class needs a guard at the mechanism. The class row carries that.

**Risks:**

- store_lock raises after its timeout (FU-301's notes). A run that cannot take the lock files run_record persisted False with the reason, as today's except does.

### A10's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- The census claim is PARTIAL in the wrong direction: 2 of its 5 functions are false positives (agent_hub.py post_message :279 and register_agent :418, whose read-modify-writes are under store_lock at :287-291 and :394-408).
- The site row says 'two runs finishing together can drop one' without its condition. There is no await between read_json_strict (:3209) and atomic_write_json (:3256), and the image runs one uvicorn process (Dockerfile:73), so one event loop cannot interleave them. The loss needs two processes or threads. store_lock serialises both (config.py:302-313).

**Bar demands the plan missed:**

- The census row should lead with the one in-process lost update the census found: swarm.py's tier stores are read at :688/:699 and written back at :1211/:1212 after every awaited tier call.

**Fixes asked for:**

- State the condition in the site row's why. Rewrite the census row as in RECORD.

**Re-sized:** XS (unchanged).

## W1214 - B3: The work budget says its figure is the platform's wherever it is read, lists every reader, and the brief's limits and the guide's switches are held to the code

**Closes:** Gap 13, corrections 6 and 7, v40 gap 1, and their two rows

**Owning item:** P4.5 and P2.41

**Held on:** W1198 and W1202 (DEPLOYMENT.md), W1209 and W1212 (ResourceFabric.tsx, work_budget.py)

**Rows:**

- FU-1856 (P4.5, medium): The hardening brief lists the work budget as a live limit, and the deploy guide names neither the work budget nor self-serve sign-up, nor what the release machine and its image set
- FU-1857 (P2.41, low): With the work budget on, every reader of its energy figure reads the platform's total, and neither the figure, the switch's report, six pages nor the cockpit say whose figure it is

**Files:** agentic_core/molecular/work_budget.py; agentic_core/api/capital_fund.py; agentic_core/api/organism_status.py; apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx; apps/workstation-superapp/src/pages/enterprise/VSBEconomy.test.tsx; apps/workstation-superapp/src/pages/developers/NativeAI.tsx; apps/workstation-superapp/src/pages/cognitive/Introspection.tsx; apps/workstation-superapp/src/pages/cognitive/Introspection.test.tsx; apps/workstation-superapp/src/pages/organism/OrganismDashboard.tsx; apps/workstation-superapp/src/pages/organism/OrganismDashboard.test.tsx; apps/workstation-superapp/src/pages/Deliverables.tsx; apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx; docs/business/PRODUCTION_HARDENING_BRIEF.md; docs/DEPLOYMENT.md

**-k:** -k "whose_figure_it_is or test_w900_ or test_w901_ or test_w902_ or test_w742_ or test_w743_ or test_w839_ or test_w909_ or test_w494_ or test_w1047_ or test_w1112_ or test_w912_ or test_w1134_ or test_w1191_ or test_w756_ or test_w462_ or test_w469_" plus vitest VSBEconomy, OrganismDashboard, Introspection, HeartbeatMonitor, NativeAI, Deliverables, ResourceFabric, VSBCockpit

**Notes from the lead:**

Refuter fixes applied:
- No OWNER row: the Owner ruled on 2026-11-22 (S18.1), and both rows cite that ruling.
- energy_scope is computed: it is the platform's only until a second person runs work.
- Scope words go on all six pages test_w902 lists and on the cockpit's cycle figure (VSBCockpit.tsx:1502), held by a census leg over every page that prints energy_ratio.
- The off-state words are made true. The biometrics efficiency reads energy() whenever it is readable (app_mvp.py:741-753), so energy()'s off-basis 'nothing reads this figure' (work_budget.py:382) is corrected.
- Corrections 6 and 7 are written here, because W1192 does not write them. The guide's note names the image's ENV (Dockerfile:63-67), and leg 6 reads it.
- energy_acts joins test_w1112's set.
- Re-read A2's chip first. The brief names no row this round closes (test_w912).

### B3 as planned (cluster B; size M, 1 round(s))

**Title:** The work budget says its figure is the platform's and names every reader of it; the brief's limits and the guide's switches are held to the code

**Closes:** Two rows W1192 registers for it: the brief-and-guide row on P4.5 (gap 13; corrections 6 and 7 written by W1192) and the energy-scope row on P2.41 (v40 new gap 1).

**Owning item:** P4.5 and P2.41: one guard holds both, because the documents must name exactly the readers the code lists

**Owner-gated:** Which figure each reader should read is the Owner's: W1192 registers an OWNER row that recommends the platform figure. This round changes no behaviour: the 0.35 reserve raise, the fund caution, admission and the throttle work as built, and it only says whose figure it is and who reads it. The switch stays off and inert as S18.1 rules, and nothing in the tree sets WORKSTATION_WORK_BUDGET.

**Depends on:** W1191 landed: the guard reads startup.sh's --env settings. W1192 landed: the brief's limits line, the guide's table rows and note, and the rows. B6 edits the brief's part 7 next, so land B3 first. Cluster C's _w703_faults rounds (gaps 20 and 25) must accept the same brief text.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The brief labels the work budget as a live limit, [observed] | docs/business/PRODUCTION_HARDENING_BRIEF.md:53. W1192 rewrites it (correction 6). |
| EXISTS | The budget ships inert, and enabled() defaults to false | agentic_core/molecular/work_budget.py:27-35 and :61-63 |
| EXISTS | With the switch on, admission is capped at 1 once less than 0.3 of the window's capacity is left, before the gate holds when the capacity is spent | agentic_core/ai/native/homeostasis.py:46 (_ATP_CONSERVE_AT = 0.3) and :104-109; the gate holds at fraction >= 1.0 or an unreadable store (work_budget.py:397-407, :422-438) |
| EXISTS | energy() is the platform total, and its basis names no scope | work_budget.py:366-385 |
| EXISTS | The readers of energy(), energy_term or energy_acts | metabolism.py:341-364 and :680-692 (reserve 0.20 to 0.35 below 0.3); capital_fund.py:256-290 (posture straight from biobus.organism_context(), not from the board pack) and :563-575 (caution); organism_status.py:616-660 (POST /homeostasis files a Change Control request to cut RPM and runs rest cycles below 0.3); heartbeat.py:752-762 (metabolic_throttle below 0.2 when its lever is set) and :964-1003 (respond_to_energy does nothing while the budget is on); biobus.py:300-307 (the blended composite's term); app_mvp.py:738-745 (biometrics); api/economy.py (passes energy_acts to the board pack) |
| EXISTS | state() reports only the gate's consumers, and gates_anything is computed from them | work_budget.py:68-75 and :410-420; test_w742 leg 5 (test_mvp_spine.py:67500-67506) holds that computation |
| EXISTS | An entity's page shows the platform's figure as 'work budget left' | apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx:820; VSBEconomy.test.tsx:77-78 pins the line; the fixture's organism_posture has energy_acts false |
| EXISTS | The guide's settings omit SELF_SERVE_SIGNUP_ENABLED and WORKSTATION_WORK_BUDGET, and the budget is named in no deploy file or doc | DEPLOYMENT.md:26-34 is the only table, under '## Backend (Render)'. A grep finds WORKSTATION_WORK_BUDGET in none of deploy/, docs/*.md, docs/business, README.md, Dockerfile, render.yaml or scripts, and 0 times in FABLE. W1192 adds both rows (correction 7). |
| PARTIAL | The release machine passes sign-in and origin settings | At HEAD, startup.sh:85 passes only FORWARDED_ALLOW_IPS. After W1191 it passes AUTH_ENABLED from the metadata and CORS_ORIGINS (scratch copy). |
| EXISTS | The other limits' strengths | Sign-in counts are kept in one process's memory (auth/core.py:357-365). The gateway's bucket is per process and makes a call wait (gateway.py:181-210; GATEWAY_RPM is 20 unless set, config.py:47). EXTERNAL_MAX_CALLS_PER_HOUR is 60 unless set, and over it the external call is refused (orchestrator.py:629-645). AI_ALLOW_EXTERNAL is false unless set (ai/native/model_resource.py:23-25). |
| EXISTS | The plan names SELF_SERVE_SIGNUP, not the budget, as an Owner's switch | FABLE:909-913 (the OWNER-GATED list); S18.1 says only 'behind a setting' (FABLE:2760-2767) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- The hardening brief lists the work budget as a live limit, and the deploy guide names neither the work budget nor self-serve sign-up, nor where the release machine reads its settings (P4.5, medium)
- With the work budget on, every reader of its energy figure reads the platform's total, and neither the figure nor the switch's report says so: an entity's page shows it as 'work budget left' (P2.41, low)
- OWNER: once the work budget is switched on, should its readers (admission, each entity's reserve raise, the fund's caution) read the platform's figure, as built, or each entity's own? (OWNER, low)

**Rows it closes:**

- the brief-and-guide row on P4.5 (built: the text W1192 wrote, now held to the code)
- the energy-scope row on P2.41 (built)

**Changes:**

- agentic_core/molecular/work_budget.py: ENERGY_READERS: a typed tuple of (module, what it does with the figure, at what level), kept beside _CONSUMERS and not inside it, because gates_anything is computed from _CONSUMERS. It lists admission's conserve cap, the reserve raise, the fund caution, metabolic_throttle, the homeostasis route's request and rest cycles, self_recovery (it reads the figure and does nothing while the budget is on), the blended composite and the biometrics efficiency (display only), and the board pack (passes the figure to the page). energy()'s basis gains: the platform's total over every entity's runs this window, never one entity's own. state() carries energy_scope 'platform' and energy_readers.
- agentic_core/api/capital_fund.py: _energy_caution says 'the platform's work budget left N%', keeping the 'work budget left N%' substring test_w901 pins.
- agentic_core/api/organism_status.py: The homeostasis route's reason names the platform's work budget, keeping 'work budget left (N%)'.
- apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx: Line 820 reads 'platform work budget left N%'. While energy_acts is false it adds ' · read by nothing while the budget is switched off', in OrganismDashboard.tsx:450's words.
- apps/workstation-superapp/src/pages/enterprise/VSBEconomy.test.tsx: Lines 77-78 expect the new line, drawn from the captured fixture (energy_acts false).
- docs/business/PRODUCTION_HARDENING_BRIEF.md and docs/DEPLOYMENT.md: W1192 wrote both. They are changed here only where the guard finds them short of ENERGY_READERS or of the code's defaults.
- integration_tests/test_mvp_spine.py: test_wNNNN_the_work_budget_says_whose_figure_it_is_and_who_reads_it_and_every_doc_states_each_limit_and_switch_as_the_code_has_them appended.
- docs/FOLLOWUPS.json: Both rows closed as built.

**Guard:** test_wNNNN_the_work_budget_says_whose_figure_it_is_and_who_reads_it_and_every_doc_states_each_limit_and_switch_as_the_code_has_them

- Readers: an AST walk of agentic_core finds every module that calls work_budget.energy() or energy_term(), or reads the key 'energy_acts', and that set equals the modules ENERGY_READERS names (work_budget.py itself left out) FAILS IF: a reader exists that is not listed, or a listed module reads nothing
- The scope, driven: with the switch on (monkeypatched) and a record with 0.9 of the capacity spent and booked to owner A alone, entity B's economy cycle still raises its reserve from 0.20 to 0.35, and its metabolic_energy_basis names the platform's total FAILS IF: the basis does not say whose figure it is, or the cycle reads B's own figure before the Owner rules (then there is no raise)
- The report: state() carries energy_readers with each effect and energy_scope 'platform', and gates_anything is unchanged FAILS IF: the readers are merged into _CONSUMERS (gates_anything goes true with no gate reader), or the list is absent
- The fund: _energy_caution on that posture says 'the platform's work budget left 10%' FAILS IF: the caution reads as the entity's own figure
- The brief: part 7's budget sentence names WORKSTATION_WORK_BUDGET, says it is off unless set (work_budget.enabled() read with the variable deleted), names each ENERGY_READERS effect in plain words, and says it is one figure for the whole platform and that nothing is refused. The sign-in sentence says one process's memory, and core.py's comment still reads 'Kept in this process's memory'. The gateway sentence says per process and that a call waits. The external cap sentence says it limits nothing while AI_ALLOW_EXTERNAL is off (model_resource.external_allowed() read with the variable deleted). _w703_faults finds nothing FAILS IF: the old 'four places' sentence returns, a code default flips, or a reader is missing from the sentence
- The guide: the settings table lists AUTH_ENABLED, SELF_SERVE_SIGNUP_ENABLED, AI_ALLOW_EXTERNAL and WORKSTATION_WORK_BUDGET, each with the default the code gives with the variable deleted. The note under it names exactly the --env names deploy/gcp/startup.sh passes, and says REAL_MONEY_ENABLED is a constant in code (owner_payments.REAL_MONEY_ENABLED is False) FAILS IF: a row is missing, a default differs from the code's, or the script passes a setting the note does not name
- The page (vitest): VSBEconomy.test.tsx draws 'platform work budget left 100% · read by nothing while the budget is switched off · health not measured · blended 87%' from the captured board pack FAILS IF: the scope words or the off-state words are dropped

**Blinds:**

- Drop the scope phrase from energy()'s basis -> Leg 2: the cycle's basis no longer names the platform.
- In the scratch copy, flip enabled()'s default to 'true' and leave the docs alone -> Legs 5 and 6: the code's default no longer matches the brief or the table.
- Remove the reserve raise from ENERGY_READERS -> Leg 1: metabolism.py reads energy() and is not listed.
- Make the cycle read entity B's own figure -> Leg 2: with B at 0 s spent there is no raise to 0.35.
- Add a reader of energy_acts in a scratch module -> Leg 1: an unlisted reader.
- Add --env=WORKSTATION_WORK_BUDGET=false to startup.sh's no-domain run -> Leg 6: the script passes a setting the note does not name.
- Restore the brief's 'The app limits itself in four places' line -> Leg 5: no switch, no default, no reader effects.
- Drop the off-state words from VSBEconomy.tsx -> Leg 7 (vitest).

**Pins:**

- VSBEconomy.test.tsx (vitest) (apps/workstation-superapp/src/pages/enterprise/VSBEconomy.test.tsx:77-78): `work budget left ${Math.round(po.energy_ratio * 100)}% · health not measured · blended ${Math.round(po.composite_health * 100)}%` -> Change on purpose to the platform-scoped line with the off-state words.
- test_w901_fu1112_the_cycle_the_fund_and_the_self_report_read_the_derived_energy (test_mvp_spine.py:77245-77262): 'work budget left 10%' and 'simulated ATP 20%' in the caution; reserve 0.35; 'switched on' in metabolic_energy_basis -> Keep: the new words only prefix these substrings.
- test_w900_fu1112_with_the_work_budget_on_every_energy_threshold_reads_what_is_left_of_it (test_mvp_spine.py:77175-77213): 'switched off' and 'switched on' in energy()['basis']; 'work budget left (10%)' in the homeostasis reason -> Keep.
- test_w902_fu1112_every_page_shows_the_derived_energy_and_none_prints_the_atp_figure (test_mvp_spine.py:77279-77291): VSBEconomy.tsx reads organism_posture?.energy_ratio and holds no atp_ratio -> Keep.
- test_w742_the_metabolism_tells_the_truth (test_mvp_spine.py:67433, :67450, :67500-67506): gates_anything is computed from the loaded consumers -> Keep ENERGY_READERS apart from _CONSUMERS.
- test_w494_a_verdict_that_cannot_come_out_otherwise_is_not_an_assessment (test_mvp_spine.py:21736-21740): 'vsb-organism-posture', the measured-health and blended template fragments, ': 'health not measured'' -> Keep these fragments verbatim.
- test_w912_fu812_the_production_hardening_brief_scopes_each_part_by_its_evidence (test_mvp_spine.py:77704-77735): _w703_faults: labels, existing files and routes, named rows open -> Any adjusted wording keeps its label and names no closed row.

**Rulings it rests on:**

- S18.1 (FABLE:2760-2767): the throttle ships INERT behind a setting
- W743 / FABLE:6355-6358: an entity's figures are reported, not enforced; the gate reads the platform total
- FU-1166 (OWNER RULING 2026-11-19): no birth is refused on the derived capacity, because it divides an assumption
- P2.41's ACCEPT is P2.23's: each surface says, where it is read, what it does not do (FABLE:4663-4682, :4802)
- FABLE:909-913: the Owner-gated switches are AUTH_ENABLED, SELF_SERVE_SIGNUP, AI_ALLOW_EXTERNAL and REAL_MONEY_ENABLED; the budget is not among them
- Lead note on v40 gap 1: the Owner question is widened to every reader of energy()

**Risks:**

- The AST walk must count display-only readers (biobus.py, app_mvp.py, api/economy.py), or the first run fails. They are listed as display readers, not ignored.
- W1192's sentence and ENERGY_READERS must use the same plain words for each effect, or leg 5 fails on the first run. Align them in B3's apply.
- energy()'s basis grows longer. Pages that draw the basis as a title show the longer text, which is harmless: the dashboard's rendered test checks only the line's words.
- Cluster C's planned _w703_faults changes (named rows open; money written after its number) run over the same brief.

### B3's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- The list of energy readers (marked EXISTS) is incomplete as a list of readings. test_w902 (test_mvp_spine.py:77269-77291) names six pages that print the figure: NativeAI.tsx:887, Introspection.tsx:132, OrganismDashboard.tsx:445-450, Deliverables.tsx:326, ResourceFabric.tsx:671 and VSBEconomy.tsx:820. VSBCockpit.tsx:1502 also prints the cycle's figure as 'Metabolic energy' under an entity. The plan changes VSBEconomy alone.
- The off-state words copied from OrganismDashboard.tsx:450 ('read by nothing while the budget is switched off') are not true of the code. The biometrics efficiency reads energy()'s ratio whenever it is readable, on or off (app_mvp.py:745, :753), so energy()'s own off-basis 'so nothing reads this figure' (work_budget.py:382) is already false.
- 'W1192 writes corrections 6 and 7' is wrong: W1192's changed files (a scratch copy outside the tree) include neither the brief nor DEPLOYMENT.md.

**Pins the plan missed:**

- test_w1112 (test_mvp_spine.py:91410-91449) holds that the board pack still answers every organism_posture field the page reads. Once VSBEconomy reads energy_acts for its off-state words, that set ({energy_ratio, composite_health, composite_health_measured_only, composite_health_basis}) must gain energy_acts.
- OrganismDashboard.test.tsx:50-57 and :71 (/work budget left ·/ and 'read by nothing while the budget is switched off') change if the off-state wording is corrected or scope words reach the dashboard.
- If scope words reach the other pages: Introspection.test.tsx:46 and :53 (bar('Work budget left')), HeartbeatMonitor.test.tsx:44 ('work budget'), and test_w902's page list.

**Conflicts with a ruling:**

- OWNER RULING 2026-11-22 (Q3 with new gap 1), recorded by W1192 at S18.1 (a scratch copy outside the tree): 'once the throttle is switched on, admission and every other reader of the energy figure read the platform's total until a second person runs work, and then each run's own chain (platform, owner, VSB); every reading of the platform's total says it is the platform's figure'. The same decisions say 'no Owner QUESTION rows; build rows cite the ruling'. B3's third row re-asks the answered question as an OWNER row, recommending the platform figure until the capacity is measured, which is not what the Owner ruled. The owner_gated text ('which figure each reader should read is the Owner's') is also overtaken.
- energy_scope is hard-coded 'platform'. Under the ruling the scope is the platform's only until a second person runs work.
- Leg 2 books spend to owner A and asserts B's raise. It must be written as the one-person case. Otherwise, once a second person runs work, it pins the platform reading that the ruling replaces.

**Bar demands the plan missed:**

- Every reading must say it is the platform's figure: all six pages test_w902 lists, plus the cockpit's cycle figure, held by a census leg over every page that prints energy_ratio.
- Off-state words that are true: 'no threshold reads it while the budget is switched off', or ENERGY_READERS records which readers read the figure while it is off. Correct energy()'s off-basis to match.
- Correction 7's note must name the image's own ENV (Dockerfile:63-67: DATA_DIR, MPLCONFIGDIR, AI_ALLOW_EXTERNAL=false, ENVIRONMENT=production, PORT), not 'every other variable reads its default'. Leg 6 should read the Dockerfile ENV lines as well as startup.sh's --env.
- Corrections 6 and 7 must be written by B3 itself or by W1193, because W1192 does not write them.

**Fixes asked for:**

- Drop the OWNER row. Register the two disclosure rows in W1193, citing the S18.1 ruling.
- Compute energy_scope: the platform until a second person runs work.
- Extend the scope words to all six pages and the cockpit.
- Correct the off-state words and energy()'s off-basis.
- Name the Dockerfile ENV in the note and in leg 6.
- Add energy_acts to test_w1112's set.
- Write corrections 6 and 7 here.

**Re-sized:** M, 1.5 rounds (six pages and a census leg, corrections 6 and 7 written here)

## W1215 - B10: With the throttle on, admission and every reader of the energy figure read the platform's total until a second person runs work, then each run's own chain, as the Owner ruled

**Closes:** The S18.1 ruling of 2026-11-22 (gap 17 as the Owner decided it), and its row

**Owning item:** P3.30

**Held on:** W1214

**Rows:**

- FU-1865 (P3.30, medium): With the throttle on, admission and every reader of the energy figure keep reading the platform's total after a second person runs work, where the Owner ruled each run's own chain

**Files:** agentic_core/molecular/work_budget.py; agentic_core/ai/native/homeostasis.py; agentic_core/economy/metabolism.py; agentic_core/api/capital_fund.py

**-k:** -k "each_runs_own_chain or whose_figure_it_is or test_w742_ or test_w743_ or test_w839_ or test_w847_ or test_w900_ or test_w901_ or test_w462_ or test_w469_"

**Notes from the lead:**

The refuter's missing round, sketched here:
- It stays inert behind WORKSTATION_WORK_BUDGET; nothing in the tree sets it, and the test monkeypatches the switch.
- A second person is detected from the budget's own booking: a second owner with booked spend in the window.
- Each run then reads the least headroom on its chain (platform, owner, VSB), which W743 already computes (work_budget.entity_state).
- A run that names no owner reads the platform total and says 'not attributed'.
- Every reading says whose figure it is.

Blinds: reading the platform total after a second person; reading the chain before.

*B10 has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## W1216 - C5: Wherever a founder chooses or sees an entity's legal form, the platform says in one wording that no company is formed, nothing is registered and no liability is limited

**Closes:** Gap 11, correction 16 and its row

**Owning item:** P5.18 clause 1

**Held on:** W1205 and W1210 (vsb.py), W1214 (VSBEconomy.tsx, VSBCockpit.tsx)

**Rows:**

- FU-1868 (P5.18, medium): Where a founder chooses or sees an entity's legal form, nothing says that no company is formed

**Files:** agentic_core/economy/entities.py; agentic_core/api/agreements.py; agentic_core/api/economy.py; agentic_core/api/vsb.py; agentic_core/api/genesis.py; apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx; apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx; apps/workstation-superapp/src/pages/enterprise/VSBSpawnStudio.tsx; twelve fixtures (GenesisJourney, VSBEconomy, VSBEconomy.fee, VSBCockpit and its chat, chief, deliverables, fee, lifecycle, org and repo fixtures, VSBSpawnStudio); GenesisJourney.test.tsx, VSBEconomy.test.tsx, VSBCockpit.test.tsx, VSBSpawnStudio.test.tsx

**-k:** -k "no_company_is_formed or test_economy_entity_types or test_w488_ or test_w502_ or test_w924_ or test_w1039_ or test_w1047_ or test_w1049_ or test_w1080_ or test_w1081_ or test_w1082_ or test_w1111_ or test_w1112_ or test_w1014_ or test_w1125_ or test_w1139_ or test_w462_ or test_w469_" plus the four pages' vitest files

**Notes from the lead:**

Refuter fixes applied:
- Leg 2's grep is scoped to agentic_core and the pages, excluding fixtures and the register.
- The sentence is carried on the establishment stream's 'Living Economy Initialised' event (genesis.py:1877), on the establish answers, and on the waterfall and cycle answers.
- All twelve fixtures are recaptured by their capture scripts, and leg 4 extends to them.
- _read_view builds a new economy dict, because vsb.py's view is a shallow copy.
- test_w1014 is in the -k.
- The OWNER row becomes a chat question, with C5b HELD on it.

This may need a second number.

### C5 as planned (cluster C; size M, 1 round(s))

**Title:** Wherever a founder chooses or sees an entity's legal form, the platform says in one wording that no company is formed, nothing is registered and no liability is limited

**Closes:** Gap 11 (n=11), correction 16 and the W1192 row for the form sentence.

**Owning item:** P5.18 clause 1 ('an entity's template form is never shown as an incorporation', FABLE:7419-7421) and its ACCEPT ('no answer shows an entity as a legal person', 7448).

**Owner-gated:** Partly. The round adds the sentence and leaves the nine names and descriptions unchanged. Rewording the two approved descriptions is the Owner's, as an OWNER row W1192 registers. The round may reword the platform's own form_note and the VSBEconomy sentence, which the Owner never approved.

**Depends on:** W1192 (the rows). It does not wait on the Owner's answer. It comes before C6, because both change GenesisJourney.tsx, its test and its fixture.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | Two template descriptions read as legal facts | agentic_core/economy/entities.py:33 'Default commercial company, limited liability.' and :68 'Registered charitable purpose; maximal charitable allocation.' |
| EXISTS | These words are in the design the Owner approved | docs/VSB_ECONOMIC_LEGAL_MODEL.md:3 ('APPROVED BY THE OWNER (2026-06-20/21, re-approved 2026-06-29)'); its section 2 table has :40 'Company, limited liability' and :46 'Registered charitable purpose'. The vision (WORKSTATION_IDBO_WHOLE_VISION.md:601-603) records 'nine selectable legal forms' as approved. entities.py:14 calls only the waterfall approved, but the table carries the same words. |
| EXISTS | GET /api/v1/economy/entity-types serves them with a virtual-WST note only | agentic_core/api/economy.py:139-151. |
| EXISTS | The only no-incorporation sentence is agreements.NOT_AN_ENTITY | agentic_core/api/agreements.py:55-57, used at :257 and :479. |
| EXISTS | Five surfaces show a form with no such sentence | GenesisJourney.tsx:784-791 (first select, names only) and :1121-1130 (second select, with the description at :1128). VSBEconomy.tsx:363-386 (cards with descriptions; :370-371 'fixed at registration; change it by re-registering the entity'; form_note at :367 and :376). VSBCockpit.tsx:1390 ('Economic model — <entity_name>'). VSBSpawnStudio.tsx:536-539 (the Economy line). |
| EXISTS | form_note says 'registered as' | economy.py:545-546. test_w488 pins 'fixed at registration' at 19619. |
| EXISTS | The Cockpit and Spawn Studio read the form from the entity's stored economy block | vsb.py:3229-3235 stores {entity_type, entity_name, waterfall, capital_preserved, currency}, and GET /api/v1/vsb/{id} returns _read_view(vsb) (3183-3190). The sentence must be added at read time to reach older entities. |
| ABSENT | A guard over the entity-types answer or these pages for an incorporation claim | test_economy_entity_types (2680-2684) checks only that the answer is non-empty. test_w1080 (88597-88599) checks only agreements.py's source. |
| EXISTS | Captured fixtures hold these answers | GenesisJourney.fixture.json (entity_types), VSBEconomy.fixture.json (answers), VSBCockpit.fixture.json (answers), VSBSpawnStudio.fixture.json (detail). test_w1047 compares 'types' (86461) and test_w924 compares keys (78612). |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- Where a founder chooses or sees an entity's legal form, nothing says that no company is formed (P5.18, medium)
- OWNER DECISION: may the two approved template descriptions that read as legal facts be reworded? (OWNER, low)

**Rows it closes:**

- The first row, closed as built. The OWNER row stays open. Answered on the morning of 2026-11-22 (W1193c): FU-1868 stays open until W1231 has landed; W1216 does not close it.

**Changes:**

- agentic_core/economy/entities.py: NOT_A_LEGAL_PERSON, one wording: 'An entity here is a record on this platform, not a person in law: no company is formed, nothing is filed with any public register, and no liability is limited. Its form is a template for a profit split, in virtual WST.' Names and descriptions unchanged.
- agentic_core/api/agreements.py: NOT_AN_ENTITY = '{id} is an entity of this platform. ' + NOT_A_LEGAL_PERSON + ' It is never a party to an agreement with an outside party. Enter the party as the person or registered body it is.' The import names only the sentence, so the source still contains no 'ENTITY_TEMPLATES', 'entity_type' or 'economy.entity_form'.
- agentic_core/api/economy.py: The entity-types answer gains an answer-level 'not_a_legal_person'. form_note keeps 'fixed at registration', adds that this is a registration on this platform's roster and not in law, and says 'recorded as' instead of 'registered as'.
- agentic_core/api/vsb.py: _read_view adds economy.not_a_legal_person at read time. No record is rewritten.
- apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx: Keep the answer's sentence and draw it under both selects.
- apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx: Draw the sentence once under 'Legal / Economic Form'. Reword 'change it by re-registering the entity' to say the form is fixed when the entity was entered on this platform.
- apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx: Draw economy.not_a_legal_person under 'Economic model —'.
- apps/workstation-superapp/src/pages/enterprise/VSBSpawnStudio.tsx: Draw it under the Economy line.
- apps/workstation-superapp/src/pages/{synthesis/GenesisJourney,enterprise/VSBEconomy,enterprise/VSBCockpit,enterprise/VSBSpawnStudio}.fixture.json: The new field captured from the routes by their capture scripts.
- apps/workstation-superapp/src/pages/... four .test.tsx files: New cases V1-V4.
- docs/FABLE_DELIVERY_PROMPT.md and docs/FOLLOWUPS.json: A P5.18 UPDATED line for clause 1's sentence. Close the first row. Answered on the morning of 2026-11-22 (W1193c): leave FU-1868 open; W1231 closes it.
- integration_tests/test_mvp_spine.py: The new guard.

**Guard:** test_wXXXX_p518_wherever_a_form_is_chosen_or_shown_it_is_said_that_no_company_is_formed

- The entity-types answer carries not_a_legal_person == entities.NOT_A_LEGAL_PERSON. GET /api/v1/vsb/{id} carries it for an entity established on the floor, and also for an older record without the field, whose stored file stays byte-identical. FAILS IF: An answer drops it, or the read rewrites a record.
- agreements.NOT_AN_ENTITY contains NOT_A_LEGAL_PERSON, and a git grep of 'no company is formed' finds it only in entities.py and the tests. FAILS IF: A second wording is typed.
- With a claim ignored, form_note keeps 'fixed at registration', says it is this platform's roster and not a registration in law, and no longer says 'is registered as'. FAILS IF: The legal-registration reading returns.
- Each fixture's captured field equals the live route's, for Genesis, the Economy page, the Cockpit and the Spawn Studio. FAILS IF: A fixture is hand-typed or stale.
- No page's _code_only source contains the sentence's words. FAILS IF: A page draws its own copy instead of the answer's.
- Vitest: GenesisJourney.test.tsx draws the sentence under both selects; VSBEconomy.test.tsx draws it once and no longer says 're-registering the entity'; VSBCockpit.test.tsx draws it under 'Economic model —'; VSBSpawnStudio.test.tsx draws it under Economy. Each text is exactly the captured answer's. FAILS IF: A surface does not draw it.

**Blinds:**

- Drop the field from the entity-types answer. -> Leg 1 and the Genesis and Economy vitest go red.
- Drop the field from _read_view. -> Leg 1 and the Cockpit and Spawn Studio vitest go red.
- Type the sentence into VSBEconomy.tsx. -> Leg 5 goes red.
- Draw it only under GenesisJourney's second select. -> The Genesis vitest goes red.
- Type the old wording back into agreements.NOT_AN_ENTITY. -> Leg 2 goes red.
- Restore 'this entity is registered as' in form_note. -> Leg 3 goes red.

**Pins:**

- test_w488_the_page_and_the_api_say_the_same_thing (19619): assert "fixed at registration" in wf["form_note"], wf["form_note"] -> Kept. The words remain, with the roster clarified.
- test_w488_the_page_and_the_api_say_the_same_thing (19762): 'data-testid="form-claim-ignored"' in econ and 'data-testid="form-in-force"' in econ -> Kept.
- test_w1047_fu399_the_vsb_economy_page_says_what_happened_when_a_read_fails (86461): client.get("/api/v1/economy/entity-types").json()["types"] == fx["answers"]["/api/v1/economy/entity-types"]["body"]["types"] -> Kept. The field is answer-level, so 'types' is unchanged; the fixture body gains the field.
- test_w924_fu399_a_genesis_journeys_stage_rail_and_rank_stage_are_guarded_by_a_render (78612): assert set(fx["entity_types"]) <= set(client.get("/api/v1/economy/entity-types").json()) -> Kept. The fixture gains a key the live answer has.
- test_w1080_p518_a_party_is_a_person_or_a_registered_body_and_an_agreements_six_facts_stay_apart (88460, 88474, 88597-88599): detail == _ag.NOT_AN_ENTITY.format(id=...); "is an entity of this platform"; "ENTITY_TEMPLATES" not in src and "entity_type" not in src and "economy.entity_form" not in src -> Kept. The opening words remain and the import names only the sentence.
- test_w1082_p519_an_asset_is_a_record_held_under_an_agreement_and_its_six_facts_are_never_merged (88768): "is an entity of this platform" -> Kept.
- VSBSpawnStudio.test.tsx (66): expect(screen.getByText(captured.detail.body.economy.entity_name)).toBeTruthy(); -> Kept. The sentence is drawn in a separate element.
- VSBEconomy.test.tsx (86): expect(await screen.findByTestId('form-in-force')).toBeTruthy(); -> Kept.

**Rulings it rests on:**

- P5.18 clause 1, ACCEPT and MEASURED FIRST (FABLE:7416-7421, 7448).
- The Owner's approval of the VSB model (2026-06-20/21, re-approved 2026-06-29): names and descriptions are kept, and rewording them is the OWNER row.
- P5.18 BOUNDARY and P5.6 BOUNDARY: no legal form is decided for anyone.
- W313 and W488: the form is fixed at registration on the roster, and the page and the API say the same thing.
- Never delete or rewrite an entity: the sentence is added at read time.

**Risks:**

- Four fixtures must be recaptured from the routes, not hand-edited.
- test_w1080 forbids 'entity_type' anywhere in agreements.py's source, so choose the import name with care.
- An Owner rewording would follow as its own round.

### C5's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'Five surfaces show a form with no such sentence' is PARTIAL. The establishment stream also shows the form: genesis.py:1876-1878 yields 'Living Economy Initialised' with '{entity_name} — virtual WST only (real rails gated).', and GenesisJourney.tsx:421 draws it in the birth stages. The waterfall answer (economy.py:456) and the cycle answer (economy.py:2273) also carry entity_name.
- 'Captured fixtures hold these answers' names four. Twelve fixtures capture the form: VSBEconomy.fee.fixture.json (the entity-types answer at :151 and :1456), VSBCockpit.chat, chief, deliverables, fee, lifecycle, org and repo fixtures, and the four named.

**Guard legs that could not fail:**

- Leg 2 ('a git grep of no company is formed finds it only in entities.py and the tests') goes red on a correct tree. The recaptured *.fixture.json files hold the sentence, and docs/FOLLOWUPS.json holds the row title '...nothing says that no company is formed'. Scope it to agentic_core/ and apps/.../src, excluding fixtures.

**Pins the plan missed:**

- test_w1014_a_rendered_test_waits_for_what_an_element_says_and_never_reads_it_as_found (84614) scans every *.test.tsx for '(await screen.findBy...(...)).textContent'. Cases V1-V4 must use waitFor. It is not in the -k.
- test_w488 also pins VSBEconomy.tsx 'const inForce = wf?.entity_type ?? null', 'wf?.claim_ignored' and '(inForce || entity) === t.id' (19764-19766). Keep them while rewording 370-371.
- test_w1125's and test_w1139's fee tests read VSBEconomy.fee.fixture.json and VSBCockpit.fee.fixture.json (92026, 93197). Add them to the -k if those fixtures are recaptured.

**Conflicts with a ruling:**

- the round design's cluster C file (a session work file, not in the tree) owner_decisions_2026_11_22: 'the Owner accepted ALL the lead's recommendations ... So: no Owner QUESTION rows; build rows cite the ruling.' C5 registers a new OWNER question row on the rewording. Before W1193 the lead should put it to the Owner as a recommendation to be ruled, or decide it is not the Owner's. The descriptions live in entities.py, and the approved table at VSB_ECONOMIC_LEGAL_MODEL.md:40 and :46 would stay as it is.
- Numbering: W1193.

**Bar demands the plan missed:**

- P5.18 ACCEPT 'no answer shows an entity as a legal person' (FABLE:7448). Carry the sentence on the establish answers: the stream's economy event and the blocking establish's economy block at genesis.py:1651. Also carry it on the waterfall and cycle answers, as the rulings refuter's sketch (2) asked. The plan leaves those out without saying why.
- Leg 4 checks four fixtures. The other eight, which hold GET /api/v1/vsb/{id} or the entity-types answer, would be left stale, against the 'captured is the route's own' rule (W1047).

**Fixes asked for:**

- Scope leg 2 to code. Add the stream event, the establish answers and the waterfall and cycle answers. Recapture all twelve fixtures through their capture scripts and extend leg 4. Add test_w1014 to the -k.
- In _read_view, build a new economy dict ({**vsb['economy'], ...}). v = dict(vsb) is a shallow copy (vsb.py:2572+), so this keeps the 'byte-identical record' leg honest.
- Resolve the OWNER row with the lead. Re-render the living plan on close.

**Re-sized:** M to L: 1-2 rounds (12 fixtures, 5 page surfaces, the stream event and 4 answers).

## W1217 - C6: One journey establishes one entity: a repeat from the same journey, including the page's own fallback after a cut stream, is answered with the first entity and creates nothing

**Closes:** Gap 19 and its row

**Owning item:** P5.1

**Held on:** W1216 (genesis.py, GenesisJourney.*)

**Rows:**

- FU-1869 (P5.1, medium): Establishing twice from one journey record makes a second entity, and the page's own fallback does it after a cut stream

**Files:** agentic_core/api/genesis.py; apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx; apps/workstation-superapp/src/pages/synthesis/GenesisJourney.test.tsx; apps/workstation-superapp/src/pages/synthesis/GenesisJourney.fixture.json

**-k:** -k "one_journey_establishes_one_entity or test_w668_ or test_w485_ or test_w452_ or test_w643_ or test_w753_ or test_w924_ or test_w1075_ or test_w1111_ or test_w1158_ or test_w1012_ or test_w1062_ or test_w1025_ or test_w1014_ or test_w462_ or test_w469_" plus vitest GenesisJourney.test.tsx

**Notes from the lead:**

Refuter fixes applied:
- Keep the pinned setError lines (test_w1012 :84370, test_w1062 :87256) and the count of 4 for 'await refusalOf(res)' (test_w1025 :85312). Test the already_established flag on a parsed body held in its own variable, or change those three pins on purpose.
- Add a stale-claim rule, with a leg: an 'establishing' claim whose entity is not saved within a stated bound is released.
- slot_source on the P5.1 row.
- The file list includes the plan documents.

### C6 as planned (cluster C; size M, 1 round(s))

**Title:** One journey establishes one entity: a repeat from the same journey, including the page's own fallback after a cut stream, is answered with the first entity and creates nothing

**Closes:** Gap 19 (n=19) and the W1192 row for it.

**Owning item:** P5.1 (one tenant's journey, driven and read back from its stores).

**Owner-gated:** No. Nothing is deleted. Duplicates already on the Owner's machine are left as they are. The refusal is on the journey, not on capacity.

**Depends on:** W1192. It comes after C5, because both change GenesisJourney.tsx, its test and its fixture.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | Both doors mint a fresh id on every establish, and nothing marks the journey used | genesis.py:1518 (blocking) and :1799 (inside the stream generator). _record_journey (1267-1282) writes no owner and no establishment. 'Idempotent' at :1298 covers one request only. |
| EXISTS | The one-call path establishes with its journey id | genesis.py:871-893 calls genesis_establish(..., journey_id=journey_id). |
| EXISTS | The page re-posts the same body to the blocking door when the stream ends without its complete frame | GenesisJourney.tsx:401-444. The complete frame is the stream's last (genesis.py:1997), after the save (:1908) and the first cycle and ship. A double click is blocked (:1135-1136). |
| EXISTS | The journey record is read for anyone who names its id | _read_journey (1285-1292) checks only the id's shape. With sign-in on, another person's journey record would be read as theirs. |
| EXISTS | A guard pins today's double establish | test_w668 at 52866-52877 establishes twice from one journey_id and asserts 200 both times. |
| ABSENT | The capture of an establishment answer for the page | GenesisJourney.fixture.json holds only request, journey, entity_types and price, and GenesisJourney.test.tsx has no establish case. |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- Establishing twice from one journey record makes a second entity, and the page's own fallback does it after a cut stream (P5.1, medium)

**Rows it closes:**

- The row above, closed as built.

**Changes:**

- agentic_core/api/genesis.py: _record_journey stamps the caller's owner. _read_journey answers another person's journey as none (W1075's rule). One helper, _claim_journey, is used by /establish, /establish/stream (claimed at request time, outside the generator, so a repeat gets a real 409 status) and the one-call path. Under store_lock on the journey file, before an id is minted, it refuses a journey that already names an entity (409, detail {message, vsb_id, journey_id, already_established: true}, message first). Otherwise it records the minted id as 'establishing'. After registration it records 'established_vsb'. A failure before registration releases the claim in a finally. A repeat that finds 'establishing' answers 409 naming the id, saying whether the entity is saved yet. An establish with no journey id is unchanged.
- apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx: When the fallback, or the stream's own answer, is a 409 whose detail is already_established, show 'This journey already established <vsb_id>; nothing new was made' with Open it (/vsb-cockpit?vsb=<id>), not 'Establishment failed'. Every other 409 is said as before.
- apps/workstation-superapp/src/pages/synthesis/GenesisJourney.fixture.json and GenesisJourney.test.tsx: Capture the route's 409 answer for a repeated journey, and add two cases.
- integration_tests/test_mvp_spine.py: The new guard. test_w668 leg 2 re-seated on a second journey.
- docs/FOLLOWUPS.json: Close the row.

**Guard:** test_wXXXX_p51_one_journey_establishes_one_entity_and_a_repeat_is_answered_with_it

- A journey (establish false), then establish with its journey_id, gives 200 and entity A. The same body again gives 409 with detail.vsb_id == A and already_established, and exactly one stored entity names that journey in its evidence_source. FAILS IF: The mark is not kept, so two entities exist.
- Establish twice with no journey id gives 200 twice and two entities. FAILS IF: The round refuses establishes that name no journey.
- A second journey's establish gives 200 and entity B, which is not A. FAILS IF: The claim is keyed wrongly.
- POST /establish/stream consumed whole gives entity C. Then POST /establish with the same body gives 409 naming C, and one entity exists. FAILS IF: The stream door skips the claim.
- A step after registration is monkeypatched to raise inside the stream, so no complete frame is sent. The fallback POST then gives 409 naming the registered entity, and no second entity exists. FAILS IF: The mark is written only at the stream's end.
- An establishment that raises before registration (a monkeypatched _derive_name) is followed by a retry that gives 200. FAILS IF: A failed claim locks the journey for good.
- POST /journey with establish true leaves established_vsb on the journey record, and a later /establish with that id gives 409. FAILS IF: The one-call path bypasses the helper.
- With sign-in on in the test process, person B naming A's journey id is answered as a journey with no record: evidence source 'caller' or 'none', and nothing of A's entity id in the answer. FAILS IF: The 409 hands A's entity id to another person.
- Two threads calling _claim_journey on one journey at once: exactly one wins. FAILS IF: The check and the set are not under one lock.
- Vitest: the stream ends without complete and /establish answers the captured 409, so the page shows the already-established notice with the id and Open it, and no 'Establishment failed'. A 409 for an unresolved parent still shows 'Establishment failed (HTTP 409): ...'. FAILS IF: The page shows a failure for the repeat, or swallows other refusals.

**Blinds:**

- Never write established_vsb. -> Legs 1, 4 and 7 go red.
- Refuse an establish that names no journey. -> Leg 2 goes red.
- Answer every journey with the last established entity. -> Leg 3 goes red.
- Claim only in /establish. -> Leg 4 goes red.
- Write the mark after the complete frame. -> Leg 5 goes red.
- Drop the release in finally. -> Leg 6 goes red.
- Name the entity whoever asks. -> Leg 8 goes red.
- The page shows 'Establishment failed' for every 409. -> The vitest case goes red.

**Pins:**

- test_w668_establish_reads_the_journeys_own_record_and_a_status_is_derived_when_read (52866-52877): _e2 = client.post("/api/v1/genesis/establish", json={**_body, "name": "W668 Rota Two", "selected_candidate": _fake, "journey_id": _jr["journey_id"]}) ... assert _e2.status_code == 200 -> Change on purpose. Run a second POST /api/v1/genesis/journey and establish once on its id with the fabricated candidate, so the record still wins. The comment says a journey now establishes once and a repeat is 409 naming the first entity.
- test_w924_fu399_a_genesis_journeys_stage_rail_and_rank_stage_are_guarded_by_a_render (78598-78613): set(cap) <= set(j) ... set(fx["entity_types"]) <= set(...) -> Kept. The 409 capture is a new fixture key.
- test_w1075_fu1262_with_sign_in_on_no_route_reads_or_writes_another_persons_entity_by_its_id (87968-87970): client.post("/api/v1/genesis/establish", headers=H["one"], json={"problem": ..., "ship_output": False, ...}) -> Unchanged: no journey id is given.

**Rulings it rests on:**

- P5.1 ACCEPT (FABLE:6805-6808).
- OWNER RULING 2026-11-19 (FABLE:281-282): no birth is refused on the carrying capacity. Untouched, since this refusal is on the journey.
- S18.6: capacity is derived from the budget, and a duplicate inflates it, which this round stops.
- W1075: another person's id is answered as one that does not exist.
- W452 F1: a refusal is a real status before the stream starts. W597: a dict detail carries its message first.
- Never delete an entity: duplicates already made are left.

**Risks:**

- Whether a client disconnect cancels the stream generator decides when the finally runs. Leg 5 drives the cut by a raise, not a real disconnect.
- Journeys recorded before the round have no owner. They are read as the single-user owner's, as W753 reads old records.
- A second journey in test_w668 lengthens a slow test.

### C6's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- None found. Verified genesis.py:1518 and :1799 mints, _record_journey 1267-1282 (no owner, no mark), _read_journey 1285-1292 (shape only), 'Idempotent' at 1298, the one-call path 871-893, the save at 1908 and complete at 1997, the page fallback at GenesisJourney.tsx:401-444, the disabled button at 1135-1136, test_w668 52866-52877, and fixture keys request, journey, entity_types and price.

**Guard legs that could not fail:**

- None.

**Pins the plan missed:**

- test_w1012_a_refusal_read_by_hand_is_never_said_as_object_object (84336) asserts, at 84369-84370, that GenesisJourney.tsx contains "const detail = bodyDetail(await bodyOrNull(res), '');" and "setError(`Establishment failed (HTTP ${res.status})${detail ? `: ${asClause(detail)}` : ''}.`);". Reading the 409 body for already_established before bodyDetail changes the first line.
- test_w1062_fu1248_a_refusal_s_reason_is_said_whole_never_cut_at_a_fixed_length (87203), at 87255-87256, pins the same setError line.
- test_w1025_a_refusal_is_said_by_its_reason_never_by_its_status_alone (85258), at 85312, asserts gj.count('await refusalOf(res)') == 4. Handling the stream's own 409 at GenesisJourney.tsx:406 changes the count.

**Conflicts with a ruling:**

- None against rulings: no birth is refused on capacity, nothing is deleted, and W1075/W452/W597 are respected. Numbering: W1193.

**Bar demands the plan missed:**

- A claim taken outside the generator but released inside it is orphaned when the stream generator never starts, for example when the client leaves before streaming. Every later establish on that journey would then answer 409 'not saved yet' for good. It needs a recovery rule, such as releasing an 'establishing' claim whose minted entity is not saved after a stated bound, and a leg for it.
- The change list omits docs/FABLE_DELIVERY_PROMPT.md and docs/WORKSTATION_IDBO_LIVING_PLAN.md, which the row close re-renders.

**Fixes asked for:**

- List the three pins as changed on purpose, or keep the pinned lines by testing the flag on a parsed body held in its own variable. Add test_w1012, test_w1062, test_w1025 and test_w1014 to the -k.
- Add the stale-claim rule and a leg: a claim taken, the generator never iterated, then a retry succeeds once the bound has passed.
- Carry slot_source on the P5.1 row.

**Re-sized:** M, 1-2 rounds.

## W1218 - B5a: With sign-in on, a founder instructs their own entity's Chief through an entity-scoped route grounded in the entity's own record; the apex Board stays the administrator's

**Closes:** Its row (the Chief half of gap 4)

**Owning item:** P4.2 (the Owner's ruling of 2026-11-22)

**Held on:** W1210 (board.py), W1216 (VSBCockpit.tsx, vsb.py)

**Rows:**

- FU-1859 (P4.2, medium): With sign-in on, a founder who is not an administrator is refused their own entity's Chief

**Files:** agentic_core/api/board.py; agentic_core/api/vsb.py; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.chief.test.tsx; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.chief.fixture.json; README.md

**-k:** -k "instructs_their_own_entitys_chief or test_w1055_ or test_w1075_ or test_w499_ or test_w602_ or test_p330_r7_ or test_w505_p26_ or test_pervsb_apex_governance_scoped or test_w661_ or test_w812_ or test_w683_ or test_tier_identity_and_founder_modelled_chief or test_w613_ or test_w633_ or test_w651_ or test_w653_ or test_w820_ or test_w926_ or test_w462_ or test_w469_" plus vitest VSBCockpit.chief.test.tsx

**Notes from the lead:**

As designed, citing the P4.2 ruling instead of 'not put to the Owner'. readme_figures --fix runs last.

*B5a is part of B5's design, split by the lead; the design below is B5's whole.*

### B5 as planned (cluster B; size M, 1.5 round(s))

**Title:** With sign-in on, a founder instructs their own entity's Chief through an entity-scoped route, grounded in the entity's own record; the apex Board stays the administrator's

**Closes:** The founder's-Chief row W1192 registers on P4.2

**Owning item:** P4.2 (a pre-flight of the invited stage)

**Owner-gated:** Not an Owner's question: the vision already rules it (§13 and §18 spine 3), and the round builds no more than that. Scope 'workstation', the apex Board, ratifications (FU-012) and material economy decisions (FU-014) stay administrator-only. The invited stage itself stays the Owner's, after FU-1817.

**Depends on:** W1192 (its row). Nothing else in this cluster. Re-run scripts/readme_figures.py --fix after the route is added: other clusters' routes move the same README figures.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The board router is mounted behind require_admin | agentic_core/app_mvp.py:518-519 |
| EXISTS | require_admin answers 403 'Admin access required.' to role 'user', the role every invited account gets | auth/core.py:288-289; register default 'user' (:341-342, :474-475); signup always 'user' (:537) |
| EXISTS | The Cockpit's Chief tab posts the board route with owner and scope in the body | apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx:565-583 |
| EXISTS | chief_instruct frames every scope as the Workstation IDBO's own | board.py:856-863: 'the standing charter of {req.owner}, the Owner/Founder of the Workstation IDBO' and 'The Owner's vision: {_OWNER['vision_summary']}' |
| EXISTS | The record's owner is stamped from the signed-in person after the run | board.py:983-992 (request_owner_id, W505 FU-029) |
| PARTIAL | The Chief's live intelligence is scoped for plan and prior directives, but not for operations | board.py:347-389: the plan and prior directives are scoped (W661), but 'Recent operations' reads _ops_load()[-50:] across the whole platform |
| EXISTS | Each entity's board record carries its own owner and purpose | genesis.py:1641-1642 (board_for_owner(owner, 'Commercialise: <problem>', domain)); board.py:426-462 |
| ABSENT | An entity-scoped Chief route | No /{vsb_id}/chief route in vsb.py's route list (vsb.py:679-4372) |
| EXISTS | _require_vsb_access, and the VSB router behind get_current_user | vsb.py:411-425 (404, never 403, when scoped out); app_mvp.py:401-402 |
| EXISTS | The canon gives every entity its own Chief | docs/WORKSTATION_IDBO_WHOLE_VISION.md:620 ('governed by its own Chief/Board, under the founder's intent') and :1109-1110 (spine 3); W300's scoped board (test_mvp_spine.py:1415) |
| EXISTS | No founder page reads an entity's work-budget figure, and no route serves it | entity_states(5) is read only by the admin organism status (organism_status.py:366-372); no page fetches it |
| EXISTS | The Chief's prompt text is not pinned by any test, and the _q seam is spied | No 'Owner/Founder of' or 'The Owner's vision' in test_mvp_spine.py; test_w661 patches board._q with signature (prompt, agent, provenance, *a, **k) (:52168-52176) |
| EXISTS | The README's operation figures are pinned | README.md:117 ('659 API operations ... 621 distinct paths'); test_w499 (test_mvp_spine.py:22864-22885) |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- With sign-in on, a founder who is not an administrator is refused their own entity's Chief (P4.2, medium)

**Rows it closes:**

- the founder's-Chief row (built)

**Changes:**

- agentic_core/api/board.py: chief_instruct's body moves to a core function that both routes call, with framing chosen by scope. 'workstation' keeps the platform's framing. A scope naming an entity record uses the entity's: its name, its owner, and its board's vision_summary or its challenge. Any other scope uses a neutral framing that names no vision. The platform's vision_summary is never used outside 'workstation'. _live_intelligence counts only the entity's own operations rows for an entity scope. The apex route's request model, its record fields (owner, owner_source, owner_as_requested) and its _q seam are unchanged.
- agentic_core/api/vsb.py: POST /{vsb_id}/chief/instruct with a STRICT model {instruction: str, cascade_to_ceo: bool = True}, so an owner or scope field is refused with 422. vsb = _require_vsb_access(vsb_id, user), then the core runs with scope=vsb_id. The record's owner is the entity's owner_id and instructed_by is the signed-in person (the single-user owner while sign-in is off).
- apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx: instructChief posts `/api/v1/vsb/${selected}/chief/instruct` with {instruction, cascade_to_ceo: true}. W1055's issuedFor logic and its error sentence are unchanged.
- apps/workstation-superapp/src/pages/enterprise/VSBCockpit.chief.test.tsx and VSBCockpit.chief.fixture.json: The new URL. ask, instructed and instruct_refused are recaptured from the new route on a fresh store.
- README.md: Line 117's figures move by one operation and one path, via scripts/readme_figures.py --fix.
- integration_tests/test_mvp_spine.py: The new test. test_w1055 now posts the new route with the fixture's ask (no scope), and its 'ask["scope"] == fx["vsb_id"]' check becomes a check that the ask carries no owner or scope.

**Guard:** test_wNNNN_with_sign_in_on_a_founder_instructs_their_own_entitys_chief_and_no_one_elses

- The founder is answered: with sign-in on, person one (role 'user') establishes entity E; POST /api/v1/vsb/E/chief/instruct answers 200, its objectives land on E's plan (read back from the store), and the record's owner is E's owner_id FAILS IF: the route is admin-gated (403) or missing, or the objectives land elsewhere
- Grounded in the entity: the Chief prompt captured at board._q names E and its board's purpose, and contains neither _OWNER['vision_summary'] nor 'the Owner/Founder of the Workstation IDBO' FAILS IF: a founder's directive is still framed as the platform's
- Live intelligence: with operations rows planted for E and for another entity, the prompt's 'Recent operations' counts E's rows only FAILS IF: the platform's last fifty rows are read into a founder's prompt
- Owner stamped, not claimed: a body naming owner or scope answers 422, and the directive count is unchanged FAILS IF: the model accepts an owner from the client
- Nobody else's: person two is answered exactly as for an id that names no entity (404 'VSB ... not found.'), and E's objective count and the directive count are unchanged FAILS IF: the entity check is dropped
- The apex stays the administrator's: person one gets 403 on POST /api/v1/board/chief/instruct (scope E and 'workstation') and on GET /api/v1/board/ratifications, and 404 on POST /api/v1/vsb/workstation/chief/instruct FAILS IF: the board router loses require_admin, or 'workstation' is reachable through the entity route
- Sign-in off is unchanged: the single user's call on the new route lands objectives as the apex route's does FAILS IF: the new route requires a person
- The page: VSBCockpit.tsx posts the new route with no owner or scope, and the rendered test passes against the recaptured fixture FAILS IF: the cockpit still posts the admin route

**Blinds:**

- Mount the new route on the board router, or depend on require_admin -> Leg 1: person one gets 403.
- Replace _require_vsb_access with _load_vsb in the new route -> Leg 5: person two lands objectives. W1075's census also goes red, since the new POST is driven automatically.
- Keep _OWNER['vision_summary'] in the entity framing -> Leg 2.
- Make the model non-STRICT and stamp the body's owner -> Leg 4.
- Read the platform's last fifty operations for an entity scope -> Leg 3: the count includes the other entity's rows.
- Point the cockpit back at '/api/v1/board/chief/instruct' -> Leg 8: the vitest and test_w1055's posting leg fail.

**Pins:**

- test_w1055_fu399_the_cockpit_s_chief_tab_keeps_the_chief_s_answer_with_the_entity_it_was_issued_for (test_mvp_spine.py:86818-86823): ask['scope'] == fx['vsb_id'] and client.post('/api/v1/board/chief/instruct', json={k: v for k, v in ask.items() if k != 'instruction'}) -> Post the new route; assert the ask carries no owner or scope; the refused answer is recaptured. The page-code checks at :86834-86845 stay.
- VSBCockpit.chief.test.tsx (vitest) (:45 and :93): url !== '/api/v1/board/chief/instruct' and expect(post).toHaveBeenCalledWith('/api/v1/board/chief/instruct', captured.ask) -> Change to the entity URL built from VID.
- test_w499_the_plan_projects_only_the_work_a_round_closes (test_mvp_spine.py:22864-22885 with README.md:117): '659 API operations (method+path; 621 distinct paths' -> Run scripts/readme_figures.py --fix: one more operation and one more path.
- test_p330_r7_the_vision_says_what_is_built (test_mvp_spine.py:56205-56212): only BoardOfDirectors.tsx and VSBCockpit.tsx contain 'chief/instruct' -> Still true, because the new URL is called only from VSBCockpit.tsx. Fixtures are .json and are not scanned.
- test_w661_a_chief_is_prompted_with_its_own_record_files_an_instruction_once_and_a_decision_names_who (test_mvp_spine.py:52145-52200): the board._q seam; the scoped founder_profile; no founder_profile call without a scope -> Keep _q as the module-level seam, and pass the scope on every founder_profile call.
- test_w812_plans_chief_instructions_transformations_and_the_apex_board_take_the_configured_owner (test_mvp_spine.py:71733-71745): the apex record's owner, owner_as_requested and owner_source -> Unchanged: the apex route's record fields stay as they are.

**Rulings it rests on:**

- Vision §13 and §18 spine 3: every generated entity carries its own Board and a Chief of its owner (WHOLE_VISION.md:620, :1109-1110)
- W300: the board's read is scope-aware so apex governance reaches the user's own entity
- P2.6 (W505, FU-029): the apex Board is the administrator's; the Board's ratification queue (FU-012) and the economy tier map (FU-014) stay apex
- FU-525 (W627): a founder's text is not drafted from Workstation's own vision; this round closes the same class at the Chief
- OWNER RULINGS 2026-10-12, 2026-11-19 and 2026-11-20 (evening) on the invited stage (FABLE:6717-6724, :6748-6754)

**Risks:**

- About thirty-five tests call the apex route with arbitrary scope strings that name no entity (test_w651, test_w653, test_w661 and others). The core must take a scope with no entity record without failing and without the platform's vision.
- Recapturing the cockpit fixture needs a capture script like W1055's, which is not in the tree; write it in the round's scratch.
- Other clusters' routes move the README figures too. Run readme_figures --fix last.
- W1075's census picks up the new POST automatically: its post count rises by one, still at least 45.

### B5's refutation: **NEEDS_FIXES**

**Pins the plan missed:**

- If the Board and budget-figure routes are added, README.md:117's figures move by three operations and paths, not one (test_w499, test_mvp_spine.py:22864-22885; run readme_figures --fix last), and W1075's census picks up the new GETs.

**Conflicts with a ruling:**

- OWNER RULING 2026-11-22 at P4.2 (Q4 (a)), recorded by W1192 (a scratch copy outside the tree): 'a founder who is not an administrator may instruct their own entity's Chief, read their entity's Board and see their entity's own work-budget figure, for the entities they own only ... it is built and driven in a test process before the invited stage'. B5 builds only the Chief. not_proposed refuses 'an owner-scoped read of an entity's work-budget figure'. 'No Owner question is put' should instead cite this ruling.

**Bar demands the plan missed:**

- An entity-scoped Board read. board_status(scope=<vsb_id>) (board.py:472-505) serves the entity's own board only behind require_admin. Add GET /api/v1/vsb/{vsb_id}/board behind _require_vsb_access, driven for the owner, for a second person (answered as for no entity) and for the apex refusal.
- An entity-scoped work-budget figure. work_budget.entity_state (work_budget.py:289) has no route. Add one carrying _ENTITY_GATE_NOTE ('reported, not enforced'), and show it on the founder's page, since the ruling says 'see'.
- Coordinate with cluster A's gap-15 round, which edits board.py's time differences.

**Fixes asked for:**

- Widen B5, or split it into B5a (the Chief, as designed) and B5b (the entity's Board and its own budget figure, each with a second-person leg and a page).
- Cite the P4.2 ruling.
- Recompute the README figures once all new routes are in.

**Re-sized:** L, 2 rounds (the Chief; then the Board and the entity's own budget figure with a page)

## W1219 - B5b: With sign-in on, a founder reads their own entity's Board and sees their entity's own work-budget figure, and no one else's

**Closes:** Its row (the Board and budget-figure half of gap 4)

**Owning item:** P4.2 (the Owner's ruling of 2026-11-22)

**Held on:** W1218

**Rows:**

- FU-1860 (P4.2, medium): With sign-in on, a founder who is not an administrator cannot read their entity's Board, and no route serves an entity's own work-budget figure

**Files:** agentic_core/api/vsb.py; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx (or the founder's entity page the round names), its test and fixture; README.md

**-k:** -k "reads_their_own_entitys_board or instructs_their_own_entitys_chief or test_w1075_ or test_w1077_ or test_w499_ or test_w743_ or test_pervsb_apex_governance_scoped or test_w505_p26_ or test_w462_ or test_w469_"

**Notes from the lead:**

This is the refuter's widening: the ruling grants three things, and B5 built one.
- GET /api/v1/vsb/{vsb_id}/board sits behind _require_vsb_access and serves board_status(scope=vsb_id) (board.py:472-505).
- A route serves the entity's own figure (work_budget.entity_state, :289) with _ENTITY_GATE_NOTE ('reported, not enforced'), drawn on the founder's page.
- Each is driven for the owner, for a second person (answered as for no entity) and for the apex refusal.
- README figures move by the routes added.

*B5b's design and refutation are printed under W1218, the first round that carries B5.*

## W1220 - C8: The read census, part 1: every mounted GET and every declared preview is called on a fresh data root, as nobody and as a reader; the five reads that advance the simulator and the registry read are fixed

**Closes:** Gap 10 and the v40 board-pack evidence (part 1)

**Owning item:** P5.10 clause 1

**Held on:** W1197 (the preview), W1214 and W1215 (capital_fund.py, organism_status.py), W1216 (economy.py), W1219 (its new GETs walked)

**Rows:**

- FU-1870 (P5.10, medium): No census holds a read to writing nothing: a reader is refused by method alone, six reads advance the energy simulator, one rewrites its store and two run a model

**Files:** scripts/read_census.py (new); docs/READ_CENSUS.json (new); agentic_core/api/organism_status.py; agentic_core/api/economy.py; agentic_core/api/capital_fund.py; agentic_core/api/change_control.py; agentic_core/api/qep_intelligence.py

**-k:** -k "no_reading_route_writes or test_organism_status or test_organism_health_summary or test_organism_lifecycle or test_w438_ or test_w439_ or test_w492_ or test_w494_ or test_w495_ or test_w635_ or test_w637_ or test_w658_ or test_w694_ or test_w742_ or test_economy_board_pack or test_w442_ or test_fund_status or test_w496_ or test_w814_ or test_w910_ or test_t2_ or test_w601_ or test_w683_ or test_w686_ or test_w966_ or test_w1075_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- State why FU-912 and FU-1108 are not returns: they sit in other files, and scripts/audit_returns.py's rule is the same file plus shared title words.
- AUTH_ENABLED=true is set only in the guard's child environment, passed by the test, never in the tracked script.
- Report first-touch creations and declare each with its reason.
- Add immune.status() and document-control meters.
- Stop the heartbeat in the child, or declare its writes.
- slot_source on the P5.10 and P4.1 rows; the living plan is in the file list.

### C8 as planned (cluster C; size M, 2 round(s))

**Title:** The read census: every mounted GET and every declared preview is called on a fresh data root, as nobody and as a reader, and writes nothing that is not declared with its reason

**Closes:** Gap 10 (n=10) and the v40 merged board-pack evidence. Closes the W1192 census row. The two reads that run a model are carried as defect entries on C9's row.

**Owning item:** P5.10 clause 1, the class guard at the mechanism every read passes. The property it holds is P4.1's 'the read-only role is refused every write'.

**Owner-gated:** No. The census runs sign-in only in its child process, and nothing in the tree is switched.

**Depends on:** W1192 (both rows). Cluster A's compose-preview round (its gap n=2, P3.30), which removes the preview's DCMS seal and chain append, must land first, or the census cannot be green. C9 follows.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | A reader is refused by HTTP method alone | agentic_core/auth/core.py:228-229 (READ_ONLY_ROLE, READING_METHODS = GET, HEAD, OPTIONS) and :232-241. scripts/auth_perimeter.py:75 counts writes by method. |
| ABSENT | A census that calls every read and compares the stores | test_w694 (63900) reads fabric handler source; test_w742 leg 8 (67535-67575) spies one read; test_w943, w945 and w947 snapshot around their own GETs; test_w1075 (87922) walks routes for ownership only. |
| EXISTS | Five GET handlers advance the process-wide ATP simulator | biobus.organism_context defaults to advance_atp=True (organism/biobus.py:269, docstring 281-284). The callers: GET /api/v1/organism/status (organism_status.py:386), /health-summary (:513), /lifecycle (:564), GET /api/v1/cca/impact/{cca_id} (change_control.py:2492) and GET /api/v1/economy/board-pack (economy.py:2257). |
| EXISTS | A sixth, through a helper | GET /api/v1/fund/status (capital_fund.py:303) calls _organism_posture() at :359, which calls organism_context() at :260. POST allocate also calls it at :616. A screen of GET handler bodies finds only the five above, so the census must call routes. |
| EXISTS | GET /api/v1/cca/impact runs a model and fires a signal | change_control.py:2507-2513 (gateway.query_meta, biobus.fire_signal). Every completion chains a checkpoint (ai/gateway.py:67-91). |
| EXISTS | GET /api/v1/intelligence/forecasts writes a cache and runs a model | products.py:926 (cache path), :956 (query_meta when the cache is over an hour old), :966 (cache_path.write_text, neither atomic nor locked). |
| EXISTS | GET /api/v1/qep/adaptation/registry rewrites its store on every read | qep_intelligence.py:451-459 (_save under store_lock). The other readers migrate in memory (:517, :561), so not saving changes no answer (test_w439, 9040-9051). |
| EXISTS | The compose preview seals and chains while saying 'Nothing is saved' | resource_fabric.py:3904-3921 calls _simulate_configuration, which calls assure_delivery (:3877; vbs/quality.py seals a DCMS version and logs the UEG). Cluster A owns the fix. |
| EXISTS | The membrane observes no GET | horizon/membrane.py:45 (OBSERVED_METHODS = POST, PUT, PATCH, DELETE). It is called in a finally at app_mvp.py:189-198. No allow entry is needed. |
| EXISTS | The stores fix their directory at import, so a fresh root needs a child process | integration_tests/conftest.py (the W394 note). test_w601 lists the isolation variables: DATA_DIR, WORKSTATION_DATA_DIR, WORKSTATION_UEG_PATH, PROJECTS_DIR, SYNTHESIS_OUTPUT_DIR, PROPOSALS_DIR, LISTINGS_DIR and AI_DISABLE_LOCAL. |
| EXISTS | A precedent allow-list with reasons and defect rows | scripts/literal_outcomes.py and docs/LITERAL_OUTCOMES.json: a reason of at least 30 characters, or a defect naming an open row; a closed row excuses nothing. Held by test_w966 (81698). |
| EXISTS | The size of the walk | About 313 @router.get decorators across agentic_core. Streams are skipped by path as test_w1075 does (stream, /events, /sse, /ws). |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- No census holds a read to writing nothing: a reader is refused by method alone, six reads advance the energy simulator, one rewrites its store and two run a model (P5.10, medium)
- Two reading routes run a model, so a reader's call records a checkpoint, an outcome and a work-budget spend (P4.1, medium)

**Rows it closes:**

- The census row, closed as built. The model-run row stays open for C9. FU-912 and FU-1108 stay done, because their sites still hold (test_w694, test_w742 leg 8).

**Changes:**

- scripts/read_census.py (new): Run as 'python scripts/read_census.py --json' with the isolation variables set to a fresh empty directory. It refuses a non-empty root, so it can never walk a real store, and it refuses outbound sockets. It seeds one entity (establish, ship_output false), one change (cca/submit) and one deliverable. It fills path, query and required body fields as test_w1075's fill does, using the seeds for id parameters. It walks every mounted GET (streams skipped by path) and each declared preview POST twice: first touch, then again. Around each call it compares (size, mtime_ns) under the root and the UEG path. It counts ATP simulator updates, with biobus._atp_last_update reset to 0 before each call (W742's meter), plus fire_signal calls and gateway completions. A change no entry covers is a finding naming the route and what changed. Each GET that never answered 2xx is listed with its status. It compares the checkout's git status before and after. A second pass sets AUTH_ENABLED=true in the child only, as a viewer, over the routes that ask who is calling. It refuses when it examined nothing.
- docs/READ_CENSUS.json (new): previews: POST /api/v1/resources/compose/simulate and POST /api/v1/resources/cell/propose, each with its why. not_previews: POSTs whose 'nothing is written' wording covers only a refusal, each with its why. entries: {method, path, effect, pass}, each with a reason of at least 30 characters or a defect naming an open row. The two model-running GETs are defect entries on the P4.1 row.
- agentic_core/api/organism_status.py: :386, :513 and :564 call organism_context(advance_atp=False).
- agentic_core/api/economy.py: Board pack at :2257 calls with advance_atp=False.
- agentic_core/api/capital_fund.py: _organism_posture(advance_atp) is passed False by GET /fund/status. POST allocate at :616 is unchanged.
- agentic_core/api/change_control.py: Impact at :2492 calls with advance_atp=False. Its model call is C9's.
- agentic_core/api/qep_intelligence.py: The registry GET at :451-459 migrates in memory and saves nothing.
- docs/FABLE_DELIVERY_PROMPT.md and docs/FOLLOWUPS.json: A P5.10 UPDATED line naming the census as clause 1's guard for reads. Close the census row.
- integration_tests/test_mvp_spine.py: The new guard.

**Guard:** test_wXXXX_p510_no_reading_route_writes_and_no_declared_preview_saves_as_nobody_or_as_a_reader

- The census child on a fresh root reports findings == [] and stale == []. FAILS IF: Any GET or preview changes a file, advances the simulator, fires a signal or runs a model that no entry covers.
- It examined at least 250 GETs and at least 150 answered 2xx, and every GET it did not reach is listed with its status. FAILS IF: The walk skipped or stopped. It refuses on zero.
- A router mounted only in the child, with GETs that write a file under the root, log a chain event, call organism_context() and call gateway.query_meta, gives exactly those four findings. FAILS IF: A meter is blind.
- Every entry has a reason of at least 30 characters or a defect naming an open row. An entry whose route no longer makes its change, or names an unmounted route, fails. FAILS IF: The allow-list's hygiene is dropped.
- Every POST whose docstring or note says nothing is saved, saves nothing, stores nothing or read-only is on previews or not_previews. FAILS IF: A new 'Nothing is saved' POST is undeclared.
- The viewer pass examined at least 100 asking routes with a 2xx and found nothing. FAILS IF: Pass B did not run, or a reader's GET writes.
- In this process, a simulator spy (W742's) sees no advance across GET /organism/status, /health-summary, /lifecycle, /economy/board-pack, /cca/impact/{id} and /fund/status. A planted legacy registry is byte-identical after GET /qep/adaptation/registry, and the answer is migrated. FAILS IF: A fixed read regresses.
- The checkout's git status is unchanged by the walk. FAILS IF: A GET writes into the repository.
- The census refuses a non-empty root. FAILS IF: It could walk a real store.

**Blinds:**

- Restore biobus.organism_context() in GET /organism/status. -> Legs 1 and 7 go red.
- Restore _save in the registry GET. -> Legs 1 and 7 go red.
- Make a plain GET save, for example GET /api/v1/business-plan writing the plan. -> Leg 1 goes red.
- Empty one entry's reason. -> Leg 4 goes red.
- Leave the UEG path out of the snapshot. -> Leg 3's chain-event plant is missed.
- Remove compose/simulate from previews. -> Leg 5 goes red.
- Remove the simulator spy. -> Leg 3 goes red.
- Allow a non-empty root. -> Leg 9 goes red.

**Pins:**

- test_w742_the_metabolism_tells_the_truth (67535-67575): leg 8: a projection advances nothing (spy on _atp.update and _update_atp) -> Unchanged. It goes in the -k as the same meter.
- test_w494_a_verdict_that_cannot_come_out_otherwise_is_not_an_assessment (21472, 21546): monkeypatch.setattr(_bb.biobus, "_update_atp", lambda *a, **k: 1.0) ... _os = client.get("/api/v1/organism/status").json() -> Kept. The stub serves direct calls, and the GET now reads without advancing; only its keys are asserted.
- test_w439_refuter_pass_findings_stay_fixed (9040-9051): legacy registry -> GET registry migrated; the compliance audit's fidelity is 'not_checked' -> Kept. The audit migrates on read (:561).
- test_organism_status / test_organism_health_summary / test_organism_lifecycle (2562-2592): the answer's keys -> Kept.
- test_w694_a_read_that_is_not_free_says_so_for_every_handler_that_makes_it_and_genesis_is_called_with_nobody (63900-63945): fabric handlers declare that a read advances ATP -> Unchanged. These are fabric runs, not GETs.

**Rulings it rests on:**

- P5.10 clause 1 (FABLE:7032-7034). Its BOUNDARY: nothing is called certified.
- P4.1 readiness: the read-only role is refused every write.
- OWNER RULINGS 2026-11-20 (evening) and 2026-11-21 (late evening, recorded by W1191): sign-in only on the Owner's machine, and no one else signs in until step 12. The census's reader pass makes that promise hold before then.
- S18.1: the work budget is measured work, so a read that spends it is a write.
- W742 and W694: reads that are not free are said or removed.
- Standing: sign-in is set only in the child process, never in the tree; data/ is untouched.

**Risks:**

- The first run will probably find more than the eight named instances. Each is fixed or carried as a defect entry on an open row named in the round; a second round may be needed.
- A slow suite (FU-301): one child walk of about 300 routes adds a minute or two.
- Background threads in the child could write during a call. The census re-calls a route once to confirm a finding before reporting it.

### C8's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- None found. Verified READING_METHODS (auth/core.py:228-229) and the refusal (232-241); auth_perimeter.py:75; biobus.organism_context(advance_atp=True) at 269 and its docstring at 282-284; the GETs at organism_status.py 380/386, 504/513 and 559/564 (616 is the POST homeostasis); GET impact at change_control.py 2484/2492 with query_meta and fire_signal at 2507-2511; GET board-pack at economy.py 2206/2257; capital_fund.py 256/260, 303/359 and the POST at 616; products.py 926/956/966; the registry save at qep_intelligence.py:451-459; compose/simulate at resource_fabric.py:3904; membrane.py:45 with app_mvp.py:189-198; and 313 @router.get decorators. No test relies on a status GET advancing ATP.

**Guard legs that could not fail:**

- None. Leg 3's planted router makes each meter fail if blind.

**Pins the plan missed:**

- None that break: test_w494 (21472-21546) stubs _update_atp and asserts keys; test_w742 at 67552-67558 uses its own meter; test_w439 (9040-9051) asserts the answer only; test_w694 reads fabric handlers only.

**Conflicts with a ruling:**

- P5.10 clause 1 (FABLE:7032-7034): 'a return reopens the row and the CLASS gets a guard'. The plan says it acts 'as clause 1 asks' while declining to reopen FU-912 and FU-1108. It should say why these are not returns: they sit in different files from FU-912's fabric handlers, and scripts/audit_returns.py's own candidate rule is the same file plus shared title words. Otherwise it should reopen them.
- Standing constraint 'no round sets AUTH_ENABLED=true in the tree'. Keep the viewer pass's AUTH_ENABLED=true in the guard's child environment, passed by the test, rather than hard-coded in a tracked script a person can run.
- Numbering: W1193. It also depends on cluster A's preview round.

**Bar demands the plan missed:**

- The warm 'first touch' pass hides any store a read creates. A reader's first GET that creates a store is a write by the read-only role (P4.1). Report first-touch creations and require each to be declared with its reason.
- The in-memory meters the reproduce-lens refuter named beyond ATP, signals and completions are absent: immune.status() events and the document-control registry.
- Stop the heartbeat in the census child, or declare its writes. A re-call can still coincide with a beat.

**Fixes asked for:**

- Add the first-touch list and its entries, the immune and document-control meters, and a stopped heartbeat. State clause 1's 'not a return' reasoning.
- List the living plan, and carry slot_source on the P5.10 and P4.1 rows.

**Re-sized:** M, 2 rounds (the first run will probably find more than the eight instances named).

## W1221 - C8: The read census, part 2: what its first run found beyond the named instances is fixed, or carried as a defect entry on an open row

**Closes:** The census row

**Owning item:** P5.10 clause 1

**Held on:** W1220

**Rows:**

- FU-1870 (P5.10, medium): No census holds a read to writing nothing: a reader is refused by method alone, six reads advance the energy simulator, one rewrites its store and two run a model

**Files:** docs/READ_CENSUS.json; the handler files the first run names

**-k:** same as W1220

**Notes from the lead:**

The planner estimated two rounds. This is the second, sized by what W1220's run finds.

*C8's design and refutation are printed under W1220, the first round that carries C8.*

## W1222 - C9: A reading route answers what is stored and never runs a model: the change impact and the portfolio forecast compose only on a write

**Closes:** Its row (P4.1) and the census's two defect entries

**Owning item:** P4.1

**Held on:** W1221, W1210 (products.py)

**Rows:**

- FU-1871 (P4.1, medium): Two reading routes run a model, so a reader's call records a checkpoint, an outcome and a work-budget spend

**Files:** agentic_core/api/change_control.py; agentic_core/api/products.py; docs/READ_CENSUS.json; README.md

**-k:** -k "a_model_runs_only_on_a_write or no_reading_route_writes or test_w499_ or test_w683_ or test_w686_ or test_w1077_ or test_w651_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- test_w1077 (:88222) calls GET /api/v1/cca/impact/{cca} as a second person, so its 404 is kept.
- A leg checks that another person's POST /api/v1/cca/{cca_id}/impact answers 404 and composes nothing.
- test_w651's _NOTHING_TYPED entry ('products.py', 'intelligence_forecasts') at :50416 moves in the same round.
- Choose in the design between a POST and retirement for the forecast; nothing in apps calls it.
- README figures move by the routes changed.

### C9 as planned (cluster C; size S, 1 round(s))

**Title:** A reading route answers what is stored and never runs a model: the change impact and the portfolio forecast compose only on a write

**Closes:** The W1192 P4.1 row on the two reads that run a model, and the census's two defect entries.

**Owning item:** P4.1 (the read-only role is refused every write). P5.10's census holds it.

**Owner-gated:** No. P4.1's promise as written decides it: a model run chains a governance checkpoint and records an outcome and a work-budget spend.

**Depends on:** C8.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The impact GET composes and fires a signal | change_control.py:2484-2514. |
| EXISTS | The forecast GET writes a non-atomic cache and composes | products.py:916-967. |
| EXISTS | Neither route has a caller | No match in apps/workstation-superapp/src or in test_mvp_spine.py. |
| EXISTS | README route figures are recomputed and held | scripts/readme_figures.py, held by test_w499 (22866-22889). |

**Rows it closes:**

- The P4.1 row W1192 registers ('Two reading routes run a model...'), closed as built.

**Changes:**

- agentic_core/api/change_control.py: GET /impact/{cca_id} answers the change's stored assessment, or says none has been composed and that POST composes one. A new POST /api/v1/cca/{cca_id}/impact composes, stores the assessment on the change under its lock, and fires the signal. It is a write, so a reader is refused at the caller dependency.
- agentic_core/api/products.py: GET /api/v1/intelligence/forecasts answers the stored forecast or says none has been composed. A POST composes it and writes it with atomic_write_json under store_lock. Alternatively, since nothing calls the route, retire it as W807 retired dead routes; the round chooses and says why.
- docs/READ_CENSUS.json, README.md (scripts/readme_figures.py): Remove both defect entries and recompute the figures.
- integration_tests/test_mvp_spine.py: The new guard.

**Guard:** test_wXXXX_p41_a_reading_route_answers_what_is_stored_and_a_model_runs_only_on_a_write

- GET impact on a seeded change makes zero gateway calls and leaves the root unchanged. FAILS IF: The GET composes.
- POST impact as a user composes once and stores the assessment, and the next GET answers it. FAILS IF: The assessment is not stored or not read back.
- With sign-in on in the test process, a viewer's POST is refused 403 and composes nothing, while the viewer's GET answers the stored text. FAILS IF: A reader composes.
- GET forecasts neither writes nor composes, and POST writes the forecast whole. FAILS IF: The GET writes.
- The census reports no finding and no entry for either route. FAILS IF: A stale defect entry remains.

**Blinds:**

- GET impact still calls query_meta. -> Leg 1 goes red.
- POST impact does not save. -> Leg 2 goes red.
- Mount POST impact without the caller dependency. -> Leg 3 goes red.
- GET forecasts writes its cache. -> Leg 4 and the census go red.
- Keep the defect entries. -> Leg 5 goes red.

**Pins:**

- test_w499_the_plan_projects_only_the_work_a_round_closes (22866-22889): README figures recomputed by scripts/readme_figures.py -> Re-run the figures in the round.
- test_w683_every_mounted_route_asks_or_is_declared_public_and_the_strict_check_passes (62666): every mounted route asks or is declared public -> Kept: the new POST asks who is calling.

**Rulings it rests on:**

- P4.1: the read-only role is refused every write.
- W505: every completion carries its governance checkpoint.
- W807: dead routes may be archived.
- W1077: another person's change is answered as not found.

**Risks:**

- The route-count figures change. Re-run readme_figures in the apply script.

### C9's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- 'Neither route has a caller: No match in apps/workstation-superapp/src or in test_mvp_spine.py' is wrong. test_w1077_fu1263_with_sign_in_on_no_listing_hands_a_person_another_persons_entities_or_records (88138) calls GET /api/v1/cca/impact/{cca} as a second person and asserts 404 with no canary (88221-88224). Nothing in apps calls either route.

**Guard legs that could not fail:**

- None.

**Pins the plan missed:**

- test_w651_every_gateway_call_says_what_the_person_wrote_or_is_named_as_having_none (50399): _NOTHING_TYPED names ('products.py', 'intelligence_forecasts') at 50416. If the forecast's query_meta moves to a new POST function, or the route is retired, that entry goes stale and fails at 50462-50464. A new silent call in a new function is unnamed and fails at 50456-50460. It must change on purpose.
- test_w1077 88221-88224: GET impact must keep answering another person's change as 404.

**Conflicts with a ruling:**

- None. P4.1's 'the read-only role is refused every write' decides it, as the plan says. Numbering: W1193.

**Bar demands the plan missed:**

- W1077: the new POST /api/v1/cca/{cca_id}/impact must answer another person's change as not found and compose nothing. No leg drives it.
- 'Or retire it; the round chooses' leaves the guard (leg 4) and the pins unsettled. Choose in the design; the route has no caller.
- Closing the P4.1 row re-renders both plan documents, and the route count changes README figures (scripts/readme_figures.py, held by test_w499).

**Fixes asked for:**

- Add a leg: another person's POST gives 404 and no composition. Move the _NOTHING_TYPED entry in the same round. Choose POST or retirement for the forecast. List FOLLOWUPS, both plan documents and README.md. Add test_w651 and test_w1077 to the -k as changed or kept pins.

**Re-sized:** S, 1 round.

## W1223 - B6: The platform measured under the release machine's caps, the gateway's pacing reported apart, from a committed raw record the guard recomputes

**Closes:** Gap 14 (with gap 18 folded in by the lead) and its row

**Owning item:** P4.5

**Held on:** W1214 (the brief's part 7). It needs Docker on the round's machine.

**Rows:**

- FU-1861 (P4.5, medium): Nothing has measured the platform under the release machine's caps: no peak memory for its heaviest route, no time per route under the e2-micro's CPU share, no point where it refuses work, and nothing separates the gateway's pacing from a run's time

**Files:** deploy/load_drill.sh (new, LF); docs/load_run_<date>.json (new); docs/LOAD_MEASURED.md (new); docs/business/PRODUCTION_HARDENING_BRIEF.md; docs/business/COST_MODEL.md; .gitattributes

**-k:** -k "load_measurement or test_w912_ or test_w962_ or test_w1136_ or test_w1126_ or test_w1128_ or test_w1130_ or test_w1134_ or test_w1140_ or test_w1191_ or test_w703_ or test_w1143_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- Every gateway call waits on GATEWAY_RPM, 20 a minute unless set (config.py:48); the suite sets 6000 (conftest.py:21-25). GATEWAY_RPM is recorded in the raw record and the report, and pacing is reported separately: one run at 20 and one with the limit lifted. A pacing timeout is never called a capacity refusal.
- Leg 2 requires every per-route figure to be present.
- Leg 5 branches on NOT READ: with no cap, the figure is an upper bound on speed.
- COST_MODEL.md is re-read after W1192 and W1193. No '%' after '## Unit economics' (test_w962), and no $ amount.
- The brief names no row this round closes.

### B6 as planned (cluster B; size M, 1 round(s))

**Title:** The platform measured under the release machine's caps: the establishment journey one at a time and a concurrency ramp to the first refusal, from a committed raw record the guard recomputes

**Closes:** The load row W1192 registers on P4.5. Gap 18's establishment cost is folded in, by the lead ruling.

**Owning item:** P4.5. The single-run leg belongs to the pre-flights; the ramp is needed before P4.2's invited stage. Neither leg gates the Owner's deploy.

**Owner-gated:** The target machine, its account and the deploy are the Owner's. This is a proxy on a round's machine and says so; part 7's done line stays open. A measured need reopens P4.4 only by the Owner's ruling. No figure is booked in the work budget (S18.1).

**Depends on:** B3 landed (the brief's part 7 line 53 first). Docker on the round's machine, as W1128 and W1137 used. Google's machine-types page read for the e2-micro's sustained CPU share: if the network refuses it, the cap is recorded as NOT READ and the run says it had no CPU cap.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The brief says nothing has measured response times or memory on the target machine | docs/business/PRODUCTION_HARDENING_BRIEF.md:54-56 |
| EXISTS | The only memory figures are W1128's idle and probe readings, with no CPU cap | docs/DEPLOYMENT.md:95-110 (225 MiB idle, 253 MiB after the probes, under the 1 GiB cap) |
| EXISTS | The drills use the memory cap but record no memory figure and set no CPU cap | deploy/drill.sh:20-27 (--memory=1g --memory-swap=1g, no --cpus); it prints seconds and read-backs only |
| ABSENT | A load driver exists | deploy/ holds drill.sh, https_drill.sh and gcp/startup.sh. scripts/soak_organism.py drives heartbeat beats in process, and test_w749 classes it as 'a long-running soak driver'. |
| ABSENT | The e2-micro's CPU share is cited somewhere | DEPLOYMENT.md:183 names one e2-micro; no CPU figure anywhere in docs/*.md |
| EXISTS | The cost model leaves the cost of generating one entity NOT MEASURED | docs/business/COST_MODEL.md:53; test_w962 pins the formula text and allows no percentage in that section |
| EXISTS | New scripts under scripts/ must be placed in test_w749's census | test_mvp_spine.py:69608-69677. Scripts under deploy/ are outside it, and each needs a .gitattributes LF line (.gitattributes:3-5). |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- Nothing has measured the platform under the release machine's caps: no peak memory for its heaviest route, no time per route under the e2-micro's CPU share, no point where it refuses work (P4.5, medium)

**Rows it closes:**

- the load row (built, as a proxy)

**Changes:**

- deploy/load_drill.sh (new, LF): Runs the image with --memory=1g --memory-swap=1g --cpus=SHARE (passed in, from the sourced figure), -e AI_DISABLE_LOCAL=1, one uvicorn worker as the image runs it. Single-run leg: N fresh containers, each one journey (POST /api/v1/genesis/establish with a made-up problem, then GET /api/v1/vsb/{id}, /health, /), reading the container's cgroup cpu.stat usage_usec before and after, and memory.peak. Ramp: one fresh container per step at 1, 2, 4, 8 and 16 at once, until the first 5xx, 429, timeout or OOMKilled (docker inspect). It writes one JSON line per run and refuses when no run completed ('examined nothing').
- docs/load_run_<date>.json (new): The raw record: the commit, image id and drill script sha256; the caps and the share's source page and date, or NOT READ; the worker count; the round's machine (cpu count, memory); every run's row. It carries no host path.
- docs/LOAD_MEASURED.md (new): Each figure with its method, computed from the raw record by the apply: median and slowest seconds, CPU seconds and peak MiB per route; per ramp step, labelled 'while N ran at once'; and the first refusal or 'none up to K'. It says: a proxy on a round's machine, not the target machine; the CPU cap models the sustained share only, so it is a lower bound on speed; what it means for P4.4 (nothing reopens without the Owner's ruling).
- docs/business/PRODUCTION_HARDENING_BRIEF.md: Part 7, lines 54-55: cite `docs/LOAD_MEASURED.md` as a proxy measurement, labelled. The done line stays as it is.
- docs/business/COST_MODEL.md: Line 53: the contribution formula's cost names the measured work of one establishment, its CPU seconds and peak memory under the caps, from `docs/LOAD_MEASURED.md`. Money stays NOT MEASURED. No percentage and no amount.
- .gitattributes: Add 'deploy/load_drill.sh text eol=lf'.
- integration_tests/test_mvp_spine.py: The new test, which reads the committed files only. It runs no Docker.

**Guard:** test_wNNNN_the_release_shape_load_measurement_says_its_method_and_its_figures_come_from_its_raw_record

- Provenance: the raw record's commit is an ancestor of HEAD (git merge-base --is-ancestor); its script digest equals the sha256 of the committed deploy/load_drill.sh; it carries the image id, the caps (1g, 1g, and the share or NOT READ) and the worker count FAILS IF: the record names no commit, or the script changed after the run
- Figures recomputed: every figure the report states for the single-run leg (median and slowest seconds, CPU seconds, peak MiB per route) equals the one computed from the raw rows at the stated precision FAILS IF: a figure in the report was typed by hand or is stale
- Overlap labelled: every ramp figure says 'while N ran at once', and no per-run CPU figure is stated for a ramp step FAILS IF: overlapping CPU time is presented as one run's cost
- Refusal stated: the report names the first ramp step with a 5xx, 429, timeout or OOMKilled and its count, or says none up to the last step it ran, and agrees with the raw record FAILS IF: the refusal point is missing or differs from the record
- A proxy said as one: the report says round's machine, not the target machine, and calls the CPU cap a lower bound; the brief's part 7 cites it and keeps its done line; _w703_faults finds nothing in the brief or the cost model; the cost model's formula text is unchanged FAILS IF: the brief or the report implies the target was measured, or a rule of the business documents breaks
- The drill keeps LF: deploy/load_drill.sh has no CR, and .gitattributes holds its line FAILS IF: bash on a Windows checkout would run a CRLF file

**Blinds:**

- Delete the CPU figure from the report -> Leg 2: a raw-derived figure is missing.
- State a per-run CPU figure for the 8-at-once step -> Leg 3.
- Drop the commit from the raw record -> Leg 1.
- Change one stated median by a tenth -> Leg 2: it no longer equals the recomputation.
- Edit deploy/load_drill.sh after the run -> Leg 1: the digests differ.
- Remove 'not the target machine' from the report -> Leg 5.

**Pins:**

- test_w912_fu812_the_production_hardening_brief_scopes_each_part_by_its_evidence (test_mvp_spine.py:77704-77735): _w703_faults over the brief; named rows open -> The new statement is labelled and names an existing file and no row.
- test_w962_fu807_the_cost_model_marks_every_cost_by_where_it_came_from_and_fills_in_none (test_mvp_spine.py:81443-81451): 'Contribution per entity generated = the once-only price − the cost of generating one entity' and no percentage in the Unit economics section -> Keep the formula verbatim; the new sentence carries no percentage.
- test_w1136_fu1278_the_deploy_channels_published_price_is_stated_as_sourced_with_its_pages_and_date (test_mvp_spine.py:93026-93028): every $ amount in the cost model is stated in the deploy section -> Add no $ amount.
- test_w1140_fu1284_https_is_caddy_in_front_of_the_platform_and_no_one_signs_in_before_it and test_w1134 (test_mvp_spine.py:93329 and the .gitattributes reads): 'deploy/https_drill.sh text eol=lf' and startup.sh's line in .gitattributes -> Only add the new line.

**Rulings it rests on:**

- OWNER RULING 2026-10-12: the first deploy comes only after the dry run measured the memory fit (FABLE:6772-6775), which W1128 met
- OWNER RULING 2026-11-19: the dry run is a boot with a health probe (FABLE:6776-6777)
- OWNER RULING 2026-11-20 (evening): the deploy is the Owner's whenever it suits, and no build waits on it (FABLE:6778-6780)
- P4.4's boundary: a measured need reopens it only by a ruling of its own (FABLE:6759-6769)
- S18.1: the measurement books nothing in the budget
- Lead ruling on gap 18: no P5.1 row; the establishment journey's seconds, CPU seconds and peak memory are measured here

**Risks:**

- memory.peak must be read from the container's cgroup (cgroup v2). A fresh container per run keeps each peak clean; record the kernel's cgroup version in the raw record.
- This environment's egress proxy refused some sites in W1134 and W1140. If Google's page cannot be read, the CPU share is NOT READ, and the report says it had no CPU cap, which makes it an upper bound on speed instead.
- The raw record must carry no path on the round's machine, because test_w1135's and test_w732's screens read docs/.
- The commit recorded is the round's parent. The image is built from it, and the round itself changes only docs/, deploy/ and the test; say so in the report.

### B6's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Blind 1 (delete the CPU figure) turns leg 2 red only if leg 2 also requires each per-route figure to be present. As written, 'every figure the report states equals its recomputation' passes when a figure is simply missing.

**Bar demands the plan missed:**

- The gateway's pacing will dominate the figures:
  - Every gateway call acquires the rate limiter (gateway.py:447, :710), at GATEWAY_RPM, which is 20 a minute unless set (config.py:47).
  - The suite raises it to 6000 because 'at the default 20 a minute the limiter slept for a measured share of every run' (conftest.py:21-25).
  - The image runs at 20, so the establishment journey's seconds and the ramp's first timeout would mostly be the limiter's sleep, not CPU or memory.
  Record GATEWAY_RPM in the raw record. Report pacing apart, for example one labelled run at 20 and one with the limit lifted, and never call a pacing timeout a capacity refusal.
- Leg 5's 'calls the CPU cap a lower bound' needs a branch for NOT READ: with no cap set, the report says it is an upper bound on speed, as the plan's own risk says.

**Fixes asked for:**

- Add GATEWAY_RPM to the raw record and the report, with pacing reported apart.
- Make leg 2 require every per-route figure to be present.
- Branch leg 5 on NOT READ.
- Re-read COST_MODEL.md after W1192, which edits its gates section, before changing line 53.

**Re-sized:** M, 1 round

## W1224 - D-RETURN: The return measurement the Owner scheduled is built as a pre-flight of the invited stage: how many people come back, counted across people only

**Closes:** Its row (gap 12's build half, as the Owner scheduled it on 2026-11-22)

**Owning item:** P4.2

**Held on:** W1198 (the users store's command); before W1225 (so the retention register lists its store)

**Rows:**

- FU-1878 (P4.2, medium): The return measurement the Owner scheduled on 2026-11-22 as a pre-flight of the invited stage is not built: nothing counts how many people come back

**Files:** to be named by its planner: a per-person sign-in-day count under the data root, a route for counts across people, docs/business/METRICS_MEASURED.md, README.md if a route is added

**-k:** -k "return_measurement or test_w878_ or test_w1154_ or test_w703_ or test_w963_ or test_w885_ or test_w1075_ or test_w1192_ or test_w1120_ or test_w499_ or test_w462_ or test_w469_"

**Notes from the lead:**

The refuter's missing round, sketched here; it needs a planner's design before its turn.
- One sign-in day and one tool use per person per day.
- Counted across people only, never a figure about one person (2026-09-30: never grade a person).
- Driven with sign-in on in a test process.
- METRICS_MEASURED.md's 'A person returning' moves only with its source route (test_w878).

*D-RETURN has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## W1225 - B7: Every store says whether a person's data reaches it, in which fields, what of it is kept by rule, and that its period is the Owner's (part 1: the enumerator and the register)

**Closes:** Gap 5's register half (part 1)

**Owning item:** P4.2 (the Owner's ruling of 2026-11-22)

**Held on:** W1196 (memory_v01 gone), W1198, W1223 (the brief), W1224

**Rows:**

- FU-1862 (P4.2, medium): No store says whether it holds a person's data, what of it is kept by rule, or how long it is kept

**Files:** agentic_core/retention.py (new); docs/RETENTION_REGISTER.json (new); docs/business/PRODUCTION_HARDENING_BRIEF.md

**-k:** -k "whether_a_persons_data_reaches_it or test_w912_ or test_w703_ or test_w885_ or test_w1075_ or test_w749_ or test_w601_ or test_w732_ or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- There is no OWNER row. Every period reads 'not decided: the Owner's' and quotes the P4.2 ruling of 2026-11-22.
- enumerate_stores also lists the roots that environment variables can move: PROJECTS_DIR, SYNTHESIS_OUTPUT_DIR and PROPOSALS_DIR (projects/api.py:46, :227, :259), the realms folder, LISTINGS_DIR (marketplace.py:37) and WORKSTATION_UEG_PATH.
- The brief names no row this round closes.

### B7 as planned (cluster B; size M, 2 round(s))

**Title:** Every store says whether a person's data reaches it, in which fields, what of it is kept by rule, and that its period is the Owner's: a register held complete by an AST walk and true by a canary drive

**Closes:** The store-inventory row W1192 registers on P4.2

**Owning item:** P4.2 (a pre-flight of the real invited stage)

**Owner-gated:** Every period reads 'not decided: the Owner's' and names the OWNER row W1192 registers. The record of processing is the Owner's. Nothing is deleted in this round.

**Depends on:** W1192: this row and the OWNER retention row, which must be open for the register to name it. Cluster A's gap-1 round (the chromadb and memory_v01 stores) decides two entries: re-read them after it lands. B8 builds on this register.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | The brief states that no store has a period and no deletion reaches every store | PRODUCTION_HARDENING_BRIEF.md:60, with the fix marked [owner decision] at :61 |
| EXISTS | The stores agentic_core writes | 86 distinct literal data_path names; about 22 non-literal data_path calls (for example entity_specialists.py:127 and :274, scholar_review.py:55 and :60, support_claims.py:77, qms.py:94 and :100); DATA_DIR joins (reactor/religion/qep_flagship.py:32, synthesis/content_production.py:71 and :101, synthesis/api.py:86, ingestion/api.py:77-78); os.getenv('DATA_DIR') in commercial/token_ledger.py:34; MEMORY_FILE, INTERACTIONS_DB, L7_REGISTRY_FILE, MEETING_LOG_FILE and CHROMA_DB_PATH (store_paths.py:35-39); the UEG ledger (gaas/v5/ueg.py:27-40) |
| EXISTS | With sign-in on, the gateway keeps a person's prompt and reply with their owner_id in the interaction log and the memory store | ai/gateway.py:553-579 (keep_text; W952 keeps lengths only before sign-in, :266-275) |
| EXISTS | The per-item deletes, none of them per person | user_workspace.py:175 and :268-291; projects/api.py:500; ingestion/api.py:257; avatars/api.py:703; religious_domain/api.py:989 |
| ABSENT | A retention register | No register file, no row and no plan text names a retention period. FU-1817's why covers only where data may be kept. |
| EXISTS | S18.6 keeps a dead entity's record, and no entity is ever deleted | FABLE:2790-2792; the standing constraint |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- No store says whether it holds a person's data, what of it is kept by rule, or how long it is kept (P4.2, medium)
- OWNER: before anyone else's data is held, set a retention period for each store that holds a person's data, approve a record of processing, and say whether the solicitor's engagement (FU-1817) also answers retention and erasure (OWNER, medium)

**Rows it closes:**

- the store-inventory row (built)

**Changes:**

- agentic_core/retention.py (new): enumerate_stores(): an AST walk of agentic_core returning every literal data_path name, every non-literal data_path call site (file and function), every DATA_DIR / literal join, the os.getenv('DATA_DIR') joins, store_paths' constants and the UEG path. canary_reach(root, canary): every file under the data root and the UEG file whose bytes hold the canary, with the JSON paths where it appears (or 'sqlite pages' or 'bytes').
- docs/RETENTION_REGISTER.json (new): One entry per store: where it lives, its writer, whether the drive reached it and the fields where the person appeared (or 'not reached by the drive'), an erasure method or what is kept by rule and why (ledger postings, the UEG chain, an entity's record under S18.6), and a period of 'not decided: the Owner's (row FU-xxxx)'.
- docs/business/PRODUCTION_HARDENING_BRIEF.md: Part 8 cites `docs/RETENTION_REGISTER.json`, labelled [observed], names the OWNER row, and still says no deletion has been carried through every store.
- integration_tests/test_mvp_spine.py: The new test.

**Guard:** test_wNNNN_every_store_says_whether_a_persons_data_reaches_it_and_that_its_period_is_the_owners

- Complete: every store enumerate_stores() finds has a register entry, and every entry names a store the walk finds FAILS IF: a new store is added with no entry, or an entry names a store no code writes
- True, by a drive: with sign-in on, a made-up person whose name and texts carry a canary writes a workspace, a profile, a project, a support claim, an avatar chat, an upload, a domain tool's call, a Genesis establishment, a board pack and an economy cycle. The stores whose bytes then hold the canary are exactly the register's 'reached' set FAILS IF: a store holding the person's text is not marked (for example interactions.db), or a marked store did not receive it
- Each reached store says where and what: the fields where the canary appeared, and an erasure method or kept-by-rule with its reason FAILS IF: a reached entry says neither
- Periods are the Owner's: every period is 'not decided: the Owner's' naming an open OWNER row, or quotes a dated Owner ruling found in the plan FAILS IF: a period is typed with no ruling
- The brief: part 8 cites the register and the row, and _w703_faults and test_w912's rows-open rule hold FAILS IF: the brief claims a deletion was carried through, or names a closed row

**Blinds:**

- Drop interactions.db's entry from the register -> Legs 1 and 2: the walk finds it, and the drive reaches it.
- Add data_path('w_retention_blind.json') written by a scratch module -> Leg 1: a store with no entry.
- Set one period to '90 days' with no ruling -> Leg 4.
- Mark users.json as holding no person -> Leg 2: the canary username is in it.
- Have canary_reach skip binary files -> Leg 2: SQLite pages that hold the canary are missed.

**Pins:**

- test_w912_fu812_the_production_hardening_brief_scopes_each_part_by_its_evidence (test_mvp_spine.py:77704-77735): _w703_faults; 'row FU-...' must be open -> The OWNER row the brief names is open.
- test_w749_an_instrument_that_examined_nothing_refuses_and_reads_what_it_names (test_mvp_spine.py:69608-69677): every scripts/*.py is placed in a census bucket -> None if the enumerator stays in agentic_core. If a scripts/ CLI is added, list it among the instruments with an 'examined nothing' refusal.

**Rulings it rests on:**

- P5.7's brief, part 8: retention and the record of processing are [owner decision]
- S18.6 (FABLE:2790-2792): death conserves the balance and retains the record; no entity is deleted
- OWNER RULING 2026-11-20 (evening): the invited stage opens only after FU-1817 has answered (FABLE:6753-6754)
- OWNER RULING 2026-11-19: the rehearsal uses made-up accounts that hold nothing about a real person (FABLE:6717-6724)
- P5.8's BOUNDARY: no record of a real person other than the Owner before sign-in (FABLE:6946-6948)

**Risks:**

- The suite's data root is shared by the whole session, so the scan reads every test's files. The canary is unique, so this costs time, not truth.
- An avatar chat that reaches chromadb's default embedding model needs the network (cluster A's gap 1). Drive the path the suite already drives offline and say which one.
- Classifying around 120 entries by hand would be L. Reach is measured, and unreached stores say 'not reached by the drive', which keeps this M.

### B7's refutation: **NEEDS_FIXES**

**Wrong state verdicts - trusting these skips or redoes real work:**

- The stores inventory (marked EXISTS) leaves out roots set by other variables:
  - PROJECTS_DIR, SYNTHESIS_OUTPUT_DIR and PROPOSALS_DIR (projects/api.py:46, :227, :259);
  - the realms folder beside the projects (api/v290/realms.py:22);
  - LISTINGS_DIR (api/marketplace.py:37);
  - WORKSTATION_UEG_PATH (gaas/v5/ueg.py:38).
  In the suite, conftest puts PROJECTS_DIR, SYNTHESIS_OUTPUT_DIR and PROPOSALS_DIR under the repository's data/test_* (conftest.py:20, :26-27), outside the test DATA_DIR.

**Pins the plan missed:**

- test_w912 (test_mvp_spine.py:77689-77731) requires every row the brief names to be open. With no OWNER retention row (see the ruling conflict), part 8 must quote the P4.2 ruling rather than name an OWNER row.

**Conflicts with a ruling:**

- OWNER RULING 2026-11-22 at P4.2 (Q7 (a)), recorded by W1192: 'A round builds the deletion drill now ... with a retention register listing each store as "not decided: the Owner's"; the Owner sets the periods once FU-1817 answers'. The same decisions say 'no Owner QUESTION rows'. B7's OWNER row re-asks the periods and adds a widening of FU-1817 the Owner was not asked about. W1192 widens FU-1817 only to licence, title, the investment perimeter and the DPIA (W1192's staged apply (a session work file, not in the tree):88-94).
- OWNER RULING 2026-11-22 at P3.32 (Q2) retires memory_v01. The 'cluster A's gap-1 round decides two entries' dependency is therefore decided: B7 runs after cluster A's retirement round.

**Bar demands the plan missed:**

- canary_reach over the data root alone misses the roots above. In the suite a project write lands in data/test_projects, so leg 2's exact equality either fails on the first run or marks projects 'not reached', which is false in production. Run the drive in a subprocess on a fresh root with those variables unset or pointed inside it, and have enumerate_stores list the roots that environment variables can move.
- Pin the drive's serving path. The suite does not set AI_DISABLE_LOCAL, so a reachable local model on the Owner's machine changes which stores a gateway call writes. Set AI_DISABLE_LOCAL=1 in the drive.

**Fixes asked for:**

- Drop the OWNER row. Every period reads 'not decided: the Owner's' and quotes the P4.2 ruling.
- Order B7 after cluster A's memory_v01 retirement.
- Run the drive in a subprocess on a fresh root.
- Enumerate the environment-set roots.

**Re-sized:** M, 2 rounds

## W1226 - B7: The retention register is held true by a canary drive (part 2)

**Closes:** The store-inventory row

**Owning item:** P4.2

**Held on:** W1225

**Rows:**

- FU-1862 (P4.2, medium): No store says whether it holds a person's data, what of it is kept by rule, or how long it is kept

**Files:** agentic_core/retention.py; docs/RETENTION_REGISTER.json

**-k:** same as W1225

**Notes from the lead:**

The drive runs in a subprocess on a fresh root. The environment-set roots are unset or put inside it, and AI_DISABLE_LOCAL=1. In the suite, conftest puts the three roots under data/test_*, outside the test DATA_DIR, so a drive inside the suite would mark projects 'not reached'.

*B7's design and refutation are printed under W1225, the first round that carries B7.*

## W1227 - B8: An administrator's erasure of one made-up person (part 1: erase() and the command over SSH)

**Closes:** Gap 5's erasure half (part 1)

**Owning item:** P4.2

**Held on:** W1226, W1198

**Rows:**

- FU-1863 (P4.2, medium): No person's erasure has been carried through every store a person's data reaches

**Files:** agentic_core/retention.py; agentic_core/auth/erase_person.py (new); docs/RETENTION_REGISTER.json

**-k:** -k "erasure_of_one_made_up_person or whether_a_persons_data_reaches_it or remove_account or test_w912_ or test_w885_ or test_w1075_ or test_user_store_survives_concurrent_writes or test_w462_ or test_w469_"

**Notes from the lead:**

Refuter fixes applied:
- The interaction log is plain sqlite3 (ai/logger.py), so its erasure sets PRAGMA secure_delete=ON and VACUUMs, and says so.
- The two made-up people are named so that one name contains the other, or blind 4 (match by substring) stays green.
- No entity is deleted; the UEG chain still verifies.

### B8 as planned (cluster B; size L, 2 round(s))

**Title:** An administrator's erasure of one made-up person, driven end to end and read back: every reached store emptied of them, what the rules keep listed with its reason, no entity deleted, the chain still whole

**Closes:** The erasure row W1192 registers on P4.2

**Owning item:** P4.2 (a pre-flight of the real invited stage)

**Owner-gated:** The periods, the record of processing, whether an erased person's founder-written text in an entity record is redacted, and who holds such an entity afterwards are all the Owner's. The drill reports each as 'not decided: the Owner's' and decides none of them. Running it on a real person comes after FU-1817 and only on the Owner's instruction. A person's own deletion route comes only before self-serve sign-up (P4.2's second half).

**Depends on:** B7 (the register and canary_reach) and B2 (remove_account) landed. The OWNER retention row is registered. Cluster A's gap-1 decision on chromadb and memory_v01.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | No route or command takes a person and erases them | Only per-item deletes exist (user_workspace.py:175 and :268; projects/api.py:500; ingestion/api.py:257; avatars/api.py:703; religious_domain/api.py:989), and none reaches the interaction log or memory.json (gateway.py:553-579) |
| EXISTS | The UEG chain can be verified | agentic_core/gaas/v5/ueg.py:317 (verify_chain) |
| EXISTS | An entity's record is kept at death, and the Owner's protected entities are still unnamed | FABLE:2790-2792; FU-1165 open |
| ABSENT | The account-removal command | B2 builds it |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- No person's erasure has been carried through every store a person's data reaches (P4.2, medium)

**Rows it closes:**

- the erasure row (built: drilled on made-up accounts)

**Changes:**

- agentic_core/retention.py: erase(username) runs each reached store's method from the register. It removes the person's workspace file and profile key, their projects, support claims, avatar sessions and uploads (bytes, registry rows and memory copies), and their rows in the interaction log and memory.json (by owner_id), then the account (B2's function). It never deletes an entity: each record the person owns keeps its economics, and its owner fields are replaced with an erasure token. Ledger postings and the UEG chain are kept, with reasons. Every step reads strictly first and refuses a store it cannot read whole.
- agentic_core/auth/erase_person.py (new): 'python -m agentic_core.auth.erase_person USERNAME' over SSH, like set_password and remove_account. It refuses the admin, an unknown person and an unreadable store, and asks for the name again. It prints a report naming each store, what was removed (counts) and what was kept by rule and why. The report holds no part of the person's name or texts.
- docs/RETENTION_REGISTER.json: Each reached store's erasure method.
- docs/business/PRODUCTION_HARDENING_BRIEF.md: Part 8: a deletion request was driven end to end on made-up accounts and read back. No real person's data is held. The periods and the record stay the Owner's (the row).
- integration_tests/test_mvp_spine.py: The new test.

**Guard:** test_wNNNN_an_administrators_erasure_of_one_made_up_person_reaches_every_store_and_keeps_what_the_rules_keep

- Reach: two made-up people with distinct canaries write through every flow B7 drives. After erasing person one, canary_reach finds person one's canary only in stores the register marks as kept by rule, each with its reason FAILS IF: any erasable store still holds person one's text
- Nothing of person two's touched: person two's canary is where it was in every store FAILS IF: an erasure matches by substring or by store, not by owner
- The chain: UEGLogger().verify_chain() still verifies, and its entry count did not fall FAILS IF: an entry is removed or rewritten
- No entity deleted: the entity store's count is unchanged, and person one's entity keeps its record and balances with its owner fields replaced FAILS IF: an entity record is removed
- The account: a token issued to person one before the erasure answers 401 after it FAILS IF: the account survives
- The report: it names each store with counts and each kept item with its reason, and holds no part of person one's name or canary FAILS IF: the erasure record itself keeps the person

**Blinds:**

- Skip the interaction log -> Leg 1: the canary is in interactions.db.
- Delete person one's UEG entries -> Leg 3: the chain fails to verify and its count falls.
- Delete person one's entity -> Leg 4.
- Match records by a substring of the username -> Leg 2: person two's records sharing the prefix are erased.
- Write the username into the report -> Leg 6.

**Pins:**

- test_w912_fu812_the_production_hardening_brief_scopes_each_part_by_its_evidence (test_mvp_spine.py:77704-77735): part 8's rules -> The new statement is labelled and names only open rows.
- B7's test and B2's test (their own legs): the register's reached set and its methods; remove_account's behaviour -> Extend, never weaken. B7's reach leg stays green.

**Rulings it rests on:**

- Never delete an entity (standing constraint); S18.6 retains the record (FABLE:2790-2792)
- The UEG chain is tamper-evident and must still verify (gaas/v5/ueg.py)
- P5.7 brief part 8: periods and the record are the Owner's
- OWNER RULING 2026-11-20 (evening): no one but the Owner is invited until FU-1817 has answered
- P4.2: self-serve comes only after the invited stage, so a person's own deletion route is not built now

**Risks:**

- Founder-written text in an entity record (name, concept, sections) is the person's but sits in a record the rules keep. The drill lists it as kept, 'the Owner's to rule', rather than redacting it on its own.
- chromadb and memory_v01 depend on cluster A's gap 1: until that lands, the drill may have to report one store as 'not erasable yet' honestly.
- Many stores carry no owner field, so an erasure needs a per-store key, often an entity id rather than a person. The register must say which key each store's erasure uses.

### B8's refutation: **NEEDS_FIXES**

**Guard legs that could not fail:**

- Blind 4 (match by a substring of the username) turns leg 2 red only if person two's name contains person one's, for example 'w-erase-ann' and 'w-erase-ann-2'. Two unrelated made-up names leave it green. The plan must name them so.

**Conflicts with a ruling:**

- P3.32's ruling of 2026-11-22 retires memory_v01, so the 'not erasable yet' contingency is obsolete. Order B8 after cluster A's retirement round.

**Bar demands the plan missed:**

- A SQLite DELETE leaves the row's bytes in free pages. interactions.db is plain sqlite3 with the default journal (ai/logger.py:12-30), so canary_reach's byte scan would still find person one's canary. The erasure must set PRAGMA secure_delete=ON and VACUUM, and say so; otherwise leg 1 fails on its first run.

**Fixes asked for:**

- Name the two people so one name contains the other.
- Add secure_delete and VACUUM to the interaction log's erasure.
- Depend on cluster A's retirement round, B7 and B2.

**Re-sized:** L, 2 rounds

## W1228 - B8: The erasure driven end to end and read back (part 2), and the brief's part 8 restated

**Closes:** The erasure row

**Owning item:** P4.2

**Held on:** W1227

**Rows:**

- FU-1863 (P4.2, medium): No person's erasure has been carried through every store a person's data reaches

**Files:** agentic_core/retention.py; docs/business/PRODUCTION_HARDENING_BRIEF.md

**-k:** same as W1227

**Notes from the lead:**

Part 8 says a deletion request was driven end to end on made-up accounts. Every period and the record of processing stay the Owner's. The brief names no row this round closes.

*B8's design and refutation are printed under W1227, the first round that carries B8.*

## W1229 - A12: TopologyDefense reports no repair it did not make: simplicial_repair is deleted, as its ledger rule says, and _interrupt_agent is recorded as latent

**Closes:** Gap 23, correction 15 and its row

**Owning item:** P3.30

**Held on:** Ordered last by the lead ruling

**Rows:**

- FU-1854 (P3.30, low): TopologyDefense.simplicial_repair returns HEALED and seals a repair event for a repair it never makes, and the class docstring claims simplicial repair

**Files:** agentic_core/topology/defense.py; docs/NATIVE_PRIMITIVE_DEFECT_LEDGER.md

**-k:** -k "reports_a_repair_it_did_not_make or test_native_topology_betti_in_house or test_w597_p324_ or test_w437_ or test_w462_ or test_w469_"

**Notes from the lead:**

SOUND as planned. One optional addition, by the ledger's own rule ('an unreached defect is a ledger entry'): record agentic_core/mjm/self_reflection_engine.py (SelfReflectionEngine, whose reflect() nothing calls) and agentic_core/simulation/nanophotonics.py (imported by nothing) as latent. The v40 body found both and neither is in the ledger. This adds ledger entries only, no code.

### A12 as planned (cluster A; size XS, 1 round(s))

**Title:** TopologyDefense reports no repair it did not make: simplicial_repair is deleted, as its ledger rule says, and _interrupt_agent is recorded as latent

**Closes:** Gap 23 as the lead ruling keeps it, merged with correction n=15 (defense.py:12, :113-132)

**Owning item:** P3.30, tier 3, as FU-1125 (W779) and FU-1158 (W792) were

**Owner-gated:** No.

**Depends on:** Ordered last, by the lead ruling.

**State checked:**

| verdict | claim | evidence |
|---|---|---|
| EXISTS | simplicial_repair returns success True, simplices_added 2 and status HEALED after an emulated step, and logs simplicial_repair_complete | defense.py:113-132 |
| EXISTS | The class docstring claims simplicial repair, and repair_success_rate is never computed | defense.py:12 and :19 |
| ABSENT | A live caller exists | git grep: the only caller is _archive/scripts/supreme_convergence_validation.py:303. The live route calls compute_persistent_homology only (native_ai.py:1656-1657). |
| EXISTS | It is recorded as latent, with a rule | NATIVE_PRIMITIVE_DEFECT_LEDGER.md:290-293 ('If revived: perform or delete, never report'); FABLE:915-917 (RECORDED, LATENT) |
| ABSENT | runtime_framework is unreached | It is reached. products/business_incubator/sdk/business_incubator.py:10 imports it, test_w597_p324 imports that SDK (test_mvp_spine.py:43665-43668), and eight copies live at products/*/sdk/runtime_framework.py. |
| ABSENT | _interrupt_agent is reached | Only apply_containment calls it, and only verify_action calls that (runtime_framework.py:76, :88, :103, :123, :125). The SDK calls check_arifos_floors only (business_incubator.py:51). |
| ABSENT | A test pins the latent list or the ledger entry | grep: only a comment at test_mvp_spine.py:8539 |

**Rows it planned to register** (W1193 registered them; the ids are in this round's heading):

- TopologyDefense.simplicial_repair returns HEALED and seals a repair event for a repair it never makes, and the class docstring claims simplicial repair (P3.30, low)

**Rows it closes:**

- The A12 row registered by W1192: closed as built

**Changes:**

- agentic_core/topology/defense.py: Delete simplicial_repair (:113-132) and the repair_success_rate attribute (:19). The docstring (:12) says persistent-homology Betti-number surveillance only. compute_persistent_homology is unchanged.
- docs/NATIVE_PRIMITIVE_DEFECT_LEDGER.md: The :290-293 entry says simplicial_repair was deleted in this round, by its rule. A latent entry is added for RuntimeConstitutionalFramework._interrupt_agent (agentic_core/governance/runtime_framework.py and its eight products/*/sdk copies): it logs that an agent 'has been PAUSED/TERMINATED' and interrupts nothing, and it is reached only through verify_action, which nothing live calls. If revived: interrupt, or say only that the tier was recorded.
- docs/FABLE_DELIVERY_PROMPT.md: The RECORDED, LATENT list (:915-917) drops simplicial_repair (dated: deleted), keeps the other three, and adds _interrupt_agent.
- integration_tests/test_mvp_spine.py: Append the new guard.

**Guard:** test_wNNNN_no_topology_code_reports_a_repair_it_did_not_make

- TopologyDefense has no simplicial_repair and no repair_success_rate, and its docstring says nothing of repair FAILS IF: Red at HEAD.
- No module under agentic_core or products passes the string 'simplicial_repair_complete' to any call FAILS IF: Red at HEAD (defense.py:131).
- POST /api/v1/native-ai/topology still gives a tree beta1 0, a cycle beta1 1 and a fracture beta0 3 FAILS IF: A keep leg: red if the deletion breaks the live method.
- The plan's RECORDED, LATENT list no longer lists simplicial_repair as present and names _interrupt_agent; the ledger entry says deleted and names the round FAILS IF: Red at HEAD.

**Blinds:**

- Restore the method body -> Legs 1 and 2.
- Restore 'and simplicial repair' in the docstring -> Leg 1.
- Log 'simplicial_repair_complete' from the native-ai topology route -> Leg 2.
- Leave _interrupt_agent off the latent list -> Leg 4.

**Pins:**

- test_native_topology_betti_in_house (test_mvp_spine.py:4556-4568): tree beta1 0, cycle beta1 1, fracture beta0 3; "topology" in tree["method"] -> Keep.
- test_w597_p324_a_schedule_never_a_forecast (test_mvp_spine.py:43665-43668): importlib.import_module("products.business_incubator.sdk.business_incubator") -> Keep. runtime_framework is untouched.

**Rulings it rests on:**

- The lead ruling: one low-severity P3.30 tier-3 row merged with correction 15. Delete simplicial_repair, correct the docstring, update the plan's list and the ledger, leave runtime_framework, record _interrupt_agent as latent, and do it last.
- P3.30 ACCEPT (1): remove a STUB.
- P5.10 clause 8: a tier-3 row is batched by file or dropped; this one is built in its own file.
- The ledger's W437 rule: perform or delete, never report.

**Risks:**

- The three other latent functions (run_evolution_cycle, get_aggregate_accuracy, network/planetary.py) stay as recorded. The lead ruling scoped this round.

### A12's refutation: **SOUND**

**Re-sized:** XS (unchanged). Checked: defense.py:10-19 and :113-132; that the only simplicial_repair caller is under _archive; FABLE:915-917 (the count stays four: three kept plus _interrupt_agent); NATIVE_PRIMITIVE_DEFECT_LEDGER.md:290-293; business_incubator.py:10 and test_w597 (:43665-43668); that verify_action of RuntimeConstitutionalFramework is called only inside runtime_framework.py (:76, :88, :103) and its eight products copies, while prompt_evolver.py:50 and ceo.py:154 call other classes' verify_action; that no suite pin names simplicial text. The lead ruling is followed and the round is ordered last.

## W1230 - A3b: HELD - chromadb's direct declaration, which brings onnxruntime, is dropped once nothing imports it

**Closes:** The dependency left after A3 (the refuter's conditional round)

**Owning item:** P2.40 (the dependency route: requirements.txt and pyproject.toml route there)

**Held on:** The Owner's answer to the chromadb question (in chat), and W1196. Answered on the morning of 2026-11-22 (W1193c): no longer held; still after W1196. The Owner's answer is recorded at P3.32.

**Rows:** none of its own; see its notes.

**Files:** pyproject.toml; poetry.lock; requirements.txt

**-k:** -k "test_w583_p325 or test_w907_ or test_w1147_ or memory_v01 or test_w499_ or test_w462_ or test_w469_" plus a full suite on a fresh environment

**Notes from the lead:**

Uses W1141's method (FU-1174, FU-1277): re-make the lock, export requirements.txt, and run a full suite on a fresh environment. Re-check test_w583 L5's opentelemetry pins (opentelemetry-api is also required by anthropic) and test_w907's sympy rule (sympy is also required by torch).

*A3b has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## W1231 - C5b: HELD - the two approved legal-form descriptions say what each template models

**Closes:** The rewording the C5 planner proposed as an OWNER row

**Owning item:** P5.18 clause 1

**Held on:** The Owner's answer to the template question (in chat), and W1216. Answered on the morning of 2026-11-22 (W1193c): no longer held; still after W1216. The Owner's answer is recorded at P5.18 and in FU-1868.

**Rows:** none of its own; see its notes.

**Files:** agentic_core/economy/entities.py; docs/VSB_ECONOMIC_LEGAL_MODEL.md (a dated note in section 2, the earlier words kept); the entity-types fixtures (GenesisJourney, VSBEconomy, VSBEconomy.fee)

**-k:** -k "no_company_is_formed or test_economy_entity_types or test_w1047_ or test_w924_ or test_w488_ or test_w462_ or test_w469_" plus the pages' vitest files

**Notes from the lead:**

The nine names are kept.

*C5b has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## W1232 - CANVAS-CREDIT: HELD - the ratified canvas's credit line gains a dated note for the carry-forward ruling, the earlier words kept

**Closes:** The residue of Q11 in the one ratified text W1192 did not amend

**Owning item:** OWNER (a ratified text)

**Held on:** The Owner's answer to the canvas question (in chat). Answered on the morning of 2026-11-22 (W1193c). Not built: W1193c made the note.

**Rows:** none of its own; see its notes.

**Files:** docs/business/BUSINESS_MODEL_CANVAS.md

**-k:** -k "test_w725_ or test_w703_ or test_w963_ or test_w1154_ or test_w1192_ or test_w462_ or test_w469_"

**Notes from the lead:**

The opening's change line becomes 'Changed three times since'. That changes test_w725's pin and test_w1192's 'Changed twice since' pin, both on purpose.

*CANVAS-CREDIT has no planner's design: the lead added it from the refutations, and its heading and notes above are what a builder starts from, after a planner's design of its own.*

## Rows with no round in this schedule

- FU-1851 (P5.10, medium): Three functions read a shared store strictly and write it back with no lock around the write; the org cascade's two tier stores lose an update inside one process when two cascades overlap Its round: none in this schedule (open; each site to be read).
- FU-1855 (P4.1, medium): With CORS_ORIGINS unset, or set by a .env copied from .env.example, the Owner's own local platform takes a write from a page of any site while sign-in is off Its round: none in this schedule (open; a round must keep every localhost origin working).
- FU-1882 (OWNER, low): OWNER: open a developer account at the Quran Foundation, whose terms P5.17 clause 7 leaves with you, after reading them whole Its round: none (the Owner's act; the row closes on the Owner's dated word).
- FU-1883 (P5.8, medium): A data protection impact assessment is to be drafted before any health-related wellbeing entry, as the Owner ruled on 2026-11-22, and no row holds the draft Its round: none in this schedule (P5.8's own rounds).
- FU-1884 (P5.10, medium): Three served texts call a management system ISO 9001- or ISO 14001-aligned and the systems registry maps clauses of ISO 9001, against P5.10's BOUNDARY that nothing is called certified, compliant or aligned and no clause of any standard is mapped Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.
- FU-1885 (P5.20, medium): The statute panel's fidelity check says the text shown was compared character for character with the text read from the publisher, but it compares the parsed text with a hash taken from that same parse, so it can never fail Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.
- FU-1886 (P5.13, medium): The Care risk door asks a model for a clinical interpretation, prioritised actions with urgency, escalation triggers and current clinical guidelines, and composes the catalogue's safeguarding entry with none of the safeguarding form's checks Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.
- FU-1887 (P4.2, medium): Nothing holds a person for a clinical score used in someone's direct care: NEWS2's score and band are returned to any caller at the unreviewed tier, though the review options name that exception Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.
- FU-1888 (P5.19, low): The simulated device rows carry no simulated label: GET /api/v290/iot/devices serves the retired frontier store's rows with only an id, a type and a status Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.
- FU-1889 (P5.17, low): The Pickthall translation the Quran platform serves has no row in the register of sources: its public-domain basis is written only in the route's own code Its round: no round in docs/V44_ROUNDS_PREP.md yet: found by the re-measurement after the round design; the item's own rounds.

## What goes to the Owner in chat

- Once the avatar and upload memory is removed (round W1196), nothing imports chromadb, but pyproject.toml still declares it and onnxruntime comes with it (requirements.txt:16 and :92). May its direct declaration be dropped? RECOMMENDED: Yes, by the method W1141 used for streamlit, plotly and pandas under your ruling FU-1174: re-make the lock, export requirements.txt, and run a full suite on a fresh environment. Re-check test_w583 L5's opentelemetry pins (opentelemetry-api is also required by anthropic) and test_w907's sympy rule (sympy is also required by torch). Round W1230 is held on this answer.
- Two template descriptions in the design you approved, 'Default commercial company, limited liability.' and 'Registered charitable purpose; maximal charitable allocation.', read as legal facts beside the new sentence that no company is formed and nothing is registered. May they be reworded? RECOMMENDED: Yes. Keep the nine names and reword the two to say what each template models, for example 'A template modelled on a private limited company's profit split' and 'A template modelled on a charity's allocation: maximal charitable allocation', with a dated note in the economic model's section 2 that keeps the earlier words. Round W1216 lands the sentence without waiting; W1231 is held on this answer.
- Your ruling of 2026-11-22 sets the retention periods once the solicitor's engagement (FU-1817) has answered. Should that engagement also be asked, in writing, about retention and erasure? And will you approve a record of processing once it has answered? RECOMMENDED: Yes to both. W1192 widened FU-1817 to the licence, the title, the investment perimeter and the DPIA only. Widen it to retention periods and erasure, and approve the record once it answers. Rounds W1225 to W1228 go ahead either way, with every period reading 'not decided: the Owner's'.
- The ratified canvas says the price of generating an enterprise is 'credited against its first profit share' (block 5). On 2026-11-22 you ruled that the credit carries forward against later fees until it is used up. May block 5 gain a dated note saying so, with the earlier words kept? RECOMMENDED: Yes, as the fee and the payee were amended on 2026-11-22. Round W1232 is held on this answer. The draft cost model and the code's two sentences are corrected without waiting (W1193, W1204), because neither is a ratified text.
- The ratified business plan's Concept bullet already names each enterprise's own owner and does not mention the platform's 25% of profit, taken first (P5.16 clause 3, ruled 2026-10-12); the canvas gained the fee on the Owner's word on 2026-11-22, and the business plan's own header requires the Owner's word for any change. May the bullet gain the fee, as a dated amendment with the earlier words kept? RECOMMENDED: yes, its header then saying it has changed twice.

## Plans held or re-planned

- A3 (UNSOUND): re-planned, not held. The Owner retired the memory on 2026-11-22, and W1192 records this at P3.32. A3 (W1196) therefore removes MemoryV01 and its two writers instead of keeping the store in process and capped. Its two OWNER rows become one build row (the retirement) and one question in chat (chromadb's declaration); A3b (W1230) is HELD on that answer. Answered on the morning of 2026-11-22 (W1193c): no longer held on the Owner; still after W1196.
- The record round as cluster D planned it (UNSOUND): re-planned as W1193, because W1192 is the round that records the Owner's decisions. It registers no OWNER question row. It drops what W1192 already does: the canvas amendment, FU-1817's widening, workpack questions 6 and 7, and FU-1838 to FU-1840 with their lines. It adds the standing answer, the developer-account OWNER row, the build rows the 2026-11-22 rulings create, and the corrections W1192 leaves. Legs D and E are rewritten, and leg C recomputes the adjusted parts from the listed moves.
- D-CANVAS: superseded, not built. W1192 amends the canvas on the Owner's word and gives the vision's section 12 and the economic model's section 4 dated notes (the business plan is not amended); the cluster D refuter read this as still to do. The residue, block 5's 'credited against its first profit share', goes to the Owner in chat, with CANVAS-CREDIT (W1232) HELD on the answer. Answered on the morning of 2026-11-22 (W1193c): on the Owner's word the business plan's Concept bullet gained a dated note, and W1193c made the canvas's credit note, so W1232 is not built.
- B5 as planned built only the Chief, against the Owner's P4.2 ruling of 2026-11-22. It is split into B5a (W1218, the Chief) and B5b (W1219, the Board and the entity's own budget figure). Neither is held.
- Three planned OWNER rows are not registered. B3's and B7's are already answered by the rulings of 2026-11-22. C5's becomes a question in chat, with C5b (W1231) HELD on the answer. Answered on the morning of 2026-11-22 (W1193c): no longer held on the Owner; still after W1216.
- HELD on the Owner: A3b (W1230), C5b (W1231) and CANVAS-CREDIT (W1232), each built only after its answer. If the Owner answers sooner, a held round may take an earlier number, provided its files do not collide with the rounds around it. Answered on the morning of 2026-11-22 (W1193c): none is held on the Owner now; W1230 still follows W1196 and W1231 W1216, and W1232 is not built (W1193c made the note).

## Completeness

- Gaps with no round: none. All 25 gaps, the 6 new v40 gaps and the law.py defect each have a round. Gap 9's larger build (start rows) is not proposed, deliberately. Gap 18 is folded into W1223 by the lead. Gap 17 is built as the Owner ruled it (W1215).
- Corrections placed nowhere: none.
  - 1, 2, 4, 5, 10 (plan half) and 11: W1193.
  - 3: W1200.
  - 6 and 7: W1214.
  - 8: W1197.
  - 9: W1196.
  - 10 (code half): W1207.
  - 12: W1201.
  - 13: W1192, with block 5's credit residue in W1232 (HELD). Answered on the morning of 2026-11-22 (W1193c): W1193c made the note, so W1232 is not built.
  - 14: W1192 (FU-1817 and workpack questions 6 and 7) and W1193 (the brand screen's LICENSE quote).
  - 15: W1229.
  - 16: W1216.
  - 17: W1200.
  - 18: W1192 (FU-1838, FU-1839) and W1193 (the developer account).
  - 19: fixed by W1190.
  REMAINING_WORK_MEASURED.md:41 ('No such instrument exists') is left for the next re-measurement, as test_w787's docstring requires.
- Rows with no closing round in this schedule:
  - the unlocked-write class census (P5.10);
  - the local platform's CORS default (P4.1). A round must keep every localhost origin working, including Vite's proxied 5173;
  - the DPIA draft (P5.8's own rounds);
  - the developer account (the Owner's act). Its follow-on, calling the two content paths once with real credentials, has no round.
  W1191's FU-1834 (a torn users.json is replaced at boot) has no round either. W1198 refuses a torn store, but the boot still replaces it, and W1206's matcher cannot see core.py's except-default loader. A P4.1 round beside W1206 should close it before anyone else signs in.
- Proposals in the assessment's section-35 inputs (a session work file, not in the tree)' integration list that no gap or round carries:
  - P5.2's sale path: price_of has no caller that sells.
  - A founder's acceptance of the opening by version hash (P5.18 clause 2's approval).
  - A seeded purpose, instead of 'commercialise', for non-distributing forms (P5.1).
  - The agent-threat classes and three facts for the outside review (P4.5): attempt counts are per process; keys are re-checked per request; Change Control has no revocation path.
  Insights with no row:
  - no test pins the Dockerfile's single uvicorn worker;
  - tiers.machine() reads host memory inside a capped container;
  - the Owner's second Care calibration run should record the runtime's own load and evaluation durations.
  v40 insight 9's two unreached constant-figure modules (agentic_core/mjm/self_reflection_engine.py and agentic_core/simulation/nanophotonics.py) are not in the defect ledger; W1229 can add them as ledger entries.
- Files that several rounds touch, and the order this schedule gives them, so that no two collide:
  - resource_fabric.py: W1197, W1209, W1210, W1212, W1213.
  - ResourceFabric.tsx: W1209, W1212, W1214. B3 must re-read A2's chip and keep test_w756's 200-character window.
  - native_ai.py: W1203, then W1210.
  - vsb.py: W1204, W1205, W1210, W1216, W1218, W1219.
  - board.py: W1210, W1218.
  - work_budget.py: W1212, W1214, W1215.
  - capital_fund.py: W1214, W1215, W1220.
  - organism_status.py: W1214, W1220.
  - economy.py: W1216, W1220.
  - metabolism.py: W1204, W1215.
  - homeostasis.py: W1197, W1215.
  - quality.py: W1197, W1205.
  - qms.py: W1205, W1206.
  - gateway.py: W1210, W1211.
  - avatars/api.py: W1196, W1210.
  - v138/ceo.py: W1196, W1211.
  - products.py: W1210, W1222.
  - change_control.py: W1220, W1222.
  - genesis.py and GenesisJourney.*: W1216, then W1217, which recaptures again.
  - VSBEconomy.tsx: W1214, W1216.
  - VSBCockpit.tsx and its fixtures: W1214, W1216, W1218, W1219. W1218 recaptures the chief fixture after W1216.
  - law.py and specialist.py: W1194, W1195.
  - DEPLOYMENT.md: W1198, W1202, W1214.
  - PRODUCTION_HARDENING_BRIEF.md: W1214, W1223, W1225-W1228. None of these may name a row it closes (test_w912).
  - COST_MODEL.md: W1192, W1193, W1223.
  - NAME_AND_BRAND_SCREEN.md: W1193, W1201.
  - FIRST_OFFER_CANDIDATES.md: W1192, W1201.
  - RESUME: W1192, W1193, W1199.
  - README.md: W1193 (status and count), plus W1218, W1219 and W1222 for route figures; each runs readme_figures --fix last.
  - docs/READ_CENSUS.json: W1220-W1222.
  - retention.py and RETENTION_REGISTER.json: W1225-W1228.
  Every bundle (W1200, W1201, W1204, W1207) was checked disjoint in code and page files.
- Couplings the designs leave for later rounds:
  - Once C2 lands (W1201), any round that closes a row named on a business document's 'Between' line must restate that line: FU-417, FU-1072 and FU-1086 on the strategy map.
  - Every round that closes a row lists docs/FOLLOWUPS.json, docs/FABLE_DELIVERY_PROMPT.md and docs/WORKSTATION_IDBO_LIVING_PLAN.md, and runs test_w462 and test_w469.
  - Every hand-slotted row needs slot_source, or test_w469's route-agreement leg (:16035-16062) fails.
  - W1232 changes test_w725's and test_w1192's 'Changed twice since' pins on purpose.
- Bundler findings against the planners and refuters:
  - W1192 already does D-CANVAS and most of correction 14.
  - .env.example:40 makes CORS_ORIGINS equal its own inline comment under python-dotenv; W1202 moves the comment.
  - The cluster D refuter's 'W1191 registers no W729 row' is refuted by the working tree (FU-1837).
  - D-TERMS (the interim README sentence from the accepted Q6 option) and D-CREDIT (the code's two credit sentences) had no design in any cluster. They are added at W1204.

## The clusters as their planners summarised them

The four clusters as their planners summarised them. Printed as written, before the lead's rulings and the Owner's decisions of 2026-11-22. Where they differ from the schedule, a round's heading or "Plans held or re-planned", those win (among them A3, the OWNER rows, gap 17 now W1215, the return measurement now W1224, and the standing answer, which W1193 recorded).

### Cluster A: Code that says what it does not do (P3.30, P3.32)

**Summary:** Cluster A covers code or plan text that claims something the code does not do. It holds seven gaps, two v40 gaps, one merged insight and four corrections. Everything was checked at 89c25eed (W1190) against the tree. For chromadb 1.5.5 the installed source was read in the W1147 scratch venv (a scratch copy outside the tree), because no interpreter on PATH has chromadb.

All seven gaps hold except the runtime_framework half of gap 23. That half is refuted: products/business_incubator/sdk/business_incubator.py:10 imports runtime_framework and test_w597_p324 imports that SDK. The lead ruling binds it: delete simplicial_repair, leave runtime_framework, record _interrupt_agent as latent, and do this round last.

Two more cases of gap 8's class were found while checking:
- the QMS reads its store tolerantly into self._state and writes it back whole (qms.py:87-100);
- five more functions do a strict read and then write the store with no lock around the write (an AST census).

The plan is twelve rounds after W1192, each one commit with its own guard:
- A1: the preview records nothing.
- A2: the capacity chip says how a composition runs. It carries the observed-concurrency leg the merged insight asked for.
- A3: memory_v01 fetches no model and says it is held in this process only.
- A4: the archive's wording on embeddings.
- A5: the DCMS becomes an append-only ledger, read whole or refused.
- A6: the class guard is widened to the attribute door, and the QMS write base is fixed.
- A7: every duration is read from the monotonic clock.
- A8: an abandoned attempt is recorded once, as abandoned.
- A9: three sentences about run evidence are restated.
- A10: the completed-run write takes the history's lock.
- A11: licence and administrator at promotion, bundled. One guard tests both, and its files are touched by no other round.
- A12: simplicial_repair is deleted, last.

W1192 registers 14 build rows and 2 OWNER rows. Thirteen build rows are closed by A1-A12; the A10 class row stays open. W1192 also writes dated CORRECTED notes at P2.13, P3.22 and P3.32, and register-text corrections on FU-282, FU-1130 and FU-1087. Plan line numbers are at 89c25eed and must be found again by text after W1191's inserts.

**Not proposed:**

- Start rows for composition runs, the M crash-evidence build of gap 9: On a one-person platform the person sees their own run fail. A9 restates the three sentences that over-claim. If crash evidence is wanted later, build it once at run_span (which wraps composition, swarm, deliverable, transformation and AI-call runs), guarded with a planted unfinished row and a clock past the ceiling rather than a killed subprocess, because the suite already has unexplained stalls (FU-301).
- A persistent chromadb client at CHROMA_DB_PATH (store_paths.py:37): It would keep avatar conversations and uploaded text across restarts before sign-in, against the Owner's split of 2026-10-12, with no retention period. It would also widen the erasure surface.
- An approved embedding model for memory_v01 (cluster question option a): Downloading a model is the Owner's, and it is ruled off for now (FU-1130, 2026-11-06). P3.32's boundary (2026-10-10) holds embeddings off, and nothing in production reads the store.
- Archiving agentic_core/governance/runtime_framework.py, as the synthesis sketched: Refuted, and the lead ruling binds it: products/business_incubator/sdk/business_incubator.py:10 imports it and test_w597_p324 imports that SDK. A12 records _interrupt_agent as latent instead.
- Fixing the other three RECORDED, LATENT functions (run_evolution_cycle, get_aggregate_accuracy, network/planetary.py): The lead ruling scoped the row to simplicial_repair. They stay recorded with their rule.
- Bundling the DCMS rebuild (A5) with FU-1297, the genome ledger: Each is M. The genome ledger also needs a chain check that the DCMS does not, and A5 shares vbs/quality.py with A1. FU-1297 can follow with the same append-and-replay pattern.
- Batching A2 with FU-1826, FU-1828 and FU-1829 in ResourceFabric.tsx: They hold different properties (a form row's provenance; a badge), and P5.10 clause 8 batches tier-3 rows while A2 is a misleading-surface row. They are sequenced, not batched.
- The research-only-lead match and the licence-hash hold at promotion, from the v40 sketch: Dropped, as the refuter showed: the only research-only lead has runtime_tag None (model_resource.py:477-478), and nothing in the tree shows a licence changing under the same digest.
- An administrator override of the licence refusal: It would be a policy decision, so it is put to the Owner as a question. The OLLAMA_MODEL fallback already lets the Owner serve any build.
- A separate row for the merged insight (the cascade guard holds only the reported grant): Folded into A2's leg 5. A2's restated tooltip claims the cascade's concurrency is held by its grant, so the round that writes the claim carries the guard that observes it.
- Clamping the stored raw duration_ms in record_outcome (operational_excellence.py:234): After A7 the platform's own sites cannot produce a negative duration. A caller's /record figure is its own claim, already stamped reported_by caller (W672) and never spent.
- A P4.5 row for memory over sustained use: A5 measures and bounds the DCMS's resident size, and FU-1297 covers the genome ledger. A sustained-use soak on the release image belongs to P4.5's own pre-flight when the Owner takes the deploy (2026-11-20: whenever it suits).
- Building the five other unlocked read-modify-writes in this cluster: They are registered as one P5.10 class row with the census, and not built here. Each needs reading first: a caller may hold the lock, and swarm.cascade_orchestration writes several stores, so lock order needs checking. They are outside this cluster's gaps.
- Retiring homeostasis.project() after A2 removes its only caller: It computes what it says and keeps its own tests (test_w742 legs 2 and 7, test_w756). Retiring it is not needed for any claim to be true.
- Deciding to retire memory_v01, or to drop chromadb and onnxruntime: Both are do-X-or-Y fixes, which M-EXEC-07 makes the Owner's. W1192 registers them as OWNER rows with recommendations.

**The refuter's verdict on the cluster:** PLAN_NEEDS_FIXES

**What the refuter checked:** Read only, at 89c25eed (clean tree; W1191 not landed). Read the round design's cluster A file (a session work file, not in the tree) in full: 7 gaps with both refuter lenses, 4 corrections, 2 v40 gaps, merged evidence, the lead ruling on gap 23, and both Owner-decision notes (2026-11-21 late evening; 2026-11-22 just after 00:52 UTC). Checked every state claim of A1-A12 at file:line in agentic_core (resource_fabric.py, quality.py, qms.py, dcms.py, immune.py, ueg.py, homeostasis.py, swarm.py, orchestrator.py, gateway.py, operational_excellence.py, membrane.py, work_budget.py, memory_v01.py, avatars/api.py, ingestion/api.py, archive.py, native_ai.py, model_resource.py, defense.py, runtime_framework.py, vsb.py, vbs_systems.py, agent_hub.py, integration_surface.py, heartbeat.py, auth/core.py, config.py store_lock), the pages and fixtures (ResourceFabric.tsx/.test.tsx/.fixture.json, HorizonCompanion.*, ArchiveSearchPanel.*, OperationalExcellence.tsx, OrganismDashboard.test.tsx, NativeAI.fixture.json, lib/api.ts) and products/business_incubator/sdk. Read chromadb 1.5.5's source in the round runner's own venv (the round runner's own environment), not only the W1147 venv: client.py:279-287, types.py:947-960, onnx_mini_lm_l6_v2.py:36-43 and :258-310, config.py:159, posthog capture is pass. Read register rows FU-1108, FU-1130, FU-282, FU-1087, FU-395, FU-298, FU-1297, FU-1277, FU-1174, FU-604, FU-321, FU-990, FU-1826/1828/1829, FU-1114, FU-596, FU-1103, FU-1121, FU-902, the retired_areas, plan_followups.py's high-row routing (:495-535) and scripts/followups.py's subcommands; docs/LITERAL_OUTCOMES.json; plan P3.22, P3.30, P3.31, P3.32, P4.1, P4.5, P5.10, S18.1-S18.6 and the RECORDED, LATENT list (:915-917); section 33 (2201-2321). Grepped integration_tests/test_mvp_spine.py and the vitest files for every string each round changes and read each pinning test (test_resource_compose*, test_compliance_sealed, test_w449, test_w506_p27_layers, test_w742, test_w756, test_p330_r6, test_w917, test_tamper_evidence, test_vbs_living_systems, test_w440, test_w534, test_w577, test_w583, test_two_authenticated_users_memory_isolated, test_w885, test_w507_fu167, test_w552, test_w599_p322, test_w978, test_w1118, test_w853, test_w495 leg, test_w505_p26, test_w841, test_w966 literal-outcome screen). No test suite, docker or network was run.

**Rounds the refuter said were missing** (the lead's schedule above answers each):

- Conditional dependency round after the A3 retirement. Once memory_v01 is retired nothing imports chromadb, but pyproject.toml:18 still declares it and onnxruntime comes with it (requirements.txt:16 and :92). The Owner's 2026-11-22 answers do not say whether the declaration goes, and FU-1174 made such removals the Owner's. The lead must decide whether Q2 ('retired ... no outside download') covers it. If it does, a round by W1141's method follows A3: a fresh-venv full suite, with test_w583 L5's opentelemetry pins (opentelemetry-api is also required by anthropic) and test_w907's sympy rule re-checked. If it does not, the question goes to the lead, not into the register as an OWNER row.

### Cluster B: Before anyone else signs in: tenancy, retention, release shape, the work budget switch (P4.1, P4.2, P4.5, P2.41)

**Summary:** Cluster B (P4.1, P4.2, P4.5, P2.41) closes in nine rounds, B1 to B9, about twelve rounds of work, all after W1191 and the record round W1192. All of it was checked at HEAD 89c25eed. W1191 is not in the tree yet. Its shape was read from the session's own scratch copy (a scratch copy outside the tree): it adds FU-1833 to FU-1836, set_password.py, and the startup script's auth-enabled and CORS_ORIGINS. Every W1191-dependent verdict below is marked ABSENT at HEAD.

The rounds, in recommended order:
- B1 (M, P4.1): an Origin and Host check keyed to the explicit CORS_ORIGINS that W1191 passes. It covers writes, the stream socket and DNS rebinding through the tunnel, and closes FU-1835.
- B2 (S, P4.1): a remove_account command over SSH on set_password's pattern. It reads the store strictly before core is imported and re-reads it under the lock. Closes FU-1836.
- B3 (M, P4.5 and P2.41): the work budget says its figure is the platform's and lists every reader of it, beside _CONSUMERS and not inside it. One guard ties the brief's limits line and the guide's settings table to the code's defaults, readers and the startup script's settings. It bundles gap 13 and v40 gap 1. W1192 writes corrections 6 and 7; B3 pins them.
- B4 (S, P5.1): the eight entity routes with a second path parameter. They are driven as a second person against real seeded state: generated pages, a specialist, a gated stage. Answers are compared by status and body, and each route is named with its test.
- B5 (M, P4.2): the thin design. A new POST /api/v1/vsb/{vsb_id}/chief/instruct behind _require_vsb_access, grounded in the entity's own record, never the platform's vision. The apex Board and ratifications stay admin-only. The cockpit and its rendered test move to the new route. No Owner question is put, because the vision's §13 and §18 spine 3 already rule it.
- B6 (M, P4.5): a load measurement under the release machine's caps. It is a committed raw record and a report whose figures the guard recomputes. It is a proxy and gates no deploy. Gap 18's establishment cost is folded in by the lead ruling.
- B7 (M, P4.2): a retention register. Completeness comes from an AST walk of every store; reach is measured by a canary drive with sign-in on. Every period reads 'not decided: the Owner's'.
- B8 (L, P4.2): an administrator's erasure of one made-up person, driven end to end and read back. No entity is deleted, the UEG chain still verifies, and a second person is untouched.
- B9 (S, P4.5): a read-only history mode of the privacy screen, credentials only. It says where a shallow walk stopped.

Gap 17's build is refuted by the lead ruling. It becomes the widened Owner question 3, kept to a recommendation of the platform figure, plus a plan line. Two Owner rows go to W1192: the energy readers' figure, and retention with the FU-1817 widening. Correction 5 lands in W1192, agreed with cluster C's gap-20 round.

**Not proposed:**

- A per-entity admission reader for the work budget (gap 17's build): Lead ruling: no build. Every P4 step runs with the switch off. Until the invited stage every entity is the Owner's. An entity's share divides an assumed capacity, the reason the Owner accepted for births on 2026-11-19 (FU-1166). It becomes the widened Owner question 3, kept as a recommendation of the platform figure, plus one plan line saying FU-1116 closed on births alone.
- A per-stage spend row on P5.1 (gap 18): Lead ruling: no P5.1 row. Tokens are booked only to the platform total (work_budget.py:156-160), every stage before establishment has no entity id, and P5.1's ACCEPT, an Owner ruling of 2026-09-27, asks for what was produced and what served it, not for spend. The establishment's seconds, CPU seconds and peak memory are measured in B6. Amending P5.1's ACCEPT is the Owner's, and no Owner row is raised because nothing needs it now.
- Re-mounting the whole board router behind get_current_user (gap 4's original sketch), and an owner-scoped read of an entity's work-budget figure: The thinner entity-scoped route keeps test_w505_p26, the apex Board, scope 'workstation' and ratifications administrator-only without re-checking every apex handler. No founder page reads an entity's budget figure, which is reported, not enforced, behind an off switch, so a route for it would have no reader.
- A route by which a signed-in person deletes their own data: P4.2 opens self-serve only after the invited stage. For the invited stage's handful of named people an administrator's erasure (B8) is proportionate. A self-serve deletion route belongs before self-serve sign-up.
- Setting any retention period, or ruling who holds an erased person's entity: Both are the Owner's: brief part 8 marks them [owner decision], and S18.6 keeps the record. B7 and B8 write 'not decided: the Owner's' and register the OWNER row.
- Adding WORKSTATION_WORK_BUDGET to the plan's OWNER-GATED list, or giving the startup script a metadata key for it or for SELF_SERVE_SIGNUP_ENABLED: The OWNER-GATED list (FABLE:909-913) is the Owner's own text. S18.1 already ships the budget inert and no step of P4's order flips it. Self-serve comes after the invited stage. The documents say each switch is off and where it would be set; nothing prepares a switch that is not due.
- Changing the local platform's CORS default ('*') inside B1: It would change the Owner's own machine (docker compose, the Vite proxy, any LAN use). It is registered as its own P4.1 row with the mechanism stated, for a round that can keep localhost origins working.
- The OWNER row asking the Owner to revoke W729's values, or confirm they are dead, with the date beside the Stripe line: Cluster D lists it for W1192 (the v40 gap's lead note). Cluster B designs only the read-only history mode (B9), whose full-clone run that row should name as its first step.
- FU-1834 (a torn users.json replaced at boot): It is W1191's own row and not in this cluster's list. B2 is built to be safe without it, and its guide sentence tells the Owner not to restart on a torn store.
- Measuring on the target machine: The deploy, the account and the machine are the Owner's. B6 is a labelled proxy, and part 7's done line stays open until the Owner's machine runs it.

**The refuter's verdict on the cluster:** PLAN_NEEDS_FIXES

**What the refuter checked:** Read at HEAD 89c25eed. W1191 is not landed. Also read: W1191's scratch (a scratch copy outside the tree); W1192's scratch (W1192's staged apply (a session work file, not in the tree), W1192's notes (a session work file, not in the tree), W1192's message (a session work file, not in the tree)); the round design's cluster B file (a session work file, not in the tree) with the Owner's decisions of 2026-11-21 23:59 and 2026-11-22; the lead's adjudication of the v44 gaps (a session work file, not in the tree); the assessment's section-35 inputs (a session work file, not in the tree); cluster A's gaps 1, 9 and 15.

Every state claim was re-read in code: app_mvp.py (CORS at :37-43, _horizon_observe at :134, mounts at :402/:440/:519/:535, biometrics at :741-753, socket at :875-912); auth/core.py; config.py; heartbeat.py; work_budget.py; metabolism.py; capital_fund.py; organism_status.py; biobus.py; board.py; vsb.py; entity_specialists.py; gateway.py (limiter at :447/:710); ai/logger.py; projects/api.py; marketplace.py; privacy_exposure.py; scripts/privacy_check.py; startup.sh; deploy/drill.sh; Dockerfile; .env.example; render.yaml; vite.config.js; conftest.py. Also read the installed python-dotenv parser (dist-packages/dotenv/parser.py:24, :125-141).

Spine tests read: w1075, w1097, w661, w742, w900-w902, w909, w912, w962, w1112, w732, w703, plus the _w703_faults helper. Vitest files read: VSBEconomy, OrganismDashboard, Introspection, HeartbeatMonitor. Register rows read: FU-1116, FU-1166, FU-1262, FU-1817, FU-1165. Plan read: P4.1-P4.6, S18.1, S18.6, the OWNER-GATED list and the W743 correction. Also read section 33. A static route scan confirmed exactly eight mixed-parameter entity routes.

Cross-cutting: W1192 is the round that records the Owner's decisions. Its rows are FU-1838 to FU-1840, and it writes rulings at S18.1, P3.32 and P4.2. Section 35's round is W1193. W1191 also registers FU-1837, the W729 row. So everything the plan gives to 'the record round W1192' belongs to W1193, under these rules: no OWNER question rows; build rows cite the ruling; ids start after FU-1840 and the other clusters' rows. W1192 does not write corrections 6 or 7.

**Rounds the refuter said were missing** (the lead's schedule above answers each):

- A round for the S18.1 ruling of 2026-11-22. Once the throttle is on and a second person runs work, admission and every reader of the energy figure read each run's own chain (platform, owner, VSB).
  - Inert behind WORKSTATION_WORK_BUDGET, and built before the invited stage.
  - A second person is detected from the budget's own booking: a second owner with booked spend.
  - A run that names no owner reads the platform total and says 'not attributed'.
  - Every reading says whose figure it is.
  Section 35's integration notes already list 'admission by the run's own chain if the Owner chooses it' as a missing P3.30 truth row (the assessment's section-35 inputs (a session work file, not in the tree)). The lead's 'no build' on gap 17 predates the Owner's choice of option (c). Size M, P3.30 or P2.41.
- Unless B5 is widened: the founder's read of their entity's Board and of its own work-budget figure, each with a page and a second-person leg, as the P4.2 ruling of 2026-11-22 requires. Size M, P4.2.

### Cluster C: Phase 5 items: census, legal form, journey, guards, the plan line, and the law.py reserved-instrument defect (P5.1, P5.10, P5.18, P5.22, P2.40)

**Summary:** Cluster C has seven gaps: 10 (the read census), 11 (the legal-form sentence), 19 (two entities from one journey), 20 (business documents name closed rows as open), 21 (PLAN NOW's Next line), 24 (the optimiser's queue disclosure is unguarded) and 25 (the money pattern only sees the currency first). It also has the law.py reserved-instrument defect (P5.18 clause 4). Both refuters upheld every gap and no lead ruling exists. The cluster file has no v40_new_gaps entries and an empty owner_questions list. Its one v40_merged_evidence item (GET /api/v1/economy/board-pack advances the ATP simulator) is folded into the census round.

I checked every claim against HEAD 89c25eed. The refuters' line corrections hold: READING_METHODS is at auth/core.py:229, P5.10 clause 1 at FABLE:7032-7034, P5.18 clause 1 at 7419-7421, P2.40 and P2.41 at 4800-4803, and the map's stale rows at LIVING_STRATEGY_MAP.md:77-78 and 90-92 (plus FU-1086 at 64-65, labelled [owner decision] though it is slotted P5.22).

Findings this pass adds, which no refuter named:
(1) GET /api/v1/fund/status also advances the simulator, through _organism_posture (capital_fund.py:260 and :359). A screen of GET handler bodies finds only the other five, so the census has to call routes, not read their source.
(2) GET /api/v1/cca/impact/{id} also runs gateway.query_meta and fires a nervous signal (change_control.py:2507-2513).
(3) The clerk (POST /api/v1/law/matter/assemble) labels an artefact with any template id. That is a second door, given to the screen round.
(4) The approved design table (VSB_ECONOMIC_LEGAL_MODEL.md:40 and :46, approved 2026-06-20/21) carries 'Company, limited liability' and 'Registered charitable purpose'. This settles the refuters' disagreement: rewording the two descriptions is the Owner's, and it becomes an OWNER row.
(5) After W1191, P4.1 carries open rows (FU-1834 and two more). A cost-model rule keyed on the item alone would therefore pass the stale 'rows are open' sentence, so the new rule requires the open rows to be named.
(6) The coverage register forbids a test on a route_only row (scripts/coverage_register.py), so clause 4's row is route_only and its guard is named in the plan.
(7) P3.30's own text does not record that ACCEPT (5) waits on the final audit; only REMAINING_WORK_MEASURED.md:86 and :89 do.
(8) test_w920 pins an exact fault list and test_w747 pins FU-1086's title (cluster D's retitle).

Nine rounds follow W1192, in this order:
- C1: the law id door.
- C2: the business-document guard (gaps 20 and 25, one function).
- C3: the plan-line hold.
- C4: the optimiser guard.
- C5: the legal-form sentence.
- C6: one entity per journey.
- C7: the law free-text screen and the clerk.
- C8: the read census. It lands after cluster A's compose-preview seal round.
- C9: the two reads that run a model.
That is about 10 rounds in all.

**Not proposed:**

- Rewording the 'ltd' and 'charity' template descriptions, or any of the nine names.: They restate the table the Owner approved (VSB_ECONOMIC_LEGAL_MODEL.md:3, :40, :46). The rewording is put to the Owner as an OWNER row, and C5 only adds the sentence beside them.
- Flipping organism_context's default to advance_atp=False.: It would change what every run advances (heartbeat, CCA review, chief instruct, the fabric's declared reads). W694 chose to declare the fabric reads' cost, and the census catches each read site anyway.
- Reopening FU-912 or FU-1108.: Their own sites still hold (test_w694, test_w742 leg 8). The return of the class is recorded as the P5.10 census row, as clause 1 asks.
- Choosing previews by a docstring regex.: 'simulate' also matches POST /vote, /ems/efficiency, /reactor/run and /twin/simulate, which are meant to write. Instead there is a declared list plus a completeness screen that requires every 'Nothing is saved' POST to be declared.
- An allow-list entry for the membrane.: membrane.py:45 observes only POST, PUT, PATCH and DELETE, so a GET records nothing.
- Changing the Transformation Dashboard's Next line or the pace block's next-item projection.: Correction 17 is about the generated document block. The page's line is pinned by TransformationDashboard.test.tsx:184 and test_w1107, so a page round can follow if wanted.
- A 200 replay of the first entity for a repeated establish.: One answer shape was required. A 409 naming the first entity keeps test_w668's 'the record wins' blind meaningful, which a replay would make vacuous.
- Touching duplicate entities already established on the Owner's machine.: An entity is never deleted. The round only stops new duplicates.
- The hardening brief's document-wide 'every named row is open' rule for all business documents.: Other documents cite done rows as evidence (METRICS_MEASURED.md:44, FOUNDERS_GUIDE.md:83), and BUSINESS_PLAN.md:133 is Owner-ratified.
- Editing BUSINESS_PLAN.md or BUSINESS_MODEL_CANVAS.md.: Both were ratified by the Owner on 2026-10-13, and a change needs the Owner's word.
- A second constant with NOT_AN_ENTITY's substance.: One wording, in entities.py and reused by agreements.py, is the plan's rule for load-bearing sentences.
- A NEW plan item for the PLAN NOW hold.: An S renderer change rides P5.22 as a row.
- Retitling FU-1086.: That is cluster D's correction 3, in a round that edits test_w747 (67104 pins the title). C2 and W1192 only describe the row in agreeing words.
- Putting the free-text screen into C1.: C1 closes the id door, which is the defect as named. The screen needs its labelled phrasings (W580), so it is its own row and round, C7.
- Reopening P5.6 or P5.7.: Both are DONE. Their rules are strengthened at the mechanism, which is C2, and the items stay done.

**The refuter's verdict on the cluster:** PLAN_NEEDS_FIXES

**What the refuter checked:** Read only, at HEAD 89c25eed (W1191 has not landed; git log shows W1190 at HEAD). I read the round design's cluster C file (a session work file, not in the tree) in full (7 gaps, both refuter lenses, 3 corrections, the law.py defect, the v40 board-pack evidence and the two owner-decision notes). I also read the parent's W1192 notes and apply script outside the tree, for sequencing only.

SEQUENCING CONFLICT, affecting every round. the round design's cluster C file (a session work file, not in the tree) owner_decisions_2026_11_22 says the Owner's 20 decisions are 'recorded by W1192 (before section 35's round W1193)'. the session's W1192's notes (a session work file, not in the tree), outside the tree, agrees: W1192 registers FU-1838..FU-1840 (OWNER rows). It edits COST_MODEL.md's gates section, adding two OWNER RULING 2026-11-22 bullets, so the P4.1 cell moves from :69 to :70. It also edits VSB_ECONOMIC_LEGAL_MODEL.md section 4, the canvas and the plan. It leaves 'the build rows these rulings create' and the next section to W1193. So the plan's record round is W1193, not W1192; every 'W1192 registers/restates' should read W1193; and C1-C9 start at W1194. The record round's -k should also take test_w962, test_w963 and test_w1192, because W1193 edits COST_MODEL.md after W1192's amendments.

Verified against the tree:
- law.py: 38-49, 51-81, 389-407, 409-424; specialist.py: 23, 28-39, 149-184.
- resource_fabric.py: 538 and _run_form 1128-1170, which returns e.status_code and detail.
- LawHub.tsx: 234-237 and 244. SOURCES.json rows lsa-2007-sch2 (with its not_read) and help-gov-find-legal-advice. GET /api/v1/law/help at law.py:615.
- scripts/coverage_register.py check() and COVERAGE_REGISTER.json: 84 rows, 30 Law.
- FU-1076 slot_source at FOLLOWUPS.json:21545. Statuses of FU-849, 1151, 1040, 1086, 1095, 417, 1072, 1010, 1061 and 603.
- _w703_faults: 64827-64898, with the row check at 64848 and money at 64872. test_w923 at 78566-78568. The map's 28-29, 43, 53-54, 64-65, 77-78 and 90-92. COST_MODEL.md:52 and :69.
- plan_followups.py: plan_items 198-231, plan_now 551-591, render_plan_now 1415-1480, route_row 494-540 and _route_matches 480-491. The register has 8 routes, all to P2.40; retired areas cover integration_tests and change_control.py.
- FABLE: 1123, 1133, 4800-4803, 6612-6622, 6712, 6800-6814, 7020-7053, 7412-7459.
- scheduler.py: 19-30, 53, 58. entities.py: 33 and 68. VSB model: 3, 40, 46. economy.py: 139-151, 456, 545-546, 2257, 2273. agreements.py: 55-57, also imported by assets.py:33/263. vsb.py: 2572 _read_view (a shallow copy), 3229-3235.
- genesis.py: 1267-1323, 1479-1518, 1772-1799, 1876-1878, 1908, 1997.
- GenesisJourney.tsx: 254/303/367/406 (refusalOf), 401-444, 784-791, 1121-1130. VSBEconomy.tsx: 360-386. VSBCockpit.tsx: 1390. VSBSpawnStudio.tsx: 536-539.
- The organism_context callers mapped to their routes: 386, 513 and 564 are GETs; 616 is the POST homeostasis; change_control 2492 is a GET; 1097/1690/1880 are a POST or helpers; board 1099 is a POST helper; capital_fund 260/303/359/616.
- products.py: 916-967. qep_intelligence.py: 451-459. membrane.py:45. app_mvp.py: 189-198. 313 @router.get decorators.
- Pins I grepped in test_mvp_spine.py: every /law/generate and /matter/assemble post; test_w714, w1170, w825, w996, w580, w1167, w1012, w1025, w1062, w1014, w1077, w651, w1107, w469, w786, w549, w1126, w1047, w924, w1080, w488, w694 and w742; and the fixtures under pages/enterprise and pages/synthesis.

Cross-cutting fix: every round that closes a row re-renders both plan documents (scripts/followups.py writes PROMPT and LIVING, 673-683). Each explicit file list therefore needs docs/FOLLOWUPS.json, docs/FABLE_DELIVERY_PROMPT.md and docs/WORKSTATION_IDBO_LIVING_PLAN.md, and each -k needs test_w469. C2, C4, C6 and C9 omit them; C1, C5, C7 and C8 omit the living plan. Every new row slotted by hand (P5.18, P5.10, P5.22, P5.1, P4.1, all outside the 8 routes) needs slot_source, or test_w469's route-agreement leg (16035-16062) fails.

**Rounds the refuter said were missing** (the lead's schedule above answers each):

- Every gap has a round: 10 (C8, C9), 11 (C5), 19 (C6), 20 and 25 (C2), 21 (C3), 24 (C4), and the law.py defect (C1, C7). Corrections 4, 16 and 17 and the board-pack evidence are placed.
- Not covered by any round, and needed for the bar: (a) a checked guard field for route_only/excluded coverage rows, so that P5.18's ACCEPT 'a row naming the test' can be met for clause 4 (fold into C1); (b) the rest of the form surfaces: the Genesis stream's 'Living Economy Initialised' event (genesis.py:1876-1878), the establish, waterfall and cycle answers' entity_name, and the eight further fixtures (fold into C5, or a C5b if C5 runs long).
- Not a missing round but a misnumbered one: the plan's record round is W1193, not W1192, because W1192 is the Owner's twenty-decision round. Its -k also needs test_w962, test_w963 and test_w1192, and its hand-slotted rows need slot_source.

### Cluster D: Owner rows, document corrections and the record round W1192

**Summary:** Cluster D covers four Owner rows, one P3.30 row, one row W1192 builds and closes, and eight corrections. The four Owner rows are: the ratified canvas names no 25% fee and gives the split's first 20 to the Owner; nothing owns the project's own licence and title; P5.6's deferred measures and the canvas's three first tests; and a named scholar. The P3.30 row is that the first-offer papers present a free Domain tool as paid for. The row W1192 builds and closes is the plan's round protocol, which still names docs/AUTONOMOUS_PROGRESS.md as the round record. All four gaps and both v40 gaps survived both refuters, and no lead ruling changes them.

W1192, the record round, lands first, after W1191. It writes section 35 in section 33's structure. It registers cluster D's six rows (not the W729 credentials row, which W1191 registers by the Owner's late-evening decision). It adds the four Owner rows to the plan's Owner list and to the local notes' 'Still yours'. It applies the unpinned corrections: README status and count, the workpack's fee date, the licence facts as solicitor questions 6 and 7, the vision's FU-448 sentence, and the round-protocol text. Two traps it must respect: section 35 may hold no numbered six-cell table and may backtick no upload or bare file name (test_w711 and test_w1133); and the notes' 'Updated' header pin in test_w1190 changes on purpose.

Four small rounds follow:
- D-FU1086 retitles FU-1086 to what remains and adds P5.22's dated BUILT line. It is pinned by test_w747:67104 and :67126, and the BUILT line may name no FU id but FU-1086.
- D-FIRST-OFFER re-states the first-offer papers as use, with the tool free, before FU-1818's interviews. It is pinned by test_w913:77769 and test_w1151:94073, uses narrow assertions rather than a new _w703_faults rule, and adds no digit to the willingness-to-pay section.
- D-SCHOLAR-REQUEST drafts the request letter for the Owner to send. It is preparation only.
- D-CANVAS is gated on the Owner's answer and is pinned by test_w725:65907.

The measurement build that gap 12 sketched is not designed here: it is the Owner's to schedule after sign-in. Of cluster D's questions, four become open OWNER rows. Six go to the Owner in chat. The v40 review question is reported as already answered: this assessment read the v40 body for what the supplements do not restate.

**Not proposed:**

- Editing LICENSE or CONTRIBUTING.md: The grant is published and legal in kind. A solicitor answers who holds the copyright. W1192 only records the facts as questions.
- Writing the licence and investment scope into FU-1817's why on a round's word: FU-1817 records an accepted recommendation, and its one later addition came by the Owner's ruling of 2026-11-21. The scope is put to the Owner as its own row.
- Amending the canvas, the business plan, the vision's section 12 or VSB_ECONOMIC_LEGAL_MODEL.md before the Owner's answer: They are ratified or approved texts: 'a change ... needs the Owner's word'. D-CANVAS waits.
- Building the return measurement (a sign-in day and a tool use per person) now: It keeps something about a person, which the 2026-10-12 ruling builds after sign-in. Sign-in is on only on the Owner's deployed machine, and the invited stage waits on FU-1817. When the Owner schedules it, it counts across people only and shows no figure about one person (2026-09-30: never grade a person).
- A class guard requiring a row for every 'until the Owner engages or names' sentence: The deferral class has one member besides the scholar (P5.6's sentence and its copy). Widening it would demand a row for the safeguarding lead behind a children's gate the Owner ruled closed.
- A broad 'paid Domain' rule inside _w703_faults: It collides with P5.7's required willingness-to-pay questions and with cluster C's P5.10 edits of the same function. D-FIRST-OFFER uses narrow assertions with negative controls instead.
- Adding an interview question on taking an idea on to an entity: The Owner accepted the interviews 'using the drafted scripts' (FU-1818). The question is offered in chat instead.
- Keying the scholar row's close on the roster store: The roster is in the data store and is empty in every CI run, so the row could never be told apart from a real engagement. It closes only on a dated plan record or a ruling.
- A git-log guard for the progress log ('the newest W in git log'): CI checkouts and this clone are shallow (root a27f491b), and merge commits carry no W. The guard reads the log's own headings.
- Re-dating README.md:157's 'up to 2026-10-03', or giving the log a date: The date comes from the shallow-clone root. Correct it only from a full clone, together with test_w1130's pin.
- Registering the W729 credentials row in W1192: By the Owner's decision of 2026-11-21 late evening, W1191 registers it, with its list and notes lines. The read-only history scan is cluster B's P4.5 row.
- A valuation note, ARR multiples, a dilution table or investor material: There is no company, customer, revenue or deploy. The ruled model has no recurring revenue. The business guard refuses unsourced money figures (test_mvp_spine.py:64866-64873), and the plan's constraint refuses template valuations (FABLE:7749-7753). Owner question n=12 recommends none.
- The fee's form in the scholar request: It is a condition before real money, and real money is a dated section 18 boundary (P4.6).
- Writing the 'digital mitochondria' standing answer now: It is the Owner's choice (question n=1). If accepted, a later round records it beside section 33.
- Editing REMAINING_WORK_MEASURED.md piecemeal: It is a dated measurement that is re-measured, not edited (test_w787's docstring).
- Numbered tables or bare file names in section 35: test_w1133 reads any '| <digits> |' six-cell row after section 34 as its own table, and test_w711 and test_w1133 require every backticked name to be a path that exists.

**The refuter's verdict on the cluster:** PLAN_NEEDS_FIXES

**What the refuter checked:** Read the round design's cluster D file (a session work file, not in the tree) whole (4 gaps with both refuters, 8 corrections, 10 Owner questions, 2 v40 gaps, 2 merged items, and the two Owner-decision notes, whose 2026-11-22 text is identical in clusters A, B and C), the round design's cluster B file (a session work file, not in the tree)'s w1191_new_rows, and the count strings in the assessment's section-35 inputs (a session work file, not in the tree) and the v40 synthesis (a session work file, not in the tree). HEAD is 89c25eed with a clean tree, a shallow clone (root a27f491b), and W1191 not yet landed. Checked at HEAD:
- FABLE: the Owner's list (:155-286); P3.30 (:6612); P4.1 to P4.6; P5.6 (:6861, BOUNDARY :6886-6887); P5.7; P5.16 (:7325-7367); P5.17 clause 7 (:7398-7401); P5.20 (:7486-7529); P5.21; P5.22 (:7556-7567, no BUILT line); V6 (:1031); the rhythm (:7811-7812); :44; the live Done line (:1136, 97 of 119).
- plan_items: P4.3, P4.4 and P4.6 are the only items RECORDED AS A BOUNDARY.
- FOLLOWUPS.json: 1329 rows, max FU-1832, 35 open, 8 open gated. Read FU-1086, FU-1817, FU-1818, FU-1188, FU-1283, FU-448, FU-1057, FU-1185, FU-1290, FU-1077 and FU-1081. No closed gated id is a substring of FU-1833 to FU-1860 (test_w594's substring match). No row names the foundation's developer account.
- plan_followups.check (:1612-1757). docs/ is a retired area (P2.18, W588).
- README :128-179 (CRLF).
- RESUME (all 129 lines).
- The assessment's sections 33 and 34.
- AUTONOMOUS_PROGRESS.md: headings W1 to W502, and the highest W anywhere is 502.
- docs/README.md:12; LIVING_PLAN.md :70, :72, :745 and :758.
- The vision: :594-600, :1434-1446 and :1725-1738 (CRLF).
- LICENSE, CONTRIBUTING.md and both manifests.
- Every docs/business document the rounds touch.
- docs/letters.
- metabolism.py :108-150 (_generation_credit says 'credited against the first fee'); owner_payments.payee_of (:214-243); quran_foundation.py's header.
- scripts/_w557_probe.mjs:1.
- Spine guards read in full or at their pins: test_w594, _w703_faults with test_w703 and test_w963, w711, w725, w747, w771, w811, w838, w878, w896, w913, w962, w1120, w1126, w1130, w1131, w1132, w1133, w1143, w1149, w1151, w1152, w1153, w1154, w1155, w1164, w1174, w1180, w1188, w1190, w464, w462 and w499.
- Vitest: GenerationPrice.test.tsx and the MethodAppraisal fixture.
- Recomputed every figure in section 35's count table and the six claim moves and one demand move: all add up.

**Rounds the refuter said were missing** (the lead's schedule above answers each):

- W1192, the decisions round, has no design for cluster D's share of the Owner's 2026-11-22 rulings: Q1, Q5, Q6, Q8, Q9, Q10, Q11, Q12, Q13, Q14 and NG6. Each needs recording at the item it governs: P5.6 and P4.2 (Q8), P5.7 and FU-1818 (Q9, Q10), P5.16 clause 2 (Q11), FU-1817 (Q6), the canvas row (Q5) and the scholar row (NG6). Each also needs a dated list paragraph that names no row, and the notes. W1192 also registers the scholar OWNER act row, the OWNER act row for the channel and price tests after the first deploy, and the P4.2 build row for the return measure. The plan builds on the opposite state.
- The return measurement as P4.2's pre-flight (Q8 (a), 'schedule now'). This is gap 12's part (b) with the refuters' changes:
  - one sign-in day and one tool use per person per day;
  - counts across people only, never a figure about one person;
  - driven with sign-in on in a test process, as the readiness rows are;
  - 'A person returning' moves in METRICS_MEASURED.md only with its source (test_w878).
  The plan declines to design it as 'the Owner's to schedule after sign-in'.
- The seventh gate's bar (Q10 (a)), unless it is folded into D-FIRST-OFFER. COST_MODEL.md:65 and test_w1126's computation change from 'any docs/ file named interview' to five interviews in the notes template plus the Owner's recorded choice. Keep test_w962's no-'%' rule after '## Unit economics'.
- The credit's carry-forward (Q11 (b)):
  - a dated ruling at P5.16 clause 2, written before the COMPLETION RECORD or naming no test, since test_w1155 (:94286-94289) compares every test name after it;
  - the accountant question on the unit;
  - metabolism._generation_credit's basis text ('credited against the first fee') said as carried forward;
  - the field credited_against_first_profit_share kept, because test_mvp_spine.py:63186 and :91604 and GenerationPrice.test.tsx:46 pin it.
- The standing answer beside section 33 (Q1), if W1193 does not carry it.
