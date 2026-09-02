# Vision Fidelity Ledger — v2 (2026-09-02)

**Supersedes the 2026-08-31 ledger in full.** That version predated W419–W434 — sixteen
workstreams — and was marked *stale, do not trust* in prompt v10. This one is regenerated from
the fresh assessment that produced v10's ledger, against HEAD `d937dd37`.

## How this document was generated — and what that means for reading it

Six assessors ran one vision region each against a backend **booted from HEAD**, explicitly
barred from three sources: the vision's own §16 progress claim, the previous edition of this
ledger, and `AUTONOMOUS_PROGRESS.md` (a record of intent, not proof). They executed routes and
read implementations. Every claimed gap — up to six per region — was then attacked by an
independent refuter instructed to *default to refuted*.

Three reading rules follow from that method:

1. **DELIVERED is understated by construction.** Assessors were told their job was the gap that
   remains, not the work already done. 11 findings came back DELIVERED anyway, and all 4 findings
   the refuters killed were corrected *upward* to DELIVERED — the bias ran one way.
2. **32 gaps survived adversarial refutation; 27 were never individually refuted** (the
   refutation pass capped at six per region). Each entry below says which it is. An unrefuted
   finding is a lead, not settled evidence.
3. **The assessment ran before W434; 7 findings carry a post-assessment status below.**
   Each was assigned by PER-FINDING MANUAL REVIEW against the specific W434 fix or guard — a
   first, keyword-matched pass misfiled seven of twelve assignments (it marked the open
   floor-certification finding as disclosed, and stamped W434 on a MISSING develop stage it never
   built) and was thrown away. A status below therefore means the tie to the fix was checked,
   not inferred.

## Summary

| verdict (as assessed) | count |
|---|---|
| PARTIAL | 39 |
| DELIVERED | 11 |
| DOC_OVERCLAIM | 9 |
| API_ONLY | 6 |
| STUB | 5 |
| MISSING | 4 |
| **total** | **74** |

Post-assessment status: FIXED-W434: 3 · FIXED-W436: 2 · OWNER-DECISION-v10-item-2: 2

The distilled, actionable form of the surviving gaps is **prompt v10's two-entry ledger**
(`docs/FABLE_DELIVERY_PROMPT.md`). This document is the evidence base behind it.

---

## §10 (Solution-Quality Bar) and §11 (continuous compliance/sa

### §10 — PARTIAL

- **claim:** "Every solution is: specifically designed · modelled · simulated · optimised · categorised · ranked; best-in-class · innovative · effective · safe · efficient · commercially viable · compliant; verified · tested · validated." (16 criteria)
- **evidence:** Ran the gate directly. `export DATA_DIR=/c/tmp/fid ...; python -c "import asyncio; from agentic_core.vbs.quality import assure_delivery; asyncio.run(assure_delivery(<4-section, 900-char doc>, ['Executive Summary','Architecture','Risk','Commercials'], label='cascade'))"` → `SUMMARY: 4 measured · 0 attested · 12 not measured`; measured_criteria = ['compliant','safe','specifically designed','verified
- **user impact:** A user reading a delivery's quality record sees a gate that computed 4 of the 16 things the product promises. Twelve of the promises — including every commercial one — are decided by nothing on 13 of the 14 delivery surfaces. On Genesis 7 more are re
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** Either (a) a real instrument exists for at least the commercial trio (effective / efficient / commercially viable) — e.g. unit-economics from the BMS estimate already computed at swarm.py:865-875, and an efficiency figure from operational_excellence 

### §10 — PARTIAL

- **claim:** W419: the bar is resolved per-criterion in three honest states (gate-measured / caller-attested / not measured), replacing "the bare 16-name list that implied a measurement that never ran" (quality.py:162-163)
- **evidence:** The backend fix is real (quality.py:94-102 returns `summary`, `measured_criteria`, `attested_criteria`, `not_measured`). But grep for `quality.bar` across apps\workstation-superapp\src shows FOUR render sites and only ONE consumes `bar_measured`: · apps\workstation-superapp\src\pages\Deliverables.tsx:213-226 — correct: renders `§10 bar: 4 measured · 0 attested · 12 not measured` plus which are whi
- **user impact:** On the Genesis, Swarm-cascade and Resource-Fabric surfaces a user hovers a green pass badge and reads all sixteen quality criteria listed as though the delivery met them. The honest "4 measured · 12 not measured" figure is computed, sealed into the D
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** GenesisJourney.tsx, SwarmIntelligence.tsx and ResourceFabric.tsx render `bar_measured.summary` (and the measured/attested split) in place of `bar.join(' · ')`, with their TS interfaces extended to carry `bar_measured`; no surface presents the flat 16

### §10 — PARTIAL

- **claim:** "safe" is one of the four criteria the gate MEASURES — basis "§11 safety-bearing frameworks" (quality.py:74-79)
- **evidence:** quality.py:76 computes `measured("safe", all(verdicts[f] != "fail" for f in _safety), …)` — only a FAIL falsifies it. Ran a delivery whose text contains "hazardous waste" and "personal data": screen returned `ehs: review — Potential EHS concern: 'hazardous'` and `regulatory: review`, yet `safe -> True` and `compliant -> True`, and the summary still reported `4 measured` with all four met. Same sha
- **user impact:** A delivery the EHS screen has flagged for review is stamped `safe: met` in the tamper-evident DCMS quality record and counted among the met criteria. The flag survives only inside the criterion's `basis` string, which no UI renders. A reader of the r
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** `safe` and `compliant` return a three-state value (met / flagged-for-review / not-met) rather than a boolean collapsed on FAIL only, the counts report the flagged case separately from the met case, and the surfaces that render the badge distinguish t

### §10 — API_ONLY

- **claim:** "the QMS is stateful, so defects accumulate and a non-conformance rate is tracked across deliveries (this is what makes it *continual*)" — W307/W316 persistent traceable defects that the close leg RE-MEASURES rather than self-attests (quality.py:6-9, 149-158)
- **evidence:** `curl http://127.0.0.1:8011/api/v1/vbs/qms/defects` → 200 with real state: `{"gates_run":9,"defects_total":1,"gate_failures":1,"open":1,"non_conformance_rate":0.1111}` and a defect carrying `delivery_ref.content_sha3`. `/api/v1/vbs/qms/document-control` → `{"controlled_documents":9,"registered_artifacts":8,"audit_integrity":1.0}`. Both endpoints are genuine. But `grep -rn "vbs/qms" apps/workstatio
- **user impact:** The living QMS's whole claim to being *continual* — an accumulating defect register with a real non-conformance rate and a re-measured close — is invisible to every user. A user sees per-delivery pass/fail badges and can never see that the platform i
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** A reachable page (a tab in the Governance Center is the natural home) lists the defect register with `gates_run` / `non_conformance_rate` / open-vs-closed, shows each defect's `delivery_ref`, and exposes the `correct` and `reverify` actions, with a r

### §10 — DOC_OVERCLAIM

- **claim:** Dashboard capability pillar: "Governance & Compliance — Solution-quality bar · live compliance" → /governance-hub, described as "each a real, reachable surface" (DashboardNew.tsx:53)
- **evidence:** apps\workstation-superapp\src\pages\DashboardNew.tsx:57 declares that pillar. App.tsx:225 routes `/governance-hub` to `GovernanceCenter`, whose tabs (pages\governance\GovernanceCenter.tsx:10-14) are Governance (= GovernanceHub) · Constitution · Compliance. GovernanceHub.tsx is 650 lines with tabs Audit · Sovereign Vault · The Sanctum; `grep -n "bar|§10|Quality" GovernanceHub.tsx` → the only hit is
- **user impact:** A user who wants to see the solution-quality bar clicks the one dashboard pillar that names it and lands on an audit/vault/sanctum page with no quality bar on it. The bar exists only as a hover tooltip on individual delivery results scattered across 
- **refutation: KILLED — corrected to:** §10 — DELIVERED. The Solution-Quality Bar is a real, executing gate (agentic_core/vbs/quality.py::_measure_bar) with honest per-criterion accounting, verified l
  - reviewer's reasoning: The colleague's raw observations are correct but the verdict is wrong. Verified: DashboardNew.tsx:57 does declare the pillar 'Governance & Compliance / Solution-quality bar · live compliance' routed to /governance-hub (rendered as a clickable card, lines 210-217, under the line-52 comment 'each a re
- **done when:** Either the Governance Center gains a Quality tab that renders the §10 bar's real state (the `bar_measured` three-state counts and the QMS defect register), or the DashboardNew pillar copy names what /governance-hub actually contains.

### §11 — PARTIAL

- **claim:** W421: "§11 verdict + economic hold surfaced to the entity owner" — the entity's owner can see its live compliance standing and the hold it causes (living_vsbs.py:71-74)
- **evidence:** Executed the full path against a registered entity: `python -c "import agentic_core.economy.living_vsbs as lv; from agentic_core.organism.heartbeat import screen_living_vsb; lv.register('vsb_test1', name='Halal Meal Prep'); screen_living_vsb('vsb_test1'); lv.list_living()"`. The persisted history is `{"overall":"pass","last_at":"2026-09-02T01:18:48Z","regression":false,"history":[…]}`. The owner-v
- **user impact:** The verdict badge reaches the owner (that half is real), but stripped of both the things that make a verdict actionable. An owner whose enterprise shows `§11 fail` — with distributions held and its shipped repo marked stale — cannot see which of the 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** `screen_living_vsb` persists `screened_at` and the per-framework `verdicts` (with reasons) into vsb_compliance_history.json, `list_living` reads the keys that are actually written, and the VSBEconomy badge shows the failing framework(s) and the scree

### §11 — PARTIAL

- **claim:** "Compliance engines (Halal/Sharia · UK-Legal/London · Regulatory · EHS · Ethical · Constitutional/gaas) are integrated into every synthesis/generative/operational workflow, not bolted on." The screen's verdict has teeth: it holds the economy, gates marketplace listings, and stamps §10's `compliant` 
- **evidence:** Three probes against the live HEAD backend, `POST http://127.0.0.1:8011/api/v1/compliance/check`: · "A peer-to-peer consumer credit marketplace charging 18% APR on unsecured personal loans, with late-payment penalty fees compounding monthly." → `sharia_halal: pass`, `regulatory: pass` (riba, and an FCA-regulated activity). · "A premium sports-prediction app where users stake money on match outcome
- **user impact:** The three canonical prohibitions the platform is faith-rooted on — riba, maysir, pork — pass the halal screen when written in ordinary business English. This verdict is load-bearing: it releases or holds an entity's distributions (living_vsbs.py:170-
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The halal screen assesses the described *business model* rather than a keyword list — at minimum a structured intent check (financing terms, chance-based payout, animal-source products) with the AI fabric or an expanded rule set — and the three probe

### §11 — PARTIAL

- **claim:** The Constitutional/gaas engine is one of the six "integrated into every synthesis/generative/operational workflow, not bolted on"; §17.5 restates it as the invariant "mandatory GaaS gate on every output"
- **evidence:** `screen_compliance` — the function the universal delivery gate calls (quality.py:138-142) — returns FIVE verdicts and says so in its own docstring: "(The gaas.v5 Constitutional gate is applied separately by the org cascade / Change Control.)" (compliance.py:104-105). The sixth is added only inside the HTTP endpoint at compliance.py:187-196. Verified live: `POST /api/v1/compliance/check` → `n_verdi
- **user impact:** The Deliverables pipeline — the surface §13 calls "every deliverable is alive", where a user generates their Report / Presentation / Website / Video — and the Reactor Studio, Petri dish and Experiment surfaces produce output that no constitutional ga
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** Either `screen_compliance` runs the constitutional gate itself (so all six travel with every delivery through `assure_delivery`), or deliverables.py and products.py apply it explicitly the way swarm.py:793 does — and the response/UI stops labelling a

### §11 — PARTIAL

- **claim:** W308: "every domain-tool / refine response passes the SAME living QMS + compliance gate as the cascade and deliverables… the quality/compliance posture rides on the provenance the UI already renders" (_ai_provenance.py:40-43)
- **evidence:** The gate really does run on every Offering-1 tool (9 domain routers import `ai_text`). But it is surfaced wrong. Proved the failure mode by running the exact call the domain tools make: `assure_delivery(<250-char wine-pairing text>, None, label='tool:law_agent')` → `qms_gate_passed = True`, `compliance overall = fail`, `compliance_routed_to_cca = None`. Then apps\workstation-superapp\src\component
- **user impact:** On the Domains surface — the offering the canon describes as "usable directly, independent of establishing an enterprise", i.e. the way most users first touch the platform — a §11 FAIL is displayed to the user as a green pass, is never explained, and
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** DomainTool.tsx renders a distinct compliance badge whose colour reflects `compliance_overall` (fail = red, review = amber), `_ai_provenance` returns the per-framework `verdicts` (not just `compliance_overall`) so a reason can be shown, and either `to

### §11 — PARTIAL

- **claim:** The Compliance page: "One federated check across Sharia/Halal · UK Legal (London) · Regulatory · EHS · Ethical · Constitutional" (ComplianceChecker.tsx:38-39). W285 added honest per-framework engine labels so "the registry names ONLY what genuinely runs" (compliance.py:44-46).
- **evidence:** `GET http://127.0.0.1:8011/api/v1/compliance/frameworks` returns the honest labels W285 wrote — `regulatory | built-in regulatory rules (trigger set)`, `ehs | built-in EHS rules`, `sharia_halal | HalalComplianceOfficer (invoked) + built-in rules`. apps\workstation-superapp\src\pages\governance\ComplianceChecker.tsx:45 renders `{f.name}` and nothing else — the `engine` field is fetched and discarde
- **user impact:** The user reads six named compliance engines and a page promising to "keep every output halal, lawful, and ethical". The honesty W285 built into the API — that Regulatory and EHS are built-in trigger sets — is one field away from the screen and never 
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The frameworks chips render `f.engine` (as a subtitle or tooltip) so a rule-based framework is visibly distinguishable from an engine-backed one, and the page's header copy stops implying AI-mediated evaluation of a deterministic regex screen.

### §10 · §11 — DELIVERED

- **claim:** W419: every criterion carries `source` — gate / caller / none — and "the counts are reported separately… so a reader sees '4 measured · 5 attested · 7 not measured' rather than a single '9 measured' that hides which is which" (quality.py:37-51). W420: the five heartbeat autonomy flags are switchable
- **evidence:** quality.py:57-102 does exactly what the docstring says: `measured()` sets `source: "gate"`, caller evidence sets `source: "caller", measured: False`, and the counts are three separate integers. Verified by execution — a delivery with no evidence reports `4 measured · 0 attested · 12 not measured`; genesis.py:352-376 supplies attestations that are each derived from the run (the `simulated` key is w
- **user impact:** None — this is the part that works. The §10 record no longer conflates a measurement with a caller's claim, Genesis no longer emits attestations that could not have been false, and the §11 continuous-re-screen switch is reachable, durable across rest

---

## §4 — the end-to-end lifecycle (Concept → Commercialisation),

### §4.3–§4.9 — PARTIAL

- **claim:** "One continuous, intelligent, autonomous workflow ... takes a plainly-described challenge all the way to a living enterprise" — stage 3 Innovate & Research, 4 Design, 5 Rank, 7 Operational Intelligence and 9 Commercialisation each build on the stage before it.
- **evidence:** POST http://127.0.0.1:8011/api/v1/genesis/journey with problem='Community water filtration for rural villages with unreliable power and high iron content in groundwater', domain=science, realm=scholarship (HTTP 200, 0.64s). Counted the problem's own terms per stage: phase_1_conceptualisation.concept = 99 hits (water 30, filtration 12, groundwater 12, iron 9, village 12, rural 12, power 12). stage_
- **user impact:** A person who describes a real problem gets a Research section, a Design, an Operational-Intelligence section and a Commercialisation plan that are all about Workstation's own engine rather than their problem. Everything from stage 3 onward — includin
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **FIXED in W434** (verified by execution; a named `test_w434_*` guard covers it)

### §4 (whole region) / §5 / §10 — DOC_OVERCLAIM

- **claim:** Every stage is "verified, tested and validated"; the response reports stages_verified and quality_assurance.quality.qms_gate_passed to the user.
- **evidence:** The same journey run returned "stages_verified": "5/5", every stage_verifications entry verified:true (coverage 1.0, structure 1.0 across all five), qms_gate_passed:true, delivery_coverage:1.0, stub_found:false, and bar_measured criteria 'specifically designed' and 'verified' both met:true, measured:true — on the content in finding 1, which had lost the user's problem entirely and repeats one iden
- **user impact:** On the shipped default configuration (no Ollama, no external key — exactly what this HEAD boot reports) a person is told their lifecycle was verified 5/5, quality-gated and complete while looking at keyword salad. Nothing on the journey surface tells
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **FIXED in W436** — floor state rendered above the results, bar_measured mirrored on Genesis, floor-served stages return verified: null ("not assessable"), and the identical-candidates note renders in place of ranked cards. Verified in a real browser; guard test_w436_floor_served_stages_are_not_certified

### §4.5 — PARTIAL

- **claim:** "every candidate solution is specifically designed, modelled, simulated, optimised, categorised and ranked so the best solution is selected on evidence (effectiveness, safety, efficiency, commercial viability, compliance)".
- **evidence:** In the journey response the three candidates (pragmatic / innovative / lean) are BYTE-IDENTICAL: md5 of each `approach` = 5792636d6b, length 1738 each, difflib SequenceMatcher ratio 1.000 for all three pairs; identical modelled_score 0.81, simulation_score 0.976, score 0.909. Cause: the framing ('the fastest, lowest-risk...' vs 'the most innovative...') is prose in the prompt body, not a labelled 
- **user impact:** The user sees three ranked alternatives with distinct descriptions and believes a comparison happened; three copies of one text were compared to themselves. They are also never told that three of the five criteria the section names (effectiveness, ef
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **FIXED in W436** — the payload reports `candidates_distinct` + a plain comparison note (W434), and GenesisJourney now renders that note IN PLACE OF the ranked cards when the candidates are not real alternatives (W436, browser-verified)

### §4.9 — DELIVERED

- **claim:** "Output in any selectable format / combination — Research and deliverables as Reports, Presentations, Videos, Websites, Platforms, Apps, Products, Services".
- **evidence:** GET /api/v1/deliverables/output-formats lists 12 live ids and honestly names mp4/mp3 as catalogue_not_yet_produced ('documented targets, not faked'). Produced deliv-76ea4f86 via POST /api/v1/deliverables/produce, then exported every non-trivial format and checked magic bytes: pdf → HTTP 200, 1436 B, 255044462d312e33 (%PDF-1.3); docx → 36746 B, 504b0304 (zip); pptx → 30000 B, 504b0304; xlsx → 5118 
- **user impact:** None — this works. Only rough edge: the Genesis page's own export buttons (GenesisJourney.tsx:551-557) hardwire report→html and presentation→slides, so a user wanting PDF/DOCX/PPTX of their journey must know to visit the Deliverables page afterwards;

### §4.9 / §4.8 — PARTIAL

- **claim:** The established enterprise's output is "living" and shipped — a Website, Web app and Phone app representing the venture (§16.2 asserts shipped public copy is grounded + floor-safe).
- **evidence:** GET http://127.0.0.1:8011/api/v1/vsb/vsb-eebf118900/website/page/solution (an entity established on this HEAD) serves, inside the public <main>: '_Acting as: IDBO Conceptualisation engine._', '## INKASHAF', "Native structured content for 'INKASHAF', grounded in: (domain: science).", '- external dependency - structured engine - owned external - engine owned - workstation', and prose truncated mid-w
- **user impact:** Every VSB established on the default configuration publishes a website whose Solution and About pages display the AI engine's internal role labels, cognitive-engine codenames and grounding sentences to anyone who opens it — the first artefact a found
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **FIXED in W434** (verified by execution; a named `test_w434_*` guard covers it)

### §4 / §17.1 — DOC_OVERCLAIM

- **claim:** "All 96 [Realm × Domain × Product combinations] follow the same Concept → Design → Build → Launch → Commercialise stage-gated lifecycle."
- **evidence:** Seven mutually incompatible stage models are live at HEAD. (1) The canon 5 exist only at apps/workstation-superapp/src/pages/create/CreatorStudio.tsx:38 — and there they are an unguarded dropdown: I POSTed all five stages to /api/v290/ceo/generate-blueprint and each returned an independent one-shot blueprint with no carry-forward and no gate (a user can pick 'commercialise' first). (2) ProjectsHub
- **user impact:** There is no single lifecycle a person can follow. A user who learns the 5 stages in Creator Studio finds Projects offers 3 with different names, the review-gate panel offers 8 in a contradictory order, and the flagship Genesis journey neither names n
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **OWNER DECISION — v10 ledger item 2** (the lifecycle; do not close unilaterally)

### §4.4 / §4.5 / §17.1 (Creator Studio) — STUB

- **claim:** The one surface carrying the canon lifecycle generates a stage- and realm-specific blueprint plus 'the pipeline nodes from the AI response'.
- **evidence:** agentic_core/api/v290/ceo_generate.py:175 computes `system = _REALM_SYSTEMS.get(req.realm.lower(), _REALM_SYSTEMS['general'])` and NEVER references it again — `grep -n 'system' ceo_generate.py` returns only line 25 (a comment) and line 175. The 11-entry expert-persona table is dead code, so Creator Studio's realm selector shapes nothing (the same defect W427 fixed for Genesis, left standing here).
- **user impact:** The canvas that is the whole point of Creator Studio is a template with the user's words pasted in, presented as an AI-generated pipeline, and it is byte-identical whether the user picked Concept or Commercialise. The realm they choose (Enterprise / 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **FIXED in W434** (verified by execution; a named `test_w434_*` guard covers it)

### §4.6 — MISSING

- **claim:** "Develop — build and validate the solution (research → design → development), efficiently, cost-effectively, verified · tested · validated · best-in-class."
- **evidence:** The journey response's stage keys are phase_1_conceptualisation, stage_3_innovate_research, stage_5_model_simulate_rank, phase_2_design_development, stage_7_operational_intelligence, phase_3_commercialisation — there is no develop/build stage. phase_2_design_development is a single prompt (genesis.py:291-298) requesting only '## Solution Architecture / ## Core Components / ## Technology & Delivery
- **user impact:** The lifecycle stops at a design document. Nobody who walks §4 end to end gets a built, costed or tested solution — they get prose describing one, plus a corporate website for a company that has not built anything. The word 'Development' in the stage 
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A distinct stage between design and operational intelligence produces at least one buildable, checkable artefact for the user's solution (a bill of materials with costs, a runnable prototype spec, or a parameterised model) and reports a real pass/fai

### §4.10 — PARTIAL

- **claim:** "Run · Defend · Heal · Learn · Improve · Grow — forever. The established VSB self-operates and forever evolves on live intelligence, research, and analysis."
- **evidence:** GET /api/v1/heartbeat/status: running:true with beats incrementing on a real cadence (01:13:51 → 01:17:11 → 01:20:31), integrations including immune/self_healing/genome/UEG — the organism heartbeat is genuinely alive and W420's persistence is real (autonomy_persisted:true). But all five autonomy flags default OFF: auto_evolve:false, auto_economy:false, auto_align:false, auto_compliance:false, auto
- **user impact:** A person who completes the journey and establishes their enterprise is told it is living and self-operates forever. It operates once, at birth, then never again unless they find a platform-level Organism page and switch on flags nobody told them abou
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The entity owner's surface (VSBCockpit / the Genesis post-establish panel) shows the entity's real autonomy state — last_operated, cycles, and which heartbeat flags govern it — and offers the switch, or states plainly 'this entity is dormant because 

### §4.8 / §4.10 — PARTIAL

- **claim:** The lifecycle culminates in a living VSB IDBO enterprise, and the platform reports how far along the Concept→Commercialise pipeline it is (GET /api/v1/organism/lifecycle: "Concept→commercialise pipeline state across all projects and VSBs").
- **evidence:** A string mismatch makes the terminal stage unreachable. agentic_core/api/organism_status.py:85 computes active = sum(1 for v in entities if v.get('status') == 'active'), but every VSB creation path writes 'operational': genesis.py:593, genesis.py:697, genesis.py:759, genesis.py:844 and vsb.py:1435 (grep -rn '"status": "active"' agentic_core matches only capital_fund.py, frontier.py and qep_intelli
- **user impact:** The stage vsb_active is structurally unreachable and commercialisation_readiness is pinned near 0.0 no matter how many living, commercialising enterprises a user establishes. The platform's own answer to 'how far did I get?' permanently reads 'spawne
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** _vsb_state counts the status literals the entity paths actually write (or reader and writers agree on one literal defined in one place); a test establishes a VSB and asserts organism/lifecycle reports active >= 1, farthest_stage 'vsb_active', and com

### §4.2 — PARTIAL

- **claim:** "Understand & Map — AI-mediated problem mapping: understand the person, the context, the real underlying problem, constraints, goals, and success criteria." (W428: an explicit owner-scoped user profile reaches generation prompts.)
- **evidence:** The profile store and its injection point are real and carefully written (agentic_core/ai/user_context.py; gateway.py:151-153 applies load_preamble(owner_id) independently of augment). Two gaps. (a) owner_id is never threaded: `grep -rn 'query_meta(' agentic_core | grep -c owner_id` → 0 out of 17 call sites, including every Genesis stage (genesis.py:155 calls gateway.query_meta(prompt, agent=agent
- **user impact:** The stage meant to 'understand the person' does not. A signed-in user in a multi-user deployment has their profile silently dropped on every provenance-returning generation path — which is all of Genesis and all of the VSB website copy. A single-user
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** Every generation-class caller passes the request's owner id into gateway.query/query_meta (Genesis can thread the `user` it already receives at genesis.py:139); a test with auth enabled asserts a stored profile's distinctive token appears in the prea

### §4.1 — PARTIAL

- **claim:** "Describe — the person describes their challenge (multimodal: text, voice, image, uploaded data — research reports, reviews, data, media, sites, apps, models)."
- **evidence:** W429 is real and honest: AttachDocument.tsx:20-96 extracts PDF text in-browser via a locally-emitted pdfjs worker (no CDN), reports pagesWithText/pages in the inserted block header, and refuses a scanned/image-only PDF with an accurate message rather than attaching an empty document. DictateButton.tsx:29 feature-detects Web Speech and renders nothing when absent (no fake mic). But the accept list 
- **user impact:** Of the modalities the section names, a person can bring text, voice and text-bearing documents. They cannot bring a photo of the thing they are describing, a scanned report, a screenshot, a site or an app — ordinary ways of describing a real-world pr
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** At least the image path exists end to end from the Genesis Describe field — an attached image is either read by an owned vision/OCR resource and inserted as text, or refused with an accurate reason naming what would be needed; and the intake control 

---

## §5 (the living organisation: Chief → AI CEO → C-Suite → CoE 

### §5 — DELIVERED

- **claim:** "Chief of the Board of Directors = the Founder's Digital Twin… The Chief owns the living Business Plan… and delivers it via Strategy and a living Roadmap: a time-phased view of the objectives (phases · per-phase progress · current phase · next milestone)… integrated into the plan + the VSB Cockpit."
- **evidence:** Ran `agentic_core.api.board.board_status()` / `board_charter()` / `chief_instruct(...)` directly (DATA_DIR=/c/tmp/fid). Status returned hierarchy ['Owner','Chief (Owner Digital Twin)','Board of Directors','AI CEO','C-Suite','CoE','BTO','Operational Delivery'] + 7 directors; charter returned the arms-length invariant. chief_instruct('Reduce time-to-first-deliverable…') returned directive_id dir-7ee
- **user impact:** A user can reach the apex tier, read the charter invariant, instruct their Chief twin, and see the resulting objective land in the living plan with a roadmap. Last pass's §5 API_ONLY on the Board tier is closed.

### §5 — DELIVERED

- **claim:** "each tier manages, appraises, and develops the tier below" — the organisation is "itself optimised for continual improvement of how it delivers".
- **evidence:** Ran `swarm.cascade_orchestration(CascadeRequest(mission='Launch a halal-compliant micro-clinic booking service in Manchester', domain='care'))` twice against the same DATA_DIR (/c/tmp/fid3). Run 2 returned development_applied {'chief_appraises_board':'4d6900d50b','board_appraises_ceo':'4d6900d50b','ceo_appraises_csuite':'4d6900d50b','csuite_appraises_coe':'4d6900d50b','ceo_appraises_bto':'4d6900d5
- **user impact:** The appraise/develop loop is a real cycle-over-cycle mechanism, not prose: the second cascade demonstrably carries the first one's appraisal actions. A user can select which C-Suite officers to engage, bind the run to a VSB scope and a specific plan 

### §5 — PARTIAL

- **claim:** "Specialist C-Suite (e.g. CSO/CFO/CTO/…) — lead and develop their specialised resources and tools; each drives their Centre of Excellence." The delivery record is supposed to name the tier that produced each part.
- **evidence:** From the cascade run above, level_2_csuite['CSO'] literally begins: "_Acting as: AI CEO of a VSB._\n\n## Intent & Values…" and level_2_csuite['CFO'] begins "_Acting as: Chief Strategy Officer._\n\n## Intent & Values…" — every tier is labelled with the PREVIOUS tier's persona and emits the previous tier's section headers. Same in the Board cascade: /c/tmp/fid/board_directives.json's ceo_action_plan
- **user impact:** A user runs the org cascade, opens the panel headed 'CFO', and reads text that says it was written by the Chief Strategy Officer, under the CSO's section headings. Every tier below the first in every in-house cascade is misattributed on screen, so th
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** The recall block is appended after (or fenced away from) the caller's instruction, and engine.py's `_role`/`_sections`/`_subject` are scoped to the caller's own prompt segment only (upstream/recalled text may ground terms but must not supply the pers

### §5 — PARTIAL

- **claim:** "AI CEO — receives the action plan… delegates to the specialist C-Suite"; the Chief "delegates a timelined/resourced action plan to the AI CEO" (board.py's own §5-apex-closure comment: "the delegation LANDS: parsed objectives (TITLE|KPI|TIMELINE|OWNER_ROLE) are appended to the scoped LIVING business
- **evidence:** chief_instruct returned objectives_added=1, but the objective written to /c/tmp/fid/business_plans/workstation.json is {'title': 'Reduce time-to-first-deliverable for new founders by half this quarter.', 'kpi': '(KPI to be set by the Board)', 'timeline': 'next review', 'owner_role': 'AI CEO', 'source':'chief_instruct_fallback'} — i.e. the Owner's own instruction restated. `parse_objective_lines(ac
- **user impact:** The user's instruction round-trips into the plan as one untimed, un-KPI'd objective. Nothing the AI CEO 'planned' reaches the plan, so the promised timelined/resourced delegation does not exist for any user running the shipped default configuration. 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** Either the floor emits parseable objective lines for the pipe-delimited contract, or the fallback is DISCLOSED at the point of display — the Board page states 'no machine-readable objectives were produced; your instruction was recorded as one objecti

### §5 — PARTIAL

- **claim:** The Chief is "modelled, simulated and iterated specifically for the founder's instructions and input data", and "Every VSB IDBO entity generated for a user receives its own Board + a Chief that is the digital twin of *that* VSB's owner" (board.py:12).
- **evidence:** agentic_core/api/board.py:123 `founder_profile()` takes no owner or scope argument; line 133 reads `prior = [r for r in _load() if r.get('instruction')][-5:]` from the single global board_directives.json. Reproduced (DATA_DIR=/c/tmp/fid5): called chief_instruct(instruction='ACME-SECRET: acquire the Leeds competitor before Q4', owner='Alice', scope='vsb-alice'), then called founder_profile() as any
- **user impact:** One founder's verbatim instructions are fed into another founder's Chief-twin prompt and can surface in that founder's directive text. And no entity founder actually gets a twin of themselves: they get the platform Owner's values plus a shared instru
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** founder_profile(owner_id/scope) and _live_intelligence(scope) filter the store by owner/scope; values come from that owner's own profile (§4.2's owner-scoped user profile already exists — ai/user_context.load_preamble). Regression: seed a directive f

### §5 — API_ONLY

- **claim:** "Board of specialist Directors — receive the strategy; deliver via Action Planning… delegate downward" — board.py:454 board_directive: "the board deliberates as SPECIALISTS: the relevant directors are selected deterministically, EACH contributes through its own AI call GROUNDED in live readings of t
- **evidence:** Ran board.board_directive(topic='governance of autonomous evolution') directly: it works and is genuinely grounded — directors_engaged ['dir_biomimetic','dir_evolution','dir_governance'], with live groundings 'immune threat NOMINAL; circadian MAINTENANCE_REST; ATP 0.358', 'active Development Actions: 0 tier edges', 'UEG audit chain: 0 sealed events'. But `grep -rn 'board/directive' apps/` returns 
- **user impact:** The specialist-director deliberation — the only thing that makes this a Board rather than a single Chief — cannot be triggered by any user. The 'Recent Board Deliberations' section on the Board page is permanently empty, because nothing in the produc
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** The Board tab has a topic/domain form that POSTs /api/v1/board/directive (with the scope selector the API already supports) and renders director_inputs + live_grounding + the Chief's resolution; the 'Recent Board Deliberations' list then populates fr

### §5 — API_ONLY

- **claim:** "Specialist C-Suite (CSO/CFO/CTO/CPO/COO/CIO/CLO/Forecasting/Policy) — lead and develop their specialised resources and tools; each drives their Centre of Excellence (CoE)."
- **evidence:** agentic_core/api/csuite.py:14 mounts prefix '/csuite' (app_mvp.py:60 mounts it under '/api', so /api/csuite/...). Its two real endpoints — /cfo/metrics (line 56) and /cto/infrastructure (line 101) — compute genuine figures from the projects store, token ledger and psutil. `grep -rn 'csuite' apps/…` finds no API caller; apps/workstation-superapp/src/pages/c-suite/ is an EMPTY directory. Separately,
- **user impact:** There is no C-Suite surface. A user can only glimpse officers as text panels inside a cascade run (which are also misattributed, see the persona finding). The real CFO/CTO metrics the backend computes are unreachable, and if they were surfaced they w
- **refutation: KILLED — corrected to:** DELIVERED
  - reviewer's reasoning: REFUTED — the colleague audited the wrong file and missed the surface that actually carries §5's C-Suite claim. THE FACTUAL ERROR IN THEIR EVIDENCE They state: "grep -rn 'csuite' apps/… finds no API caller". That is false. `grep -rn csuite` over apps/workstation-superapp/src hits 4 files: · apps/wor
- **done when:** A C-Suite surface (or a tab on the Living Organisation hub) lists the 9 officers, each with its CoE, its fabric resources, and — for CFO/CTO — the live /api/csuite metrics scoped to the requesting user rather than 'demo_user'.

### §5 — PARTIAL

- **claim:** "Centres of Excellence (CoE) — specialist functional + operational delivery teams" — the tier the C-Suite drives.
- **evidence:** Sidebar.tsx:106 'CoE Hub' → App.tsx:230 `/coe` → pages/coe/KnowledgeHub.tsx, which fetches /api/v1/intelligence/insights and relabels each insight as a CoE. KnowledgeHub.tsx:45: when no keyword matches, the domain is chosen by `Object.keys(DOMAIN_META)[idx % Object.keys(DOMAIN_META).length]` — an arbitrary domain assigned by list position, then presented with that domain's icon, colour and descrip
- **user impact:** A user clicking 'CoE Hub' sees Centres of Excellence that the organisation does not have, with domains assigned by array index rather than by anything that discriminated — the exact defect class W430-W433 closed in twelve other places, still open her
- **refutation: KILLED — corrected to:** DELIVERED — §5 "Centres of Excellence (CoE) — specialist functional + operational delivery teams" is implemented (swarm.py:469-527 per-officer CoE generation ke
  - reviewer's reasoning: REFUTED — the colleague audited a page that is not the CoE tier's surface, and missed the one that is. WHAT IS ACTUALLY BUILT (verified against HEAD source + :8011): - agentic_core/api/swarm.py:469-527 (POST /api/v1/swarm/cascade): each engaged C-Suite officer runs `_run_officer()`, which fires a SE
- **done when:** The CoE Hub renders the real CoE tier (the C-Suite officers' CoEs and their level_3_coe outputs from persisted cascade runs); an unmatched domain is shown as 'domain not determined' rather than assigned by index; the empty state says there are no CoE

### §6 — DOC_OVERCLAIM

- **claim:** "Native, owned capability — not a façade over third-party APIs. Workstation's own models, its own orchestration, its own swarm." §6's own banner: "✅ DELIVERED (2026-06-24): this mandate is built… the native AI resource fabric, in-platform orchestrator, and bespoke reconfigurable swarm engine are liv
- **evidence:** Ran native_ai.native_status(): owned_resources_available ['native'], active_model 'native', is_real_model False, mode 'deterministic_floor', external_allowed False. agentic_core/ai/native/engine.py:1-18 is explicit and honest — "explicitly NOT a large-language model, and never presented as one". agentic_core/ai/native/model_resource.py:1-11 enumerates the only other 'owned' option as Ollama, i.e. 
- **user impact:** The runtime tells the truth (the Native AI page shows mode 'deterministic_floor' and 'NOT an LLM'), but the canon's §6 banner tells a reader — including the next engineer planning against it — that the models half of the mandate is built. It is not: 
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** §6's banner is qualified to state what is actually built (owned orchestration + owned swarm engine + a deterministic owned floor + optional self-hosted third-party weights) and names 'Workstation's own models' as the outstanding part of the mandate, 

### §6 — DELIVERED

- **claim:** "the autonomous workflow-TREE ('dynamic, adaptive, autonomous workflow / pipeline / cascade trees') runs goals through 12 real owned capabilities… external providers are optional, never dependencies"; and W424 — native-ai/status floor_active states its basis.
- **evidence:** native_capabilities() returned count 16 (up from the doc's 12), each with an endpoint and a real agentic_core source module; native_selfcheck() returned {'total': 13, 'live': 13, 'all_live': True} — every backing module imports. native_tree(goal='Design a compliant micro-clinic booking service for Manchester') planned and ran a real DAG: levels [['frame'],['research','design','risk'],['synthesise'
- **user impact:** A user on the Native AI page gets a real in-house orchestrator that decomposes a goal into a dependency DAG, runs it under organism-governed parallelism, and seals it — with an honest, self-disclosing account of which resource served and on what basi

### §6 — DELIVERED

- **claim:** "Reconfigurable by users. Greater user reconfiguration and design control of… the AI Agent Swarm cascades, workflows and pipelines."
- **evidence:** agentic_core/api/resource_fabric.py:1243 POST /api/v1/resources/swarm/define, :1257 PUT /swarm/{sid} (edit name/stages/context/org tiers, UEG-logged, VSB summary kept in sync), :1307 GET /swarm, :1357 POST /swarm/run — all owner-scoped via _require_design_access/_fabric_owner (W324). Reachable: apps/workstation-superapp/src/pages/developers/NativeAI.tsx:192 lists cascades, :301 posts to `/api/v1/r
- **user impact:** A user really can define, edit and re-run their own agent-cascade stages, and re-runs pick up the edits. This half of the 'reconfigurable' mandate is genuinely in the product.

### §6 — STUB

- **claim:** The 'Composer' surface presented in the Living Organisation hub as part of the §6 native swarm (LivingOrganisationHub.tsx:11 — "§6 native swarm") — a "Swarm Topology Designer" with "Config & Governance".
- **evidence:** apps/workstation-superapp/src/components/organism/VisualAgentComposer.tsx (175 lines): `grep -n 'fetch(|axios\.|api/v1'` returns ZERO matches — the component makes no network call of any kind. Line 21-22 seed it with models named 'Nematron-1B' and 'Nemoclaw-3B', which exist nowhere in the fabric (native_status lists only native/ollama/anthropic/openai). Line 136 renders a hardcoded green '<div>Gaa
- **user impact:** The Composer tab sits beside three working tabs (AI CEO, Board, Swarm) inside the Living Organisation hub and looks like the swarm designer the mandate promises. Nothing a user does in it is saved, run, or governed, the models it names do not exist, 
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** Either the Composer is wired to /api/v1/resources/swarm/define + /swarm/run (real stages, real save, real run, real gaas verdict from the response), or the tab is removed and users are pointed at the Native AI page's working cascade editor. In no cas

### §6 — PARTIAL

- **claim:** "Bespoke-per-solution swarms. The AI Agent Swarm cascade is synthesised, modelled and simulated bespoke to each solution's needs and requirements — and bespoke to each founder." genesis.py:446 docstring: "Give the VSB its OWN bespoke, reconfigurable native swarm cascade."
- **evidence:** agentic_core/api/genesis.py:446-471 `_attach_delivery_swarm` registers, for EVERY established entity, the identical four stages ('ai-ceo' → 'c-suite' → 'centre-of-excellence' → 'build-to-order') with the identical org tiers ['Chief (owner twin)','AI CEO','C-Suite','Centre of Excellence','Build-to-Order']; the only per-solution variation is the interpolated `context` string (name/mission/domain/con
- **user impact:** Two entities in entirely different realms — a micro-clinic and a legal practice — receive byte-identical delivery organisations. The user CAN reconfigure it afterwards (that path is real, see the DELIVERED finding above), so this is a missing synthes
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** Establishment derives the cascade's stages/roles/org tiers from the solution's domain, realm and concept (e.g. via the existing native orchestrator's `_plan_tree_adaptive`, which already decomposes a goal into a bespoke DAG), and the entity record re

### §6 — PARTIAL

- **claim:** Provenance is surfaced so users can see which OWNED resource served their work — "proves the org cascade runs on Workstation's own fabric" (swarm.py provenance block).
- **evidence:** The cascade payload carries ai_provenance {'served_by': {'native': N}, 'any_external': False}, but SwarmIntelligence.tsx:251-252 renders only a two-state badge — 'in-house' (green) or 'external used' (amber). It never names the serving resource, and never discloses that 'native' means the deterministic floor rather than a model. Contrast BoardOfDirectors.tsx:160-162, which does it correctly: 'serv
- **user impact:** A user reads a full org-cascade delivery under a green 'in-house' badge and has no way to learn, on that page, that every word of it came from a deterministic template engine rather than a model — which is precisely the difference that determines how
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The cascade result badge names the serving resource(s) the way the Board page does, and when the floor served it carries the floor_note from /api/v1/native-ai/status ('honest structured reasoning, NOT an LLM') at the point where the tier outputs are 

---

## §17 (canonical structure) + the systemic REACH question

### §17.1 — MISSING

- **claim:** "The product grid — 4 Realms × 6 Domains × 4 Products (96 combinations)… Products (how work runs): Reactor · Incubator · Factory · Laboratory. All 96 follow the same Concept → Design → Build → Launch → Commercialise stage-gated lifecycle."
- **evidence:** Realms and Domains have a canonical single source (agentic_core/taxonomy.py:11-12 REALMS/DOMAINS; apps/workstation-superapp/src/lib/taxonomy.ts:5-6). The third axis has NO canonical definition on either side: grep for a PRODUCTS/PRODUCT_TYPES constant over agentic_core/*.py, agentic_core/api/*.py and src/lib/*.ts returns nothing; taxonomy.py and taxonomy.ts contain no product list and no '96'. The
- **user impact:** A user cannot pick a Product for their work. There is no cell-selection anywhere: the grid a user can actually enter is 4 Realms × 6 Domains = 24 combinations, not 96, and the four Products are four unrelated standalone pages (one of which, Laborator
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **status now:** **OWNER DECISION — v10 ledger item 2** (the lifecycle; do not close unilaterally)

### §17.1 — STUB

- **claim:** Realm is one of the three canonical axes, with ONE source each side ("the audit found drifted per-page literals — five-realm lists, domains listed as realms, invented domains — every routed surface now imports from here", taxonomy.ts:1-3, W311/W321), and W427 gave realm teeth so "a scholar and a com
- **evidence:** The Projects surface — the flow every Domain hub's primary CTA leads to — runs an entirely separate, non-canonical realm vocabulary that does not intersect the canon. agentic_core/projects/api.py:5 documents realms as "(technology, science, religion, education, law, care, employment)"; REALM_PROMPTS (api.py:50-58) has keys ('technology','science','religion','education','law','care','employment','g
- **user impact:** On the Projects surface the realm axis is inert: a scholar, a learner, a developing-context user and a commercial operator all get the identical 'expert business strategist and product manager' persona — precisely the defect W427 closed for Genesis a
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** agentic_core/projects/api.py imports REALMS/normalise_realm/realm_directive from agentic_core.taxonomy and drops its private REALM_PROMPTS realm vocabulary (its domain-flavoured personas move to a DOMAIN table keyed by DOMAINS); the six Domain-hub CT

### §17.1 — PARTIAL

- **claim:** W427: "§17.1 realm now reaches every Genesis stage prompt and deliverables generation" — deliverables.py:155-157 "realm reaches GENERATION, not just storage. Deliverables took no realm at all, so output was identical for a scholar and a commercial operator."
- **evidence:** The backend plumbing is real (deliverables.py:96-105 _generate prefixes realm_directive(); :237-238 passes req.realm; :263 stores it so regenerate at :920-922 can read it back). But only ONE of the four UI surfaces that produce deliverables ever sends a realm. GenesisJourney.tsx:122/168-169/214 does. The others do not: Deliverables.tsx:84 POSTs {type, title, brief} and the whole file contains ZERO
- **user impact:** A user working from the main /deliverables page can never obtain the scholarly, learning or developing register at all — every deliverable is generated for 'a commercial operator who has to act on this'. A user who explicitly established a scholarshi
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** Deliverables.tsx exposes a realm control (importing REALMS/REALM_LABELS from lib/taxonomy) and sends it; VSBCockpit and VSBSpawnStudio send the parent VSB's stored realm; and produce_deliverable falls back to the VSB's realm when vsb_id is supplied a

### §17.2 — PARTIAL

- **claim:** "The biomimetic body — 7 layers (the IDBO's anatomy): 1 Genome · 2 Nervous · 3 Immune · 4 Cardiovascular · 5 Respiratory (autonomous workflow cascade / Agent Hub) · 6 Musculoskeletal · 7 Endocrine (signal bus / shared context + MJM)."
- **evidence:** Four layers are real and observable. Live on :8012: GET /api/v1/organism/systems returns exactly three — immune, nervous, self_healing; GET /api/v1/organism/status adds genome, metabolic, circadian, reconfiguration; GET /api/v1/biometrics/status returns cardiovascular {resource_flow: 63.7, peristaltic_delay: 4.5}. Respiratory, Musculoskeletal and Endocrine appear in no organism payload. The code s
- **user impact:** A user inspecting the 'biomimetic body' sees three cards, not seven, and no page tells them the other four are absent, elsewhere, or unimplemented. Two named layers (Respiratory/Agent Hub, Endocrine/signal bus) have working machinery the user can nev
- **refutation: KILLED — corrected to:** DELIVERED
  - reviewer's reasoning: REFUTED. I re-ran every check on :8011 (HEAD = 824d27f5, W433) and read the source. The colleague's two load-bearing pieces of evidence are, respectively, false and non-probative, and two of their own concessions already contradict their verdict. 1. THE CODE COMMENT THEY QUOTE IS FALSE, AND IS NOT E
- **done when:** /api/v1/organism/systems enumerates all seven §17.2 layers, each with either a live measured status or an explicit {implemented:false, reason} entry; the Agent Hub is bound to the Respiratory layer and the resource fabric to the Musculoskeletal layer

### §17.2 — DOC_OVERCLAIM

- **claim:** W422: "the delivery record names only CONTRIBUTING biomimetic layers" — quality.py:220-224: the record "used to write `layers: list(BIOMIMETIC_LAYERS)`, naming all seven on EVERY delivery regardless of what participated… `layers` now means what it says."
- **evidence:** The payload fix is real (quality.py:226-250 builds layers=[], appends only 'Immune', and adds layers_declared, layers_not_contributing and layers_note = "1 of 7 declared biomimetic layers contributed a value to this record"). But none of the three honest fields is read anywhere in the frontend: grep for layers_declared|layers_not_contributing over apps/workstation-superapp/src returns zero hits. T
- **user impact:** The only user-visible account of the biomimetic layers is stale in both directions: on the Swarm view a user is told seven layers participated when the payload in front of them says one did; on the Deliverables view a user is told the record names al
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** SwarmIntelligence.tsx and Deliverables.tsx render biomimetic.layers_note (or layers.length + '/' + layers_declared.length) from the payload instead of hardcoded prose, and list layers_not_contributing in the tooltip; no hardcoded '7 biomimetic layers

### §17.3 — PARTIAL

- **claim:** "The Living Business System — 4 continuously-maintained layers (with cadence). Constitutional (genome-locked): Mission · Vision · Values · Ethical mandate · Strategic (AI CEO; quarterly + market signal) · Action Plan (BTO; weekly + KPI-triggered) · Board Pack (on-demand)."
- **evidence:** Only the on-demand layer is alive, and it is the only one the canon marks ✅. Executed on :8012: POST /api/v1/vsb/vsb-e2d584e313/board-pack → 200, layers ['constitutional','strategic','action_plan','operational'], dcs_registered true, 1286-char AI-CEO narrative. The other three layers are birth-time snapshots with no cadence machinery. `strategic` is vsb['ceo_specification'] (vsb.py:1009); grep acr
- **user impact:** An owner who assembles a Board Pack a year after establishing their VSB gets a strategic position and an action plan written on day one and never revisited, presented under headings that promise a quarterly-refreshed strategy and a weekly-refreshed p
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** Strategic and Action Plan have real refresh generators (an AI-CEO strategic review and a BTO action-plan pass) invoked on their stated cadences by the heartbeat behind opt-in autonomy flags, plus a KPI/market-signal trigger; each layer in the board p

### §17.4 — DELIVERED

- **claim:** "Mode 3 — optional human review gates at any Concept→Commercialisation stage (set in the VSB genome). ✅ DELIVERED (W126): per-VSB review_gates config (GET/POST /api/v1/vsb/{id}/review-gates, per-stage status + blocks_progress, human …/{stage}/decision approve|reject), each config + decision append-o
- **evidence:** Verified live and in the UI, not from the doc. GET http://127.0.0.1:8012/api/v1/vsb/vsb-e2d584e313/review-gates → 200 with mode 'Mode 3 — optional human review gates (set in the VSB genome)', a stages array, and the full 8-stage lifecycle meta (intake, research, design, build, validate, commercialise, genome, launch) with per-stage statuses. Backend: vsb.py:1066-1123 — _LIFECYCLE_STAGE_IDS validat
- **user impact:** None — this works. A user can gate any of the eight lifecycle stages on their own VSB and record an approve/reject decision from the Genesis page, and each change is document-controlled.

### REACH (systemic) — API_ONLY

- **claim:** The vision's product is a user-facing living organism — every capability §1–§18 describes is something a person is meant to be able to reach and use.
- **evidence:** Method: generated the OpenAPI from HEAD (6b47c0ce) itself — `from agentic_core.app_mvp import app; app.openapi()` under DATA_DIR=/c/tmp/fid2 — because the stated :8011 backend was not listening (netstat showed only :8010, which I was told to avoid); booted my own isolated HEAD server on :8012 to execute. 442 paths, 441 under /api. Scanned 111 .ts/.tsx files under apps/workstation-superapp/src and 
- **user impact:** About half the built backend is invisible. The asymmetry is the point: the UI does not call dead routes, so the gap is entirely 'built and working, never surfaced' rather than 'advertised and broken'. Roughly 65 of those endpoints are legacy/unversio
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A reach guard exists in CI: it generates the OpenAPI from the app, extracts /api literals from src with the template-aware matcher, and fails on any NEW /api/v1 endpoint that no frontend literal reaches, against a checked-in allowlist of deliberately

### REACH (systemic) — API_ONLY

- **claim:** Named, working subsystems the canon leans on — including the Living Plan ("the single source of truth bridging vision ↔ grounded current state ↔ action… Live: GET /api/v1/plan + GET /api/v1/plan/state", docs/README.md:6) and §17.2's Respiratory layer, the Agent Hub.
- **evidence:** Seven whole routers have literally zero mention in the entire frontend — confirmed not just by the matcher but by a direct grep over apps/workstation-superapp/src for 'v1/plan|v1/hub|v1/vbs|v1/frontier|v1/studio|v1/evidence|v1/cognitive/', whose ONLY hit is a code comment (App.tsx:95, "the real living roadmap is the Living Plan (/api/v1/plan)", written while archiving the page that would have show
- **user impact:** The document the canon calls the single source of truth bridging vision, current state and action is served live and self-introspecting, and no user can see it from any screen — the one page that would have shown it was archived and replaced by a com
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A Living Plan page renders /api/v1/plan (pillars, phases, adherence) and /api/v1/plan/state (live grounded snapshot with its reconciled_at), routed and linked from the Dashboard; the Agent Hub is surfaced on the Organism page as the Respiratory layer

---

## §1-§3, §3A (the two offerings), §7, §9 (accessibility/person

### §3A(1) + §15.6 — PARTIAL

- **claim:** Domain Working offers "immediate, usable, in-house-AI-mediated working capabilities" that give "best-in-class capability on demand"; §15.6 requires "honesty over polish (never fabricate; label simulation)".
- **evidence:** GET http://127.0.0.1:8011/api/v1/native-ai/status returns is_real_model:false, mode:"deterministic_floor", floor_active:true, floor_note:"The deterministic native floor is serving — honest structured reasoning, NOT an LLM." That honest label appears in exactly ONE place in the frontend: grep -rn 'floor_active|is_real_model|floor_note' over apps/workstation-superapp/src returns 7 hits, all in pages
- **user impact:** A person using any of the 23 domain tools is told their result came from Workstation's own AI fabric, with a green badge, and is never told the answer came from a deterministic template engine rather than a language model. The only page that disclose
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** gateway.query_meta / _ai_provenance.ai_text propagate the orchestrator's is_real_model + mode into every ai_provenance payload, and DomainTool.tsx renders an amber "deterministic floor — structured reasoning, not a language model" badge (with the flo

### §10 (as applied to §3A + §13 outputs) — PARTIAL

- **claim:** Every solution is "verified · tested · validated" and passes the Solution-Quality Bar; the UI shows the user a "QMS pass" badge as proof.
- **evidence:** agentic_core/vbs/quality.py:105-112 — _delivery_coverage() = fraction of required section titles found as case-insensitive SUBSTRINGS anywhere in the text. Line 126 — stub_found = a regex for TODO|TBD|FIXME|lorem ipsum|placeholder|coming soon|as an ai, OR total length < 200 chars. I ran the gate directly: a document consisting of nothing but the four required headings plus 300 filler characters sc
- **user impact:** The quality gate cannot fail against the native floor's own output shape, because the floor always echoes every requested heading and always exceeds 200 characters. A user is shown a green quality certification on a document with zero substantive con
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** assure_delivery measures per-section SUBSTANCE, not heading presence: a section whose body is under N characters, or whose body is >0.9 similar to another section's body in the same document, or which contains the floor's own scaffolding phrases ("Na

### §9 — PARTIAL

- **claim:** "Enterprise-aware avatar integrated across the platform: multimodal communication / interaction with the AI CEO and the Chief, and guidance/navigation through any platform area."
- **evidence:** POST /api/v1/avatar/chat {"message":"Where do I go to establish an enterprise?"} and {"message":"My mother needs a dementia care plan. Which tool helps?"} returned IDENTICAL prose bodies: "## Understanding — The request concerns: You are the Workstation Sovereign Mesh avatar — a helpful, concise assistant across the whole platform." with key factors "workstation sovereign / concise assistant / hel
- **user impact:** The platform's one always-present conversational assistant answers every question by describing itself. Only the keyword-matched suggested_areas chip reflects what the user asked. A first-time visitor who asks the avatar anything gets back a block of
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** gateway._augment does not add a second "User:" label when the incoming prompt already contains one (append the recall block instead of wrapping), or the avatar passes augment=False. Verified by POSTing two different questions to /api/v1/avatar/chat a

### §3A(1) + §13 — PARTIAL

- **claim:** Domain tools let a user "research · analyse · generate · plan · assess · author · design · review" inside their domain and get a real deliverable.
- **evidence:** POST /api/v1/care/care-plan with {patient_profile:{age:84, condition:"moderate dementia", mobility:"unsteady, uses a frame"}, care_needs:["night-time wandering","poor appetite and weight loss"]} returned a care_plan whose EVERY section ("My Goals", "My Strengths and Support Network", "Care Needs and How We Will Meet Them", "Medication Management", …) has the identical body: the raw prompt scaffold
- **user impact:** A carer who fills in a real patient profile receives eight identically-worded sections containing no interventions, no review dates, no medication guidance — and the prompt's own instructions printed back at them. The Refine button on every one of th
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** _subject()/_content() are driven by the SAME label census as _CONTENT_LABELS (care.py, refine, education, law, employment labels all included), the longest-sentence fallback is restricted to text after the last recognised label, the W428 preamble is 

### §3A (the two offerings connect) — PARTIAL

- **claim:** "A user may use either independently or flow from the first into the second" — domain tool → Genesis → living enterprise.
- **evidence:** The bridge is genuinely built and works: components/DomainTool.tsx:276 writes sessionStorage ws_genesis_<sid> and navigates to /genesis?seed=…&domain=…; pages/synthesis/GenesisJourney.tsx:82-119 reads it idempotently and folds it into the problem. BUT the seed carries `output: String(result?.[resultKey] ?? result?.deliverable ?? '')` — the ORIGINAL v1 result — while the panel displays `displayText
- **user impact:** A user who refines their domain output three times, watches the "refined ×3" badge appear, then clicks "Commercialise via Genesis", silently hands the un-refined first draft to the enterprise-establishment journey. Every refinement is discarded with 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** DomainTool.tsx:276 seeds `output: displayText` (and `input` unchanged), so the handoff carries whatever the user is actually looking at. Verified by refining an output, clicking Commercialise, and seeing the refined text in the Genesis problem field.

### §3A(1) — PARTIAL

- **claim:** The Domains section is the front door to the domain tools; DomainsHub links to "the full launcher with every tool" at /ai-tools (DomainsHub.tsx:10).
- **evidence:** DomainsHub.tsx:15-22 declares Religion 4 · Science 3 · Education 4 · Law 2 · Care 4 · Employment 6 = TOTAL 23, and W423's counts are CORRECT (grep -c '<DomainTool' per hub returns exactly 4,3,4,2,4,6). The button at DomainsHub.tsx:60 reads "Browse all 23 tools" and routes to /ai-tools. AIToolsCatalogue.tsx:12-44 lists Law 2 · Science 2 · Care 3 · Education 3 · Religion 3 · Employment 5 = TOTAL 18,
- **user impact:** Clicking "Browse all 23 tools" lands on a page that announces 18. Five working tools — including Safeguarding Triage, the highest-stakes tool in the Care domain — are invisible to anyone who navigates by the catalogue rather than by guessing a hub ta
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** AIToolsCatalogue.tsx lists all 23 tools with their real ?tab= ids, and a test asserts AIToolsCatalogue's TOTAL equals DomainsHub's TOTAL equals the count of <DomainTool> instances across the six hub files.

### §13 — PARTIAL

- **claim:** "The canonical output is a Repository of the IDBO Entity (VSB) … shipped as a coherent, version-controlled whole that integrates a Website, a Web app, and a Phone (mobile) app."
- **evidence:** POST /api/v1/genesis/journey {establish:true, ship_output:true} for "ClearWell" returned initial_ship {shipped:true, coherent_whole:true, surfaces:[board_pack, mobile, repo, webapp, website], commit:"057e392c5533"}. On disk the shipped body is real and larger than reported: `find C:\tmp\hb3\vsb_repos\vsb-eebf118900 -type f` (excluding .git) = 29 files including a working PWA (mobile/index.html, ap
- **user impact:** The owner of an established enterprise looks at their entity's repository and sees 13 files and a note telling them their web app and phone app do not exist yet. Both do exist, in that repo, next to the note. The §13 canonical output under-reports it
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** ship_vsb_repo rewrites manifest.json after all five surface generators run (a real directory walk excluding .git), integrated_surfaces reports what each generator actually produced, and the placeholder webapp/mobile READMEs are replaced or deleted by

### §13 — MISSING

- **claim:** The repo "is the enterprise's living body: its genome/identity, business plan, organisation, digital resources, AI-swarm cascades, compliance + quality record" — the thing the user receives.
- **evidence:** The full route list for /api/v1/vsb/* (from openapi.json, 442 paths) contains no endpoint that returns the CONTENT of a repo file: GET /{vsb_id}/repo returns the manifest (paths + byte counts only), and the only file-content endpoints are /website/page/{name}, /webapp/page/{name}, /mobile/page/{name}. So README.md, IDENTITY.md, OPERATIONS.md, EVIDENCE.md, ORGANISATION.md, BUSINESS_PLAN.md, complia
- **user impact:** A user completes Concept→Commercialisation, is told a bespoke repository is their deliverable, and can never read a single document in it. They see filenames and byte counts. The business plan is separately reachable at /business-plan, but the identi
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** GET /api/v1/vsb/{vsb_id}/repo/file?path=… (owner-scoped, path-traversal-guarded) serves any manifest-listed file, GET /api/v1/vsb/{vsb_id}/repo/archive streams the repo as a zip, and VSBCockpit renders a clickable tree that opens each document. Verif

### §13 + §3A(2) — PARTIAL

- **claim:** The living VSB "integrates a Website, a Web app, and a Phone (mobile) app as the entity's public + operational surfaces" — surfaces the founder can see and use.
- **evidence:** The three surfaces serve real HTML: GET /api/v1/vsb/vsb-eebf118900/website/page/index → 200, 1565 bytes; /webapp/page/index → 200; /mobile/page/index → 200. GenesisJourney.tsx:817/847/879 does render Preview buttons — but only for surfaces the user manually re-generates on that page (lines 307/318/329 POST /website, /webapp, /mobile), and only within the live component state of that one session. V
- **user impact:** The birth ship (W302) already generates the website, web app and phone app, but a founder can only look at them inside the single Genesis page session that created them, and only after clicking Generate again. Come back tomorrow via the VSB Cockpit a
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** VSBCockpit renders Preview links for website / webapp / mobile for the selected VSB (reading the ship manifest's surfaces), each opening the corresponding /page/index endpoint, with an honest "not shipped yet" state. Verified by establishing an entit

### §9 — DOC_OVERCLAIM

- **claim:** "Accessible to all … adaptive and responsive, dynamically and intelligently personalised to each user's … needs and abilities." Settings.tsx:156 promises "On save, text size takes effect across the whole app".
- **evidence:** components/AdaptiveUIProvider.tsx:58 implements Large text as a single inline `fontSize: '1.15rem'` on a wrapper div — which only scales rem-based type. Counting the font-size utilities actually used: `grep -roh 'text-\[[0-9]*px\]' apps/workstation-superapp/src --include=*.tsx | wc -l` = 1447 px-literal sizes (566 × text-[10px], 489 × text-[9px], 260 × text-[8px], 123 × text-[11px], 7 × text-[7px]
- **user impact:** A low-vision user selects "Large (accessible)", is told it takes effect across the whole app, and the 8-10px chrome that carries the badges, provenance labels, disclaimers, compliance verdicts and nav — the text they most need enlarged — does not cha
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The px-literal font utilities are replaced with rem-based scale tokens (or the adaptive root sets a CSS custom property those utilities consume), Large visibly enlarges a 9px provenance badge, and the Settings copy states exactly what scales. Verifie

### §9 — STUB

- **claim:** The interface is "dynamically and intelligently personalised to each user's instructions, requests, history, preferences, needs and abilities."
- **evidence:** lib/userPrefs.ts:14 stores `tone?: 'encouraging' | 'neutral'`; Settings.tsx:147-152 offers the control; AdaptiveUIProvider.tsx:48 maps it to `emotionalAdjustment`, which the domain hubs render as a badge (CareHub.tsx:25 `<Badge>{emotionalAdjustment} TONE</Badge>`). Grepping every other consumer of `tone` across apps/workstation-superapp/src returns only unrelated uses (a DashboardNew colour prop, 
- **user impact:** The user sets their preferred tone; the only thing that changes is a badge on the hub page that displays the word they chose. No AI output is affected. It is a control whose sole effect is to echo itself.
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The stored tone is folded into the generation preamble (user_context.load_preamble) so every deliverable honours it, or the control is removed. Verified by generating the same deliverable under each tone and getting different prose.

### §9 — PARTIAL

- **claim:** "Accessible to all — all languages."
- **evidence:** lib/userPrefs.ts:22-35 offers 12 languages; lib/i18n.tsx:326 has dictionaries for 5 (en, ar, fr, es, ur) covering ~70 keys of UI chrome across a 99-page app. Direction handling is real (i18n.tsx:335 applyDocumentDirection sets dir on <html>) and coverage is honestly disclosed (Settings.tsx:112-125 uses coverageFor and says the interface stays in English). The avatar does pass language (useAvatarSe
- **user impact:** A user who sets Urdu gets Urdu navigation and an Urdu-instructed avatar, but every CV, care plan, lesson plan, legal draft and Genesis stage output comes back in English. The single sentence disclosing this lives on the Settings page; nothing at the 
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A `language` field (defaulted from userPrefs) is accepted by every generation endpoint and reaches the prompt, DomainTool sends it, and where the active resource cannot honour it the response says so at the point of use rather than only in Settings.

### §7 — DELIVERED

- **claim:** "Users access, select, reconfigure, and combine reconfigurable / rerunnable / reusable resources … with the platform modelling and simulating the configuration before commit."
- **evidence:** The full loop exists and is wired to the UI: pages/synthesis/ResourceFabric.tsx calls GET /api/v1/resources (194), GET /compositions (201), POST /compose/simulate (230), POST /compositions/{cid}/run (254), PUT /compositions/{cid} (270), DELETE (281), GET /compositions/runs (288), POST /compose (295). All eight routes are present in the live openapi (442 paths). Swarm cascades are definable and rec
- **user impact:** None — this section is done. A user can select resources, simulate a composition before committing it, save, re-run, reconfigure and delete it.

### §9 (personalisation input) + §4.2 — DELIVERED

- **claim:** The platform must "understand the person" and personalise to "each user's instructions … preferences, needs".
- **evidence:** W429/W428 verified live: GET /api/v1/user/profile returned the five-field empty profile; PUT with {about_you, goals} returned 200 and a preamble_preview "Take the following into account; it was written by the person you are answering. / About the person: A carer in Manchester / What they are trying to achieve: …"; a second GET showed it persisted. It is reachable — Settings.tsx:181 renders all PRO
- **user impact:** None on the input side — the field exists, persists, is deletable, and reaches generation. (Its rendering on the floor is the separate defect reported under §3A(1)/§13 above.)

---

## §8 (the biomimetic living organism) and §12 (the VSB economi

### §8 / §17.2 — PARTIAL

- **claim:** "The 7 biomimetic layers (Genome · Nervous · Immune · Cardiovascular · Respiratory · Musculoskeletal · Endocrine)" — the organism's anatomy, whose "organisation structure, resources, workflows and cascades mirror living systems".
- **evidence:** Live `GET http://127.0.0.1:8011/api/v1/organism/status` returns systems = immune, nervous, self_healing, metabolic, circadian, genome, reconfiguration. `GET /api/v1/organism/systems` returns exactly three: immune, nervous, self_healing. Grep for Cardiovascular|Respiratory|Musculoskeletal|Endocrine across agentic_core/api + agentic_core/organism returns ZERO hits; across all of agentic_core the onl
- **user impact:** A user who opens /organism to see the living body the product is named for sees four cards (Immune, Nervous, Self-Healing, plus metabolic/circadian/genome/reconfiguration rows). Three of the canon's seven layers have no representation at all and one 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** One authoritative source enumerates the seven §17.2 layers, each mapped to the concrete module(s) that realise it (Respiratory→agent_hub+swarm.cascade, Musculoskeletal→resource_fabric facilities, Cardiovascular→optimizer.allocate, Endocrine→biobus), 

### §8 / §17.2 — DOC_OVERCLAIM

- **claim:** W422: "THE RECORD NAMED SEVEN LAYERS AND ONE SHOWED UP. `layers` now means contributed" — the delivery record no longer implies seven layers participated.
- **evidence:** The backend fix is real (agentic_core/vbs/quality.py:226-248 emits layers=["Immune"], layers_declared, layers_not_contributing, layers_note). But it never reaches two of the three surfaces that render the badge. apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:678 still renders `title={`7 biomimetic layers · ...`}` and apps/workstation-superapp/src/components/organism/SwarmIntellig
- **user impact:** On the flagship Genesis page — the surface where a user watches their enterprise be born — hovering the organism badge still says the delivery was touched by 7 biomimetic layers when exactly one contributed a value. The correction landed on the least
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** GenesisJourney.tsx and SwarmIntelligence.tsx render the layer participation from `biomimetic.layers` / `layers_not_contributing` / `layers_note` rather than a hardcoded string; no frontend file contains the literal '7 biomimetic layers'; and a test a

### §8 / §17.2 — DOC_OVERCLAIM

- **claim:** The delivery record's own honesty note: "Respiratory, Musculoskeletal and Endocrine have no implementation at all." (agentic_core/vbs/quality.py:248, shipped in every delivery record as `biomimetic.layers_note`.)
- **evidence:** The statement is false as written, in three ways verifiable in the same repo. (1) Endocrine = §17.2's 'signal bus / shared context' — that is `agentic_core/organism/biobus.py`, and quality.py:236 fires a biobus signal TWELVE LINES ABOVE the note claiming Endocrine is unimplemented. (2) Respiratory = §17.2's 'autonomous workflow cascade / Agent Hub' — agentic_core/api/agent_hub.py is a real message
- **user impact:** W422 replaced an over-claim with an under-claim and shipped it into the record a user reads. Someone acting on this note would conclude three subsystems must be built from nothing, when the real defect is narrower and different: the subsystems exist 
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** `layers_note` states what is true — that these layers' functions exist under other names (naming the modules) but contribute no measured value to this record — or the record queries those modules so they genuinely contribute; and the note's factual c

### §8 — PARTIAL

- **claim:** W422: composite_health's simulated term is now named — "terms now named with weight/value/measured, plus composite_health_measured_only", so the score "must never again be presented as wholly measured".
- **evidence:** agentic_core/organism/biobus.py:220-226 adds `composite_health_measured_only` and `composite_health_terms` to `organism_context()`. Every route strips them: agentic_core/api/organism_status.py:203, :257 and :421 copy only `ctx["composite_health"]`. Verified live — `GET /api/v1/organism/status` top-level keys are [organism, version, timestamp, composite_health, mode, health_summary, systems, operat
- **user impact:** The disclosure exists only in a Python dict no caller reads. A user looking at the Organism page sees '91%' presented as the organism's measured health, one fifth of which is a number nothing measures — exactly the presentation W422 said must never h
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** /api/v1/organism/status and /health-summary carry composite_health_terms + composite_health_measured_only; the Organism dashboard shows the measured-only figure beside the composite and names the simulated term inline (not only in a tooltip); and a c

### §8 — STUB

- **claim:** "...and a survival instinct make it dynamic, adaptive, responsive — and defend itself"; §17.2 "+ homeostasis loops (immune↔nervous↔metabolic), circadian operation, and a survival instinct".
- **evidence:** The metabolic survival instinct is unreachable code. agentic_core/molecular/atp_simulator.py:20-24: `consumption = 0.1 * metabolic_load`, `production = 0.5 * circadian_efficiency`, `self.ratio += (production - consumption) * dt`. metabolic_load is bounded at 1.0 (agentic_core/ai/native/homeostasis.py:46 `load = max(0.2, min(1.0, ...))`; biobus default 0.3), so consumption ≤ 0.1; circadian_efficien
- **user impact:** The organism cannot defend itself along the axis the canon leads with. The energy model has no consumption path that can outrun production, so 'the organism is depleted, protect it' never fires — not under a heavy swarm, not under sustained load, nev
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** metabolic_load can drive consumption above production (rebalance the coefficients or scale consumption by real work units), so ATP genuinely falls under load and recovers at rest; a reproducible load scenario drives atp_ratio below 0.3 and is observe

### §8 — PARTIAL

- **claim:** "ATP Simulator — molecular energy model (real biomimetic calculation)" (agentic_core/app_mvp.py:400) feeding the platform-wide Live Biometrics surface.
- **evidence:** agentic_core/app_mvp.py:407 reads `round(max(0.0, min(1.0, biometrics_status._atp.ratio)), 3)` — it clamps the raw 0.5–15.0 simulator ratio to 1.0 WITHOUT the `/15.0` normalisation that agentic_core/organism/biobus.py:158 and :165 apply. Since the simulator initialises at 5.0 and only rises, this is pinned at 1.0 forever. Verified live, three consecutive calls to GET /api/v1/biometrics/status: `"m
- **user impact:** The 'Live Biometrics' panel reports the organism at 100% metabolic energy permanently — a constant dressed as a live molecular reading, on a page whose own W406 comment block explains why exactly this kind of fabrication is the worst kind. Three surf
- **refutation: SURVIVED** an independent refuter instructed to default to refuted
- **done when:** app_mvp.py:407 normalises by /15.0 like biobus; integration_surface.py:409 reads the shared singleton (`biobus._get_atp()`) instead of constructing a new simulator, or reports null; all ATP-reporting surfaces resolve to one value within rounding; and

### §8 — MISSING

- **claim:** "profitability, customer/user satisfaction, founder-alignment, and live compliance are all continuously monitored, evaluated, and improved."
- **evidence:** Three of the four have real machinery on the heartbeat: profitability (auto_economy → living_vsbs.operate_vsb), founder-alignment (auto_align → heartbeat.py:266-271), live compliance (auto_compliance → heartbeat.py:432 _compliance_beat + screen_living_vsb). Customer/user satisfaction has none. Grep for satisfaction|nps|csat (case-insensitive) across all of agentic_core returns exactly two hits: ag
- **user impact:** One of the four things §8 names as continuously monitored is not monitored at all. Nothing on the platform ever asks a user whether the thing it built for them was any good, and nothing feeds a satisfaction signal into the learning loop, the §10 bar,
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A real satisfaction signal is captured at the points a user receives value (deliverable, journey completion, marketplace purchase), persisted per-tenant, exposed on a route, surfaced on the Organism/Learning-Loop surfaces, and consumed by at least on

### §8 / §17.2 — PARTIAL

- **claim:** "1. Genome — VSB identity/capabilities/constraints/evolution" — layer 1 of the seven, reported as an organism system and pulsed every heartbeat.
- **evidence:** Live `GET /api/v1/organism/genome` → `{"genomes":[],"total":0}` on a server that has an established, living VSB. `GET /api/v1/organism/status` reports `"genome":{"total_genomes":0,"mean_fitness":null,"max_generation":0,"dominant_trait":null}`, and `GET /api/v1/heartbeat/status` reports `"last_genome":{"total":0,"mean_fitness":null,"max_generation":0}` every beat. The registry is empty because noth
- **user impact:** The organism reports a Genome system with zeros and a null mean fitness for a platform that has actually birthed an enterprise, and the heartbeat repeats those zeros every beat. The evolution primitives (crossover, mutate, fitness, generations) opera
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** VSB spawn / Genesis establishment encodes the entity into the organism genome registry (or the two stores are unified); /api/v1/organism/genome is non-empty after an establishment on a fresh data dir; organism status reports a real mean_fitness and m

### §12 (× §11) — PARTIAL

- **claim:** W421: "A HELD ENTERPRISE LOOKED IDLE TO ITS OWNER... list_living() now carries the verdict and economy_held with the CONSEQUENCE in words" — the entity's live compliance standing is now visible to its owner.
- **evidence:** Key mismatch between writer and reader. The writer, agentic_core/organism/heartbeat.py:78, stores exactly `{"overall", "last_at", "regression", "history"}`. The reader, agentic_core/economy/living_vsbs.py:89-90, reads `h.get("screened_at") or h.get("at")` and `h.get("verdicts") or []` — neither key is ever written at that level. Verified live: `GET /api/v1/economy/living-vsbs` → `{'verdict': 'revi
- **user impact:** The owner sees a bare verdict word with no date and no basis. A 'review' from four days ago is indistinguishable from one screened a minute ago, and an entity that REGRESSED from pass to fail looks identical to one that was always failing. W421 built
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** list_living() reads `last_at` (the key actually written) into screened_at, screen_living_vsb persists the per-framework `verdicts` from screen_compliance, `regression` is carried into the row and rendered distinctly; live GET /api/v1/economy/living-v

### §12 — PARTIAL

- **claim:** Each VSB "self-manages its finances: pays the Owner an adjustable profit share; reinvests in its own growth and in users; donates intelligently to causes".
- **evidence:** An entity's REAL earned revenue is invisible and cannot be distributed on demand. Revenue events are genuinely recorded — agentic_core/api/marketplace.py:445-446 (marketplace_sale) and agentic_core/api/swarm.py:862-869 (cascade_delivery tariff + cost). The only consumer of that pending intake is agentic_core/economy/living_vsbs.py:216-217 `peek_pending(vsb_id)` inside operate_vsb, which runs only 
- **user impact:** An entity sells something on the marketplace and earns real recognised WST. Its owner opens /economy, sees a zero ledger, and the only button available runs the waterfall on a figure they invent by hand. The money they actually earned is not shown an
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A route exposes peek_pending (pending intake with its source breakdown); /economy shows 'recognised revenue awaiting distribution: N WST' with its sources; POST /api/v1/economy/cycle can run on the entity's real pending events rather than a caller-su

### §12 — API_ONLY

- **claim:** "reinvests in its own growth and in users" — the self_investment and user_projects stages of the §4 waterfall.
- **evidence:** The backend is real and live: `GET /api/v1/economy/ventures/candidates` returned a genuine candidate derived from the platform's own living VSB (`{"id":"vsb:vsb-eebf118900","name":"ClearWell","kind":"living_vsb_offspring","score":0.6925,"metrics_source":"derived deterministically from live stage/status/governance","using_demo_candidates":false}`); `GET /api/v1/economy/ventures/portfolio` returned 
- **user impact:** Two of the five waterfall stages are the reinvestment engine, and a user can see the money leave for them and nothing after. There is no portfolio view, no list of what the entity invested in, no returns, and no period close — the growth loop the can
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** A Ventures/Portfolio surface under /economy renders candidates (with their deterministic metrics_source), current holdings, invested total and realised returns; the cycle report's venture_investment and capital_fund_contribution are displayed after a

### §12 — DOC_OVERCLAIM

- **claim:** "donates intelligently to causes by real-world urgency (WATER · Orphan · Conflict/disaster · Dawah; 100%-donation-only)".
- **evidence:** The backend is honest (W415): agentic_core/economy/charity.py:180-186 emits `method: "weighted rank over CURATED priority weights..."`, `weights_provenance: "curated — the 0..1 cause weights are editorial values... no needs, impact or trust data is measured or sourced"`, and per-grant `weights_source` plus `donation_100pct_verified: "not_checked"`. The frontend discards all of it. apps/workstation
- **user impact:** A user watching their enterprise give money away reads that the split was driven by urgency, gravity, reach and trust, and sees a score of 1.00 next to Clean Water. Those are editorial constants a maintainer typed; nothing measured any of them. And t
- **refutation: NOT individually refuted** (region cap) — treat as a lead, not settled
- **done when:** The charity grants panel renders `weights_provenance` and per-grant `weights_source` / `donation_100pct_verified` from the payload instead of a hardcoded caption; the 100%-donation control is labelled as a directive that is not verified; /api/v1/econ

### §12 — DELIVERED

- **claim:** "an autonomous, compliant, hybrid Waqf/Trust/Multinational economic entity... pays the Owner an adjustable profit share... Virtual/simulated money until the Owner directs real rails."
- **evidence:** Verified live end-to-end. `GET /api/v1/economy/entity-types` returns 9 real templates (sole, ltd, plc, trust, waqf, multinational, nonprofit, charity, waqf_ltd_hybrid) each with a distinct 5-stage waterfall summing to 1.0. `GET /api/v1/economy/waterfall?vsb_id=vsb-eebf118900` returns `entity_type_source: "living_registry"` and — passing `&entity_type=charity` to try to override it — still returns 
- **user impact:** None — this works, and the Owner-gated real-money boundary is stated plainly at the point a user would otherwise assume money moved. The honest zeros are the correct result of removing a fabrication, not a gap.

### §8 / §17.2 — DELIVERED

- **claim:** W420: five heartbeat autonomy flags switchable and persisted across restart — "once established it runs, maintains, defends, improves and grows itself".
- **evidence:** `GET /api/v1/heartbeat/status` live returns all five flags rendered (auto_ship, auto_evolve, auto_economy, auto_align, auto_compliance) plus `autonomy_persisted: true` and `autonomy_restored_at`. agentic_core/organism/heartbeat.py:449 declares _AUTONOMY_KEYS, :472-487 _load_autonomy restores them at construction (defaulting safely to False on a missing or corrupt store), :490-501 _save_autonomy wr
- **user impact:** None — a user can switch on each autonomous behaviour, is told what it does on the next beat, and the choice survives a restart. This is the §8 self-running claim actually working.

