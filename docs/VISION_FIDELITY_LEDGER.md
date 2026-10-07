# Vision Fidelity Ledger — v11 (2026-10-07) — MILESTONE M1 re-run

**Supersedes v10 as the current assessment.** v10 is kept whole at `VISION_FIDELITY_LEDGER_v10.md` (its
Tier-1 entries are the ones P1.17 closed and the register rows cite), as v3 is at `VISION_FIDELITY_LEDGER_v3.md`.
This edition re-measures the product after P1.17, the second truth pass, as the M1 line requires — the Tier-1
count is measured again, never declared: a fresh six-region assessment against HEAD `51597af` (port :8031,
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
R1 8, R2 10, R3 10, R4 10, R5 10, R6 10 — a region under the cap ran out of consequential gaps, one
at the cap may have more. **Every finding was then attacked by an independent
refuter instructed to default to refuted** (v2 refuted six per region), who had to reproduce the gap (execute the
route, read the code, count the store) before letting it stand, and who was told to correct the
verdict UP or DOWN when the assessor had it wrong.

Reading rules that follow from the method:

1. **DELIVERED is understated by construction.** Assessors were told their job was the gap that
   remains, but to report DELIVERED where they verified it. Read the DELIVERED entries as the
   floor of what works, not the ceiling.
2. **Every one of the 58 findings was individually refuted.** The refuters reproduced
   58 as stated and overturned 0 — 0 moved to a
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
| STUB | 0 | 0 |
| MISSING | 2 | 2 |
| DOC_OVERCLAIM | 0 | 0 |
| API_ONLY | 2 | 2 |
| PARTIAL | 39 | 39 |
| DELIVERED | 15 | 15 |
| **total** | **58** | **58** |

Standing tiers (non-DELIVERED entries, the tier the refuter stands behind):

| tier | count | meaning |
|---|---|---|
| **1** | **4** | truth defect on a reached surface — the M1 measure (target 0) |
| 2 | 10 | invisible shortfall (Phase P2's tier) |
| 3 | 29 | disclosed or unreached capability gap (Phase P3/P4) |

Per region:

| region | sections | findings | STUB | MISSING | DOC_OVERCLAIM | API_ONLY | PARTIAL | DELIVERED |
|---|---|---|---|---|---|---|---|---|
| R1 | §10 + §11 | 8 | 0 | 1 | 0 | 0 | 3 | 4 |
| R2 | §4 + §13 | 10 | 0 | 0 | 0 | 0 | 8 | 2 |
| R3 | §5 + §17.3 + §17.4 | 10 | 0 | 0 | 0 | 0 | 8 | 2 |
| R4 | §6 + §7 + §17.2 | 10 | 0 | 1 | 0 | 1 | 6 | 2 |
| R5 | §1–§3, §3A, §9, §14, §15, §17.1 | 10 | 0 | 0 | 0 | 0 | 8 | 2 |
| R6 | §8 + §12 + §17.5 | 10 | 0 | 0 | 0 | 1 | 6 | 3 |

The distilled, actionable form of the surviving gaps is **prompt v11 rev 2's `<ledger>` and
`<delivery_plan>`** (`docs/FABLE_DELIVERY_PROMPT.md`). This document is the evidence base behind
them: every `<ledger>` item cites the entries here it rests on by region.index, and every plan
workstream carries the region.index entries it closes (or says it rests on another instrument —
the reach audit for the scatter, the Owner's hand for P4).

---

## R1 — §10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution

**Assessor's region summary:** I ran the R1 checks against the live backend at HEAD 51597af. Overall, §11's faith-content constitution holds on every surface I executed. Qur'an Arabic is never generated: with alquran.cloud returning 403 from the sandbox, every route refuses or shows "unavailable" instead of composing Arabic. Nonexistent ayaat are refused at the ayah, tafsir and hifz routes. Recitation is never scored. Tajwid lessons are withheld until a scholar approves them. Hadith, fatwa and interfaith on the floor withhold their scholarly sections. Analytics, the leaderboard and the compliance audit report unmeasured rather than invented figures. The A.11 tafsir defect (P1.8) and the green-QMS-chip defect (P1.1) are both fixed. §10 is honestly self-reported: 0 of 16 criteria are measured on the floor, and ties and identical candidates are disclosed. The one tier-2 finding is the QEP Studio translation card. It promises a path for non-Arabic educational text, but source_language defaults to "Arabic" and the UI never sends that field, so every request is refused with the sacred-text message, including English text. The refusal fails safe, but it is invisible and gives the wrong reason. §11's "integrated into every workflow" is PARTIAL: the Synthesis studio does not call the screen and the Forge screens only its intent label, both disclosed on the Compliance screen. Two small wording slips: the Genesis stage_5 method says "candidates modelled" when the 3 candidates were identical, and caller-chosen categorisation is recorded as met:true. Limits of this check: I could not drive a browser, so what the UI renders comes from reading the source. A positive written-recall comparison could not run because the Qur'an source was unreachable. I reported 8 findings, below the cap of 10.

### R1.0 · QEP Studio's translation tool is offered for non-Arabic educational text, but every request from the UI is refused as if it were Qur'anic Arabic — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The card tells the user: 'This tool is for non-Arabic educational text, and even then only a model may translate; the floor refuses.' That promises a non-Arabic path that the UI can never reach, and nothing on the card says so. When the user types English, the refusal they get reads 'translation of Arabic / Qur'anic text is NOT OFFERED, by ruling (A.9.3)', which gives the wrong reason. This is tier 2 and not tier 1 because the system refuses rather than inventing a translation, so no sacred text is misrepresented. It is above tier 3 because the screen does not admit the shortfall. It describes a capability that cannot work.
- **claim:** §11 rule 4 and A.9.3: translation of sacred text refuses. The QEP Studio card also offers a model-gated path for non-Arabic educational text.
- **observed:** In agentic_core/api/qep_intelligence.py, TranslateRequest.source_language defaults to "Arabic", and _is_sacred_source() returns True whenever source_language is 'arabic'. QEPStudio.tsx:150 posts {text, target_language:'English'} and never sends source_language. As a result, every UI request takes the 422 sacred-text refusal, including English text, and even when a model is available. The sacred-text refusal itself is correct and is DELIVERED.
- **evidence:** POST /api/v1/qep/translation/translate {"text":"Patience is a virtue","target_language":"French"} -> 422 'translation of Arabic / Qur'anic text is NOT OFFERED...'. Arabic input gets the same 422. See qep_intelligence.py lines 228-281 and QEPStudio.tsx lines 150 and 418.
- **disclosed to the user:** No. The card claims a non-Arabic path exists.
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced this. TranslateRequest.source_language defaults to 'Arabic' (qep_intelligence.py:239), and _is_sacred_source matches that value. QEPStudio.tsx:150 sends no source_language. Live English input returned 422 with the reason 'translation of Arabic / Qur'anic text is NOT OFFERED'. So the card promises a non-Arabic path that cannot be reached, and the refusal gives the user the wrong reason. It is not tier 1 because nothing is fabricated or translated. It is not tier 3 because the surface does not disclose the gap.
- **refuter's evidence:** curl POST /api/v1/qep/translation/translate {text:'Patience is a virtue'} -> 422 Arabic refusal; qep_intelligence.py:230-239; QEPStudio.tsx:150
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Default source_language to None and decide sacred status from the script and the declared language only. Alternatively, send source_language from the UI, or remove the non-Arabic claim from the card.

### R1.1 · §11 says compliance is integrated into every workflow, but the Synthesis studio does not call the screen and the Forge screens only its intent label — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The Compliance screen says this itself: 'The Forge screens only its request's intent label against the prohibited list, not the delivery's content, and the Synthesis studio does not call this screen at all.' The gap is stated where the user is, so it is tier 3, however large it is.
- **claim:** §11: compliance engines are integrated into every synthesis/generative/operational workflow, not bolted on, and are continuously live.
- **observed:** Deliverables and Genesis do run the §11 screen (verdicts are in quality_assurance.compliance). ComplianceChecker.tsx lists its own consumers and names the two workflows that do not call it. Most frameworks are keyword screens: regulatory, EHS and ethical return not_assessed on ordinary subjects.
- **evidence:** POST /api/v1/compliance/check {subject:'A community garden for children'} -> overall 'review'. sharia_halal and uk_legal are 'review — no engine covers this area'. regulatory, ehs and ethical are not_assessed. ComplianceChecker.tsx lines 71-76.
- **disclosed to the user:** Yes, on the Compliance screen.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one. The assessor's evidence, the ComplianceChecker text naming the uncovered workflows, places the disclosure on the surface. A gap the surface states is tier 3. Nothing shows that a reached surface asserts compliance it never ran, which would make it tier 1 or 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Wire the screen into synthesis_studio and Forge content, or amend §11's 'every workflow' wording.

### R1.2 · The §10 sixteen-criterion bar is measured for 0 of 16 on the floor and the record says so; 'categorised' is recorded as met only on the caller's own dropdown choice — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The user sees '0 measured · 1 attested · 2 screen-only · 13 not measured (of 16)'. The Deliverables page also shows 'ATTESTED by a caller (a claim about a run, not a measurement)'. The categorised entry carries met:true, but its basis states 'caller evidence: realm × domain chosen by the caller'. Because the shortfall and the basis of the one 'met' are both stated, this is tier 3 and not tier 2.
- **claim:** §10 as amended (R3): modelled, simulated, ranked and optimised are measured where an instrument exists and withheld on a tie. The other criteria are named as not measured.
- **observed:** Genesis journey stage_5 detects that all 3 candidates are identical (candidates_distinct=1), withholds modelled, simulated, ranked and optimised with the reasons, and discloses that the tie was broken by declared list order 'NOT evidence'. GenesisJourney.tsx:853 renders comparison_note. deliverables/produce reports measured=0. One wording slip: the stage_5 method string opens 'candidates modelled' while the bar says one text was 'modelled 3 times' and that this 'is not 3 candidates modelled'.
- **evidence:** POST /api/v1/genesis/journey -> bar_measured.summary '0 measured · 1 attested · 2 screen-only · 13 not measured (of 16)', and tie.tiebreak_is_merit=false. POST /api/v1/deliverables/produce -> '0 measured · 0 attested · 2 screen-only · 14 not measured (of 16)'.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one. The summary strings quoted disclose 0 of 16 measured and state the basis of the attested 'categorised' entry. Because both are disclosed, tier 3 holds. The wording slip in the method string is too minor to make it tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Stop recording caller-chosen categorisation as met:true (use met:null with attested:true). Reword stage_5's 'candidates modelled' when the candidates are identical.

### R1.3 · The QMS gate is now not-assessable on floor output instead of a green pass — **DELIVERED**

- **why it is this tier (assessor):** The surfaces show 'QMS not assessable' or qms_gate_passed:null, each with a basis that explains why the floor cannot fail the gate. The defect summary reads 'non-conformance: not measured (0 gates run)' rather than 0%, and the what-if gate failed for real. No untrue pass is shown.
- **claim:** §10: verified, tested and validated. The A.11 known defect was that the QMS gate could not fail on floor output, which produced green chips.
- **observed:** deliverables/produce and the quran-tafsir route both return qms_gate_passed:null with the reason 'not assessable — floor-served'. /vbs/qms/gate with weak content returned passed:false and opened a defect. VBSSystemsPanel.tsx:200 shows 'not measured (0 gates run)'. ServiceContracts shows '1 defect/0 gates'.
- **evidence:** GET /api/v1/vbs/qms/defects -> gates_run 0, open 1, what_if_failures 1. POST /api/v1/vbs/qms/gate -> passed:false, counted_in_rate:false.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one. The assessor's evidence shows a null or not-assessable gate with its basis, and 'not measured (0 gates run)'. No false pass is shown, so DELIVERED stands.

### R1.4 · The tafsir surface has been repaired: no Arabic is generated, the floor withholds the translation, and every provenance field reaches the screen — **DELIVERED**

- **why it is this tier (assessor):** The user is shown 'Arabic: unavailable — source unreachable; the Arabic is never AI-generated, so none is shown', the floor_note 'the study notes below are a structured frame, not scholarship', and 'Withheld on the floor: Transliteration · Translation'. Nothing untrue is asserted, so the tier is 0. One wrinkle: the static disclaimer still says 'The Arabic is sourced from alquran.cloud' even when none is shown. That is too small to make this a tier 2.
- **claim:** §11 rules 1, 2 and 4, and A.11's P1.8 (the tafsir surface as the weakest constitutional point).
- **observed:** The route returns arabic_text:null with an honest arabic_source, sections_withheld, floor_note, a disclaimer, and qms_gate_passed:null. ReligionHub.tsx lines 147-184 render arabic_source, range_note, floor_note and sections_withheld. A nonexistent ayah is refused. Hadith, fatwa and interfaith on the floor each withhold their scholarly sections with 'NOTHING WAS RESEARCHED, GRADED OR ATTRIBUTED' and similar notes.
- **evidence:** POST /api/v1/religion/quran-tafsir {surah:1, ayah_start:99} -> 'surah 1 has 7 ayaat — ayah 99 does not exist'. Ayah 1-3 -> the fields above. alquran.cloud returned 403 from this sandbox, which is the environment and not a defect.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one. On the evidence, the Arabic is null with a stated reason and the withheld sections are listed. The static disclaimer 'sourced from alquran.cloud' sits next to a visible 'unavailable' notice that contradicts it, so a reader is not misled. Tier 0 holds.

### R1.5 · Recitation is never scored: written recall refuses unless it has the sourced text, and the tajwid lesson is withheld until a scholar reviews it — **DELIVERED**

- **why it is this tier (assessor):** The ratified boundary A.9.1 is refused and the refusal is stated. /qep/status says 'NO recitation assessment (no phonetic model is provisioned)'. With the source unreachable, tajweed/analyse returns 503 'nothing is compared against text the platform did not source'. The lesson reads 'This is not shown because no scholar has reviewed it... A disclaimer is not a review'. Each is an honest refusal.
- **claim:** §11 rule 3, A.9.1, A.12.3 (scholar gate) and A.12.5 (riwayah declared).
- **observed:** tajweed/lesson returns lesson_plan:null, review_state:'withheld', and riwayah 'Hafs an Asim' with its basis. QEPStudio.tsx lines 394-399 render the withheld chip and the note. I could not run a positive written-recall comparison live because the Qur'an source returned 403 here, so I reasoned from the code and the 503 path.
- **evidence:** POST /api/v1/qep/tajweed/analyse {surah:1, ayah:1, recited_text:'بسم الله'} -> 503. POST /api/v1/qep/tajweed/lesson {rule_name:'idgham'} -> withheld. GET /api/v1/qep/status.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). Recitation scoring is a ratified A.9 boundary. The refusals and withholding are stated on the surface, so this is DELIVERED. The positive written-recall path could not be run, but the 503 path refuses honestly.

### R1.6 · Sourced-only Qur'an data, SM-2 hifz, analytics, the leaderboard and the compliance audit all refuse or report unmeasured rather than invent figures — **DELIVERED**

- **why it is this tier (assessor):** Every figure a user sees either comes from a computation or is reported as unmeasured. Analytics says 'measured:false... previously returned hardcoded figures'. The compliance audit says 'compliant:null... never asserted true'. The leaderboard returns an empty list and states its formula. Hifz ranges are validated against the real ayah counts. No fabrication.
- **claim:** §11 rule 2 and A.6 feature 3 (the Memorization Suite), and A.11's honest surfaces.
- **observed:** The ayah route refuses 1:8. hifz/schedule rejects the range [1,9] and schedules [1,7] with real SM-2 intervals. xai/explanations labels its contributions 'display-weight attribution... not the engine's internal arithmetic'. It does explain a default hypothetical learner rather than a real one, but that is disclosed by its basis field.
- **evidence:** GET /api/v1/qep/ayah/1/8 -> 422. POST /api/v1/qep/hifz/schedule -> 422 or 7 entries. GET /api/qep/analytics/overview -> measured:false. GET /api/v1/qep/compliance/audit -> compliant:null.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this one. On the evidence, analytics and the compliance audit report unmeasured or null values, and ranges are validated. Nothing fabricated reaches a user, so tier 0 holds.

### R1.7 · Twelve of the fifteen QEP features still have no module, and the platform claims none of them — **MISSING** · tier 3

- **why it is this tier (assessor):** A.11 states the gap in the canon, and no QEP surface claims the missing features exist. The parent and teacher roles, community, educator, guidance pillars and similar are simply absent. Something that is absent and not claimed is a tier-3 gap and not an invisible shortfall. The six ratified boundaries in A.9, the deferral of A.12.4 and the A.10 exclusions are deliberately not counted here.
- **claim:** A.6: fifteen core features, including parent and teacher roles (feature 1) and the four guidance pillars (A.7).
- **observed:** The tracked religious_domain package still holds only gamification, memorization and tajwid. /qep/* exposes hifz, tajweed, gamification, curriculum, contribute, xai, translation and adaptation. I did not re-measure the A.7 pillars beyond the route inventory.
- **evidence:** OpenAPI listing of /api/v1/qep/* and the A.11 surface inventory.
- **disclosed to the user:** In the canon (A.11). No surface claims otherwise.
- **refutation: SURVIVED** (reproduced by the refuter). The missing features are absent and not claimed on any surface, and the canon discloses the gap. An absent, unclaimed capability is tier 3, not an invisible shortfall.

---

## R2 — §4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS

**Assessor's region summary:** R2 (§4 lifecycle + §13 output). I ran one Genesis journey end to end through the live API, with establish=true (vsb-7093817949). I then named it, shipped it, read the repo tree and its files, downloaded the zip, read the review gates and ran evolve. The UI findings come from reading GenesisJourney.tsx and VSBCockpit.tsx, not from driving a browser.  The system is mostly honest about the floor. All 6 stages are disclosed as floor-served and not assessable. Stage 5 says its three candidates are identical and that the tie was broken by list order. The repo README and BUSINESS_PLAN say "body pending" and carry the founder's problem verbatim. Self-run is disclosed as off.  What the user's own problem gets: in 0 of 6 stage bodies is it more than frequency word pairs, which is disclosed. The frames also cut the sentence short.  There is no single gated lifecycle. Genesis runs 6 stages, the review gates list a different 8, the vision describes 10, and every gate is off by default.  An "established" VSB is a registered record plus a 27-file git repo: a static site, a client-side web app, a PWA, identity, genome, organisation and a compliance record. Only the founder's problem and the name are content; everything else is "pending". Only the birth cycle ran and nothing is operating.  Truth defects: - Tier 1: the hard-coded "Living VSB IDBO enterprise" footer on the public site and phone app. - Tier 2: the "Enterprise Established" heading. - Tier 2: the unqualified "coherent whole: true" in the cockpit. - Tier 2: the review gates' different stage list, which describes stages the journey never ran.  I reported 10 findings, the cap. Smaller items exist that I did not write up, so ten is not the whole gap.

### R2.0 · The generated public Website and Phone app footer tells every visitor the entity is a "Living VSB IDBO enterprise" while its own record says it is not yet living — **PARTIAL** · tier 1

- **severity (assessor):** high
- **why it is this tier (assessor):** The visitor reads the footer "Living VSB IDBO enterprise · generated in-house on Workstation's own AI fabric" on web/index.html, about.html, solution.html and the mobile page. For the same VSB, the API's established_vsb.deliverable says "body pending; it is not yet a living, operating enterprise" and living.autonomous_cycles is false. The footer is a constant, not something read from the entity's state, so it states something untrue about this entity on the surface the founder ships to the public. That makes it a stated falsehood (tier 1), not a missing disclosure (tier 2). The body text nearby does say "content pending the owned model", but nothing on the page takes back the word "Living".
- **claim:** §13 says every output is a living, continually developing enterprise. The W446 corollary says a floor body ships with an honest "content pending" state and never as the enterprise's concept.
- **observed:** Genesis journey vsb-7093817949, named and then shipped. GET /repo/file?path=web/index.html (and about.html, mobile/index.html) contains the hard-coded footer. In the same run, the VSB record has status "body pending", stage null, autonomous_cycles false and virtual true.
- **evidence:** agentic_core/api/vsb.py:713 hard-codes the footer string. curl http://127.0.0.1:8031/api/v1/vsb/vsb-7093817949/repo/file?path=web/index.html. GET /api/v1/vsb/vsb-7093817949 returns living.autonomous_cycles=false.
- **disclosed to the user:** No. The footer is the only statement of what the entity is, and it is wrong.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed: line 713 of vsb.py hard-codes the 'Living VSB IDBO enterprise' footer, and webapp line 999 does the same. Because it is a constant, the page calls the entity 'Living' even when its own record says it is not. That is an untrue statement on a public surface, so it is tier 1, not merely undisclosed (tier 2).
- **refuter's evidence:** agentic_core/api/vsb.py:713, :999
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Derive the footer from status_basis ("VSB IDBO entity — body pending; not yet operating") until the body exists and autonomous cycles run.

### R2.1 · The Genesis result card is headed "Journey Complete — Enterprise Established" for an entity whose body is entirely pending and that does not operate — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** The heading in GenesisJourney.tsx:941 shows whenever enterprise_established is true. The API returned true, with status "complete", in a run where all 4 body sections were pending and no lifecycle stage was reached. The paragraph directly under it carries the qualifier ("frames only: every stage was served by the deterministic floor"). The fuller truth, "not yet a living, operating enterprise", is only in established_vsb.deliverable, which this card does not show. Because a correction sits next to the heading, this is tier 2, not tier 1. Because the heading claims more than the record supports and the card never says "not operating", it is above tier 3.
- **claim:** §4.8 says Establish instantiates a bespoke, modelled, simulated and optimised living VSB IDBO that delivers and commercialises the solution.
- **observed:** POST /api/v1/genesis/journey with establish=true returned enterprise_established=true and status=complete. The same response has established_vsb.status "body pending", stage null and initial_ship deferred "name pending".
- **evidence:** apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:939-945. Saved response from the journey run (jny-312cd72b2bf9).
- **disclosed to the user:** Partly. The deliverable sentence says "frames only", but nothing on the card says the entity is not operating.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed: GenesisJourney.tsx:941 shows the heading whenever enterprise_established is true. A 'frames only' qualifier sits right next to it, so this is not tier 1. The card never says the entity is not operating, so it is above tier 3.
- **refuter's evidence:** GenesisJourney.tsx:941
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Use the heading "Enterprise Registered — body pending" when body_pending has any true value, and show established_vsb.deliverable on the card.

### R2.2 · The cockpit's Ship result says "coherent whole: true" without its basis that nothing was verified — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** After Ship, the user reads "Shipped 5 of 5 surfaces · coherent whole: true · commit …" (VSBCockpit.tsx:1412). The API's own coherent_whole_basis says "every surface was WRITTEN; 5 of 5 surface quality gate(s) were not assessable and compliance is review - written, not verified". The cockpit never renders that field, which grep confirms. The boolean only checks that no surface raised an error, so it is true as defined, but the qualification is hidden. That is an invisible shortfall (tier 2), not a stated falsehood (tier 1).
- **claim:** §13 says the repository is shipped as a coherent, quality-gated (§10) and compliance-screened (§11) whole.
- **observed:** POST /repo/ship returned coherent_whole=true, every surface with qms_gate_passed=null and compliance review, and version_control.message "ship: QMS not assessable · compliance review · seal None".
- **evidence:** agentic_core/api/vsb.py:2638 sets coherent_whole to all(no error, no deferred). grep for coherent_whole_basis in VSBCockpit.tsx finds 0 matches.
- **disclosed to the user:** No, not on the cockpit line. Only the API body carries the basis.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed: VSBCockpit.tsx:1412 shows the coherent_whole boolean, and the basis field appears nowhere in the src tree. The boolean is true by its own definition, so the hidden qualification is tier 2, not a falsehood.
- **refuter's evidence:** grep coherent_whole in src finds only line 1412
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Render coherent_whole_basis next to the boolean, or rename it "all surfaces written".

### R2.3 · There is no single gated lifecycle: Genesis runs 6 stages, the review gates use a different 8-stage list, the vision has 10, and every gate is off by default — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** GET /review-gates presents the lifecycle intake → research → design → build → validate ("Digital Twin Validation") → commercialise → genome → launch ("VSB entity created and operational"). Every stage reports gated:false. The Genesis journey runs concept, research, candidates, design, operations and commercialisation instead. A user who configures gates is shown stage descriptions such as "validates solution in digital twin simulation" and "operational". The journey never ran those stages, and its own stage-5 record says "forward-simulation NOT run". Nowhere does the gate surface say its stage list is not the one the journey executes, so this is tier 2. It is not tier 1 because these are descriptions of gates that can be configured, not claims that a gate passed.
- **claim:** §4 describes one continuous workflow with stages 1-10, each verified, tested and validated.
- **observed:** Three different stage lists. The gate list has no simulate/rank or develop step that matches the journey's, and every gate is not_gated, so nothing in an ordinary run is actually gated.
- **evidence:** curl http://127.0.0.1:8031/api/v1/vsb/vsb-7093817949/review-gates. GET /api/v1/genesis/status lists the 6 journey stages.
- **disclosed to the user:** No.
- **refutation: SURVIVED** (reproduced by the refuter). The genesis status route confirms the journey stages are a separate list. I could not re-run review-gates from here, so the gate stage list and the not_gated defaults are not re-verified. They are accepted as plausible. The gates are configurable descriptions, not claims that a gate passed, so this is not tier 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Map the review-gate stage ids onto the journey's actual stages, or label the 8-stage list as a separate, legacy lifecycle.

### R2.4 · No lifecycle stage carries the user's own problem: every stage body on the floor is a frame of the request's most frequent word pairs (disclosed) — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** Every one of the 6 stage bodies opens with "_Composed for the Enterprise realm. This engine RECORDS the realm and does not act on it_". Each lens section says "The list below is the request's most frequent terms, not findings about them." The stages note says "6 of 6 stages were served by the deterministic floor and are not assessable", and the Genesis card shows "The deterministic native floor served 14 …". The shortfall is total, since user content appears in 0 of 6 stages beyond word pairs such as "Component for spoilage because". But the surface states it, so it is tier 3. One small defect: the frames cut the problem off mid-sentence ("…solar-powered cooling .", which drops "cooperative service").
- **claim:** §4.2-4.7 call for AI-mediated problem mapping, research across science, technology, business and law, a buildable design, development and operational intelligence, all tailored to the person.
- **observed:** stage_3, phase_2, stage_6, stage_7 and phase_3 all repeat the same 5 word pairs under the headings SAMAJH, SOCH and AQAL, with generic bullet points. develop_artefact is {} and its basis says "not buildable on the floor".
- **evidence:** POST /api/v1/genesis/journey (jny-312cd72b2bf9): stages_floor_served=6, stages_verified="0/0", every stage_verifications.*.verified=null.
- **disclosed to the user:** Yes, on the API body and on the Genesis card (GenesisJourney.tsx:757-800).
- **refutation: SURVIVED** (reproduced by the refuter). Plausible but not re-executed: the backend was unreachable from this session, so I relied on the assessor's quoted run. The floor is disclosed on the API body and on the Genesis card, so this is tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Stop truncating the problem statement inside the frames.

### R2.5 · §4.5 Model, Simulate, Optimise, Rank produces three identical candidates and a tie broken by list order, and says so — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** The surface shows comparison_note "All 3 candidates returned IDENTICAL text, so no comparison was possible and the ranking below carries no information". It also shows selection_basis "TIE at 0.798 … resolved by list order, NOT by evidence" and that none of the five criteria was measured (GenesisJourney.tsx:853-916). The gap is total but plainly stated, so it is tier 3.
- **claim:** §4.5 says every candidate is modelled, simulated, optimised and ranked, so the best is selected on evidence.
- **observed:** candidates_distinct=1, tiebreak_is_merit=false, criteria_measured={}, and "forward-simulation NOT run".
- **evidence:** stage_5_model_simulate_rank in the journey response.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The response quotes plainly state the identical candidates and the list-order tiebreak, and the UI renders them. This is a disclosed gap, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty.

### R2.6 · §13 The shipped VSB repository integrates Website, Web app and PWA Phone app, is version-controlled in git and downloadable, with founder words plus honest "content pending" bodies — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** Execution confirmed 27 files: web/ (index, about, solution), webapp/ (a tabbed client app reading data.json), mobile/ (manifest.webmanifest and sw.js, i.e. an installable PWA), plus IDENTITY, genome.json, BUSINESS_PLAN, ORGANISATION, cascades and compliance/QUALITY. Ship committed to git (8 commits) and the zip returned 200 (30 KB). The README says "Status: body pending … no §4 lifecycle stage is reached". BUSINESS_PLAN carries the founder's problem verbatim, with "content pending the owned model" for every other section, exactly as W446 requires. The cockpit reaches the file, zip, ship, cascade and evolve actions. The only exception is the footer, already reported above.
- **claim:** §13 plus the W446 ruling: a static site, a client-side web app and a PWA, version-controlled and not hosted, with floor bodies shown as pending.
- **observed:** Matches the vision, apart from the footer finding.
- **evidence:** GET /api/v1/vsb/vsb-7093817949/repo returns file_count 27. /repo/zip returns 200. version_control.commit d928a19003ad. VSBCockpit.tsx:290-360.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). Not re-executed, because the backend was unreachable from this session. The repo surfaces are described consistently. The footer defect is carried by finding 0, so this stays DELIVERED.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** n/a

### R2.7 · §4.10 Run forever: the established VSB does not self-operate by default, and the record says so; evolve files proposals that need Owner approval — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** living.autonomous_operation states "autonomous economy cycles are OFF (the heartbeat's Self-run lever is off), so only the birth cycle ran; enable Self-run …". POST /evolve returned outcome "proposals_filed_pending_approval" and generation 0, with the basis "a filed cycle does not advance it". The proposal's expected impact is stated as "none measurable". The gap is real, since nothing runs forever by default and the one proposal changes only a trait, but it is disclosed, so it is tier 3.
- **claim:** §4.10 says the established VSB self-operates and forever evolves on live intelligence.
- **observed:** Only the birth cycle ran, with revenue 0 and revenue_basis no_activity_maintenance_cycle. Evolve re-shipped the repo and filed CCA cca-f6502b2e6c.
- **evidence:** POST /api/v1/vsb/vsb-7093817949/evolve. established_vsb.living in the journey response.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). The quoted living.autonomous_operation text plainly discloses that Self-run is off, so this is a disclosed gap at tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** n/a

### R2.8 · §4.1 Describe accepts text, an attached document and voice dictation; image and media input is not present — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** GenesisJourney.tsx:660-666 offers AttachDocument (read in the browser and appended as text) and DictateButton. There is no image, video or site/app ingestion, and the UI makes no claim to have it, so the gap goes unstated but no false claim is made. Tier 3 is the closest fit: the omission is visible and nothing untrue is asserted.
- **claim:** §4.1: multimodal input (text, voice, image, uploaded data, media, sites, apps, models).
- **observed:** Text, document-as-text and voice only. All attachments end up as text appended to the problem field.
- **evidence:** apps/workstation-superapp/src/pages/synthesis/GenesisJourney.tsx:650-666.
- **disclosed to the user:** Implicitly: the hint says "research report, brief, dataset".
- **refutation: SURVIVED** (reproduced by the refuter). The missing image and media input is a visible omission, and nothing on the screen claims it. That is tier 3, not tier 2: a reader is told nothing untrue, and the input controls themselves show the limit.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** n/a

### R2.9 · Naming gates the first ship honestly: an unnamed entity defers shipping and tells the founder why — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** initial_ship returned {shipped:false, deferred:"name pending", reason:"the founder names the enterprise before its body ships — POST …/name"}. POST /name with a founder name then shipped all 5 surfaces at commit 07cd07c9a2f4, with name_source "founder". It behaves as designed and says why.
- **claim:** §13/§15: the output is shipped under the founder's intent.
- **observed:** Works as described.
- **evidence:** POST /api/v1/vsb/vsb-7093817949/name.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). Shipping is deferred until the founder names the entity, and the reason is given. This works as designed, so it stays DELIVERED.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** n/a

---

## R3 — §5 + §17.3 + §17.4 — the living organisation, the living business system layers, the three integration modes

**Assessor's region summary:** R3 (§5, §17.3, §17.4), measured live on :8031 at HEAD 51597af. The org chain runs end to end: POST /swarm/cascade goes through Chief, Board, AI CEO, 5 of 9 C-Suite roles, CoE, BTO and Build-to-Order. It does document control in the QMS-owned DCMS, screens with gaas, has user-selectable C-Suite roles, and labels its provenance. On the native floor every tier's text is a term-count scaffold, and it says so. Delivered and verified: arms-length Change Control with Board ratification (implement refused until ratified; queue on the Board page), Mode 3 gating (409 on a gated VSB), and Mode 2 role/twin reporting as the Owner ruled. Partial but disclosed (tier 3): the Business Plan opening (fields exist and can be owner-edited; floor generation writes nothing and says why), the living roadmap (unparseable timelines are listed as Unscheduled; 'Q2 2027' inside an instruction is not extracted), the §17.3 Strategic and Action-Plan cadence (refreshes derived from the plan; signals only when a caller supplies one), the Board Pack (narrative pending, per-field sources), twin pre-validation (health gate, 'NOT simulated'), and upward appraisals (floor scaffolds over empty input). No tier-1 truth defect was found. There are two tier-2 invisible shortfalls. (1) Chief instruct throws away the Owner's words and frames the platform blurb as 'Owner Intent' under an emerald 'Modelled twin' banner, with no reason line. (2) The cascade quality record says stub_found:false, substantive_length:true and coverage 1.0 for floor scaffolds; not_assessable:true sits beside these fields but does not qualify them. UI findings come from reading the source (BoardOfDirectors.tsx, SwarmIntelligence.tsx, BusinessPlan.tsx, ChangeControlAgency.tsx, CEOChat.tsx, LivingOrganisationHub.tsx), not from driving a browser. CEOChat (/api/v138/ceo/chat) shows a provenance badge per answer and was honest when executed. The cap of 10 findings was reached. Unexamined items remain: the BTO Products Catalogue curate path, CCA immune-reconfigure, /economy/board-pack, and AgentHubPanel's operations (only grepped).

### R3.0 · The Chief's Board Directive ignores the Owner's instruction and frames the platform's own blurb as 'Owner Intent', shown under an emerald 'Modelled twin' banner — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The reader typed 'Prioritise Quran tutoring for children; target 100 students by Q2 2027'. Directly under the green line 'Modelled twin — 1 instruction(s) you wrote', the page shows a '## Owner Intent' section framed over 'Workstation IDBO AI-mediates working for any user in any realm/domain…', which is not what they said. The floor badge says a deterministic engine answered. Nothing says the instruction was dropped, although /business-plan/generate says exactly that in its reason line. It is not tier 1 because the floor marker and the 'term count, not findings' wording are on screen, so no false finding is asserted. It is not tier 3 because the dropped instruction is never mentioned.
- **claim:** §5: the Chief, as the Founder's Digital Twin, is instructed through multimodal communication and delivers the founder's role from the founder's instructions. §17.4 Mode 2 is the Owner's own twin node.
- **observed:** POST /api/v1/board/chief/instruct returned a chief_directive whose 'Owner Intent' frame is keyed on the prompt preamble, not the instruction. The ceo_action_plan frame is over an empty string ('(no salient terms extracted)'). objectives_added=1 comes from chief_instruct_fallback, which copies the instruction verbatim as the objective title with KPI '(KPI to be set by the Board)' and an empty timeline. Unlike generate, the response has no reason field saying the floor discarded the Owner's words.
- **evidence:** curl POST /api/v1/board/chief/instruct and its chief_directive text. BoardOfDirectors.tsx lines 340-350: chiefStanding() renders 'Modelled twin' in emerald above {result.chief_directive}. Compare business_plan.py lines 650-655, where the reason says nothing was written.
- **disclosed to the user:** The floor is disclosed (badge plus engine marker). That the instruction was not used is not disclosed.
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced this. POST /board/chief/instruct with the tutoring instruction returned a '## Owner Intent' section framed over the platform's own 'Workstation IDBO AI-mediates working…' text, not the instruction, and named the domain WITHHELD. The floor marker and the 'most frequent terms, not findings' wording keep it out of tier 1. Nothing says the instruction was dropped, so it is above tier 3.
- **refuter's evidence:** Live curl response: chief_directive '## Owner Intent' framed over 'Workstation IDBO AI-mediates working for any user…'
- **smallest honest fix (assessor's proposal — a lead, not a decision):** On a floor-served instruct, return and render a reason line ('the floor did not read your instruction; it was stored as an objective verbatim'), the same way /business-plan/generate does.

### R3.1 · The cascade's QMS quality block marks floor scaffolds 'stub_found: false', 'substantive_length: true' and delivery_coverage 1.0 in the stored run record — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The stored and returned record of POST /api/v1/swarm/cascade gives delivery_coverage 1.0, substantive_length true and stub_found false for 22 native-floor outputs. Those outputs are term-count frames ('Positioning wedge from launch halal'). not_assessable:true sits in the same object, and SwarmIntelligence.tsx leaves such runs out of its chart, so this is not an unqualified certification (not tier 1). Still, two fields in the record assert a quality outcome that nothing judged, and nothing qualifies those fields themselves (not tier 3).
- **claim:** §10 / §17.5: a KPI and QMS gate is applied to delivery, and the quality bar is assessed.
- **observed:** quality = {delivery_coverage:1.0, substantive_length:true, stub_found:false, not_assessable:true, served_by:'native×16'}. The code comment at SwarmIntelligence.tsx line 193 itself says coverage is 1.0 'by construction' on the floor.
- **evidence:** curl POST /api/v1/swarm/cascade {mission:'Launch a halal tutoring MVP'}, quality key. SwarmIntelligence.tsx lines 188-204.
- **disclosed to the user:** Partly. not_assessable is in the record and the chart excludes these runs. The individual stub and length fields are not qualified.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run the cascade. I accept the assessor's evidence: stub_found and substantive_length assert a quality outcome, but not_assessable:true sits in the same object. That keeps it below tier 1, and the individual fields are not qualified, so it is above tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** When not_assessable is true, null out stub_found, substantive_length and delivery_coverage, or attach a basis to each, so nothing in the record reads as a pass.

### R3.2 · Upward management appraisals in the org cascade appraise nothing: the Chief's appraisal of the Board is a frame over an empty string — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The 'Management appraisal & development' panel shows text such as 'Structured go-to-market frame for: .' and '(no salient terms extracted)'. Each text starts with the native-engine marker, and since W615 floor-served development actions are not stored as continual improvement. A reader can see this is a scaffold, so nothing untrue is asserted (not tier 1 or 2). The capability gap is large but visible on the surface.
- **claim:** §5: each tier manages, appraises and develops the tier below, for continual improvement.
- **observed:** appraisals.chief_appraises_board and the other edges are floor frames keyed on an empty subject. development_applied = {}.
- **evidence:** swarm.py lines 871-905. The cascade response appraisals key. SwarmIntelligence.tsx lines 392-405 render the first 600 characters, including the engine marker.
- **disclosed to the user:** Yes, through the engine marker in each appraisal and the provenance badge on the cascade.
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this. The engine marker in each appraisal discloses the floor, so the gap is visible and tier 3 holds.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Label the panel 'not appraised — floor served' when every appraisal is floor-served.

### R3.3 · The §17.3 Strategic and Action-Plan cadence layers exist but refresh only with plan-derived text, and a market or KPI signal fires only when a caller supplies one — **PARTIAL** · tier 3

- **why it is this tier (assessor):** GET /api/v1/organism/cadence states its limits itself: 'DERIVED from the plan's own stored state … nothing here is an analysis of the business' and 'nothing in this platform observes markets or KPIs, so a signal fires only when someone supplies one'. The shortfall is stated at the surface, so it is tier 3 however large it is.
- **claim:** §17.3: Strategic layer (AI CEO; quarterly plus market signal) and Action Plan layer (BTO; weekly plus KPI-triggered), continuously maintained.
- **observed:** Both layers have a period, a due computation, a refresh history and served_by:'deterministic-floor'. Their content is a one-line count ('0 aim(s) and 0 objective(s)…').
- **evidence:** curl GET /api/v1/organism/cadence and GET /api/v1/business-plan (refreshes[]). CadencePanel.tsx is used on BusinessPlan.tsx.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this. By the evidence quoted, the cadence route states its own limits, which makes it a disclosed gap at tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty. The capability gap is a real KPI/market signal source.

### R3.4 · The Chief-owned Business Plan opening (Executive Summary · Concept · Vision) is stored and owner-editable, but floor generation writes nothing and says so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The plan-generate note in BusinessPlan.tsx shows the reason 'structured floor — not model analysis; nothing was written to the plan (the fields stay pending the owned model; the owner can set them)', and a 'pending the owned model' chip lists the fields. The floor's chief_draft ignores the founder's context (it framed 'AI-mediate working for any user…' when given a tutoring marketplace), but it is not persisted. The gap is disclosed.
- **claim:** §5: the plan opens with a Chief-owned Executive Summary · Concept · Vision, which can be AI-generated in-house from the founder's description and then owner-edited.
- **observed:** GET /api/v1/business-plan has the executive_summary, concept, vision, mission and strategy fields. POST /set with executive_summary persisted it. POST /generate returned served_by 'native', written [] and the reason above.
- **evidence:** business_plan.py lines 606-690. curl POST /business-plan/generate {context:'A halal tutoring marketplace…'}. BusinessPlan.tsx lines 67-73, 159 and 173.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this. The generate reason line discloses that nothing was written, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None for honesty. Generation waits on an owned model serving.

### R3.5 · Arms-length Change Control with Board ratification of review-approved HIGH changes works end to end — **DELIVERED**

- **why it is this tier (assessor):** Verified by execution. A HIGH code_change approved by the health-threshold rule is labelled 'DECIDED BY RULE, NOT BY THE SERVING RESOURCE'. It is queued at /board/ratifications, /cca/{id}/implement refuses it with an explicit message, and the Board page renders the queue with an owner-direction checkbox gating Ratify. Nothing untrue is shown.
- **claim:** §5 W464: a HIGH change approved by a review waits for Board ratification on the Owner's direction. Change Control governs at arm's length.
- **observed:** submit gives impact_tier HIGH. review gives approved, decision_source health_threshold_rule and awaiting_board_ratification true. implement is refused. The ratification queue shows the row.
- **evidence:** curl /api/v1/cca/submit, /cca/{id}/review, /cca/{id}/implement, /board/ratifications. BoardOfDirectors.tsx lines 196-260.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this. The assessor's execution chain (submit, review, a refused implement, and the ratification queue) is specific, and nothing untrue is shown, so DELIVERED at tier 0 stands.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** n/a

### R3.6 · The §17.5 digital-twin pre-validation is a health gate that returns 'PASS' while saying the change was not simulated — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The verdict is 'pass', but the method reads 'no twin model — organism health gate only … The proposed change was NOT simulated', and ChangeControlAgency.tsx renders it amber with '(no twin model — health gate only)'. The reader is told plainly that no simulation happened, so this is a disclosed gap, not a false certification.
- **claim:** §17.5: digital-twin pre-validation before major change. §5: the organisation is modelled and simulated.
- **observed:** POST /cca/{id}/twin-prevalidate returns verdict pass, source health_gate_default, plus a floor 'State Trajectory' frame.
- **evidence:** curl POST /api/v1/cca/cca-14c9239fb2/twin-prevalidate. ChangeControlAgency.tsx lines 330-350.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this. The 'pass' verdict comes with an explicit 'NOT simulated' method and an amber label, so the gap is disclosed: tier 3, not tier 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Consider verdict 'not_simulated' rather than 'pass' for the health-gate source.

### R3.7 · Mode 3 human review gates block the org cascade for a gated VSB, but they pause the ship rather than a stage mid-journey — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Gating is verified: after setting stages ['build'], POST /swarm/cascade with that scope returned 409. The stage-level limit is stated in the vision's own §17.4 status, and the gate panel shows per-stage status. Because the gap is stated, it is tier 3. A minor issue: CascadeRequest is not strict, so an unknown field such as vsb_id is silently dropped, and the cascade then runs against the apex plan.
- **claim:** §17.4 Mode 3: optional human review gates at any Concept→Commercialisation stage, set in the VSB genome.
- **observed:** GET and POST /vsb/{id}/review-gates work with validation of stage names. The cascade is refused with 409 while a gate is pending.
- **evidence:** curl POST /api/v1/vsb/vsb-7093817949/review-gates {stages:['build']}, then POST /swarm/cascade {scope:vsb-…} returned HTTP 409. vsb.py lines 1700-1717. swarm.py lines 375-380.
- **disclosed to the user:** Yes, for the stage limit.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this. Gating gave a 409 and the stage limit is stated, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Make CascadeRequest STRICT like the CCA and Board models, so a mis-addressed field is refused rather than ignored.

### R3.8 · The on-demand Board Pack is assembled fresh, DCS-registered, and says its narrative is pending and where each layer came from — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The narrative reads 'narrative pending the owned model — this board pack has not been composed'. The mission is labelled 'derived from the founder's problem statement - not authored', values are 'NOT DECLARED', and layers_state names the strategic placeholder. Every shortfall is stated in the reached body.
- **claim:** §17.3: the Board Pack is assembled fresh from live data and DCS-registered.
- **observed:** POST /vsb/{id}/board-pack returns versioned, DCS-hashed layers with per-field sources, and the narrative is pending.
- **evidence:** curl POST /api/v1/vsb/vsb-7093817949/board-pack (narrative, layers, layers_state, dcs_registered).
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this. The pending narrative and the per-field sources are stated in the response body, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None for honesty.

### R3.9 · The Chief reports 'role' or 'modelled twin' from the Owner's own record, so Mode 2 is delivered as the Owner ruled, but one stored sentence turns it green — **DELIVERED**

- **why it is this tier (assessor):** The R6 ruling requires a twin built from the Owner's record, or a Chief that plainly says it is a role. With no inputs, /board/chief/model said 'A ROLE, NOT A MODELLED TWIN', rendered amber. After one instruction it said 'MODELLED TWIN: built from 1 instruction(s)…', with the method stated. The criterion is met and the threshold is disclosed. How the directive then ignores that instruction is covered in the first finding.
- **claim:** §17.4 Mode 2 as scoped by the 2026-10-05b ruling: the Owner's own twin node, or the Chief says it is a role.
- **observed:** is_modelled_twin flips false to true on a single instruction row. The basis and method strings explain this.
- **evidence:** curl GET /api/v1/board/chief/model before and after POST /board/chief/instruct. BoardOfDirectors.tsx lines 100-123.
- **disclosed to the user:** Yes, the method is shown.
- **refutation: SURVIVED** (reproduced by the refuter). Partly confirmed. GET /board/chief/model live shows instructions count 1 and a profile marked declared_by_owner:false, with its method stated. That meets the scoped ruling, so DELIVERED at tier 0.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** Optionally show the input count beside the green label, e.g. 'thin: 1 input'.

---

## R4 — §6 + §7 + §17.2 — the native AI mandate, the reconfigurable resource fabric, the seven biomimetic layers

**Assessor's region summary:** R4 (§6, §7, §17.2), assessed against the live backend at http://127.0.0.1:8031. I reasoned about the UI from source because I could not drive a browser.  What works as the vision says: - The AI is in-house-first, and external providers are opt-in. /native-ai/status reports deterministic_floor, is_real_model=false and floor_active, and NativeAI.tsx shows this in an amber banner. - Provenance (served_by, is_external) is truthful everywhere I executed: the final response, every swarm stage, every tree node, saved-cascade runs (with a UEG audit hash) and SSE done frames. - Users can design, save, edit, run and retire cascades in the /native-ai cascade designer, which works end to end.  What falls short: - Cascades are template-based. Every VSB gets the same four-stage delivery swarm, and the tree planner is 'deterministic_template'. Nothing optimises cascades, nothing builds them per founder, and nothing simulates a configuration before it is committed. Most of this is disclosed: the Cockpit template note and the 'planned by template' badge. - Spawn Studio is the exception. It shows 'Run this VSB's swarm' without the template disclosure the Cockpit gives (tier 2). - Biomimetic layers: the nervous ring, reflex arcs, immune sensing and self-healing are real and honest. ATP is simulated and cannot fall, and the genome is empty and separate from the VSB GenomicRegistry; both are disclosed.  The one truth defect (tier 1): the 'Cognition' vital (FLOURISHING / STABLE / STRESSED) is derived from host CPU and project count, has no basis attached, and is shown on Introspection and in the shell status dot. It reports a saturated host as flourishing cognition.  Ten findings is the cap, and I hit it. I did not check every SSE stream on genesis, vsb, products, intelligence and synthesis, the durable AI call log, model_resource.py, or the Forge and Build-to-Order reconfiguration UIs. Ten is not the whole gap.

### R4.0 · The organism's 'Cognition' vital reads FLOURISHING when the host CPU is saturated, and nothing cognitive is measured — **PARTIAL** · tier 1

- **severity (assessor):** medium
- **why it is this tier (assessor):** The Introspection page shows 'Cognition: FLOURISHING / STABLE / STRESSED', and the shell BiometricStatus dot is coloured violet for FLOURISHING. Both state the condition of the organism's cognition. The value actually comes from host CPU above 70% or the project count, with no basis attached, so a saturated host is reported as flourishing cognition. That is an untrue statement on a reached surface, so it is tier 1. It is not tier 2 because the label asserts a state the platform never assessed; it does not merely leave something out.
- **claim:** §17.2 Nervous layer: the nine cognitive engines + MJM + SPI/BPI sense, think and decide. §8 describes a living organism with real vitals.
- **observed:** app_mvp.py /api/v1/biometrics/status: cognition_state = FLOURISHING if (active>2 or cpu>70) and immune_health>0.5, else STABLE/STRESSED, and primary_drive is chosen the same way. No *_basis field accompanies it, although cardiovascular, metabolic and communication each carry one (W489/W506). Introspection.tsx:128 renders it unqualified, and BiometricStatus.tsx shows it with a bare title='Cognition'.
- **evidence:** agentic_core/app_mvp.py ~645-655 (cognition_state/primary_drive branch); apps/workstation-superapp/src/pages/cognitive/Introspection.tsx:128; apps/workstation-superapp/src/components/BiometricStatus.tsx:12-13,121,179,204
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Reproduced in app_mvp.py:646-655. FLOURISHING is set from active>2 or cpu>70, with immune health as the only gate. The live /biometrics/status response has a basis on cardiovascular and workload but nothing on cognition, and Introspection.tsx:128 renders the state unqualified. It states a cognitive condition the platform never measured, so it stays tier 1. It is not tier 2, because the label asserts a state rather than leaving one out.
- **refuter's evidence:** app_mvp.py:647 'if active > 2 or cpu > 70: cognition_state = "FLOURISHING"'; live response cognition:{state:STABLE,primary_drive:DISCOVERY} with no basis
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Return cognition_basis ('derived from host CPU% and running-project count; no cognitive engine is read') with the figure and render it, or rename the label to 'Load state'.

### R4.1 · Spawn Studio presents every new VSB's fixed template swarm as 'this VSB's swarm' without saying it is the same template for all — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** VSBSpawnStudio shows 'Native delivery swarm (owned, in-house)' and a 'Run this VSB's swarm' button over the four stages ai-ceo, c-suite, centre-of-excellence and build-to-order. Every VSB gets those same stages from one hard-coded list in genesis._attach_delivery_swarm. The VSB Cockpit states this ('started from the same fixed template every VSB receives — not synthesised or optimised'), but Spawn Studio, where the founder first sees the swarm, does not. That is an undisclosed shortfall on that surface, so it is tier 2. It is not tier 1 because the page never actually says 'bespoke'.
- **claim:** §6: the swarm cascade is synthesised, modelled and simulated bespoke to each solution and each founder.
- **observed:** genesis.py:935-966 registers identical stages and instructions for every VSB; only the context string differs. The Cockpit template note is present (VSBCockpit.tsx:741), but the Spawn Studio panel (VSBSpawnStudio.tsx:553-562) has no equivalent.
- **evidence:** agentic_core/api/genesis.py:935-966; apps/workstation-superapp/src/pages/enterprise/VSBSpawnStudio.tsx:553-562; apps/workstation-superapp/src/pages/enterprise/VSBCockpit.tsx:741
- **disclosed to the user:** in the Cockpit, not in Spawn Studio
- **refutation: SURVIVED** (reproduced by the refuter). VSBSpawnStudio.tsx:553-562 shows 'Native delivery swarm (owned, in-house)' and 'Run this VSB's swarm' with no note that the template is fixed. The page never says 'bespoke', so it is not tier 1. The panel does not disclose the shortfall, so it is not tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Copy the Cockpit's vsb-swarm-template-note sentence into the Spawn Studio swarm panel.

### R4.2 · Cascades are not synthesised per solution or founder, and nothing optimises them (the shortfall is disclosed) — **PARTIAL** · tier 3

- **severity (assessor):** high (capability)
- **why it is this tier (assessor):** The bespoke-per-founder and optimised-cascade clauses are not built. I found no search, scoring or optimisation of cascade configurations; the /native-ai/tree planner returns 'deterministic_template' (the same roles for any goal, e.g. 'Write a poem about rain' gets framing analyst, research analyst, solution designer, chief synthesiser, critical reviewer). The UI labels this ('planned by template' badge in NativeAI.tsx; the Cockpit template note), so the gap is large but disclosed: tier 3.
- **claim:** §6 bespoke-per-solution and per-founder swarms (founder digital twin), and optimised cascades.
- **observed:** I ran POST /native-ai/tree twice; both returned planner='deterministic_template' and template roles. grep found no optimise or score function over cascades. No founder-twin input reaches cascade construction.
- **evidence:** POST /api/v1/native-ai/tree response.planner; NativeAI.tsx:102-112 tree-planner badge; genesis.py:958
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run the tree route. The assessor's evidence of the planner=deterministic_template response and the UI badge supports a disclosed gap, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty; the capability is the remaining work.

### R4.3 · The AI is native and in-house-first; external providers are opt-in, and provenance is truthful on the final response, swarm stages, saved runs and SSE done frames — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** Every response I executed told the reader who served it: served_by='native' and is_external=false on /native-ai/complete; per-stage served_by on /swarm and /resources/swarm/run traces (with served_by_all and a UEG audit hash); per-node served_by on /tree; served_by in the SSE done frame of /api/v310/entrepreneur/generate-plan/stream. /native-ai/status reports is_real_model=false, mode=deterministic_floor, floor_active=true, and NativeAI.tsx shows it as an amber floor banner. The floor's text says it is 'framing the request above rather than analysing it'. There is nothing to tier.
- **claim:** §6 native owned capability, with external providers as optional accelerants and never dependencies.
- **observed:** /native-ai/status: posture in-house-first, external_allowed false, selection_order ['native']. /models lists owned tiers and notes AI_ALLOW_EXTERNAL opt-in. No external call was needed to serve anything.
- **evidence:** curl /api/v1/native-ai/status, /models, POST /complete, /swarm, /tree, /api/v1/resources/swarm/run, /api/v310/entrepreneur/generate-plan/stream (done frame served_by native)
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The assessor's executed provenance evidence is consistent with the floor posture I saw. Nothing contradicts it.

### R4.4 · Users can design, save, edit, run and retire their own swarm cascades in the Primitive Console cascade designer — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** I defined a one-stage 'critic' cascade through POST /resources/swarm/define, which is the call NativeAI.tsx makes, and ran it through /resources/swarm/run. It executed my stage with per-step provenance and a UEG hash. The UI exposes Edit (PUT), Run and Retire (DELETE with a confirmation that names what else it touches), and /visual-composer redirects to /native-ai?focus=cascade-designer. It works as described, so there is no tier.
- **claim:** §6/§7 users reconfigure the AI Agent Swarm cascades, workflows and pipelines.
- **observed:** swarm-fb064028 was created and run (run sr-ec493a23, served_by_all ['native'], audit.logged true).
- **evidence:** apps/workstation-superapp/src/pages/developers/NativeAI.tsx:544-590,938-1030; POST /api/v1/resources/swarm/define and /run
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). I accept the assessor's executed define and run with a named run id. I did not re-run it.

### R4.5 · There is no step that models or simulates a user's cascade or organisation reconfiguration before it is committed — **MISSING** · tier 3

- **severity (assessor):** medium
- **why it is this tier (assessor):** §7 says the platform models and simulates the configuration before commit. In the designer, Save writes the cascade directly. The define response contains no simulation, and NativeAI.tsx has no preview or simulate control. The page does not claim to simulate, so nothing untrue is said, and the absence is visible from the surface. That puts it at tier 3, not tier 2.
- **claim:** §7: the platform models and simulates the configuration before commit.
- **observed:** /resources/swarm/define returned the stored record immediately, with no simulation or validation output. I found no simulate-before-commit path in the designer.
- **evidence:** POST /api/v1/resources/swarm/define response; NativeAI.tsx saveCascade (~560-580)
- **disclosed to the user:** implicitly (no such control exists)
- **refutation: SURVIVED** (reproduced by the refuter). The UI makes no claim to simulate, so nothing untrue is shown. The absence is visible from the surface, so tier 3.

### R4.6 · The workflow tree's QMS gate, integration check and decision report 'not assessable' honestly on floor output — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** The tree response says qms_passed=null with the basis 'not assessable — every node floor-served; the length proxy cannot fail', integrated=null with the basis 'overlap measured over templates says nothing', and decision/consensus 'not assessable'. The governance steps cannot certify floor output, and the response says exactly that instead of certifying it. Disclosed, so tier 3.
- **claim:** §6 autonomous workflow trees verified, tested and validated.
- **observed:** From POST /native-ai/tree: the governance, validation, decision and consensus blocks all carry not-assessable bases.
- **evidence:** POST /api/v1/native-ai/tree
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The response states its not-assessable bases explicitly, so the gap is disclosed: tier 3.

### R4.7 · The metabolic/ATP term behind cardiovascular allocation is a simulator that cannot fall, so the 'conserving' survival posture can never be reached (disclosed) — **PARTIAL** · tier 3

- **severity (assessor):** medium (capability)
- **why it is this tier (assessor):** The homeostasis payload says atp_measured=false, atp_can_fall=false and conserving_posture_reachable=false, and explains why. Introspection labels the bar 'Metabolic (simulated ATP …)'. The Cardiovascular layer allocates parallelism partly from a simulated figure, and the system says so, so this is tier 3.
- **claim:** §17.2 Cardiovascular dynamic resource allocation; homeostasis loops and a survival instinct.
- **observed:** The tree response's homeostasis.organism carries atp_basis and conserving_posture_basis. composite_health_basis states that 40% of the weight is measured.
- **evidence:** POST /api/v1/native-ai/tree .homeostasis; GET /api/v1/organism/status composite_health_basis; Introspection.tsx:119
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The payload and the UI both label the ATP figure simulated, so tier 3. The fallback branch in app_mvp.py also labels a real measurement correctly.

### R4.8 · The seven biomimetic layers: the nervous ring, the immune sensing and the reflex arcs are real; the genome is empty and separate from the VSB registry — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** Live /organism/systems shows a real nervous signal ring (68 signals in 60s, reflex_arcs_registered=2, registered by heartbeat.py:1106), real immune sensing, and self-healing that honestly says 'no circuit has carried a call yet — health unknown'. /organism/genome returns 0 genomes with 'no genomes stored yet', and organism/genome.py is not the VSB GenomicRegistry, so the arms-length identity is not one thing. Each gap is stated in its payload, so this is tier 3, not tier 2.
- **claim:** §17.2 seven layers (Genome, Nervous, Immune, Cardiovascular, Respiratory, Musculoskeletal, Endocrine).
- **observed:** organism/* totals about 4,000 lines of real code. Endpoints respond with measured or explicitly unmeasured values.
- **evidence:** GET /api/v1/organism/systems, /api/v1/organism/genome; agentic_core/organism/heartbeat.py:1085-1106
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). Each gap is stated in its own payload, so tier 3.

### R4.9 · The streaming business-plan generator carries correct provenance, but no page calls it — **API_ONLY** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** POST /api/v310/entrepreneur/generate-plan/stream ends with a truthful done frame (served_by native, is_external false). grep finds no caller in apps/workstation-superapp/src, so nobody reaches it from the UI. It is not misleading anyone, which makes it tier 3 (a surface nobody reaches).
- **claim:** §6 the native AI resource serves the VSBs it generates.
- **observed:** I executed the stream: the done frame includes served_by. There is no frontend reference to the route.
- **evidence:** agentic_core/api/v310/business.py:70-115; grep 'generate-plan/stream' over apps/workstation-superapp/src returns nothing
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). No UI calls the route, and its body is truthful, so tier 3 (a surface nobody reaches).

---

## R5 — §1–§3, §3A, §9, §14, §15, §17.1 — the offerings, the avatar/UX, democratisation, the founding principles, the 4×6×4 grid

**Assessor's region summary:** I ran tools in all six Domains against the live server. Every floor-served surface (the six Domain tools and avatar chat) labels itself as the native floor through a banner, ai_provenance/served_by and floor_note. avatar/status reports 'deterministic floor'. I found no fabricated figures. Care NEWS2 is a real computation, and the QEP Tajwid coach refuses recitation scoring per A.9.1.  The one truth-adjacent issue, at tier 2: in the legal analysis and CV outputs, the floor's 'risk frame' bullets ('Exposure on <term>') lack the 'terms, not findings' caveat that the other sections carry.  Everything else is a disclosed capability gap (tier 3): - the tafsir frame is built from the platform's own text; - the avatar does not ground answers in enterprise data and does not say so; - there is no in-house text-to-speech; - interface translation covers chrome only, in five languages; - no single view shows the whole grid.  UI checks came from reading the source (I could not drive a browser), and I sampled one tool per domain. I reported 10 findings and did not hit the cap, but this was a sample, not an exhaustive sweep.

### R5.0 · The floor's 'risk' sections assert 'Exposure on <term>' for words echoed from the request, as if they were identified risks — **PARTIAL** · tier 2

- **why it is this tier (assessor):** A reader of POST /law/analyse sees '## Legal Risks ... - Exposure on deposit discretion', and of /employment/cv sees '## Gaps & Recommendations - Exposure on nurse. - Exposure on years.' Other sections carry 'The list below is the request's most frequent terms, not findings about them'. These risk bullets get only 'surface, don't invent', so they read as findings. The response does label the native floor (banner plus ai_provenance.floor_note), so nobody is told a model ran; that keeps it out of tier 1. The risk wording on its own is not disclosed, so it is tier 2 rather than 3.
- **claim:** §2/§3 six Domains offer in-house-AI-mediated tools; Principle 6 says never fabricate
- **observed:** Law analyse and Employment CV return term-count frames. Their risk and gap headings list 'Exposure on X' for X taken from the input words.
- **evidence:** curl POST /api/v1/law/analyse {document_text:'The tenant shall pay a deposit...'} and POST /api/v1/employment/cv {target_role:'nurse',experience:'5 years'} at 127.0.0.1:8031
- **disclosed to the user:** floor disclosed; the risk-bullet semantics are not
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. /employment/cv shows 'Gaps & Recommendations' followed by '- Exposure on nurse.' and '- Exposure on years.', and those bullets lack the 'not findings' caveat the other sections carry. The floor is disclosed, so this is not tier 1. The risk semantics are undisclosed, so it is not tier 3 either.
- **refuter's evidence:** I sent POST /employment/cv live and saw both 'Exposure on nurse.' and 'Exposure on years.' in the body.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Give the risk-frame bullets the same 'terms, not findings' caveat, or word them as 'Check: <term>'.

### R5.1 · The floor's CV and legal frames print an empty 'Subject:' line — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The reader sees 'Subject:  (domain: WITHHELD — the request named no domain)'. The field is blank, which is an omission and asserts nothing untrue, so it is tier 3 rather than 2.
- **claim:** §3 Domain tools usable end to end
- **observed:** The CV and law analysis outputs open with an empty Subject line.
- **evidence:** POST /api/v1/employment/cv and /api/v1/law/analyse response bodies
- **disclosed to the user:** yes, as floor output
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced the line 'Subject:  (domain: WITHHELD — the request named no domain)'. The blank field is an omission and asserts nothing untrue, so tier 3 is right rather than tier 2.
- **refuter's evidence:** Live CV body.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Fill Subject from target_role or document_type.

### R5.2 · The six Domain tools answer from the term-count floor and say so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Every body starts '_[Workstation native structured engine ...]_', and ai_provenance.served_by='native' comes with a floor_note saying it was 'Composed by the native floor, not by a model'. The shortfall is fully stated at the surface, so it is tier 3. Care's NEWS2 is a real deterministic computation that reports missing observations honestly.
- **claim:** §2-§3 every Domain offers real in-house-AI-mediated tools
- **observed:** Routes exist for religion, science, education, law, employment and care, and each executed tool returned a disclosed frame. Care risk-assess computes NEWS2 from the published table and declines to give a total when observations are missing.
- **evidence:** POST /religion/quran-tafsir, /science/hypothesis, /law/analyse, /employment/cv, /care/risk-assess. Only /employment/services exists as a /services listing; the other domains list via /religion/schools, /science/methodologies, /education/frameworks, /care/tools and /law/templates.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The native-engine banner and served_by:native are visible on the CV body I fetched. I did not run NEWS2 myself. The floor is disclosed, so this is tier 3 rather than tier 2.
- **refuter's evidence:** The CV body starts with '_[Workstation native structured engine ...'.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none needed for honesty; the gap is model capability in this environment

### R5.3 · Quran tafsir withholds the Arabic when its source is unreachable, then builds its frame from its own meta-text — **PARTIAL** · tier 3

- **why it is this tier (assessor):** arabic_source reads 'unavailable — source unreachable; the Arabic is never AI-generated, so none is shown', which honours A.9's ban on generated Arabic. The sections for Context of Revelation, Linguistic Analysis and Exegesis list 'authoritative arabic', 'not fetched' and 'text could' as terms. That is nonsense, but the response labels it 'not findings', so it is a disclosed gap (tier 3).
- **claim:** Appendix A.1/A.6: Religion offering-1 depth (tafsir and study)
- **observed:** No Arabic was invented. The tafsir content is the floor's term list over the platform's own composed sentence.
- **evidence:** POST /api/v1/religion/quran-tafsir {surah:2,ayah_start:255,ayah_end:255}
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed live that arabic_source reads 'unavailable ... never AI-generated'. I did not check the meta-text term lists myself, but they follow the same floor pattern that labels terms as not findings, so the gap is disclosed and sits at tier 3.
- **refuter's evidence:** POST /religion/quran-tafsir 2:255.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Leave the platform's own caveat text out of the term count, and say 'no tafsir available offline'.

### R5.4 · The Tajwid coach refuses to score recitation and says why (A.9.1 boundary) — **DELIVERED**

- **why it is this tier (assessor):** The source renders 'Recitation assessment unavailable ... No judgement is made about your recitation', and the recitation tournament card reads 'REFUSED (A.9.1)'. A refused and disclosed ratified boundary counts as delivered. I read this in the source; I could not drive a browser.
- **claim:** Appendix A.9: recitation is never scored
- **observed:** The former 94.2% score literal has been removed, and the UI states the refusal.
- **evidence:** apps/workstation-superapp/src/pages/domains/QEPReligionHub.tsx lines 55-243
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). QEPReligionHub.tsx:211 shows 'REFUSED (A.9.1)', and line 55 records that the 94.2% score was removed. This is a ratified boundary that is refused and disclosed, so it counts as delivered. I read this in the source; I did not drive a browser.
- **refuter's evidence:** QEPReligionHub.tsx:55, 211
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R5.5 · Avatar chat answers 'What are my open projects?' generically, without saying it read no enterprise data — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The response body gives grounded_in:null and context:'general', and the UI shows 'grounded in your enterprise ...' only when groundedIn is set. Saying nothing about grounding is an omission, not a false claim, and the floor banner is present. That makes it tier 3, and it would rise to 2 only if the UI implied grounding.
- **claim:** §9 multimodal, enterprise-aware avatar
- **observed:** With no enterprise present, the chat returns the floor frame and puts null in the grounding fields. image_understood is false, image_status is 'none', and profile_applied is false with the basis 'you have not written a profile'.
- **evidence:** POST /api/v1/avatar/chat; GET /avatar/status reports effective_serving_mode 'deterministic floor'; ConversationPanel.tsx:131
- **disclosed to the user:** partly (floor yes, ungrounded only by the absence of a grounding line)
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this one. If grounded_in is null, the missing grounding is an omission, and the floor is disclosed. That makes it tier 3, not tier 2, unless the UI implies grounding, which the assessor reports it does not.
- **refuter's evidence:** Assessor's evidence; not executed by me.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** State 'not grounded in any enterprise' when grounded_in is null.

### R5.6 · Avatar voice output refuses external TTS honestly and defers to the browser's speechSynthesis — **PARTIAL** · tier 3

- **why it is this tier (assessor):** POST /avatar/speak returns 503 with 'External voice output is unavailable ... The browser's speechSynthesis is the in-house path — nothing was sent externally.' The limitation is stated outright, so it is tier 3.
- **claim:** §9 voice avatar
- **observed:** There is no server-side in-house TTS. Voice depends on the browser.
- **evidence:** curl POST /api/v1/avatar/speak
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced the 503, which says the browser's speechSynthesis is the in-house path and nothing was sent externally. The limitation is stated outright, so this is tier 3.
- **refuter's evidence:** Live /avatar/speak
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none needed

### R5.7 · Interface translation covers only chrome in five languages, and Settings says so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Settings shows 'The interface is translated (N strings)' or 'not translated into this language yet — it stays in English', followed by 'Translation covers interface chrome, not every screen, and AI-generated content is still produced in English'. That is a disclosed gap (tier 3). useT is used in about 7 of roughly 71 page and component files.
- **claim:** §14 democratisation: all-language, accessible
- **observed:** Dictionaries exist for en, ar, fr, es and ur. The picker is trimmed to those, RTL flips for ar and ur, and dictation honestly defers to the browser.
- **evidence:** apps/workstation-superapp/src/pages/Settings.tsx:115-160; src/lib/i18n.tsx:363-390
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-read Settings.tsx. If the disclosure text is as quoted, the gap is disclosed at the surface, so tier 3 rather than tier 2.
- **refuter's evidence:** Assessor's evidence.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none for honesty; extend coverage

### R5.8 · The explicit user profile (W428) is stored and reported honestly, including when it is empty — **DELIVERED**

- **why it is this tier (assessor):** GET /user/profile returns the empty fields with applied_to 'generation prompts on this platform (never shared with other users)'. The avatar reports profile_applied:false with the basis 'you have not written a profile', which is accurate.
- **claim:** §14 personalisation through an explicit profile
- **observed:** The route works, and its effect is surfaced in the avatar response.
- **evidence:** curl /api/v1/user/profile; avatar/chat profile_state
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. GET /user/profile returns the empty fields and the applied_to statement, which is accurate.
- **refuter's evidence:** Live /user/profile
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R5.9 · The 4 Realms x 6 Domains x 4 Products grid has one canonical vocabulary, and Genesis exposes it — **PARTIAL** · tier 3

- **why it is this tier (assessor):** taxonomy.ts mirrors agentic_core/taxonomy.py (four realms, six domains, four products), and GenesisJourney renders a product picker from PRODUCTS. taxonomy.py states that realm changes only depth and register, by Owner decision. There is no single grid view. That is a scope decision stated in the canon, not a hidden claim, so it is tier 3.
- **claim:** §17.1 the 4x6x4 grid
- **observed:** The vocabulary is canonical and imported by 10 surfaces. No surface presents the grid as a whole.
- **evidence:** apps/workstation-superapp/src/lib/taxonomy.ts:5-9; GenesisJourney.tsx:3,691; agentic_core/taxonomy.py:45-50
- **disclosed to the user:** in canon comments, not in the UI
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-verify the import count. No surface presents the whole grid, but that is a scope gap and does not assert anything untrue, so tier 3 rather than tier 2.
- **refuter's evidence:** Assessor's evidence.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Optionally render the grid on DomainsHub.

---

## R6 — §8 + §12 + §17.5 — the biomimetic living organism, the economic organism, the ten architecture invariants

**Assessor's region summary:** I assessed R6 at HEAD 51597af by running the live routes. I posted cycles under four probe ids (r6-probe-a, c, d and e), ran two period closes, tried one transfer, and briefly set a charity exclusion and then cleared it. The UI was assessed by reading its source, not by driving a browser.  Delivered: the economy's double-entry books balance across a cycle and two closes, the virtual-WST and real-money disclosures appear everywhere, and heartbeat beats honestly record what they could not do.  The two truth defects: - The Organism dashboard says ATP 'recovers on the circadian cycle', but the circadian link is off and ATP cannot fall. - A charity cycle stores a false reason for not funding an Owner-excluded cause ('not among the candidate causes'), and calls editorial defaults 'Owner-named'.  The organism still cannot regulate itself: the survival instinct can never fire. That is disclosed in the API and on a developer page, but not on the organism pages.  Selection, mitosis and removal can be reached only through the API, and the API answers honestly.  On the ten invariants: most hold. The GaaS gate is not held and the system says so (37 of 63 modules). User isolation on sovereign_evolution could not be tested live because auth is off. The vision's §17.5 status line is stale and understates what the code now holds.  I did not exercise a transfer between two living entities, because only one exists. I stayed under the ten-finding cap only by not itemising each invariant separately.

### R6.0 · The Organism dashboard tells users ATP 'recovers on the circadian cycle', but the circadian-to-ATP link is off and ATP cannot fall — **PARTIAL** · tier 1

- **why it is this tier (assessor):** OrganismDashboard.tsx:270 shows every visitor the sentence 'each run expends ATP, which recovers on the circadian cycle'. In the live heartbeat status circadian_to_atp is false (the default under the Owner ruling of 2026-10-07), and /native-ai/homeostasis reports atp_can_fall:false. The sentence states a mechanism that is not running, so it is an untrue assertion, not an omission. That makes it tier 1 rather than tier 2.
- **claim:** §8: homeostasis loops, circadian operation and a survival instinct make the organism dynamic and self-regulating. The W512 record says it cannot yet regulate, because ATP cannot deplete and the circadian map is never passed to metabolism.
- **observed:** GET /api/v1/heartbeat/status returned circadian_to_atp:false. GET /api/v1/native-ai/homeostasis returned atp_can_fall:false and conserving_posture_reachable:false, with a basis saying production 0.40 is always more than consumption 0.10. The dashboard's Metabolic card shows 'ATP ratio 100%' with no 'simulated' label beside it.
- **evidence:** apps/workstation-superapp/src/pages/organism/OrganismDashboard.tsx:270-271 and :424-429; agentic_core/organism/biobus.py:47-77 (atp_depletion_state); live /heartbeat/status and /native-ai/homeostasis
- **disclosed to the user:** Only on the developer NativeAI page and in API basis strings. The organism pages do not disclose it.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. OrganismDashboard.tsx:270-271 shows every visitor the sentence 'each run expends ATP, which recovers on the circadian cycle'. That states a mechanism that does not run (circadian_to_atp is off and ATP cannot fall). It is an untrue assertion on a page people reach, so tier 1 rather than 2.
- **refuter's evidence:** apps/workstation-superapp/src/pages/organism/OrganismDashboard.tsx:270-271
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Change the sentence based on circadian_to_atp and atp_can_fall, for example: 'ATP is a simulation that cannot fall; the circadian link is off'. Label the Metabolic card 'simulated'.

### R6.1 · A charity cycle gives a false reason for not funding an Owner-excluded cause and calls editorial defaults 'Owner-named' — **PARTIAL** · tier 1

- **why it is this tier (assessor):** With the Owner's exclusion of 'dawah' saved, the cycle's stored giving_back record says priorities_unfunded: dawah, 'not among the candidate causes, so it cannot be funded'. Dawah is a candidate cause: charity.py:19 defines it, and the next cycle after the exclusion was cleared funded it with 22.91 WST. The record also keeps dawah under 'priorities', excluded_by_compliance is empty, and allocation_rule says 'each Owner-named priority… receives 10%' while directives report priorities_owner_named:[]. These are false statements in the stored record about why money moved, so tier 1 rather than tier 2.
- **claim:** §12: the Owner sets directives for the four causes and inclusions and exclusions are honoured. Every split is UEG-logged.
- **observed:** The exclusion itself IS honoured: no dawah grant was made while it was excluded. Only the record of why is untrue. Five causes were funded, including two outside the four named ones (famine_food and emergency_health). The weights are disclosed as curated, editorial values.
- **evidence:** POST /economy/charity/directives {exclusions:[dawah]}, then POST /economy/cycle {vsb_id:r6-probe-d, revenue:1000}, giving_back.priorities_unfunded and allocation_rule; then exclusion cleared and r6-probe-e funded dawah 22.91; agentic_core/economy/charity.py:13-25
- **disclosed to the user:** No. The record asserts the wrong cause.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed in code. In charity.py:223-232, _unfunded_priorities builds its list from _candidates(), which drops excluded causes. An Owner-excluded priority therefore gets the reason 'not among the candidate causes, so it cannot be funded'. The real reason is the Owner's exclusion. A stored record giving a false reason for how money moved is tier 1.
- **refuter's evidence:** agentic_core/economy/charity.py:223-232
- **smallest honest fix (assessor's proposal — a lead, not a decision):** When a cause is unfunded because of an exclusion, give the reason 'excluded by the Owner's directive'. Drop excluded causes from 'priorities'. Say 'editorial-default priority' when priorities_owner_named is empty.

### R6.2 · The survival instinct and energy regulation cannot fire, and the organism pages do not say so — **PARTIAL** · tier 2

- **why it is this tier (assessor):** HeartbeatMonitor shows a 'self-healed ATP' badge described as 'the §8 survival instinct — the organism autonomously rested'. The badge can never appear, because ATP cannot fall below 0.3. No organism page states that the instinct is unreachable. That is an invisible shortfall, not a false figure, because a badge that never renders asserts nothing. So tier 2 rather than 1. It is not tier 3, because the disclosure exists only in API JSON and on a developer page.
- **claim:** §8: the organism defends itself and heals, with a survival instinct and homeostasis loops.
- **observed:** Each beat runs pulse, homeostasis and transformation_tick. last_recovery and last_self_healing are null after 9 beats. self-healing health is 'defaulted to 1.0, not a measurement', which IS disclosed on the dashboard and Anatomy pages. Every lever (auto_economy, auto_evolve, auto_metabolic, and others) is off by default.
- **evidence:** GET /api/v1/heartbeat/status (recent[] beats 8-9, actions); HeartbeatMonitor.tsx:345-346; /native-ai/homeostasis conserving_posture_reachable:false
- **disclosed to the user:** Only on the developer NativeAI page. Not on the Heartbeat, Organism or Anatomy pages.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. The badge at HeartbeatMonitor.tsx:346 renders only if a recovery happens, and that cannot happen. A badge that never renders asserts nothing, so this is not tier 1. The organism pages do not disclose that the instinct is unreachable, so it is not tier 3. Tier 2.
- **refuter's evidence:** HeartbeatMonitor.tsx:346
- **smallest honest fix (assessor's proposal — a lead, not a decision):** On HeartbeatMonitor, render conserving_posture_basis or atp_can_fall next to the survival-instinct legend.

### R6.3 · The heartbeat API reports 'last_realisation: 0.924' with no label saying it is API-surface coverage — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The UI labels this figure correctly as 'API coverage (not delivery)' (HeartbeatMonitor.tsx:130). The /heartbeat/status body, and every beat record and UEG heartbeat event, store it as 'realisation' with no measure field. A reader of the API or the audit chain is not told what was measured. Tier 2: the API surface does not state the shortfall, but the surface people actually use does, so the figure misleads nobody there and it is not tier 1. Note that the source of the number, _realise(), DOES carry a measure string.
- **claim:** §8 W482 naming invariant: 'API-surface coverage is not vision realisation'.
- **observed:** In /heartbeat/status, last_realisation is 0.924 and each recent[] entry has realisation 0.924, with no basis or measure field.
- **evidence:** agentic_core/organism/heartbeat.py:640, 840-846, 1299; agentic_core/api/transformation.py:194-199
- **disclosed to the user:** In the UI, yes. In the API and the UEG record, no.
- **refutation: SURVIVED** (reproduced by the refuter). Accepted on the cited lines; I did not re-execute the route. The API and the UEG record carry the bare word 'realisation' with no label saying it measures API coverage. The UI does label it, so nobody using the UI is misled: not tier 1. Tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename the field to last_api_coverage, or carry _realise()['measure'] alongside it in the status and the beat record.

### R6.4 · Organism selection, mitosis and removal exist as honest APIs but no page reaches them — **API_ONLY** · tier 3

- **why it is this tier (assessor):** GET /organism/selection/{id} returns status NOT_ASSESSABLE. It says user_satisfaction and founder_alignment are 'NOT MEASURED… nothing is counted as a zero'. That is an honest response that no UI calls, so it is a surface nobody reaches: tier 3.
- **claim:** §8 W512: the organism must turn over (apoptosis and mitosis together) and select on the four measures (profitability, satisfaction, founder alignment, compliance).
- **observed:** No .tsx file references /organism/selection, propose-mitosis, propose-removal or retirement-check. Only living-vsbs/{id}/lifecycle is wired, in VSBCockpit.tsx:1199.
- **evidence:** live GET /api/v1/organism/selection/vsb-7093817949; grep of apps/workstation-superapp/src
- **disclosed to the user:** Yes, in the API body. There is no UI.
- **refutation: SURVIVED** (reproduced by the refuter). The responses are honest and no page calls them. A surface nobody reaches is tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Show the selection reading, with its NOT_ASSESSABLE basis, on the VSB Cockpit or the Anatomy page.

### R6.5 · The GaaS gate on every output (invariant 2) is not held, and the system says so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** _gaas_coverage() reports '37 of 63 API modules call a… gate… There is NO global gate… §17.5 invariant 2 is NOT held', and this appears in the governance pillar evidence. The system states the shortfall itself, so it is tier 3 however large the gap.
- **claim:** §17.5 invariant: mandatory GaaS gate on every output.
- **observed:** 26 API modules make no gate call. The HTTP middleware observes traffic and does not gate it.
- **evidence:** agentic_core/api/transformation.py:152-165, run against HEAD
- **disclosed to the user:** Yes, in the realisation evidence the CognitionIntegration page shows.
- **refutation: SURVIVED** (reproduced by the refuter). The system states the shortfall itself. A shortfall the surface discloses is tier 3, however large.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Add a global output gate, or keep the disclosure as it is.

### R6.6 · The vision's own §17.5 status paragraph is stale: the code now holds more than it says — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The vision (lines 880-888) says 'GaaS gate… true for 8 of 57 API modules', that the organism perimeter 'carries no auth dependency', and that for the KPI gate 'nothing gates any delivery'. The code has 37 of 63, mounts heartbeat with dependencies=[_require_admin] (app_mvp.py:475), and has kpi_release_gate enforced on marketplace listings (marketplace.py:377-385). The doc understates the system, so it overclaims nothing and misleads no user into trusting more than exists. Tier 3, not tier 1.
- **claim:** §17.5 status of the ten invariants.
- **observed:** Six invariants hold in code by inspection: append-only DCS, single router mount (include_router only in app_mvp.py), arms-length via CCA-gated evolution_auto_apply, twin pre-validation, plan staleness, and torch optionality (live backend running and torch not importable in this interpreter). The KPI gate is a presence test that the code says is a presence test. Partly held: user isolation (sovereign_evolution.py has 0 Depends; not verifiable live with AUTH off) and GaaS.
- **evidence:** docs/WORKSTATION_IDBO_WHOLE_VISION.md:871-888; agentic_core/app_mvp.py:475; agentic_core/api/business_plan.py:201-231; agentic_core/api/marketplace.py:377-385
- **disclosed to the user:** n/a (canon doc)
- **refutation: SURVIVED** (reproduced by the refuter). The doc understates what the code does, so it overclaims nothing and misleads no user. That rules out DOC_OVERCLAIM and keeps it a stale canon paragraph at tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Re-measure the §17.5 status line from code.

### R6.7 · Double-entry books balance across a cycle and two period closes, and the statements disclose their own limits — **DELIVERED**

- **why it is this tier (assessor):** Executed, not read: the trial balance was 1000/1000 and balanced; the balance sheet was 200 = 200 and balanced; the second close rolled 200 to retained_earnings and still balanced. net_profit_basis says it is a 'SURPLUS AFTER WATERFALL DISTRIBUTIONS, not a profit', and the cash-flow basis says the zero is 'ZERO BY CONSTRUCTION'. No untrue figure was found.
- **claim:** §12: double-entry books with period close and CFO statements.
- **observed:** POST /economy/cycle r6-probe-a (revenue 1000, costs 100) gave reserves 200 (costs + 20%... note: 200 = 20% of revenue, with costs 100 deducted separately) and distributable 700. That splits 140/210/140/105/105 under the 20/30/20/15/15 template. Two POST /close-period calls both balanced.
- **evidence:** live POST /api/v1/economy/cycle, /close-period x2, GET /ledger/r6-probe-a
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). I accept the executed balances. The assessor's note on how reserves were derived is muddled, but the figures it reports are internally consistent.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R6.8 · Virtual WST and the real-money gate are stated on every economy surface — **DELIVERED**

- **why it is this tier (assessor):** Every response carries 'Virtual/simulated WST… not real money'. owner-payments shows real_money_rails:'DISABLED'. A transfer to an unregistered entity is refused with 'no transfers into the void'. Nothing implies real funds moved.
- **claim:** §12: virtual/simulated money until the Owner directs real rails; REAL_MONEY_ENABLED is False.
- **observed:** Confirmed on /economy/status, /owner-payments, /cycle and the transfer refusal. A transfer between two living entities was not exercised, because only one living VSB exists.
- **evidence:** live GET /economy/owner-payments, POST /economy/transfer (r6-probe-a to r6-probe-b, refused)
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The virtual-money disclosure is present on every economy surface checked. No figure implies that real funds moved.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

### R6.9 · Each heartbeat reports what it could not do as well as what it did — **DELIVERED**

- **why it is this tier (assessor):** Every beat record carries steps_failed. Its basis says 'an EMPTY steps_failed means no step raised'. A quiet cadence says 'NO layer was due. This is a quiet cadence, not a broken one'. That is exactly the vision's demand that a beat report what it could not do.
- **claim:** §8: self-running and self-managing, and an engine 'computes or says it cannot'.
- **observed:** The heartbeat was running (9 beats, 60 s interval). _step_failed is used at every step (heartbeat.py:288-843). Opt-in levers are disclosed as off, and as runtime-only where they are not persisted.
- **evidence:** GET /api/v1/heartbeat/status recent[]; agentic_core/organism/heartbeat.py:1127-1134
- **disclosed to the user:** yes (HeartbeatMonitor)
- **refutation: SURVIVED** (reproduced by the refuter). Every beat record carries steps_failed and says plainly what it could not do. That matches the vision.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

---

*Regenerated by W632 from the audit workflow's journal. Every entry above is an observation against
the booted HEAD named in the header — routes executed, handlers and components read, stores counted —
not a claim read from another document. No browser was driven: statements about what a user SEES
(a chip's colour, a tab's default, a rendered badge) are reasoned from the component source, and the
assessors and refuters say so where it matters.*
