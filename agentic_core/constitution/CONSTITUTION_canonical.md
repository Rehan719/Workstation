# The Workstation Constitution

**Thirty-three articles, each checkable against this platform, each naming how it is verified.**

Authored W515 under the Owner's ruling (FU-266, 2026-09-28) for a new short constitution of the order of
twenty to forty articles. **No numbering is imported from any archived version**, and this starts at 1.

## Why the archived canon is not restored

Measured across the repository: **41 CONSTITUTION documents exist (v52–v139)**; the one live file declared 297
articles and contained 33; and across the 32 parseable documents **9,547 articles are declared while 778 are
present** — 92% asserted by a section header and never written. The document called canonical states that
"Articles 1–695 retained from v126.0 as immutable genomic anchors" and contains none of them. It mandates
capabilities this platform does not have and mostly should not: signed MoUs, global marketplace listings,
scholar onboarding with reputation scores, a monthly revenue floor, cryptographic verifiable credentials,
post-quantum deployment. And two of its articles are self-certifying completion claims — a NO-STUBS MANDATE and
a "100% completion … no stubs or placeholders are permitted".

**A document cannot make code complete by forbidding incompleteness.** That is the single reason none of it is
inherited.

## What an article here must do

Every article is drawn from what genuinely governs this platform — the ratified Owner rulings, ruling A.9.5,
the virtual-WST-only boundary with real-money rails owner-gated, the ten architecture invariants, and the
never-fabricate principle — and every article carries a `Verified:` line naming the mechanism that checks it.
An article that cannot name one is a statement rather than a rule, and the surface says so.

**This document names its own unmet articles.** Four are currently unmet or unbuilt and say so in place
(Articles 8, 11, 13 and 21). A constitution that cannot record its own breaches is a claim, not a governance
instrument, and Article 33 makes that structural.

**Where this document and the platform disagree, the platform is the fact and the difference is the work.** No
article here asserts that something is true because it is written here.

---

## 1 — A PLATFORM MAY ONLY REPORT WHAT IT DID
No surface, record, export or figure may state an outcome the platform did not produce. Where something was not
done, the record says so.
*Verified:* the three-state verdict discipline (`MET` / `UNMET` / `NOT_ASSESSABLE`, each with a basis) across
`agentic_core/api/method.py` and the delivery gate; the truth sweeps in `docs/TRUTH_SWEEP_W477.md`.

## 2 — A FIGURE CARRIES ONLY THE NAME OF WHAT IT MEASURED
A number may not be reported under the name of a quantity it did not measure.
*Verified:* `vbs/quality.py` reports `delivery_coverage` with a `delivery_coverage_basis`, and returns `None`
rather than a length check when no structure was declared (`_delivery_coverage`).

## 3 — A VERDICT HAS THREE STATES, NEVER TWO
Any assessment may return not-assessable with a reason. A binary pass/fail forces a verdict where none was
reached.
*Verified:* `ValidationResult` / `ConsultationResponse` three-state work under P3.12; `assure_delivery` returns
`qms_gate_passed: None` with `qms_basis` when the gate could not run.

## 4 — A SCREEN MAY FLAG AND ESCALATE; IT MAY NEVER CLEAR
A word list, regex or heuristic may raise a concern. The absence of a match is not evidence of safety.
*Verified:* `compliance/ethical_engine.py` — every dimension returns `review` or `not_assessed`, never `pass`,
and `_LEXICON_NOT_A_VERDICT` states the limit in each reason.

## 5 — AN INSTRUMENT THAT CANNOT FAIL IS NOT EVIDENCE
A check is admissible only if its red state is reachable. Green from an instrument that cannot go red reports
nothing.
*Verified:* the blind harness (`scripts/blind_sweep.py`) separates BLIND(red) from VACUOUS and BAD BLIND; every
new guard is driven red before it is trusted.

## 6 — A GUARD DRIVES ITS PRECONDITION AND ITS SUBJECT
A check may not rely on the ambient environment, nor on whichever record a store happens to hold, to create the
condition it tests.
*Verified:* W514 corrected `test_w473`'s FU-070 leg, which chose its subject ambiently and went red against
correct code when that subject became an `OWNER`-slotted row.

## 7 — PROSE IS NEVER THE MEASUREMENT
A check asserts a field, a binding or an AST node. Source text, comments and basis strings are not evidence,
because a comment naming a forbidden thing satisfies a search for it.
*Verified:* the AST-based legs throughout `integration_tests/test_mvp_spine.py`; `scripts/selfcheck_diff.py`
detects an assertion that matches its own text.

## 8 — A COUNT IS COMPUTED, NOT ASSERTED
A quantity stated in a sentence must be derived from the state it describes.
*Verified:* open — `api/method.py:719` states "eleven of seventy were defended" as prose beside a computed
`f"{len(wanted)} of {len(classes)}"` nine lines above (FU-305). This article is currently **UNMET** and names its
own breach.
*Status:* MET as of W515 — the figure is now read live from the ledger, and the answer refuses rather than substituting when the ledger cannot be parsed

## 9 — PROVENANCE TRAVELS WITH THE OUTPUT
Whatever produced a result is recorded where a reader meets the result — in the file, the export, the download
and the card, not only in the DOM.
*Verified:* `served_by` / `is_external` threaded through the gateway writers; provenance headers on exports
(`provenanceHeader`, `provHeader`).

## 10 — AN ABSENCE IS RECORDED AS AN ABSENCE, AND "NOBODY" IS NOT "NOT RECORDED"
A missing value is stored as a stated absence with a reason, never omitted and never defaulted.
*Verified:* `/bto/configure` distinguishes a deterministic absence of provenance from an unrecorded one;
FU-276's 39 owner-less call sites are to record `owner_id=None` **with a reason**.

## 11 — A STORE THAT COULD NOT BE READ WHOLE SAYS SO WHERE ITS NUMBERS ARE READ
Tolerant reading keeps a surface up; it may not present a partial count as a complete one.
*Verified:* `config.read_json_reported(path, default) -> (value, reason)`; `economy/revenue.py` surfaces
`counts_are_incomplete`. Thirteen callers remain (FU-075 / FU-298) and this article is **partially UNMET**.
*Status:* UNMET — thirteen tolerant readers still do not surface an incomplete store (FU-075 / FU-298)

## 12 — A SHARED STORE IS WRITTEN UNDER A LOCK, ATOMICALLY
*Verified:* `store_lock` + `atomic_write_json` at every shared-store writer.

## 13 — AN EVICTION IS DISCLOSED WHERE THE COUNT IS READ
A capped store that has discarded rows may not present its contents as the whole population.
*Verified:* `economy.py:1089` records the fix for `rows[-500:]`. `deliverables.py:72` (`rows[-300:]`) and
`resource_fabric.py:1485` (`rows[-200:]`) still do not say so — measured W514, both sitting exactly on their cap.
**UNMET**, and it is why FU-302's population is unrecoverable.
*Status:* UNMET — two capped stores do not disclose that their oldest rows are gone (registered W515)

## 14 — ALL MONEY IN THIS PLATFORM IS VIRTUAL WST
No real value moves. The economic model, waterfall, ledger and payments are simulated.
*Verified:* `REAL_MONEY_ENABLED` defaults off and gates the rails; the binding virtual-only disclaimer on the
Board Pack; `docs/VSB_ECONOMIC_LEGAL_MODEL.md`.

## 15 — THE REAL-MONEY RAILS, A LIVE AI KEY, MANAGED POSTGRES AND PRODUCTION DEPLOY ARE OWNER-GATED
No round may enable any of them, and no agent may flip `AUTH_ENABLED`, `SELF_SERVE_SIGNUP`, `AI_ALLOW_EXTERNAL`
or `REAL_MONEY_ENABLED` in configuration.
*Verified:* config defaults plus the standing prohibition in `docs/FABLE_DELIVERY_PROMPT.md`; the Owner rulings
are constitution, not preference.

## 16 — THE OWNER ADJUSTS THE WATERFALL; THE PLATFORM DOES NOT
Distribution proportions are the Owner's, bounded by the entity template, and every change is logged.
*Verified:* `GET`/`POST /api/v1/economy/waterfall`, template-bounded, UEG-logged.

## 17 — NO AI VERDICT IS PASSED ON A PERSON'S SPIRITUAL STATE (RULING A.9.5)
The Fitrah Spectrum is never a measurement. No virtue, gratitude, barakah or spiritual-outcome field is computed
about a person. An Owner-typed reflection is the Owner's own words and is not an inference.
*Verified:* asserted on the binding across `agentic_core` and the Horizon surfaces — not on a word list, since a
comment naming a forbidden field would satisfy a search.

## 18 — QURAN ARABIC IS NEVER GENERATED
Quranic text comes only from quran.com, alquran.cloud or tanzil.net, with provenance.
*Verified:* the source allow-list; no generation path emits scripture; scripture is never typed into a test.

## 19 — RECITATION IS NEVER SCORED
*Verified:* no scoring path exists over recitation audio.

## 20 — AI-PRODUCED CONTENT IS LABELLED AS SUCH
*Verified:* the AI-content labelling on generated surfaces; `served_by` naming the producer.

## 21 — A RELIGIOUS RULING IS REFERRED TO A QUALIFIED HUMAN SCHOLAR
The platform does not issue one, and does not claim scientific proof over a theological truth.
*Verified:* the P2.12 guardrails, attached to the `gaas.v5` interceptor. Currently **NOT BUILT** — Horizon is
spec-only (`docs/HORIZON_INTEGRATION.md`); this article states the standing rule and its own absence.
*Status:* UNMET — the Horizon guardrails are specification only; no code implements them

## 22 — ON A DISTRESS SIGNAL THE PLATFORM WITHHOLDS AI COUNSEL AND NAMES A HUMAN ROUTE
It says plainly that it is not a person. Where the route list is unsupplied it renders NOT SUPPLIED — never a
default, never a placeholder, never a plausible-looking number a person in distress might dial.
*Verified:* Owner ruling FU-270 (2026-09-28). The refusal ships; the list is supplied later with its reviewer.

## 23 — CROSS-REQUEST RECALL IS OFF BY DEFAULT AND EXPLICIT AT EVERY CALL SITE
One request's content is never prepended to another's and presented as analysis of its subject.
*Verified:* `augment=False` explicit at all 57 gateway call sites (W511); a row written from an augmented prompt
is marked at all four writers (W507).

## 24 — ATTRIBUTION IS NOT RECALL
An account identifier records who produced something. It is never used to retrieve another request's content.
*Verified:* the FU-276 split keeps `owner_id` for attribution only; conflating the two caused W489's
twenty-nine-caller defect.

## 25 — NO EGRESS THE OWNER DID NOT ASK FOR
Indexed content is local data, never committed and never sent anywhere. Only what the Owner copies into a named
inbox is read; the four desktop archives are not.
*Verified:* Owner rulings FU-167 (no egress) and FU-268 (an explicit inbox only). One archive holds a `.env`, and
a narrower true claim beats a wider one resting on a skip list.

## 26 — HALAL IS ASSESSED BY CERTIFICATE VERIFICATION; THE BODY CLEARS, NEVER THE PLATFORM
*Verified:* Owner ruling FU-239 (2026-09-29).

## 27 — WHAT MAY CHANGE IS DECIDED AT ARM'S LENGTH
A material change is proposed, reviewed and ratified through the Change Control Agency, and the decision is
logged in the universal evidence ledger. A proposer does not approve its own proposal.
*Verified:* `/api/v1/cca`; CCA decisions → UEG (FU-013); `economy_material` CRITICAL and `code_change` HIGH
(FU-014); the Board ratifies review-approved HIGH changes (FU-012).

## 28 — THE ORGANISM MAY NOT APPLY A GUARDRAIL, A GATE, A SCHEMA, MONEY, FAITH CONTENT OR A LAW DOMAIN TO ITSELF
Self-improvement is proposed and submitted, never self-applied, above the lowest risk tiers.
*Verified:* the Sovereign Evolution Office routes to Change Control; `change_control_handoff` records
`requested` / `directives_considered` / `met_the_rule` / `submitted`, with the rule verbatim — "AN EMPTY LIST IS
NOT AN ANSWER".

## 29 — A DECLARED CAPABILITY THAT NOTHING REACHES IS RECORDED AS UNREACHED
A layer, engine or resource that exists in code but is never called says so rather than counting as working.
*Verified:* `vbs/quality.py`'s `LAYER_STATE` table (`code_exists_unreached`, `implemented_not_on_this_path`,
`measurement_under_this_name`) and the `layers_note` rendered to the viewer via `layerTitle()`.

## 30 — A DEFECT FOUND AND NOT FIXED IS REGISTERED IN THE SAME COMMIT
*Verified:* `docs/FOLLOWUPS.json` via `scripts/followups.py`, slotted to a plan item; `plan_followups.check`
refuses drift between an item's text and the rows riding it.

## 31 — AN ITEM CLOSES ON ITS STATED ACCEPTANCE CRITERIA, NOT ON ACTIVITY
Zero rows against an item means unexamined, not nearly done.
*Verified:* every open build item in `docs/FABLE_DELIVERY_PROMPT.md` states an ACCEPT clause — measured W514, the
only exception being `P3.0`, which holds an Owner ruling and has no build bar.

## 32 — A REPEATED BREACH OF THIS METHOD ESCALATES TO CHANGE CONTROL AUTOMATICALLY
*Verified:* `POST /api/v1/method/breach`; `ESCALATE_AT = 3` in `api/method.py`; it has fired three times on this
project's own repeated mistakes.

## 33 — THIS DOCUMENT NAMES ITS OWN UNMET ARTICLES
A constitution that cannot record its own breaches is a claim, not a governance instrument. Articles 8, 11, 13
and 21 are currently unmet or unbuilt and say so above.
*Verified:* a guard asserts that at least one article carries an explicit UNMET state, so the document cannot
quietly become self-congratulatory; and the endpoint's `canon_present: False` branch remains reachable.

---

## Not included, deliberately

Signed MoUs · global marketplace listings · ORCID onboarding with reputation scores · ≥50,000 WST monthly
revenue · cryptographic Verifiable Credentials · post-quantum deployment · any "100% complete / no stubs"
mandate. Each appears in the archived canon; none is a capability of this platform, and a constitution may not
mandate one into existence.

**FU-295's one outstanding measurement gap is now closed, and the row's own note is out of date.** It records
that `products/OctoVeritasEngine/constitution` *"refused read with a permission error"*. Measured W514: the path
reads fine — it is a **Python package, not a document**. It holds `articles_parser.py` (40 lines),
`compliance_checker.py` (52) and `constitutional_audit.py` (22), **114 lines in total and no article corpus at
all**. So there is nothing there to examine, inherit or exclude, and the gap closes as an absence rather than as
a refusal. Update the row when this lands; a stale "never examined" note invites the same search again.
