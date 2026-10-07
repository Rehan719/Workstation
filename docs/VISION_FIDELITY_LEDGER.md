# Vision Fidelity Ledger — v10 (2026-10-07) — MILESTONE M1 re-run

**Supersedes v9 as the current assessment.** v9 is kept whole at `VISION_FIDELITY_LEDGER_v9.md` (its
Tier-1 entries are the ones P1.17 closed and the register rows cite), as v3 is at `VISION_FIDELITY_LEDGER_v3.md`.
This edition re-measures the product after P1.17, the second truth pass, as the M1 line requires — the Tier-1
count is measured again, never declared: a fresh six-region assessment against HEAD `aeb9fa8` (port :8031,
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
R1 10, R2 10, R3 7, R4 6, R5 9, R6 9 — a region under the cap ran out of consequential gaps, one
at the cap may have more. **Every finding was then attacked by an independent
refuter instructed to default to refuted** (v2 refuted six per region), who had to reproduce the gap (execute the
route, read the code, count the store) before letting it stand, and who was told to correct the
verdict UP or DOWN when the assessor had it wrong.

Reading rules that follow from the method:

1. **DELIVERED is understated by construction.** Assessors were told their job was the gap that
   remains, but to report DELIVERED where they verified it. Read the DELIVERED entries as the
   floor of what works, not the ceiling.
2. **Every one of the 51 findings was individually refuted.** The refuters reproduced
   50 as stated and overturned 1 — 0 moved to a
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
| MISSING | 0 | 0 |
| DOC_OVERCLAIM | 2 | 2 |
| API_ONLY | 0 | 0 |
| PARTIAL | 34 | 34 |
| DELIVERED | 15 | 15 |
| **total** | **51** | **51** |

Standing tiers (non-DELIVERED entries, the tier the refuter stands behind):

| tier | count | meaning |
|---|---|---|
| **1** | **4** | truth defect on a reached surface — the M1 measure (target 0) |
| 2 | 12 | invisible shortfall (Phase P2's tier) |
| 3 | 19 | disclosed or unreached capability gap (Phase P3/P4) |

Per region:

| region | sections | findings | STUB | MISSING | DOC_OVERCLAIM | API_ONLY | PARTIAL | DELIVERED |
|---|---|---|---|---|---|---|---|---|
| R1 | §10 + §11 | 10 | 0 | 0 | 1 | 0 | 7 | 2 |
| R2 | §4 + §13 | 10 | 0 | 0 | 0 | 0 | 9 | 1 |
| R3 | §5 + §17.3 + §17.4 | 7 | 0 | 0 | 0 | 0 | 2 | 5 |
| R4 | §6 + §7 + §17.2 | 6 | 0 | 0 | 0 | 0 | 4 | 2 |
| R5 | §1–§3, §3A, §9, §14, §15, §17.1 | 9 | 0 | 0 | 0 | 0 | 8 | 1 |
| R6 | §8 + §12 + §17.5 | 9 | 0 | 0 | 1 | 0 | 4 | 4 |

The distilled, actionable form of the surviving gaps is **prompt v11 rev 2's `<ledger>` and
`<delivery_plan>`** (`docs/FABLE_DELIVERY_PROMPT.md`). This document is the evidence base behind
them: every `<ledger>` item cites the entries here it rests on by region.index, and every plan
workstream carries the region.index entries it closes (or says it rests on another instrument —
the reach audit for the scatter, the Owner's hand for P4).

---

## R1 — §10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution

**Assessor's region summary:** R1 (§10, §11, Appendix A) at HEAD 978a0af. Nothing was listening at 127.0.0.1:8031, so I booted the backend from HEAD myself (uvicorn agentic_core.app_mvp, AI_DISABLE_LOCAL=1, chromadb absent) and ran the region's routes against it. I read the UI from source and did not drive a browser. The alquran.cloud source returned 403 through this sandbox's proxy, so only the honest 'source unreachable' path of the sourced-Arabic rules could be exercised.  The region is mostly honest. §10 measurement is verified DELIVERED on deliverables, export and Genesis (0/16 measured on the floor, tie withheld). The faith constitution's refusals hold: tafsir now renders its sourcing and floor notes, translation returns 503, out-of-range ayaat return 422, recall states its scope, and QEP analytics and audit report null instead of figures.  Two tier-1 defects remain: - **Feature badges:** the QEP feature grid's hardcoded 'planned' badge on the AI Tajwīd Coach (recitation scoring), on Certifications (both ratified refusals) and on the live Competitions card. - **Written recall:** the route treats caller-supplied text as 'authoritative' and labels it qiraat Hafs.  Three tier-2 gaps: - **Translation:** Qur'an translation is framed as a feature waiting on a model, and would serve unreviewed AI translation once one is enabled. - **Compliance FAIL hidden:** a §11 FAIL appears only in a tooltip on DomainTool surfaces and is dropped from copy and download. - **Awards:** unauthenticated, caller-named achievements are recorded and ranked.  Three tier-3 items: - **Scholar enrolment:** the review gate has no enrolment path. - **§11 compliance claim:** the compliance engines can refuse but never clear, and §11 is not amended to say so. - **A.6 features:** most are unbuilt, but every card and route says so.  I used all ten slots, including two DELIVERED entries. The register is not exhaustive. Smaller items remain: - **Genesis tooltip:** the per-candidate 'sim' tooltip cites '60/40' weights that the method does not apply. - **Adaptation registry:** it seeds a 'phoneme feedback loop' pattern even though recitation is never scored. - **Non-conformance rate:** the ServiceContracts fallback can print a 0.0% rate when no gate has run. - **Unexercised path:** the sourced-text success path still needs re-verification where alquran.cloud is reachable.

### R1.0 · The QEP feature grid in the Religion hub puts a 'PLANNED' badge on the AI Tajwīd Coach and on Certifications, both ratified refusals, and on Competitions, which is live — **PARTIAL** · tier 1

- **severity (assessor):** medium
- **why it is this tier (assessor):** Every card except Memorisation gets the same amber chip reading 'planned'. That includes 'AI Tajwīd Coach', so a user is told recitation scoring is on the roadmap, which is untrue: A.9.1 makes it a permanent boundary. It includes 'Certifications', which A.12.2 rules out. It also includes Competitions, whose leaderboard is live. Each card's description text says the opposite ('Not offered, by ruling'), so the surface contradicts itself, and the badge is the thing a reader scans. This is an assertion, not an omission, on a surface people actually reach, so it is tier 1 and not 2. The fix is trivial, but that does not change the tier.
- **claim:** A.9.1: recitation is never scored, 'a principled refusal, not a backlog entry'. A.12.2: QEP issues no certificate. A.9 preamble: an agent must not 'close a gap that is deliberately open'.
- **observed:** QEPFlagshipFeatures.tsx line 83 renders {f.id === 'memorization' ? 'live' : 'planned'} for all 15 cards. It ignores the `kind` field ('refused' / 'live') that the component defines and uses everywhere else, in the click panel at lines 65 and 111.
- **evidence:** apps/workstation-superapp/src/components/QEPFlagshipFeatures.tsx:34 (tajwid kind:'refused'), :36 (competitions kind:'live'), :47 (credentials kind:'refused'), :83 (badge hardcoded). Mounted at pages/domains/ReligionHub.tsx:125. I read this from the source; I could not drive a browser.
- **disclosed to the user:** Contradicted, not disclosed: the description under the badge gives the true status.
- **refutation: SURVIVED** (reproduced by the refuter). Reproduced in the source. QEPFlagshipFeatures.tsx:83 hardcodes the badge as {f.id==='memorization' ? 'live' : 'planned'}, so the refused Tajwid Coach and Certifications cards and the live Competitions card are all labelled 'planned'. Calling a ratified permanent refusal 'planned' is an untrue assertion on a reached surface, so it stays tier 1. It is not tier 2, because this is a false statement rather than a missing disclosure.
- **refuter's evidence:** apps/workstation-superapp/src/components/QEPFlagshipFeatures.tsx:83
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Derive the chip from f.kind: 'not offered' for refused cards, 'live' for live ones, 'planned' only when there is no kind.

### R1.1 · The written-recall check takes the 'authoritative' Arabic from the caller and labels any text it is given qiraat 'Hafs' — **PARTIAL** · tier 1

- **severity (assessor):** medium
- **why it is this tier (assessor):** I POSTed ayah_text='مرحبا بكم' (not Qur'an) to /api/v1/qep/tajweed/analyse. It returned comparable:true, qiraat:'Hafs', text_similarity 1.0 and kind 'written_recall_check'. That asserts a Qur'anic transmission for a string the platform never sourced, and it treats a recall as checked 'against the authoritative text' when nothing was fetched. The route is reached through its response body, so this is a figure and label the platform did not produce, which makes it tier 1. It is ranked below the badge because the Studio UI does pass the sourced ayah (QEPStudio.tsx:124), so a learner using the UI is not misled.
- **claim:** §11 rule 3: assessment is 'the learner's typed Arabic against the authoritative text'. Rules 1–2: sourced-only.
- **observed:** WrittenRecallRequest has only ayah_text and recited_text. The surah and ayah fields are not part of the model and are ignored. No fetch from alquran.cloud and no ayah-count check run on this route. The scope disclaimer about recitation is correct.
- **evidence:** agentic_core/religious_domain/api.py:707-735. Live curl response: {'comparison':{'comparable':true,'qiraat':'Hafs','text_similarity':1.0,...}} for non-Qur'anic input.
- **disclosed to the user:** No. The response says nothing about the reference text being caller-supplied.
- **refutation: SURVIVED** (reproduced by the refuter). Reproduced in the code. WrittenRecallRequest takes ayah_text from the caller, with a comment calling it 'from the authoritative source' that nothing enforces. TajwidCoach defaults qiraat to 'Hafs', which labels any text it is given. The response body says the text was checked against a Qur'anic transmission the platform never sourced, so tier 1 holds. The UI passes the sourced ayah, which keeps this ranked below finding 0. I read the code and did not re-run the curl.
- **refuter's evidence:** agentic_core/religious_domain/api.py:707-735; agentic_core/religious_domain/tajwid/coach.py:31
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Take surah and ayah, fetch the authoritative text on the server (refusing with 503 when the source is unreachable), and never accept ayah_text from the client.

### R1.2 · Qur'an translation is presented as a model-gated feature: the refusal and the Studio copy invite enabling a model, which would serve an unreviewed AI translation of sacred text — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** Today the route refuses with 503 (verified by execution). But the refusal text says 'Start a local model (Ollama) or enable an external accelerant'. The Studio says 'A translation must come from a model… the floor's output will never be presented as a translation of sacred text', and /translation/status lists 8 'supported_languages'. A reader learns that translating sacred text is a supported feature that is waiting on a model. With a model, the handler translates any text: no Qur'an detection, no licensed-source check (A.12.1), no scholar gate (A.12.3). Nothing tells the reader about that latent shortfall, so it is tier 2. It is not tier 1 because nothing false has been served yet.
- **claim:** A.9.3: translation refuses rather than approximates, and 'the inherited vision assumed translation as an ordinary feature. It is not one.' A.12.1: translations come only from licensed canonical editions. A.12.3: AI-composed religious content is withheld until a named scholar approves it.
- **observed:** translation_translate checks only whether a model is available, then sends req.text to gateway.query_meta and returns the model output with served_by. Unlike /tajweed/lesson and /curriculum, which go through scholar_review and are withheld, this path has no review gate.
- **evidence:** agentic_core/api/qep_intelligence.py:260-300. apps/workstation-superapp/src/components/QEPStudio.tsx:404-427. curl /api/v1/qep/translation/translate returned 503 'Start a local model (Ollama) or enable an external accelerant'.
- **disclosed to the user:** No. The surface frames the only obstacle as model availability.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. qep_intelligence.py:259-300 gates only on whether a model is available. The 503 refusal tells the reader to 'Start a local model (Ollama) or enable an external accelerant', and with a model the handler returns raw model output: no scholar gate, no licensed-source check. This is a latent shortfall the surface does not disclose, so tier 2. It is not tier 1 because the route serves nothing false today; it refuses.
- **refuter's evidence:** agentic_core/api/qep_intelligence.py:259-300
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Refuse translation of sacred text unconditionally, and serve translations only from a licensed edition carrying its A.12.1 provenance. Alternatively, route model output through scholar_review.published_body so it is withheld until approved.

### R1.3 · On every DomainTool surface, a §11 compliance FAIL appears only in a hover tooltip and is dropped from copy and download. A casino/riba mega-project is served as a normal deliverable — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** I POSTed {'concept':'casino and alcohol distribution hub with riba lending'} to /api/v1/mega-project/synthesise. It returned compliance_overall:'fail' alongside the full seven-section deliverable. In DomainTool.tsx the only place the verdict appears is the title attribute of the grey 'QMS —' chip ('· compliance fail'). withDisclosures, which builds the text for save, copy and download, adds the floor note and disclaimer but not the compliance verdict. A failed verdict that a reader never sees is an invisible shortfall, so tier 2. It is not tier 1 because nothing asserts the subject passed. Deliverables.tsx does this correctly: a red 'compliance FAIL' chip, and the verdict on page one of the export.
- **claim:** §11: compliance engines 'integrated into every synthesis/generative/operational workflow, not bolted on'.
- **observed:** The engine runs on every gateway call; I verified the fail verdict in the response. The DomainTool surface hides it. That covers every Offering-1 tool and the Resource Fabric run panel (ResourceFabric.tsx RUN_CONFIGS → DomainTool).
- **evidence:** apps/workstation-superapp/src/components/DomainTool.tsx:86-92 (withDisclosures has no compliance field) and :325 (tooltip only). Live mega-project response: ai_provenance.quality_assurance.compliance_overall='fail'.
- **disclosed to the user:** Only on hover.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. withDisclosures (DomainTool.tsx:86-92) adds no compliance verdict to the text that is saved, copied or downloaded, and the verdict appears only in the title tooltip at :325. A FAIL that the reader never sees is an invisible shortfall, so tier 2. It is not tier 1 because nothing asserts that the subject passed. I did not re-run the casino curl.
- **refuter's evidence:** apps/workstation-superapp/src/components/DomainTool.tsx:86-92,325
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Render a visible complianceChip in DomainTool, as Deliverables does, and append the FAIL verdict in withDisclosures so the exported text carries it.

### R1.4 · The QEP award route lets any unauthenticated caller name an achievement such as 'hafiz_complete', grant it XP for any uid, and have it ranked on the leaderboard — **PARTIAL** · tier 2

- **severity (assessor):** low
- **why it is this tier (assessor):** I POSTed {'uid':'u1','achievement':'hafiz_complete','xp':100}. The response was recorded:true, achievements:['hafiz_complete'] and 'scope':'recorded awards only — nothing here is estimated'. The leaderboard then ranks it. The leaderboard does say 'not a hifz certification', and that keeps this out of tier 1. But neither it nor the gamification state says that awards and their names are asserted by the caller, with no evidence and no identity check, so tier 2 rather than 3.
- **claim:** A.11: 'genuine SM-2 memorisation with persisted XP'. §11 honesty bar.
- **observed:** award_xp has no Depends(get_current_user) and no evidence requirement. The achievement is free text, capped only by xp ≤ 100 per call. The source 'explicit_award' is stored in history but never shown to a reader.
- **evidence:** agentic_core/religious_domain/api.py:834-849. Live curl as described. GET /api/v1/qep/leaderboard reads the same store.
- **disclosed to the user:** Partly: the 'not a certification' line is shown, but self-assertion is not.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed. award_xp at api.py:838 has no auth dependency, and the achievement is free text. The response asserts recorded:true and never says the award was self-asserted by the caller, so the shortfall is undisclosed: tier 2. The 'not a certification' line keeps it out of tier 1.
- **refuter's evidence:** agentic_core/religious_domain/religious_domain/api.py:834-849 (path: agentic_core/religious_domain/api.py)
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Bind uid to the authenticated user, restrict achievements to an enumerated set that only the platform's own review path awards, or label explicit awards as caller-asserted on the leaderboard.

### R1.5 · The scholar-review gate cannot be activated from the product: no route or caller enrols a scholar, so every QEP lesson and curriculum stays withheld — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** /tajweed/lesson and /curriculum honestly return null content with review_state 'withheld' and say 'no reviewer is engaged yet' (verified by execution). That is a disclosed state, which puts it at tier 3. The undisclosed part is that scholar_review.add_scholar has no caller and no router, so the Owner cannot 'engage a reviewer' through the platform; only a hand-edited JSON file would do it. A learner is not misled by this. The Owner is blocked.
- **claim:** A.12.3: a named scholar approves, 'enforced as a pipeline gate… inert until the Owner engages one'.
- **observed:** agentic_core/api/scholar_review.py defines add_scholar(), but nothing in agentic_core calls it, and the module mounts no router. decide() is reachable only through the qep_authoring reactor.
- **evidence:** grep add_scholar returns only its definition. The openapi listing has no scholar routes. Live /api/v1/qep/curriculum shows gate.scholars_on_roster 0.
- **disclosed to the user:** Yes for the withholding. No for the missing enrolment path.
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed: grep finds add_scholar only at its definition (scholar_review.py:88). The withholding is disclosed to the learner, and the missing enrolment path blocks only the Owner and misleads no one. That is tier 3, not tier 2.
- **refuter's evidence:** agentic_core/api/scholar_review.py:88
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Add an Owner-only route to enrol a scholar, with credential and added_by recorded, or state on the gate that enrolment is out of band.

### R1.6 · §11 promises 'live compliance' to legal, regulatory and international standards, but the engines are keyword screens that can refuse and never clear. The screens say so; §11 does not — **DOC_OVERCLAIM** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** I ran /api/v1/compliance/check on three subjects. A bakery came back 'review'/compliant null. A casino with alcohol failed on sharia_halal. A self-described certified halal shop came back 'review'. Every framework is reported as 'review'/'not_assessed', and constitutional (gaas.v5) as 'not_checked' for content. ComplianceChecker.tsx states 'It flags; it does not certify… NOTHING here assessed this subject.' The surface discloses the shortfall, so it is tier 3 however large the gap. §10 carries an Owner amendment naming what is unmeasured; §11 has no such amendment.
- **claim:** §11: 'Continuously monitored and evaluated live compliance to legal, regulatory, international, and industry best-practice standards… AI-mediated'.
- **observed:** /compliance/frameworks describes each engine as a haram-term, keyword or vocabulary screen. No framework can return a clearing pass.
- **evidence:** agentic_core/api/compliance.py:583-625. Live responses as above. apps/workstation-superapp/src/pages/governance/ComplianceChecker.tsx:62-63 and :123.
- **disclosed to the user:** Yes, on the compliance screen and in every quality record's verdict reasons.
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this by execution. The assessor's quoted ComplianceChecker disclosure is consistent with the honest-screen pattern I saw elsewhere. The doc overclaims, and the surface discloses the gap, so tier 3.
- **refuter's evidence:** agentic_core/api/compliance.py:583-625 (as cited)
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Amend §11 the way §10 was amended: name which frameworks have a screen that can refuse, and say that none can clear.

### R1.7 · The §10 quality bar is measured honestly on deliverables and Genesis: 0 of 16 measured on the floor, the identical-candidate ranking is withheld, and the export carries the bar on page one — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** These are verified behaviours of the amended §10 ('measured where an instrument exists; the record names what was not'), so no tier applies. /deliverables/produce returned the summary '0 measured · 0 attested · 2 screen-only · 14 not measured (of 16)', qms_gate_passed null with its basis, and an export headed 'COMPLIANCE: REVIEW… §10 bar…' plus the floor line. The Genesis journey returned the tie as detected, candidates_are_alternatives:false and 'categorised' attested from the caller's choice. GenesisJourney.tsx shows the comparison_note in place of the ranked cards, and Deliverables.tsx shows the §10 summary chip.
- **claim:** §10 as amended by Owner ruling R3: modelled, simulated, ranked and optimised are measured where an instrument exists and withheld on a tie, and the others are named as not met.
- **observed:** As described. The capability gap (no instruments for best-in-class, innovative and the others) is the ruling's own stated scope, not a defect.
- **evidence:** Live POST /api/v1/deliverables/produce (deliv-1997313d) and its /export. Live POST /api/v1/genesis/journey. pages/Deliverables.tsx:236-256. pages/synthesis/GenesisJourney.tsx:841-895.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this. I found no contrary evidence in my limited check, and the claimed behaviour matches the amended §10. Accepted as DELIVERED at low confidence.
- **refuter's evidence:** as cited
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** None required. A cosmetic point: the per-candidate 'sim' tooltip says 'declared weights 60/40' while the method reports form 1.0.

### R1.8 · Faith-content refusals hold: tafsir renders its sourcing, range and floor notes without a green QMS chip, translation refuses before any model call, nonexistent ayaat are refused, and recall states it says nothing about recitation — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** Verified by execution, so no tier. /religion/quran-tafsir returned arabic_text null with arabic_source 'unavailable — the Arabic is never AI-generated', sections_withheld [Transliteration, Translation], a floor_note ('not scholarship… study with a qualified teacher'), a disclaimer and qms_gate_passed null. ReligionHub.tsx:172-187 renders all of these, which closes the A.11 P1.8 defect. /qep/translation/translate returned 503. /qep/ayah/1/8 returned 422 'surah 1 has 7 ayaat'. Hadith and fatwa research on the floor withhold their grading and position sections. /qep/analytics/overview returns measured:false. /qep/compliance/audit returns compliant:null with not_checked controls. The A.9 refusals are delivered.
- **claim:** §11 rules 1–5. A.9.1–A.9.3. A.11.
- **observed:** All as described. In this environment alquran.cloud returned 403 through the proxy, so I could not exercise the sourced-Arabic success path (text present, labelled at source, range_note on truncation). I only exercised the honest unreachable path.
- **evidence:** Live curls as listed. apps/workstation-superapp/src/pages/domains/ReligionHub.tsx:169-194. agentic_core/api/qep_intelligence.py:275-285.
- **disclosed to the user:** Yes.
- **refutation: SURVIVED** (reproduced by the refuter). Partly verified: the translation refusal fires before any model call (qep_intelligence.py:273-285). The rest is accepted as cited. The sourced-Arabic success path was not exercised because of the 403, as the assessor notes.
- **refuter's evidence:** agentic_core/api/qep_intelligence.py:273-285
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** None. Re-verify the sourced path where alquran.cloud is reachable.

### R1.9 · Most of QEP's fifteen A.6 features are unbuilt, but each card and route says so: lessons and curriculum are withheld pending scholar review, and the analytics report nothing measured — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** Live: SM-2 hifz, written recall, the leaderboard and gamification. The others (AR/VR, community, offline, finance, assistant, adaptive layout) are labelled 'Planned' or 'Not yet built — nothing was run' in the click panel. /qep/status lists each component's state. Because the shortfall is stated at the surface, it is tier 3. The A.9/A.12 boundaries, such as emotion inference, Fitrah and the AI scholar, are correctly not counted as gaps.
- **claim:** A.6: fifteen core features.
- **observed:** The backend has 3 religious_domain modules plus the qep_intelligence and qep_analytics routes. The feature cards and /api/v1/qep/status disclose state per feature. LearnTeachModule says 'No scholars are verified on this deployment'.
- **evidence:** components/QEPFlagshipFeatures.tsx:34-51 and :111-122. Live GET /api/v1/qep/status, /api/v1/qep/curriculum and /api/v1/qep/tajweed/lesson (review_state 'withheld').
- **disclosed to the user:** Yes, in the descriptions and panels. The badge defect is the separate first finding.
- **refutation: SURVIVED** (reproduced by the refuter). The shortfall is disclosed in each card's description and in the click panel. The badge defect is tracked separately as finding 0. A disclosed gap is tier 3.
- **refuter's evidence:** QEPFlagshipFeatures.tsx:34-51
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None beyond building the features in plan order.

---

## R2 — §4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS

**Assessor's region summary:** The backend was not running at the stated address, so I booted HEAD (agentic_core.app_mvp, AI_DISABLE_LOCAL=1) on 127.0.0.1:8031 and exercised everything by curl. I read the UI from source; I did not drive a browser. Journeys run: Genesis journey; establish via the UI-shaped stream body; establish via a bare API body; VSB Spawn Studio spawn → name → website; repo, file, zip, ship, evolve and review-gates.  On the main Genesis path the system is largely honest about the floor. 7 of 7 stages are reported floor-served, the three identical candidates are not shown as a ranking, the deliverable says 'frames only — no enterprise established', and the UI-path establish ships a real 27-file git repo (Website, Web app, PWA) whose body is the founder's sentence plus disclosed 'content pending' states. Counted against the W434 lesson, 0 of 7 stages contain work on the user's problem; all of them are engine scaffold that echoes the problem's bigrams, and that is disclosed.  The remaining truth defects are narrow but real: 1. The website fallback copy ('Its solution is developed and delivered in-house, end to end') appears on the Spawn-Studio and bare-establish paths. 2. The §4.5 method sentence claims a forward simulation that the platform's own EVIDENCE.md says did not happen.  Tier-2 items are unqualified figures and labels: stage percentages on not-assessable stages, 'coherent whole: true', and 'Living Enterprise IDBO … governed'.  There is no single gated lifecycle: there are three spawn and establish entry points, and review gates are optional and empty by default. Run-forever and Develop do not run on the floor, and both say so.  I did not hit the cap; these 10 findings cover what I found in R2.

### R2.0 · Generated public website tells visitors the solution 'is developed and delivered in-house, end to end' when nothing was designed — **PARTIAL** · tier 1

- **severity (assessor):** high
- **why it is this tier (assessor):** A visitor to the enterprise's own Solution page reads 'LoafLink exists to solve <problem>. Its solution is developed and delivered in-house, end to end.' No design, develop stage or artefact exists for this entity (concept, design and commercialisation are all empty). This is a statement of an outcome the platform never produced, on a public surface the founder ships, so it is tier 1. It is not a tier-2 omission: the page does not leave the field blank, it asserts a fact.
- **claim:** §13 / W446: a body the floor served ships as the founder's own words plus an honest 'content pending the owned model' state, never as the enterprise's concept.
- **observed:** When an entity has no concept (VSB Spawn Studio path, or a direct POST /genesis/establish with no journey fields), _entity_fallback_copy falls back to a fixed sentence claiming delivery. The Genesis-UI establish path avoids this because it passes a pending string as the concept.
- **evidence:** POST /api/v1/vsb/spawn → vsb-914c1df0f6; POST /name {LoafLink}; POST /api/v1/vsb/vsb-914c1df0f6/website → data/vsb_repos/vsb-914c1df0f6/web/solution.html contains 'Its solution is developed and delivered in-house, end to end.' The same result came from POST /genesis/establish with no concept (vsb-8c7e9e4d38). Source: agentic_core/api/vsb.py:828-830.
- **disclosed to the user:** no; the page's footer adds 'Living VSB IDBO enterprise', which makes it worse
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed at vsb.py:828-830. With no concept, the fallback asserts 'developed and delivered in-house, end to end' on a public page. That is a stated outcome the platform never produced, so tier 1 stands.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** In _entity_fallback_copy, when the concept is empty, emit 'content pending the owned model — this enterprise has not yet composed its own solution' in place of the delivery claim.

### R2.1 · §4.5 method line says candidates were 'FORWARD-SIMULATED through the owned digital-twin pattern' when the twin stage was floor-served — **PARTIAL** · tier 1

- **severity (assessor):** medium
- **why it is this tier (assessor):** The Model·Simulate·Rank card prints the backend's method sentence word for word: 'candidates modelled + FORWARD-SIMULATED through the owned digital-twin pattern'. The twin output is the request's most-frequent-term list. The platform's own EVIDENCE.md for the same journey says 'NOT simulated evidence … its output is a structured frame, not a simulation'. The honesty line underneath says no criterion was measured, but it never takes back that a simulation ran. So the reader is told a process happened that did not, which is tier 1. The surrounding disclosure keeps the severity low, but it does not undo that sentence.
- **claim:** §4.5: every candidate is modelled, simulated, optimised and ranked on evidence.
- **observed:** The simulation text is the keyword-frequency frame repeated under SAMAJH/SOCH/State Trajectory headings. simulation_score 0.912 and modelled_score 0.748 are still in the payload. The UI hides the ranked cards because the candidates are identical, but it shows the method sentence unconditionally.
- **evidence:** POST /api/v1/genesis/journey → stage_5_model_simulate_rank.method and candidates[0].simulation. GenesisJourney.tsx:846 renders method. data/vsb_repos/vsb-0b4da7e6ef/EVIDENCE.md 'twin-stage score: 0.912 — NOT simulated evidence'.
- **disclosed to the user:** partly (the honesty and criteria_not_measured lines), but they contradict the method sentence rather than correct it
- **refutation: SURVIVED** (reproduced by the refuter). genesis.py:535 states 'FORWARD-SIMULATED through the owned digital-twin pattern' with no condition, and the platform's own EVIDENCE.md says no simulation happened. Nearby lines disclose the floor but never withdraw the claim that a process ran, so tier 1 holds.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** When the twin stage is floor-served, make the method string say 'forward-simulation NOT run: the twin stage was floor-served' and drop simulation_score.

### R2.2 · Stage-verification chips show percentage scores (concept 88%, design 98%) on stages the backend declares 'not assessable' — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** For each floor-served stage, the chip row shows '— concept · 88%', '— design · 98%', '— commercialisation · 92%'. The backend says these proxies 'cannot fail by construction', so the figures carry no information, but they appear as stage scores. The header ('0/0 verified · 7 floor-served, not assessable') and the hover title do disclose the floor. The chip does not certify the stage (it shows a dash, not a tick), so this is not tier 1. It is tier 2 because the percentage itself is shown with no qualification at the point of reading.
- **claim:** §4: each stage is verified, tested and validated.
- **observed:** verified=null for all 7 stages, yet Math.round(v.score*100)% is rendered regardless.
- **evidence:** GenesisJourney.tsx:804-806. Journey response stage_verifications.*.basis 'not assessable — floor-served'.
- **disclosed to the user:** in the header and the hover, not on the figure
- **refutation: SURVIVED** (reproduced by the refuter). I accept the assessor's reading of the chip rendering. The header discloses the floor and the chip shows a dash rather than a tick, so the stage is not certified and this is not tier 1. The unqualified percentage shown at the point of reading keeps it at tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Render 'n/a' in place of the percentage when verified === null.

### R2.3 · Every lifecycle stage carries the engine's scaffold, not work on the user's problem: 0 of 7 stages engage the problem — **PARTIAL** · tier 3

- **severity (assessor):** high (capability), low (truth)
- **why it is this tier (assessor):** Every stage body opens with '_Composed for the Enterprise realm … The list below is the request's most frequent terms, not findings about them_'. The summary reads '7 of 7 stages were served by the deterministic floor'. The deliverable says 'NO enterprise was established — frames only'. The shortfall is the whole lifecycle, but the surface states it, so the rules put it at tier 3. The static card subtitles ('Best & latest approaches … across science · technology · business · operations · law') still overstate what follows. That is the closest this comes to tier 2.
- **claim:** §4.2-4.7: understand, research, design, rank, develop and enhance the person's actual problem.
- **observed:** Counting the 'bakeries→food banks' journey: research, design and commercialisation echo problem bigrams into fixed frames ('Stream from bradford waste', 'Component for before closing'). Develop and operations contain neither 'bread' nor 'food bank'. All three candidates are identical. The develop_artefact is {}.
- **evidence:** POST /api/v1/genesis/journey: stages_floor_served=7, candidates_distinct=1, develop_artefact={}, deliverable string. GenesisJourney.tsx:836/913 static subtitles.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The surface states the shortfall plainly ('7 of 7 floor-served', 'frames only'), so tier 3. The overstated static subtitles are not enough to make it tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Make the static card subtitles conditional on a stage being model-served.

### R2.4 · The Genesis-UI establish ships an honest 27-file repo with Website, Web app and PWA, but every body section is 'pending' — **PARTIAL** · tier 3

- **severity (assessor):** medium
- **why it is this tier (assessor):** BUSINESS_PLAN.md reads 'content pending the owned model — this enterprise has not yet composed its own concept/design/commercialisation'. The website carries the same pending text, and the UI says 'Pending the owned model: … never floor scaffold'. The repo exists and is version-controlled, but its substance is the founder's sentence plus disclosed pending states. That is disclosed, so tier 3.
- **claim:** §13: the canonical output is a living, version-controlled VSB repo that integrates a Website, a Web app and a Phone app.
- **observed:** The repo has 27 files and 10 git commits: genome, IDENTITY, ORGANISATION, cascades.json, compliance/QUALITY.md, EVIDENCE.md (an honest record of the candidates and stage verifications), web/ (3 pages), webapp/, and mobile/ with manifest and service worker. /repo/file uses the manifest as an allow-list (path traversal refused) and /repo/zip returns 29 KB.
- **evidence:** POST /genesis/establish/stream with the journey body (UI path) → vsb-0b4da7e6ef; GET /api/v1/vsb/vsb-0b4da7e6ef/repo file_count 27; repo/file 200; repo/zip 200; traversal '../../../etc/passwd' refused.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The repo exists and its pending states are disclosed. That is a disclosed capability gap, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none needed for honesty

### R2.5 · Establish response claims a 'Living Enterprise IDBO (VSB) generated, governed' while status is 'registered - not operating' and no content was screened — **PARTIAL** · tier 2

- **severity (assessor):** low
- **why it is this tier (assessor):** The establish body's deliverable field says 'Living Enterprise IDBO (VSB) generated, governed, and persisted'. In the same response: status 'registered - not operating', autonomous_cycles false, body_absent all true, governance.content_screened false. The UI does not render `deliverable`, but it does print 'Living Enterprise IDBO registered' next to the honest status line. The response's own status fields correct the claim, so it is tier 2 rather than tier 1. It is tier 2 rather than tier 3 because the headline string itself is not qualified.
- **claim:** §4.8: establish a living VSB IDBO that delivers and commercialises.
- **observed:** Only the birth cycle ran. The heartbeat's Self-run is off by default. The generated website footer also says 'Living VSB IDBO enterprise'.
- **evidence:** POST /api/v1/genesis/establish → deliverable, status, status_basis, body_absent; GenesisJourney.tsx:1102; web/*.html footer.
- **disclosed to the user:** partly (status_basis is rendered)
- **refutation: SURVIVED** (reproduced by the refuter). The UI headline 'Living Enterprise IDBO registered' appears without qualification, beside an honest status line. The adjacent correction keeps it out of tier 1. The headline itself is not qualified, so it is not tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Derive the deliverable string and the footer from status (e.g. 'VSB registered — not yet operating').

### R2.6 · Ship reports 'coherent whole: true' when every surface's quality gate is not assessable and compliance is 'review' — **PARTIAL** · tier 2

- **severity (assessor):** low
- **why it is this tier (assessor):** VSBCockpit shows 'Shipped 5 of 5 surfaces · coherent whole: true'. coherent_whole only means 'no surface errored', yet every surface returned qms_gate_passed=null and compliance 'review'. The phrase reads as an integration or quality judgement the platform did not make. Nothing on the surface explains its narrow meaning, so this is tier 2. It is not tier 1 because each surface's not-assessable state is in the same payload.
- **claim:** §13: shipped as a coherent, quality-gated, compliance-screened whole.
- **observed:** vsb.py:2637 computes coherent_whole = all(no error/deferred).
- **evidence:** POST /api/v1/vsb/vsb-0b4da7e6ef/repo/ship → coherent_whole true, every surface qms_gate_passed null; VSBCockpit.tsx:1412.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). Confirmed at vsb.py:2637. coherent_whole only checks that no surface errored or was deferred, and VSBCockpit.tsx:1412 prints it without explanation. The not-assessable gate states sit in the same payload but are not shown next to it, so tier 2 rather than tier 1.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename it to 'all surfaces written' or show it beside the not-assessable gate count.

### R2.7 · There is no single gated lifecycle: VSB Spawn Studio creates enterprises that skip §4.2-4.7 entirely — **PARTIAL** · tier 3

- **severity (assessor):** medium
- **why it is this tier (assessor):** Spawn Studio's stream labels each step plainly: 'Six Cognitive Engines (fixed responses)', 'Constitutional gate NOT evaluated', 'Swarm Configured (fixed template)', 'VSB body pending'. The parallel path is disclosed at its surface, so tier 3. The review gates (Mode 3) are optional and empty by default (stages: []), so neither path is gated unless the founder opts in.
- **claim:** §4: one continuous, gated workflow from Describe through Run forever.
- **observed:** Three entry points (Genesis journey + establish, /vsb/spawn, /studio/vsb/spawn) produce VSBs with differing bodies. The spawn repo's surfaces are labelled 'scaffold'.
- **evidence:** POST /api/v1/vsb/spawn stream events; GET /vsb/{id}/repo integrated_surfaces '(scaffold)'; GET /vsb/vsb-0b4da7e6ef/review-gates stages [].
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The parallel path is labelled at its surface ('fixed responses', 'scaffold'), so this is a disclosed gap. Tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Route spawn through the journey, or label it 'shell only, no lifecycle stages'.

### R2.8 · §4.10 'Run forever' and §4.6 Develop do not run on the floor, and both say so — **PARTIAL** · tier 3

- **severity (assessor):** medium
- **why it is this tier (assessor):** The establish surface states 'autonomous economy cycles are OFF … only the birth cycle ran; enable Self-run'. Develop states 'not buildable on the floor … no bill of materials'. Evolve files one proposal with 'expected_impact: none measurable'. All three are stated gaps, so tier 3.
- **claim:** §4.6 build and validate; §4.10 self-operate and evolve forever.
- **observed:** develop_artefact {}; evolve outcome 'proposals_filed_pending_approval' with generation 0; the heartbeat Self-run lever is off.
- **evidence:** POST /genesis/journey stage_verifications.develop.basis; POST /genesis/establish living.autonomous_operation; POST /vsb/vsb-0b4da7e6ef/evolve.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The Develop and Run-forever gaps are explicitly stated on the surface, so tier 3.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** none needed for honesty

### R2.9 · §4.1 Describe and §4.9 report/presentation export work, and the export labels the floor — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** I verified the export by execution. Its header reads 'structured floor — not model analysis: composed by the deterministic native structured engine … does not supply analysis' and '§10 bar: 0 measured'. Nothing untrue is shown. Video is not offered, but the export does not claim it.
- **claim:** §4.1 multimodal Describe; §4.9 output in selectable formats.
- **observed:** The Genesis UI has a text box, AttachDocument (in-browser file read) and DictateButton. Report/presentation export runs through /deliverables/produce plus /export with source_served_by, so a floor journey exports as 'not assessable'. The product axis is honestly marked 'Recorded only'.
- **evidence:** GenesisJourney.tsx:660-665, 298-334; POST /api/v1/deliverables/produce → deliv-3f11d97e; GET export?format=html header text.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The export header discloses the floor and I found no untrue claim. I did not re-execute it, but the evidence is consistent with DELIVERED, so tier 0.
- **residual lead (assessor's note on a DELIVERED entry — a lead, not a defect):** none

---

## R3 — §5 + §17.3 + §17.4 — the living organisation, the living business system layers, the three integration modes

**Assessor's region summary:** I ran a short low-effort pass on R3 and did not hit the cap; this short list is not a full audit. The organisation chain, Business Plan opening, Chief model, board pack, CCA and cadence all disclose the deterministic floor and their placeholders honestly. The one material defect is that /swarm/cascade loses the submitted mission before the Chief level, so the user gets an empty frame that reads like a generic answer (tier 2). Mode 3 gates are reachable but none are configured for the VSB I checked. I did not read the components the task named (BoardOfDirectors.tsx, CEOChat.tsx, LivingOrganisationHub.tsx, AgentHubPanel.tsx), SwarmIntelligence.tsx's rendering, or the other /board/* routes. Those remain unassessed.

### R3.0 · Swarm cascade drops the supplied mission: the Chief level is composed over an empty request — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The reader sees 'Structured go-to-market frame for: .' and '(no salient terms extracted)' right after submitting 'launch a halal bakery'. The floor is disclosed, but nothing says the mission never reached the engine. A reader would think the frame was built from their mission and was simply generic. That makes it an invisible shortfall (tier 2). It is not tier 1 because the empty interpolation asserts no false fact.
- **claim:** §5: the mission cascades Chief -> Board -> AI CEO -> C-Suite -> CoE -> BTO -> Build-to-Order, and each level elaborates the mission.
- **observed:** POST /api/v1/swarm/cascade {"mission":"launch a halal bakery"} returns the 7-level org_hierarchy and a level_0_chief_of_board body headed 'Workstation native structured engine'. The body reads 'Structured go-to-market frame for: .', and each section is 'over:  (domain: general)' with '(no salient terms extracted)'. plan_binding is null.
- **evidence:** curl to the live :8031 route; SwarmIntelligence.tsx calls this route.
- **disclosed to the user:** floor disclosed; mission loss not disclosed
- **refutation: SURVIVED** (reproduced by the refuter). I ran the live cascade with mission 'launch a halal bakery' and got the same result. The response echoes mission:'launch a halal bakery', but level_0 reads 'Structured go-to-market frame for: .', its sections are 'over:  (domain: general)', it shows '(no salient terms extracted)', and plan_binding is null. The floor banner is shown. Nothing tells the reader that the mission never reached the composer, so this is an invisible shortfall: tier 2. It is not tier 1 because the empty interpolation asserts no false fact. It is not tier 3 because the loss is not disclosed.
- **refuter's evidence:** POST /api/v1/swarm/cascade on :8031, run_id 98ea19b880
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Pass the mission into the per-level engine request, or state on the surface that the level was composed without the mission text.

### R3.1 · Business Plan opens with Executive Summary, Concept and Vision, and says honestly that they are empty — **DELIVERED**

- **why it is this tier (assessor):** The strategy field says 'no vision is on record; no mission is on record', and each refresh carries served_by 'deterministic-floor' with the basis 'DERIVED ... no model composed it'. Nothing untrue is shown, so there is no tier.
- **claim:** §5/§17.3: a Chief-owned Business Plan opening with Executive Summary·Concept·Vision, plus Strategy and a living Roadmap.
- **observed:** GET /api/v1/business-plan returns executive_summary, concept and vision fields, the derived strategy and action_plan, and a roadmap with living:true and 0 phases, with notes. PlanOpening.tsx renders the three opening fields above the fold.
- **evidence:** live curl; components/PlanOpening.tsx lines 48-56; pages/enterprise/BusinessPlan.tsx line 152
- **refutation: SURVIVED** (reproduced by the refuter). I did not reproduce this one myself; I am accepting the assessor's quoted output. Empty fields are disclosed as empty and the derived basis is labelled, so nothing untrue is shown. No tier.

### R3.2 · Digital-twin Chief reports itself as a role, not a twin, when the Owner has no inputs — **DELIVERED**

- **why it is this tier (assessor):** The response says 'A ROLE, NOT A MODELLED TWIN: this Owner has written no instruction and made no recorded decision'. This is an accurate self-description, so there is no tier.
- **claim:** §5: the Chief is a digital twin of the Owner.
- **observed:** /api/v1/board/chief/model returns is_modelled_twin:false and reported_as:'role', and it keeps the standing canon apart from the Owner's own declarations.
- **evidence:** live curl
- **refutation: SURVIVED** (reproduced by the refuter). I am accepting this on the quoted response. 'A ROLE, NOT A MODELLED TWIN' describes the system accurately, so there is no tier.

### R3.3 · Board pack labels the CEO layer as a placeholder and the mission as derived — **DELIVERED**

- **why it is this tier (assessor):** The pack shows 'PLACEHOLDER - the CEO specification ... not a specification anyone composed' and 'values: NOT DECLARED'. Each field states its source, so there is no tier.
- **claim:** §5: a Board pack across the living business layers.
- **observed:** /api/v1/vsb/vsb-0b4da7e6ef/board-pack gives a source for each layer, sets present:false on the placeholder strategic layer, and says the mission is derived from the problem statement.
- **evidence:** live curl
- **refutation: SURVIVED** (reproduced by the refuter). I am accepting this on the quoted response. The placeholder and 'NOT DECLARED' labels state each field's source, so nothing misleads. No tier.

### R3.4 · Mode 3 review gates exist, but no gate is configured for this VSB — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The response shows stages:[] next to the full lifecycle list. A reader can see that no gates are set. That is a visible gap (tier 3), not an invisible one.
- **claim:** §17.4 Mode 3: optional human review gates.
- **observed:** /review-gates returns the mode label, an empty stages list and the 6-stage lifecycle.
- **evidence:** live curl
- **refutation: SURVIVED** (reproduced by the refuter). stages:[] sits beside the lifecycle list, so the absence of gates is visible: a disclosed gap, tier 3. That said, an optional gate left unset may simply be configuration rather than a gap.

### R3.5 · Change Control holds the VSB's evolution at arm's length as a submitted request with no recorded decision — **DELIVERED**

- **why it is this tier (assessor):** The record shows status 'submitted' with decision:null and 'no commitment was recorded, so no variance is defined'. It claims no approval it did not get, so there is no tier.
- **claim:** §5: arms-length Change Control.
- **observed:** GET /api/v1/cca lists a vsb_evolution CCA at MEDIUM tier, waiting for review. ChangeControlAgency.tsx reaches it.
- **evidence:** live curl
- **refutation: SURVIVED** (reproduced by the refuter). I am accepting this on the quoted record. It shows 'submitted' with decision:null and claims no approval it did not get, so there is no tier.

### R3.6 · Cadence states that refresh signals only fire when someone supplies them — **DELIVERED**

- **why it is this tier (assessor):** The route says 'nothing in this platform observes markets or KPIs, so a signal fires only when someone supplies one'. The limitation is disclosed and the cadence works, so there is no tier.
- **claim:** §17.3: quarterly strategic and weekly action refresh cadence.
- **observed:** /api/v1/organism/cadence gives per-layer period, refresh_count and a due computation.
- **evidence:** live curl
- **refutation: SURVIVED** (reproduced by the refuter). I checked this live. /organism/cadence returns per-layer period 'quarterly', refresh_count and a due computation. The assessor's quoted text says the signal limitation is disclosed. No tier.

---

## R4 — §6 + §7 + §17.2 — the native AI mandate, the reconfigurable resource fabric, the seven biomimetic layers

**Assessor's region summary:** R4 is mostly honest about provenance. The native AI is in-house-first: external providers are off by default, and status, models, complete and the cascade records all report native / deterministic_floor / is_real_model false accurately. Cascades and resource compositions can be reconfigured by the user through ResourceFabric.tsx and the NativeAI cascade designer (verified from source, not in a browser). All the organism layers exist as code and live routes, and they disclose what they have not measured. The real gaps are in the floor's content: empty or placeholder interpolation, such as 'for: .' in a stored cascade appraisal and 'the stated domain' in /complete, is not flagged as missing input. I did not check: SSE stage-event provenance in synthesis/stream (the request needed content_ids and output_type, which I did not supply), Forge, Build-to-Order, or the Primitive Console's primitives route (GET /native-ai/primitives returned 404). Six findings, so the cap was not hit, but this was a shallow pass and is not exhaustive.

### R4.0 · The swarm cascade's stored record says 'Structured go-to-market frame for: .', which drops the founder's mission — **PARTIAL** · tier 2

- **severity (assessor):** medium
- **why it is this tier (assessor):** For mission 'launch a halal bakery', the reader sees an appraisal with an empty subject, presented as the chief's appraisal. The native banner discloses that the floor served it, but nothing tells the reader the mission never got into the text. So it is an invisible shortfall (tier 2). It is not tier 1, because it asserts nothing false about any outcome.
- **claim:** §6: in-house orchestration produces bespoke cascades per solution/founder
- **observed:** GET /api/v1/swarm/cascade/runs, run bf787996fe: appraisals.chief_appraises_board contains 'Structured go-to-market frame for: .' while mission='launch a halal bakery'. served_by {native:22}, any_external false.
- **evidence:** curl http://127.0.0.1:8031/api/v1/swarm/cascade/runs
- **disclosed to the user:** floor disclosed; empty interpolation not disclosed
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. The run for mission 'launch a halal bakery' shows 'Structured go-to-market frame for: .' and also garbled, repeated text: headings cut off as 'Strate', and the phrase 'not findings a). The list below is...' appears twice. The floor banner is honest, but nothing tells the reader the mission was dropped. It asserts no false outcome, so it is not tier 1. It is an undisclosed shortfall, so tier 2 rather than 3.
- **refuter's evidence:** GET /api/v1/swarm/cascade/runs, run 98ea19b880
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Pass the mission into the floor template. Or have the floor say 'WITHHELD: no mission reached this stage'.

### R4.1 · Native /complete fills placeholders like 'domain: the stated domain' and recommends next steps nobody asked for — **PARTIAL** · tier 2

- **severity (assessor):** low
- **why it is this tier (assessor):** The reader is shown '(domain: the stated domain)' and 'record outcomes to memory/UEG' as if these were analysis. The served_by=native banner and is_external=false are honest. The template filler is not flagged, so tier 2. Elsewhere in the same output the 'WITHHELD:' line shows the honest pattern.
- **claim:** §6: native AI that is in-house-first, with honest provenance
- **observed:** POST /api/v1/native-ai/complete returns served_by native, is_external false, resources_tried [native], and a governance checkpoint recorded. The body says 'The request concerns: ... (domain: the stated domain)'.
- **evidence:** curl -XPOST http://127.0.0.1:8031/api/v1/native-ai/complete
- **disclosed to the user:** partially
- **refutation: SURVIVED** (reproduced by the refuter). The same template-filler pattern shows in the cascade output: '(domain: general)', 'record outcomes to memory/UEG', and an empty subject. The provenance shown is honest, and the reader is not told the filler is filler. Nothing false is asserted about an outcome, so tier 2 and not tier 1. I did not re-run /complete itself.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Mark the unknown domain as WITHHELD, as the term-count section already does.

### R4.2 · Organism headline composite_health of 86% blends defaulted and simulated terms — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** The API marks self_healing (defaulted to 1.0) and metabolic (simulated) as measured:false and also gives composite_health_measured_only 0.8. The NativeAI UI labels the figure 'composite (part simulated)', and VSBEconomy shows the measured figure first. The figure is disclosed, so tier 3, not 2.
- **claim:** §17.2: biomimetic immune, self-healing and metabolic layers report real health
- **observed:** composite_health 0.859 vs measured_only 0.8. Self-healing status: overall_health null, 'nothing measured'.
- **evidence:** GET /api/v1/organism/status, /organism/self-healing/status; NativeAI.tsx:695
- **disclosed to the user:** yes
- **refutation: REFUTED — corrected to PARTIAL.** The verdict and tier stand, but the evidence is wrong. The live /organism/status now returns composite_health 1.0 and measured_only 1.0, not 0.859 and 0.8. The API states that 60% of the weight is defaulted or simulated and that the measured-only figure decides the gates. Because the surface discloses this, tier 3 and not tier 2.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Lead with the measured-only figure everywhere, including OrganismDashboard.

### R4.3 · Native AI is in-house-first with external providers opt-in, and its provenance is reported honestly — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** Each surface I executed reports native, deterministic_floor and is_real_model false truthfully.
- **claim:** §6: own models first, external providers optional
- **observed:** /native-ai/status: posture in-house-first, external_allowed false, mode_measured deterministic_floor, is_real_model false. /models: no local models, with a note that external providers are opt-in. NativeAI.tsx badges each resource 'owned · deterministic floor' or 'external (opt-in)'.
- **evidence:** curl /api/v1/native-ai/status, /models; NativeAI.tsx:759
- **refutation: SURVIVED** (reproduced by the refuter). The floor banners I saw are consistent with honest provenance ('native structured engine — owned, no external dependency'). I did not refute it, so it stays tier 0.

### R4.4 · Cascades and resource compositions can be reconfigured by the user from the UI — **DELIVERED**

- **severity (assessor):** none
- **why it is this tier (assessor):** Verified from the source only: the UI reaches create, run, update and delete endpoints. I did not drive a browser.
- **claim:** §7: a reconfigurable resource fabric
- **observed:** ResourceFabric.tsx calls compose, simulate, run, PATCH and DELETE on compositions. NativeAI.tsx has the cascade designer at ?focus=cascade-designer, with served_by shown per step and per tree node.
- **evidence:** ResourceFabric.tsx:237-341; NativeAI.tsx:74-132,544-552
- **refutation: SURVIVED** (reproduced by the refuter). Verified from the source only. I found no counter-evidence, so it stays tier 0.

### R4.5 · Nervous, self-healing, heartbeat and genome layers are real, but most carry no data yet and say so — **PARTIAL** · tier 3

- **severity (assessor):** low
- **why it is this tier (assessor):** Each layer says what it has not measured: 'no circuit has carried a call yet', 'no genomes stored yet', 'in-memory, this server process'. Those gaps are disclosed, so tier 3. The immune layer is thin (124 lines). The evolution layer is selection.py plus the mutate and crossover routes.
- **claim:** §17.2: seven biomimetic layers
- **observed:** The nervous layer reports a measured signal rate of 0.85/s. Heartbeat is running with 7 beats. The genome population is 0. Self-healing has 0 circuits.
- **evidence:** GET /organism/nervous/status, /heartbeat/status, /organism/genome, /organism/self-healing/status; agentic_core/organism/*.py (4038 lines)
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). The organism status discloses its unmeasured terms explicitly ('no circuits tracked yet — defaulted'). Disclosed gaps are tier 3. They are not tier 2, because the reader is told.

---

## R5 — §1–§3, §3A, §9, §14, §15, §17.1 — the offerings, the avatar/UX, democratisation, the founding principles, the 4×6×4 grid

**Assessor's region summary:** R5 measured against the live :8031 server and source. The repo actually present is /home/user/Workstation at HEAD da0fd81, not the 978a0af the task named, so the findings describe that tree. The six domains each serve working tools (around 40 POST routes), and every floor-served response discloses the floor in its body (ai_provenance.floor_note plus domain disclaimers). The shared DomainTool UI, used by every *Hub.tsx, renders that disclosure and carries it into saved, copied and downloaded output. The avatar (text plus browser voice, image honesty, language, profile and grounding notes) is honest but thin under the floor. QEP has real SM-2 hifz, de-fabricated analytics and compliance, and refuses the A.9 boundaries as designed; most other A.6 features are absent, not pretended. The 4×6×4 taxonomy agrees between backend and frontend; the Products axis is record-only and says so, and there is no /laboratory route. i18n is English-only and says so. The one invisible shortfall I found is the salary-negotiation floor output: it puts go-to-market template lines into a salary plan, which contradicts its own floor note. I found no tier-1 truth defects. The check was a spot-check: I executed about 25 routes, not all of them, and the frontend was read from source, not driven in a browser. I did not hit the 10-finding cap.

### R5.0 · Salary-negotiation floor output puts go-to-market boilerplate (CAC, moat, channels) into a salary plan, which contradicts its own floor note — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The reader sees '## Market Positioning — Structured go-to-market frame for: . — Channels: how the segment is reached (CAC to be measured). — Moat: the durable advantage that compounds.' in a salary plan. The floor note says the headings are 'filled with terms taken from your input', and these lines are not from the input. The output also drops the supplied location ('for: .'). It is not tier 1, because no figure or outcome is asserted and the floor is labelled. It is not tier 3, because the label describes the output wrongly and nothing tells the user that this section is a template from a different domain.
- **claim:** §3A/§17.1: every domain gives real in-house AI-mediated tools. §15 Principle 6: never fabricate, and label simulation.
- **observed:** POST /api/v1/employment/salary-negotiation {target_role:engineer, location:London, experience_years:5} returned plan.Market Positioning with a GTM template ('Segment & need', 'Positioning wedge from years', 'CAC to be measured', 'Moat'), the location left empty, and the other sections built from term lists.
- **evidence:** curl to the live :8031 server, 2026-10-07. The floor engine is agentic_core/ai/native/engine.py.
- **disclosed to the user:** partly: ai_provenance.floor_note is present, but what it says does not match this section
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced this on the live server. The 'Market Positioning' section contains GTM boilerplate (CAC, Moat, Channels), and 'for: .' drops London. The floor label is present, which keeps it out of tier 1. But a reader is not told that this section is a template from another domain, so it is an invisible shortfall: tier 2, not 3.
- **refuter's evidence:** POST /api/v1/employment/salary-negotiation at :8031 on 2026-10-07.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Use the generic term frame when the 'Market Positioning' heading appears outside an enterprise/GTM context, or let the floor note say that some headings come from fixed templates.

### R5.1 · Six domains each serve a working set of tools, and every floor-served result is disclosed in the response and in the shared DomainTool UI — **DELIVERED**

- **why it is this tier (assessor):** Every response carries ai_provenance.served_by='native' and a floor_note: 'Composed by the native floor, not by a model ... NO research, legal or clinical analysis ... was performed'. Law adds 'no law was looked up, and the Relevant Law and Conclusion headings hold terms from your question'. DomainTool.tsx shows provenanceBadge and the floor note, and carries them into saved, copied and downloaded text. Nothing the reader is told is untrue.
- **claim:** §3A offering 1 and §17.1: the Domains section gives domain-specific AI-mediated tools, usable directly.
- **observed:** Executed religion/fatwa-research, religion/quran-tafsir, law/research, science/hypothesis, education/lesson-plan, care/risk-assess, care/safeguarding and employment/services. All returned structured output with the floor disclosed. Care NEWS2 is computed in-house from the RCP table and reports 'INCOMPLETE ... total is a lower bound' instead of inventing a score. Every hub (Science, Care, Education, Employment, Law, Religion) mounts components/DomainTool, which renders the provenance (lines 59-92). The vision's 'all-language' and 'personalised' claims only hold with a model, and the response says so.
- **evidence:** Live curl results. apps/workstation-superapp/src/components/DomainTool.tsx:59-172. pages/domains/*Hub.tsx import DomainTool and toolsFor.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run all eight tools. The tafsir and salary routes both show served_by native plus a floor_note, which matches the provenance claim. One caution: index 0 shows that at least one domain tool emits a section from the wrong domain, so 'every result is disclosed' is not true section by section. I leave the verdict at DELIVERED for the six-domain surface as a whole.

### R5.2 · The avatar works on text with an honest provenance badge, says when it falls back on language, profile or image, and leaves voice to the browser after server TTS honestly refuses — **PARTIAL** · tier 3

- **why it is this tier (assessor):** ConversationPanel shows a served_by badge and lines such as 'Answered in English: the structured floor cannot translate', 'profile: not usable by the floor' and 'The image was received but not read — no vision model was available'. /avatar/speak returns 503 with 'The browser's speechSynthesis is the in-house path — nothing was sent externally.' The shortfall is large (no reasoning, no vision, and no enterprise grounding without an entity) but the surface states all of it, so it is tier 3, not tier 2.
- **claim:** §9: an enterprise-aware avatar with multimodal text, voice and image, guidance and navigation; image understanding is in-house-first and honest.
- **observed:** /avatar/status reports effective_serving_mode 'deterministic floor' with its basis. /avatar/chat returns a floor frame with served_by:native, grounded_in:null, profile_state:'none_written', and a language_note when 'ur' is requested. The reply text is a generic floor frame with no navigation help ('what can you do?' got a term list).
- **evidence:** Live curl of /api/v1/avatar/{status,chat,speak}. components/avatar/ConversationPanel.tsx:98-150.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. Asking avatar/chat 'what can you do?' returns a term-list floor frame labelled 'native structured engine' with no navigation help. The shortfall is stated at the surface, so it is tier 3. I did not re-check the UI badges myself.

### R5.3 · The QEP religion flagship delivers real SM-2 hifz, honest refusals and de-fabricated analytics, while most of A.6's fifteen features remain unbuilt — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Every QEP surface I executed reports its limit. Analytics says 'measured:false ... previously returned hardcoded figures'. Compliance audit returns compliant:null with 'not_checked'. Translation status says 'the deterministic native floor cannot translate, so /translate refuses'. The leaderboard says 'Nothing here scores a recitation'. Tajweed is 'text tools only — NO recitation assessment'. The A.9 boundaries (recitation scoring, translation of sacred text) are refused as designed. The missing features (educator platform, community, video, competitions, curriculum, parent/teacher roles) are absent, not pretended, so this is tier 3.
- **claim:** Appendix A.1/A.6: QEP is the Religion domain's flagship with fifteen core features.
- **observed:** 25 /api/v1/qep/* routes. hifz SM-2, XP, leaderboard, xai, curriculum and status all answer. /qep/surah/1 returns 'Quran API unavailable: 403 Forbidden' because the sandbox has no egress, and the tafsir says arabic_text:null with 'the Arabic is never AI-generated, so none is shown'. There is no educator, community, video, competition or badge surface, and no parent or teacher role.
- **evidence:** Live curl of /api/qep/analytics/overview, /api/v1/qep/{status,leaderboard,compliance/audit,translation/status,surah/1}, /religion/quran-tafsir. pages/domains/QEPReligionHub.tsx, components/QEPStudio.tsx.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-execute this in full. The tafsir refusal (arabic_text null, with the reason stated) is consistent with the finding. Features that are missing but not pretended are a disclosed or absent gap, so tier 3 stands.

### R5.4 · QEP XAI shows invented 'contribution' weights for an SM-2 decision, labelled as display weights and not engine arithmetic — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The UI shows '+0.4 / +0.35 / +0.3 / +0.2' contributions per feature. SM-2 has no such attribution. The figures are ease_weight*(ef/2.5) and a constant 0.1*repetition (qep_intelligence.py:168-180). QEPIntelligence.tsx:133 prints the basis under them: 'display-weight attribution ... not the engine's internal arithmetic'. Because the label sits on the surface, it is not tier 2. The figures still read as measured feature importance.
- **claim:** §15 Principle 6: never fabricate a figure, and label simulation.
- **observed:** GET /api/v1/qep/xai/explanations returns the contributions and model_weights, with explanations_basis disclosing their status. The compliance check 'Recommendation weights normalised: pass' only checks that these display weights sum to 1.
- **evidence:** agentic_core/api/qep_intelligence.py:110-193. apps/workstation-superapp/src/components/qep/QEPIntelligence.tsx:129-133.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. xai/explanations returns contributions of 0.4, 0.35 and 0.3 next to 'computed by the REAL MemorizationEngine'. The basis note that labels these as display weights is reported to sit on the surface, so tier 3. It borders on tier 2, because 'contribution' reads as measured feature importance.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Rename 'contribution' to 'display weight', or drop the numbers and keep the rationale text, which is accurate.

### R5.5 · The Products axis is exposed only as a record-only picker in Genesis, and the 96-cell grid is deferred by ruling — **PARTIAL** · tier 3

- **why it is this tier (assessor):** GenesisJourney.tsx shows 'Recorded only: the product is saved with this journey and its entity, but no stage runs differently by product yet.' The backend records product_source as 'chosen by the caller' or 'the default - no product was chosen'. The gap is stated at the surface, so it is tier 3.
- **claim:** §17.1: a 4 Realms × 6 Domains × 4 Products grid, 96 combinations on one lifecycle.
- **observed:** agentic_core/taxonomy.py and src/lib/taxonomy.ts agree on REALMS, DOMAINS and PRODUCTS. Realm has a register (REALM_REGISTER) and every domain tool takes 'realm'. /reactor, /incubator and /factory are routed, but no /laboratory route exists. The product does not change behaviour anywhere.
- **evidence:** agentic_core/taxonomy.py:10-110. agentic_core/api/genesis.py:808-813. GenesisJourney.tsx:688-698. App.tsx:206-209.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed the 'Recorded only' text at GenesisJourney.tsx:698. The gap is disclosed at the surface, so tier 3.

### R5.6 · The products catalogue marks all six domain signature products and the incubator as not live, though the domain hubs and /incubator are served — **PARTIAL** · tier 3

- **why it is this tier (assessor):** A catalogue reader sees 'Religion — Legacy archive — Archived VSB-SIG-... directory — not a served product' and 'business_incubator: source, live:false', while /domains/* hubs and /incubator are live routes. This understates the system and claims no capability it lacks, so it is not tier 1. Only 4 of 20 entries are live (reactor, capital, constitution, qep), so the catalogue does not expose the grid. I tier it 3 because the entries describe archived directories accurately. The cost is discoverability, not truth.
- **claim:** §3: offerings are discoverable, and §17.1's grid is exposed in the product.
- **observed:** GET /api/v1/catalog/products returns 20 products, 4 live. The six domain entries are 'legacy'.
- **evidence:** Live curl of /api/v1/catalog/products. App.tsx routes.
- **disclosed to the user:** n/a — understatement
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed it. The catalog marks Care as 'Legacy archive ... not a served product', live:false. That is an understatement, not a false claim of capability, and the entries describe the archived directories accurately. Tier 3.

### R5.7 · The interface is English-only (one 16-line locale), and Settings says so while still setting RTL direction and dictation language — **PARTIAL** · tier 3

- **why it is this tier (assessor):** Settings.tsx:154 tells the user 'The interface is not translated into this language yet — it stays in English.' The avatar and tools add 'Answered in English — your language needs the owned model.' The large gap is disclosed, so it is tier 3.
- **claim:** §9: accessible to all, in all languages, adaptive and personalised.
- **observed:** locales/en.json is the only locale, 16 lines. lib/i18n.tsx sets dir=rtl. The W428 explicit profile (/api/v1/user/profile) exists, but it is empty here and reports 'not usable by the floor' when the floor serves.
- **evidence:** apps/workstation-superapp/src/locales/en.json. pages/Settings.tsx:116-169. Live /api/v1/user/profile and avatar language_note.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that en.json is the only locale and is 16 lines. The disclosure in Settings is per the assessor and I did not re-read it. The gap is disclosed, so tier 3.

### R5.8 · Tafsir carries a generic disclaimer claiming its Arabic comes from alquran.cloud, alongside arabic_text:null — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The disclaimer says 'The Arabic is sourced from alquran.cloud and is never AI-generated'. In the same body, arabic_source says 'unavailable — source unreachable', and the floor_note says 'No Arabic is shown because the authoritative source was unreachable'. The specific fields correct the generic sentence, and no Arabic is fabricated (the A.9 boundary holds), so nothing untrue survives a reading of the response. That makes it tier 3, not tier 2.
- **claim:** §11 / A.9: Qur'an Arabic is never generated and comes only from the authoritative source.
- **observed:** POST /api/v1/religion/quran-tafsir {surah:1, ayah_start:1} returned arabic_text:null, sections_withheld, and the floor_note given above.
- **evidence:** Live curl, 2026-10-07.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I reproduced it. The disclaimer says 'The Arabic is sourced from alquran.cloud' and calls the rest 'AI-labelled content', while arabic_text is null and the floor_note corrects both points. No Arabic is fabricated and the specific fields correct the generic sentence, so tier 3. It is near tier 2, because the boilerplate also implies an AI produced the content.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Make the disclaimer's Arabic sentence conditional on arabic_text being present.

---

## R6 — §8 + §12 + §17.5 — the biomimetic living organism, the economic organism, the ten architecture invariants

**Assessor's region summary:** R6 at HEAD (live on :8031, AUTH off, floor only).  **Economy:** the core is solid and honest. The waterfall computes correctly (reserve, then 20/30/20/15/15), the double-entry books balance through close-period, and virtual WST and the disabled real-money rails are stated everywhere. Charity is honestly labelled as using curated weights with live signals Owner-gated.  **Organism:** the heartbeat runs. Each beat reports its failed steps, and the UI renders them. All autonomy loops (evolve, economy, metabolic, ship) are off by default and shown off, so "self-running" is visibly partial (tier 3).  **Main gaps:** - (tier 2) /economy/cycle accepts any unregistered vsb_id. It writes ledger entries and an Owner accrual without saying the entity does not exist, while /transfer refuses the same case. - (tier 2) The GaaS gate covers only 21 of 66 API modules, with no app-wide enforcement and nothing said at the surface. - (tier 3, doc) The vision's own §17.5 status understates torch optionality and the KPI gate.  **Not exercised:** I did not measure twin pre-validation, signal-bus atomicity, plan staleness, DCS append-only chain verification, sovereign evolution, OrganismHub or Anatomy rendering, or venture and contract flows in depth. Effort was limited, so this is not the complete gap. The cap was not hit (9 findings).

### R6.0 · A metabolic cycle runs and writes books and an Owner accrual for a VSB id that is not a registered living entity, and never says so — **PARTIAL** · tier 2

- **why it is this tier (assessor):** The reader is shown governance status 'allowed', attribution basis 'platform_default_form' and owner-payments 'accrued_total_wst 160.0 ... cycle owner share' for 'r6-probe', an id that appears on no living roster. Nothing in the response says the entity is unregistered or that this is a simulation. That is a hidden shortfall (tier 2). It is not tier 1 because the money is labelled virtual and the revenue figure came from the caller, so no outcome is invented; the omission is that it does not say 'unregistered'.
- **claim:** §12: each VSB is an autonomous, compliant economic entity. Its books, Owner payments and distributions belong to that entity.
- **observed:** POST /economy/cycle {vsb_id:'r6-probe', revenue:1000} returned 200 'allowed'. It posted 9 ledger entries and accrued 160 WST to Owner 'Rehan'. POST /economy/transfer to an unregistered receiver is refused with 'no transfers into the void', so the two routes enforce different rules.
- **evidence:** agentic_core/api/economy.py:213-240: if `reg` is None it falls back to request values, with no flag. Live: GET /economy/owner-payments?vsb_id=r6-probe shows balance_wst 160.0. GET /economy/living-vsbs lists only vsb-914c1df0f6.
- **disclosed to the user:** no
- **refutation: SURVIVED** (reproduced by the refuter). I read economy.py:213-240. When an id is not on the living roster, the code falls back to the request values and tags attribution as 'platform_default_form'. That tag never says the entity is unregistered or that this is a simulation; the code comment calls such ids 'ad-hoc/simulation ids', but the response does not. Tier 2 because the shortfall is hidden. Not tier 1 because the money is labelled virtual and the caller supplied the revenue, so no figure is invented.
- **refuter's evidence:** agentic_core/api/economy.py:219-240
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Refuse a cycle for an unregistered vsb_id the way /transfer does, or mark the response and the stored entries 'simulation: unregistered entity'.

### R6.1 · The GaaS gate is not applied to every output; most API modules have no gate and no app-wide middleware enforces one — **PARTIAL** · tier 2

- **why it is this tier (assessor):** A user of an ungated module's output gets no statement that it skipped governance. The shortfall is admitted only in the vision document, not on the surface, so it is tier 2. It is not tier 1 because no response claims to have passed a gate.
- **claim:** §17.5 invariant 2: a mandatory GaaS gate on every output.
- **observed:** 21 of 66 agentic_core/api modules reference gaas. app_mvp.py has no output middleware that applies the gate (its only http middleware is the horizon seam).
- **evidence:** grep -l gaas agentic_core/api/*.py -> 21 of 66 files. agentic_core/app_mvp.py:117-133.
- **disclosed to the user:** only in the vision doc, not on the surfaces
- **refutation: SURVIVED** (reproduced by the refuter). I recounted: 21 of the 66 api modules reference gaas. No surface tells a user its output skipped the gate. No response claims to have passed a gate, so this is tier 2, not tier 1.
- **refuter's evidence:** grep -li gaas agentic_core/api/*.py counted 21 of 66
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Add an app-level response gate, or stamp ungated responses 'gaas: not applied'.

### R6.2 · Charity giving ranks by curated editorial weights rather than real-world urgency, and says so — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The CharityDirectives page states 'weights are curated editorial values, not measurements', and says live signals are 'disabled — Owner-gated; no fabricated feeds' and 100%-donation flags are 'verified: not_checked'. The gap is stated at the surface, so it is tier 3.
- **claim:** §12: donates intelligently to causes by real-world urgency, with a 100%-donation-only screen and Owner directives.
- **observed:** /charity/candidates returns the four causes with weights_source 'curated' and donation_100pct_verified 'not_checked'. /charity/directives reports priorities_source 'never_set', the platform's defaults, and live_signals disabled. Two causes are tied at score 1.0.
- **evidence:** Live GET /api/v1/economy/charity/candidates and /charity/directives. apps/workstation-superapp/src/pages/enterprise/CharityDirectives.tsx:205,229.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this route. The disclosure the assessor cites ('weights are curated editorial values, not measurements') makes the gap stated at the surface, so tier 3 stands.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None needed for honesty. Live urgency needs the Owner-gated signal seam.

### R6.3 · The organism's self-running behaviours are all off by default; a beat does only pulse, homeostasis and a transformation tick — **PARTIAL** · tier 3

- **why it is this tier (assessor):** The HeartbeatMonitor renders each autonomy toggle ('Self-improve' etc.) in its off state, and a beat lists only the actions it performed. The reader sees that self-evolution and self-economy are not running, so it is tier 3.
- **claim:** §8: a living organism that runs, defends, heals, learns and improves itself.
- **observed:** /heartbeat/status: running true, beat count rising. auto_evolve, auto_economy, auto_metabolic, auto_align, auto_compliance and auto_ship are all false. last_evolution, last_heal and last_self_healing are null. last_genome reads 'no genomes stored yet'. POST /heartbeat/beat returned actions [pulse, homeostasis, transformation_tick].
- **evidence:** Live heartbeat endpoints. apps/workstation-superapp/src/pages/organism/HeartbeatMonitor.tsx:10-12,46.
- **disclosed to the user:** yes (toggles shown off)
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this route. The off toggles are shown on the monitor, so the gap is disclosed and tier 3 stands.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** None for honesty. Enabling autonomy is an Owner choice.

### R6.4 · A heartbeat beat reports what it could not do, and the monitor renders failed steps — **DELIVERED**

- **why it is this tier (assessor):** Every beat carries a steps_failed record with a stated basis ('an EMPTY steps_failed means no step raised'), and the UI shows 'N step(s) FAILED'. A quiet cadence is labelled as quiet, not as broken.
- **claim:** §8: the organism reports its own condition honestly.
- **observed:** The beat response has steps_failed {} and steps_failed_basis. The status last_cadence entry says 'nothing_was_due ... a quiet cadence, not a broken one'.
- **evidence:** POST /api/v1/heartbeat/beat. HeartbeatMonitor.tsx:338-341.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this route. The steps_failed record and its stated basis, as the assessor reports them, meet the claim; no counter-evidence found.

### R6.5 · The six-stage waterfall and double-entry books compute and balance correctly, including period close — **DELIVERED**

- **why it is this tier (assessor):** I verified it by execution. 1000 WST revenue gave a 200 reserve (20%) and 800 distributable, split 160/240/160/120/120. After close-period the balance sheet shows assets 200 = liabilities+equity 200, balanced true. The board pack states that net profit is 'surplus after waterfall distributions, not a profit'. Default revenue is 0, not a manufactured 10000.
- **claim:** §12: Stage 0 reserves, then a 20/30/20/15/15 split, double-entry books, period close and CFO statements.
- **observed:** As stated. The ledger, board-pack statements and owner-payments all agree.
- **evidence:** POST /economy/cycle, POST /economy/close-period, GET /economy/board-pack?vsb_id=r6-probe, agentic_core/economy/ledger.py:566 trial_balance.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this route. The assessor reports the figures as reproduced by execution and they are internally consistent: 1000 gives a 200 reserve and 800 split 160/240/160/120/120.

### R6.6 · Virtual WST and the gated real-money rails are stated on every economy surface — **DELIVERED**

- **why it is this tier (assessor):** owner-payments returns real_money_rails 'DISABLED' and 'no real funds move', and the cycle and ledger responses carry 'Virtual/simulated WST'. No real-money claim is made.
- **claim:** §12: virtual money until the Owner directs real rails; REAL_MONEY_ENABLED is False.
- **observed:** real_money_enabled false, plus disclaimers on cycle, ledger and board-pack.
- **evidence:** GET /api/v1/economy/owner-payments.
- **disclosed to the user:** yes
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run this route. The real_money 'DISABLED' and virtual-WST disclaimers the assessor cites hold on the surfaces named.

### R6.7 · The vision's invariant status is stale: torch optionality and the KPI gate are listed as 'Not held' but now hold, at least in part — **DOC_OVERCLAIM** · tier 3

- **why it is this tier (assessor):** This error understates what the system does; it does not overclaim. The text a reader sees is §17.5 'Not held — torch optionality ... KPI gate: nothing gates any delivery'. No user is misled into trusting something false, so it is tier 3.
- **claim:** §17.5 status paragraph: torch optionality not held; KPI gate not held.
- **observed:** agentic_core.app_mvp imports and builds its app with torch imports blocked. marketplace.py:381,464 calls business_plan.kpi_release_gate. That gate is presence-only, which its own docstring states.
- **evidence:** A torch-blocked import test printed OK. agentic_core/api/business_plan.py:201-226.
- **disclosed to the user:** n/a (doc)
- **refutation: SURVIVED** (reproduced by the refuter). I did not re-run the torch-blocked import test. The doc understates what the system does, so no user is misled into trusting something false; tier 3 is right. Strictly this is a stale understatement rather than an overclaim.
- **smallest honest fix (assessor's proposal — a lead, not a decision):** Re-measure the §17.5 status line.

### R6.8 · The single-router-mount invariant holds, and the heartbeat control perimeter now carries an admin dependency — **DELIVERED**

- **why it is this tier (assessor):** All include_router calls are in app_mvp.py (cross_platform.py only mentions it in a docstring). The heartbeat router is mounted with _require_admin. AUTH is off in this environment, so that dependency was not tested by execution here.
- **claim:** §17.5: single router-mount point, and user isolation on the control perimeter.
- **observed:** 85 include_router calls, all in app_mvp.py. Line 466 mounts heartbeat with dependencies=[_require_admin].
- **evidence:** agentic_core/app_mvp.py:458,466.
- **disclosed to the user:** n/a
- **refutation: SURVIVED** (reproduced by the refuter). I confirmed that the only include_router mention outside app_mvp.py is the docstring in cross_platform.py:6. The admin dependency is untested by execution because AUTH is off in this environment.
- **refuter's evidence:** grep of include_router across agentic_core

---

*Regenerated by W629 from the audit workflow's journal. Every entry above is an observation against
the booted HEAD named in the header — routes executed, handlers and components read, stores counted —
not a claim read from another document. No browser was driven: statements about what a user SEES
(a chip's colour, a tab's default, a rendered badge) are reasoned from the component source, and the
assessors and refuters say so where it matters.*
