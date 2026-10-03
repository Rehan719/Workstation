# HORIZON — the conscious membrane, integrated into Workstation IDBO

**Status:** design accepted for build as plan items **P2.11 – P2.16**. Nothing in this document describes
running code unless the row says MEASURED. Every "what exists" claim below was measured against this
working tree on **2026-09-27 (round W495)** by the command named beside it; nothing is inferred from a
module's name.

**Source.** The Owner supplied an architect's Phase 0–5 brief for a subsystem called **Horizon**: an MDL
(Minimum Description Length) compression membrane in front of the existing plan/execute/verify loop, a
local-archive "asset genome", a self-correction daemon ("systemic Muhasabah"), a relational companion
surface, and epistemic/theological guardrails. The instruction was to *interrogate and review to adjust
accordingly, and build on it*. This document is that interrogation. It states what is adopted, what is
rejected and why, what the Owner must decide before parts of it can be built, and the plan items the
adopted parts become.

The brief is a good design carried on two bad habits. The design — compress intent before acting, record
what a run consumed, route correction through an arms-length office — is sound and fills real gaps. The
habits are (1) presenting a *simulated* audit as an audit, and (2) writing functions that return
hard-coded verdicts a real implementation would have to compute. Both are the exact defect class rounds
W477–W495 removed from 132 surfaces of this platform. Adopting the design means building it under the
rule those rounds established:

> **A platform may only report what it did.** A score, rank, verdict, transcript or spiritual state that
> nothing produced is ABSENT and says why. There is no third habit where "for now" it returns a constant.

---

## 1 · The audit, measured

The brief's audit table lists five subsystems as "Exists". Measured, the picture is more specific, and
two of its five rows are wrong in ways that change the design.

| Brief's claim | Measured on 2026-09-27 | Verdict |
| :-- | :-- | :-- |
| "Core Orchestrator exists (VSB AI CEO logic, basic routing)" | `agentic_core/ai/native/orchestrator.py` and `agentic_core/ai/gateway.py` exist; 459 route decorators across `agentic_core` | **CONFIRMED** |
| "PEV loop exists (standard agentic workflow loops)" | There is no single module named for plan/execute/verify. The loop is **distributed**: `agentic_core/projects/api.py` (concept→prototype→commercialise with governance proposals), `agentic_core/api/transformation_orchestration.py`, `agentic_core/api/operational_excellence.py` (run outcomes), `agentic_core/vbs/quality.py` (the QMS gate) | **PARTLY** — Horizon cannot "wrap the PEV loop"; there is no one seam. It must attach at the four named seams, or at one new seam built for it. |
| "QEP exists (Hifz, Tafsir, Hadith modules)" | `agentic_core/api/religion.py` exists with 6 routes. There is no `quran.py`, no hifz module, no tafsir module. The Quran Education Platform is a **vision document** (`docs/QURAN_EDUCATION_PLATFORM_VISION.md`), not a built product | **WRONG** — Horizon must not plan against QEP modules that do not exist. |
| "Legal/Employment exists (UK law, tribunal logic, ACAS codes)" | `agentic_core/api/law.py` and `agentic_core/api/career.py` exist | **CONFIRMED** (scope not audited here) |
| "Archives exist (scattered docs, markdown)" | `docs/` holds the canon; `_archive/` holds what the cleanups moved (see `scripts/recovery_audit.py`) | **CONFIRMED** |

What the brief did not list, and Horizon must reuse rather than duplicate:

| Exists (measured) | Path | Why Horizon must not rebuild it |
| :-- | :-- | :-- |
| Constitutional interceptor (gaas.v5) | `agentic_core/gaas/v5/__init__.py` | Already the runtime intent gate. Horizon's guardrails extend it; they do not replace it. |
| Change Control Agency | `agentic_core/api/change_control.py` | Already the arms-length office with risk classes and an audit chain. Horizon's risk tiers MAP onto it. |
| Organism context / biobus | `agentic_core/organism/biobus.py` | Already the measured-health and mode source, with a three-state discipline (W494). |
| Run-outcome ledger | `agentic_core/api/operational_excellence.py` | Already records every run with a three-state quality verdict (W495, FU-125). |
| Follow-up register + tooling | `docs/FOLLOWUPS.json`, `scripts/followups.py` | Already the lessons-and-work register with priority, pace and batch mechanisms. |
| Ingestion with three-state extraction | `agentic_core/ingestion/api.py` | Already answers EXTRACTED / NOT_EXTRACTED / NOT_TRANSCRIBED with a basis, and only puts read text in the knowledge base (W495, FU-124). |
| The delivery-method item | plan item **P2.10** | Already the register + derivation + arms-length gate for *how we build*. Horizon's Muhasabah is the same mechanism for *how the organism runs*. **One register, one gate.** |

---

## 2 · The four local paths, measured

The brief registers four desktop folders as "external sensory organs" and assigns each an asset type.
Measured (`os.walk`, excluding `node_modules .git dist build __pycache__ .next venv .venv`):

| Path | Brief's label | Measured content | Readable by this platform **today** |
| :-- | :-- | :-- | :-- |
| `…\Desktop\Book n Guidance App` | SPIRITUAL_ONTOLOGY | 14 files: 9 `.docx`, 5 `.pdf` (drafts of one book) | **NONE.** No pdf or docx extractor is installed; `_pdf_docx_extractor` probes for one and reports NOT_EXTRACTED. |
| `…\Desktop\github_repos` | EXECUTION_TOOLS | 48,230 files raw; 4,089 after exclusions — 1,815 `.ts`, 992 `.tsx`, 256 `.md`, 150 `.txt`, 77 `.py`. Contains `Quran-recitation-mvp/` and `Quran-recitation-platform/` | **Most of it** (text formats). |
| `…\Desktop\openQuran` | PRIMARY_SOURCE_TRUTH · Quranic ontology, ayat/hadith linkages | **One** file after exclusions, and it is `mvp/frontend-vite/.env` | **NOTHING of the claimed kind.** The claim is false today; the one file is a **credentials file**. |
| `…\Desktop\p3` | COMMERCIAL_AND_ARCHIVE | 9 files: 5 `.txt`, 4 `.docx` | **The 5 `.txt`.** |

Four consequences, none of which the brief's ingestor would have surfaced:

1. **Its ingestor would have reported success over nothing.** It filters to `.md .txt .py .json`, so it
   matches **zero** files in the book folder — and still returns `{"status": "ASSIMILATED"}` per organ,
   with a `print()` where the vector write should be. That is the FU-124 defect (a file the platform never
   read counted as knowledge) and the FU-127 defect (a status nothing earned) in one function.
2. **An indexer over `openQuran` would ingest a secrets file.** Any Horizon ingestor must exclude
   `.env`, `.pem`, `*_key*`, `*secret*`, `credentials*`, `id_rsa*` **by rule**, and must record what it
   excluded and why — an exclusion nobody can see is indistinguishable from a file that was not there.
3. **The "primary source truth" organ is empty**, so the Quran-source rule is unaffected but the design
   premise is not: Horizon gets no Quranic ontology from the local paths. Quranic text continues to come
   only from `quran.com`, `alquran.cloud` or `tanzil.net` with recorded provenance, per canon.
4. **48,230 raw files is a real cost.** The scan is explicitly bounded (exclusion list, size cap, file
   cap) and the manifest states the bound. A silent cap reads as "covered everything".

---

## 3 · Adopted, adjusted, rejected

### 3.1 Adopted as-is (the design's real contribution)

| Idea | Why it is worth building here |
| :-- | :-- |
| **Compress before acting.** A raw situation becomes a small explicit record: what is being asked, in which domain, what is at stake, what is missing. | Today a prompt goes from the page to an engine unexamined. Every truth defect this platform had began as an unexamined request producing an over-claimed answer. |
| **Route from the compressed record**, not from the raw prose. | Makes routing inspectable and testable; the record is the thing a guard can assert on. |
| **Account for what a run consumed** (time, calls, whose data). | `operational_excellence` records outcomes; nothing records *cost of attention* — the Owner's "favours utilised" reframed as measurable consumption. |
| **Return: friction becomes a recorded lesson, and a lesson reaches an arms-length office.** | This is P2.10's mechanism at runtime scope. Same register, same gate. |
| **Guardrails: no ruling, no proof-claim, no clinical care.** | Extends the canon's existing refusals (no AI Ask-a-Scholar, no generated Arabic, no recitation scoring). |
| **Bounded, explicit self-modification.** Low-risk auto-applied and logged; anything structural goes to Change Control. | Exactly the CCA's existing contract. |

### 3.2 Adopted with adjustment

| Brief | Adjustment, and why |
| :-- | :-- |
| `compress_noise_to_meaning()` returns a hard-coded `IntentEnvelope` with a written-out `compressed_meaning`, marked "Simulated MDL Output for demonstration". | **A compressor with no compressor returns `NOT_COMPRESSED`** with the reason (`no model served this` / `the floor served this and does not compress`), and the router then handles the raw request with the request-level guardrails still applied. It never invents the user's meaning. On this platform the deterministic floor serves most calls, so the un-compressed path is the COMMON path, not an edge case. |
| `AlignmentEvaluator.evaluate_fitness()`: `divine_alignment = 1.0 if envelope.compressed_meaning else 0.0`, then a weighted sum with invented weights. | **Deleted as written.** A non-empty string is not alignment; a verdict that cannot come out otherwise is not an assessment (W494, FU-102). What replaces it: each term is either MEASURED (from a fact — a guardrail fired, a source was cited, a required field is missing) or NOT ASSESSABLE, and the overall answer is **PROCEED / ESCALATE / NOT ASSESSABLE** with the terms shown. No single number stands in for "divine alignment" — see §4. |
| `spiritual_station: SpiritualStation` assigned to the user's situation by the compressor. | **Refused as an AI verdict** under ratified ruling **A.9.5** (the Fitrah Spectrum is never a measurement; AI must not claim to measure the soul). A station may be **chosen by the user** for their own record, or shown as a *reflection prompt* the user may accept or dismiss — never asserted, never scored, never persisted as a fact about the person. |
| `virtue_forged` written into the ledger by the system. | Same ruling. The ledger records **what the platform did** (what it consumed, what it produced) and **what the Owner declared**. A virtue is only ever an Owner-entered field. An empty field stays empty; it is never filled by inference. |
| Local ingestor returning `ASSIMILATED`. | Replaced by the three states this platform already uses: `INDEXED` / `NOT_READ (no extractor for <ext>)` / `EXCLUDED (<rule>)`, each with a basis, plus the scan's own bounds. A file the platform never read is not in its knowledge base. |
| `MuhasabahDaemon.capture_friction()` with `root_cause = "…" # Simulated LLM analysis`. | A lesson record carries **observed evidence** (what failed, what was asked, what the response was) and a **candidate** cause with its basis, or `cause: not determined`. A candidate is not a finding, and a finding is not an approved change. |
| Risk tiers 0–5 with their own approval logic. | Mapped onto the existing `change_control` classes rather than a second governance. Tier→class mapping and the auto-apply boundary are §6. |
| Prisma models / SQL DDL. | **There is no Prisma and no SQL database in this repo.** State lives in JSON stores under `data/` with `store_lock` + `atomic_write_json` (three real data-loss bugs came from ignoring that — see the shared-store class). The three tables become three stores with that discipline and a documented schema. |
| ChromaDB / Pinecone vector store. | No embedding backend is installed, and external calls are Owner-gated (`AI_ALLOW_EXTERNAL`). The asset genome ships with a **lexical index the platform owns**, and reports `embeddings: none installed` rather than implying semantic recall it does not have. |
| A React companion panel rendering the envelope. | Kept, with the same rule as every other surface: it prints the record's own three states, including "this was not compressed" and "no station was assigned". |

### 3.3 Rejected

| Rejected | Reason |
| :-- | :-- |
| "Simulated Audit based on provided context" presented as `HORIZON_REPO_AUDIT.md`. | An audit of a repository that was not read is not an audit. §1 and §2 above replace it with measured rows. |
| `HORIZON_DOC_TRACEABILITY_MATRIX.csv` rows asserting status ("Exists", "Partial") and metrics ("Alignment score > 0.85", "Asset reuse rate > 40%", "User shame-spiral reduction"). | The statuses were guesses, and three of the five metrics are unmeasurable here: there is no instrument for an alignment score, no reuse instrument, and **no instrument for a psychological outcome** — proposing one would be emotion inference, refused by canon. Traceability lives in `docs/FOLLOWUPS.json` + the P2.10 method register, which already carry `enforced_by` and a basis per row. |
| "The Organism is Now Alive", "Forward circulation is active", "The membrane is secure". | Claims about code that has not been written. This is the class the last twenty rounds removed. |
| `npx prisma migrate dev`, `python …/local_ingestor.py` as deployment steps. | Neither runs in this repo. |
| `SpiritualStation` with `# ... (Mapped to all 25 stations)`. | An ellipsis is not a mapping. The 25 stations and the 0–9 node blueprint are **not in the canon** (see §7 — Owner decision). Until ratified, Horizon carries `domain` and `stakes` and no station taxonomy. |
| Regex `FATWA_PATTERNS` as the theological guardrail. | Kept only as one **trigger**, never as the guarantee: it screens an English request for ruling-seeking phrasing and misses every other phrasing and language. The guardrail's own statement of coverage is part of the deliverable (see §5), and the escalation defaults ON when the screen cannot decide. |
| `EpistemicFilter` returning a crisis message as the whole response. | Kept in substance — a distress signal must reach a human, and the platform must not pretend to care for someone — but it is not a regex on two English phrases, it is not presented as clinical judgement, and its limits are stated. §5. |

---

## 4 · The loop, mapped onto what exists

Horizon's five steps, each named with the seam it attaches to and the state it must be able to report.

**1 OBSERVE.** A request, a run failure, or an Owner note enters as a `HorizonObservation`:
source, raw text, the surface it came from, timestamp. Nothing is interpreted here.
*Seam:* a middleware in front of the domain routes + a hook on the run paths that already call
`operational_excellence.record_outcome`.

**2 COMPRESS.** Produce an `IntentRecord`: `asked_for`, `domain`, `stakes`, `missing`,
`escalations` (a list, e.g. *a ruling was sought*, *a legal filing is implied*), and
`compression` = `COMPRESSED` (a model served it, named) | `NOT_COMPRESSED` (with the reason).
**Never a sentence the platform wrote about what the user "really" means when nothing compressed it.**
Plus `reflection_tag` — **ADDED W549 (FU-336), from the Owner's ruling recorded as FU-267 and
closed in W505, which this section never learned about.** An OPTIONAL tag the **user** selects
and can clear, stored as **the user's own words**. It is the sharpest case of the rule in the line
above: a compression the platform wrote is forbidden, and this field is the one place the user's
own account of their intent is kept — so **no AI ever writes it**, there is no default, no
suggestion is persisted as a value, and nothing infers it from the observation's text. It needs a
**WRITE route** (the user selects and clears it), which every sizing of P2.11 missed because this
section only ever implied a read.

**3 DECIDE.** `PROCEED` | `ESCALATE` | `NOT ASSESSABLE`, from stated terms:
a guardrail escalation present → `ESCALATE`; a required field missing → `ESCALATE`;
`NOT_COMPRESSED` and a domain on the escalation list → `ESCALATE` (**fail closed**);
otherwise `PROCEED`. Each term is shown with its basis. There is no blended score, because three of
the four terms the brief wanted to blend have no instrument.

**4 ACT.** Route to the existing engine for the domain. Horizon adds nothing to the answer.
*Seam:* the same handlers as today; Horizon passes the `IntentRecord` id so the outcome can be joined.

**5 ACCOUNT.** A `ConsumptionRecord` joined to the run: wall time, calls made and what served each
(the provenance map that already exists), which stores were read, and whose data. Plus the
Owner-declared fields, empty until the Owner fills them.

**6 RETURN.** On friction — a raised handler, a refused gate, an Owner correction — write a
`LessonRecord` into **the same register P2.10 defines** (`docs/DELIVERY_METHOD.json` for method lessons;
a runtime store for runtime lessons, with one shared shape), carrying evidence, a candidate cause with
its basis or `not determined`, and a proposed change. Low-risk proposals are applied and logged;
anything else is submitted to `change_control`. **Horizon never approves its own structural change.**

Circulation, in the Owner's terms, with the honest edge: forward is OBSERVE→ACT, reverse is
ACCOUNT→RETURN→a governed change. The "countercurrent exchange" — extracting reusable meaning at the
crossing — is the asset genome (§2, P2.13). It is the part most likely to over-claim, so it reports
`reuse: not measured` until something measures reuse.

---

## 5 · Guardrails, with their coverage stated

Three gates, each attached to the existing gaas.v5 interceptor rather than beside it. Each returns a
verdict **and the statement of what it did not look at** — the W494 rule that a screen may refuse but
never clear.

1. **No ruling.** If the request seeks a religious ruling, the answer carries context and an explicit
   referral to a qualified human scholar, and the platform issues no ruling. *Coverage:* a phrase screen
   over the request, English, extensible. *Stated limit:* it does not screen the answer for correctness
   and does not detect every phrasing; it may only ESCALATE, never certify that no ruling was sought.
   Consistent with canon's refusal of an AI Ask-a-Scholar, and with A.9.5.
2. **No proof-claim.** The platform does not assert that a scientific result establishes a theological
   truth. Where such a claim appears in generated text it is reframed as reflection, and the reframing
   is recorded. *Stated limit:* pattern-based; absence of a flag is not a certificate.
3. **No clinical care, and a human is named.** On a distress signal the response withholds AI counsel,
   states plainly that the platform is not a person and cannot help with this, and surfaces the
   appropriate human route. *Requirements:* the routes must be real and current (an out-of-date helpline
   is worse than none), so the list is data with a reviewed-on date, and the surface says when it was
   last reviewed. *Stated limit:* a phrase screen catches some signals and misses others; it is never
   presented as detection, and never as assessment.

Plus the existing canon rules, unchanged and unrelaxed by Horizon: Quran Arabic is never generated;
Quranic text comes only from the three named sources with provenance; recitation is never scored; AI
content is labelled; the Fitrah Spectrum is never a measurement.

---

## 6 · Storage and governance, in this repo's idiom

Three stores under `data/horizon/`, each a JSON document written through `store_lock` +
`atomic_write_json`, each row carrying its basis:

- `intent.json` — `IntentRecord` + `HorizonObservation` (ids, domain, stakes, compression state, decision, terms).
- `lessons.json` — `LessonRecord` (evidence, candidate cause + basis, proposed change, risk tier, state).
- **`reflection_tag` — ADDED W549 (FU-336), from the Owner's ruling recorded as FU-267 and closed in W505, which this spec never learned about.** An OPTIONAL tag the **user** selects and can clear, stored as **the user's own words**. It changes the work in two ways a sizing from this section would have missed: it needs a **WRITE route** (every sizing of P2.11 had budgeted a read route only), and it is the sharpest instance of that item's *no field is filled by inference* rule — its guard must prove **no AI ever writes it**, which means no default, no suggestion persisted as a value, and no inference from the lesson's own text. A ruling recorded in the register and absent from the spec is a ruling a round silently omits, which is why it is written here rather than only in the item body.
- `genome.json` — the asset index (path, organ, type, `INDEXED|NOT_READ|EXCLUDED` + basis, size, indexed-at)
  with the scan's bounds recorded beside it.

Risk tiers map onto `change_control`, they do not replace it.

**CORRECTED W549 (FU-335), and the correction is about two scales rather than one.** This section used to
route tier 2 to `config_minor` and leave tiers 3–5 with no `change_type` at all. Measured:
`agentic_core/api/change_control.py` has **no 0–5 scale** to map onto. `_TIER_MAP` carries 16
`change_type` STRINGS and the Agency derives its own **four** ranks from them — LOW / MEDIUM / HIGH /
CRITICAL. So the mapping is tier → `change_type`, and the Agency's rank follows from the type. A round
reading the old table would have had to invent the type for tiers 3–5, and that invented choice decides
whether the Board ever sees the lesson.

**WHY THAT MATTERED:** `awaiting_board_ratification()` is reached only by a change that is `approved`,
ranks **HIGH or above**, and was approved by a REVIEW rather than by the Owner. `config_minor` is LOW, so
a tier-2 record is reviewable after the fact and **never reaches the Board** — which is correct for tier 2
and was never stated, so the old table read as an escalation that silently does not escalate.

**NAMED W556 (P2.14 built).** The table below used the 0–5 numbering throughout, which is the scale
W549's own note says change_control does not have — the mapping was corrected and the VOCABULARY was
left, so the item body (corrected W535 to dispositions) and this table described the same bands in two
languages. That is how they drifted the first time. The DISPOSITION column is the name the code uses:
`agentic_core/horizon/muhasabah.py` DISPOSITIONS, which is what a round builds from. The tier column is
kept so an older reading still lands somewhere, and it is not the authority.

| Disposition (the code's name) | old tier | Example | `change_type` filed | Agency rank | Reaches the Board? |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `APPLIED_AND_LOGGED` | 0–1 | a wording fix in Horizon's own output, a new exclusion pattern | **none** — no change is filed | — (no change, so no rank) | no |
| `APPLIED_AND_RECORDED` | 2 | a routing weight, a new escalation trigger | `config_minor` | LOW | **no, by design** — reviewable after the fact, and the surface must not imply otherwise |
| `SUBMIT_ONLY` | 3–4 | a guardrail, a gate, a routing policy | `policy_amendment` | HIGH | **yes**, once a review approves it — and it may NOT be self-applied |
| `REFUSED` | 5 | faith content, the law domains, anything constitutional | **none** — surfaced to the Owner | — | no; Horizon may not reach for it at all |

**ONE ROW OF THAT TABLE CHANGED MEANING, and it is recorded rather than quietly swapped.** Tier 5 read
"`constitutional` / CRITICAL / a review may never approve it at all; the Owner decides". Horizon does not
file it: a CRITICAL change is never approved by a review, so filing one would put a record into the queue
that the mechanism Horizon has cannot resolve. The subject is REFUSED and surfaced to the Owner instead —
which is what the item body already said ("Horizon may not apply a guardrail, a gate, a schema, money,
faith content or the law domains") and what `FORBIDDEN_SUBJECTS` enforces.

**TWO FENCES THAT ARE NOT OPTIONAL, both measured against the code rather than inferred:**

1. **A lesson touching money is NOT FILED AS A CHANGE.** `submit_change` REFUSES `change_type:
   "economy_material"` and the three reserved `[economy] material …` title prefixes with HTTP 422, because
   the economy files its own materiality holds and keeps them current (Owner ruling, W463/W502). So a
   money-touching lesson is **surfaced to the Owner**, not submitted — a round that files it gets a 422,
   and a round that files it under some other type has routed a money decision around the gate that
   exists for it.
2. **`data_schema` is MEDIUM, not HIGH.** A store-schema lesson filed under it would not reach the Board.
   If a schema change is meant to be ratified, it is filed as `policy_amendment`; the type is chosen for
   the rank it carries, and the rank is read from `_TIER_MAP` rather than assumed.

Horizon may not apply a guardrail, a gate, a schema, money, faith content or the law domains.

The boundary is the same one the Owner already set for the platform: real-money rails, live keys,
production deploy and faith-content policy are Owner-gated and are not in any tier Horizon can apply.

---

## 7 · The four Owner decisions — ALL FOUR ARE RULED

These were design gaps, not engineering gaps. **All four have since been ruled, and nothing in
P2.11–P2.16 is blocked on the Owner any more** (FU-267 ruled 2026-09-27; FU-268, FU-269 and FU-270 ruled
2026-09-28). The rulings are recorded verbatim in `docs/FABLE_DELIVERY_PROMPT.md` beside P2.11 and are
constitution, not preference: a later round may not quietly widen the inbox, invent a route, or present an
absent list as a filled one.

Each decision is kept below with its question intact, because the question is what the ruling answers.
**The `Blocks:` lines below are HISTORICAL** — they record what was blocked before the ruling, not what is
blocked now.

1. **The node/station taxonomy.** The brief introduces a 0–9 "cosmic blueprint" and 25 "spiritual
   stations". Neither is in this repo's canon. The canon's closest structure — the 99-aspect Fitrah
   Spectrum — was *never enumerated*, and ruling A.9.5 forbids treating it as a measurement. Decision
   needed: (a) ratify a taxonomy as canon, to be used only as user-chosen labels and reflection prompts;
   (b) keep Horizon taxonomy-free (domain + stakes only); (c) defer. **Blocks:** the station field and
   any Suitcase virtue vocabulary. **Default if undecided: (b).**
   → **RULED (FU-267, 2026-09-27): (b) — Horizon stays TAXONOMY-FREE**, domain and stakes only. This
   governs P2.11 and P2.15 whenever they are taken.
2. **May the platform read the four desktop folders at all?** They are outside the repo, on OneDrive,
   and one of them contains a credentials file. Decision needed: read-only indexing with the exclusion
   rules of §2, per-path, plus whether the index may be committed (proposal: **no** — the index is local
   data, never committed, never sent anywhere). **Blocks:** P2.13.
   → **RULED (FU-268, 2026-09-28): AN EXPLICIT INBOX ONLY.** The platform indexes only what the Owner
   copies into a named inbox folder; the four archives themselves are not read. One of them holds a `.env`,
   and a narrower claim that is true beats a wider one resting on a skip list being complete. P2.13's
   coverage claim is over the inbox, and says so.
3. **Is a docx/pdf extractor to be installed?** Without one, the book folder and 4 of 9 `p3` files
   contribute nothing, and Horizon will say so. Installing `pypdf` / `python-docx` is a dependency
   decision. **Blocks:** any claim of coverage over those folders.
   → **RULED (FU-269, 2026-09-28): (a) — both are added to requirements.** `_pdf_docx_extractor()`
   (`agentic_core/ingestion/api.py`) already probes for them, so extraction begins working with no further
   code. **HALF-DELIVERED as measured in W514:** `python-docx` is in `requirements.txt` and **`pypdf` is
   absent entirely**, and neither imports in the local environment. Until the install lands a `.docx`/`.pdf`
   still answers NOT_EXTRACTED with its reason — which is the honest state the ruling said to keep, so this
   is a completeness gap and not a false claim.
4. **The distress-route list.** Real, current human routes for the Owner's jurisdiction, and who reviews
   them. The platform must not invent them. **Blocks:** guardrail 3 shipping as more than a refusal.
   → **RULED (FU-270, 2026-09-28): SHIP THE REFUSAL, LEAVE THE LIST UNFILLED.** The gate refuses and
   escalates now; the routes render as NOT SUPPLIED — never a default, never a placeholder, never a
   plausible-looking number a person in distress might dial. **P2.12 closes on its refusal paths** with the
   unfilled field visible on the surface; the list is supplied later with its reviewer.

---

## 8 · The plan items

| Item | What it delivers | Blocked by |
| :-- | :-- | :-- |
| **P2.11** | The Horizon kernel: `HorizonObservation`, `IntentRecord`, the three-state compression, the term-based decision, `intent.json`, and the middleware seam. Guarded so each state is reachable and asserted. | — |
| **P2.12** | The three guardrails with their coverage statements, attached to gaas.v5, with the fail-closed default and the refusal paths asserted. | §7.4 for the route list |
| **P2.13** | The asset genome over the four local paths: bounded scan, exclusion rules, three-state index, a manifest that states its own bounds, owned lexical search. | §7.2, §7.3 |
| **P2.14** | Systemic Muhasabah: `LessonRecord`, the friction hooks on the existing run paths, the candidate-cause discipline, and the tier routing into `change_control` — sharing P2.10's register shape. | P2.10 |
| **P2.15** | Accounting: `ConsumptionRecord` joined to runs (time, calls, provenance, stores read) and the Owner-declared fields, with nothing inferred. | — |
| **P2.16** | The companion surface: the record, its states, the escalations, the consumption, and the Owner's own entries — printing "not compressed" and "no station assigned" where that is the truth. | P2.11 |

Each item's acceptance is the same in shape as P2.10's: every state reachable and asserted by a guard,
and the mechanism's own limits stated on the surface rather than implied. **The risk each item must not
realise:** a Horizon that reports an alignment it did not evaluate, a knowledge base holding files it
never read, or a spiritual verdict about a person. That is the class this platform has spent twenty
rounds removing, and Horizon is the most tempting place in the system to re-introduce it.
