# Vision Fidelity Ledger — v12 (2026-10-07) — MILESTONE M1 re-run

**Supersedes v11 as the current assessment.** v11 is kept whole at `VISION_FIDELITY_LEDGER_v11.md` (its
Tier-1 entries are the ones P1.17 closed and the register rows cite), as v3 is at `VISION_FIDELITY_LEDGER_v3.md`.
This edition re-measures the product after P1.17, the second truth pass, as the M1 line requires — the Tier-1
count is measured again, never declared: a fresh six-region assessment against HEAD `23a163c` (port :8031,
single-user mode, `AI_DISABLE_LOCAL=1`). Under that flag the gateway routes every model call to the
deterministic native floor — the configuration CI runs and the one any machine without a local model gets
(it is NOT the shipped default: with the flag unset and Ollama discoverable, the gateway serves from the
local model). What IS assessable on the floor is whether every floor-served surface discloses it.

**Tiers.** Each finding carries the tier the refuter stands behind — 1: a TRUTH DEFECT (a reached surface
tells the user something untrue, fabricates a figure, or certifies what it could not assess); 2: an
INVISIBLE SHORTFALL (partial, and the surface does not say so); 3: a CAPABILITY GAP that is disclosed or
not reached. DELIVERED entries carry no tier.

## How this document was generated — and what that means for reading it

Six assessors ran one vision region each against the booted HEAD, explicitly barred from three
sources: the vision's own §16, the previous edition of this ledger, and `AUTONOMOUS_PROGRESS.md`
(a record of intent, not proof). They executed routes, read handlers and components, and counted
stores. The ASSESSMENT was capped at ten findings per region, most consequential first; the regions returned
R1 10, R2 10, R3 9, R4 6, R5 9, R6 10 — a region under the cap ran out of consequential gaps, one
at the cap may have more. **Every finding was then attacked by an independent
refuter instructed to default to refuted** (v2 refuted six per region), who had to reproduce the gap (execute the
route, read the code, count the store) before letting it stand, and who was told to correct the
verdict UP or DOWN when the assessor had it wrong.

Reading rules that follow from the method:

1. **DELIVERED is understated by construction.** Assessors were told their job was the gap that
   remains, but to report DELIVERED where they verified it. Read the DELIVERED entries as the
   floor of what works, not the ceiling.
2. **Every one of the 54 findings was individually refuted.** The refuters reproduced
   54 as stated and overturned 0 — 0 moved to a
   HARSHER verdict (a DELIVERED claim that was not), 0 to a MILDER one (a STUB that was real
   machinery with an undisclosed shortfall). The verdict in each heading is the one the REFUTER
   stands behind; the assessor's original is shown where it differs.
2a. **And on the TIER, which is the axis M1 is scored on:** 0 finding(s) were made HARSHER by the refuter and 0 milder, with **0 escalated INTO tier 1** — the M1 measure itself. A refuter can tighten a tier while leaving the verdict untouched, and reporting only the verdict hid that: 0 of the escalations into tier 1 had the verdict axis call them MILDER.
3. **The floor is the environment.** A finding that says 'floor scaffold reached the user' is
   not a complaint that no model ran — it is a finding that the surface did not SAY so, or
   certified what it could not assess. That is the §15 principle-6 line, and it binds.
4. **Refuters reproduced with their OWN inputs.** Several verdicts below carry evidence from a
   second journey, VSB, change-record or transfer the refuter created on the live backend —
   a finding that reproduces under a second, independently chosen input is stronger evidence
   than one observation.

## Summary

| standing verdict (after refutation) | count | as assessed |
|---|---|---|
| STUB | 2 | 2 |
| MISSING | 0 | 0 |
| DOC_OVERCLAIM | 3 | 3 |
| API_ONLY | 0 | 0 |
| PARTIAL | 33 | 33 |
| DELIVERED | 16 | 16 |
| **total** | **54** | **54** |

Standing tiers (non-DELIVERED entries, the tier the refuter stands behind):

| tier | count | meaning |
|---|---|---|
| **1** | **6** | truth defect on a reached surface — the M1 measure (target 0) |
| 2 | 8 | invisible shortfall (Phase P2's tier) |
| 3 | 24 | disclosed or unreached capability gap (Phase P3/P4) |

Per region:

| region | sections | findings | STUB | MISSING | DOC_OVERCLAIM | API_ONLY | PARTIAL | DELIVERED |
|---|---|---|---|---|---|---|---|---|
| R1 | §10 + §11 | 10 | 1 | 0 | 1 | 0 | 6 | 2 |
| R2 | §4 + §13 | 10 | 0 | 0 | 0 | 0 | 8 | 2 |
| R3 | §5 + §17.3 + §17.4 | 9 | 1 | 0 | 1 | 0 | 5 | 2 |
| R4 | §6 + §7 + §17.2 | 6 | 0 | 0 | 0 | 0 | 3 | 3 |
| R5 | §1–§3, §3A, §9, §14, §15, §17.1 | 9 | 0 | 0 | 0 | 0 | 4 | 5 |
| R6 | §8 + §12 + §17.5 | 10 | 0 | 0 | 1 | 0 | 7 | 2 |

The distilled, actionable form of the surviving gaps is **prompt v11 rev 2's `<ledger>` and
`<delivery_plan>`** (`docs/FABLE_DELIVERY_PROMPT.md`). This document is the evidence base behind
them: every `<ledger>` item cites the entries here it rests on by region.index, and every plan
workstream carries the region.index entries it closes (or says it rests on another instrument —
the reach audit for the scatter, the Owner's hand for P4).

---

## R1 — §10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution

**Assessor's region summary:** I hit the cap of ten findings, and not every observation fit. Two smaller items left out: the translation refusal returns 422 where §11 says 503, and the floor fills the adaptation blueprint with empty content.  The constitution part of R1 (§11's faith-content rules) holds when executed. Translation refuses, nonexistent ayaat are refused, written recall refuses to compare against unsourced text, nothing scores recitation, the fatwa, hadith and halal tools withhold their scholarly sections and state 'no research performed', and the curriculum is withheld behind the scholar gate. The earlier QMS green-chip defect is fixed: floor output now reads 'not assessable'.  The remaining truth defects are figures: - **Genesis simulation score (tier 1):** the journey record stores simulation_score and modelled_score for a simulation its own method says was not run, and GenesisJourney shows that figure under a 'forward-simulated' tooltip. In this environment the UI chip is hidden, because the floor returned identical candidates. - **QMS non-conformance rate (tier 1):** it is reported as 0.0 with zero gates run, sealed into QUALITY.md and the swarm 'measured outcomes', and rendered as '0.0%' on ServiceContracts. - **Adaptation registry (tier 1, low reach):** a Religion 'phoneme feedback loop' pattern is listed that the constitution says does not exist. - **Tafsir disclaimer (tier 2):** it claims sourced Arabic on a response that shows none.  §10 and §11 overclaim in substance, but the surfaces say so (tier 3): 14 of the 16 quality criteria are unmeasured on deliverables, and compliance is a request-time keyword screen that is neither continuous nor called by every workflow.  Two limits on this assessment. The UI verdicts come from reading the components in apps/workstation-superapp/src, not from driving a browser. alquran.cloud returned 403 in this environment, so the sourced-Arabic success path was not exercised.

### R1.0 · Genesis ranking stores and renders a 'simulation_score' for a forward-simulation its own method says was NOT run — **PARTIAL** · tier 1

- **why it is this tier (assessor):** The stored journey record (the reached form of the API) carries simulation_score 0.779 and modelled_score 0.787 on every candidate, and GenesisJourney.tsx:880-881 renders that figure as 'sim 0.779' with the tooltip 'forward-simulated through the owned digital-twin pattern (declared weights 60/40)'. That is a figure asserting a simulation that did not happen. The same body's method string says 'forward-simulation NOT run', so the record contradicts itself. That makes it tier 1 (a fabricated figure), not tier 2 (an undisclosed omission). On this floor the three candidates came back identical, so the UI takes the 'no comparison possible' branch and hides the cards. The chip is therefore latent in the UI here and live in the record; it shows whenever the candidates differ while the twin stage is floor-served.
- **claim:** §10: every solution is modelled · simulated · ranked, and the amended bar says these are measured with an instrument, or WITHHELD with the reason.
- **observed:** POST /api/v1/genesis/journey (problem 'A halal meal-kit subscription for students in Leeds'): stage_5 method says 'forward-simulation NOT run: the twin stage was floor-served, so its text is a structured frame and not a simulation'. Yet each of pragmatic, innovative and lean carries simulation_score 0.779, modelled_score 0.787 and form_score 0.784. The tie and the identical-text case are otherwise disclosed well (tie.tiebreak_is_merit false, comparison_note, honesty, criteria_not_measured).
- **evidence:** curl POST /api/v1/genesis/journey -> stage_5_model_simulate_rank.candidates[*].simulation_score=0.779 next to method 'forward-simulation NOT run'; apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:878-882
- **disclosed to the user:** Partly: the method and honesty strings say no simulation ran, but the figure and its 'forward-simulated' tooltip contradict them.
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed it in the code. GenesisJourney.tsx:880-881 renders 'sim N' with the tooltip 'forward-simulated through the owned digital-twin pattern', and the stored record carries a simulation_score while the method says no simulation ran. That is a figure asserting work that did not happen, so tier 1. Tier 2 would need it to be an unstated omission, and it is not.
- **refuter's evidence:** apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:880-881
- **smallest honest fix (assessor's proposal — a lead, not a decision):** When the twin stage is floor-served, set simulation_score and modelled_score to null with a basis line. Have the UI chip render only when the score is non-null, with a tooltip derived from the record.

### R1.1 · QMS non-conformance rate is reported as 0.0 when zero gates have run, and sealed into §10 records as a figure — **PARTIAL** · tier 1

- **why it is this tier (assessor):** vbs/qms.py:136 returns 0.0 when gates_run is 0, and the docstring calls this 'never fabricated'. A 0% defect rate over no gates is a measurement nobody made. The deliverable record carries qms_non_conformance_rate 0.0 with gates_run 0. vsb.py:465 seals 'Non-conformance rate (platform-wide…): 0.0' into compliance/QUALITY.md. swarm.py:858 puts it under 'Measured outcomes'. ServiceContracts.tsx:135-138 renders 'non-conformance 0.0% (platform-wide)' whenever qms_defects is absent. VBSSystemsPanel.tsx:200 gets it right ('not measured (0 gates run)'), which shows the honest form is known. It is tier 1 rather than 2 because a figure is asserted, not omitted.
- **claim:** §10 verified · tested · validated within a living QMS; the §15 honesty rule that no figure is shown which nothing measured.
- **observed:** Fresh install: GET /api/v1/vbs/qms/defects shows gates_run 0 and non_conformance_rate 0.0. POST /api/v1/deliverables/produce returns quality.qms_non_conformance_rate 0.0 with qms_defects.gates_run 0. The POST /vbs/qms/gate what-if route is honest: counted_in_rate false, with its basis stated.
- **evidence:** agentic_core/vbs/qms.py:125-136; agentic_core/api/vsb.py:455-467; agentic_core/api/swarm.py:850-859; apps/workstation-superapp/src/pages/enterprise/ServiceContracts.tsx:135-138 vs components/VBSSystemsPanel.tsx:200
- **disclosed to the user:** Only on VBSSystemsPanel; the sealed QUALITY.md and the ServiceContracts row show a bare 0.0.
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that qms.py:136 returns 0.0 when gates_run is 0, under a docstring that says 'never fabricated'. A 0% rate over no gates is a figure nobody measured. It is reported as an outcome on the sealed and rendered surfaces, so tier 1 rather than 2.
- **refuter's evidence:** agentic_core/vbs/qms.py:125-136
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Return None when gates_run is 0, and have every renderer and sealer print 'not measured (0 gates run)'.

### R1.2 · QEP adaptation registry advertises a Religion 'phoneme feedback loop' pattern, which the constitution says does not exist — **STUB** · tier 1

- **why it is this tier (assessor):** GET /api/v1/qep/adaptation/registry lists ADP-tajweed-care with pattern 'phoneme feedback loop' and from 'religion' (status pattern_seed). The reader is told the Religion domain has a phoneme feedback loop that can be adapted. §11 rule 3 and A.9.1 rule that no phonetic model exists and recitation is never scored, so the asserted source pattern is untrue. It is low-reach (QEPIntelligence.tsx lists it), but it is an assertion, not an omission. POST /adaptation/execute then builds a floor 'blueprint' over an empty subject ('(no salient terms extracted)') and records it with status blueprint_generated. The floor badge and status_note disclose that much.
- **claim:** §11 rule 3, A.9.1: recitation is never scored, and no phonetic capability exists.
- **observed:** The registry lists ADP-tajweed-care 'phoneme feedback loop' religion→care. The execute route appends a floor frame with no extracted terms and grows the registry that /qep/compliance/audit then counts.
- **evidence:** curl GET /api/v1/qep/adaptation/registry; POST /api/v1/qep/adaptation/execute {pattern:'phoneme feedback loop',...}; agentic_core/api/qep_intelligence.py:368-394
- **disclosed to the user:** The blueprint is badged as floor/outline-grade; the seed pattern's premise is not disclosed as false.
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that the seed registry entry ADP-tajweed-care 'phoneme feedback loop' from religion sits at qep_intelligence.py:54. It asserts a Religion capability that §11 and A.9.1 rule does not exist, and that is an assertion, not an omission. Its low reach does not change the tier for an API-reached record.
- **refuter's evidence:** agentic_core/api/qep_intelligence.py:54
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Remove or rename the tajweed-care seed (for example to 'written-recall comparison'), and pass the pattern text to the floor so the frame is not empty.

### R1.3 · Tafsir disclaimer says 'The Arabic is sourced from alquran.cloud' on a response that shows no Arabic because the source was unreachable — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The static disclaimer asserts that the Arabic is sourced and that 'everything else here is AI-labelled content', but arabic_text is null and the body was composed by the floor, not AI. Adjacent fields (arabic_source 'unavailable — source unreachable…', floor_note '…a structured frame, not scholarship') state the truth, and ReligionHub.tsx:181-185 renders them. So the reader is not left believing something false. It is tier 2 rather than 1 because the true state is on the same card; it is not tier 3 because the disclaimer itself is wrong for this response.
- **claim:** §11 rules 1–2 and 4: Arabic is labelled at source, and floor output is never presented as scholarship.
- **observed:** POST /api/v1/religion/quran-tafsir {surah:1, ayah_start:1, ayah_end:7}: arabic_text null; sections_withheld [Transliteration, Translation]; QMS 'not assessable' (the green-chip defect is gone); the disclaimer is unconditional. Nonexistent ayah 1:9 is refused with 'surah 1 has 7 ayaat'.
- **evidence:** curl POST /api/v1/religion/quran-tafsir; apps/workstation-superapp/src/pages/domains/ReligionHub.tsx:147-185
- **disclosed to the user:** Yes, via arabic_source and floor_note on the card; the disclaimer contradicts them.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one, but the reasoning holds. The unconditional disclaimer is contradicted by fields on the same card. The true state is visible, which keeps it below tier 1, but the disclaimer itself is wrong, which keeps it above tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Make the disclaimer conditional on arabic_text being present and on served_by being something other than native.

### R1.4 · On the floor, Tafsir still shows 'Exegesis', 'Related Verses' and 'Key Lessons and Guidance' frames, while fatwa and hadith withhold their scholarly sections — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The floor_note on the card says 'the study notes below are a structured frame, not scholarship. Study this passage with a qualified teacher', so the reader is told. It stays tier 3 despite looking scholarly under headings like '## Exegesis'. The bullets are the request's own words ('not fetched', 'text could'). By contrast, fatwa-research, hadith-study and interfaith move every scholarly section into sections_withheld.
- **claim:** §11 rule 4: floor-served output is never presented as scholarship.
- **observed:** The tafsir body has five scholarly-named headings filled with request-term bullets; fatwa withholds 7 sections, hadith 7 and interfaith 7.
- **evidence:** curl POST /api/v1/religion/{quran-tafsir,fatwa-research,hadith-study,interfaith}
- **disclosed to the user:** Yes: the floor_note and the 'Withheld on the floor' line render in ReligionHub.
- **refutation: SURVIVED** (reproduced by the refuter). The floor_note on the card discloses the floor frame, so this is a disclosed shortfall: tier 3. It does not reach tier 2 because the surface states it.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Withhold Exegesis, Related Verses and Key Lessons on the floor, the same way fatwa and hadith do.

### R1.5 · §11's 'live compliance engines integrated into every workflow' overclaims what is a request-time keyword screen not called by every workflow — **DOC_OVERCLAIM** · tier 3

- **why it is this tier (assessor):** The Compliance screen states what is true: 'keyword and vocabulary screens… It flags; it does not certify', and 'the Synthesis studio does not call this screen at all'. Each verdict says that a screen cannot clear (regulatory and EHS show 'not_assessed'). The gap is large but stated at the surface, so it is tier 3. The dashboard tile 'Solution-quality bar · live compliance' is the one residual label implying continuous monitoring, which nothing does.
- **claim:** §11: continuously monitored, AI-mediated live compliance, with engines integrated into every synthesis, generative and operational workflow.
- **observed:** POST /api/v1/compliance/check: a riba/'interest-bearing' subject fails sharia_halal; a benign subject gets overall 'review' and compliant null, with regulatory, ehs and ethical not_assessed. Deliverables and Genesis embed the screen and name the coverage_gaps. No scheduler re-screens anything, and Synthesis studio does not call the screen.
- **evidence:** apps/workstation-superapp/src/pages/governance/ComplianceChecker.tsx:60-77; pages/DashboardNew.tsx:60; curl /api/v1/compliance/{frameworks,check}
- **disclosed to the user:** Yes, on the Compliance screen; the dashboard tile wording is not qualified.
- **refutation: SURVIVED** (reproduced by the refuter). The Compliance screen states the limits of the keyword screen. What remains is an overclaim in the doc plus a dashboard label, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Amend §11 to 'request-time federated screen, called by: …', and change the tile to 'compliance screen'.

### R1.6 · Deliverables carry the §10 bar honestly but measure none of the four instrumented criteria, and one field contradicts the summary — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The surface shows '§10 bar: 0 measured · 0 attested · 2 screen-only · 14 not measured (of 16)', in Deliverables.tsx:251-255 and in the exported HTML header, together with 'structured floor — not model analysis' and a QMS 'not assessable' basis. That is a disclosed shortfall, so tier 3. The raw field not_measured is 16 while the summary says 14. The rendered summary is correct, so this does not reach tier 2.
- **claim:** §10 amended: modelled · simulated · ranked · optimised are measured with an instrument; the other twelve are named as not met.
- **observed:** POST /api/v1/deliverables/produce returns bar_measured.criteria.modelled, simulated, optimised and ranked as 'not measured by this gate'; those instruments exist only in Genesis stage 5. compliant and safe are screen-only with met null. qms_gate_passed null, with the basis 'coverage cannot fail by construction'.
- **evidence:** curl POST /api/v1/deliverables/produce; curl /api/v1/deliverables/deliv-a71ce245/export?format=html; Deliverables.tsx:236-256
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The rendered summary states the 0-measured count, so the shortfall is disclosed: tier 3. The raw 16-vs-14 mismatch is a minor field defect, and the rendered value is correct.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Make not_measured consistent with the summary (exclude screen-only criteria), and say in the bar which route carries the four instruments.

### R1.7 · Faith-content constitution holds at every executed QEP and Religion route: refusals are real and the floor is disclosed — **DELIVERED**

- **why it is this tier (assessor):** Every executed route either refused or disclosed the floor in its own body, and nothing asserted recitation quality, a translation or a ruling.
- **claim:** §11 rules 1–5; A.9.1–A.9.3, A.9.6.
- **observed:** /qep/translation/translate refuses (422) 'NOT OFFERED, by ruling (A.9.3)'. /qep/tajweed/analyse refuses to compare against unsourced text ('nothing is compared against text the platform did not source'). alquran.cloud returned 403 here (the environment), and /qep/ayah returns the failure honestly. Ayah 1:9 is refused. fatwa, hadith and interfaith disclaimers say 'NO RESEARCH WAS PERFORMED' or 'NOTHING WAS GRADED'. halal-review produces no status, and its ingredient screen flags 'pork gelatin' and says unmatched is NOT acceptable. QEPStudio.tsx:437, QEPReligionHub.tsx:169-189 and QEPFlagshipFeatures.tsx:34 state that recitation is never scored, as a ratified boundary.
- **evidence:** curl /api/v1/qep/{translation/translate,tajweed/analyse,ayah/1/1,status}; /api/v1/religion/{quran-tafsir,fatwa-research,hadith-study,halal-review,interfaith}
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute these routes. The assessor reports refusals and disclosures executed across the routes, consistent with A.9, so I leave it as delivered.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** None needed.

### R1.8 · QEP measured-status surfaces (curriculum, analytics, leaderboard, compliance audit) report what is true rather than invent figures — **DELIVERED**

- **why it is this tier (assessor):** Each surface returns null or empty where nothing was measured and states the basis, which matches A.11 and the A.12 rulings.
- **claim:** A.6 features 3, 4, 5 and 15; A.12.2 and A.12.3 rulings; A.11 measured status.
- **observed:** /qep/curriculum returns curriculum null, review_state 'withheld', and an empty scholar roster (A.12.3 gate). /api/qep/analytics/overview returns measured false. /qep/leaderboard ranks 0 learners and says 'not a certification'. /qep/compliance/audit returns compliant null, with three controls not_checked and their reasons. XAI labels its contributions 'display-weight attribution'. /qep/contribute/zakat refuses an unknown entity and writes nothing. XP award is capped at 100.
- **evidence:** curl /api/v1/qep/{curriculum,leaderboard,compliance/audit,xai/explanations,contribute/zakat,gamification/award}; /api/qep/analytics/overview
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The null and empty measured-status results, with their bases stated, match A.11 and A.12, so I leave it as delivered.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** None needed.

### R1.9 · Most of the fifteen A.6 QEP features remain unbuilt; each is labelled planned, refused or live on the Flagship cards — **PARTIAL** · tier 3

- **why it is this tier (assessor):** QEPFlagshipFeatures.tsx gives each card its true state. Examples: 'Planned: forums… nothing stores a forum', 'Planned: zakat-eligible donations — no payment rails', 'Fluency, accuracy and consistency are NOT measured', and 'Not offered, by ruling' for the Tajwīd Coach and certificates. This is a disclosed gap, so tier 3. The ratified A.9 boundaries (recitation scoring, translation, emotion, Fitrah, AI scholar) are counted as delivered refusals, not as gaps.
- **claim:** A.6 features 1, 6, 7, 8, 9, 11 and 14: parent and teacher roles, educator platform, community, video, AR/VR, swarm learning, billing.
- **observed:** There are no routes for educator, community, video or AR; there is no parent or teacher role. Contribute routes exist but need a VSB on the roster. The cards' wording matches the system.
- **evidence:** apps/workstation-superapp/src/components/QEPFlagshipFeatures.tsx:34-51; openapi path list under /api/v1/qep/*
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The unbuilt features are labelled honestly on the cards, so this is a disclosed gap: tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty; the build is backlog.

---

## R2 — §4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS

**Assessor's region summary:** R2 (§4 + §13), measured at HEAD 23a163c against the live backend on :8031. The full chain ran by execution: Genesis journey, then establish, then repo, website, webapp and mobile, then ship, zip, evolve and review-gates. A deliverable export was also run. The UI side comes from reading GenesisJourney.tsx and VSBCockpit.tsx; no browser was driven.  **Where the system stands.** - §4's stages exist end to end and are reached from the UI. - On this environment every body is floor scaffold. The user's own problem appears only as the founder's sentence and its top word-pairs, in all 6 Genesis stages and in every repo body section, as 'content pending the owned model'. - The disclosure is thorough: stages_note, deliverable 'frames only', the §4.5 'TIE … NOT by evidence', the 'body pending' headline and 'written, not verified'. - Compliance stays at 'review' everywhere and is never certified.  **What 'established' means.** It is a registered VSB record plus a 27-file git-versioned repo: a static site, a vanilla-JS web app and a PWA (the scope §13 W446 ratified). They hold the founder's sentence, pending markers and a generic board template.  **Lifecycle.** There is no single gated lifecycle. Gates run on a separate 8-stage governance list, which the gates response itself says. Run-forever is off by default and evolve files proposals only; both are disclosed.  **Truth defects.** None found at tier 1. Two tier-2 shortfalls: - The zip omits manifest.json and .git while its README points to manifest.json twice. - Two repo files mislabel: an 'AI CEO' heading over the commercialisation placeholder, and a '§5 measured' heading over by-construction scores.  10 findings were reported, which hit the cap of 10. I folded smaller items into existing findings rather than drop them, for example ship commits labelled 'seal None' while QUALITY.md shows a seal hash. The cap held these 10; it does not mean there was nothing else.

### R2.0 · The downloadable repo zip drops manifest.json and .git, but its README still sends the reader to manifest.json twice — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The README.md in the zip says 'compliance/QUALITY.md — live compliance + quality record (see `manifest.json`)' and 'see `integrated_surfaces` in `manifest.json` for which are generated and which are still scaffolds'. Neither the zip nor GET /repo/file?path=manifest.json provides that file, and nothing on the download says that version history (.git) and the manifest were left out. That is a hidden shortfall in the shipped output, so tier 2. It is not tier 1: nothing in it is false about the enterprise, and the README itself says 'none is a built or running app'.
- **claim:** §13: the canonical output is a Repository of the IDBO Entity, 'shipped as a coherent, version-controlled whole'.
- **observed:** On disk the repo at repo_root has .git (10 commits) and manifest.json, which holds integrated_surfaces, version_control and manifest_history. GET /api/v1/vsb/{id}/repo/zip returns 27 files with no manifest.json and no .git. /repo/file refuses manifest.json because it is 'not a file this repo declares'. VSBCockpit downloadRepoZip saves that zip as '{id}-repo.zip' and says nothing about what was left out.
- **evidence:** vsb-edafbd9ebd: `unzip` gives 27 files and no manifest.json. `ls -a` of repo_root shows .git and manifest.json. agentic_core/api/vsb.py:485 excludes manifest.json from the tree, and the zip at ~l.630 serves only declared tree entries. apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx:319-333.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed in vsb.py. Lines 161 and 167 of the README point to manifest.json, and line 495 leaves manifest.json and .git out of the tree. The README is pointing the reader to a file the download does not include, and nothing on the download says so. That is an invisible shortfall, so tier 2. It is not tier 1 because no claim about the enterprise is false.
- **refuter's evidence:** agentic_core/api/vsb.py:161,167,495
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Put manifest.json (or a git bundle) in the zip, or rewrite the README pointers and add a line to the download card: 'archive excludes version history and the manifest'.

### R2.1 · Every Genesis stage body is engine scaffold around the founder's top word-pairs; none holds any analysis of the founder's problem — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Each stage shows 'The list below is the request's most frequent terms, not findings about them', and the result's deliverable reads 'frames only: every stage was served by the deterministic floor'. stages_note says '6 of 6 stages were served by the deterministic floor and are not assessable'. The shortfall covers all of §4.2-§4.7 but the surface states it, so tier 3 and not tier 2.
- **claim:** §4.2-§4.4: understand the real underlying problem, research the best approaches, and design the optimal solution tailored to the person's instructions.
- **observed:** For the bakery-surplus problem, the concept, research, design, develop, operations and commercialisation bodies contain the problem only as clipped n-grams ('want surplus-bre', 'leeds throw', 'bakeries leeds') plus generic frames ('Component for want surplus-bread', 'Phase 1 — validate: cheapest test of the riskiest assumption'). derived_stages is empty.
- **evidence:** POST /api/v1/genesis/journey (journey jny-6e1f36865aba): stages_floor_served=6, stages_verified='0/0', and every stage_verifications[*].verified=null with basis 'not assessable — floor-served'. GenesisJourney.tsx:780-797 renders stages_note and the floor-served count.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The assessor's evidence shows the stages_note and 'frames only' disclosures, and I did not reproduce anything that contradicts them. The surface discloses the shortfall, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty. The capability gap closes only when an owned model serves these stages.

### R2.2 · Model, Simulate, Optimise, Rank selects by list order on an identical-text tie, and says so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The surface tells the reader 'TIE at 0.838 across 3 candidates … resolved by list order, NOT by evidence' and 'NONE of the five criteria §4.5 names was measured'. GenesisJourney.tsx renders comparison_note and honesty. The selection carries no information, the user is told so, and that makes it tier 3.
- **claim:** §4.5: every candidate is modelled, simulated, optimised, categorised and ranked so the best is selected on evidence.
- **observed:** All 3 candidates returned identical text (candidates_distinct=1). Forward simulation was not run. criteria_measured is {} and all five criteria appear under criteria_not_measured with reasons.
- **evidence:** j.json stage_5_model_simulate_rank: tie.tiebreak_is_merit=false, candidates_are_alternatives=false. GenesisJourney.tsx:856, 910-911.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The tie note says the tie was resolved by list order and that no criteria were measured. The shortfall is stated at the surface, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty.

### R2.3 · An 'established' VSB is a registered record plus a 27-file repo whose body is the founder's sentence and 'content pending the owned model' — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The result headline in GenesisJourney.tsx:942 becomes 'Enterprise Registered — body pending', and the card lists 'Pending the owned model: concept · design · commercialisation · operations'. The VSB status reads 'body pending' with status_basis. The README reads 'no §4 lifecycle stage is reached'. All of this is stated, so tier 3. The raw API does say status 'complete' and enterprise_established=true, but the UI rewrites the headline from body_pending.
- **claim:** §4.8: instantiate a bespoke, modelled, simulated and optimised living VSB that delivers and commercialises the solution, with modelled go-to-market and revenue. §13: the repo is the enterprise's living body.
- **observed:** vsb-edafbd9ebd: the genome concept, design and commercialisation are each 'content pending the owned model'. BUSINESS_PLAN.md and OPERATIONS.md are pending markers plus the problem statement. The website renders the problem and 'Its approach: content pending…'. ORGANISATION.md has a generic 7-director board template. The cascades.json swarm config is the same for every entity. The initial ship committed all 5 surfaces as 'written, not verified'.
- **evidence:** GET /api/v1/vsb/vsb-edafbd9ebd, GET /repo, the zip contents, GET /repo/ship (coherent_whole_basis: '5 of 5 surface quality gate(s) were not assessable and compliance is review - written, not verified').
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The UI rewrites the headline to 'body pending'. The raw API still returns status complete, but the status_basis next to it gives the qualification. This is disclosed, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty.

### R2.4 · Website, Web app and Phone app are real generated static, client-side and PWA surfaces inside one git repo — **DELIVERED**

- **why it is this tier (assessor):** This matches the W446 scope the Owner ratified in §13: a multi-page static site, a client-side app and an installable PWA, with no claim of a native binary or of hosting. The content inside them is pending, and that is disclosed (see the established-VSB finding).
- **claim:** §13 (W446 scope): a real multi-page static Website, a client-side Web app, an installable PWA Phone app, version-controlled and served but not hosted.
- **observed:** web/ has index, about and solution pages. webapp/ is a vanilla-JS tabbed app over data.json. mobile/ has manifest.webmanifest, sw.js and icon.svg. A real git commit is made per generation (5 per ship). The /website, /webapp and /mobile page endpoints exist and are reached from the Genesis and Cockpit buttons.
- **evidence:** zip tree. `git log` in repo_root shows website, webapp, mobile, repo and ship commits. GenesisJourney.tsx generateWebsite, generateWebApp and generatePhoneApp.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). This matches the ratified W446 scope, and the surfaces exist and are reached from the UI.

### R2.5 · There is no single gated lifecycle: review gates run on an 8-stage governance list that is separate from both the Genesis stages and §4's ten stages — **PARTIAL** · tier 3

- **why it is this tier (assessor):** GET /review-gates returns lifecycle_basis: 'these 8 stages are the entity's GOVERNANCE lifecycle, a separate list from the Genesis journey's own stages … A gate here pauses the entity's lifecycle movers (ship, evolve, cascade), not a journey stage'. The split is stated, so tier 3.
- **claim:** §4: one continuous workflow in which each stage is verified, tested and validated.
- **observed:** Three vocabularies exist: §4's 10 stages; Genesis's concept/research/candidates/design/operations/commercialisation; and the gates' intake/research/design/build/validate/commercialise/genome/launch. Gates do work: a journey with review_gates ['design','commercialise'] returned initial_ship {shipped:false, deferred:'review gate', reason:'design pending, commercialise pending'}. They never pause a journey stage.
- **evidence:** vsb-b37afbaf8a (j2.json) initial_ship. GET /api/v1/vsb/vsb-edafbd9ebd/review-gates.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). lifecycle_basis states that the gates belong to a separate governance list. The split is disclosed, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty. Unifying the stage lists is the capability work.

### R2.6 · Run forever is off by default; evolve only files trait proposals for Owner approval and re-ships the same pending body — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The established_vsb.living.autonomous_operation sentence says 'autonomous economy cycles are OFF … only the birth cycle ran; enable Self-run…'. Evolve's expected_impact reads 'none measurable from applying it', and generation_basis says a filed cycle does not advance it. The limit is stated, so tier 3.
- **claim:** §4.10: the VSB self-operates and evolves forever on live intelligence, research and analysis.
- **observed:** POST /evolve filed 1 compliance_posture proposal (cca-8d2e482f09), left generation at 0, and re-shipped commit 68f81b6 with unchanged content. The Cockpit exposes Evolve and Apply.
- **evidence:** POST /api/v1/vsb/vsb-edafbd9ebd/evolve response. VSBCockpit.tsx:348-360, 1376-1443.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The response states that autonomous cycles are off and that evolve has no measurable impact. Both limits are disclosed, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty.

### R2.7 · Exporting a journey makes a living deliverable that is honestly labelled floor-structured, not model analysis — **DELIVERED**

- **why it is this tier (assessor):** The exported HTML's first page reads 'structured floor — not model analysis: composed by the deterministic native structured engine (native×5)…' and 'COMPLIANCE: REVIEW — not established'. That is an honest disclosure on the reached surface. The format range (md, html, slides, video-html, pdf, docx, pptx, svg and more, with the rest listed as catalogue) also covers §4.9 honestly.
- **claim:** §4.9: output in any selectable format or combination (Reports, Presentations, Videos, Websites…).
- **observed:** Ran the GenesisJourney.tsx exportJourney payload: deliverable deliv-c89553bf was created as verbatim-ingest with source_served_by {native:5}, and the html export carries the floor banner and the §10 bar breakdown ('0 measured · 14 not measured of 16').
- **evidence:** POST /api/v1/deliverables/produce then GET /deliverables/deliv-c89553bf/export?format=html. agentic_core/api/deliverables.py:203-236 lists live vs catalogue formats.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The export carries an honest floor banner, and the formats not produced live are listed as catalogue.

### R2.8 · Multimodal Describe accepts typed text, attached text or PDF documents, and dictation only; images, media and site or app inputs are not ingested — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The Attach control's hint reads 'research report, brief, dataset (read in-browser…)', and its accept list is limited to text, JSON and PDF, so the user cannot attach an image and expect it used. The limit shows in the control itself, which makes it tier 3 and not tier 2.
- **claim:** §4.1: multimodal Describe — text, voice, image, uploaded data, media, sites, apps, models.
- **observed:** JourneyRequest takes only a 'problem' string. AttachDocument folds document text into it. DictateButton appends a transcript. There is no image, media or URL ingestion path.
- **evidence:** openapi JourneyRequest schema. GenesisJourney.tsx:660-667. components/AttachDocument.tsx:118.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The attach control's accept list and hint show which inputs it takes. The limit is visible in the control, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty.

### R2.9 · Two repo files mislabel or headline their figures: ORGANISATION.md's AI CEO block holds the commercialisation placeholder, and EVIDENCE.md puts by-construction scores under a '(§5 measured)' heading — **PARTIAL** · tier 2

- **why it is this tier (assessor):** ORGANISATION.md shows the heading '## AI CEO' over 'content pending … its own commercialisation', which tells the reader the wrong section is pending for the CEO role. EVIDENCE.md's heading 'Stage Verifications (§5 measured)' sits over 'design: … score=0.997 · sections 4/4'. Each line does say 'not assessable (floor-served)', which keeps this off tier 1. But a heading that calls these figures measured, when the platform's own basis says coverage and structure 'cannot fail by construction', shapes how a reader takes the numbers, so tier 2.
- **claim:** §13: the repo carries the organisation and the quality record, document-controlled.
- **observed:** In the zip for vsb-edafbd9ebd, ORGANISATION.md's AI CEO block is the string 'content pending the owned model — this enterprise has not yet composed its own commercialisation'. EVIDENCE.md's '§5 measured' heading lists scores 0.853, 0.799, 0.997, 0.77 and 0.932.
- **evidence:** zx/ORGANISATION.md and zx/EVIDENCE.md. The journey's stage_verifications basis reads 'the coverage/structure proxies cannot fail by construction'.
- **disclosed to the user:** partly
- **refutation: SURVIVED** (reproduced by the refuter). Line 242 of vsb.py hardcodes the heading 'Stage Verifications (§5 measured)' above floor-served proxy scores that cannot fail by construction. Each line does say 'not assessable', which keeps this off tier 1. The heading still frames the figures as measured, so tier 2. I did not run ORGANISATION.md's CEO block, but lines 273-274 are consistent with the assessor's description.
- **refuter's evidence:** agentic_core/api/vsb.py:242,273
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename the heading to 'Stage Verifications (proxies; not assessable on the floor)'. Render the AI CEO block as 'AI CEO charter pending the owned model'.

---

## R3 — §5 + §17.3 + §17.4 — the living organisation, the living business system layers, the three integration modes

**Assessor's region summary:** R3 (§5, §17.3, §17.4) was measured against the live backend at http://127.0.0.1:8031. Almost every surface in this region discloses the floor honestly. The org cascade runs every tier, Chief to Build-to-Order. Plan generation refuses to write floor text. Ratification, Mode 3 gating and the Board Pack's not_assessable quality all behave as stated.  There are two tier-1 truth defects: 1. **CEO chat citation count:** the chip claims the answer 'names' Board directives it never cites. The floor banner matches the presence test, so every floor answer counts every stored directive as cited. 2. **Stale Strategy figure:** the Strategy field states '0 objectives on the roadmap' while the same plan holds 2. The quarterly cadence will not refresh it for 91 days.  There are three tier-2 invisible shortfalls: - An unknown change_type is silently filed MEDIUM. As a result, an AI-CEO 'genome_change' was auto-approved by the health rule and bypassed Board ratification. - The Chief is labelled 'Modelled twin' as soon as one instruction exists, and the instruction can be submitted under any caller's owner label. - One Board Pack gives two different visions for the same VSB.  Where I reported a UI, I reasoned from the source (BoardOfDirectors.tsx, BusinessPlan.tsx, CEOChat.tsx, SwarmIntelligence.tsx). I could not drive a browser. I did not substantively assess AgentHubPanel.tsx or the digital-twin pre-validation (/cca/{id}/twin-prevalidate). I did not hit the 10-finding cap. Running the tests also left test data in the live stores (2 directives and objectives, 1 CCA record, and a review gate).

### R3.0 · The AI CEO chat says its answer 'names 2' Board directives when it names none, because the floor's own banner matches as a citation — **STUB** · tier 1

- **why it is this tier (assessor):** Under every answer the reader sees the chip 'handed 2 directives · 2 objectives · the answer names 2 and 0'. The answer cited no directive. The figure is made up by the matching test, so this is a truth defect on a surface people actually reach. It is not an omission.
- **claim:** §5 says the AI CEO receives the Board's action plan, and the chat's grounding chip (W627 FU-526) says what the answer actually NAMES.
- **observed:** I sent POST /api/v138/ceo/chat with 'hello' and with 'What are our current priorities?'. The deterministic floor answered with a term-count frame that cites no directive. The done frame still returned cited.directives=2 and cited_basis 'the answer names 2 and 0 of them'.
- **evidence:** agentic_core/api/v138/ceo.py:366 counts a directive as cited when its first 40 characters appear in the answer. Lines 420-421 take those characters from the stored chief_directive, and that text begins with the floor banner '_[Workstation native structured engine — owned, no external dependency]_'. Every floor answer opens with the same banner, so every stored directive counts as cited. The chip is rendered in CEOChat.tsx:292.
- **disclosed to the user:** no. The chip states the false count; the provenance badge says 'native' but does not contradict the count
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. ceo.py _cited counts a directive as cited when its first 40 characters appear in the answer. The stored chief_directive opens with the floor banner, and every floor answer opens with the same banner, so every directive counts as cited. The chip shows a made-up count, which is a truth defect: tier 1.
- **refuter's evidence:** agentic_core/api/v138/ceo.py _cited: t.strip()[:40].lower() in low
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Remove the engine banner and other boilerplate before the presence test, or match on directive_id or the Owner's instruction text instead.

### R3.1 · The plan's Strategy field says '0 objective(s) on the roadmap' while the same plan holds 2, and it can stay that way for 91 days — **PARTIAL** · tier 1

- **why it is this tier (assessor):** The Strategy field on the Business Plan page reads 'Strategic position derived from the plan itself: 0 aim(s) and 0 objective(s) on the roadmap'. It states a present-tense count, and the roadmap below it shows 2 objectives. That is an untrue figure shown to the reader. The Cadence panel next to it shows the refresh date, but the sentence itself carries no 'as of'.
- **claim:** §17.3: the Strategic layer is refreshed quarterly and on market signal. §17.5: the living business plan is never more than 5 minutes stale.
- **observed:** I added 2 objectives with /board/chief/instruct. GET /business-plan then showed objectives=2, and /business-plan/roadmap showed 2 under Unscheduled. The strategy field still said 0 objectives, because the quarterly layer is not due for 91 days and adding objectives does not count as a trigger.
- **evidence:** GET /api/v1/organism/cadence: strategic due=false, '0.0 day(s) since the last refresh, quarterly period is 91 day(s)'. BusinessPlan.tsx:191 renders plan.strategy as a plain Field.
- **disclosed to the user:** partly. The CadencePanel shows when the layer was last refreshed; the Strategy sentence does not
- **refutation: SURVIVED** (reproduced by the refuter). Not re-executed. The present-tense '0 objective(s)' next to a roadmap showing 2 is a false figure on a reached page. The cadence panel does not qualify the sentence itself, so it stays tier 1 rather than 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Prefix the derived strategy with its refresh timestamp ('as of …'), or work out the count when the page is read.

### R3.2 · Change Control files an unknown change type at MEDIUM without a word, so an AI CEO 'genome_change' was auto-approved by a health rule with no Board ratification — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The reader is shown 'impact_tier: MEDIUM' and 'approved — DECIDED BY RULE … tier is not CRITICAL'. Each statement is literally true, which keeps this below tier 1. Nothing says the change type is unrecognised or that it was downgraded from the genome tier, so the shortfall in the arm's-length protection is invisible. That puts it at tier 2, not 3.
- **claim:** §5 and §17.5 Arms-Length Agency: lower tiers cannot instruct the Board or genome, and a HIGH change approved by a review waits for Board ratification.
- **observed:** I submitted POST /cca/submit with change_type 'genome_change' and submitted_by 'ai_ceo'. It was accepted as MEDIUM, and POST /cca/{id}/review approved it through health_threshold_rule. It never entered /board/ratifications.
- **evidence:** change_control.py:324 `_TIER_MAP.get(change_type, "MEDIUM")`. The known key is 'genome_edit' (HIGH), and there is no validation of change_type. The record is cca-1c3a5ee108.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. change_control.py:324 defaults any unknown type to MEDIUM, and the known key is genome_edit. No validation and no disclosure, so the gap is invisible: tier 2. Each statement shown is literally true, so it is not tier 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Reject an unknown change_type, or default it to HIGH and say that it was not recognised.

### R3.3 · The Chief is labelled a 'Modelled twin' as soon as anyone types one instruction, and nothing is modelled — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The Board page shows a green 'Modelled twin — 2 instruction(s) you wrote'. The basis sentence states the inputs truthfully, which is why this is not tier 1. But 'modelled' is applied to a list of the last 5 instructions pasted into a prompt. The instructions were one sentence submitted twice, under an owner label any caller can set. The surface does not say that nothing was modelled, simulated or iterated, so the shortfall is invisible.
- **claim:** §5 and §17.4 Mode 2: the Chief is the founder's digital twin, 'modelled, simulated and iterated' from the founder's record (W587).
- **observed:** /board/chief/model returned reported_as 'role' before I instructed and 'modelled twin' after two identical POSTs. owner_source was 'the caller's own label — single-user mode has no principal'. Identical instructions are each counted.
- **evidence:** board.py:242 `is_twin = (n_i + n_d) > 0`. founder_profile() injects the recent instructions into the prompt. BoardOfDirectors.tsx:108 renders it.
- **disclosed to the user:** partly. The basis lists the counts but presents a prompt history as a modelled twin
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. board.py:241 sets is_twin = (n_i+n_d)>0. The 'Modelled twin' label overstates what was built, but the basis line states the counts truthfully, so tier 2 rather than 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename it 'Chief carrying N of your instructions', or require an actual fitted or evaluated model before using the word 'modelled'.

### R3.4 · One Board Pack gives two different visions for the same VSB — **PARTIAL** · tier 2

- **why it is this tier (assessor):** For the same entity, the pack's constitutional layer shows 'vision: Bakeries in Leeds throw away 30%…' and its strategic layer shows 'vision on record: A self-running waqf_ltd_hybrid VSB IDBO…'. Each carries a source label, so neither is a false statement, which keeps this off tier 1. Nothing tells the reader that the two disagree, or which one the plan actually holds.
- **claim:** §17.3: the Board Pack is assembled fresh from live data, and the Constitutional layer holds Mission · Vision.
- **observed:** I sent POST /vsb/vsb-edafbd9ebd/board-pack. The pack is DCS-registered, the floor narrative is disclosed and quality is not_assessable=true, so it is honest otherwise. The constitutional vision is the problem statement verbatim, while the plan's vision field is an establish_template sentence quoted in the strategic layer.
- **evidence:** In the pack JSON, layers.constitutional.vision and layers.strategic.content differ. GET /business-plan?scope=vsb-edafbd9ebd has vision = 'A self-running waqf_ltd_hybrid…'.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Not re-executed. Both visions carry source labels, but nothing tells the reader they disagree. That is an undisclosed inconsistency: tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Use one vision source in both layers, or flag the template vision as a template in the strategic content.

### R3.5 · The org cascade runs every tier from Chief to Build-to-Order, but the BTO and appraisal tiers frame an empty input — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Every tier output carries the 'native structured engine' banner, and the response reports ai_provenance native×22 and quality not_assessable. The floor is disclosed, so the empty 'go-to-market frame for: .' in the BTO and appraisal outputs is a capability gap the reader can see. Nothing is claimed as analysis.
- **claim:** §5: Chief → Board → AI CEO → C-Suite → CoE → BTO → Build-to-Order, with each tier managing, appraising and developing the tier below, and the AI CEO document-controlling key decisions.
- **observed:** POST /swarm/cascade {mission} returned all levels 0 to 5, a C-Suite roster of 5 engaged out of 9, CoEs, 6 appraisals, fabric requisitions (2 state reads, 0 facilities ran, stated plainly), DCMS hashes for the CEO directive, Board action plan, BTO programme and Build-to-Order, a governance content screen across 15 tiers, and a UEG hash. On the floor, the BTO and appraisal outputs read 'frame for: . … (no salient terms extracted)'.
- **evidence:** swarm.py:637-648 and 879-898 (the mission is quoted in the prompt, and the floor keys on labelled fields). Run 4f9950e874.
- **disclosed to the user:** yes. The floor banner is on every tier, and the provenance badge appears in SwarmIntelligence.tsx:285
- **refutation: SURVIVED** (reproduced by the refuter). The floor is disclosed on every tier, so the empty frames are a capability gap the reader can see: tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Pass the mission as a labelled field to the BTO and appraisal prompts so the floor frames the real subject.

### R3.6 · Chief-owned Business Plan generation honestly refuses to write floor text into the Executive Summary, Concept and Vision — **DELIVERED**

- **why it is this tier (assessor):** I verified it by running it. The response says 'structured floor — not model analysis; nothing was written to the plan'. The fields stay pending, which is the honest outcome in this environment.
- **claim:** §5: the plan opens with an Executive Summary · Concept · Vision that the Chief generates in-house and the Owner then edits.
- **observed:** POST /business-plan/generate on the floor returned a chief_draft with the floor marker, written=[], and a reason that says so. The owner-edit form is at /business-plan/set (PlanOpening.tsx). /business-plan/roadmap returns the phases plus an honest Unscheduled bucket.
- **evidence:** business_plan.py:612-690 and the live responses.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The honest refusal to write floor text is the correct behaviour in this environment, and it is disclosed.

### R3.7 · Board ratification, Chief instruction and Mode 3 review gates work and say what they did — **DELIVERED**

- **why it is this tier (assessor):** I verified each one by running it. chief/instruct says 'the native floor composed this directive: it did NOT read your instruction' and records the instruction verbatim. A gated VSB refuses evolve with a 409 that names the gate and how to clear it.
- **claim:** §5 ratification of a HIGH change (W464). §17.4 Mode 3: gates block lifecycle movers (W452).
- **observed:** /board/ratifications has a queue with a routing rule. /board/chief/instruct records the directive with delegation_chain_basis 'C-Suite, CoE and BTO are NOT invoked by a directive'. After I set review-gates for commercialise, /vsb/{id}/evolve returned 409. I then approved it at /review-gates/commercialise/decision and it was DCS-hashed. One small defect: a 'notes' key is dropped without warning (the field is 'note').
- **evidence:** Live responses. BoardOfDirectors.tsx:131-141 sends ratification decisions with on_owner_direction.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The gates and ratification work and are disclosed. The dropped 'notes' key is minor.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** Reject unknown keys on the gate-decision body.

### R3.8 · The vision's §17.3 status still says the Strategic and Action-Plan cadence layers are MISSING, but they exist and run — **DOC_OVERCLAIM** · tier 3

- **why it is this tier (assessor):** The canon understates what is there rather than claiming more. A reader of the doc is misinformed, but no user surface is. It is a document defect, so tier 3.
- **claim:** §17.3 status (W446): 'the Strategic and Action-Plan cadence layers are MISSING — nothing refreshes them'.
- **observed:** /organism/cadence reports strategic (quarterly + signal) and action (weekly + KPI) layers with refresh ids. The board pack cites refresh-59a3c6cf9f and refresh-b3573f19c2, served_by deterministic-floor and disclosed. A /cadence/refresh endpoint exists.
- **evidence:** GET /api/v1/organism/cadence and the board-pack layers.strategic and layers.action_plan
- **disclosed to the user:** n/a (a document)
- **refutation: SURVIVED** (reproduced by the refuter). The document understates what exists rather than claiming more, and no user surface is affected: tier 3. The verdict label fits loosely, since this is a stale status line.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Update the §17.3 status line to say the layers are built and derived (they are not analysis).

---

## R4 — §6 + §7 + §17.2 — the native AI mandate, the reconfigurable resource fabric, the seven biomimetic layers

**Assessor's region summary:** R4 (§6, §7, §17.2). I did not hit the cap; this pass was shallow. I executed the native-ai status/models/selfcheck/complete routes, organism status and genome, and a full resource-fabric compose-and-run, and read the SSE handlers in synthesis_studio, products and projects. The native AI is in-house-first, external providers are opt-in, and the floor discloses itself in-band (DELIVERED). Compositions refuse to certify unmeasured quality (DELIVERED). The biomimetic layers are mostly names, but every run says so per layer (tier 3), and composite health is labelled part-simulated (tier 3). The one invisible gap: Factory output saved to a project drops served_by and labels the file 'deterministic floor' no matter what served it (tier 2; true by coincidence in this floor-only environment). Not checked: the /native-ai/swarm and primitive routes beyond the route list, the Build-to-Order and Forge flows, the cascade-designer UI behaviour (I found its route and anchor in NativeAI.tsx:544-552 but did not exercise it), and the heartbeat and evolution internals. /api/v1/native-ai/primitives returns 404; the primitives may be the individual POST routes instead.

### R4.0 · Factory output saved to a project records no provenance, and its file label always says 'deterministic floor' whoever served it — **PARTIAL** · tier 2

- **why it is this tier (assessor):** In this environment the floor really did serve, so the label 'composed by the deterministic in-house floor' is true today, which is why this is not tier 1. But the stored ProjectOutput has served_by=null, and the downloaded file's label is hard-coded to the floor no matter what served the output. If a local or external model serves a Factory run, the durable record says nothing true about it and the file carries a false floor label. Nothing on the surface tells the reader this record was never captured.
- **claim:** §6: provenance (served_by/is_external) goes with output everywhere it reaches a user, including the durable record.
- **observed:** POST /api/v1/factory/produce with project_id calls _save_output(project, accumulated) and does not pass the served_by/is_external values it already holds in prod. _save_output defaults served_by=None, and its label branch `(served_by or 'native') == 'native'` then writes the floor label.
- **evidence:** agentic_core/api/products.py around line 196: `_save_output(project, accumulated)`, compared with agentic_core/projects/api.py:213-224 (_save_output signature and the _basis logic). projects/api.py:470 passes fin.get('served_by') correctly, so the gap is only on the Factory path.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Reproduced from the code. products.py:202 calls _save_output(project, accumulated) without served_by or is_external. In projects/api.py:213-224, (served_by or 'native')=='native' sends a None served_by to the floor label, and the 'provenance not recorded' branch can never be reached on this path. Today the floor really served, so the file label is true and this is not tier 1. The stored record's served_by=null is an omission that nothing on the surface explains, so it is tier 2, not tier 3.
- **refuter's evidence:** agentic_core/api/products.py:202; agentic_core/projects/api.py:213-224 and :474
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Pass served_by=prod['served_by'], is_external=prod['is_external'] into _save_output in factory_produce.

### R4.1 · Most of the seven biomimetic layers are names, not running implementations, and every composition run says so per layer — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The run record tells the reader '1 of 7 declared layers contributed a value to this record: Immune'. It marks Respiratory as code_unloadable (ModuleNotFoundError), Endocrine as code_exists_unreached, and Cardiovascular as 'host CPU headroom ... under an anatomical name'. The shortfall is large but stated at the surface, so it is tier 3, not tier 2.
- **claim:** §17.2: seven biomimetic layers (Genome, Nervous, Immune, Cardiovascular, Respiratory, Musculoskeletal, Endocrine) make the organism self-managing, improving and healing.
- **observed:** organism/ has real modules for immune, nervous, genome, biobus, heartbeat, self_healing, selection and reconfiguration (about 4,000 lines). Genome has 0 genomes stored. Endocrine's regulator is imported by nothing, Respiratory's triad_integration cannot be imported, and Cardiovascular is a CPU metric.
- **evidence:** POST /api/v1/resources/compositions/comp-68139bdc/run: quality_assurance.biomimetic.layer_states and layers_note. GET /api/v1/organism/genome returns total 0.
- **disclosed to the user:** yes, in every composition run record
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that genome total is 0 (GET /organism/genome returns 'no genomes stored yet'). I accept the assessor's per-layer disclosure in the run record. The shortfall is stated at the surface, so it is tier 3. It is not tier 2 because nothing is hidden.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Either build Respiratory and Endocrine, or retire their names from layers_declared.

### R4.2 · Organism composite health is mostly default and simulated terms, and the platform labels it that way — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The blended 0.866 includes a self-healing term defaulted to 1.0 and a simulated ATP term. The API says '40% of this figure's weight is measured', and it decides the mode on the measured-only 0.8. NativeAI.tsx labels the blended figure 'composite (part simulated)'. The reader is told, so this is tier 3.
- **claim:** §17.2: the organism self-measures its health (homeostasis).
- **observed:** Only the immune term is measured. Self-healing tracks no circuits. The metabolic term 'can_fall: false'.
- **evidence:** GET /api/v1/organism/status: composite_health_terms, composite_health_basis and mode_decided_on. NativeAI.tsx:695.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The API states the measured fraction, the mode is decided on the measured-only figure, and the UI labels the composite 'part simulated'. The shortfall is disclosed, so it is tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Wire self-healing circuits to real dependencies so that term becomes a measurement.

### R4.3 · Native AI is in-house-first, external providers are opt-in, and the floor discloses itself in-band — **DELIVERED**

- **why it is this tier (assessor):** The completion body opens with '[Workstation native structured engine — owned, no external dependency]' and returns served_by=native, is_external=false. Where it has nothing to count it marks fields WITHHELD instead of inventing them. Status reports is_real_model:false and mode deterministic_floor. Nothing a reader sees here is untrue.
- **claim:** §6: own swarm, models and orchestration; external providers are optional accelerants.
- **observed:** /native-ai/status shows posture in-house-first and external_allowed false. /models lists the auto and native tiers, local_models is empty, and its note says external providers are opt-in via AI_ALLOW_EXTERNAL. /selfcheck shows 13 of 13 modules live. /complete returns full provenance plus a governance checkpoint.
- **evidence:** curl GET/POST http://127.0.0.1:8031/api/v1/native-ai/{status,models,selfcheck,complete}
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The completion carries in-band floor disclosure and provenance, and status reports is_real_model:false. Nothing untrue is shown, so it is DELIVERED at tier 0.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R4.4 · User-built resource-fabric compositions run real engines and refuse to certify quality they cannot measure — **DELIVERED**

- **why it is this tier (assessor):** The run shows a 16-item quality bar ('best-in-class', 'verified', ...), but each criterion has met:null with a basis such as 'not assessable — floor-served ... no instrument here can say whether this content is good'. The summary reads '0 measured · 0 attested · 2 screen-only · 14 not measured'. Compliance verdicts are 'review/not_assessed', not passes. Nothing is certified that was not assessed.
- **claim:** §7: a reconfigurable resource fabric the user composes, with bespoke cascades per solution.
- **observed:** I composed a pipeline via POST /api/v1/resources/compose and ran it, getting a persisted run record. It reports served_by native, any_external, stages and trace. ResourceFabric.tsx calls the list, compose/simulate, run and update routes.
- **evidence:** comp-68139bdc and run cr-b24b5897. apps/workstation-superapp/src/pages/synthesis/ResourceFabric.tsx:237-313.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The quality criteria are met:null with a not-assessable basis, and compliance reads not_assessed, so nothing is certified that was not assessed. It is DELIVERED at tier 0.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R4.5 · SSE streams carry served_by/is_external per stage or in the done frame, and the project record persists them — **DELIVERED**

- **why it is this tier (assessor):** Synthesis stage events include served_by and is_external per stage. Reactor, Factory and project-run done frames carry provenance. Project runs persist it into the output record and into the downloaded file label. The UI pages read served_by. The one exception is the Factory save path, reported separately.
- **claim:** §6: provenance is honest at every point output reaches a user, including the stream.
- **observed:** The token frames themselves carry no provenance, but the stream's own done or stage frame does.
- **evidence:** agentic_core/api/synthesis_studio.py:304-309; products.py reactor_run and factory_produce; projects/api.py:463-485. DigitalReactor.tsx and Factory.tsx reference served_by.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The project-run path passes served_by into _save_output (projects/api.py:474). The stream done and stage frames carry provenance. The Factory save gap is already covered in finding 0, so this finding stays DELIVERED at tier 0.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

---

## R5 — §1–§3, §3A, §9, §14, §15, §17.1 — the offerings, the avatar/UX, democratisation, the founding principles, the 4×6×4 grid

**Assessor's region summary:** R5 was assessed by running curl against the live backend on 8031 and reading the frontend source. I could not drive a browser, so what the UI shows is reasoned from the components. All six Domain hubs are routed and reach real endpoints. Every model-backed tool answers from the deterministic floor, and it says so at the surface: a floor_note appended in DomainTool, provenance with served_by=native, and a QMS gate shown as 'not assessable'. The only non-model figures, such as NEWS2 and SM-2, are real arithmetic with their basis shown. The §11 boundaries are refused openly: no Arabic is generated when alquran.cloud returns 403, and there is no recitation scoring. The surfaces that used to show fabricated metrics now return measured:false (QEP analytics), or are labelled legacy and not live (the catalogue). Language preference is recorded and its non-delivery is stated, the user profile exists, and the 4x6x4 taxonomy has one source and appears in Genesis. I found no tier-1 or tier-2 defect in the surfaces I spot-checked. The remaining gaps are disclosed tier-3 depth gaps that come from the environment, plus one cosmetic issue: an 'Acting as: senior solicitor' persona line shown above floor text that does no analysis. Two small items: A.6 item 4 understates the system because the leaderboard exists, and GET /qep/curriculum returns 404, though curriculum content is an open Owner ruling (A.12.3). Coverage was a spot-check of one tool per domain plus the avatar and QEP, not a full sweep. Nine findings, below the cap.

### R5.0 · The six domain tools give back frames built from counted words, not domain analysis, and they say so in plain words — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Every tool response carries the floor_note 'Composed by the native floor, not by a model ... NO research, legal or clinical analysis ... was performed - read it as an outline'. DomainTool.tsx (lines 97-98) adds that note to the text the user sees, and every section repeats 'a term count, not an analysis'. The gap is large but the surface states it, so it is tier 3. It is not tier 2 because nothing is hidden.
- **claim:** §2/§3: each of the six Domains offers real in-house-AI-mediated tools that run through the end-to-end lifecycle.
- **observed:** I ran POST /religion/quran-tafsir, /science/hypothesis, /law/analyse, /education/lesson-plan, /employment/salary-negotiation and /care/risk-assess. Each returned 200. The text under each heading is the request's most frequent bigrams. Care's NEWS2 score is real deterministic arithmetic and reports INCOMPLETE with the missing observations listed. ai_provenance served_by=native, and the QMS gate is null with 'not assessable — floor-served'.
- **evidence:** Run with curl against 127.0.0.1:8031. Read apps/workstation-superapp/src/components/DomainTool.tsx and the *Hub.tsx pages under pages/domains. All six hubs are routed in App.tsx at lines 178 and after.
- **disclosed to the user:** yes — the floor_note is appended to the output, and a provenance badge is shown
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced /law/analyse. Each section says 'a term count, not an analysis', and the surface discloses this, so it stays at tier 3. It is not tier 2 because nothing is hidden.
- **refuter's evidence:** law/analyse body: 'This engine lists them; it does not analyse the material'
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty. Real depth needs an owned model, which is the environment.

### R5.1 · Floor output still opens with expert personas ('Acting as: senior UK solicitor') above text that does no analysis — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The reader sees 'Acting as: senior UK solicitor specialising in contract law' and 'Acting as: Islamic scholar and Quranic exegete'. The same body then says 'This engine lists them; it does not analyse the material', and the floor_note denies any legal analysis. A persona line asserts a role, not an outcome, and the disclosure sits next to it, so it lands at 3, not 1. It is listed because the persona line is the first thing a reader sees.
- **claim:** §15 principle 6: never fabricate; label simulation.
- **observed:** Every floor response starts with an 'Acting as:' persona line. The floor also adds generic 'Next steps' such as 'record outcomes to memory/UEG'.
- **evidence:** Responses from /law/analyse, /religion/quran-tafsir and /avatar/chat.
- **disclosed to the user:** yes, in the same body
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed the line 'Acting as: senior England & Wales solicitor', followed straight away by a disclaimer. A persona line is a role claim, and the disclosure sits next to it, so tier 3 rather than tier 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Drop or reword the persona line when served_by=native, for example 'prompt persona (not applied — floor)'.

### R5.2 · Qur'an tafsir shows no Arabic when the external text source is blocked, and says why instead of making it up — **DELIVERED**

- **why it is this tier (assessor):** arabic_text is null and arabic_source reads 'unavailable — source unreachable; the Arabic is never AI-generated'. GET /qep/surah/1 returns 'Quran API unavailable: 403'. This is a refusal of a §11 boundary (A.9), and the surface states it.
- **claim:** A.9 / §11: no generated Qur'an Arabic.
- **observed:** No Arabic was fabricated. QEPReligionHub shows a 'verse unavailable' badge.
- **evidence:** POST /religion/quran-tafsir {surah:1, ayah_start:1, ayah_end:2}; QEPReligionHub.tsx line 127.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). This is a refusal of an A.9 boundary, and the surface states it. I did not re-run the route; I accept the assessor's evidence, which is consistent with the floor behaviour I saw.

### R5.3 · QEP Religion offering: SM-2 hifz, written Tajwid recall, XP and the leaderboard are real, and analytics refuses to fabricate figures — **PARTIAL** · tier 3

- **why it is this tier (assessor):** /qep/status says 'NO recitation assessment' and /qep/analytics/overview returns measured:false with 'previously returned hardcoded figures that no measurement produced'. The leaderboard states that it ranks recorded awards only. The features that are not built (A.6 items 6-9: classes, community, video, AR/VR) are stated in the vision and on the surfaces. No false figure is shown, so it is not 1 or 2.
- **claim:** A.1 / A.6: QEP is the Religion domain's flagship, with fifteen features.
- **observed:** The XAI endpoint runs the real SM-2 step (interval 6, ease factor 2.5 gives 15 days). It labels the per-feature contributions 'display-weight attribution ... not the engine's internal arithmetic'. GET /qep/curriculum is listed in the OpenAPI document but returns 404 on GET. Curriculum content is an open Owner ruling (A.12.3), so it is not a gap. Small doc drift: A.6 item 4 says leaderboards 'do not exist', but /qep/leaderboard exists and is honest.
- **evidence:** /qep/status, /qep/leaderboard, /qep/xai/explanations, /api/qep/analytics/overview; QEPStudio.tsx and qep/QEPIntelligence.tsx reach them.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The disclosed limits are consistent with what I saw. One note: /api/v1/qep/analytics/overview returned 404 at that path, so the analytics route may be mounted somewhere else. That does not change the tier, because no false figure is shown.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Update A.6 item 4 to record that the leaderboard exists.

### R5.4 · The avatar runs on the floor: replies are framing text, and its multimodal paths disclose what they could not do — **PARTIAL** · tier 3

- **why it is this tier (assessor):** GET /avatar/status reports effective_serving_mode 'deterministic floor ... it cannot translate or reason like a model'. A chat reply carries the native-engine banner. ConversationPanel.tsx (line 108) shows an 'image received but not analysed' state when no vision model ran. These limits are stated, so tier 3.
- **claim:** §9: an enterprise-aware, multimodal (text, voice, image) avatar that guides users through any area.
- **observed:** POST /avatar/chat 'hello what can you do' returned a generic frame of counted terms with no enterprise awareness or guidance. Session, history, ratification, transcribe and speak routes exist.
- **evidence:** /api/v1/avatar/status, /api/v1/avatar/chat; components/avatar/ConversationPanel.tsx
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that /avatar/status reports 'deterministic floor ... cannot translate or reason like a model'. The limit is disclosed, so tier 3.

### R5.5 · Language preference is honoured honestly: a request for Arabic is recorded and the reply says it is not delivered — **DELIVERED**

- **why it is this tier (assessor):** With Accept-Language: ar, the provenance reads language_delivered 'en' with 'NOT DELIVERED IN AR: the deterministic native floor composed this ...'. Settings tells the user when the interface is not translated ('it stays in English') and switches to right-to-left for RTL languages. This is the §9 corrected claim, delivered.
- **claim:** §9: accessible to all, in all languages, and says so when the serving resource cannot honour the language.
- **observed:** DomainTool sends Accept-Language from user prefs. Only locales/en.json is present (16 lines), and Settings computes coverage per language and states it.
- **evidence:** POST /education/lesson-plan with Accept-Language: ar; Settings.tsx lines 146-154; DomainTool.tsx line 155.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run it, but the 'NOT DELIVERED IN AR' disclosure fits the floor pattern I saw. Delivered as the §9 corrected claim.

### R5.6 · The explicit user profile exists and is applied to generation prompts — **DELIVERED**

- **why it is this tier (assessor):** GET /user/profile returns the fields about_you, context, goals, constraints and success_criteria, with 'applied_to: generation prompts on this platform (never shared)' and an empty preamble when blank. Nothing is overstated.
- **claim:** §9 personalisation (W428).
- **observed:** The profile is empty and reports profile_is_incomplete false and store_incomplete null. Settings is the UI for it.
- **evidence:** curl /api/v1/user/profile
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). Nothing on this surface is overstated. I did not verify it independently, so I accept it on the assessor's evidence.

### R5.7 · The 4 Realms x 6 Domains x 4 Products grid has one canonical source, and the product exposes it as Genesis selectors — **DELIVERED**

- **why it is this tier (assessor):** agentic_core/taxonomy.py and lib/taxonomy.ts define the same four realms, six domains and four products. GenesisJourney.tsx draws all three axes from the canon (lines 174-202 and 672-691). There is no drifted vocabulary in what I checked, and nothing the reader sees is untrue.
- **claim:** §17.1: the 4x6x4 grid.
- **observed:** The grid is exposed as realm and product selectors in Genesis and as DOMAINS selectors in Incubator and DigitalReactor. There is no page that shows the grid as a matrix. I did not verify that choosing a product changes what is generated.
- **evidence:** taxonomy.py lines 10-19; taxonomy.ts line 9; GenesisJourney.tsx
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). There is one canonical taxonomy. The assessor did not verify whether choosing a product changes what is generated, but no untrue claim is shown, so it stays at tier 0.

### R5.8 · The product catalogue labels the legacy domain Signature Products as archived and not live — **DELIVERED**

- **why it is this tier (assessor):** GET /catalog/products lists 'Care Domain Signature Product' with status 'legacy', live false, and 'Archived ... not a served product'. That is honest labelling, not fabrication.
- **claim:** §15 principle 6: never fabricate.
- **observed:** The catalogue states what is and is not served.
- **evidence:** curl /api/v1/catalog/products
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that /catalog/products returns status 'legacy', live false, and 'not a served product'.

---

## R6 — §8 + §12 + §17.5 — the biomimetic living organism, the economic organism, the ten architecture invariants

**Assessor's region summary:** R6 assessed live against HEAD 23a163c. Economy: the 6-stage waterfall (Stage 0 reserves plus the five-way split) computes correctly, double-entry close and trial balance balance after cycle + transfer + close, virtual-WST is disclosed on every surface, real-money rails are disabled, and economy routes are access-checked. The one truth defect is the charity path. Grants are funded at compliance 'review' (unassessed), and even when the engine is unavailable. allocation_rule and method still say they 'clear the compliance screen' / are 'compliance-screened', and the UI shows that text as each grant's tooltip. The organism beats and reports failed steps and quiet cadence honestly. It does not run itself by default because every auto_* loop is off, and that is disclosed. Selection is NOT_ASSESSABLE (satisfaction and founder alignment unmeasured), and self-healing reports health unknown. Both are disclosed tier-3 gaps. The undisclosed shortfall is 'organism_health' on plan state and the board snapshot: it is only the AI-call error rate, and HTTP 5xx is never recorded despite the immune docstring. Invariants: single router mount, torch optionality (backend live without torch) and the KPI gate (marketplace) hold. User isolation is improved (economy, plus admin on heartbeat and organism-status). The GaaS gate on every output still does not hold (21 of 75 API modules reference it). The vision's §17.5 status line is stale and understates this. Not executed: twin pre-validation 409, signal-bus atomicity, ≤5-min plan staleness, and DCS chain verification, so those are unverified rather than confirmed. I could not drive a browser, so UI claims come from reading HeartbeatMonitor.tsx and VSBEconomy.tsx. 10 findings, which is the cap. Their seriousness is modest: one tier 1, one tier 2, the rest tier 3 or delivered.

### R6.0 · Charity grants are funded and labelled as having cleared a compliance screen that cannot clear anything — **PARTIAL** · tier 1

- **why it is this tier (assessor):** The cycle response a user gets from the VSB Economy 'Run cycle' action carries allocation_rule 'each ... priority that clears the compliance screen ... receives 10.0%', and that text is the hover tooltip on every grant row. It sits beside method 'every grant compliance-screened (halal/ethical)'. Every grant actually comes back with compliance:'review', which means not assessed. The text states an outcome (cleared) that the platform did not produce, so this is tier 1 and not just an undisclosed gap. It is not tier 3 because nothing on the screen says the screen passed nothing.
- **claim:** §12: the four causes go through a 100%-donation-only screen and every distribution is compliance-checked (charity.py docstring: 'Halal / ethical only (enforced + checked)').
- **observed:** POST /api/v1/economy/cycle {revenue:1000,costs:100} funded 4 grants out of a 105 WST charity pot. Each grant had compliance:'review' and donation_100pct_verified:'not_checked'. charity.py only excludes a grant when the verdict is 'fail', so 'review' gets funded, and so does 'unscreened (engine unavailable)'. The UI footnote does say the 100%-donation flag is not_checked, but it says nothing about compliance being unassessed.
- **evidence:** agentic_core/economy/charity.py:250-263 (only verdict=='fail' excluded; 'review' and 'unscreened (engine unavailable)' go to cleared), :307 method string, :322 allocation_rule 'clears the compliance screen'; apps/workstation-superapp/src/pages/enterprise/VSBEconomy.tsx:597-602 (grant row tooltip = allocation_rule, compliance field never rendered).
- **disclosed to the user:** Half. The editorial weights and the not_checked 100%-donation flag are disclosed in the UI footnote. The fact that compliance cleared nothing is not.
- **refutation: SURVIVED** (reproduced by the refuter). Reproduced in code: charity.py:260-263 excludes only verdict=='fail'. 'review' and 'unscreened' grants are put into the cleared set, and the allocation_rule text at :322 says each such priority 'clears the compliance screen'. That states an outcome the platform did not produce, so this is a truth defect and tier 1.
- **refuter's evidence:** agentic_core/economy/charity.py:250-263,307,322
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Change 'clears the compliance screen' to 'is not refused by the screen (verdict: review = unassessed)', show each grant's compliance verdict on its row, and stop funding 'unscreened (engine unavailable)' grants.

### R6.1 · 'organism_health' on plan state and the board snapshot is just the AI-call error rate, and HTTP 5xx failures are never counted — **PARTIAL** · tier 2

- **why it is this tier (assessor):** GET /api/v1/plan/state returns organism_health:1.0 with threat_level NOMINAL and no basis. /organism/health-summary says 'Organism at peak on what is measured ... measured health 100%'. The only measured term is the immune ring buffer, and it is fed only by AI-gateway failures and compliance regressions. Nothing records HTTP 5xx, even though immune.py's docstring says it tracks them. The figure is a real count of AI-call errors, so it is not fabricated, which keeps it out of tier 1. But the surface never states this scope, so it is an invisible shortfall (tier 2), not a disclosed one.
- **claim:** §8: the organism defends itself; profitability, satisfaction, alignment and compliance are continuously monitored. The naming invariant: a quantity carries a name only when it is computed as that thing.
- **observed:** organism_health = immune.status().health = max(0, 1 - errors/10) over 5 minutes. immune.record is called only from ai/gateway.py, ai/native/orchestrator.py, heartbeat compliance regression, biobus and vbs/quality. No http_5xx recorder exists anywhere.
- **evidence:** agentic_core/api/transformation.py:72 and agentic_core/api/board.py:427 (organism_health = immune health); agentic_core/organism/immune.py:1-9 docstring claims HTTP 5xx tracking; grep for 'http_5xx' outside immune.py finds nothing; live /api/v1/plan/state shows organism_health 1.0.
- **disclosed to the user:** No. The composite discloses that 60% of its weight is unmeasured, but it presents the 'measured' immune term without saying what it watches.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed: 'http_5xx' appears only as a type comment in immune.py:24, and no recorder for it exists anywhere. The figure is a real count, so it is not tier 1. Its scope is never stated at the surface, so it is tier 2 rather than tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename the field immune_ai_error_health or attach a scope basis ('AI-call failures and compliance regressions only; route 5xx not tracked'), or add a 5xx middleware recorder.

### R6.2 · The six-stage waterfall and double-entry books work and balance after a cycle, a transfer and a period close — **DELIVERED**

- **why it is this tier (assessor):** Every figure shown checks out arithmetically: 1000 revenue - 100 costs - 200 reserve = 700 distributable, split 140/210/140/105/105. The close reports trial_balance 200/200 balanced and balance sheet assets 200 = equity 200. The net-profit basis honestly says distributions are booked as expenses. Nothing misleads.
- **claim:** §12: six-stage waterfall with Stage 0 reserves (costs + 20% of revenue) off the top, then the Owner 20 / Self 30 / Capital 20 / User 15 / Charity 15 split; double-entry books with period close and CFO statements; virtual WST.
- **observed:** Cycle, ledger, close-period and transfer all executed live. The transfer debited the sender's reserve_fund to 190, queued the amount for the receiver, and said explicitly that no autonomous cycle is scheduled. The board pack and owner payments say 'WST (virtual)' and real_money_rails DISABLED.
- **evidence:** Live POST /api/v1/economy/cycle, /close-period (balanced:true both sheets), /transfer xfer-8e34bb02d9; GET /economy/owner-payments; VSBEconomy.tsx:294 'All flows are virtual/simulated WST'.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). The assessor's live arithmetic is internally consistent. I did not re-execute it, and nothing in the code I read contradicts it.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R6.3 · Heartbeat beats report failed steps and quiet cadence honestly — **DELIVERED**

- **why it is this tier (assessor):** A beat returns steps_failed with a basis saying 'an EMPTY steps_failed means no step raised'. last_cadence says 'NO layer was due. This is a quiet cadence, not a broken one'. HeartbeatMonitor.tsx renders 'N step(s) FAILED'. The beat reports what it could not do, not just what it did.
- **claim:** §8: circadian heartbeat, self-running organism.
- **observed:** POST /heartbeat/beat returned actions [pulse, homeostasis, transformation_tick], steps_failed {} with basis, and a circadian phase. The router is mounted behind require_admin.
- **evidence:** agentic_core/organism/heartbeat.py:285-300; app_mvp.py:475; HeartbeatMonitor.tsx:340-343.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). Plausible from the cited code. Not re-executed.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R6.4 · The organism does not run itself by default: every autonomy loop (economy, evolve, align, compliance, metabolic, ship) is off — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The heartbeat beats, but auto_economy, auto_evolve, auto_align, auto_compliance, auto_metabolic and auto_ship are all false. A transfer response says outright 'autonomous economy cycles are OFF ... enable Self-run'. The shortfall is stated at the surface, so it is tier 3, not tier 2.
- **claim:** §8: 'once established, it is ever self-managing, improving, growing, evolving, healing'.
- **observed:** GET /heartbeat/status shows all auto_* flags false. evolution_auto_apply is disabled and governed by the CCA. auto_metabolic is 'NOT persisted, so a restart returns it to off'.
- **evidence:** Live /api/v1/heartbeat/status; transfer response settlement text.
- **disclosed to the user:** Yes, on the heartbeat status and in the transfer settlement text.
- **refutation: SURVIVED** (reproduced by the refuter). The autonomy loops are off by default and the surface says so, so this is a disclosed gap at tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none needed for honesty. Enabling the loops is an Owner or configuration decision.

### R6.5 · Selection cannot run: user satisfaction and founder alignment have no mechanism, and the surface says NOT_ASSESSABLE — **PARTIAL** · tier 3

- **why it is this tier (assessor):** /organism/selection/{vsb} returns status NOT_ASSESSABLE. It says satisfaction is 'NOT MEASURED ... absence of a signal, not a low one' and that founder alignment 'has no mechanism anywhere in this platform'. A large gap that the surface states itself is tier 3.
- **claim:** §8: the organism learns and improves, with profitability, satisfaction, founder alignment and compliance continuously monitored. Evolution needs selection.
- **observed:** Profitability is measured (roster cycles only). Satisfaction and alignment are null with honest bases. The genome summary shows 'no genomes stored yet'.
- **evidence:** Live GET /api/v1/organism/selection/vsb-b37afbaf8a; /heartbeat/status last_genome.mean_fitness_basis.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The surface itself returns NOT_ASSESSABLE with honest bases, so the gap is disclosed and tier 3 is correct.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Build the satisfaction capture (FU-311) and a founder-alignment mechanism before selection.

### R6.6 · Self-healing has no measurement and says health unknown rather than defaulting to healthy — **PARTIAL** · tier 3

- **why it is this tier (assessor):** /organism/self-healing/status returns overall_health:null with 'no circuit has carried a call yet — nothing measured, health unknown'. The composite marks the 1.0 default as 'not a measurement'. The gap is disclosed, so tier 3.
- **claim:** §8: the organism heals itself.
- **observed:** There are zero tracked circuits, and the healing log is empty and in-memory only. The metabolic term is an ATPSimulator on a constant load, also disclosed. The vision itself notes that no apoptosis or turnover mechanism exists, while living-vsbs exposes propose-mitosis and propose-removal routes.
- **evidence:** Live GET /api/v1/organism/self-healing/status and /organism/status composite_health_terms.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The surface reports overall_health null with a stated reason rather than defaulting to healthy. It is disclosed, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none for honesty.

### R6.7 · The vision's §17.5 status line is stale: it says KPI gate and torch optionality are not held, but the code holds both — **DOC_OVERCLAIM** · tier 3

- **why it is this tier (assessor):** This is a canon doc misreporting the system, though in the pessimistic direction. It says 'torch optionality: the app fails to import without torch' and 'KPI gate: nothing gates any delivery on KPIs'. No user is misled into trusting something false, and a document read by maintainers is not a reached product surface, so it is tier 3.
- **claim:** §17.5: the ten invariants. The status text (W446) puts torch optionality and the KPI gate under 'Not held'.
- **observed:** Torch is not installed (ModuleNotFoundError) and the backend is live, so torch optionality holds. business_plan.kpi_release_gate is enforced at marketplace.py:381 and :464 (W627, FU-541). Single router mount holds: include_router is called only in agentic_core/app_mvp.py. User isolation now covers economy (_require_economy_access on every handler) and the heartbeat and organism-status mounts (require_admin), which partly supersedes the 'carries no auth dependency' line.
- **evidence:** docs/WORKSTATION_IDBO_WHOLE_VISION.md:876-886; agentic_core/api/marketplace.py:377-385,457-464; agentic_core/app_mvp.py:408,475; agentic_core/api/economy.py:37,219.
- **disclosed to the user:** n/a (doc)
- **refutation: SURVIVED** (reproduced by the refuter). The doc is stale in the pessimistic direction and it is not a reached product surface, so tier 3. Strictly this is a doc under-claim, but DOC_OVERCLAIM is the closest verdict in the vocabulary.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Re-measure the §17.5 status line against HEAD.

### R6.8 · GaaS gate on every output still does not hold: most API modules never reference the GaaS gate — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The vision itself discloses the invariant as Partial ('true for 8 of 57 API modules'). A grep of the 75 files in agentic_core/api finds 21 that mention gaas/GaaS, so most outputs are still ungated. Because the canon states the gap, this is tier 3. I did not check whether individual ungated surfaces claim to be gated.
- **claim:** §17.5: mandatory GaaS gate on every output.
- **observed:** The economy cycle does run governance (status 'allowed', checkpoint CHK-...). Other modules do not reference a gate.
- **evidence:** grep -l 'gaas|GaaS' agentic_core/api/*.py gives 21 of 75 files; the cycle response governance block.
- **disclosed to the user:** Disclosed in the canon, not at each surface.
- **refutation: SURVIVED** (reproduced by the refuter). The canon discloses the gap. Whether individual ungated surfaces claim to be gated was not checked by the assessor or by me, so tier 3 stands for now.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Route every response through one gate dependency at the single mount point.

### R6.9 · The economy cycle silently ignores misnamed fields and books a zero-revenue cycle — **PARTIAL** · tier 3

- **why it is this tier (assessor):** POST /economy/cycle with {revenue_wst:1000,costs_wst:100} returned 200 and posted two ledger entries, which counted as cycles_posted 1, all at 0 WST. The response truthfully showed intake_revenue 0.0, so nothing false was asserted (an omission, not a false claim), and the UI form sends the right names. A caller can still get a booked empty cycle without being told it got the field names wrong.
- **claim:** §12: books record real cycles.
- **observed:** The CycleRequest model accepts extra fields, so the misnamed ones were dropped and a 0-revenue cycle went into the books.
- **evidence:** Live POST /api/v1/economy/cycle; then /economy/ledger/workstation-idbo showed entry_count 2, cycles_posted 1, all 0.0.
- **disclosed to the user:** Partly: the 0.0 figures are shown, but the rejected fields are not named.
- **refutation: SURVIVED** (reproduced by the refuter). The CycleRequest model exists at economy.py:168 with no extra-forbid configuration found in the grep, so unknown fields are dropped silently. The response truthfully shows 0.0, which is an omission rather than a false assertion. The UI form sends the correct field names, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Set extra='forbid' on CycleRequest (and the transfer and close requests).

---

*Regenerated by W634 from the audit workflow's journal. Every entry above is an observation against
the booted HEAD named in the header — routes executed, handlers and components read, stores counted —
not a claim read from another document. No browser was driven: statements about what a user SEES
(a chip's colour, a tab's default, a rendered badge) are reasoned from the component source, and the
assessors and refuters say so where it matters.*
